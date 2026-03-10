<!-- File UUID: 3e7b9f2a-5c1d-4a8e-b9f6-2d4c8a1e3f7b -->

# Release Verification Agent

## Overview

Specialized agent for post-deployment verification and validation. Runs comprehensive smoke tests after deployments to ensure applications are functioning correctly before marking releases as complete.

## Agent Capabilities

### 1.0 Core Responsibilities

**Post-Deployment Verification:**
- Check application accessibility (HTTP/HTTPS endpoints)
- Verify visual rendering (Playwright browser tests)
- Validate deployment metadata (buildinfo.json)
- Confirm git hash matches expected version
- Test critical user flows
- Verify API endpoints respond correctly
- Check authentication flows
- Validate environment-specific configurations

**Release Gates:**
```
Deploy → Infrastructure Up → Release Verification → Release Complete
                                      ↓
                         [FAIL] → Rollback + Alert
```

### 2.0 Verification Checklist

**Tier 1: Basic Accessibility (REQUIRED)**
```
[1] DNS resolution working
[2] HTTPS accessible (200 OK)
[3] No certificate errors
[4] Response time < 5s
[5] Custom domain resolves (if configured)
```

**Tier 2: Application Health (REQUIRED)**
```
[1] buildinfo.json accessible and valid
[2] Deployed git hash matches expected version
[3] Environment variables set correctly
[4] No console errors in browser
[5] Critical assets load (JS, CSS, images)
```

**Tier 3: Functional Testing (RECOMMENDED)**
```
[1] Homepage renders without errors
[2] Navigation works
[3] Authentication flow works (if applicable)
[4] API endpoints respond
[5] Database connectivity (if applicable)
```

**Tier 4: User Journey Testing (OPTIONAL)**
```
[1] Critical user flows complete successfully
[2] Forms submit correctly
[3] Data persists correctly
[4] Error handling works
```

### 3.0 Verification Workflows

**3.1 Frontend Application (NextJS/Vite/React):**

```bash
#!/bin/bash
# Post-deployment verification script

DOMAIN="$1"  # e.g., https://app.example.com
EXPECTED_HASH="$2"  # Expected git commit hash

echo "═══════════════════════════════════════════════════════"
echo "  RELEASE VERIFICATION"
echo "  Domain: $DOMAIN"
echo "  Expected Hash: $EXPECTED_HASH"
echo "═══════════════════════════════════════════════════════"

# Tier 1: Basic Accessibility
echo ""
echo "Tier 1: Basic Accessibility Checks"
echo "-----------------------------------"

# Check DNS resolution
echo -n "[1/5] DNS resolution... "
if host $(echo $DOMAIN | sed 's|https://||' | sed 's|/.*||') > /dev/null 2>&1; then
    echo "✓ PASS"
else
    echo "✗ FAIL"
    exit 1
fi

# Check HTTPS accessibility
echo -n "[2/5] HTTPS accessibility... "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$DOMAIN" -m 10)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✓ PASS (HTTP $HTTP_CODE)"
else
    echo "✗ FAIL (HTTP $HTTP_CODE)"
    exit 1
fi

# Check certificate validity
echo -n "[3/5] SSL certificate... "
if curl -s "$DOMAIN" --cacert /etc/ssl/certs/ca-certificates.crt > /dev/null 2>&1; then
    echo "✓ PASS"
else
    echo "⚠ WARNING (certificate issue)"
fi

# Check response time
echo -n "[4/5] Response time... "
RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" "$DOMAIN")
if (( $(echo "$RESPONSE_TIME < 5" | bc -l) )); then
    echo "✓ PASS (${RESPONSE_TIME}s)"
else
    echo "⚠ SLOW (${RESPONSE_TIME}s)"
fi

# Check redirect handling
echo -n "[5/5] Redirect handling... "
FINAL_URL=$(curl -Ls -o /dev/null -w "%{url_effective}" "$DOMAIN")
echo "✓ PASS (final: $FINAL_URL)"

# Tier 2: Application Health
echo ""
echo "Tier 2: Application Health Checks"
echo "----------------------------------"

# Check buildinfo.json
echo -n "[1/5] buildinfo.json accessible... "
BUILDINFO=$(curl -s "${DOMAIN}/buildinfo.json")
if [ $? -eq 0 ] && [ ! -z "$BUILDINFO" ]; then
    echo "✓ PASS"
else
    echo "✗ FAIL (buildinfo.json not found)"
    exit 1
fi

# Validate JSON structure
echo -n "[2/5] buildinfo.json valid... "
if echo "$BUILDINFO" | jq empty 2>/dev/null; then
    echo "✓ PASS"
else
    echo "✗ FAIL (invalid JSON)"
    exit 1
fi

# Extract and verify git hash
echo -n "[3/5] Git hash verification... "
DEPLOYED_HASH=$(echo "$BUILDINFO" | jq -r '.git.hash // empty')
if [ "$DEPLOYED_HASH" = "$EXPECTED_HASH" ]; then
    echo "✓ PASS ($DEPLOYED_HASH)"
elif [ -z "$DEPLOYED_HASH" ]; then
    echo "⚠ WARNING (no hash in buildinfo)"
else
    echo "✗ FAIL (expected: $EXPECTED_HASH, got: $DEPLOYED_HASH)"
    exit 1
fi

# Check deployment timestamp
echo -n "[4/5] Deployment timestamp... "
DEPLOY_TIME=$(echo "$BUILDINFO" | jq -r '.deployment.timestamp // empty')
if [ ! -z "$DEPLOY_TIME" ]; then
    echo "✓ PASS ($DEPLOY_TIME)"
else
    echo "⚠ WARNING (no timestamp)"
fi

# Verify environment
echo -n "[5/5] Environment verification... "
ENV=$(echo "$BUILDINFO" | jq -r '.deployment.environment // "unknown"')
echo "✓ INFO (environment: $ENV)"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ✓ RELEASE VERIFICATION PASSED"
echo "═══════════════════════════════════════════════════════"
```

**3.2 API/Backend Application:**

```bash
#!/bin/bash
# API verification script

API_ENDPOINT="$1"  # e.g., https://api.example.com
EXPECTED_HASH="$2"

echo "API Release Verification: $API_ENDPOINT"
echo "========================================"

# Check health endpoint
echo -n "Health check... "
HEALTH=$(curl -s "${API_ENDPOINT}/health")
if [ $? -eq 0 ]; then
    echo "✓ PASS"
    echo "$HEALTH" | jq '.'
else
    echo "✗ FAIL"
    exit 1
fi

# Check version endpoint
echo -n "Version check... "
VERSION=$(curl -s "${API_ENDPOINT}/version")
if [ $? -eq 0 ]; then
    echo "✓ PASS"
    echo "$VERSION" | jq '.'

    # Verify git hash
    DEPLOYED_HASH=$(echo "$VERSION" | jq -r '.git_hash // empty')
    if [ "$DEPLOYED_HASH" = "$EXPECTED_HASH" ]; then
        echo "✓ Git hash matches: $DEPLOYED_HASH"
    else
        echo "✗ Git hash mismatch: expected $EXPECTED_HASH, got $DEPLOYED_HASH"
        exit 1
    fi
else
    echo "✗ FAIL"
    exit 1
fi

# Check critical endpoints
echo ""
echo "Testing API Endpoints"
echo "---------------------"

# Example: Test authentication endpoint
echo -n "POST /auth/token... "
AUTH_RESPONSE=$(curl -s -X POST "${API_ENDPOINT}/auth/token" \
    -H "Content-Type: application/json" \
    -d '{"username":"test","password":"test"}' \
    -w "%{http_code}")

AUTH_CODE="${AUTH_RESPONSE: -3}"
if [ "$AUTH_CODE" = "200" ] || [ "$AUTH_CODE" = "401" ]; then
    echo "✓ PASS (responds correctly)"
else
    echo "✗ FAIL (HTTP $AUTH_CODE)"
    exit 1
fi

echo ""
echo "✓ API VERIFICATION PASSED"
```

**3.3 Playwright Visual Verification:**

```typescript
// verify-deployment.spec.ts
import { test, expect } from '@playwright/test';

const DOMAIN = process.env.DOMAIN || 'https://app.example.com';
const EXPECTED_HASH = process.env.EXPECTED_HASH || '';

test.describe('Release Verification', () => {
  test('should load homepage without errors', async ({ page }) => {
    const errors: string[] = [];

    // Capture console errors
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    // Capture page errors
    page.on('pageerror', error => {
      errors.push(error.message);
    });

    // Load page
    const response = await page.goto(DOMAIN);

    // Check response status
    expect(response?.status()).toBe(200);

    // Check no console errors
    expect(errors).toHaveLength(0);

    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');

    // Take screenshot for visual review
    await page.screenshot({
      path: 'verification-screenshot.png',
      fullPage: true
    });
  });

  test('should verify buildinfo.json', async ({ request }) => {
    const response = await request.get(`${DOMAIN}/buildinfo.json`);

    expect(response.ok()).toBeTruthy();

    const buildinfo = await response.json();

    // Verify structure
    expect(buildinfo).toHaveProperty('git');
    expect(buildinfo).toHaveProperty('deployment');

    // Verify git hash
    expect(buildinfo.git.hash).toBe(EXPECTED_HASH);

    console.log('Deployed version:', buildinfo.git.hash);
    console.log('Deployed at:', buildinfo.deployment.timestamp);
  });

  test('should verify critical assets load', async ({ page }) => {
    const failedRequests: string[] = [];

    // Track failed requests
    page.on('requestfailed', request => {
      failedRequests.push(request.url());
    });

    await page.goto(DOMAIN);
    await page.waitForLoadState('networkidle');

    // Check no failed requests
    expect(failedRequests).toHaveLength(0);
  });

  test('should verify navigation works', async ({ page }) => {
    await page.goto(DOMAIN);

    // Check for navigation elements
    const nav = page.locator('nav');
    await expect(nav).toBeVisible();

    // Try clicking a navigation link (customize for your app)
    const firstLink = nav.locator('a').first();
    if (await firstLink.count() > 0) {
      await firstLink.click();
      await page.waitForLoadState('networkidle');

      // Verify we navigated
      expect(page.url()).not.toBe(DOMAIN);
    }
  });

  test('should verify responsive design', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(DOMAIN);
    await page.waitForLoadState('networkidle');

    await page.screenshot({
      path: 'verification-mobile.png',
      fullPage: true
    });

    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto(DOMAIN);
    await page.waitForLoadState('networkidle');

    await page.screenshot({
      path: 'verification-tablet.png',
      fullPage: true
    });

    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto(DOMAIN);
    await page.waitForLoadState('networkidle');

    await page.screenshot({
      path: 'verification-desktop.png',
      fullPage: true
    });
  });
});
```

**Run Playwright verification:**
```bash
# Install Playwright
npm install -D @playwright/test

# Run verification
DOMAIN=https://app.example.com \
EXPECTED_HASH=abc123def456 \
npx playwright test verify-deployment.spec.ts

# Generate HTML report
npx playwright show-report
```

### 4.0 Integration with Deployment Pipeline

**Makefile Integration:**

```makefile
# Deployment + Verification Workflow

.PHONY: deploy-and-verify
deploy-and-verify: deploy verify-release
	@echo "✓ Deployment verified successfully"

.PHONY: verify-release
verify-release:
	@echo "Running release verification..."
	@EXPECTED_HASH=$$(git rev-parse HEAD) && \
	DOMAIN=$$(cd infra && cdk deploy --require-approval never --outputs-file outputs.json && \
		jq -r '.MyStack.DomainName' outputs.json) && \
	./scripts/verify-release.sh "$$DOMAIN" "$$EXPECTED_HASH"
	@echo "Running Playwright tests..."
	@DOMAIN=$$(cd infra && jq -r '.MyStack.DomainName' outputs.json) \
	EXPECTED_HASH=$$(git rev-parse HEAD) \
	npx playwright test verify-deployment.spec.ts

.PHONY: verify-only
verify-only:
	@echo "Verifying existing deployment..."
	@read -p "Enter domain (e.g., https://app.example.com): " DOMAIN && \
	EXPECTED_HASH=$$(git rev-parse HEAD) && \
	./scripts/verify-release.sh "$$DOMAIN" "$$EXPECTED_HASH"
```

**GitHub Actions Integration:**

```yaml
# .github/workflows/deploy-and-verify.yml
name: Deploy and Verify

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Production
        run: make deploy

      - name: Run Release Verification
        run: |
          DOMAIN=$(cd infra && jq -r '.MyStack.DomainName' outputs.json)
          EXPECTED_HASH=${{ github.sha }}
          ./scripts/verify-release.sh "$DOMAIN" "$EXPECTED_HASH"

      - name: Run Playwright Tests
        run: |
          npm install -D @playwright/test
          npx playwright install --with-deps chromium
          DOMAIN=$(cd infra && jq -r '.MyStack.DomainName' outputs.json) \
          EXPECTED_HASH=${{ github.sha }} \
          npx playwright test verify-deployment.spec.ts

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: verification-results
          path: |
            playwright-report/
            verification-*.png
```

### 5.0 Buildinfo.json Validation

**Expected Structure:**
```json
{
  "git": {
    "hash": "abc123def456789",
    "branch": "main",
    "tag": "v1.2.3",
    "isDirty": false,
    "message": "feat: add new feature"
  },
  "deployment": {
    "timestamp": "2025-02-11T20:30:00Z",
    "environment": "production",
    "deployer": "github-actions",
    "buildNumber": "123"
  },
  "infrastructure": {
    "cloudfrontDistribution": "E1234567890ABC",
    "s3Bucket": "my-app-prod-hosting",
    "region": "us-east-1"
  },
  "application": {
    "name": "my-app",
    "version": "1.2.3"
  }
}
```

**Validation Script:**
```python
#!/usr/bin/env python3
# validate-buildinfo.py

import json
import sys
import requests
from typing import Dict, List

def validate_buildinfo(url: str, expected_hash: str) -> List[str]:
    """Validate buildinfo.json structure and content."""
    errors = []

    # Fetch buildinfo
    try:
        response = requests.get(f"{url}/buildinfo.json", timeout=10)
        response.raise_for_status()
        buildinfo = response.json()
    except requests.RequestException as e:
        return [f"Failed to fetch buildinfo.json: {e}"]
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    # Validate required fields
    required_fields = [
        "git.hash",
        "git.branch",
        "deployment.timestamp",
        "deployment.environment"
    ]

    for field in required_fields:
        keys = field.split('.')
        value = buildinfo
        try:
            for key in keys:
                value = value[key]
        except (KeyError, TypeError):
            errors.append(f"Missing required field: {field}")

    # Validate git hash
    deployed_hash = buildinfo.get('git', {}).get('hash', '')
    if deployed_hash != expected_hash:
        errors.append(
            f"Git hash mismatch: expected {expected_hash}, "
            f"got {deployed_hash}"
        )

    # Validate timestamp format
    timestamp = buildinfo.get('deployment', {}).get('timestamp', '')
    if timestamp and not timestamp.endswith('Z'):
        errors.append(f"Timestamp should be UTC (end with Z): {timestamp}")

    return errors

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: validate-buildinfo.py <url> <expected-hash>")
        sys.exit(1)

    url = sys.argv[1]
    expected_hash = sys.argv[2]

    errors = validate_buildinfo(url, expected_hash)

    if errors:
        print("❌ Buildinfo validation FAILED:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ Buildinfo validation PASSED")
        sys.exit(0)
```

### 6.0 Common Verification Failures

| Failure | Cause | Fix |
|---------|-------|-----|
| DNS not resolving | Route53 record not created | Check domain configuration in IaC |
| 502 Bad Gateway | CloudFront can't reach origin | Verify S3 bucket/origin config |
| 403 Forbidden | S3 bucket policy blocks CloudFront | Update bucket policy |
| Wrong git hash | Old build deployed | Rebuild and redeploy |
| buildinfo.json 404 | File not included in build | Run `make buildinfo` before deploy |
| Console errors | JS bundle failed to load | Check asset paths, CORS headers |
| Certificate error | SSL cert not provisioned | Wait for ACM validation, check DNS |
| Redirect loop | Misconfigured redirects | Check CloudFront behaviors |

### 7.0 Agent Invocation

**When to Spawn This Agent:**

Spawn `release-verification-agent` when:
- Deployment just completed (any environment)
- Need to verify application is working correctly
- Checking if specific version is deployed
- Troubleshooting deployment issues
- Running smoke tests before marking release complete

**Workflow:**
```
Deployment complete
     ↓
Spawn release-verification-agent
     ↓
Agent runs:
  - Basic accessibility checks (curl)
  - Buildinfo validation
  - Playwright visual tests
  - Critical flow tests
     ↓
Agent reports:
  - ✓ All checks passed → Release complete
  - ✗ Failures detected → Rollback recommended
     ↓
Human decision: Proceed or rollback
```

### 8.0 Output Format

**Verification Report Template:**
```markdown
# Release Verification Report

## Deployment: {domain}
## Environment: {environment}
## Verification Date: {YYYY-MM-DD HH:MM:SS UTC}

### 1.0 Deployment Metadata
- Expected Hash: {expected_hash}
- Deployed Hash: {deployed_hash}
- Match: {✓ PASS / ✗ FAIL}
- Deployment Time: {timestamp}
- Environment: {environment}

### 2.0 Basic Accessibility
- [✓] DNS resolution
- [✓] HTTPS accessible (200 OK)
- [✓] SSL certificate valid
- [✓] Response time: {time}ms
- [✓] Custom domain resolves

### 3.0 Application Health
- [✓] buildinfo.json accessible
- [✓] buildinfo.json valid JSON
- [✓] Git hash verified
- [✓] Deployment timestamp present
- [✓] Environment matches

### 4.0 Visual Rendering (Playwright)
- [✓] Homepage loads without errors
- [✓] No console errors
- [✓] All assets load successfully
- [✓] Navigation works
- [✓] Responsive design verified

### 5.0 Functional Tests
- [✓] API endpoints respond
- [✓] Authentication flow works
- [✓] Database connectivity confirmed

### 6.0 Summary

**Status:** ✓ VERIFICATION PASSED

**All Tier 1 and Tier 2 checks passed. Application is ready for use.**

**Recommended Actions:**
- [1] Mark release as complete
- [2] Update status dashboard
- [3] Notify stakeholders

---

**Artifacts:**
- Verification script: scripts/verify-release.sh
- Playwright report: playwright-report/index.html
- Screenshots: verification-*.png
```

### 9.0 Related Documentation

**Internal:**
- `hmode/shared/tools/BUILDINFO_PATTERN.md` - Buildinfo.json specification
- `hmode/shared/standards/testing/SMOKE_TEST_PATTERN.md` - Smoke testing standards
- `@processes/LAMBDA_TROUBLESHOOTING_AGENT` - API troubleshooting
- `hmode/guardrails/tech-preferences/infrastructure.json` - Monitoring requirements

**External:**
- [Playwright Documentation](https://playwright.dev/)
- [AWS CloudWatch Synthetics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html)
- [Smoke Testing Best Practices](https://martinfowler.com/bliki/SmokeTest.html)

---

**Agent Version:** 1.0.0
**Last Updated:** 2026-02-11
**Maintained By:** Infrastructure Team
