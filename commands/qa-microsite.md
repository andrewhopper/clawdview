---
description: QA a deployed microsite for required elements (URL to test)
version: 1.0.0
---

# QA Microsite

Validate a deployed microsite against required standards.

## Arguments

```
$ARGUMENTS = URL to test (required)
```

## Required Checks

1. **Accessibility** - HTTP 200 via curl
2. **Copyright** - Current year + "Andrew Hopper"
3. **Email** - demo@example.com visible
4. **Git Branch** - Branch name in footer/metadata
5. **Git Hash** - Commit hash in footer/metadata
6. **Date Published** - Publication date (YYYY-MM-DD)
7. **Time Published** - Publication time (HH:MM EST)

## Instructions

### Step 1: Parse URL

```bash
URL="$ARGUMENTS"
```

If no URL provided, ask user for the deployed microsite URL.

### Step 2: Run Accessibility Check

```bash
# Check HTTP status
HTTP_STATUS=$(curl -sI -o /dev/null -w "%{http_code}" "${URL}" --max-time 10)
```

- **PASS**: Status is 200
- **FAIL**: Any other status or timeout

### Step 3: Fetch Page Content

```bash
# Get full HTML content
CONTENT=$(curl -s "${URL}" --max-time 30)
```

### Step 4: Validate Copyright

```python
import re
from datetime import datetime

current_year = datetime.now().year
# Look for: © 2025 Andrew Hopper or Copyright 2025 Andrew Hopper
pattern = rf'(©|copyright)\s*{current_year}\s*andrew\s*hopper'
match = re.search(pattern, content, re.IGNORECASE)
```

**Expected**: `© {CURRENT_YEAR} Andrew Hopper`

### Step 5: Validate Email

```bash
# Check for email
echo "${CONTENT}" | grep -i "demo@example.com"
```

**Expected**: `demo@example.com` appears in page

### Step 6: Validate Git Branch

```bash
# Look for branch name patterns
echo "${CONTENT}" | grep -iE "(branch[:\s=]*['\"]?[a-zA-Z0-9/_-]+|data-branch)"
```

**Expected patterns**:
- `Branch: main`
- `data-branch="feature/xyz"`
- `branch: claude/something`

### Step 7: Validate Git Hash

```bash
# Look for commit hash (7-40 hex chars)
echo "${CONTENT}" | grep -iE "(commit|hash)[:\s=]*['\"]?[a-f0-9]{7,40}"
```

**Expected patterns**:
- `Commit: abc1234`
- `data-commit="abc1234def5678"`
- `Hash: ca7ef9b8`

### Step 8: Validate Date Published

```bash
# Look for publication date (YYYY-MM-DD format)
echo "${CONTENT}" | grep -iE "(published|date)[:\s=]*['\"]?\d{4}-\d{2}-\d{2}"
```

**Expected patterns**:
- `Published: 2025-11-22`
- `Date: 2025-11-22`
- `data-published-date="2025-11-22"`

### Step 9: Validate Time Published

```bash
# Look for publication time (HH:MM EST format)
echo "${CONTENT}" | grep -iE "(time|published)[:\s=]*['\"]?\d{2}:\d{2}.*EST"
```

**Expected patterns**:
- `Time: 14:30 EST`
- `Published: 14:30 EST`
- `data-published-time="14:30 EST"`

### Step 10: Generate Report

Present results in table format:

```markdown
# Microsite QA Report

**URL**: {url}
**Tested**: {timestamp}

## Results

| Check | Status | Found |
|-------|--------|-------|
| Accessibility | {PASS/FAIL} | HTTP {code} |
| Copyright | {PASS/FAIL} | {text or "Not found"} |
| Email | {PASS/FAIL} | {email or "Not found"} |
| Git Branch | {PASS/FAIL} | {branch or "Not found"} |
| Git Hash | {PASS/FAIL} | {hash or "Not found"} |
| Date Published | {PASS/FAIL} | {date or "Not found"} |
| Time Published | {PASS/FAIL} | {time or "Not found"} |

## Summary

**Score**: {X}/7 checks passed
**Status**: {PASS if 7/7, else FAIL}
```

### Step 9: Provide Fixes (if needed)

For each failed check, provide specific fix:

**Missing Copyright:**
```html
<footer>
  <p>&copy; 2025 Andrew Hopper</p>
</footer>
```

**Missing Email:**
```html
<a href="mailto:demo@example.com">demo@example.com</a>
```

**Missing Git Metadata:**
```html
<div class="build-info">
  <span>Branch: main</span>
  <span>Commit: abc1234</span>
</div>
```

**Missing Published Date/Time:**
```html
<div class="publish-info">
  <span>Published: 2025-11-22 14:30 EST</span>
</div>
```

Or recommend build script injection:
```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
HASH=$(git rev-parse --short HEAD)
PUB_DATE=$(date +%Y-%m-%d)
PUB_TIME=$(TZ='America/New_York' date +%H:%M)
```

## Example Output

```
# Microsite QA Report

**URL**: https://my-microsite.example.com
**Tested**: 2025-11-22T10:30:00Z

## Results

| Check | Status | Found |
|-------|--------|-------|
| Accessibility | PASS | HTTP 200 |
| Copyright | PASS | © 2025 Andrew Hopper |
| Email | PASS | demo@example.com |
| Git Branch | PASS | Branch: main |
| Git Hash | PASS | Commit: ca7ef9b8 |
| Date Published | PASS | 2025-11-22 |
| Time Published | PASS | 14:30 EST |

## Summary

**Score**: 7/7 checks passed
**Status**: PASS

Site meets all QA requirements.
```

## Error Handling

**URL unreachable:**
```
ERROR: Could not reach {url}
Status: Connection failed

Troubleshooting:
1. Verify URL is correct
2. Check if site is deployed
3. Try accessing in browser
```

**Partial content:**
```
WARNING: Page loaded but may be incomplete
Some checks may have false negatives
```

## Notes

- Run AFTER deployment, not before
- Current year is checked dynamically
- All 7 checks must pass for QA approval
- Use /publish first, then /qa-microsite to validate
