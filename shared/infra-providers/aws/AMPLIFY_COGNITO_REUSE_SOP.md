# AWS Amplify & Cognito Reuse SOP

<!-- File UUID: 8a3e2f1c-4b5d-4e9a-b7c8-9d0e1f2a3b4c -->

## Overview

This SOP documents common anti-patterns when deploying to AWS Amplify and Cognito, and provides solutions to ensure resource reuse, proper builds, and deployment verification.

---

## Problem Summary

| # | Problem | Impact | Solution |
|---|---------|--------|----------|
| 1 | New Amplify apps created instead of reusing | Orphaned apps, URL drift, quota exhaustion | Lookup by name first |
| 2 | New Cognito pools created instead of reusing | User data loss, broken auth | Import existing pools |
| 3 | GitHub integration used instead of S3 zip | Requires PAT, webhook setup, not CC-web compatible | Use S3 zip deployment |
| 4 | URLs not tested after deploy | Silent failures, broken deploys | Automated URL verification |
| 5 | Build artifacts in wrong directory | 404 errors, blank pages | Use correct baseDirectory |
| 6 | CDK includes hardcoded values | Non-portable, environment drift | Config-driven approach |

---

## Problem 1: New Amplify Apps Created Instead of Reusing

### Symptom
Each deployment creates a new Amplify app, resulting in:
- Multiple orphaned apps in the AWS console
- Different URLs each time
- Quota exhaustion (100 apps per region default)

### Root Cause
Scripts call `create_app()` without first checking if an app with the same name exists.

### Solution: Lookup-First Pattern

```python
def get_or_create_amplify_app(
    amplify_client,
    app_name: str,
    platform: str = 'WEB_COMPUTE'
) -> dict:
    """
    Find existing app by name or create new one.
    ALWAYS call this instead of create_app directly.
    """
    # Step 1: Search for existing app by name
    paginator = amplify_client.get_paginator('list_apps')
    for page in paginator.paginate():
        for app in page['apps']:
            if app['name'] == app_name:
                print(f"✓ Found existing app: {app['appId']}")
                return app

    # Step 2: Create only if not found
    print(f"Creating new app: {app_name}")
    response = amplify_client.create_app(
        name=app_name,
        platform=platform,
    )
    return response['app']
```

### CDK Pattern: Import Existing or Create

```typescript
// In CDK stack, use CfnApp.fromAppId to reference existing apps
interface AmplifyStackProps extends cdk.StackProps {
  existingAppId?: string;  // Pass existing app ID if known
}

// Check if app exists via SSM parameter or config
const existingAppId = ssm.StringParameter.valueForStringParameter(
  this,
  `/amplify/${appName}/app-id`
).toString();

if (existingAppId && existingAppId !== 'NONE') {
  // Reference existing app
  this.amplifyApp = amplify.CfnApp.fromAppId(this, 'ExistingApp', existingAppId);
} else {
  // Create new app and store ID
  this.amplifyApp = new amplify.CfnApp(this, 'NewApp', { ... });
  new ssm.StringParameter(this, 'AppIdParam', {
    parameterName: `/amplify/${appName}/app-id`,
    stringValue: this.amplifyApp.attrAppId,
  });
}
```

---

## Problem 2: New Cognito Pools Created Instead of Reusing

### Symptom
Each CDK deploy creates a new Cognito User Pool:
- Existing users cannot log in
- OAuth redirect URIs point to old pools
- Multiple orphaned pools accumulate

### Root Cause
CDK creates new resources by default. Cognito pools are NOT idempotent.

### Solution: Import Shared Cognito Pool

```typescript
// config/env.yaml - Reference shared pool
auth:
  userPoolId: us-east-1_XXXXXXXXX  # Existing shared pool ID
  domain: auth.myapp.com           # Existing domain

// In CDK stack - IMPORT, don't create
const userPool = cognito.UserPool.fromUserPoolId(
  this,
  'SharedUserPool',
  config.auth.userPoolId
);

// Only create app client (NOT the pool itself)
const appClient = userPool.addClient('MyAppClient', {
  userPoolClientName: `${appName}-${environment}`,
  // ... oauth config
});
```

### Cognito Resource Hierarchy

```
SHARED (create once, import everywhere):
├── User Pool (us-east-1_XXXXXXXXX)
├── Domain (auth.myapp.com)
└── Identity Providers (Google, GitHub)

PER-APP (create for each app):
├── App Client (unique per app)
└── Callback URLs (per environment)
```

### Pre-Deployment Check

```bash
#!/bin/bash
# scripts/check-cognito-pool.sh

POOL_ID="${COGNITO_USER_POOL_ID:-}"

if [ -z "$POOL_ID" ]; then
  echo "ERROR: COGNITO_USER_POOL_ID not set"
  echo "Set it to an existing pool ID to avoid creating duplicates"
  exit 1
fi

# Verify pool exists
aws cognito-idp describe-user-pool --user-pool-id "$POOL_ID" > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "ERROR: User pool $POOL_ID does not exist"
  exit 1
fi

echo "✓ Using existing Cognito pool: $POOL_ID"
```

---

## Problem 3: GitHub Integration Instead of S3 Zip

### Symptom
- Deployments require GitHub PAT with repo access
- Webhook setup needed
- Not compatible with Claude Code Web (no git push capability)
- Branch management complexity

### Root Cause
Current SOPs default to `repository` + `accessToken` pattern.

### Solution: S3 Zip Deployment Pattern

```python
import boto3
import zipfile
import tempfile
import urllib.request

def deploy_via_s3_zip(
    amplify_client,
    app_id: str,
    branch_name: str,
    build_dir: str,  # Path to built artifacts (dist/, .next/, build/)
) -> str:
    """
    Deploy pre-built artifacts via S3 presigned URL.
    Works in Claude Code Web without GitHub integration.
    """
    # Step 1: Create deployment (gets presigned URL)
    response = amplify_client.create_deployment(
        appId=app_id,
        branchName=branch_name
    )
    zip_url = response['zipUploadUrl']
    job_id = response.get('jobId')

    # Step 2: Create zip of build artifacts
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
        with zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(build_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, build_dir)
                    zf.write(file_path, arc_name)
        zip_path = tmp.name

    # Step 3: Upload zip to presigned URL
    with open(zip_path, 'rb') as f:
        req = urllib.request.Request(zip_url, data=f.read(), method='PUT')
        req.add_header('Content-Type', 'application/zip')
        urllib.request.urlopen(req)

    # Step 4: Start deployment
    response = amplify_client.start_deployment(
        appId=app_id,
        branchName=branch_name,
        jobId=job_id
    )

    return response['jobSummary']['jobId']
```

### When to Use Each Approach

| Scenario | Approach |
|----------|----------|
| Claude Code Web | S3 zip (no git available) |
| CI/CD pipeline | Git integration |
| Manual deploy | S3 zip |
| Auto-deploy on push | Git integration |
| Monorepo | Git integration with appRoot |

---

## Problem 4: URLs Not Tested After Deploy

### Symptom
- Deploys report success but site returns 404/503
- No visibility into actual deployment health
- Users report issues before developers notice

### Root Cause
Deployment scripts check job status but not actual URL availability.

### Solution: Post-Deployment URL Verification

```python
import urllib.request
import time

def verify_deployment_url(
    url: str,
    expected_status: int = 200,
    max_retries: int = 6,
    retry_delay: int = 10,
    expected_content: str = None,
) -> bool:
    """
    Verify deployed URL is accessible and returning expected content.
    ALWAYS call this after deployment completes.
    """
    print(f"Verifying URL: {url}")

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, method='GET')
            req.add_header('User-Agent', 'Amplify-Deploy-Verify/1.0')

            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.status
                content = response.read().decode('utf-8', errors='ignore')

                if status == expected_status:
                    if expected_content and expected_content not in content:
                        print(f"  ⚠ Status {status} but missing expected content")
                    else:
                        print(f"  ✓ URL verified: {status}")
                        return True
                else:
                    print(f"  ✗ Unexpected status: {status} (expected {expected_status})")

        except Exception as e:
            print(f"  Attempt {attempt + 1}/{max_retries}: {e}")

        if attempt < max_retries - 1:
            time.sleep(retry_delay)

    print(f"  ✗ URL verification FAILED after {max_retries} attempts")
    return False


# Usage in deploy script
def deploy_and_verify(app_id: str, branch_name: str, build_dir: str):
    job_id = deploy_via_s3_zip(amplify, app_id, branch_name, build_dir)

    # Wait for job to complete
    wait_for_job(amplify, app_id, branch_name, job_id)

    # Get URL
    app = amplify.get_app(appId=app_id)['app']
    url = f"https://{branch_name}.{app['defaultDomain']}"

    # CRITICAL: Verify URL is working
    if not verify_deployment_url(url, expected_content='<!DOCTYPE html>'):
        raise Exception(f"Deployment verification failed: {url}")

    print(f"✓ Deployment verified: {url}")
```

### Verification Checklist

```python
VERIFICATION_CHECKS = [
    # Basic availability
    {'url': '/', 'status': 200},

    # Static assets
    {'url': '/_next/static/', 'status': 200},

    # API routes (if applicable)
    {'url': '/api/health', 'status': 200},

    # Auth callback (if using OAuth)
    {'url': '/auth/callback', 'status': 200},  # or 302 redirect
]

def run_verification_suite(base_url: str) -> bool:
    results = []
    for check in VERIFICATION_CHECKS:
        url = f"{base_url}{check['url']}"
        result = verify_deployment_url(url, expected_status=check['status'])
        results.append(result)

    return all(results)
```

---

## Problem 5: Build Artifacts in Wrong Directory

### Symptom
- Deployed site shows 404 or blank page
- Build succeeds but artifacts not found
- Works locally but not on Amplify

### Root Cause
Amplify buildspec `baseDirectory` doesn't match actual build output.

### Framework-Specific Build Directories

| Framework | Build Command | Output Directory | baseDirectory |
|-----------|---------------|------------------|---------------|
| Next.js (SSR) | `npm run build` | `.next/` | `.next` |
| Next.js (Static) | `npm run build && npm run export` | `out/` | `out` |
| Vite | `npm run build` | `dist/` | `dist` |
| Create React App | `npm run build` | `build/` | `build` |
| Vue CLI | `npm run build` | `dist/` | `dist` |
| Angular | `ng build` | `dist/{project}/` | `dist/{project}` |

### Correct Buildspec Examples

**Next.js SSR:**
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next  # NOT dist/
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
```

**Vite/React:**
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: dist  # Vite outputs to dist/
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

### Pre-Deployment Build Verification

```bash
#!/bin/bash
# scripts/verify-build.sh

FRAMEWORK="${1:-nextjs}"

case "$FRAMEWORK" in
  nextjs)
    BUILD_DIR=".next"
    REQUIRED_FILE=".next/BUILD_ID"
    ;;
  vite)
    BUILD_DIR="dist"
    REQUIRED_FILE="dist/index.html"
    ;;
  react)
    BUILD_DIR="build"
    REQUIRED_FILE="build/index.html"
    ;;
esac

if [ ! -d "$BUILD_DIR" ]; then
  echo "ERROR: Build directory '$BUILD_DIR' not found"
  echo "Run 'npm run build' first"
  exit 1
fi

if [ ! -f "$REQUIRED_FILE" ]; then
  echo "ERROR: Required file '$REQUIRED_FILE' not found"
  echo "Build may have failed or used wrong output directory"
  exit 1
fi

echo "✓ Build verified: $BUILD_DIR"
ls -la "$BUILD_DIR"
```

---

## Problem 6: CDK Includes Hardcoded Values

### Symptom
- Stacks fail when deployed to different accounts/regions
- Environment-specific values mixed with infrastructure code
- Cannot reuse stacks across projects

### Root Cause
Values like app IDs, domains, account IDs embedded directly in CDK code.

### Anti-Pattern Examples

```typescript
// ❌ BAD: Hardcoded values
const amplifyApp = new amplify.CfnApp(this, 'App', {
  name: 'my-app',  // Hardcoded
  environmentVariables: [
    { name: 'API_URL', value: 'https://api.myapp.com' },  // Hardcoded
    { name: 'COGNITO_POOL', value: 'us-east-1_ABC123' },  // Hardcoded
  ],
});

// ❌ BAD: Hardcoded monorepo path
buildSpec: `
  - cd projects/personal/active/ppm-personal-priority-manager-p1m2n/frontend
`
```

### Solution: Config-Driven CDK

**Step 1: Create config schema**

```typescript
// infra/config/schema.ts
export interface EnvConfig {
  stage: 'dev' | 'staging' | 'prod';
  projectPath: string;  // e.g., 'projects/personal/active/my-app'

  domain: {
    rootDomain: string;      // e.g., 'app.example.com'
    hostedZone: string;      // e.g., 'example.com'
  };

  auth: {
    userPoolId: string;      // Existing pool ID
    domain: string;          // Existing Cognito domain
  };

  github?: {
    owner: string;
    repo: string;
    branch: string;
  };
}
```

**Step 2: Environment-specific config files**

```yaml
# infra/config/personal.yaml
stage: prod
projectPath: projects/personal/active/ppm

domain:
  rootDomain: ppm.b.lfg.new
  hostedZone: b.lfg.new

auth:
  userPoolId: ${SSM:/shared-auth/personal/user-pool-id}
  domain: ${SSM:/shared-auth/personal/cognito-domain}

github:
  owner: andrewhopper
  repo: protoflow
  branch: main
```

**Step 3: Config-driven stack**

```typescript
// ✅ GOOD: All values from config
const amplifyApp = new amplify.CfnApp(this, 'App', {
  name: `${config.projectPath.split('/').pop()}-${config.stage}`,
  buildSpec: this.generateBuildSpec(config.projectPath),
  environmentVariables: [
    { name: 'NEXT_PUBLIC_COGNITO_USER_POOL_ID', value: config.auth.userPoolId },
    { name: 'NEXT_PUBLIC_COGNITO_DOMAIN', value: config.auth.domain },
    { name: 'NEXT_PUBLIC_DOMAIN', value: config.domain.rootDomain },
  ],
});

// Generate buildspec from config (no hardcoded paths)
private generateBuildSpec(projectPath: string): string {
  return `version: 1
applications:
  - frontend:
      phases:
        preBuild:
          commands:
            - cd ${projectPath}/frontend
            - npm ci
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: ${projectPath}/frontend/.next
        files:
          - '**/*'
    appRoot: ${projectPath}/frontend
`;
}
```

### Config Resolution Pattern

```typescript
// infra/config/load-config.ts
import * as ssm from 'aws-cdk-lib/aws-ssm';

export function resolveConfig(raw: EnvConfig, stack: cdk.Stack): ResolvedConfig {
  // Resolve SSM parameter references
  const resolved = { ...raw };

  for (const [key, value] of Object.entries(raw)) {
    if (typeof value === 'string' && value.startsWith('${SSM:')) {
      const paramName = value.slice(6, -1);
      resolved[key] = ssm.StringParameter.valueForStringParameter(stack, paramName);
    }
  }

  return resolved;
}
```

---

## Complete Deployment Script

```python
#!/usr/bin/env python3
"""
Amplify deployment script following reuse SOP.
Handles: app lookup, S3 zip deploy, URL verification.
"""

import boto3
import os
import sys
import time
import zipfile
import tempfile
import urllib.request
from pathlib import Path

class AmplifyDeployer:
    def __init__(self, region: str = 'us-east-1'):
        self.amplify = boto3.client('amplify', region_name=region)
        self.region = region

    def get_or_create_app(self, name: str, platform: str = 'WEB_COMPUTE') -> dict:
        """Find existing app or create new one."""
        # Search existing
        paginator = self.amplify.get_paginator('list_apps')
        for page in paginator.paginate():
            for app in page['apps']:
                if app['name'] == name:
                    print(f"✓ Reusing existing app: {app['appId']}")
                    return app

        # Create new
        print(f"Creating new app: {name}")
        response = self.amplify.create_app(name=name, platform=platform)
        return response['app']

    def ensure_branch(self, app_id: str, branch_name: str) -> dict:
        """Create branch if it doesn't exist."""
        try:
            response = self.amplify.get_branch(appId=app_id, branchName=branch_name)
            return response['branch']
        except self.amplify.exceptions.NotFoundException:
            response = self.amplify.create_branch(
                appId=app_id,
                branchName=branch_name,
                enableAutoBuild=False
            )
            return response['branch']

    def deploy_zip(self, app_id: str, branch_name: str, build_dir: str) -> str:
        """Deploy pre-built artifacts via S3 zip."""
        # Create deployment
        response = self.amplify.create_deployment(appId=app_id, branchName=branch_name)
        zip_url = response['zipUploadUrl']
        job_id = response.get('jobId')

        # Create and upload zip
        print(f"Packaging {build_dir}...")
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
            with zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as zf:
                build_path = Path(build_dir)
                for file_path in build_path.rglob('*'):
                    if file_path.is_file():
                        arc_name = file_path.relative_to(build_path)
                        zf.write(file_path, arc_name)

            print("Uploading to Amplify...")
            with open(tmp.name, 'rb') as f:
                req = urllib.request.Request(zip_url, data=f.read(), method='PUT')
                req.add_header('Content-Type', 'application/zip')
                urllib.request.urlopen(req)

        # Start deployment
        response = self.amplify.start_deployment(appId=app_id, branchName=branch_name, jobId=job_id)
        return response['jobSummary']['jobId']

    def wait_for_job(self, app_id: str, branch_name: str, job_id: str, timeout: int = 600) -> str:
        """Wait for deployment job to complete."""
        start = time.time()
        while time.time() - start < timeout:
            job = self.amplify.get_job(appId=app_id, branchName=branch_name, jobId=job_id)
            status = job['job']['summary']['status']
            print(f"  Status: {status}")

            if status in ['SUCCEED', 'FAILED', 'CANCELLED']:
                return status

            time.sleep(10)

        raise TimeoutError(f"Job did not complete within {timeout}s")

    def verify_url(self, url: str, retries: int = 6) -> bool:
        """Verify deployed URL is accessible."""
        for attempt in range(retries):
            try:
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'Amplify-Verify/1.0')
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        print(f"  ✓ URL verified: {url}")
                        return True
            except Exception as e:
                print(f"  Attempt {attempt + 1}/{retries}: {e}")
            time.sleep(10)

        return False

    def deploy(self, app_name: str, branch_name: str, build_dir: str) -> str:
        """Full deployment with verification."""
        # Step 1: Get or create app (REUSE existing)
        app = self.get_or_create_app(app_name)
        app_id = app['appId']

        # Step 2: Ensure branch exists
        self.ensure_branch(app_id, branch_name)

        # Step 3: Deploy via S3 zip (NOT GitHub)
        job_id = self.deploy_zip(app_id, branch_name, build_dir)
        print(f"Deployment started: {job_id}")

        # Step 4: Wait for completion
        status = self.wait_for_job(app_id, branch_name, job_id)
        if status != 'SUCCEED':
            raise Exception(f"Deployment failed: {status}")

        # Step 5: Verify URL (CRITICAL)
        url = f"https://{branch_name}.{app['defaultDomain']}"
        if not self.verify_url(url):
            raise Exception(f"URL verification failed: {url}")

        return url


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-name', required=True)
    parser.add_argument('--branch', default='main')
    parser.add_argument('--build-dir', required=True, help='Path to build artifacts (dist/, .next/, build/)')
    parser.add_argument('--region', default='us-east-1')
    args = parser.parse_args()

    deployer = AmplifyDeployer(region=args.region)
    url = deployer.deploy(args.app_name, args.branch, args.build_dir)
    print(f"\n✓ Deployed: {url}")
```

---

## Checklist

Before every Amplify/Cognito deployment:

- [ ] **App Reuse**: Using `get_or_create_app()` pattern (not blind `create_app`)
- [ ] **Cognito Reuse**: Importing existing pool via `fromUserPoolId()` (not creating new)
- [ ] **Deployment Method**: Using S3 zip for Claude Code Web (not GitHub integration)
- [ ] **Build Directory**: Correct `baseDirectory` for framework (.next/dist/build)
- [ ] **URL Verification**: `verify_url()` called after deploy completes
- [ ] **Config-Driven**: All values from config files (no hardcoded strings in CDK)
- [ ] **SSM Parameters**: Storing app IDs in SSM for future reuse

---

## Related Documentation

- [AMPLIFY_MONOREPO_DEPLOYMENT_SOP.md](./AMPLIFY_MONOREPO_DEPLOYMENT_SOP.md) - Git-based SSR deployment
- [AMPLIFY_CUSTOM_DOMAIN_SOP.md](./AMPLIFY_CUSTOM_DOMAIN_SOP.md) - Custom domain setup
- [shared/shared-auth-gateway/](../../shared-auth-gateway/) - Shared Cognito infrastructure
