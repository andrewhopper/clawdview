# Infrastructure Import Guide

Import existing AWS CloudFormation/CDK stacks into the Capistrano-style deployment structure with proper secrets management.

## Quick Start

### 1. List Available Stacks

```bash
make infra-import-list
```

**Output:**
```
📋 CloudFormation Stacks (12):

   • my-api-stack
     Status: UPDATE_COMPLETE
     Updated: 2025-12-15 10:30:00

   • my-web-frontend
     Status: CREATE_COMPLETE
     Updated: 2025-12-14 15:20:00
```

### 2. Import a Single Stack

```bash
make infra-import STACK=my-api-stack
```

**What happens:**
1. ✅ Fetches stack details from CloudFormation
2. ✅ Extracts all outputs (ARNs, URLs, IDs)
3. ✅ Identifies and extracts secrets from parameters
4. ✅ Stores secrets in AWS Secrets Manager
5. ✅ Creates Capistrano-style deployment structure
6. ✅ Generates git-safe config files

**Created structure:**
```
infra/
├── config/
│   ├── config.yml              # Git-safe config (secrets as {{secrets.key}})
│   ├── .env.example            # Template for environment variables
│   └── load-secrets.sh         # Script to load secrets from AWS
├── deploys/
│   ├── current -> releases/20251215-1030
│   ├── releases/
│   │   └── 20251215-1030/
│   │       ├── outputs.json    # Stack outputs (ARNs, URLs)
│   │       ├── manifest.json   # Deployment metadata
│   │       ├── resources.json  # All stack resources
│   │       └── deploy.log      # Import log
│   └── shared/                 # Persistent data across deployments
```

### 3. Import All Stacks (Bulk Import)

```bash
# Import all stacks in account
make infra-import-all

# Filter by prefix
python3 ../../shared/tools/infra-import.py --all --prefix my-project-
```

## Secrets Management

### Automatic Secret Detection

The import tool automatically detects secrets in:
- **Parameter names** containing: `password`, `secret`, `key`, `token`, `credential`, `api_key`
- **Parameter values** matching patterns:
  - AWS access keys: `AKIA...`
  - AWS secret keys: `[A-Za-z0-9+/]{40}`
  - API keys: `sk-...`
  - Long hex strings: `[a-f0-9]{32,}`

### Load Secrets in Your Environment

```bash
# Load secrets from AWS Secrets Manager
source infra/config/load-secrets.sh

# Verify secrets are loaded
env | grep -i secret
```

### Store New Secrets

```bash
# From .env file
make secrets-store SECRET_NAME=myproject/config SECRET_FILE=.env

# Manual storage
aws secretsmanager create-secret \
  --name myproject/config \
  --secret-string '{"DB_PASSWORD":"secret123","API_KEY":"sk-abc"}' \
  --profile admin-507745175693
```

## Git-Safe Configuration

### What Goes in Git ✅

```yaml
# infra/config/config.yml
project: my-api-stack
region: us-east-1
account_id: "507745175693"
database:
  host: db.example.com
  port: 5432
  password: "{{secrets.DB_PASSWORD}}"  # Secret reference
api:
  key: "{{secrets.API_KEY}}"            # Secret reference
```

### What Stays Out of Git ❌

```bash
# .env (local only)
DB_PASSWORD=actual_secret_value
API_KEY=sk-actual_key_value
```

### Recommended .gitignore

```gitignore
# Secrets and local config
.env
.env.local
*.pem
*.key

# Optional: Deployment history (large)
infra/deploys/releases/
!infra/deploys/releases/.gitkeep

# Keep current symlink for reference
!infra/deploys/current

# CDK artifacts
cdk.out/
*.js
*.d.ts
node_modules/
```

## Using Imported Outputs

### Access Stack Outputs (ARNs, URLs)

```bash
# Show all outputs
make infra-outputs

# Parse specific output
cat infra/deploys/current/outputs.json | jq -r '.ApiEndpoint.value'
```

**Example outputs.json:**
```json
{
  "ApiEndpoint": {
    "value": "https://api.example.com",
    "description": "API Gateway endpoint",
    "export_name": "MyApiEndpoint"
  },
  "DatabaseArn": {
    "value": "arn:aws:rds:us-east-1:507745175693:db:mydb",
    "description": "RDS database ARN"
  },
  "BucketName": {
    "value": "my-assets-bucket-abc123",
    "description": "S3 bucket for assets"
  }
}
```

### Reference in CDK Code

```typescript
// lib/stacks/my-stack.ts
import * as fs from 'fs';
import * as path from 'path';

// Load outputs from import
const deploysPath = path.join(__dirname, '../../deploys/current/outputs.json');
const outputs = JSON.parse(fs.readFileSync(deploysPath, 'utf-8'));

// Reference existing resources
const existingBucket = s3.Bucket.fromBucketName(
  this,
  'ImportedBucket',
  outputs.BucketName.value
);

const existingApi = apigateway.RestApi.fromRestApiId(
  this,
  'ImportedApi',
  outputs.ApiId.value
);
```

### Reference in Environment Variables

```bash
# infra/config/.env.example (template)
API_ENDPOINT={{outputs.ApiEndpoint.value}}
DATABASE_ARN={{outputs.DatabaseArn.value}}
BUCKET_NAME={{outputs.BucketName.value}}
DB_PASSWORD={{secrets.DB_PASSWORD}}
```

## Multi-Computer Workflow

### Initial Setup (Computer A)

```bash
# 1. Import infrastructure
make infra-import STACK=my-stack

# 2. Commit config to git
git add infra/config/config.yml
git add infra/config/.env.example
git add infra/config/load-secrets.sh
git commit -m "feat: Import infrastructure config"
git push
```

### Setup on Computer B

```bash
# 1. Pull config from git
git pull

# 2. Load secrets from AWS
source infra/config/load-secrets.sh

# 3. Start working
make infra-status
```

**No manual secret sharing needed!** Secrets are in AWS Secrets Manager.

## Deployment Workflow

### Deploy with Imported Config

```bash
# 1. Load secrets
source infra/config/load-secrets.sh

# 2. Deploy (secrets are auto-loaded)
make infra-deploy
```

### Check Deployment Status

```bash
# Show current deployment
make infra-status

# Show outputs
make infra-outputs
```

### Rollback to Previous Release

```bash
# List releases
make infra-rollback

# Rollback to specific release
make infra-rollback RELEASE=20251214-1520
```

## Advanced Usage

### Import with Custom Profile/Region

```bash
python3 ../../shared/tools/infra-import.py \
  --stack my-stack \
  --profile my-aws-profile \
  --region us-west-2
```

### Import Without Secrets Extraction

```bash
python3 ../../shared/tools/infra-import.py \
  --stack my-stack \
  --no-secrets
```

### Import to Custom Directory

```bash
python3 ../../shared/tools/infra-import.py \
  --stack my-stack \
  --output-dir /path/to/project
```

## Troubleshooting

### "Stack not found"

```bash
# Verify stack exists
aws cloudformation describe-stacks --stack-name my-stack

# Check different region
aws cloudformation describe-stacks --stack-name my-stack --region us-west-2
```

### "Permission denied" when accessing secrets

```bash
# Verify IAM permissions
aws iam get-user-policy \
  --user-name admin-programmatic \
  --policy-name SecretsManagerAccess

# Add SecretsManager permissions if needed
```

### Secrets not loading

```bash
# Debug secrets loader
bash -x infra/config/load-secrets.sh

# Manually test secret retrieval
aws secretsmanager get-secret-value \
  --secret-id myproject/config \
  --profile admin-507745175693
```

### Missing jq command

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Amazon Linux
sudo yum install jq
```

## Best Practices

### 1. Import Strategy
- ✅ Import all related stacks together (API + Database + Frontend)
- ✅ Use consistent naming: `myproject-api`, `myproject-db`, `myproject-web`
- ✅ Tag stacks with `Project` tag for easy filtering

### 2. Secrets Management
- ✅ Use AWS Secrets Manager for ALL secrets
- ✅ Rotate secrets regularly
- ✅ Never commit `.env` files to git
- ✅ Use `.env.example` as template for new developers

### 3. Git Workflow
- ✅ Commit config files (`config.yml`, `load-secrets.sh`)
- ✅ Optionally exclude `deploys/releases/` (can get large)
- ✅ Keep `deploys/current` symlink for reference
- ✅ Document required secrets in `.env.example`

### 4. Deployment History
- ✅ Keep last 5 releases (configurable in Makefile)
- ✅ Review `manifest.json` for deployment metadata
- ✅ Use `infra-status` to track current state

## Security Considerations

1. **Secrets are NEVER in git** - Only references like `{{secrets.KEY}}`
2. **AWS Secrets Manager** - Central, encrypted secret storage
3. **IAM Permissions** - Restrict who can read secrets
4. **Secret Rotation** - Regularly update secrets in Secrets Manager
5. **Audit Trail** - CloudTrail logs all secret access

## Next Steps

1. **Import your stacks**: `make infra-import STACK=...`
2. **Review config**: Check `infra/config/config.yml`
3. **Load secrets**: `source infra/config/load-secrets.sh`
4. **Commit to git**: `git add infra/config/ && git commit`
5. **Deploy**: `make infra-deploy`

---

**Questions?** See the main [README](../README.md) or run `make help`
