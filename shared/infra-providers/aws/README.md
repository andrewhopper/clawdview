# AWS Deployment Configurations

Deploy-time configurations for AWS services (Amplify, CodeBuild, CodePipeline).

---

## Overview

This directory contains deployment configuration templates for AWS hosting services. For AWS SDK wrappers and credential handling, see `shared/aws/`.

---

## Files

| File | Purpose | Service |
|------|---------|---------|
| `amplify.yml` | Build specification | AWS Amplify |
| `buildspec.yml` | Build specification | AWS CodeBuild |
| `AMPLIFY_MULTI_ENV_DEPLOYMENT_SOP.md` | **Multi-environment deployment (dev/stage/prod)** | AWS Amplify + Route 53 + CDK |
| `AMPLIFY_CUSTOM_DOMAIN_SOP.md` | Custom domain setup guide | AWS Amplify + Route 53 |
| `AMPLIFY_COGNITO_REUSE_SOP.md` | Resource reuse patterns | AWS Amplify + Cognito |
| `AMPLIFY_MONOREPO_DEPLOYMENT_SOP.md` | Monorepo deployment guide | AWS Amplify |
| `CDK_ASSET_REUSE_GUIDE.md` | Asset decomposition & reuse patterns | AWS CDK |
| `CODEBUILD_DOCKER_SOP.md` | Docker builds in Claude Code Web | AWS CodeBuild + ECR |
| `SSO_CONFIG.md` | SSO configuration | AWS IAM Identity Center |

---

## AWS Amplify

### Multi-Environment Deployment (Recommended)

**CRITICAL:** NEVER use S3 static hosting for microsites - ALWAYS use AWS Amplify.

For production deployments with dev/stage/prod environments:

```bash
# See AMPLIFY_MULTI_ENV_DEPLOYMENT_SOP.md for complete guide

# One-time setup
make infra-bootstrap

# Deploy infrastructure (creates dev, stage, prod branches)
make infra-deploy

# Deploy to environments
make deploy-dev     # → dev-myapp.b.lfg.new
make deploy-stage   # → stage-myapp.b.lfg.new
make deploy-prod    # → prod-myapp.b.lfg.new
```

**Features:**
- ✅ Branch-based environments (dev, stage, prod)
- ✅ Custom Route53 domains (`{env}-{project}.b.lfg.new`)
- ✅ Infrastructure as Code (AWS CDK)
- ✅ Automated deployments (git push triggers build)
- ✅ SSL certificates (automatic via ACM)
- ✅ Post-deploy smoke tests (git hash verification)

See **[AMPLIFY_MULTI_ENV_DEPLOYMENT_SOP.md](./AMPLIFY_MULTI_ENV_DEPLOYMENT_SOP.md)** for complete guide.

### Quick Start (Single Environment)

1. Copy `amplify.yml` to your project root
2. Connect repo to Amplify Console
3. Amplify auto-detects the build spec

### Config Template

See `amplify.yml` for:
- Frontend build commands
- Backend build commands (if applicable)
- Artifact configuration
- Cache paths

### CLI Deployment (Single Environment)

```bash
# Basic deployment
python shared/scripts/amplify_deploy.py deploy ./my-app --app-name my-app

# Deploy with custom domain (auto-configures Route 53)
python shared/scripts/amplify_deploy.py deploy ./dist --app-name portfolio --domain myapp.example.com --yes

# List all apps
python shared/scripts/amplify_deploy.py list

# Check status
python shared/scripts/amplify_deploy.py status my-app
```

See `AMPLIFY_CUSTOM_DOMAIN_SOP.md` for detailed custom domain setup.

---

## AWS CodeBuild

### Quick Start

1. Copy `buildspec.yml` to your project root
2. Reference in CodePipeline or standalone CodeBuild project

### Config Template

See `buildspec.yml` for:
- Install phase (dependencies)
- Pre-build phase (tests, lint)
- Build phase (compile, bundle)
- Post-build phase (deploy, notify)

### Docker Builds (Claude Code Web)

**IMPORTANT:** Local Docker is NOT available in Claude Code Web. Use CodeBuild for Docker image builds.

```python
import boto3
codebuild = boto3.client('codebuild', region_name='us-east-1')
response = codebuild.start_build(
    projectName='docker-builder',
    sourceTypeOverride='GITHUB',
    sourceLocationOverride='https://github.com/owner/repo.git',
    # ... buildspec with docker commands
)
```

See `CODEBUILD_DOCKER_SOP.md` for complete patterns including:
- ECR authentication
- Multi-architecture builds
- Build monitoring
- Troubleshooting

---

## Environment Variables

### Amplify Console
Set in: Amplify Console > App settings > Environment variables

### CodeBuild
Set in: CodeBuild project > Environment > Environment variables
Or via `env` section in buildspec.yml

---

## AWS CDK

### Asset Reuse & Optimization

See `CDK_ASSET_REUSE_GUIDE.md` for:
- Decomposing monolithic stacks into L3 constructs
- Shared asset patterns (Lambda, Docker)
- Asset deduplication strategies
- Custom resource reuse
- Construct versioning

### Quick Start

See `shared/golden-repos/typescript-cdk/` for:
- Multi-context/multi-stage template
- Base stack pattern
- Example stacks and constructs

---

## Terraform HCL

### When to Use Terraform Instead of CDK

- **Multi-cloud** deployments (AWS + GCP + Azure)
- **Existing Terraform** codebases or team expertise
- **Declarative HCL** preference over imperative TypeScript
- **State management** requirements beyond CloudFormation

### Quick Start

See `shared/golden-repos/terraform-hcl/` for:
- Multi-context/multi-stage template (mirrors CDK structure)
- Base module (equivalent to CDK BaseStack)
- Example modules: API (Lambda + API Gateway), Monitoring (SNS + CloudWatch)
- Same Makefile targets as CDK (`infra-bootstrap`, `infra-deploy`, etc.)
- S3 remote state + DynamoDB locking
- Capistrano-style deployment history

```bash
# Bootstrap (creates state bucket + lock table + terraform init)
make infra-bootstrap CONTEXT=personal STAGE=dev

# Deploy
make infra-deploy CONTEXT=personal STAGE=dev

# Check status
make infra-status CONTEXT=personal STAGE=dev
```

### CDK ↔ Terraform Mapping

| CDK | Terraform |
|-----|-----------|
| Stack | Module |
| BaseStack construct | `modules/base` |
| `config/schema.ts` (Zod) | `variables.tf` (validation blocks) |
| YAML config files | `.tfvars` files |
| `cdk deploy` | `terraform apply` |
| CloudFormation state | S3 + DynamoDB state |

---

## Related

- SDK wrappers: `shared/aws/`
- Amplify deploy script: `shared/scripts/amplify_deploy.py`
- Route53 CNAME: `shared/aws/route53_cname.py`
- Docker builds SOP: `CODEBUILD_DOCKER_SOP.md`
- Dockerfile templates: `shared/golden-repos/*/Dockerfile`
- CDK asset patterns: `CDK_ASSET_REUSE_GUIDE.md`
- CDK golden repo: `shared/golden-repos/typescript-cdk/`

---

## References

- [Amplify Build Spec](https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html)
- [CodeBuild Build Spec](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
