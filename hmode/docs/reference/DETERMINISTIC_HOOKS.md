# Deterministic Condition-Based Hooks

<!-- File UUID: 8a3f9c2d-4b7e-4f1a-9d2c-6e8a1b5c3d7f -->

## Overview

Automated actions triggered by deterministic conditions. These hooks run automatically when specific file/deployment/code events are detected.

## 1.0 FILE GENERATION HOOKS

### 1.1 HTML Files
**Condition:** HTML file created (*.html)
**Actions:**
1. Detect if standalone mockup or app component
2. If standalone mockup:
   - Offer: `[1] View locally [2] Publish to S3 [3] Skip`
   - If published → Show clickable URL
3. If app component:
   - Inform: "HTML component created: {path}"

### 1.2 PDF Files
**Condition:** PDF generated (*.pdf)
**Actions:**
1. Calculate file size
2. If < 10MB:
   - Offer: `[1] Open in default viewer [2] Publish to S3 [3] Skip`
3. If >= 10MB:
   - Inform: "Large PDF created: {path} ({size}MB)"

### 1.3 Excel/CSV Files
**Condition:** Spreadsheet created (*.xlsx, *.csv)
**Actions:**
1. Count rows (if feasible)
2. Offer: `[1] Open in Excel/Numbers [2] Publish to S3 [3] Skip`
3. Show first 5 rows as preview table

### 1.4 Images/Diagrams
**Condition:** Image generated (*.png, *.jpg, *.svg)
**Actions:**
1. If SVG:
   - Offer: `[1] View inline [2] Publish to S3 [3] Skip`
   - Show preview if < 50KB
2. If PNG/JPG:
   - Offer: `[1] Open in viewer [2] Publish to S3 [3] Skip`

### 1.5 Markdown Documentation
**Condition:** Markdown file created in docs/ or project root
**Actions:**
1. Check if it's a README or phase report
2. If README:
   - Inform: "README created: {path}"
3. If phase report:
   - Offer: `[1] View formatted [2] Generate PDF [3] Skip`

### 1.6 buildinfo.json
**Condition:** buildinfo.json created/updated
**Actions:**
1. Parse git hash, branch, timestamp
2. Inform: "Build info updated: {hash} on {branch} at {timestamp}"
3. If deployment detected → Trigger smoke test hook (2.1)

---

## 2.0 DEPLOYMENT HOOKS

### 2.1 Site Deployed (Any Method)
**Condition:** Deployment completed (CloudFront, Amplify, S3 static site)
**Actions:**
1. Extract primary URL (canonical domain preferred)
2. Show clickable URL: `🌐 Deployed: https://example.com`
3. **Automatically run smoke test:**
   - Check for `tests/smoke/` directory
   - If smoke test exists → Run it
   - If no smoke test → Fallback to curl + Playwright check
4. Report results:
   ```
   ✅ Smoke test passed
   ✅ HTTP 200 from https://example.com
   ✅ Git hash verified: abc123
   ```

### 2.2 CloudFront Distribution
**Condition:** CloudFront distribution created/updated
**Actions:**
1. Extract distribution URL and custom domain (if any)
2. Show both URLs:
   ```
   🌐 CloudFront: https://d1234abcd.cloudfront.net
   🌐 Custom: https://example.com (if configured)
   ```
3. Check cache invalidation status
4. Trigger smoke test (2.1)

### 2.3 Amplify App
**Condition:** Amplify app deployed
**Actions:**
1. Extract Amplify URL and custom domain
2. Show both URLs:
   ```
   🌐 Amplify: https://main.d1234abcd.amplifyapp.com
   🌐 Custom: https://example.com (if configured)
   ```
3. Show branch and commit
4. Trigger smoke test (2.1)

### 2.4 Lambda Function
**Condition:** Lambda function deployed
**Actions:**
1. Extract function ARN and URL (if Function URL enabled)
2. Show: `λ Lambda deployed: {function-name}`
3. If Function URL:
   - Show clickable URL
   - Offer: `[1] Test with curl [2] Skip`

### 2.5 API Gateway
**Condition:** API Gateway deployed
**Actions:**
1. Extract API endpoint
2. Show: `🔌 API deployed: https://api-id.execute-api.region.amazonaws.com/stage`
3. List available routes (if detectable)
4. Offer: `[1] Test with curl [2] View OpenAPI spec [3] Skip`

---

## 3.0 CODE EVENT HOOKS

### 3.1 Tests Written
**Condition:** Test file created/updated (test_*.py, *.test.ts, *.spec.ts)
**Actions:**
1. Detect test framework (pytest, jest, vitest, cucumber)
2. Offer: `[1] Run tests now [2] Run in watch mode [3] Skip`
3. If tests run:
   - Show pass/fail summary
   - If failures → Show first 3 failures

### 3.2 Feature Implemented
**Condition:** Multiple files changed + git status shows unstaged changes
**Actions:**
1. Detect if in Phase 8+ (implementation phase)
2. Offer commit: `[1] Commit changes [2] Review diff first [3] Skip`
3. If commit → Auto-generate commit message from diff

### 3.3 Dependencies Updated
**Condition:** package.json, requirements.txt, Pipfile changed
**Actions:**
1. Detect package manager (npm, pnpm, yarn, pip, pipenv)
2. Offer: `[1] Install dependencies [2] Skip`
3. If installed → Show added/updated packages

### 3.4 Type Errors Detected
**Condition:** TypeScript or mypy errors in output
**Actions:**
1. Count total errors
2. Show first 3 errors with file:line references
3. Offer: `[1] Fix automatically [2] Show all errors [3] Skip`

---

## 4.0 INFRASTRUCTURE HOOKS

### 4.1 CDK Stack Deployed
**Condition:** `cdk deploy` completed
**Actions:**
1. Extract stack outputs (URLs, ARNs, etc.)
2. Show outputs in table format
3. If outputs include URLs → Show clickable links
4. Trigger relevant deployment hooks (2.1, 2.2, etc.)

### 4.2 Domain Configured
**Condition:** Route53 record created
**Actions:**
1. Extract domain name and record type
2. Verify DNS propagation: `dig +short {domain}`
3. Show:
   ```
   🌐 DNS configured: {domain} → {target}
   ✅ Propagated (or ⏳ Propagating...)
   ```

### 4.3 Certificate Issued
**Condition:** ACM certificate issued
**Actions:**
1. Extract domain name and validation status
2. Show: `🔒 Certificate issued: {domain}`
3. If pending validation → Show validation records

### 4.4 Database Created
**Condition:** RDS, DynamoDB, or other DB created
**Actions:**
1. Extract connection endpoint
2. Show (sanitized): `🗄️ Database created: {db-name}`
3. If RDS → Remind to store credentials in Secrets Manager
4. If DynamoDB → Show table name and partition key

---

## 5.0 TESTING & QUALITY HOOKS

### 5.1 Smoke Test Available
**Condition:** `tests/smoke/` directory exists OR `make smoke-test` target exists
**Actions:**
1. Automatically run after any deployment (2.1)
2. Show results:
   ```
   Running smoke tests...
   ✅ Git hash verified
   ✅ Page loads (HTTP 200)
   ✅ No console errors
   ```

### 5.2 No Smoke Test Found
**Condition:** Deployment completed but no smoke test detected
**Actions:**
1. Fallback to basic checks:
   - curl -I {url} (verify HTTP 200)
   - Playwright check (if available): visit page, check for errors
2. Show results
3. Offer: `[1] Create smoke test [2] Skip`

### 5.3 Build Artifacts Generated
**Condition:** `dist/`, `build/`, `.next/` directory created/updated
**Actions:**
1. Calculate build size
2. Show: `📦 Build completed: {size}MB in {time}s`
3. If web app → Check for buildinfo.json (1.6)

### 5.4 Git Hash Mismatch
**Condition:** Deployed git hash ≠ expected hash (from smoke test)
**Actions:**
1. Show warning:
   ```
   ⚠️ Git hash mismatch!
   Expected: abc123
   Deployed: def456
   ```
2. Offer: `[1] Redeploy [2] Investigate [3] Skip`

---

## 6.0 ERROR & WARNING HOOKS

### 6.1 AWS Credentials Expired
**Condition:** AccessDenied or ExpiredToken error from AWS CLI
**Actions:**
1. Show: `⚠️ AWS credentials expired`
2. Offer: `[1] Refresh credentials [2] Skip`
3. If refresh → Run: `eval $(isengardcli credentials ...)`

### 6.2 Port Already in Use
**Condition:** EADDRINUSE error when starting dev server
**Actions:**
1. Detect port number
2. Find process using port: `lsof -i :{port}`
3. Show process details
4. Offer: `[1] Kill process [2] Use different port [3] Skip`

### 6.3 Missing Environment Variables
**Condition:** Error message contains "environment variable" or "not defined"
**Actions:**
1. Extract variable name
2. Check if .env.example exists
3. Show: `⚠️ Missing env var: {VAR_NAME}`
4. Offer: `[1] Add to .env [2] Skip`

### 6.4 Dependency Conflict
**Condition:** npm/pip error about incompatible versions
**Actions:**
1. Extract conflicting packages
2. Show conflict details
3. Offer: `[1] Auto-resolve [2] Show dependency tree [3] Skip`

---

## 7.0 SPECIAL CASE HOOKS

### 7.1 Amplify Build Failure
**Condition:** Amplify build failed (from boto3 or CLI output)
**Actions:**
1. Fetch build logs using `amplify-deploy-specialist` agent
2. Show first 20 lines of error logs
3. Offer: `[1] Full logs [2] Retry build [3] Skip`

### 7.2 CloudFront Invalidation
**Condition:** Files updated in S3 + CloudFront distribution detected
**Actions:**
1. Show: `🔄 CloudFront cache may be stale`
2. Offer: `[1] Invalidate cache [2] Skip`
3. If invalidated → Show invalidation ID and status

### 7.3 Large File Detected
**Condition:** File > 100MB being added to git
**Actions:**
1. Show warning: `⚠️ Large file: {filename} ({size}MB)`
2. Offer: `[1] Add to .gitignore [2] Use Git LFS [3] Continue anyway`

### 7.4 Security Issue Detected
**Condition:** Hardcoded secret, AWS key, or password pattern detected
**Actions:**
1. Show warning: `🔒 Possible secret detected in {file}:{line}`
2. Redact in output: `AWS_KEY=AKIAXXX...***`
3. Offer: `[1] Remove and use env var [2] Add to .gitignore [3] False positive`

---

## 8.0 IMPLEMENTATION NOTES

### 8.1 Hook Execution Order
```
1. File detection (1.0)
2. Error checks (6.0)
3. Code events (3.0)
4. Deployment events (2.0)
5. Infrastructure events (4.0)
6. Testing/quality (5.0)
7. Special cases (7.0)
```

### 8.2 Hook Suppression
Users can suppress hooks with:
- `--no-hooks` flag
- `CLAUDE_HOOKS=false` env var
- `.clauderc` setting: `hooks.enabled = false`

### 8.3 Hook Verbosity Levels
```
silent:  No hook output
minimal: Show only clickable URLs and critical warnings
normal:  Default behavior (all hooks)
verbose: Include diagnostic info (file sizes, timings, etc.)
```

### 8.4 Hook Configuration
Store in `.claude/hooks-config.yaml`:
```yaml
hooks:
  file_generation:
    html: enabled
    pdf: enabled
    offer_publish: true

  deployment:
    auto_smoke_test: true
    show_urls: true
    verify_git_hash: true

  code_events:
    auto_run_tests: false
    suggest_commit: true

  errors:
    auto_fix: false
    show_suggestions: true
```

---

## 9.0 QUICK REFERENCE

| Event | Auto Action | Manual Offer |
|-------|------------|--------------|
| HTML created | - | View/Publish |
| Site deployed | Show URL, run smoke test | - |
| Lambda deployed | Show ARN | Test with curl |
| Tests written | - | Run tests |
| Dependencies updated | - | Install |
| AWS creds expired | - | Refresh |
| Amplify build failed | Fetch logs | Retry |
| Large file detected | Warn | .gitignore/LFS |

---

**Version:** 1.0.0
**Last Updated:** 2026-02-04
