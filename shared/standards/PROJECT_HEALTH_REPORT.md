# Project Health Report Template

<!-- File UUID: 8f3a2c1d-4e5b-6a7c-9d0e-1f2b3c4d5e6f -->

## Overview

This document defines the standard format for project health reports. Each project should maintain a `HEALTH.md` or `health.json` file in its root directory.

---

## Report Dimensions

### 1. Deployment Status by Environment

| Environment | Last Deployed | Git Hash | Deployed By | Status |
|-------------|---------------|----------|-------------|--------|
| **Work** | | | | |
| └─ dev | 2026-01-20 14:32 | `a1b2c3d` | CI/CD | ✅ healthy |
| └─ stage | 2026-01-19 09:15 | `e4f5g6h` | CI/CD | ✅ healthy |
| └─ prod | 2026-01-15 16:45 | `i7j8k9l` | manual | ✅ healthy |
| **Personal** | | | | |
| └─ dev | 2026-01-21 11:00 | `m0n1o2p` | CI/CD | ✅ healthy |
| └─ stage | 2026-01-18 08:30 | `q3r4s5t` | CI/CD | ⚠️ stale |
| └─ prod | 2026-01-10 12:00 | `u6v7w8x` | manual | ✅ healthy |

**Status Legend:**
- ✅ healthy - deployed within policy window
- ⚠️ stale - deployed > 7 days ago (configurable)
- ❌ unhealthy - deployment failed or unavailable
- 🔄 deploying - deployment in progress

---

### 2. Configuration Method

| Category | Method | Location | Notes |
|----------|--------|----------|-------|
| **Secrets** | | | |
| └─ API Keys | SSM | `/app/{env}/api-keys/*` | ✅ secure |
| └─ DB Credentials | SSM | `/app/{env}/db/*` | ✅ secure |
| └─ JWT Secret | SSM | `/app/{env}/jwt-secret` | ✅ secure |
| **Config** | | | |
| └─ Feature Flags | Env Vars | `FEATURE_*` | ✅ ok |
| └─ Log Level | Env Vars | `LOG_LEVEL` | ✅ ok |
| └─ API URLs | Env Vars | `API_BASE_URL` | ✅ ok |
| **Warnings** | | | |
| └─ DB Host | ⚠️ Hardcoded | `src/config.ts:42` | migrate to env var |
| └─ Region | ⚠️ Hardcoded | `infra/stack.ts:15` | migrate to env var |

**Method Legend:**
- **SSM** - AWS Systems Manager Parameter Store (preferred for secrets)
- **Secrets Manager** - AWS Secrets Manager (for rotation-enabled secrets)
- **Env Vars** - Environment variables (ok for non-secret config)
- **Hardcoded** - ⚠️ Values in source code (should be migrated)

---

### 3. Infrastructure Health

| Resource | Work Dev | Work Stage | Work Prod | Personal Dev |
|----------|----------|------------|-----------|--------------|
| CloudFront | ✅ | ✅ | ✅ | ✅ |
| S3 Bucket | ✅ | ✅ | ✅ | ✅ |
| Lambda | ✅ | ✅ | ✅ | n/a |
| RDS | ✅ | ✅ | ✅ | n/a |
| Cognito | ✅ | ✅ | ✅ | ✅ |

---

### 4. Dependency Health

| Dependency | Current | Latest | Status |
|------------|---------|--------|--------|
| next | 15.0.3 | 15.1.0 | ⚠️ minor update |
| react | 19.0.0 | 19.0.0 | ✅ current |
| typescript | 5.6.3 | 5.7.0 | ⚠️ minor update |
| @aws-cdk/core | 2.170.0 | 2.175.0 | ⚠️ minor update |

---

### 5. Security Posture

#### 5.1 Code Security Scans

| Check | Status | Last Scanned |
|-------|--------|--------------|
| npm audit | ✅ 0 vulnerabilities | 2026-01-21 |
| Secrets scan | ✅ no leaks | 2026-01-21 |
| SAST | ✅ passed | 2026-01-20 |
| License compliance | ✅ passed | 2026-01-15 |

#### 5.2 S3 Bucket Policies

| Bucket | Public Access | Bucket Policy | ACL | Status |
|--------|---------------|---------------|-----|--------|
| `app-assets-prod` | ❌ blocked | ✅ least privilege | ❌ disabled | ✅ secure |
| `app-uploads-prod` | ❌ blocked | ✅ least privilege | ❌ disabled | ✅ secure |
| `app-logs-prod` | ❌ blocked | ✅ CloudTrail only | ❌ disabled | ✅ secure |
| `app-static-dev` | ⚠️ allowed | ⚠️ public read | ⚠️ public | ⚠️ review |

**S3 Policy Checks:**
- [ ] Block Public Access enabled (account + bucket level)
- [ ] Bucket policy follows least privilege
- [ ] ACLs disabled (use policies instead)
- [ ] No `s3:*` wildcard permissions
- [ ] Cross-account access explicitly defined
- [ ] VPC endpoint policy (if applicable)

#### 5.3 API Security Policies

| API | Auth Method | Authorization | Rate Limit | WAF | Status |
|-----|-------------|---------------|------------|-----|--------|
| REST API (prod) | Cognito JWT | IAM policy | 1000/min | ✅ enabled | ✅ secure |
| REST API (dev) | API Key | None | 100/min | ❌ disabled | ⚠️ review |
| WebSocket API | Cognito JWT | Lambda auth | 500/min | ✅ enabled | ✅ secure |
| GraphQL | Cognito JWT | Field-level | 500/min | ✅ enabled | ✅ secure |

**API Policy Checks:**
- [ ] Authentication required (Cognito, IAM, API Key)
- [ ] Authorization enforced (not just authentication)
- [ ] Rate limiting configured
- [ ] WAF attached (prod environments)
- [ ] CORS properly configured
- [ ] Input validation enabled
- [ ] No wildcard (`*`) resource permissions
- [ ] Lambda authorizer timeout < 30s

**Lambda Execution Policies:**

| Function | IAM Role | Permissions | Status |
|----------|----------|-------------|--------|
| `api-handler` | `app-lambda-role` | ✅ least privilege | ✅ secure |
| `data-processor` | `app-processor-role` | ✅ least privilege | ✅ secure |
| `admin-function` | `app-admin-role` | ⚠️ broad S3 access | ⚠️ review |

#### 5.4 Encryption Status

| Resource | At Rest | In Transit | Key Management | Status |
|----------|---------|------------|----------------|--------|
| **S3 Buckets** | | | | |
| └─ app-assets-prod | ✅ SSE-KMS | ✅ TLS 1.2+ | CMK | ✅ secure |
| └─ app-uploads-prod | ✅ SSE-KMS | ✅ TLS 1.2+ | CMK | ✅ secure |
| └─ app-logs-prod | ✅ SSE-S3 | ✅ TLS 1.2+ | AWS managed | ✅ ok |
| └─ app-static-dev | ❌ none | ✅ TLS 1.2+ | n/a | ⚠️ review |
| **Databases** | | | | |
| └─ RDS (prod) | ✅ AES-256 | ✅ TLS 1.2+ | CMK | ✅ secure |
| └─ DynamoDB (prod) | ✅ AES-256 | ✅ TLS 1.2+ | CMK | ✅ secure |
| └─ RDS (dev) | ✅ AES-256 | ✅ TLS 1.2+ | AWS managed | ✅ ok |
| **Secrets** | | | | |
| └─ SSM Parameters | ✅ KMS | ✅ TLS 1.2+ | CMK | ✅ secure |
| └─ Secrets Manager | ✅ KMS | ✅ TLS 1.2+ | CMK | ✅ secure |
| **Messaging** | | | | |
| └─ SQS Queues | ✅ SSE-KMS | ✅ TLS 1.2+ | CMK | ✅ secure |
| └─ SNS Topics | ✅ SSE-KMS | ✅ TLS 1.2+ | CMK | ✅ secure |
| **Compute** | | | | |
| └─ EBS Volumes | ✅ AES-256 | n/a | CMK | ✅ secure |
| └─ Lambda env vars | ✅ KMS | ✅ TLS 1.2+ | CMK | ✅ secure |

**Encryption Legend:**
- **SSE-S3** - Server-side encryption with S3-managed keys (baseline)
- **SSE-KMS** - Server-side encryption with KMS (preferred)
- **CMK** - Customer Managed Key (most control)
- **AWS managed** - AWS managed key (less control, still encrypted)

**Encryption Checks:**
- [ ] All S3 buckets encrypted at rest
- [ ] All databases encrypted at rest
- [ ] TLS 1.2+ enforced for all connections
- [ ] No unencrypted EBS volumes
- [ ] KMS keys have rotation enabled
- [ ] Lambda environment variables encrypted
- [ ] Secrets use SSM SecureString or Secrets Manager

---

## JSON Schema

For programmatic access, projects can also maintain `health.json`:

```json
{
  "$schema": "https://protoflow.dev/schemas/health-report.json",
  "version": "1.0.0",
  "project": {
    "name": "example-project",
    "uuid": "abc12345"
  },
  "generated_at": "2026-01-21T15:30:00Z",
  "environments": {
    "work": {
      "dev": {
        "last_deployed": "2026-01-20T14:32:00Z",
        "git_hash": "a1b2c3d4e5f6g7h8i9j0",
        "git_hash_short": "a1b2c3d",
        "deployed_by": "ci/cd",
        "status": "healthy",
        "url": "https://dev.example.work.com"
      },
      "stage": {
        "last_deployed": "2026-01-19T09:15:00Z",
        "git_hash": "e4f5g6h7i8j9k0l1m2n3",
        "git_hash_short": "e4f5g6h",
        "deployed_by": "ci/cd",
        "status": "healthy",
        "url": "https://stage.example.work.com"
      },
      "prod": {
        "last_deployed": "2026-01-15T16:45:00Z",
        "git_hash": "i7j8k9l0m1n2o3p4q5r6",
        "git_hash_short": "i7j8k9l",
        "deployed_by": "manual",
        "status": "healthy",
        "url": "https://example.work.com"
      }
    },
    "personal": {
      "dev": {
        "last_deployed": "2026-01-21T11:00:00Z",
        "git_hash": "m0n1o2p3q4r5s6t7u8v9",
        "git_hash_short": "m0n1o2p",
        "deployed_by": "ci/cd",
        "status": "healthy",
        "url": "https://dev.example.personal.com"
      },
      "stage": {
        "last_deployed": "2026-01-18T08:30:00Z",
        "git_hash": "q3r4s5t6u7v8w9x0y1z2",
        "git_hash_short": "q3r4s5t",
        "deployed_by": "ci/cd",
        "status": "stale",
        "url": "https://stage.example.personal.com"
      },
      "prod": {
        "last_deployed": "2026-01-10T12:00:00Z",
        "git_hash": "u6v7w8x9y0z1a2b3c4d5",
        "git_hash_short": "u6v7w8x",
        "deployed_by": "manual",
        "status": "healthy",
        "url": "https://example.personal.com"
      }
    }
  },
  "configuration": {
    "secrets": {
      "method": "ssm",
      "path_pattern": "/app/{env}/*",
      "items": [
        { "name": "api-keys", "method": "ssm", "path": "/app/{env}/api-keys/*" },
        { "name": "db-credentials", "method": "ssm", "path": "/app/{env}/db/*" },
        { "name": "jwt-secret", "method": "ssm", "path": "/app/{env}/jwt-secret" }
      ]
    },
    "config": {
      "method": "env_vars",
      "items": [
        { "name": "feature-flags", "method": "env_vars", "pattern": "FEATURE_*" },
        { "name": "log-level", "method": "env_vars", "var": "LOG_LEVEL" },
        { "name": "api-urls", "method": "env_vars", "var": "API_BASE_URL" }
      ]
    },
    "warnings": [
      {
        "name": "db-host",
        "method": "hardcoded",
        "location": "src/config.ts:42",
        "recommendation": "migrate to env var"
      },
      {
        "name": "region",
        "method": "hardcoded",
        "location": "infra/stack.ts:15",
        "recommendation": "migrate to env var"
      }
    ]
  },
  "infrastructure": {
    "work_dev": { "cloudfront": "healthy", "s3": "healthy", "lambda": "healthy", "rds": "healthy", "cognito": "healthy" },
    "work_stage": { "cloudfront": "healthy", "s3": "healthy", "lambda": "healthy", "rds": "healthy", "cognito": "healthy" },
    "work_prod": { "cloudfront": "healthy", "s3": "healthy", "lambda": "healthy", "rds": "healthy", "cognito": "healthy" },
    "personal_dev": { "cloudfront": "healthy", "s3": "healthy", "lambda": "n/a", "rds": "n/a", "cognito": "healthy" }
  },
  "dependencies": {
    "outdated": [
      { "name": "next", "current": "15.0.3", "latest": "15.1.0", "type": "minor" },
      { "name": "typescript", "current": "5.6.3", "latest": "5.7.0", "type": "minor" },
      { "name": "@aws-cdk/core", "current": "2.170.0", "latest": "2.175.0", "type": "minor" }
    ],
    "security_vulnerabilities": 0
  },
  "security": {
    "code_scans": {
      "npm_audit": { "status": "passed", "vulnerabilities": 0, "last_scanned": "2026-01-21T00:00:00Z" },
      "secrets_scan": { "status": "passed", "leaks_found": 0, "last_scanned": "2026-01-21T00:00:00Z" },
      "sast": { "status": "passed", "last_scanned": "2026-01-20T00:00:00Z" },
      "license_compliance": { "status": "passed", "last_scanned": "2026-01-15T00:00:00Z" }
    },
    "s3_policies": [
      {
        "bucket": "app-assets-prod",
        "public_access_blocked": true,
        "bucket_policy": "least_privilege",
        "acl_disabled": true,
        "status": "secure"
      },
      {
        "bucket": "app-static-dev",
        "public_access_blocked": false,
        "bucket_policy": "public_read",
        "acl_disabled": false,
        "status": "review"
      }
    ],
    "api_policies": [
      {
        "api": "REST API (prod)",
        "auth_method": "cognito_jwt",
        "authorization": "iam_policy",
        "rate_limit": "1000/min",
        "waf_enabled": true,
        "cors_configured": true,
        "status": "secure"
      },
      {
        "api": "REST API (dev)",
        "auth_method": "api_key",
        "authorization": "none",
        "rate_limit": "100/min",
        "waf_enabled": false,
        "cors_configured": true,
        "status": "review"
      }
    ],
    "lambda_policies": [
      {
        "function": "api-handler",
        "iam_role": "app-lambda-role",
        "permissions": "least_privilege",
        "status": "secure"
      }
    ],
    "encryption": {
      "s3": [
        { "bucket": "app-assets-prod", "at_rest": "SSE-KMS", "in_transit": "TLS1.2+", "key_management": "CMK", "status": "secure" },
        { "bucket": "app-static-dev", "at_rest": "none", "in_transit": "TLS1.2+", "key_management": "n/a", "status": "review" }
      ],
      "databases": [
        { "resource": "RDS (prod)", "at_rest": "AES-256", "in_transit": "TLS1.2+", "key_management": "CMK", "status": "secure" },
        { "resource": "DynamoDB (prod)", "at_rest": "AES-256", "in_transit": "TLS1.2+", "key_management": "CMK", "status": "secure" }
      ],
      "secrets": [
        { "resource": "SSM Parameters", "at_rest": "KMS", "in_transit": "TLS1.2+", "key_management": "CMK", "status": "secure" },
        { "resource": "Secrets Manager", "at_rest": "KMS", "in_transit": "TLS1.2+", "key_management": "CMK", "status": "secure" }
      ],
      "messaging": [
        { "resource": "SQS Queues", "at_rest": "SSE-KMS", "in_transit": "TLS1.2+", "key_management": "CMK", "status": "secure" },
        { "resource": "SNS Topics", "at_rest": "SSE-KMS", "in_transit": "TLS1.2+", "key_management": "CMK", "status": "secure" }
      ],
      "compute": [
        { "resource": "EBS Volumes", "at_rest": "AES-256", "in_transit": "n/a", "key_management": "CMK", "status": "secure" },
        { "resource": "Lambda env vars", "at_rest": "KMS", "in_transit": "TLS1.2+", "key_management": "CMK", "status": "secure" }
      ]
    }
  }
}
```

---

## Usage

### Generate Report

```bash
# From project root
make health-report

# Or manually
bin/generate-health-report.py --output HEALTH.md
```

### CI/CD Integration

Add to your pipeline:

```yaml
# .github/workflows/health.yml
- name: Generate Health Report
  run: make health-report

- name: Upload Report
  uses: actions/upload-artifact@v3
  with:
    name: health-report
    path: HEALTH.md
```

---

## Configuration Detection Heuristics

The health report generator uses these heuristics to detect configuration methods:

| Pattern | Detected Method |
|---------|-----------------|
| `process.env.AWS_*` | Env Vars |
| `ssm.getParameter()` | SSM |
| `secretsManager.getSecretValue()` | Secrets Manager |
| Literal strings in config (URLs, credentials) | Hardcoded ⚠️ |
| `.env` files committed | Hardcoded ⚠️ |
| `const API_KEY = "sk-..."` | Hardcoded ⚠️ |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-22 | Added S3 policies, API policies, encryption status |
| 1.0.0 | 2026-01-21 | Initial template |
