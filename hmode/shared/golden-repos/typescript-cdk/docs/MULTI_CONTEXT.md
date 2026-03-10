# Multi-Context, Multi-Stage Infrastructure

Deploy the same infrastructure to multiple contexts (work, personal, clients) with different stages (dev, prod, blue/green, alpha/beta/gamma).

## Quick Start

### 1. List Available Configurations

```bash
make infra-list
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Available Configurations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Context: personal
  Stages: alpha blue dev green

Context: work
  Stages: dev prod stage
```

### 2. Deploy to Specific Context + Stage

```bash
# Deploy work dev environment
make infra-deploy CONTEXT=work STAGE=dev

# Deploy personal blue environment
make infra-deploy CONTEXT=personal STAGE=blue

# Deploy personal alpha environment
make infra-deploy CONTEXT=personal STAGE=alpha
```

### 3. Check Status

```bash
# Check work prod status
make infra-status CONTEXT=work STAGE=prod

# Check personal green status
make infra-status CONTEXT=personal STAGE=green
```

## Concepts

### Context
**Organizational boundaries** - separates work from personal projects, or different clients/teams.

Examples:
- `work` - Work/employment projects
- `personal` - Personal projects
- `client-acme` - Client-specific infrastructure
- `team-platform` - Team-specific infrastructure

### Stage
**Deployment stages** - any naming pattern you want within a context.

Common patterns:
- **Traditional:** `dev`, `stage`, `prod`
- **Blue/Green:** `blue`, `green`
- **Greek letters:** `alpha`, `beta`, `gamma`, `delta`
- **Semantic:** `development`, `staging`, `production`
- **Feature branches:** `feature-123`, `experiment-ai`

### Deploy ID
Automatically generated identifier: `{context}-{stage}`

Examples:
- `work-dev`
- `personal-blue`
- `client-acme-prod`

## Configuration Structure

```
config/
├── work/
│   ├── dev.yml
│   ├── stage.yml
│   └── prod.yml
└── personal/
    ├── dev.yml
    ├── alpha.yml
    ├── blue.yml
    └── green.yml
```

Each config file specifies:
- AWS account ID and region
- Project settings
- Domain configuration
- Database settings
- Compute resources
- Monitoring options
- Resource tags

## Deployment History

Each context-stage pair maintains **separate deployment history**:

```
infra/deploys/
├── work-dev/
│   ├── releases/
│   │   ├── 20251222-1030/
│   │   └── 20251222-1400/
│   ├── current -> releases/20251222-1400
│   └── shared/
├── work-prod/
│   ├── releases/
│   ├── current -> releases/...
│   └── shared/
├── personal-blue/
│   ├── releases/
│   ├── current -> releases/...
│   └── shared/
└── personal-green/
    ├── releases/
    ├── current -> releases/...
    └── shared/
```

Benefits:
- **Independent rollbacks** - Roll back personal-blue without affecting work-prod
- **Audit trail** - Complete history for each environment
- **Zero-downtime** - Blue/green deployments with separate state

## Usage Examples

### Deploy to Work Dev

```bash
make infra-deploy CONTEXT=work STAGE=dev
```

**What happens:**
1. ✅ Loads `config/work/dev.yml`
2. ✅ Sets environment variables `CONTEXT=work STAGE=dev`
3. ✅ CDK synthesizes stacks with names: `myapp-work-dev-Api`, `myapp-work-dev-Monitoring`
4. ✅ Deploys to work AWS account
5. ✅ Saves deployment to `infra/deploys/work-dev/releases/TIMESTAMP/`
6. ✅ Updates `infra/deploys/work-dev/current` symlink

### Blue/Green Deployment (Personal Context)

#### Step 1: Deploy to Blue

```bash
make infra-deploy CONTEXT=personal STAGE=blue
```

#### Step 2: Test Blue Environment

```bash
# Check blue outputs
make infra-outputs CONTEXT=personal STAGE=blue

# Verify application works
curl https://api.blue.b.lfg.new/health
```

#### Step 3: Deploy to Green

```bash
make infra-deploy CONTEXT=personal STAGE=green
```

#### Step 4: Test Green Environment

```bash
# Check green outputs
make infra-outputs CONTEXT=personal STAGE=green

# Verify application works
curl https://api.green.b.lfg.new/health
```

#### Step 5: Switch Traffic

Update DNS/load balancer to point to green environment.

#### Step 6: Rollback if Needed

If issues arise, instantly switch DNS back to blue (still running).

### Alpha/Beta/Gamma Testing

```bash
# Deploy alpha for early testing
make infra-deploy CONTEXT=personal STAGE=alpha

# Promote to beta after alpha validation
make infra-deploy CONTEXT=personal STAGE=beta

# Promote to gamma (pre-production) after beta validation
make infra-deploy CONTEXT=personal STAGE=gamma

# Finally deploy to production
make infra-deploy CONTEXT=personal STAGE=prod
```

### Feature Branch Deployments

```bash
# Create config for feature branch
cp config/personal/dev.yml config/personal/feature-ai.yml

# Edit feature-ai.yml (change domains, reduce resources)
# ...

# Deploy feature branch
make infra-deploy CONTEXT=personal STAGE=feature-ai

# Test feature
curl https://api.feature-ai.b.lfg.new

# Destroy when done
make infra-destroy CONTEXT=personal STAGE=feature-ai
```

## Stack Naming

Stacks are automatically prefixed with `{stackPrefix}-{context}-{stage}-{stackName}`:

```
work-dev deployment:
  - myapp-work-dev-Monitoring
  - myapp-work-dev-Api

personal-blue deployment:
  - personal-personal-blue-Monitoring
  - personal-personal-blue-Api
```

This ensures:
- ✅ No naming conflicts between contexts/stages
- ✅ Easy identification in CloudFormation console
- ✅ Proper tagging for cost allocation

## Resource Tags

All resources are automatically tagged:

```yaml
Project: my-app
Context: work
Stage: dev
ManagedBy: CDK
```

Plus any custom tags from config:

```yaml
tags:
  Team: Platform
  CostCenter: Engineering
```

Use tags for:
- Cost allocation by context/stage
- Resource filtering
- Compliance tracking

## Advanced Operations

### Check Infrastructure Diff

```bash
# See what will change before deploying
make infra-diff CONTEXT=work STAGE=prod
```

### Rollback Deployment

```bash
# List available releases
make infra-rollback CONTEXT=personal STAGE=blue

# Rollback to specific release
make infra-rollback CONTEXT=personal STAGE=blue RELEASE=20251222-1030
```

### Destroy Environment

```bash
# Destroy personal alpha environment
make infra-destroy CONTEXT=personal STAGE=alpha
```

**Warning:** This destroys ALL resources. Use with caution!

### View Stack Outputs

```bash
# View outputs (ARNs, URLs, etc.)
make infra-outputs CONTEXT=work STAGE=prod
```

## Creating New Contexts

### 1. Create Context Directory

```bash
mkdir config/client-acme
```

### 2. Create Stage Configs

```bash
# Copy from existing config
cp config/work/dev.yml config/client-acme/dev.yml
cp config/work/prod.yml config/client-acme/prod.yml
```

### 3. Edit Configs

Update `config/client-acme/dev.yml`:

```yaml
# AWS Account & Region
account: "999888777666"  # Client's AWS account
region: "us-west-2"

# Project Settings
projectName: "acme-portal"
stackPrefix: "acme"

# Domain Configuration
domain:
  rootDomain: "dev.acme.com"
  subdomain: "api"

# ... rest of config
```

### 4. Deploy

```bash
make infra-deploy CONTEXT=client-acme STAGE=dev
```

## Creating New Stages

### 1. Copy Existing Stage

```bash
cp config/personal/dev.yml config/personal/beta.yml
```

### 2. Edit Stage Config

Update `config/personal/beta.yml`:

```yaml
domain:
  rootDomain: "beta.b.lfg.new"  # Change domain
  subdomain: "api"

# Adjust resources as needed
compute:
  desiredCount: 2  # More instances than dev
  
monitoring:
  enableDashboards: true  # Enable for beta
  enableTracing: true
```

### 3. Deploy

```bash
make infra-deploy CONTEXT=personal STAGE=beta
```

## Production Readiness

The loader automatically detects production-like stages:

```typescript
// Detected as production:
isProduction(config) // true for:
// - prod
// - production
// - green (blue/green)
// - gamma (alpha/beta/gamma)
```

Production stages typically have:
- ✅ Multi-AZ database
- ✅ Deletion protection enabled
- ✅ Longer backup retention
- ✅ More compute resources
- ✅ Enhanced monitoring
- ✅ Longer log retention

## Best Practices

### 1. Context Separation
- **Work** - Company/employment infrastructure
- **Personal** - Personal projects and experiments
- **Per-client** - Client-specific infrastructure with their AWS accounts

### 2. Stage Naming
- **Traditional projects:** dev → stage → prod
- **High-velocity deployments:** blue/green
- **Testing pipelines:** alpha → beta → gamma → prod
- **Feature testing:** feature-{name}

### 3. Configuration Management
- ✅ Keep production configs minimal (only differences from dev)
- ✅ Use consistent naming across contexts
- ✅ Document stage purposes in config comments
- ✅ Version control all configs (they're git-safe)

### 4. Deployment Workflow
- ✅ Test in dev first
- ✅ Use `infra-diff` before deploying to production
- ✅ Keep last 5 releases for rollback
- ✅ Tag releases with git commits

### 5. Cost Management
- ✅ Use smaller resources in dev/alpha stages
- ✅ Destroy unused feature branch deployments
- ✅ Monitor costs by Context and Stage tags
- ✅ Set budget alerts per context

## Troubleshooting

### "Configuration file not found"

```bash
# List available configs
make infra-list

# Check if config exists
ls config/work/dev.yml
```

### "No current deployment"

You haven't deployed yet:

```bash
make infra-deploy CONTEXT=work STAGE=dev
```

### Stack already exists

You may have manually created a stack. Either:
- Import it: `make infra-import STACK=name`
- Destroy it: Delete via CloudFormation console
- Use different stage name

### Wrong AWS account

Check config file has correct `account` field:

```yaml
account: "123456789012"  # Must match target account
```

## Migration from Single-Environment

If you have existing configs in `config/`:

### 1. Create Context Directory

```bash
mkdir config/work
```

### 2. Move Existing Configs

```bash
mv config/dev.yml config/work/
mv config/stage.yml config/work/
mv config/prod.yml config/work/
```

### 3. Deploy with Context

```bash
make infra-deploy CONTEXT=work STAGE=dev
```

Your existing deployments will continue working, and new deployments use the multi-context structure.

## Summary

Multi-context, multi-stage infrastructure provides:

✅ **Separation** - Work vs personal vs client infrastructure  
✅ **Flexibility** - Any stage naming pattern (dev/prod, blue/green, alpha/beta)  
✅ **Independence** - Separate deployment history per context-stage  
✅ **Safety** - Independent rollbacks, no cross-contamination  
✅ **Clarity** - Clear naming: `myapp-work-dev-Api`  
✅ **Cost tracking** - Tags for Context and Stage  

---

**Next Steps:**

1. Create your configs: `config/{context}/{stage}.yml`
2. Deploy: `make infra-deploy CONTEXT=work STAGE=dev`
3. Check status: `make infra-status CONTEXT=work STAGE=dev`
4. View outputs: `make infra-outputs CONTEXT=work STAGE=dev`
