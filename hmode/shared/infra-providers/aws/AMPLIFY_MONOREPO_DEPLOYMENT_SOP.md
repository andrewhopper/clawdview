# AWS Amplify Monorepo Deployment SOP

## Overview

This document describes how to deploy a Next.js SSR application from a monorepo to AWS Amplify using Git-based deployments with a `claude/` prefixed branch.

**Key Points:**
- Amplify does NOT support manual zip deployments for SSR (WEB_COMPUTE) apps
- Git-based deployment is required for SSR to work
- Uses fine-grained branch targeting for monorepo apps

## Prerequisites

1. **AWS Credentials** with Amplify permissions
2. **GitHub Personal Access Token** (classic) with scopes:
   - `repo` (full control of private repositories)
   - `admin:repo_hook` (webhooks)
3. **Existing Amplify App** configured as `WEB_COMPUTE` platform

## Token Management

### Store GitHub Token in Secrets Manager

```python
import boto3

sm = boto3.client('secretsmanager', region_name='us-east-1')
sm.update_secret(
    SecretId='github-token',
    SecretString='ghp_your_token_here'
)
```

### Retrieve Token

```python
response = sm.get_secret_value(SecretId='github-token')
token = response['SecretString']
```

## Deployment Steps

### Step 1: Delete Existing Manual Branches

Amplify requires all manually-deployed branches to be deleted before connecting a Git repository.

```python
import boto3

amplify = boto3.client('amplify', region_name='us-east-1')
APP_ID = 'your-app-id'

# List and delete all branches
branches = amplify.list_branches(appId=APP_ID)['branches']
for b in branches:
    amplify.delete_branch(appId=APP_ID, branchName=b['branchName'])
    print(f"Deleted: {b['branchName']}")
```

### Step 2: Connect GitHub Repository

```python
# Retrieve GitHub token from Secrets Manager
sm = boto3.client('secretsmanager', region_name='us-east-1')
token = sm.get_secret_value(SecretId='github-token')['SecretString']

# Monorepo buildspec
buildspec = """version: 1
applications:
  - appRoot: path/to/your/frontend
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
"""

# Connect repository
response = amplify.update_app(
    appId=APP_ID,
    repository='https://github.com/owner/repo',
    accessToken=token,
    buildSpec=buildspec,
    platform='WEB_COMPUTE',
    environmentVariables={
        'AMPLIFY_MONOREPO_APP_ROOT': 'path/to/your/frontend',
        '_LIVE_UPDATES': '[{"pkg":"node","type":"nvm","version":"20"}]'
    }
)
print(f"Repository connected: {response['app'].get('repository')}")
```

### Step 3: Create Branch with claude/ Prefix

```python
BRANCH_NAME = 'claude/your-feature-branch'

response = amplify.create_branch(
    appId=APP_ID,
    branchName=BRANCH_NAME,
    stage='PRODUCTION',
    enableAutoBuild=True,
    enablePullRequestPreview=False,
    environmentVariables={
        'AMPLIFY_MONOREPO_APP_ROOT': 'path/to/your/frontend'
    }
)
print(f"Branch created: {response['branch']['branchName']}")
```

### Step 4: Trigger Build

```python
import time

# Start the build
response = amplify.start_job(
    appId=APP_ID,
    branchName=BRANCH_NAME,
    jobType='RELEASE'
)
job_id = response['jobSummary']['jobId']
print(f"Build started: Job {job_id}")

# Monitor progress
while True:
    time.sleep(10)
    job = amplify.get_job(appId=APP_ID, branchName=BRANCH_NAME, jobId=job_id)
    status = job['job']['summary']['status']
    print(f"Status: {status}")

    if status in ['SUCCEED', 'FAILED', 'CANCELLED']:
        break

if status == 'SUCCEED':
    print(f"✅ Build successful!")
    print(f"URL: https://{BRANCH_NAME.replace('/', '-')}.{APP_ID}.amplifyapp.com")
```

### Step 5: Configure Custom Domain (Optional)

```python
response = amplify.update_domain_association(
    appId=APP_ID,
    domainName='your-domain.com',
    subDomainSettings=[
        {
            'prefix': 'app',  # app.your-domain.com
            'branchName': BRANCH_NAME
        }
    ]
)
print(f"Domain status: {response['domainAssociation']['domainStatus']}")
```

## Complete Script

```python
#!/usr/bin/env python3
"""
Amplify Monorepo Deployment Script
Usage: python deploy_amplify.py --app-id <APP_ID> --branch <BRANCH_NAME>
"""

import boto3
import time
import argparse

def deploy_to_amplify(app_id: str, branch_name: str, app_root: str):
    sm = boto3.client('secretsmanager', region_name='us-east-1')
    amplify = boto3.client('amplify', region_name='us-east-1')

    # Get GitHub token
    token = sm.get_secret_value(SecretId='github-token')['SecretString']

    # Buildspec for monorepo
    buildspec = f"""version: 1
applications:
  - appRoot: {app_root}
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
"""

    # Check if repo is connected
    app = amplify.get_app(appId=app_id)['app']
    if not app.get('repository'):
        print("Connecting repository...")
        # Delete existing branches first
        for b in amplify.list_branches(appId=app_id)['branches']:
            amplify.delete_branch(appId=app_id, branchName=b['branchName'])

        amplify.update_app(
            appId=app_id,
            repository='https://github.com/andrewhopper/protoflow',
            accessToken=token,
            buildSpec=buildspec,
            platform='WEB_COMPUTE',
            environmentVariables={
                'AMPLIFY_MONOREPO_APP_ROOT': app_root,
                '_LIVE_UPDATES': '[{"pkg":"node","type":"nvm","version":"20"}]'
            }
        )

    # Create or update branch
    try:
        amplify.create_branch(
            appId=app_id,
            branchName=branch_name,
            stage='PRODUCTION',
            enableAutoBuild=True,
            environmentVariables={'AMPLIFY_MONOREPO_APP_ROOT': app_root}
        )
    except amplify.exceptions.BadRequestException:
        amplify.update_branch(
            appId=app_id,
            branchName=branch_name,
            enableAutoBuild=True
        )

    # Trigger build
    response = amplify.start_job(
        appId=app_id,
        branchName=branch_name,
        jobType='RELEASE'
    )
    job_id = response['jobSummary']['jobId']
    print(f"Build started: {job_id}")

    # Wait for completion
    while True:
        time.sleep(10)
        job = amplify.get_job(appId=app_id, branchName=branch_name, jobId=job_id)
        status = job['job']['summary']['status']
        print(f"  Status: {status}")
        if status in ['SUCCEED', 'FAILED', 'CANCELLED']:
            break

    return status == 'SUCCEED'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-id', required=True)
    parser.add_argument('--branch', required=True)
    parser.add_argument('--app-root', required=True)
    args = parser.parse_args()

    success = deploy_to_amplify(args.app_id, args.branch, args.app_root)
    exit(0 if success else 1)
```

## Troubleshooting

### "Bad credentials" Error
- GitHub token is expired or revoked
- Token doesn't have `repo` or `admin:repo_hook` scopes
- For fine-grained PATs: token wasn't granted access to the specific repository

### "Cannot connect your app to repository while manually deployed branch still exists"
- Delete all existing branches before connecting the repository
- Use `list_branches` + `delete_branch` to remove all branches

### Build Succeeds but Site Returns 404
- This happens with manual zip deployments for SSR apps
- Solution: Use Git-based deployment (this SOP)

### 503 on Custom Domain
- Domain association may need to be updated to point to the new branch
- Use `update_domain_association` to reconfigure

## Reference

- **Amplify App ID**: Found in Amplify Console URL or via `list_apps` API
- **GitHub Token Secret**: `github-token` in Secrets Manager (us-east-1)
- **PPM App ID**: `d1prps0dv0afcm`
- **PPM App Root**: `projects/personal/active/ppm-personal-priority-manager-p1m2n/frontend`

## Related Documentation

- [AWS Amplify Hosting Docs](https://docs.aws.amazon.com/amplify/latest/userguide/)
- [Amplify Monorepo Setup](https://docs.aws.amazon.com/amplify/latest/userguide/deploy-nextjs-monorepo.html)
- [Amplify SSR Support](https://docs.aws.amazon.com/amplify/latest/userguide/ssr-amplify-support.html)
