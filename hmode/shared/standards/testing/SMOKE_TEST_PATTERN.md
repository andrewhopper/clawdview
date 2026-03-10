# Post-Deploy Smoke Test Pattern

Every deployed app MUST have a smoke test that runs after deployment.

## Required: Git Hash Verification

Apps must expose their git commit hash and the smoke test must verify it matches the expected deployed version:

```bash
# Build-time: Inject git hash into app
GIT_HASH=$(git rev-parse --short HEAD)
# Expose via: meta tag, /health endpoint, or window.__GIT_HASH__

# Smoke test verifies deployed hash matches
curl -s https://app.example.com/health | jq -r '.gitHash'
# Or: curl -s https://app.example.com | grep -o 'data-git-hash="[^"]*"'
```

## Recommended: Playwright Render Test

Ideally, include a Playwright test to verify the page renders correctly:

```typescript
// tests/smoke.spec.ts
import { test, expect } from '@playwright/test';

test('smoke test - page renders and git hash matches', async ({ page }) => {
  const expectedHash = process.env.EXPECTED_GIT_HASH;

  await page.goto(process.env.APP_URL);

  // Verify page renders (no crash, key elements present)
  await expect(page.locator('body')).toBeVisible();
  await expect(page.locator('[data-testid="main-content"]')).toBeVisible();

  // Verify git hash matches deployed version
  const gitHash = await page.getAttribute('meta[name="git-hash"]', 'content');
  expect(gitHash).toBe(expectedHash);
});
```

## Implementation Pattern

### 1. Inject hash at build time

```javascript
// vite.config.ts or next.config.js
define: {
  __GIT_HASH__: JSON.stringify(process.env.GIT_HASH || 'dev')
}
```

### 2. Expose in app

```html
<!-- In HTML head -->
<meta name="git-hash" content="abc1234">
```

```typescript
// Or via API endpoint
app.get('/health', (req, res) => res.json({
  status: 'ok',
  gitHash: process.env.GIT_HASH
}));
```

### 3. Add Makefile target

```makefile
smoke-test:
	@echo "Running post-deploy smoke test..."
	@EXPECTED_GIT_HASH=$$(git rev-parse --short HEAD) \
	APP_URL=$(DEPLOY_URL) \
	npx playwright test tests/smoke.spec.ts
	@echo "✓ Smoke test passed"
```

### 4. Run after deploy

```makefile
infra-deploy:
	# ... existing deploy steps ...
	@$(MAKE) smoke-test
```

## CRITICAL: Use Canonical Domain

Smoke tests MUST use the canonical app domain (e.g., `mo.b.lfg.new`), NOT temporary CloudFront or Amplify URLs:

```bash
# ✅ CORRECT - canonical domain
APP_URL=https://mo.b.lfg.new

# ❌ WRONG - temporary/internal URLs
APP_URL=https://d1234abcd.cloudfront.net
APP_URL=https://main.d1234abcd.amplifyapp.com
```

This ensures you're testing what users actually see, including DNS propagation and CDN configuration.

## Why This Matters

- Catches deployment failures where wrong version is deployed
- Verifies CDN cache invalidation worked
- Confirms DNS and routing are correctly configured
- Confirms app renders without JavaScript errors
- Provides confidence before announcing deployment success
