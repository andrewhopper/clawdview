<!-- File UUID: m6p5o4p3-6q7n-4o8p-0l3m-4f5g6h7i8j9l -->

# CDK Pre-Deployment Validation Tool

Validates AWS CDK deployments **before** provisioning resources using the new CloudFormation validation features (announced Nov 2025).

## Features

1. **CloudFormation Change Set Validation** (new Nov 2025)
   - Validates templates before provisioning
   - Catches invalid property syntax
   - Detects resource name conflicts
   - Checks S3 bucket emptiness constraints

2. **Resource Name Collision Detection**
   - Checks if resources with same names already exist
   - Prevents deployment failures

3. **S3 Bucket Validation**
   - Verifies bucket names are available
   - Warns about existing buckets

4. **Required Parameter Validation**
   - Checks all required parameters are provided
   - Validates environment variables

## Installation

```bash
npm install @lab/validate-cdk-deployment
```

Or use directly with `ts-node`:

```bash
npx ts-node shared/tools/validate-cdk-deployment.ts --stack-name my-stack
```

## Usage

### Command Line

```bash
# Basic usage (auto-finds template in cdk.out/)
validate-cdk-deployment --stack-name my-stack

# Specify custom template path
validate-cdk-deployment \
  --stack-name my-stack \
  --template path/to/template.json

# Specify region
validate-cdk-deployment \
  --stack-name my-stack \
  --region us-west-2

# Skip change set validation (faster, less thorough)
validate-cdk-deployment \
  --stack-name my-stack \
  --skip-change-set
```

### Integrated with CDK Deployment

Add to your `Makefile`:

```makefile
.PHONY: validate deploy

validate:
	@echo "Validating deployment..."
	@cdk synth --quiet > /dev/null
	@npx ts-node ../../shared/tools/validate-cdk-deployment.ts \
		--stack-name $(STACK_NAME) \
		--region $(AWS_REGION)

deploy: validate
	@echo "Validation passed. Deploying..."
	@cdk deploy --all --require-approval never
```

### Programmatic Usage

```typescript
import { validateDeployment } from '@lab/validate-cdk-deployment';

const result = await validateDeployment({
  stackName: 'my-stack',
  region: 'us-east-1',
  templatePath: 'cdk.out/my-stack.template.json',
});

if (!result.valid) {
  console.error('Validation failed:', result.errors);
  process.exit(1);
}

console.log('Validation passed!');
if (result.warnings.length > 0) {
  console.warn('Warnings:', result.warnings);
}
```

## Output Example

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Pre-Deployment Validation
   Stack: work-prod-auth
   Region: us-east-1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Template file found: cdk.out/work-prod-auth.template.json

[1/4] Creating CloudFormation change set for validation...
✓ CloudFormation change set validation passed

[2/4] Checking for resource name collisions...
✓ Stack exists with 12 resources

[3/4] Validating S3 bucket references...
✓ No S3 buckets to validate

[4/4] Validating required parameters...
✓ All required parameters provided

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Validation Summary
   Errors: 0
   Warnings: 0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Validation PASSED - safe to deploy
```

## Validation Checks

### 1. CloudFormation Change Set Validation

Uses the new CloudFormation validation API (Nov 2025) to catch:
- Invalid property syntax
- Resource name conflicts
- S3 bucket emptiness constraints
- Other template errors

**How it works:**
1. Creates a temporary change set
2. CloudFormation validates the template
3. Returns status: FAILED (with reason) or CREATE_COMPLETE
4. Deletes the temporary change set

**Benefits:**
- Catches errors **before** resource provisioning
- Reduces deployment cycle time from minutes to seconds
- Provides detailed error messages

### 2. Resource Name Collision Detection

Checks if the stack already exists and lists existing resources:
- If stack doesn't exist → No collisions possible
- If stack exists → Shows number of existing resources
- If resources conflict → CloudFormation change set will catch it

### 3. S3 Bucket Validation

For each S3 bucket in the template:
- Checks if bucket name is available
- Warns if bucket already exists
- Helps avoid deployment failures

### 4. Required Parameter Validation

Checks that all required CloudFormation parameters are provided:
- Via environment variables
- Via default values in template
- Errors if any parameters are missing

## Integration Examples

### With CDK Deploy

```typescript
// bin/app.ts
import { validateDeployment } from '@lab/validate-cdk-deployment';

async function deploy() {
  // Synthesize first
  console.log('Synthesizing CDK app...');
  execSync('cdk synth --quiet', { stdio: 'inherit' });

  // Validate
  console.log('Validating deployment...');
  const result = await validateDeployment({
    stackName: 'my-stack',
  });

  if (!result.valid) {
    console.error('Validation failed. Aborting deployment.');
    process.exit(1);
  }

  // Deploy
  console.log('Deploying...');
  execSync('cdk deploy --all', { stdio: 'inherit' });
}

deploy();
```

### With CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    steps:
      - name: Install dependencies
        run: npm install

      - name: Synthesize CDK
        run: npm run cdk synth

      - name: Validate deployment
        run: |
          npx ts-node shared/tools/validate-cdk-deployment.ts \
            --stack-name ${{ env.STACK_NAME }} \
            --region ${{ env.AWS_REGION }}

      - name: Deploy to AWS
        if: success()
        run: npm run cdk deploy
```

## Benefits

1. **Faster Feedback**: Catch errors in seconds vs minutes
2. **Cost Savings**: Avoid failed deployments that incur charges
3. **Better DX**: Clear error messages before deployment starts
4. **CI/CD Ready**: Easy integration with pipelines
5. **CloudFormation Native**: Uses official AWS validation API

## Comparison: Before vs After

**Before (without validation):**
```bash
$ cdk deploy
... 5 minutes pass ...
❌ CREATE_FAILED: UserPool already exists
```

**After (with validation):**
```bash
$ make validate
... 10 seconds pass ...
❌ Validation failed: Resource 'UserPool' already exists

$ make deploy
# Doesn't run - validation caught the error
```

## Requirements

- AWS CDK v2.0+
- AWS SDK v3
- Node.js 18+
- AWS credentials configured

## Related

- [CloudFormation Validation Announcement](https://aws.amazon.com/about-aws/whats-new/2025/11/cloudformation-dev-test-cycle-validation-troubleshooting/)
- [CDK Best Practices](https://docs.aws.amazon.com/cdk/latest/guide/best-practices.html)

## License

MIT
