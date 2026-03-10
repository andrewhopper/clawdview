<!-- File UUID: 6d3f8a2e-1b4d-4e8f-9c2a-5d6e7f8a9b0c -->

# SSM Resolver: Hierarchical Parameter Store

**Status:** Production Ready
**Version:** 1.0.0

Hierarchical SSM Parameter Store resolver with automatic fallback chain for AWS CDK and CLI tools.

---

## 1.0 Problem Solved

**Before:**
```typescript
// Hardcoded paths, duplication, no inheritance
const clientId1 = ssm.StringParameter.valueFromLookup(this, '/gocoder/dev/auth/cognito-client-id');
const clientId2 = ssm.StringParameter.valueFromLookup(this, '/gocoder/work/dev/cognito-client-id');
const clientId3 = ssm.StringParameter.valueFromLookup(this, '/ppm/work/prod/auth/cognito-client-id');
```

**After:**
```typescript
// Automatic resolution with fallback
const ssm = new SSMResolver(this, {
  accountType: 'work',
  environment: 'dev',
  project: 'gocoder',
});

const clientId = ssm.resolve('auth', 'cognito-client-id');
```

---

## 2.0 Namespace Structure

```
/{account-type}/{environment}/{project}/{category}/{key}
```

**Hierarchy:**

| Level | Examples | Purpose |
|-------|----------|---------|
| Account Type | work, personal, shared | Separate AWS accounts |
| Environment | dev, prod, beta, staging | Deploy environments |
| Project | gocoder, ppm, story-wizard | Project identifier |
| Category | auth, iot, features, secrets | Configuration grouping |
| Key | cognito-client-id, google-client-id | Specific parameter |

---

## 3.0 Automatic Fallback Chain

When resolving `/work/dev/gocoder/auth/google-client-id`:

```
1. /work/dev/gocoder/auth/google-client-id  ← Project override
2. /work/dev/auth/google-client-id          ← Environment default
3. /work/auth/google-client-id              ← Account default
4. /shared/auth/google-client-id            ← Global default
```

**Benefits:**
- No duplicate values (DRY)
- Projects inherit environment defaults
- Environments inherit account defaults
- Easy to override at any level

---

## 4.0 TypeScript Usage (AWS CDK)

### 4.1 Installation

```bash
cd shared/libs/ssm-resolver
npm install
npm run build
```

In your CDK project:
```json
{
  "dependencies": {
    "@protoflow/ssm-resolver": "file:../../../shared/libs/ssm-resolver"
  }
}
```

### 4.2 Basic Usage

```typescript
import { SSMResolver } from '@protoflow/ssm-resolver';
import * as cdk from 'aws-cdk-lib';

export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MyStackProps) {
    super(scope, id, props);

    // Create resolver
    const ssm = new SSMResolver(this, {
      accountType: 'work',
      environment: 'dev',
      project: 'gocoder',
    });

    // Resolve with fallback
    const userPoolId = ssm.resolve('auth/cognito', 'user-pool-id', {
      required: true,  // Throw if not found
      debug: true,     // Log resolution chain
    });

    // Read for runtime (Lambda env vars)
    const clientIdParam = ssm.fromName('auth', 'cognito-client-id');
    const clientId = clientIdParam.stringValue;

    // Write project-specific value
    ssm.write('auth', 'cognito-client-id', appClient.userPoolClientId);

    // Write environment-shared value
    ssm.write('iot', 'endpoint', iotEndpoint, {
      scope: 'environment',
      description: 'IoT Core endpoint for dev',
    });

    // Write secure parameter
    ssm.write('secrets', 'api-key', apiKey, {
      scope: 'project',
      secure: true,
    });

    // Grant Lambda read access
    ssm.grantRead(myLambda, 'auth', 'cognito-client-id');
  }
}
```

### 4.3 Path Generation

```typescript
const ssm = new SSMResolver(this, {
  accountType: 'work',
  environment: 'dev',
  project: 'gocoder',
});

// Get paths for different scopes
ssm.path('auth', 'client-id', 'project');      // /work/dev/gocoder/auth/client-id
ssm.path('auth', 'client-id', 'environment');  // /work/dev/auth/client-id
ssm.path('auth', 'client-id', 'account');      // /work/auth/client-id
ssm.path('auth', 'client-id', 'shared');       // /shared/auth/client-id
```

---

## 5.0 Python Usage (CLI Tools)

### 5.1 Basic Usage

```python
from ssm_resolver import SSMResolver

# Create resolver
resolver = SSMResolver(
    account_type='work',
    environment='dev',
    project='gocoder',
    debug=True
)

# Resolve with fallback
client_id = resolver.resolve('auth', 'google-client-id')
if client_id:
    print(f"Client ID: {client_id}")

# Required parameter (raises ValueError if not found)
user_pool_id = resolver.resolve('auth/cognito', 'user-pool-id', required=True)

# Write parameter
resolver.write('auth', 'cognito-client-id', 'us-east-1_ABC123')

# Write secure parameter
resolver.write('secrets', 'api-key', 'sk-...', secure=True, scope='project')

# Get path
path = resolver.path('auth', 'client-id', scope='project')
print(f"Path: {path}")
```

### 5.2 Command-Line Usage

```bash
# Resolve parameter
python3 shared/libs/ssm-resolver/ssm_resolver.py work dev gocoder auth google-client-id

# Output:
# [SSMResolver] Resolving auth/google-client-id
# [SSMResolver] Fallback chain:
#   - /work/dev/gocoder/auth/google-client-id
#   - /work/dev/auth/google-client-id
#   - /work/auth/google-client-id
#   - /shared/auth/google-client-id
# [SSMResolver] Found at: /work/auth/google-client-id
#
# Resolved value: 123456789.apps.googleusercontent.com
```

---

## 6.0 Migration Guide

### 6.1 Existing Projects

**Step 1: Install Resolver**
```bash
cd your-project/infra
npm install @protoflow/ssm-resolver
```

**Step 2: Update Stack**
```typescript
// Before
const userPoolId = ssm.StringParameter.valueFromLookup(
  this,
  '/protoflow/shared/cognito/user-pool-id'
);

// After
import { SSMResolver } from '@protoflow/ssm-resolver';

const ssm = new SSMResolver(this, {
  accountType: 'work',
  environment: 'dev',
  project: 'myproject',
});

const userPoolId = ssm.resolve('auth/cognito', 'user-pool-id', { required: true });
```

**Step 3: Migrate Parameters**
```bash
# See shared/tools/migrate-ssm-params.sh
./shared/tools/migrate-ssm-params.sh
```

---

## 7.0 Standard Paths Reference

### 7.1 Common Auth Parameters

```
/work/auth/cognito/user-pool-id          # Shared Cognito pool
/work/auth/cognito/user-pool-arn
/work/auth/cognito/domain
/work/dev/gocoder/auth/cognito-client-id # Project-specific client
```

### 7.2 Feature Flags

```
/work/dev/features/enable-google-oauth
/work/prod/features/enable-code-execution
```

### 7.3 Secrets

```
/work/dev/gocoder/secrets/test-user-password  # SecureString
/shared/secrets/anthropic-api-key             # Global secret
```

---

## 8.0 Benefits

1. **DRY:** No duplicate values across projects
2. **Inheritance:** Projects automatically use environment/account defaults
3. **Override:** Easy to override at any scope level
4. **Clarity:** Path structure shows ownership (project/env/account/shared)
5. **Consistency:** Single naming standard across all projects
6. **Debugging:** Built-in debug mode shows resolution chain

---

## 9.0 Testing

```bash
cd shared/libs/ssm-resolver
npm test
```

Example test:
```typescript
test('resolves with fallback chain', () => {
  const resolver = new SSMResolver(mockScope, {
    accountType: 'work',
    environment: 'dev',
    project: 'gocoder',
  });

  const chain = resolver.buildFallbackChain('auth', 'client-id');
  expect(chain).toEqual([
    '/work/dev/gocoder/auth/client-id',
    '/work/dev/auth/client-id',
    '/work/auth/client-id',
    '/shared/auth/client-id',
  ]);
});
```

---

## 10.0 Related Documentation

- Audit report: `docs/reports/SSM_NAMING_AUDIT.md`
- Migration script: `shared/tools/migrate-ssm-params.sh`
- AWS SSM reference: `.claude/docs/reference/AWS_SECRETS.md`

---

[END OF README]
