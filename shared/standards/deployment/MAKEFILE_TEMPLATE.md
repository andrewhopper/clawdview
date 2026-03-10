# Standard Deployment Makefile Template

All deployable projects MUST use this two-phase deployment pattern.

## Required Makefile Targets

```makefile
.PHONY: infra-bootstrap infra-deploy infra-destroy infra-diff infra-rollback
.PHONY: validate-config post-deploy-validate infra-shadow

TIMESTAMP := $(shell date +%Y%m%d-%H%M)
RELEASES_DIR := infra/deploys/releases
RELEASE_DIR := $(RELEASES_DIR)/$(TIMESTAMP)
CURRENT_LINK := infra/deploys/current
KEEP_RELEASES := 5
GIT_HASH := $(shell git rev-parse --short HEAD)
MONOREPO_ROOT := $(shell git rev-parse --show-toplevel)

# Configuration (override in project Makefile)
DEPLOY_URL ?= https://your-app.example.com
COGNITO_POOL_ID ?=
COGNITO_CLIENT_ID ?=
AWS_REGION ?= us-east-1
RETRY_DELAY ?= 60
MAX_RETRIES ?= 3
STACK_NAME ?= $(shell basename $(CURDIR))-dev

# ========================================
# Pre-deployment: Config Validation
# ========================================
validate-config:
	@echo "🔍 Validating configuration files..."
	@python $(MONOREPO_ROOT)/shared/tools/validate-deployment-config.py --project . --strict
	@echo "✓ Configuration valid"

# ========================================
# Infrastructure Deployment
# ========================================
infra-bootstrap:
	@echo "Bootstrapping CDK..."
	@mkdir -p $(RELEASE_DIR)
	cd infra && cdk bootstrap aws://$(AWS_ACCOUNT)/$(AWS_REGION) 2>&1 | tee ../$(RELEASE_DIR)/deploy.log

infra-deploy: validate-config
	@echo "Deploying infrastructure to $(RELEASE_DIR)..."
	@mkdir -p $(RELEASE_DIR) infra/deploys/shared
	cd infra && cdk deploy --all --require-approval never --outputs-file ../$(RELEASE_DIR)/outputs.json 2>&1 | tee ../$(RELEASE_DIR)/deploy.log
	@ln -sfn releases/$(TIMESTAMP) $(CURRENT_LINK)
	@echo '{"timestamp":"$(TIMESTAMP)","status":"deployed","git_hash":"$(GIT_HASH)"}' > $(RELEASE_DIR)/manifest.json
	@echo "✓ Deployed: $(RELEASE_DIR)"
	@echo "✓ Current symlink updated"
	@# Cleanup old releases (keep last N)
	@cd $(RELEASES_DIR) && ls -t | tail -n +$$(($(KEEP_RELEASES)+1)) | xargs -r rm -rf
	@# Run post-deploy validation
	@$(MAKE) post-deploy-validate

# ========================================
# Post-deployment: Smoke Tests & Validation
# ========================================
post-deploy-validate:
	@echo ""
	@echo "⏳ Waiting 30 seconds for deployment propagation..."
	@sleep 30
	@echo "🔍 Running post-deployment validation..."
	@python $(MONOREPO_ROOT)/shared/tools/post-deploy-validate.py \
		--url $(DEPLOY_URL) \
		--expected-hash $(GIT_HASH) \
		$(if $(COGNITO_POOL_ID),--cognito-pool $(COGNITO_POOL_ID)) \
		$(if $(COGNITO_CLIENT_ID),--cognito-client $(COGNITO_CLIENT_ID)) \
		--region $(AWS_REGION) \
		--max-retries $(MAX_RETRIES) \
		--retry-delay $(RETRY_DELAY)
	@echo "✅ Post-deployment validation PASSED"

# Validate only (no retry, for quick checks)
validate-deployment:
	@python $(MONOREPO_ROOT)/shared/tools/post-deploy-validate.py \
		--url $(DEPLOY_URL) \
		--expected-hash $(GIT_HASH) \
		$(if $(COGNITO_POOL_ID),--cognito-pool $(COGNITO_POOL_ID)) \
		$(if $(COGNITO_CLIENT_ID),--cognito-client $(COGNITO_CLIENT_ID)) \
		--max-retries 1 \
		--no-auto-fix

# ========================================
# Infrastructure Shadow (Resource Discovery)
# ========================================
infra-shadow:
	@echo "🔍 Generating infrastructure shadow file..."
	@python $(MONOREPO_ROOT)/bin/infra-shadow.py \
		--stack-name $(STACK_NAME) \
		--output infra/config/infra_shadow.yml \
		--html
	@echo "✓ Shadow file generated at infra/config/infra_shadow.yml"

# Sync shadow without HTML
infra-shadow-quick:
	@python $(MONOREPO_ROOT)/bin/infra-shadow.py \
		--stack-name $(STACK_NAME) \
		--output infra/config/infra_shadow.yml

# ========================================
# Rollback & Destroy
# ========================================
infra-rollback:
	@echo "Available releases:"
	@ls -t $(RELEASES_DIR) | head -$(KEEP_RELEASES)
	@echo "Usage: make infra-rollback RELEASE=YYYYMMDD-HHMM"
ifdef RELEASE
	@ln -sfn releases/$(RELEASE) $(CURRENT_LINK)
	@echo "✓ Rolled back to $(RELEASE)"
endif

infra-destroy:
	@echo "Destroying infrastructure..."
	@mkdir -p $(RELEASE_DIR)
	cd infra && cdk destroy --all --force 2>&1 | tee ../$(RELEASE_DIR)/deploy.log

infra-diff:
	@echo "Showing infrastructure diff..."
	cd infra && cdk diff
```

## Environment Configuration

```bash
# Required environment variables
AWS_PROFILE=your-profile          # Or use AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY
AWS_REGION=us-east-1              # Target region
DEPLOY_ENV=dev|staging|prod       # Environment name
```

## Project Structure (Capistrano-style)

```
project/
├── Makefile                      # Contains infra-bootstrap, infra-deploy targets
├── infra/
│   ├── app.py                    # CDK app entry point
│   ├── stacks/                   # CDK stack definitions
│   ├── deploys/                  # Deployment history (Capistrano-style)
│   │   ├── releases/             # Timestamped release folders
│   │   │   ├── 20250929-2345/    # Each deploy gets a folder
│   │   │   │   ├── deploy.log    # Full CDK output
│   │   │   │   ├── outputs.json  # Stack outputs (ARNs, URLs)
│   │   │   │   └── manifest.json # Deployed resources manifest
│   │   │   └── 20250930-1200/
│   │   ├── current -> releases/20250930-1200  # Symlink to active release
│   │   └── shared/               # Persistent across releases
│   │       └── tfstate/          # State files (if applicable)
│   └── requirements.txt          # CDK dependencies
└── .env.example                  # Template for required env vars
```

## Deployment History

Modeled after Rails Capistrano for atomic deploys and easy rollback:
- **releases/** - Each deployment gets a timestamped folder
- **current** - Symlink to active release (enables atomic switches)
- **shared/** - Resources persisted across deployments
- Keep last 5 releases for rollback capability
- Git-tracked for audit trail

## Release Contents

- `deploy.log` - Full CDK output with timestamps
- `outputs.json` - Stack outputs (ARNs, URLs, endpoints)
- `manifest.json` - Deployed resources with versions, git hash

## Post-Deployment Validation

**CRITICAL:** Every deploy now automatically runs validation. You can also run manually:

```bash
# Full validation with retries (runs automatically after infra-deploy)
make post-deploy-validate DEPLOY_URL=https://app.example.com

# Quick validation (no retries)
make validate-deployment DEPLOY_URL=https://app.example.com
```

### Validation Checks

| Check | What it validates |
|-------|-------------------|
| DNS Resolution | Domain resolves to an IP address |
| URL Accessible | Returns HTTP 200 |
| SSL Certificate | Valid and not expiring soon |
| Git Hash | Matches expected commit (footer, meta tag) |
| Footer/Build Date | Contains recent date |
| Health Endpoint | /health returns OK |
| Cognito Auth | Smoke test user can authenticate |
| Page Render | Playwright verifies page loads without errors |

### Configuration Variables

Set these in your project Makefile:

```makefile
# Required
DEPLOY_URL := https://your-app.example.com

# Optional (for auth testing)
COGNITO_POOL_ID := us-east-1_AbcDef123
COGNITO_CLIENT_ID := 1234567890abcdefghijklmnop

# Retry settings
MAX_RETRIES := 3      # Default: 3 attempts
RETRY_DELAY := 60     # Default: 60 seconds between retries
```

### Smoke Test User

When Cognito is configured, the validator automatically:
1. Creates a `smoketest-*@smoketest.local` user in the pool
2. Sets a secure password
3. Uses this user to test authentication flow
4. Reuses the user on subsequent runs

## Pre-Deployment Config Validation

Config files are validated before deployment:

```bash
# Validate config files in project
make validate-config

# Or run directly
python shared/tools/validate-deployment-config.py --project .
```

### What Gets Checked

- **No placeholders:** `YOUR_*`, `REPLACE_*`, `TODO`, `<placeholder>`, etc.
- **Valid AWS resource IDs:** Cognito pool IDs, ARNs, bucket names, etc.
- **Type validation:** Numeric IDs have correct format

### Pre-commit Hook

The hook is automatically configured in `.pre-commit-config.yaml`:

```bash
# Run on all config files
pre-commit run validate-deployment-config --all-files
```

## Infrastructure Shadow

The shadow command creates a local YAML file containing your deployed AWS resources for easy lookup. This "shadow" mirrors your deployed infrastructure, making it simple to find SSM parameter paths, DynamoDB table names, API endpoints, etc.

### Usage

```bash
# Generate shadow file from CloudFormation stack
make infra-shadow STACK_NAME=my-project-dev

# Quick sync (no HTML viewer)
make infra-shadow-quick STACK_NAME=my-project-dev

# Or run directly with options
python bin/infra-shadow.py --stack-name my-project-dev --html
```

### What Gets Discovered

| Resource Type | Information Captured |
|---------------|---------------------|
| Stack Outputs | All CloudFormation outputs (URLs, ARNs, IDs) |
| SSM Parameters | Parameter paths under `/protoflow/projects/` |
| DynamoDB Tables | Table names, ARNs, key schemas |
| API Gateway | REST/HTTP APIs, endpoints, stages |
| Cognito | User pools, app client IDs |
| Lambda | Function names, ARNs, runtimes |
| S3 Buckets | Bucket names, ARNs |

### Output Files

```
infra/config/
├── infra_shadow.yml    # YAML file with all resources
└── infra_shadow.html   # Interactive HTML viewer
```

### Example Shadow File

```yaml
account_id: '123456789012'
region: us-east-1
environment: dev
stack_name: my-project-dev

outputs:
  ApiUrl: 'https://abc123.execute-api.us-east-1.amazonaws.com/prod/'
  TableName: my-project-dev-users

dynamodb_tables:
  - name: my-project-dev-users
    arn: arn:aws:dynamodb:us-east-1:123456789012:table/my-project-dev-users
    key_schema: 'pk (HASH), sk (RANGE)'

ssm_parameters:
  - path: /protoflow/projects/my-project/api-url
    type: String
```

### When to Use

1. **After deploy** - Run `make infra-shadow` to capture current state
2. **Manual sync** - Run when you need updated resource IDs
3. **Troubleshooting** - Quick reference for resource names/IDs
4. **Code reference** - Copy IDs directly from the HTML viewer
