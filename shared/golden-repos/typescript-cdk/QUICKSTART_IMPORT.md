# Quick Start: Import Existing Infrastructure

Import your existing AWS infrastructure into the Capistrano-style deployment structure in 3 steps.

## Prerequisites

- AWS CLI configured with `admin-507745175693` profile
- Python 3.7+ with boto3 (`pip3 install boto3 pyyaml`)
- jq installed (`brew install jq`)

## Step 1: List Your Stacks

```bash
cd /path/to/your/project

# Copy Makefile from golden repo
cp /Users/andyhop/dev/protoflow/shared/golden-repos/typescript-cdk/Makefile .

# List all CloudFormation stacks
make infra-import-list
```

**Example output:**
```
📋 CloudFormation Stacks (8):

   • my-api-production
     Status: UPDATE_COMPLETE
     Updated: 2025-12-15 10:30:00

   • my-web-frontend-prod
     Status: CREATE_COMPLETE
     Updated: 2025-12-14 15:20:00
```

## Step 2: Import a Stack

```bash
# Import single stack
make infra-import STACK=my-api-production
```

**What you'll see:**
```
📥 Importing stack: my-api-production

📦 Importing stack: my-api-production
   Stack ID: arn:aws:cloudformation:us-east-1:507745175693:stack/...
   Status: UPDATE_COMPLETE
   Resources: 24
   Outputs: 5
   Secrets: 3 stored in Secrets Manager
   ✓ Created release: infra/deploys/releases/20251215-1430
   ✓ Created config files in infra/config

✓ Import complete: my-api-production
```

**Created structure:**
```
your-project/
├── infra/
│   ├── config/
│   │   ├── config.yml           # ✅ Git-safe (commit this)
│   │   ├── .env.example         # ✅ Template (commit this)
│   │   └── load-secrets.sh      # ✅ Secrets loader (commit this)
│   └── deploys/
│       ├── current -> releases/20251215-1430
│       ├── releases/
│       │   └── 20251215-1430/
│       │       ├── outputs.json  # ARNs, URLs, IDs
│       │       ├── manifest.json
│       │       ├── resources.json
│       │       └── deploy.log
│       └── shared/
```

## Step 3: Use the Outputs

### View Stack Outputs (ARNs, URLs)

```bash
make infra-outputs
```

**Example output:**
```json
{
  "ApiEndpoint": {
    "value": "https://abc123.execute-api.us-east-1.amazonaws.com/prod",
    "description": "API Gateway endpoint"
  },
  "DatabaseArn": {
    "value": "arn:aws:rds:us-east-1:507745175693:db:mydb",
    "description": "RDS database ARN"
  },
  "BucketName": {
    "value": "my-assets-bucket-xyz789",
    "description": "S3 bucket for assets"
  }
}
```

### Access in Your Code

#### TypeScript/Node.js
```typescript
import * as fs from 'fs';
import * as path from 'path';

// Load imported outputs
const outputsPath = path.join(__dirname, '../deploys/current/outputs.json');
const outputs = JSON.parse(fs.readFileSync(outputsPath, 'utf-8'));

console.log('API Endpoint:', outputs.ApiEndpoint.value);
console.log('Bucket Name:', outputs.BucketName.value);
```

#### CDK Stack
```typescript
// Reference existing resources
import { Bucket } from 'aws-cdk-lib/aws-s3';

const outputs = JSON.parse(
  fs.readFileSync('../deploys/current/outputs.json', 'utf-8')
);

const existingBucket = Bucket.fromBucketName(
  this,
  'ImportedBucket',
  outputs.BucketName.value
);
```

#### Shell Script
```bash
#!/bin/bash
API_ENDPOINT=$(cat infra/deploys/current/outputs.json | jq -r '.ApiEndpoint.value')
echo "Calling API: $API_ENDPOINT"
curl "$API_ENDPOINT/health"
```

### Load Secrets

```bash
# Load secrets from AWS Secrets Manager
source infra/config/load-secrets.sh

# Now you can use environment variables
echo $DB_PASSWORD
echo $API_KEY
```

## Multi-Computer Setup

### Computer A (Initial Setup)
```bash
# 1. Import infrastructure
make infra-import STACK=my-api-production

# 2. Commit config to git (NOT secrets!)
git add infra/config/config.yml
git add infra/config/.env.example
git add infra/config/load-secrets.sh
git add .gitignore
git commit -m "feat: Import infrastructure config"
git push
```

### Computer B (Clone & Use)
```bash
# 1. Clone repo
git clone ...
cd project

# 2. Load secrets from AWS (no manual sharing!)
source infra/config/load-secrets.sh

# 3. View outputs
make infra-outputs
```

## Common Use Cases

### 1. Reference Existing API Gateway in New CDK Stack

```typescript
// lib/stacks/new-stack.ts
import { RestApi } from 'aws-cdk-lib/aws-apigateway';

const outputs = JSON.parse(
  fs.readFileSync('../deploys/current/outputs.json', 'utf-8')
);

const existingApi = RestApi.fromRestApiId(
  this,
  'ExistingApi',
  outputs.ApiId.value
);

// Add new resources to existing API
existingApi.root.addResource('new-endpoint');
```

### 2. Connect to Existing Database

```typescript
// lib/stacks/lambda-stack.ts
const outputs = JSON.parse(
  fs.readFileSync('../deploys/current/outputs.json', 'utf-8')
);

const lambda = new Function(this, 'MyFunction', {
  environment: {
    DATABASE_ARN: outputs.DatabaseArn.value,
    DATABASE_ENDPOINT: outputs.DatabaseEndpoint.value,
  },
});
```

### 3. Use Existing S3 Bucket

```typescript
// lib/stacks/frontend-stack.ts
const outputs = JSON.parse(
  fs.readFileSync('../deploys/current/outputs.json', 'utf-8')
);

const assetsBucket = Bucket.fromBucketName(
  this,
  'AssetsBucket',
  outputs.BucketName.value
);

// Grant access to new resources
assetsBucket.grantRead(myLambda);
```

## Troubleshooting

### "Stack not found"
```bash
# Check region
aws cloudformation list-stacks --region us-east-1 --profile admin-507745175693

# Try different region
make infra-import STACK=my-stack AWS_REGION=us-west-2
```

### "Permission denied" accessing secrets
```bash
# Verify AWS credentials
aws sts get-caller-identity --profile admin-507745175693

# Check Secrets Manager permissions
aws secretsmanager list-secrets --profile admin-507745175693
```

### "jq: command not found"
```bash
# macOS
brew install jq

# Ubuntu
sudo apt-get install jq
```

## Next Steps

1. ✅ Import your stacks
2. ✅ Review `infra/config/config.yml`
3. ✅ Load secrets with `source infra/config/load-secrets.sh`
4. ✅ Commit config files to git
5. ✅ Use outputs in your code

**Full documentation:** [docs/INFRASTRUCTURE_IMPORT.md](docs/INFRASTRUCTURE_IMPORT.md)

**Makefile help:** `make help`
