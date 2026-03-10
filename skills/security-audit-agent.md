<!-- File UUID: 9e4f5a2b-6c8d-4e1f-b7a9-d8e0f1a2b3c4 -->
---
name: security-audit-agent
description: Comprehensive security vulnerability scanner with one-page report
version: 1.0.0
aliases: [vuln-audit, sec-audit, cve-scan]
---

# Security Audit Agent

**Comprehensive security vulnerability scanner that generates a one-page findings report.**

## Scan Categories

| Category | Checks | Priority |
|----------|--------|----------|
| Dependencies | CVEs, outdated packages, unmaintained libs | CRITICAL |
| Authentication | JWT issues, missing auth, session problems | CRITICAL |
| Injection | SQL injection, command injection, XSS | CRITICAL |
| CSRF | Missing tokens, unprotected forms | HIGH |
| Encryption | Weak algorithms, password policies | HIGH |
| Transport | ws:// usage, SSL issues | MEDIUM |
| Headers | Missing security headers | MEDIUM |
| Files | Unprotected sensitive files | MEDIUM |

## Execution Steps

### 1. Project Detection

Detect project type and frameworks:

```bash
# Check package managers
[ -f "package.json" ] && echo "nodejs"
[ -f "requirements.txt" ] || [ -f "pyproject.toml" ] && echo "python"
[ -f "go.mod" ] && echo "go"
[ -f "Cargo.toml" ] && echo "rust"

# Check frameworks
grep -l "express" package.json 2>/dev/null && echo "express"
grep -l "fastapi\|FastAPI" **/*.py 2>/dev/null && echo "fastapi"
grep -l "django" **/*.py 2>/dev/null && echo "django"
grep -l "next" package.json 2>/dev/null && echo "nextjs"
```

### 2. Dependency CVE Scan

**Node.js:**
```bash
npm audit --json 2>/dev/null | jq -r '
  .vulnerabilities | to_entries[] |
  "\(.value.severity | ascii_upcase): \(.key) - \(.value.via[0].title // "unknown")"
'
```

**Python:**
```bash
pip-audit --format=json 2>/dev/null | jq -r '.[] |
  "CVE: \(.name)@\(.version) - \(.vulns[0].id)"'
```

**Outdated packages:**
```bash
npm outdated --json 2>/dev/null
pip list --outdated --format=json 2>/dev/null
```

### 3. JWT Security Issues

```
PATTERNS TO DETECT:

🔴 CRITICAL:
- jwt.decode(..., verify=False)
- jwt.verify with algorithms: ['none']
- JWT secret < 32 characters
- No algorithm restriction in verify

🟠 HIGH:
- Missing 'exp' claim (no expiration)
- Token stored in localStorage (XSS risk)
- Token passed in URL parameters
- Weak secret (common words, short)

🟡 MEDIUM:
- Long expiration times (> 24h for access tokens)
- No refresh token rotation
- Missing 'iat' claim
```

**Detection commands:**
```bash
# No verification
grep -rn "verify\s*=\s*False\|verify\s*:\s*false" --include="*.py" --include="*.js" .

# Algorithm none
grep -rn "algorithm.*none\|alg.*none" --include="*.py" --include="*.js" .

# Token in localStorage
grep -rn "localStorage.*token\|sessionStorage.*token" --include="*.js" --include="*.ts" .

# Token in URL
grep -rn "\?.*token=\|&token=" --include="*.js" --include="*.ts" --include="*.py" .

# Missing expiration
grep -rn "jwt\.(sign|encode)" --include="*.js" --include="*.py" . | grep -v "exp"
```

### 4. API Endpoints Without Auth

```
DETECTION PATTERNS:

Express.js:
- app.get('/api/...') without auth middleware
- router.post('/api/...') without protect/authenticate

FastAPI:
- @app.get("/api/...") without Depends(get_current_user)
- @router.post("/api/...") without auth dependency

Django:
- path('api/...') without @login_required
- APIView without permission_classes

Next.js:
- pages/api/*.ts without getSession/getToken check
- app/api/*/route.ts without auth verification
```

**Detection commands:**
```bash
# Express without middleware
grep -rn "app\.\(get\|post\|put\|delete\)\s*(['\"]\/api" --include="*.js" --include="*.ts" . | \
  grep -v "auth\|protect\|middleware\|verify\|session"

# FastAPI without Depends
grep -rn "@app\.\(get\|post\|put\|delete\)\s*(['\"]\/api" --include="*.py" . | \
  grep -v "Depends\|get_current_user\|verify"

# Next.js API routes
find . -path "*/api/*.ts" -o -path "*/api/*.js" 2>/dev/null | while read f; do
  grep -L "getSession\|getToken\|auth\|verify" "$f" 2>/dev/null
done
```

### 5. SQL Injection Detection

```
DANGEROUS PATTERNS:

🔴 Python:
cursor.execute(f"SELECT * FROM {table} WHERE id = {id}")
query = "SELECT * FROM users WHERE name = '" + name + "'"
db.execute("SELECT * FROM users WHERE id = %s" % user_id)

🔴 JavaScript:
db.query(`SELECT * FROM users WHERE id = ${userId}`)
connection.query("SELECT * FROM " + table)

🔴 Go:
db.Query("SELECT * FROM users WHERE id = " + id)
```

**Detection commands:**
```bash
# Python f-strings in execute
grep -rn "execute\s*(f['\"]" --include="*.py" .

# Python string concat in queries
grep -rn "(SELECT|INSERT|UPDATE|DELETE).*\+.*\(user\|name\|id\|input\)" --include="*.py" .

# JS template literals
grep -rn "query\s*(\`.*\$\{" --include="*.js" --include="*.ts" .

# String concat in SQL
grep -rn "(SELECT|INSERT|UPDATE|DELETE).*\+" --include="*.js" --include="*.ts" --include="*.py" .
```

### 6. CSRF Protection

```
CHECKS:

🟠 Missing CSRF middleware:
- Express without csurf/csrf-csrf
- Django with CSRF_COOKIE_HTTPONLY = False
- FastAPI without CSRF protection

🟠 Forms without tokens:
- <form method="post"> without csrf_token
- AJAX POST without X-CSRF-Token header

🟠 Configuration issues:
- SameSite=None without Secure
- Missing CSRF in cookie settings
```

**Detection commands:**
```bash
# Check for CSRF middleware (Express)
grep -rq "csurf\|csrf" package.json || echo "WARN: No CSRF middleware"

# Forms without CSRF
grep -rn "<form.*method=['\"]post" --include="*.html" --include="*.jsx" --include="*.tsx" . | \
  grep -v "csrf\|_token"

# Django CSRF settings
grep -rn "CSRF_COOKIE" --include="settings.py" .
```

### 7. Encryption & Password Issues

```
WEAK PATTERNS:

🔴 CRITICAL:
- MD5 for password hashing
- SHA1 for security purposes
- DES/3DES encryption
- ECB mode for AES
- Hardcoded encryption keys/IVs

🟠 HIGH:
- Password min length < 8
- No complexity requirements
- Plaintext password storage
- Reversible password encoding (base64)

🟡 MEDIUM:
- Key size < 256 bits
- No key rotation mechanism
- Weak PRNG (Math.random for crypto)
```

**Detection commands:**
```bash
# MD5/SHA1 for passwords
grep -rn "md5\|sha1" --include="*.py" --include="*.js" . | grep -i "password\|hash"

# ECB mode
grep -rn "ECB\|MODE_ECB" --include="*.py" --include="*.js" .

# Hardcoded IV
grep -rn "iv\s*[:=]\s*['\"][a-fA-F0-9]" --include="*.py" --include="*.js" .

# Weak random
grep -rn "Math\.random" --include="*.js" --include="*.ts" . | grep -i "token\|key\|secret"

# Short password requirements
grep -rn "minlength.*[<].*8\|min.*length.*[<].*8" --include="*.py" --include="*.js" .
```

### 8. Transport Security

```
ISSUES:

🟠 HIGH:
- ws:// instead of wss:// (unencrypted WebSocket)
- http:// for sensitive endpoints
- SSL verification disabled
- Allow insecure TLS versions (< 1.2)

🟡 MEDIUM:
- Mixed content (http resources on https page)
- Missing HSTS header
- Weak cipher suites
```

**Detection commands:**
```bash
# ws:// usage
grep -rn "ws://" --include="*.js" --include="*.ts" --include="*.py" .

# http:// for APIs
grep -rn "http://.*api\|http://.*auth\|http://.*login" --include="*.js" --include="*.py" .

# SSL verification disabled
grep -rn "verify\s*=\s*False\|rejectUnauthorized.*false\|CERT_NONE" --include="*.py" --include="*.js" .
```

### 9. Security Headers

```
REQUIRED HEADERS:

- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security
- X-XSS-Protection (deprecated but still useful)
- Referrer-Policy
- Permissions-Policy
```

**Detection commands:**
```bash
# Check for helmet (Express)
grep -q "helmet" package.json && echo "PASS: helmet installed" || echo "WARN: No helmet"

# Check Next.js headers
grep -rn "headers" next.config.* 2>/dev/null

# Check for CSP
grep -rn "Content-Security-Policy" --include="*.js" --include="*.ts" --include="*.py" .
```

### 10. Sensitive File Protection

```
FILES TO CHECK:

🔴 Should NOT be in repo:
- .env (with real values)
- *.pem, *.key (private keys)
- credentials.json, secrets.json
- .aws/credentials

🟠 Should be in .gitignore:
- .env.local, .env.*.local
- *.p12, *.pfx
- config/secrets/*
- id_rsa, id_ed25519
```

**Detection commands:**
```bash
# Check tracked sensitive files
git ls-files | grep -E "\.env$|\.pem$|\.key$|credentials|secrets"

# Check .gitignore coverage
for pattern in ".env" "*.pem" "*.key" "credentials.json"; do
  grep -qF "$pattern" .gitignore || echo "MISSING: $pattern"
done
```

## Report Template

Generate `SECURITY_AUDIT.md`:

```markdown
# 🔒 Security Audit Report

**Project:** {project_name}
**Scanned:** {timestamp}
**Duration:** {duration}

---

## Executive Summary

| Category | 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low |
|----------|-------------|---------|-----------|--------|
| Dependencies | {n} | {n} | {n} | {n} |
| Authentication | {n} | {n} | {n} | {n} |
| Injection | {n} | {n} | {n} | {n} |
| CSRF | {n} | {n} | {n} | {n} |
| Encryption | {n} | {n} | {n} | {n} |
| Transport | {n} | {n} | {n} | {n} |
| Headers | {n} | {n} | {n} | {n} |
| Files | {n} | {n} | {n} | {n} |
| **TOTAL** | **{n}** | **{n}** | **{n}** | **{n}** |

**Risk Score:** {score}/100 ({CRITICAL|HIGH|MEDIUM|LOW|PASS})

---

## 🔴 Critical Findings

### 1. {finding_title}
- **Category:** {category}
- **File:** `{file}:{line}`
- **Issue:** {description}
- **Fix:** {remediation}

---

## 🟠 High Priority Findings

{high_findings}

---

## 🟡 Medium Priority Findings

{medium_findings}

---

## 🟢 Low Priority Findings

{low_findings}

---

## Remediation Checklist

### Immediate (Today)
- [ ] {critical_fix_1}
- [ ] {critical_fix_2}

### This Week
- [ ] {high_fix_1}
- [ ] {high_fix_2}

### This Month
- [ ] {medium_fix_1}
- [ ] {medium_fix_2}

---

## Prevention Recommendations

1. **Add pre-commit hooks** - gitleaks, pip-audit
2. **CI/CD scanning** - npm audit, SAST tools
3. **Dependency updates** - Dependabot, Renovate
4. **Security training** - OWASP Top 10 awareness

---

*Generated by Security Audit Agent v1.0*
```

## CLI Usage

```bash
# Full audit
/security-audit

# Audit specific path
/security-audit ./projects/my-api

# Quick scan (deps + auth only)
/security-audit --quick

# Specific categories
/security-audit --categories=deps,auth,injection

# Output formats
/security-audit --format=md    # Markdown (default)
/security-audit --format=html  # HTML report
/security-audit --format=json  # JSON for CI/CD

# Minimum severity
/security-audit --min-severity=high
```

## Severity Definitions

| Level | Description | Action | Examples |
|-------|-------------|--------|----------|
| 🔴 CRITICAL | Active exploitation risk | Fix immediately | SQL injection, leaked AWS keys, RCE |
| 🟠 HIGH | Significant vulnerability | Fix this week | JWT issues, missing auth, XSS |
| 🟡 MEDIUM | Potential risk | Fix this month | CSRF, weak encryption, ws:// |
| 🟢 LOW | Best practice violation | Track/plan | Missing headers, info disclosure |

## CI/CD Integration

Exit codes:
- `0`: No critical/high findings
- `1`: High findings present
- `2`: Critical findings present

JSON output for automation:
```json
{
  "summary": {
    "critical": 2,
    "high": 5,
    "medium": 10,
    "low": 3,
    "score": 45
  },
  "findings": [...],
  "recommendations": [...]
}
```
