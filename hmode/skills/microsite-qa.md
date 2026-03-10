---
name: microsite-qa
description: QA testing for deployed microsites - validates accessibility, footer requirements, and build metadata
version: 1.0.0
---

# Microsite QA Skill

**Validate deployed microsites against required standards after deployment.**

## Required Elements

Every microsite MUST contain:

1. **Accessibility** - Site loads successfully via curl
2. **Copyright footer** - Current year with "Andrew Hopper"
3. **Contact email** - demo@example.com visible in footer
4. **Git branch** - Branch name displayed (build metadata)
5. **Git hash** - Commit hash displayed (build metadata)
6. **Date published** - Publication date (e.g., "2025-11-22")
7. **Time published** - Publication time in EST (e.g., "14:30 EST")

## Execution Flow

1. **Get URL** - User provides deployed microsite URL
2. **Fetch content** - Use curl to retrieve HTML
3. **Parse and validate** - Check for all required elements
4. **Generate report** - Pass/fail with details
5. **Suggest fixes** - For any missing elements

## Validation Checks

### 1. Accessibility Check
```bash
curl -sI "${URL}" | head -1
```
- **PASS**: HTTP 200 OK
- **FAIL**: Any other status code or timeout

### 2. Copyright Footer Check
```bash
curl -s "${URL}" | grep -i "copyright\|©"
```
**Required pattern**: `© {CURRENT_YEAR} Andrew Hopper` or `Copyright {CURRENT_YEAR} Andrew Hopper`

**Validation rules**:
- Year must match current year (dynamic check)
- "Andrew Hopper" must appear near copyright symbol
- Case insensitive matching for "copyright"

### 3. Email Check
```bash
curl -s "${URL}" | grep -i "demo@example.com"
```
**Required**: Email address `demo@example.com` must appear in page

### 4. Git Branch Check
```bash
curl -s "${URL}" | grep -iE "branch[:\s]*[a-zA-Z0-9/_-]+"
```
**Required**: Branch name visible in footer/metadata

**Common patterns**:
- `Branch: main`
- `branch: feature/xyz`
- Data attribute: `data-branch="main"`

### 5. Git Hash Check
```bash
curl -s "${URL}" | grep -iE "[a-f0-9]{7,40}"
```
**Required**: Git commit hash (7-40 hex characters)

**Common patterns**:
- `Commit: abc1234`
- `Hash: abc1234def5678`
- Data attribute: `data-commit="abc1234"`

### 6. Date Published Check
```bash
curl -s "${URL}" | grep -iE "(published|date)[:\s]*\d{4}-\d{2}-\d{2}"
```
**Required**: Publication date in ISO format (YYYY-MM-DD)

**Common patterns**:
- `Published: 2025-11-22`
- `Date: 2025-11-22`
- Data attribute: `data-published-date="2025-11-22"`

### 7. Time Published Check
```bash
curl -s "${URL}" | grep -iE "(time|published)[:\s]*\d{2}:\d{2}"
```
**Required**: Publication time (HH:MM format in EST)

**Common patterns**:
- `Time: 14:30 EST`
- `Published: 14:30 EST`
- Data attribute: `data-published-time="14:30 EST"`

## Report Format

```markdown
# Microsite QA Report

**URL**: {url}
**Tested**: {timestamp}
**Status**: {PASS / FAIL}

---

## Results

| Check | Status | Details |
|-------|--------|---------|
| Accessibility | {status} | HTTP {code} |
| Copyright | {status} | {found text or "Missing"} |
| Email | {status} | {found or "Missing"} |
| Git Branch | {status} | {branch name or "Missing"} |
| Git Hash | {status} | {hash or "Missing"} |
| Date Published | {status} | {date or "Missing"} |
| Time Published | {status} | {time or "Missing"} |

---

## Summary

**Passed**: {X}/7
**Failed**: {Y}/7

---

## Fixes Required

{If any checks failed, list specific fixes}

### Missing Copyright
Add to footer:
```html
<footer>
  <p>&copy; 2025 Andrew Hopper</p>
</footer>
```

### Missing Email
Add to footer:
```html
<a href="mailto:demo@example.com">demo@example.com</a>
```

### Missing Git Metadata
Add build info (usually auto-generated):
```html
<div class="build-info">
  <span data-branch="main">Branch: main</span>
  <span data-commit="abc1234">Commit: abc1234</span>
</div>
```

### Missing Published Date/Time
Add publication timestamp:
```html
<div class="publish-info">
  <span data-published-date="2025-11-22">Published: 2025-11-22</span>
  <span data-published-time="14:30 EST">Time: 14:30 EST</span>
</div>
```

---

## Recommended Footer Template

```html
<footer class="site-footer">
  <div class="footer-content">
    <p>&copy; 2025 Andrew Hopper</p>
    <p>Contact: <a href="mailto:demo@example.com">demo@example.com</a></p>
    <div class="build-meta">
      <span>Branch: main</span> |
      <span>Commit: abc1234</span> |
      <span>Published: 2025-11-22 14:30 EST</span>
    </div>
  </div>
</footer>
```
```

## Usage

```bash
# QA a deployed microsite
/qa-microsite https://example.com

# QA with verbose output
/qa-microsite https://example.com --verbose

# QA multiple sites
/qa-microsite https://site1.com https://site2.com
```

## Interactive Mode

**Single URL:**
```
User: QA my microsite at https://example.com
Assistant:
  - Fetches URL
  - Runs all 5 checks
  - Generates report
  - Suggests fixes for failures
```

**No URL provided:**
```
User: QA my microsite
Assistant:
  - Asks for deployed URL
  - Proceeds with checks
```

## Integration with Deploy Workflow

**Recommended workflow:**
1. Deploy microsite (via /publish or manual)
2. Run `/qa-microsite {url}`
3. Fix any failing checks
4. Re-deploy and re-test until all pass

## Error Handling

**Site not accessible:**
```
URL: https://example.com
Status: UNREACHABLE

Error: curl: (7) Failed to connect

Troubleshooting:
1. Verify URL is correct
2. Check if site is deployed
3. Check DNS propagation
4. Verify SSL certificate
```

**Partial failures:**
```
3/5 checks passed

Critical: Missing git metadata
- Add build script to inject branch/commit
- Or add static values manually
```

## Success Criteria

A microsite PASSES QA when ALL of these are true:
- HTTP 200 response
- Copyright includes current year + "Andrew Hopper"
- Email demo@example.com is visible
- Git branch name is visible
- Git commit hash is visible
- Publication date is visible (YYYY-MM-DD format)
- Publication time is visible (HH:MM EST format)

## Build Script Integration

**For automated builds**, inject git and publish metadata:

```bash
#!/bin/bash
# inject-build-info.sh

BRANCH=$(git rev-parse --abbrev-ref HEAD)
HASH=$(git rev-parse --short HEAD)
YEAR=$(date +%Y)
PUB_DATE=$(date +%Y-%m-%d)
PUB_TIME=$(TZ='America/New_York' date +%H:%M)

# Replace placeholders in HTML
sed -i "s/{{BRANCH}}/${BRANCH}/g" dist/index.html
sed -i "s/{{HASH}}/${HASH}/g" dist/index.html
sed -i "s/{{YEAR}}/${YEAR}/g" dist/index.html
sed -i "s/{{PUB_DATE}}/${PUB_DATE}/g" dist/index.html
sed -i "s/{{PUB_TIME}}/${PUB_TIME}/g" dist/index.html
```

**HTML template with placeholders:**
```html
<footer>
  <p>&copy; {{YEAR}} Andrew Hopper</p>
  <p><a href="mailto:demo@example.com">demo@example.com</a></p>
  <small>Branch: {{BRANCH}} | Commit: {{HASH}} | Published: {{PUB_DATE}} {{PUB_TIME}} EST</small>
</footer>
```

## Notes

- Always run QA after deployment, not before
- Git metadata should be injected at build time
- Current year is dynamically checked (not hardcoded)
- All checks must pass for a site to be considered production-ready
