<!-- File UUID: 4e8f5a6b-7c9d-0e1f-a2b3-6f7a8b9c0d1e -->

# Terraform HCL Golden Repo Template

Multi-context, multi-stage Terraform infrastructure template with Capistrano-style deployment history.

## Quick Start

```bash
# 1. List available configurations
make infra-list

# 2. Bootstrap (creates S3 state bucket + DynamoDB lock table)
make infra-bootstrap CONTEXT=personal STAGE=dev

# 3. Deploy
make infra-deploy CONTEXT=personal STAGE=dev

# 4. Check status
make infra-status CONTEXT=personal STAGE=dev
```

## Configuration

### Directory Structure

```
config/
├── work/
│   ├── dev.tfvars       # work-dev
│   ├── stage.tfvars     # work-stage
│   └── prod.tfvars      # work-prod
└── personal/
    ├── dev.tfvars       # personal-dev
    ├── alpha.tfvars     # personal-alpha
    ├── blue.tfvars      # personal-blue
    └── green.tfvars     # personal-green
```

### Adding a New Environment

1. Create `config/{context}/{stage}.tfvars`
2. Set required variables: `context`, `stage`, `account`, `region`, `project_name`, `notifications`
3. Run `make infra-bootstrap CONTEXT={context} STAGE={stage}`
4. Run `make infra-deploy CONTEXT={context} STAGE={stage}`

### Variable Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `context` | Yes | - | Deployment context (work, personal) |
| `stage` | Yes | - | Stage name (dev, prod, blue, green) |
| `account` | Yes | - | 12-digit AWS account ID |
| `region` | No | us-east-1 | AWS region |
| `project_name` | Yes | - | Lowercase project name |
| `stack_prefix` | No | project_name | Resource naming prefix |
| `domain` | No | null | Domain config (root_domain, subdomain) |
| `notifications` | Yes | - | Alert emails (admin_email required) |
| `database` | No | null | RDS config |
| `compute` | No | defaults | Lambda/ECS sizing |
| `monitoring` | No | defaults | CloudWatch/X-Ray toggles |
| `tags` | No | {} | Additional resource tags |

## Project Structure

```
├── infra/
│   ├── main.tf              # Root module (composes all modules)
│   ├── variables.tf         # Variable definitions with validation
│   ├── outputs.tf           # Root outputs
│   ├── locals.tf            # Shared local values
│   ├── provider.tf          # AWS provider + required versions
│   ├── backend.tf           # S3 remote state configuration
│   ├── modules/
│   │   ├── base/            # Common naming, tags, env detection
│   │   ├── api/             # Lambda + API Gateway
│   │   └── monitoring/      # SNS alerts + CloudWatch dashboard
│   └── deploys/             # Capistrano-style release history
│       └── {context}-{stage}/
│           ├── releases/
│           │   └── YYYYMMDD-HHMM/
│           │       ├── deploy.log
│           │       ├── outputs.json
│           │       └── manifest.json
│           └── current -> releases/...
├── config/
│   ├── {context}/
│   │   └── {stage}.tfvars
├── Makefile
└── README.md
```

## Modules

### base

Common infrastructure: resource naming prefix, tag generation, production detection.

**Outputs:** `resource_prefix`, `is_production`, `common_tags`

### api

Lambda function + HTTP API Gateway with health check endpoint.

**Outputs:** `api_url`, `lambda_function_name`, `lambda_function_arn`

### monitoring

SNS alert topic with email subscriptions, optional CloudWatch dashboard.

**Outputs:** `alert_topic_arn`, `alert_topic_name`

### Adding a New Module

1. Create `infra/modules/{name}/` with `main.tf`, `variables.tf`, `outputs.tf`
2. Accept `resource_prefix`, `common_tags`, `is_production` from base module
3. Wire it into `infra/main.tf`
4. Add outputs to `infra/outputs.tf`

## Environment-Specific Patterns

### Resource Sizing

```hcl
# dev: small, cheap
compute = { lambda_memory = 128, lambda_timeout = 15 }

# prod: large, reliable
compute = { lambda_memory = 1024, lambda_timeout = 30 }
```

### Conditional Features

```hcl
# Enable dashboards and tracing only in production
monitoring = {
  enable_dashboards = true   # false in dev
  enable_tracing    = true   # false in dev
  log_retention_days = 90    # 3 in dev
}
```

### Production Detection

Stages `prod`, `production`, `green`, `gamma` are auto-detected as production.
The base module sets `is_production = true` for these stages, which modules
use to control retention policies and protection settings.

## Deployment

### Remote State

State is stored in S3 with DynamoDB locking. `make infra-bootstrap` creates both automatically.

State key pattern: `{context}/{stage}/terraform.tfstate`

### Capistrano-Style Releases

Each deployment creates a timestamped release directory with:
- `deploy.log` — Full Terraform output
- `outputs.json` — All outputs as JSON
- `manifest.json` — Deployment metadata (timestamp, context, stage, git commit)

A `current` symlink always points to the active release. Last 5 releases are retained.

### Makefile Targets

| Target | Description |
|--------|-------------|
| `infra-bootstrap` | Create state bucket + DynamoDB lock + terraform init |
| `infra-deploy` | Plan + apply with release history |
| `infra-destroy` | Destroy all resources |
| `infra-diff` | Show pending changes |
| `infra-rollback` | Rollback to previous release |
| `infra-status` | Show current deployment info |
| `infra-outputs` | Show stack outputs |
| `infra-list` | List available configurations |
| `secrets-load` | Load secrets from Secrets Manager |
| `secrets-store` | Store .env file in Secrets Manager |

## CDK vs Terraform Mapping

| CDK Concept | Terraform Equivalent |
|-------------|---------------------|
| Stack | Module |
| Construct | Resource / Module |
| BaseStack | `modules/base` |
| `cdk.json` | `provider.tf` + `backend.tf` |
| `config/schema.ts` (Zod) | `variables.tf` (validation blocks) |
| `config/loader.ts` | Makefile `-var-file` flag |
| `CfnOutput` | `output` block |
| `addDependency()` | Implicit via module references |
| `cdk bootstrap` | `make infra-bootstrap` (S3 + DynamoDB) |
| `cdk deploy` | `terraform plan` + `terraform apply` |
| `cdk diff` | `terraform plan` |
| `cdk destroy` | `terraform destroy` |
| YAML config files | `.tfvars` files |
