<!-- File UUID: a1b2c3d4-5e6f-7a8b-9c0d-e1f2a3b4c5d6 -->
---
description: Comprehensive security audit (CVEs, JWT, SQL injection, CSRF, encryption)
version: 1.0.0
---

# Security Audit

Comprehensive security vulnerability scanner. Checks for CVEs, JWT issues, SQL injection, CSRF, weak encryption, unprotected endpoints, and generates a one-page findings report.

## Arguments

```
$ARGUMENTS = [options] [path]

Options:
  --quick              Fast scan (deps + secrets only)
  --categories=<list>  Specific categories: deps,auth,injection,csrf,encryption,transport,headers,files
  --format=<type>      Output: md (default), html, json
  --min-severity=<s>   Filter: critical, high, medium, low

Path:
  Directory to scan (default: current directory)

Examples:
  /security-audit
  /security-audit ./projects/my-api
  /security-audit --quick
  /security-audit --categories=deps,auth,injection
  /security-audit --min-severity=high --format=html
```

## Instructions

Execute each category in sequence, collecting findings, then generate the report.

### Step 1: Detect Project Type

```bash
cd "${1:-.}"
PROJECT_PATH=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_PATH")

echo "🔍 Scanning: $PROJECT_NAME"
echo "📁 Path: $PROJECT_PATH"
echo ""

# Detect stack
HAS_NODE=$([ -f "package.json" ] && echo "true" || echo "false")
HAS_PYTHON=$([ -f "requirements.txt" ] || [ -f "pyproject.toml" ] && echo "true" || echo "false")
HAS_GO=$([ -f "go.mod" ] && echo "true" || echo "false")

echo "Stack detected:"
[ "$HAS_NODE" = "true" ] && echo "  - Node.js"
[ "$HAS_PYTHON" = "true" ] && echo "  - Python"
[ "$HAS_GO" = "true" ] && echo "  - Go"
```

### Step 2: CVE / Dependency Audit

```bash
echo ""
echo "📦 DEPENDENCY AUDIT"
echo "==================="

# Node.js
if [ "$HAS_NODE" = "true" ]; then
  echo ""
  echo "Node.js (npm audit):"
  npm audit 2>/dev/null || echo "  Run: npm install first"

  echo ""
  echo "Outdated packages:"
  npm outdated 2>/dev/null | head -20
fi

# Python
if [ "$HAS_PYTHON" = "true" ]; then
  echo ""
  echo "Python (pip-audit):"
  pip-audit 2>/dev/null || echo "  Install: pip install pip-audit"

  echo ""
  echo "Outdated packages:"
  pip list --outdated 2>/dev/null | head -20
fi
```

### Step 3: JWT Security

Use Grep tool to find JWT issues:

```
Patterns to search:

1. No verification:
   Pattern: verify\s*=\s*False|verify\s*:\s*false
   Files: *.py, *.js, *.ts
   Severity: CRITICAL

2. Algorithm 'none':
   Pattern: algorithm.*none|alg.*none
   Files: *.py, *.js, *.ts
   Severity: CRITICAL

3. Token in localStorage:
   Pattern: localStorage\.(setItem|getItem).*token
   Files: *.js, *.ts, *.jsx, *.tsx
   Severity: HIGH

4. Token in URL:
   Pattern: \?.*token=|&token=
   Files: *.js, *.ts, *.py
   Severity: HIGH

5. Missing expiration:
   Pattern: jwt\.(sign|encode)
   Check if 'exp' is NOT present
   Severity: HIGH
```

### Step 4: Unprotected API Endpoints

Use Grep tool to find unprotected routes:

```
Patterns to search:

1. Express without auth:
   Pattern: app\.(get|post|put|delete|patch)\s*\(['\"]\/api
   Exclude lines with: auth, protect, middleware, verify, session
   Severity: HIGH

2. FastAPI without Depends:
   Pattern: @app\.(get|post|put|delete)\s*\(['\"]\/api
   Exclude lines with: Depends, get_current_user, verify
   Severity: HIGH

3. Django without decorator:
   Pattern: path\(['\"]api/
   Exclude lines with: login_required, permission
   Severity: HIGH
```

### Step 5: SQL Injection

Use Grep tool to find injection vulnerabilities:

```
Patterns to search:

1. Python f-string in execute:
   Pattern: execute\s*\(f['\"]
   Severity: CRITICAL

2. Python string format:
   Pattern: execute\s*\(['\"].*%s.*['\"].*%
   Severity: CRITICAL

3. String concatenation in SQL:
   Pattern: (SELECT|INSERT|UPDATE|DELETE).*\+\s*(user|name|id|input|req)
   Severity: CRITICAL

4. JS template literal in query:
   Pattern: query\s*\(\`.*\$\{
   Severity: CRITICAL
```

### Step 6: XSS Detection

```
Patterns to search:

1. dangerouslySetInnerHTML:
   Pattern: dangerouslySetInnerHTML
   Files: *.jsx, *.tsx
   Severity: HIGH

2. innerHTML assignment:
   Pattern: \.innerHTML\s*=
   Files: *.js, *.ts
   Severity: HIGH

3. document.write:
   Pattern: document\.write\(
   Files: *.js, *.ts
   Severity: HIGH

4. v-html in Vue:
   Pattern: v-html=
   Files: *.vue
   Severity: HIGH
```

### Step 7: CSRF Protection

```bash
echo ""
echo "🛡️ CSRF PROTECTION"
echo "=================="

# Check for CSRF middleware
if [ "$HAS_NODE" = "true" ]; then
  if grep -q "csurf\|csrf" package.json 2>/dev/null; then
    echo "✅ CSRF middleware found in package.json"
  else
    echo "⚠️  WARNING: No CSRF middleware detected"
  fi
fi

# Check forms without CSRF
echo ""
echo "Forms without CSRF tokens:"
grep -rn "<form.*method=['\"]post" --include="*.html" --include="*.jsx" --include="*.tsx" . 2>/dev/null | \
  grep -v "csrf\|_token\|CSRF" | head -10
```

### Step 8: Encryption Issues

```
Patterns to search:

1. MD5 for passwords:
   Pattern: md5|MD5
   Context must include: password, hash
   Severity: CRITICAL

2. SHA1 for security:
   Pattern: sha1|SHA1
   Context: password, hash, sign
   Severity: HIGH

3. ECB mode:
   Pattern: ECB|MODE_ECB
   Severity: HIGH

4. Hardcoded IV:
   Pattern: iv\s*[:=]\s*['\"][a-fA-F0-9]{16,}
   Severity: HIGH

5. Weak random:
   Pattern: Math\.random
   Context: token, key, secret
   Severity: HIGH
```

### Step 9: Transport Security

```
Patterns to search:

1. Insecure WebSocket:
   Pattern: ws://
   Files: *.js, *.ts, *.py
   Severity: HIGH

2. HTTP for sensitive:
   Pattern: http://.*api|http://.*auth|http://.*login
   Severity: HIGH

3. SSL disabled:
   Pattern: verify\s*=\s*False|rejectUnauthorized.*false|CERT_NONE
   Severity: CRITICAL
```

### Step 10: Security Headers

```bash
echo ""
echo "📋 SECURITY HEADERS"
echo "==================="

# Express - helmet
if [ "$HAS_NODE" = "true" ]; then
  if grep -q "helmet" package.json 2>/dev/null; then
    echo "✅ helmet middleware installed"
  else
    echo "⚠️  WARNING: helmet not installed (security headers)"
    echo "   Fix: npm install helmet"
  fi
fi

# Next.js headers config
if [ -f "next.config.js" ] || [ -f "next.config.mjs" ]; then
  if grep -q "headers" next.config.* 2>/dev/null; then
    echo "✅ Next.js headers configured"
  else
    echo "⚠️  WARNING: No security headers in next.config"
  fi
fi
```

### Step 11: Sensitive Files

```bash
echo ""
echo "📁 SENSITIVE FILES"
echo "=================="

# Check for tracked sensitive files
echo "Sensitive files in git:"
git ls-files 2>/dev/null | grep -E "\.env$|\.pem$|\.key$|credentials|secrets" | head -10

# Check .gitignore
echo ""
echo "Missing .gitignore entries:"
for pattern in ".env" "*.pem" "*.key" "credentials.json" "secrets.json"; do
  grep -qF "$pattern" .gitignore 2>/dev/null || echo "  MISSING: $pattern"
done
```

### Step 12: Generate Report

Create `SECURITY_AUDIT.md` with all findings:

```markdown
# 🔒 Security Audit Report

**Project:** {project_name}
**Path:** {project_path}
**Date:** {timestamp}

---

## Summary

| Category | 🔴 | 🟠 | 🟡 | 🟢 |
|----------|----|----|----|----|
| Dependencies | {n} | {n} | {n} | {n} |
| Authentication | {n} | {n} | {n} | {n} |
| Injection | {n} | {n} | {n} | {n} |
| CSRF | {n} | {n} | {n} | {n} |
| Encryption | {n} | {n} | {n} | {n} |
| Transport | {n} | {n} | {n} | {n} |
| Headers | {n} | {n} | {n} | {n} |
| Files | {n} | {n} | {n} | {n} |

**Risk Score:** {score}/100

---

## Critical Findings

{critical_findings}

---

## High Priority

{high_findings}

---

## Medium Priority

{medium_findings}

---

## Checklist

- [ ] Upgrade vulnerable dependencies
- [ ] Fix JWT implementation
- [ ] Add auth to unprotected endpoints
- [ ] Implement CSRF protection
- [ ] Use secure encryption
- [ ] Switch to wss://
- [ ] Add security headers
- [ ] Update .gitignore

---

*Generated by /security-audit*
```

## Related Commands

- `/scan-security` - Focused secrets/credentials detection
- `/brownfield-audit` - Full codebase maintenance audit
- `/check-for-leaks` - Git history secret scanning
