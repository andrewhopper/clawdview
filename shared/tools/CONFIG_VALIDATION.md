# Configuration Validation Tools

Two tools work together to prevent configuration issues from reaching production:

1. **Pre-commit validation** - Catches placeholder values before they're committed
2. **Post-deploy validation** - Verifies the app works after deployment

## Problem Statement

Common deployment issues that cost debugging time:

| Issue | Symptom | Solution |
|-------|---------|----------|
| Placeholder values committed | Cognito pool ID is `YOUR_POOL_ID` | Pre-commit hook |
| Wrong resource format | Numeric ID has letters `abc123` | Type validation |
| Stale deployment | Footer shows old git hash | Post-deploy hash check |
| OAuth broken | Login fails silently | Smoke test user auth |
| DNS not propagated | Domain doesn't resolve | Retry with backoff |
| CDN cache stale | Old version still served | Auto-invalidation |

## Tool 1: validate-deployment-config.py

**Purpose:** Catch invalid configurations before commit/deploy.

### Quick Start

```bash
# Validate a single file
python shared/tools/validate-deployment-config.py config.yaml

# Validate entire project
python shared/tools/validate-deployment-config.py --project .

# Pre-commit mode (strict, fails on any error)
python shared/tools/validate-deployment-config.py --pre-commit *.yaml

# With AWS resource verification
python shared/tools/validate-deployment-config.py config.yaml --verify-aws
```

### What It Checks

#### 1. Placeholder Detection

Catches common placeholder patterns:

| Pattern | Example | Severity |
|---------|---------|----------|
| `YOUR_*` | `YOUR_COGNITO_POOL_ID` | Error |
| `REPLACE_*` | `REPLACE_WITH_ACTUAL` | Error |
| `TODO` | `TODO: add value` | Error |
| `<placeholder>` | `<your-bucket>` | Error |
| `example-*` | `example-bucket` | Error |
| `000000000000` | Fake AWS account | Error |
| `123456789012` | Example AWS account | Error |

#### 2. AWS Resource Format Validation

Validates resource IDs match expected patterns:

| Resource Type | Pattern | Example |
|---------------|---------|---------|
| Cognito Pool ID | `[region]_[9 chars]` | `us-east-1_AbcDefGhi` |
| Cognito Client ID | `26 lowercase alphanumeric` | `1234567890abcdefghijklmnop` |
| AWS Account ID | `12 digits` | `507745175693` |
| ARN | `arn:aws:service:region:account:resource` | `arn:aws:s3:::my-bucket` |
| S3 Bucket | `3-63 lowercase, dots, hyphens` | `my-app-bucket-dev` |
| Region | `[2 letters]-[region]-[number]` | `us-east-1` |

#### 3. Key Name Inference

The validator infers expected types from key names:

```yaml
# These keys trigger validation:
cognito_user_pool_id: us-east-1_AbcDefGhi  # Validates as Cognito Pool ID
user_pool_client_id: abc123...              # Validates as Cognito Client ID
aws_account_id: 507745175693                # Validates as 12-digit account
bucket_name: my-bucket                      # Validates as S3 bucket name
table_arn: arn:aws:dynamodb:...             # Validates as ARN
```

### Pre-commit Integration

Already configured in `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: validate-deployment-config
      name: "🔧 Config Validation (no placeholders)"
      entry: python shared/tools/validate-deployment-config.py --pre-commit --quiet
      language: system
      types_or: [yaml, json]
```

Files excluded by default:
- `.example`, `.template`, `.sample` files
- Lock files (package-lock.json, etc.)
- Build outputs (node_modules, cdk.out, dist, etc.)

### Output Example

```
============================================================
📁 infra/config/auth.yaml
============================================================

❌ [no-placeholders] Placeholder value detected: Placeholder prefix YOUR_
   Path: cognito.user_pool_id
   Value: YOUR_POOL_ID
   Suggestion: Replace with actual value before committing

❌ [valid-cognito_client_id] Invalid Cognito App Client ID format
   Path: cognito.client_id
   Value: abc123
   Suggestion: Expected format: 1234567890abcdefghijklmnop

============================================================
📊 Summary: 2 errors, 0 warnings
============================================================

❌ Validation FAILED
```

---

## Tool 2: post-deploy-validate.py

**Purpose:** Verify the deployed application works correctly.

### Quick Start

```bash
# Basic validation
python shared/tools/post-deploy-validate.py --url https://app.example.com

# With expected git hash
python shared/tools/post-deploy-validate.py \
    --url https://app.example.com \
    --expected-hash abc1234

# With Cognito auth testing
python shared/tools/post-deploy-validate.py \
    --url https://app.example.com \
    --cognito-pool us-east-1_AbcDef123 \
    --cognito-client 1234567890abcdefghijklmnop

# Full validation with retry
python shared/tools/post-deploy-validate.py \
    --url https://app.example.com \
    --expected-hash abc1234 \
    --max-retries 5 \
    --retry-delay 300
```

### Validation Checks

| # | Check | What It Validates | Required? |
|---|-------|-------------------|-----------|
| 1 | DNS Resolution | Domain resolves to IP | Yes |
| 2 | URL Accessible | Returns HTTP 200 | Yes |
| 3 | SSL Certificate | Valid, not expiring | Yes |
| 4 | Git Hash | Matches expected version | If provided |
| 5 | Footer/Build Date | Contains recent date | Warning only |
| 6 | Health Endpoint | /health returns OK | Optional |
| 7 | Cognito Auth | Smoke test user can login | If configured |
| 8 | Page Render | Playwright - no JS errors | If available |

### Retry Logic

When validation fails, the tool:

1. Waits `--retry-delay` seconds (default: 60)
2. Attempts auto-fixes if enabled:
   - CloudFront cache invalidation for hash mismatch
3. Retries up to `--max-retries` times (default: 3)
4. Reports final pass/fail

This handles:
- DNS propagation delays
- CDN cache staleness
- CloudFront distribution updates

### Smoke Test User

For Cognito-authenticated apps, the validator:

1. Searches for existing `smoketest-*` user in the pool
2. If found, resets the password
3. If not found, creates a new user:
   - Email: `smoketest-abc123@smoketest.local`
   - Email verified: true
   - Permanent password set
4. Authenticates using USER_PASSWORD_AUTH flow

This ensures OAuth flows are actually working, not just returning 200.

### Auto-Fix Capabilities

| Issue | Auto-Fix Attempt |
|-------|------------------|
| Git hash mismatch | CloudFront invalidation |
| Stale cache | Wait and retry |
| DNS not resolved | Wait and retry |

### Output Example

```
============================================================
🔍 Post-Deployment Validation (Attempt 1/3)
   URL: https://app.example.com
   Time: 2025-01-15T10:30:00
============================================================

[1] Checking DNS resolution...
[2] Checking URL accessibility...
[3] Checking SSL certificate...
[4] Checking git hash...
[5] Checking footer/build date...
[6] Checking health endpoint...
[7] Checking Cognito authentication...
[8] Checking page render (Playwright)...

────────────────────────────────────────────────────────────
📊 Validation Results
────────────────────────────────────────────────────────────
✅ DNS Resolution: Domain app.example.com resolves to 52.1.2.3
✅ URL Accessible: URL returns HTTP 200
✅ SSL Certificate: SSL certificate valid (45 days remaining)
✅ Git Hash: Git hash matches: abc1234
✅ Footer/Build Date: Build date is recent: 2025-01-15 (0 days ago)
⏭️ Health Endpoint: No health endpoint found
✅ Cognito Auth: Authentication successful for smoketest-xyz@smoketest.local
✅ Page Render: Page renders correctly (title: My App)

📈 Summary: 6/8 passed, 0 failed, 0 warnings, 2 skipped

✅ All validation checks PASSED!
```

---

## Makefile Integration

Add to your project Makefile:

```makefile
# Required
DEPLOY_URL := https://your-app.example.com

# Optional
COGNITO_POOL_ID := us-east-1_AbcDef123
COGNITO_CLIENT_ID := 1234567890abcdefghijklmnop
MAX_RETRIES := 3
RETRY_DELAY := 60

# These targets are defined in the standard template:
# - validate-config (runs before infra-deploy)
# - post-deploy-validate (runs after infra-deploy)
# - validate-deployment (quick check, no retry)
```

The flow:
```
make infra-deploy
    │
    ├─► validate-config (pre-deploy)
    │   └─► Fails fast if placeholders found
    │
    ├─► CDK deploy
    │
    └─► post-deploy-validate (post-deploy)
        ├─► Waits 30s for propagation
        ├─► Runs all checks
        ├─► If fail: auto-fix + retry (up to 3x)
        └─► Reports final result
```

---

## Requirements

### Python Dependencies

```bash
pip install pyyaml requests boto3
```

### Optional: Playwright

For page render validation:

```bash
npm install -D playwright
npx playwright install chromium
```

### AWS Credentials

For `--verify-aws` and Cognito testing:

```bash
export AWS_PROFILE=your-profile
# or
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

---

## Best Practices

1. **Always use canonical domains** in `DEPLOY_URL`, not CloudFront/Amplify URLs
2. **Set expected git hash** to catch stale deployments
3. **Configure Cognito credentials** for auth-required apps
4. **Increase retry delay** for DNS-heavy changes (new domains)
5. **Run `pre-commit install`** to enable automatic config validation
