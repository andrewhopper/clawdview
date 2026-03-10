# Observability E2E Tests

Stub Playwright tests for verifying AWS X-Ray and CloudWatch integration.

## Overview

These tests ensure that all AWS projects have proper observability configured:

1. **CloudWatch Logs** - Application logs are captured and structured
2. **CloudWatch Metrics** - Custom metrics are published
3. **CloudWatch Alarms** - Error rate and latency alarms are configured
4. **X-Ray Tracing** - Distributed traces are captured with proper annotations

## Prerequisites

### AWS Permissions

Test account needs the following IAM permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricData",
        "cloudwatch:DescribeAlarms",
        "logs:GetLogEvents",
        "logs:FilterLogEvents",
        "logs:DescribeLogGroups",
        "xray:GetTraceSummaries",
        "xray:BatchGetTraces",
        "xray:GetServiceGraph"
      ],
      "Resource": "*"
    }
  ]
}
```

### Environment Variables

```bash
# AWS Configuration
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=<your-access-key>
export AWS_SECRET_ACCESS_KEY=<your-secret-key>

# Application Configuration
export APP_NAME=your-app-name
export ENVIRONMENT=dev  # dev, staging, prod

# Test Account (optional, see test-accounts.json)
export TEST_ADMIN_USERNAME=test-admin
export TEST_ADMIN_PASSWORD=<password>
```

## Usage

### Running Tests

```bash
# Install dependencies
npm install

# Run all observability tests
npx playwright test e2e/observability/

# Run CloudWatch tests only
npx playwright test e2e/observability/cloudwatch.spec.ts

# Run X-Ray tests only
npx playwright test e2e/observability/xray.spec.ts
```

### Implementing Tests

These are stub tests marked with `test.skip()`. To implement:

1. Remove `test.skip` and replace with `test`
2. Install AWS SDK v3:
   ```bash
   npm install @aws-sdk/client-cloudwatch @aws-sdk/client-cloudwatch-logs @aws-sdk/client-xray @aws-sdk/client-lambda
   ```
3. Implement the test logic following the TODO comments
4. Add appropriate wait times for eventual consistency

## Test Structure

```
e2e/observability/
├── README.md           # This file
├── cloudwatch.spec.ts  # CloudWatch logs, metrics, alarms tests
└── xray.spec.ts        # X-Ray tracing tests
```

## Required Configuration

Per `.guardrails/tech-preferences/infrastructure.json`, ALL AWS projects must have:

### CloudWatch

- Log groups with `/aws/{service}/{environment}/{app-name}` naming
- 30-day minimum log retention
- Custom metrics in `Protoflow/{AppName}` namespace
- Alarms for:
  - Error rate > 1% for 5 minutes
  - P99 latency > 3s for 5 minutes
  - 5xx responses > 10 in 5 minutes

### X-Ray

- Active tracing enabled on all Lambda functions
- Sampling: 1% for high-volume, 100% for low-volume services
- Required annotations: `user_id`, `request_id`, `environment`, `version`
- Subsegments for external API calls and database queries

## Related Files

- `/shared/standards/testing/test-accounts.json` - Test account configuration
- `/.guardrails/tech-preferences/infrastructure.json` - Infrastructure requirements
- `/.guardrails/tech-preferences/testing.json` - Testing framework preferences
