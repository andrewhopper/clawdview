<!-- File UUID: 4f8b3e9a-7d2c-4e1b-9a5f-3c6d8e2f4a1b -->

# AWS Amplify Multi-Environment Deployment SOP

Deploy SPAs (React, Vite, static HTML) and Next.js apps to AWS Amplify with multi-environment branch deployments (dev, stage, prod) and custom Route53 domains.

**CRITICAL:** NEVER use S3 static hosting for microsites - ALWAYS use AWS Amplify.

---

## Quick Start

```bash
# Bootstrap infrastructure (one-time)
make infra-bootstrap

# Deploy all environments
make infra-deploy

# Deploy specific environment
make deploy-dev
make deploy-stage
make deploy-prod
```

**Domain Pattern:** `{env}-{project}.b.lfg.new`
- `dev-myapp.b.lfg.new`
- `stage-myapp.b.lfg.new`
- `prod-myapp.b.lfg.new`

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Prerequisites](#2-prerequisites)
3. [Project Structure](#3-project-structure)
4. [CDK Stack Implementation](#4-cdk-stack-implementation)
5. [Deployment Workflow](#5-deployment-workflow)
6. [Smoke Testing](#6-smoke-testing)
7. [Troubleshooting](#7-troubleshooting)
8. [Reference](#8-reference)

---

## 1. Architecture Overview

### 1.1 Multi-Environment Strategy

```
Repository (main branch)
│
├── dev branch     → Amplify Dev Environment    → dev-myapp.b.lfg.new
├── stage branch   → Amplify Stage Environment  → stage-myapp.b.lfg.new
└── prod branch    → Amplify Prod Environment   → prod-myapp.b.lfg.new
```

### 1.2 Deployment Flow

```
1. Developer commits to dev branch
2. Amplify auto-detects push and triggers build
3. Build runs (npm install → npm run build)
4. Artifacts deployed to CloudFront edge locations
5. Route53 CNAME updated (if first deploy)
6. Smoke test runs to verify deployment
7. Success notification sent
```

### 1.3 Platform Selection

| App Type | Amplify Platform | Build Output | Use Case |
|----------|------------------|--------------|----------|
| Static HTML | `WEB` | `index.html`, assets | Plain HTML/CSS/JS |
| React (Vite) | `WEB` | `dist/` folder | Client-side SPA |
| Next.js (SSG) | `WEB` | `out/` folder | Static export |
| Next.js (SSR) | `WEB_COMPUTE` | `.next/` folder | Server-side rendering |

---

## 2. Prerequisites

### 2.1 AWS Resources

1. **Route53 Hosted Zone** for `b.lfg.new`
   ```bash
   aws route53 list-hosted-zones --query "HostedZones[?Name=='b.lfg.new.'].Id" --output text
   ```

2. **GitHub Personal Access Token** (stored in Secrets Manager)
   ```bash
   aws secretsmanager get-secret-value --secret-id github-token --query SecretString --output text
   ```

3. **AWS Credentials** with permissions:
   - Amplify (create/update apps, branches, domains)
   - Route53 (manage DNS records)
   - Secrets Manager (read GitHub token)
   - ACM (implicit, for SSL certificates)

### 2.2 Repository Setup

1. **Branch Structure**
   ```bash
   git checkout -b dev
   git push -u origin dev

   git checkout -b stage
   git push -u origin stage

   git checkout -b prod
   git push -u origin prod
   ```

2. **Git Strategy Options**

   **Option A: Independent Branches** (recommended for active development)
   ```
   main ← dev ← feature branches
   main ← stage (manual merges from dev)
   main ← prod (manual merges from stage)
   ```

   **Option B: Promotion Flow** (recommended for production)
   ```
   feature → dev → stage → prod
   (automatic builds at each level)
   ```

### 2.3 Project Requirements

1. **Build Configuration**
   - `package.json` with `build` script
   - Build output directory (`dist/`, `out/`, `.next/`)
   - Node.js version specified (`.nvmrc` or in build spec)

2. **Environment Variables** (optional)
   - Create `.env.development`, `.env.staging`, `.env.production`
   - Reference in build spec via Amplify environment variables

---

## 3. Project Structure

### 3.1 Directory Layout

```
my-nextjs-app/
├── src/                          # Application code
├── public/                       # Static assets
├── infra/                        # Infrastructure as code
│   ├── app.ts                    # CDK app entry point
│   ├── stacks/
│   │   └── amplify-stack.ts      # Amplify stack definition
│   ├── deploys/                  # Capistrano-style releases
│   │   ├── releases/
│   │   │   ├── 20250103-1430/
│   │   │   │   ├── deploy.log
│   │   │   │   └── outputs.json
│   │   │   └── 20250103-1500/
│   │   ├── current -> releases/20250103-1500
│   │   └── shared/
│   └── requirements.txt          # CDK dependencies
├── Makefile                      # Deployment automation
├── amplify.yml                   # Amplify build spec
├── package.json
└── .env.example
```

### 3.2 Amplify Build Spec

**For Static Sites / React / Vite:**
```yaml
# amplify.yml
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
    baseDirectory: dist
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

**For Next.js SSR:**
```yaml
# amplify.yml
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
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
```

**For Monorepo:**
```yaml
# amplify.yml
version: 1
applications:
  - appRoot: frontend
    frontend:
      phases:
        preBuild:
          commands:
            - npm ci
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: dist
        files:
          - '**/*'
      cache:
        paths:
          - node_modules/**/*
```

### 3.3 Environment Variables

Set in CDK stack or Amplify Console:

```typescript
environmentVariables: {
  // Node.js version
  '_LIVE_UPDATES': '[{"pkg":"node","type":"nvm","version":"20"}]',

  // Monorepo root (if applicable)
  'AMPLIFY_MONOREPO_APP_ROOT': 'frontend',

  // Custom env vars
  'VITE_API_URL': 'https://api.example.com',
  'NEXT_PUBLIC_APP_ENV': 'production'
}
```

---

## 4. CDK Stack Implementation

### 4.1 Amplify Stack (TypeScript)

```typescript
// infra/stacks/amplify-stack.ts
// File UUID: 8a2c4e6f-9b1d-4c3e-8f5a-7d9e2b4c6a8f

import * as cdk from 'aws-cdk-lib';
import * as amplify from 'aws-cdk-lib/aws-amplify';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';

export interface AmplifyStackProps extends cdk.StackProps {
  projectId: string;           // e.g., 'myapp'
  repository: string;          // e.g., 'https://github.com/owner/repo'
  hostedZoneName: string;      // e.g., 'b.lfg.new'
  platform: 'WEB' | 'WEB_COMPUTE';  // WEB for static/SSG, WEB_COMPUTE for SSR
  appRoot?: string;            // Optional: for monorepo
  buildSpec?: string;          // Optional: custom build spec
}

export class AmplifyStack extends cdk.Stack {
  public readonly app: amplify.CfnApp;
  public readonly branches: Map<string, amplify.CfnBranch> = new Map();

  constructor(scope: Construct, id: string, props: AmplifyStackProps) {
    super(scope, id, props);

    // Retrieve GitHub token from Secrets Manager
    const githubToken = secretsmanager.Secret.fromSecretNameV2(
      this,
      'GitHubToken',
      'github-token'
    );

    // Default build spec
    const defaultBuildSpec = props.buildSpec || `
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
    baseDirectory: ${props.platform === 'WEB_COMPUTE' ? '.next' : 'dist'}
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
`;

    // Create Amplify app
    this.app = new amplify.CfnApp(this, 'AmplifyApp', {
      name: props.projectId,
      repository: props.repository,
      accessToken: githubToken.secretValue.unsafeUnwrap(),
      platform: props.platform,
      buildSpec: defaultBuildSpec,
      iamServiceRole: undefined, // Use default service role
      environmentVariables: [
        {
          name: '_LIVE_UPDATES',
          value: '[{"pkg":"node","type":"nvm","version":"20"}]'
        },
        ...(props.appRoot ? [{
          name: 'AMPLIFY_MONOREPO_APP_ROOT',
          value: props.appRoot
        }] : [])
      ]
    });

    // Get Route53 hosted zone
    const hostedZone = route53.HostedZone.fromLookup(this, 'HostedZone', {
      domainName: props.hostedZoneName
    });

    // Define environments
    const environments = [
      { name: 'dev', stage: 'DEVELOPMENT' },
      { name: 'stage', stage: 'BETA' },
      { name: 'prod', stage: 'PRODUCTION' }
    ];

    // Create branches
    environments.forEach(env => {
      const branch = new amplify.CfnBranch(this, `Branch-${env.name}`, {
        appId: this.app.attrAppId,
        branchName: env.name,
        stage: env.stage as any,
        enableAutoBuild: true,
        enablePullRequestPreview: false,
        ...(props.appRoot && {
          environmentVariables: [{
            name: 'AMPLIFY_MONOREPO_APP_ROOT',
            value: props.appRoot
          }]
        })
      });

      this.branches.set(env.name, branch);
    });

    // Create custom domain with all subdomains
    const domain = new amplify.CfnDomain(this, 'CustomDomain', {
      appId: this.app.attrAppId,
      domainName: props.hostedZoneName,
      subDomainSettings: environments.map(env => ({
        prefix: `${env.name}-${props.projectId}`,
        branchName: env.name
      })),
      enableAutoSubDomain: false
    });

    // Add dependency to ensure branches exist before domain
    environments.forEach(env => {
      const branch = this.branches.get(env.name)!;
      domain.addDependency(branch);
    });

    // Outputs
    environments.forEach(env => {
      new cdk.CfnOutput(this, `Url-${env.name}`, {
        value: `https://${env.name}-${props.projectId}.${props.hostedZoneName}`,
        description: `${env.name.toUpperCase()} environment URL`
      });

      new cdk.CfnOutput(this, `AmplifyUrl-${env.name}`, {
        value: `https://${env.name}.${this.app.attrDefaultDomain}`,
        description: `${env.name.toUpperCase()} Amplify default URL`
      });
    });

    new cdk.CfnOutput(this, 'AppId', {
      value: this.app.attrAppId,
      description: 'Amplify App ID'
    });
  }
}
```

### 4.2 CDK App Entry Point

```typescript
// infra/app.ts
#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { AmplifyStack } from './stacks/amplify-stack';

const app = new cdk.App();

new AmplifyStack(app, 'MyAppAmplifyStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'us-east-1'
  },
  projectId: 'myapp',
  repository: 'https://github.com/yourusername/yourrepo',
  hostedZoneName: 'b.lfg.new',
  platform: 'WEB', // or 'WEB_COMPUTE' for Next.js SSR
  // appRoot: 'frontend', // Uncomment for monorepo
});
```

### 4.3 CDK Dependencies

```json
// infra/package.json
{
  "name": "infra",
  "version": "1.0.0",
  "scripts": {
    "build": "tsc",
    "cdk": "cdk"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "aws-cdk": "^2.150.0",
    "typescript": "^5.3.0"
  },
  "dependencies": {
    "aws-cdk-lib": "^2.150.0",
    "constructs": "^10.3.0",
    "source-map-support": "^0.5.21"
  }
}
```

---

## 5. Deployment Workflow

### 5.1 Makefile Targets

```makefile
# Makefile
.PHONY: infra-bootstrap infra-deploy deploy-dev deploy-stage deploy-prod smoke-test

TIMESTAMP := $(shell date +%Y%m%d-%H%M)
RELEASES_DIR := infra/deploys/releases
RELEASE_DIR := $(RELEASES_DIR)/$(TIMESTAMP)
CURRENT_LINK := infra/deploys/current
KEEP_RELEASES := 5

PROJECT_ID := myapp
HOSTED_ZONE := b.lfg.new

# Bootstrap CDK (one-time)
infra-bootstrap:
	@echo "Bootstrapping CDK..."
	@mkdir -p $(RELEASE_DIR)
	cd infra && npm install
	cd infra && npx cdk bootstrap 2>&1 | tee ../$(RELEASE_DIR)/deploy.log

# Deploy infrastructure
infra-deploy:
	@echo "Deploying Amplify infrastructure to $(RELEASE_DIR)..."
	@mkdir -p $(RELEASE_DIR) infra/deploys/shared
	cd infra && npx cdk deploy --all --require-approval never --outputs-file ../$(RELEASE_DIR)/outputs.json 2>&1 | tee ../$(RELEASE_DIR)/deploy.log
	@ln -sfn releases/$(TIMESTAMP) $(CURRENT_LINK)
	@echo '{"timestamp":"$(TIMESTAMP)","status":"deployed"}' > $(RELEASE_DIR)/manifest.json
	@echo "✓ Infrastructure deployed: $(RELEASE_DIR)"
	@# Cleanup old releases (keep last N)
	@cd $(RELEASES_DIR) && ls -t | tail -n +$$(($(KEEP_RELEASES)+1)) | xargs -r rm -rf
	@echo "⏳ Waiting 30s for Amplify apps to initialize..."
	@sleep 30
	@echo "✓ Ready for environment deployments"

# Deploy dev environment
deploy-dev:
	@echo "Deploying to dev..."
	git push origin dev
	@$(MAKE) smoke-test ENV=dev

# Deploy stage environment
deploy-stage:
	@echo "Deploying to stage..."
	git push origin stage
	@$(MAKE) smoke-test ENV=stage

# Deploy prod environment
deploy-prod:
	@echo "Deploying to prod..."
	git push origin prod
	@$(MAKE) smoke-test ENV=prod

# Smoke test (verifies deployment)
smoke-test:
	@echo "Running smoke test for $(ENV)..."
	@EXPECTED_GIT_HASH=$$(git rev-parse --short HEAD) \
	APP_URL=https://$(ENV)-$(PROJECT_ID).$(HOSTED_ZONE) \
	python3 infra/scripts/smoke-test.py
	@echo "✓ Smoke test passed for $(ENV)"

# Destroy infrastructure
infra-destroy:
	@echo "⚠️  WARNING: This will destroy all Amplify apps and custom domains"
	@read -p "Type 'destroy' to confirm: " confirm && [ "$$confirm" = "destroy" ]
	@mkdir -p $(RELEASE_DIR)
	cd infra && npx cdk destroy --all --force 2>&1 | tee ../$(RELEASE_DIR)/destroy.log
```

### 5.2 Initial Deployment

```bash
# 1. Bootstrap (one-time)
make infra-bootstrap

# 2. Deploy infrastructure (creates Amplify app + branches + domains)
make infra-deploy

# 3. Configure Route53 DNS records (see section 5.3)
# After infra-deploy, CDK outputs will show required DNS records

# 4. Deploy to environments
make deploy-dev
make deploy-stage
make deploy-prod
```

### 5.3 DNS Configuration

**IMPORTANT:** After first `make infra-deploy`, you must add DNS records to Route53.

**Automated DNS Setup (Recommended):**

```python
# infra/scripts/setup-dns.py
import boto3
import json

with open('infra/deploys/current/outputs.json') as f:
    outputs = json.load(f)

amplify = boto3.client('amplify', region_name='us-east-1')
route53 = boto3.client('route53')

app_id = outputs['MyAppAmplifyStack']['AppId']
hosted_zone_id = 'Z1234567890ABC'  # Get from: aws route53 list-hosted-zones

# Get domain association
domain = amplify.get_domain_association(
    appId=app_id,
    domainName='b.lfg.new'
)

# Parse and create DNS records
changes = []

# Certificate validation record
cert_record = domain['domainAssociation']['certificateVerificationDNSRecord']
parts = cert_record.split()
changes.append({
    'Action': 'UPSERT',
    'ResourceRecordSet': {
        'Name': parts[0],
        'Type': 'CNAME',
        'TTL': 300,
        'ResourceRecords': [{'Value': parts[2]}]
    }
})

# Subdomain records for each environment
for subdomain in domain['domainAssociation']['subDomains']:
    dns_record = subdomain['dnsRecord'].split()
    changes.append({
        'Action': 'UPSERT',
        'ResourceRecordSet': {
            'Name': f"{dns_record[0]}.b.lfg.new",
            'Type': 'CNAME',
            'TTL': 300,
            'ResourceRecords': [{'Value': dns_record[2]}]
        }
    })

# Apply changes
route53.change_resource_record_sets(
    HostedZoneId=hosted_zone_id,
    ChangeBatch={'Changes': changes}
)

print("✓ DNS records created")
print("⏳ SSL certificate provisioning takes 10-30 minutes")
```

**Run DNS setup:**
```bash
python3 infra/scripts/setup-dns.py
```

### 5.4 Ongoing Deployments

After initial setup, deployments are automatic:

```bash
# Make changes to code
git add .
git commit -m "feat: add new feature"

# Deploy to dev
git push origin dev
# Amplify auto-builds and deploys to dev-myapp.b.lfg.new

# Promote to stage
git checkout stage
git merge dev
git push origin stage
# Amplify auto-builds and deploys to stage-myapp.b.lfg.new

# Promote to prod
git checkout prod
git merge stage
git push origin prod
# Amplify auto-builds and deploys to prod-myapp.b.lfg.new
```

---

## 6. Smoke Testing

### 6.1 Git Hash Verification

**CRITICAL:** Every deployment MUST verify the deployed git hash matches the expected version.

**Inject git hash at build time:**

```yaml
# amplify.yml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
        - export GIT_HASH=$(git rev-parse --short HEAD)
        - echo "Building commit $GIT_HASH"
    build:
      commands:
        - npm run build
```

**Expose in app:**

```html
<!-- public/index.html or generated HTML -->
<!DOCTYPE html>
<html>
<head>
  <meta name="git-hash" content="__GIT_HASH__">
</head>
```

```javascript
// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  define: {
    __GIT_HASH__: JSON.stringify(process.env.GIT_HASH || 'dev')
  }
});
```

### 6.2 Smoke Test Script

```python
# infra/scripts/smoke-test.py
#!/usr/bin/env python3
"""
Post-deploy smoke test - verifies deployment success

Usage:
  EXPECTED_GIT_HASH=abc1234 APP_URL=https://dev-myapp.b.lfg.new python3 smoke-test.py
"""

import os
import sys
import requests
from bs4 import BeautifulSoup

def smoke_test():
    app_url = os.environ['APP_URL']
    expected_hash = os.environ['EXPECTED_GIT_HASH']

    print(f"🔍 Testing {app_url}")
    print(f"📌 Expected git hash: {expected_hash}")

    # Verify page loads
    response = requests.get(app_url, timeout=10)
    if response.status_code != 200:
        print(f"❌ HTTP {response.status_code}")
        sys.exit(1)

    # Extract git hash from meta tag
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find('meta', {'name': 'git-hash'})

    if not meta_tag:
        print("⚠️  No git-hash meta tag found (check build config)")
        sys.exit(1)

    deployed_hash = meta_tag.get('content')

    print(f"📦 Deployed git hash: {deployed_hash}")

    if deployed_hash != expected_hash:
        print(f"❌ Hash mismatch! Expected {expected_hash}, got {deployed_hash}")
        sys.exit(1)

    print("✅ Smoke test passed")
    print(f"✓ Correct version deployed: {deployed_hash}")
    return 0

if __name__ == '__main__':
    try:
        sys.exit(smoke_test())
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        sys.exit(1)
```

### 6.3 Playwright Smoke Test (Recommended)

```typescript
// tests/smoke.spec.ts
import { test, expect } from '@playwright/test';

test('smoke test - page renders and git hash matches', async ({ page }) => {
  const expectedHash = process.env.EXPECTED_GIT_HASH!;
  const appUrl = process.env.APP_URL!;

  await page.goto(appUrl);

  // Verify page renders
  await expect(page.locator('body')).toBeVisible();

  // Verify no error boundary
  await expect(page.locator('[data-testid="error-boundary"]')).not.toBeVisible();

  // Verify git hash matches
  const gitHash = await page.getAttribute('meta[name="git-hash"]', 'content');
  expect(gitHash).toBe(expectedHash);

  console.log(`✅ Deployed version: ${gitHash}`);
});
```

**Run Playwright test:**
```bash
EXPECTED_GIT_HASH=$(git rev-parse --short HEAD) \
APP_URL=https://dev-myapp.b.lfg.new \
npx playwright test tests/smoke.spec.ts
```

---

## 7. Troubleshooting

### 7.1 Common Issues

#### Issue: "Repository not found" or "Bad credentials"

**Cause:** GitHub token is expired or doesn't have correct permissions

**Fix:**
```bash
# Generate new GitHub token with scopes: repo, admin:repo_hook
# Update in Secrets Manager
aws secretsmanager update-secret \
  --secret-id github-token \
  --secret-string "ghp_new_token_here"

# Re-deploy CDK stack
make infra-deploy
```

#### Issue: Build succeeds but site returns 404

**Cause:** Incorrect artifact `baseDirectory` in `amplify.yml`

**Fix:**
```yaml
# Check your build output directory
artifacts:
  baseDirectory: dist  # For Vite, React
  # baseDirectory: out   # For Next.js SSG
  # baseDirectory: .next # For Next.js SSR
```

#### Issue: SSL certificate stuck on "Pending"

**Cause:** Missing DNS validation CNAME record

**Fix:**
```bash
# Run DNS setup script
python3 infra/scripts/setup-dns.py

# Or manually add record from Amplify Console
aws amplify get-domain-association \
  --app-id <APP_ID> \
  --domain-name b.lfg.new \
  --query 'domainAssociation.certificateVerificationDNSRecord'
```

#### Issue: Smoke test fails with hash mismatch

**Cause:** Old CDN cache or build not triggered

**Fix:**
```bash
# Trigger manual build
aws amplify start-job \
  --app-id <APP_ID> \
  --branch-name dev \
  --job-type RELEASE

# Wait for build to complete (5-10 minutes)
# Then re-run smoke test
```

#### Issue: "Cannot modify app connected to repository" error

**Cause:** Trying to change platform type after Git connection

**Fix:**
```bash
# Delete and recreate app
aws amplify delete-app --app-id <APP_ID>
make infra-deploy
```

### 7.2 Debugging Build Failures

**View build logs:**
```bash
# Get latest job ID
aws amplify list-jobs --app-id <APP_ID> --branch-name dev \
  --query 'jobSummaries[0].jobId' --output text

# View logs
aws amplify get-job --app-id <APP_ID> --branch-name dev --job-id <JOB_ID>
```

**Test build locally:**
```bash
# Use same Node version as Amplify (20.x)
nvm use 20

# Run build
npm ci
npm run build

# Verify output directory
ls -la dist/  # or .next/, out/
```

### 7.3 Domain Status Reference

| Status | Meaning | Action |
|--------|---------|--------|
| `CREATING` | Setting up domain | Wait |
| `AWAITING_APP_CNAME` | Need DNS records | Run setup-dns.py |
| `PENDING_VERIFICATION` | Validating SSL cert | Wait 10-30 min |
| `PENDING_DEPLOYMENT` | Deploying to edge | Wait |
| `AVAILABLE` | Ready | Done! |
| `FAILED` | Error occurred | Check `statusReason` |

**Check domain status:**
```bash
aws amplify get-domain-association \
  --app-id <APP_ID> \
  --domain-name b.lfg.new \
  --query 'domainAssociation.domainStatus'
```

---

## 8. Reference

### 8.1 Environment Variables

Set these in CDK stack or Amplify Console:

| Variable | Purpose | Example |
|----------|---------|---------|
| `_LIVE_UPDATES` | Node.js version | `[{"pkg":"node","type":"nvm","version":"20"}]` |
| `AMPLIFY_MONOREPO_APP_ROOT` | Monorepo subdirectory | `frontend` |
| `VITE_API_URL` | Frontend API endpoint | `https://api.example.com` |
| `NEXT_PUBLIC_APP_ENV` | Next.js environment | `production` |

### 8.2 Amplify CLI Commands

```bash
# List all apps
aws amplify list-apps --query 'apps[*].[name,appId,defaultDomain]' --output table

# Get app details
aws amplify get-app --app-id <APP_ID>

# List branches
aws amplify list-branches --app-id <APP_ID> \
  --query 'branches[*].[branchName,displayName,stage]' --output table

# Trigger build
aws amplify start-job --app-id <APP_ID> --branch-name dev --job-type RELEASE

# Get build status
aws amplify get-job --app-id <APP_ID> --branch-name dev --job-id <JOB_ID> \
  --query 'job.summary.status'

# Delete app
aws amplify delete-app --app-id <APP_ID>
```

### 8.3 Route53 Helper Script

```python
# infra/scripts/get-hosted-zone-id.py
import boto3

route53 = boto3.client('route53')
zones = route53.list_hosted_zones()['HostedZones']

for zone in zones:
    if zone['Name'] == 'b.lfg.new.':
        print(zone['Id'].split('/')[-1])
        break
```

```bash
python3 infra/scripts/get-hosted-zone-id.py
# Output: Z1234567890ABC
```

### 8.4 Project Examples

See these projects for reference implementations:

- **Static SPA:** `projects/personal/fake-image-detector-38b09/`
- **Next.js SSR:** `projects/personal/active/ppm-personal-priority-manager-p1m2n/`
- **Monorepo:** `projects/shared/proto-audio-notetaker-4bdf7-001/`

### 8.5 Related Documentation

- [AMPLIFY_CUSTOM_DOMAIN_SOP.md](./AMPLIFY_CUSTOM_DOMAIN_SOP.md) - Single-environment domain setup
- [AMPLIFY_MONOREPO_DEPLOYMENT_SOP.md](./AMPLIFY_MONOREPO_DEPLOYMENT_SOP.md) - Monorepo Git deployments
- [AMPLIFY_COGNITO_REUSE_SOP.md](./AMPLIFY_COGNITO_REUSE_SOP.md) - Shared Cognito integration
- [AWS Amplify Hosting Docs](https://docs.aws.amazon.com/amplify/latest/userguide/)
- [CDK Amplify Construct](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_amplify-readme.html)

### 8.6 Key Metrics

**Expected Timings:**
- CDK deploy: 2-5 minutes
- SSL certificate provisioning: 10-30 minutes (first deploy only)
- Amplify build: 3-10 minutes (depending on project size)
- CloudFront propagation: 2-5 minutes
- Total first deploy: ~30-45 minutes
- Subsequent deploys: ~5-15 minutes

**Cost Estimate (per environment):**
- Amplify hosting: $0.01 per build minute + $0.15 per GB served
- Route53: $0.50 per hosted zone per month
- ACM SSL certificate: Free
- CloudFront: Included with Amplify

---

## Summary

This SOP provides a complete multi-environment deployment strategy using AWS Amplify with:

1. ✅ **Branch-based environments** (dev, stage, prod)
2. ✅ **Custom Route53 domains** (`{env}-{project}.b.lfg.new`)
3. ✅ **Infrastructure as Code** (AWS CDK)
4. ✅ **Automated deployments** (git push triggers build)
5. ✅ **SSL certificates** (automatic via ACM)
6. ✅ **Post-deploy smoke tests** (git hash verification)
7. ✅ **Capistrano-style releases** (atomic deploys with rollback)

**NEVER use S3 static hosting for microsites - ALWAYS use AWS Amplify per this SOP.**
