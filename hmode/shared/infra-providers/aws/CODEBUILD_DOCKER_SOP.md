# AWS CodeBuild Docker Builds SOP

Build Docker images using AWS CodeBuild when local Docker is unavailable (e.g., Claude Code Web).

---

## When to Use

| Environment | Docker Available | Use This SOP |
|-------------|------------------|--------------|
| Local dev machine | Yes | No - use local Docker |
| Claude Code CLI | Usually yes | No - use local Docker |
| **Claude Code Web** | **No** | **Yes** |
| CI/CD pipelines | Varies | Yes - for consistency |

---

## Quick Start

```python
import boto3
import json
import time

codebuild = boto3.client('codebuild', region_name='us-east-1')

# Start build
response = codebuild.start_build(
    projectName='docker-builder',  # Pre-configured project
    sourceTypeOverride='NO_SOURCE',
    buildspecOverride='''
version: 0.2
phases:
  pre_build:
    commands:
      - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO
  build:
    commands:
      - docker build -t $IMAGE_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_NAME:$IMAGE_TAG $ECR_REPO/$IMAGE_NAME:$IMAGE_TAG
  post_build:
    commands:
      - docker push $ECR_REPO/$IMAGE_NAME:$IMAGE_TAG
''',
    environmentVariablesOverride=[
        {'name': 'IMAGE_NAME', 'value': 'my-app', 'type': 'PLAINTEXT'},
        {'name': 'IMAGE_TAG', 'value': 'latest', 'type': 'PLAINTEXT'},
        {'name': 'ECR_REPO', 'value': '507745175693.dkr.ecr.us-east-1.amazonaws.com', 'type': 'PLAINTEXT'}
    ]
)

build_id = response['build']['id']
print(f'Build started: {build_id}')
```

---

## Prerequisites

### 1. CodeBuild Project (One-Time Setup)

Create a CodeBuild project with Docker support:

```python
import boto3

codebuild = boto3.client('codebuild', region_name='us-east-1')

codebuild.create_project(
    name='docker-builder',
    description='Generic Docker image builder for Claude Code Web',
    source={
        'type': 'NO_SOURCE',
        'buildspec': 'version: 0.2\nphases:\n  build:\n    commands:\n      - echo "Override with buildspecOverride"'
    },
    artifacts={'type': 'NO_ARTIFACTS'},
    environment={
        'type': 'LINUX_CONTAINER',
        'image': 'aws/codebuild/amazonlinux2-x86_64-standard:5.0',
        'computeType': 'BUILD_GENERAL1_MEDIUM',
        'privilegedMode': True,  # Required for Docker
        'environmentVariables': []
    },
    serviceRole='arn:aws:iam::507745175693:role/CodeBuildServiceRole'
)
```

### 2. IAM Role Permissions

The CodeBuild service role needs:
- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:BatchGetImage`
- `ecr:PutImage`
- `ecr:InitiateLayerUpload`
- `ecr:UploadLayerPart`
- `ecr:CompleteLayerUpload`
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`

### 3. ECR Repository

```bash
aws ecr create-repository --repository-name my-app --region us-east-1
```

---

## Build Patterns

### Pattern 1: Build from GitHub Repository

```python
response = codebuild.start_build(
    projectName='docker-builder',
    sourceTypeOverride='GITHUB',
    sourceLocationOverride='https://github.com/owner/repo.git',
    sourceVersion='main',  # branch, tag, or commit
    buildspecOverride='''
version: 0.2
phases:
  pre_build:
    commands:
      - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO
  build:
    commands:
      - docker build -t $IMAGE_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_NAME:$IMAGE_TAG $ECR_REPO/$IMAGE_NAME:$IMAGE_TAG
  post_build:
    commands:
      - docker push $ECR_REPO/$IMAGE_NAME:$IMAGE_TAG
''',
    environmentVariablesOverride=[
        {'name': 'IMAGE_NAME', 'value': 'my-app', 'type': 'PLAINTEXT'},
        {'name': 'IMAGE_TAG', 'value': 'v1.0.0', 'type': 'PLAINTEXT'},
        {'name': 'ECR_REPO', 'value': '507745175693.dkr.ecr.us-east-1.amazonaws.com', 'type': 'PLAINTEXT'}
    ]
)
```

### Pattern 2: Build from S3 Source

```python
# First upload Dockerfile and context to S3
s3 = boto3.client('s3')
# ... upload files ...

response = codebuild.start_build(
    projectName='docker-builder',
    sourceTypeOverride='S3',
    sourceLocationOverride='my-bucket/docker-context.zip',
    buildspecOverride='...'
)
```

### Pattern 3: Build with Build Args

```python
buildspec = '''
version: 0.2
phases:
  pre_build:
    commands:
      - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO
  build:
    commands:
      - |
        docker build \
          --build-arg NODE_ENV=production \
          --build-arg API_URL=$API_URL \
          -t $IMAGE_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_NAME:$IMAGE_TAG $ECR_REPO/$IMAGE_NAME:$IMAGE_TAG
  post_build:
    commands:
      - docker push $ECR_REPO/$IMAGE_NAME:$IMAGE_TAG
'''
```

### Pattern 4: Multi-Architecture Build

```python
buildspec = '''
version: 0.2
phases:
  pre_build:
    commands:
      - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO
  build:
    commands:
      - docker buildx create --use
      - |
        docker buildx build \
          --platform linux/amd64,linux/arm64 \
          --tag $ECR_REPO/$IMAGE_NAME:$IMAGE_TAG \
          --push .
'''
```

---

## Monitoring Builds

### Check Build Status

```python
def wait_for_build(build_id: str, timeout_minutes: int = 30) -> dict:
    """Wait for CodeBuild build to complete."""
    import time

    codebuild = boto3.client('codebuild', region_name='us-east-1')
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60

    while True:
        response = codebuild.batch_get_builds(ids=[build_id])
        build = response['builds'][0]
        status = build['buildStatus']

        if status == 'SUCCEEDED':
            print(f'Build succeeded: {build_id}')
            return build
        elif status in ['FAILED', 'FAULT', 'STOPPED', 'TIMED_OUT']:
            print(f'Build failed with status: {status}')
            print(f'Logs: {build.get("logs", {}).get("deepLink", "N/A")}')
            raise Exception(f'Build failed: {status}')

        if time.time() - start_time > timeout_seconds:
            raise TimeoutError(f'Build timed out after {timeout_minutes} minutes')

        print(f'Build status: {status}, waiting...')
        time.sleep(10)
```

### Stream Build Logs

```python
def stream_build_logs(build_id: str):
    """Stream CloudWatch logs from a CodeBuild build."""
    logs_client = boto3.client('logs', region_name='us-east-1')

    # Get log group/stream from build
    response = codebuild.batch_get_builds(ids=[build_id])
    logs_info = response['builds'][0].get('logs', {})

    if 'groupName' in logs_info and 'streamName' in logs_info:
        response = logs_client.get_log_events(
            logGroupName=logs_info['groupName'],
            logStreamName=logs_info['streamName']
        )
        for event in response['events']:
            print(event['message'])
```

---

## Complete Example: Build and Deploy

```python
#!/usr/bin/env python3
"""
Build Docker image via CodeBuild and deploy to ECS.
Use this in Claude Code Web when local Docker is unavailable.
"""

import boto3
import time
import sys

def build_and_push_image(
    image_name: str,
    image_tag: str,
    github_repo: str,
    github_branch: str = 'main',
    ecr_repo: str = '507745175693.dkr.ecr.us-east-1.amazonaws.com'
) -> str:
    """Build Docker image via CodeBuild and push to ECR."""

    codebuild = boto3.client('codebuild', region_name='us-east-1')

    buildspec = f'''
version: 0.2
phases:
  pre_build:
    commands:
      - echo "Logging into ECR..."
      - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {ecr_repo}
  build:
    commands:
      - echo "Building Docker image..."
      - docker build -t {image_name}:{image_tag} .
      - docker tag {image_name}:{image_tag} {ecr_repo}/{image_name}:{image_tag}
  post_build:
    commands:
      - echo "Pushing to ECR..."
      - docker push {ecr_repo}/{image_name}:{image_tag}
      - echo "Image URI: {ecr_repo}/{image_name}:{image_tag}"
'''

    response = codebuild.start_build(
        projectName='docker-builder',
        sourceTypeOverride='GITHUB',
        sourceLocationOverride=github_repo,
        sourceVersion=github_branch,
        buildspecOverride=buildspec
    )

    build_id = response['build']['id']
    print(f'Started build: {build_id}')

    # Wait for completion
    while True:
        result = codebuild.batch_get_builds(ids=[build_id])
        build = result['builds'][0]
        status = build['buildStatus']

        if status == 'SUCCEEDED':
            image_uri = f'{ecr_repo}/{image_name}:{image_tag}'
            print(f'Build succeeded! Image: {image_uri}')
            return image_uri
        elif status in ['FAILED', 'FAULT', 'STOPPED', 'TIMED_OUT']:
            logs_link = build.get('logs', {}).get('deepLink', 'N/A')
            raise Exception(f'Build failed: {status}. Logs: {logs_link}')

        print(f'Status: {status}...')
        time.sleep(15)


if __name__ == '__main__':
    image_uri = build_and_push_image(
        image_name='my-service',
        image_tag='v1.0.0',
        github_repo='https://github.com/myorg/myrepo.git',
        github_branch='main'
    )
    print(f'Deploy using image: {image_uri}')
```

---

## Troubleshooting

### Build Fails with "Cannot connect to Docker daemon"

**Cause:** `privilegedMode` not enabled on CodeBuild project

**Fix:** Enable privileged mode:
```python
codebuild.update_project(
    name='docker-builder',
    environment={
        'type': 'LINUX_CONTAINER',
        'image': 'aws/codebuild/amazonlinux2-x86_64-standard:5.0',
        'computeType': 'BUILD_GENERAL1_MEDIUM',
        'privilegedMode': True  # Required for Docker
    }
)
```

### ECR Push Fails with "no basic auth credentials"

**Cause:** ECR login expired or failed

**Fix:** Ensure pre_build phase includes ECR login:
```yaml
pre_build:
  commands:
    - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO
```

### Build Timeout

**Cause:** Default timeout too short for large images

**Fix:** Set longer timeout in start_build:
```python
codebuild.start_build(
    projectName='docker-builder',
    timeoutInMinutesOverride=60,  # 60 minutes
    ...
)
```

---

## Cost Considerations

| Compute Type | vCPU | Memory | Cost/min (approx) |
|--------------|------|--------|-------------------|
| BUILD_GENERAL1_SMALL | 2 | 3 GB | $0.005 |
| BUILD_GENERAL1_MEDIUM | 4 | 7 GB | $0.010 |
| BUILD_GENERAL1_LARGE | 8 | 15 GB | $0.020 |

For typical Docker builds, `BUILD_GENERAL1_MEDIUM` provides good balance.

---

## Related

- `shared/infra-providers/aws/buildspec.yml` - Generic buildspec template
- `shared/golden-repos/*/Dockerfile` - Dockerfile templates
- ECR repositories: AWS Console > ECR

---

## References

- [CodeBuild Docker Sample](https://docs.aws.amazon.com/codebuild/latest/userguide/sample-docker.html)
- [CodeBuild Build Spec Reference](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
- [ECR Authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)
