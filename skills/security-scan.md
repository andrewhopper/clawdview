<!-- File UUID: 8d2f4e1a-3b7c-4a9e-b5d8-c6e7f8a9b0c1 -->
---
name: security-scan
description: Scan codebase for security vulnerabilities and generate findings report
version: 1.0.0
aliases: [sec, audit, vuln-scan]
---

# Security Scan Agent

**Comprehensive security vulnerability scanner for codebases**

## Execution Flow

1. **Detect project type** → Identify package managers, frameworks, languages
2. **Run dependency audit** → npm audit, pip-audit, cargo audit, etc.
3. **Scan for code vulnerabilities** → Pattern matching for common issues
4. **Check configurations** → Auth, encryption, password policies
5. **Generate report** → Single-page HTML/Markdown with findings

## Scan Categories

### 1. Dependency Vulnerabilities (CRITICAL)

**Package Managers:**
```bash
# Node.js
npm audit --json 2>/dev/null || echo '{"vulnerabilities":{}}'

# Python
pip-audit --format json 2>/dev/null || echo '[]'

# Check package.json for outdated
npm outdated --json 2>/dev/null || echo '{}'

# Check requirements.txt / pyproject.toml versions
```

**Checks:**
- Known CVEs in dependencies
- Outdated packages with security patches
- Deprecated packages
- Packages with no maintainer activity (>2 years)

### 2. Authentication & Authorization Issues

**API Endpoints Without Auth:**
```
# Patterns to detect unprotected routes
- app.get('/api/...') without auth middleware
- @app.route('/api/...') without @login_required
- router.get('/api/...') without protect/auth middleware
- Express routes without passport/jwt middleware
- FastAPI routes without Depends(get_current_user)
```

**JWT Vulnerabilities:**
```
# Critical patterns
- jwt.decode(..., verify=False)
- jwt.verify without algorithm restriction
- 'none' algorithm accepted
- Weak secrets (< 32 chars, common words)
- Missing expiration (no 'exp' claim)
- Token in URL parameters
- Token stored in localStorage (XSS risk)
```

**Session Issues:**
```
- session.secret using default/weak value
- Missing secure/httpOnly cookie flags
- Session fixation vulnerabilities
- Missing CSRF tokens on state-changing endpoints
```

### 3. Injection Vulnerabilities

**SQL Injection:**
```python
# Dangerous patterns
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
query = "SELECT * FROM users WHERE name = '" + name + "'"
db.query(`SELECT * FROM ${table}`)
```

**Command Injection:**
```python
# Dangerous patterns
os.system(f"ls {user_input}")
subprocess.call(user_input, shell=True)
exec(user_input)
eval(user_input)
```

**XSS (Cross-Site Scripting):**
```javascript
# Dangerous patterns
element.innerHTML = userInput
document.write(userInput)
dangerouslySetInnerHTML={{ __html: userInput }}
v-html="userInput"
```

### 4. CSRF Protection

**Missing CSRF Checks:**
```
- POST/PUT/DELETE routes without CSRF token validation
- Missing csrf middleware in Express/FastAPI
- Forms without hidden CSRF field
- AJAX requests without X-CSRF-Token header
```

### 5. Sensitive Data Exposure

**Hardcoded Secrets:**
```
# Pattern matching for
- API keys: /api[_-]?key\s*[:=]\s*['"][a-zA-Z0-9]{20,}/
- AWS keys: /AKIA[0-9A-Z]{16}/
- Private keys: /-----BEGIN (RSA |EC )?PRIVATE KEY-----/
- Passwords: /password\s*[:=]\s*['"][^'"]+['"]/
- JWT secrets: /jwt[_-]?secret\s*[:=]\s*['"][^'"]+['"]/
- Database URLs: /mongodb(\+srv)?:\/\/[^:]+:[^@]+@/
```

**Unprotected Files:**
```
- .env files committed to git
- Config files with credentials
- Private keys in repo
- .pem, .key, .p12 files
- credentials.json, secrets.json
```

### 6. Encryption & Password Policies

**Weak Encryption:**
```
# Flag usage of
- MD5 for password hashing
- SHA1 for security purposes
- DES/3DES encryption
- ECB mode for AES
- Hardcoded IVs
- Key sizes < 256 bits
```

**Password Policy Issues:**
```
# Check for
- No minimum length enforcement (< 8 chars)
- No complexity requirements
- Passwords stored in plaintext
- Reversible password storage
- Missing rate limiting on login
- No account lockout mechanism
```

### 7. Transport Security

**TLS/SSL Issues:**
```
- ws:// instead of wss://
- http:// instead of https:// for sensitive ops
- SSL verification disabled
- Outdated TLS versions (< 1.2)
- Weak cipher suites
```

### 8. Security Headers (Web Apps)

**Missing Headers:**
```
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security
- X-XSS-Protection
- Referrer-Policy
```

## Severity Levels

| Level | Color | Description | Examples |
|-------|-------|-------------|----------|
| CRITICAL | 🔴 | Immediate exploitation risk | SQL injection, RCE, leaked secrets |
| HIGH | 🟠 | Significant vulnerability | JWT issues, missing auth, XSS |
| MEDIUM | 🟡 | Potential risk | CSRF, outdated deps, weak encryption |
| LOW | 🟢 | Best practice violations | Missing headers, info disclosure |
| INFO | ⚪ | Observations | Deprecated patterns, suggestions |

## Report Format

Generate a single-page report:

```markdown
# 🔒 Security Scan Report

**Project:** {project_name}
**Scan Date:** {date}
**Scan Duration:** {duration}

## 📊 Summary

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | {n} |
| 🟠 HIGH | {n} |
| 🟡 MEDIUM | {n} |
| 🟢 LOW | {n} |

**Overall Risk Score:** {score}/100 ({rating})

---

## 🔴 Critical Findings

### CVE-XXXX-XXXXX: {vulnerability_name}
- **File:** `path/to/file.js:123`
- **Package:** {package}@{version}
- **Description:** {description}
- **Fix:** Upgrade to {package}@{fixed_version}

### Hardcoded AWS Credentials
- **File:** `config/settings.py:45`
- **Pattern:** `AKIA...` detected
- **Fix:** Move to environment variable or AWS Secrets Manager

---

## 🟠 High Findings

### Unprotected API Endpoint
- **File:** `routes/users.js:78`
- **Endpoint:** `POST /api/users/delete`
- **Issue:** No authentication middleware
- **Fix:** Add `authMiddleware` before route handler

### JWT Without Expiration
- **File:** `auth/token.js:34`
- **Issue:** Token generated without `exp` claim
- **Fix:** Add expiration: `{ expiresIn: '1h' }`

---

## 🟡 Medium Findings

{list medium findings}

---

## 🟢 Low Findings

{list low findings}

---

## 📋 Recommendations

1. **Immediate Actions** (Critical/High)
   - [ ] Rotate exposed credentials
   - [ ] Add auth to unprotected endpoints
   - [ ] Upgrade vulnerable packages

2. **Short-term** (Medium)
   - [ ] Implement CSRF protection
   - [ ] Add security headers
   - [ ] Review password policies

3. **Long-term** (Low/Best Practices)
   - [ ] Set up automated dependency scanning
   - [ ] Implement security testing in CI/CD
   - [ ] Conduct penetration testing

---

## 🛠️ Tools Used

- npm audit / pip-audit
- Pattern matching for code vulnerabilities
- Configuration analysis

**Generated by:** Claude Security Scanner v1.0
```

## CLI Arguments

```bash
# Scan current directory
/security-scan

# Scan specific path
/security-scan path/to/project

# Output formats
/security-scan --format md      # Markdown (default)
/security-scan --format html    # HTML report
/security-scan --format json    # JSON for CI/CD

# Severity filter
/security-scan --min-severity high  # Only HIGH and CRITICAL

# Skip categories
/security-scan --skip deps      # Skip dependency audit
/security-scan --skip secrets   # Skip secret scanning

# Quick scan (deps + secrets only)
/security-scan --quick

# Verbose output
/security-scan --verbose
```

## Implementation Rules

1. **Non-destructive** → Read-only scanning, never modify files
2. **Privacy-aware** → Never log actual secret values, only patterns
3. **False positive handling** → Mark uncertain findings as "potential"
4. **Context-aware** → Check .gitignore, distinguish test vs prod code
5. **Incremental** → Show progress during scan

## Detection Patterns

### Language-Specific Checks

**Python:**
```python
# File patterns to scan
*.py

# Framework detection
- Django: settings.py, urls.py
- FastAPI: main.py with FastAPI import
- Flask: app.py with Flask import

# Specific checks
- DEBUG = True in production
- ALLOWED_HOSTS = ['*']
- insecure deserialization (pickle.loads)
```

**JavaScript/TypeScript:**
```javascript
// File patterns
*.js, *.ts, *.jsx, *.tsx

// Framework detection
- Express: app.use(), router.get()
- Next.js: pages/, app/, next.config.js
- React: components with dangerouslySetInnerHTML

// Specific checks
- NODE_ENV !== 'production' checks missing
- prototype pollution vulnerabilities
- regex DoS (ReDoS)
```

**Go:**
```go
// File patterns
*.go

// Specific checks
- sql.Query with string concatenation
- http.ListenAndServe without TLS
- weak random (math/rand vs crypto/rand)
```

## Output Location

Save report to:
```
{project_root}/SECURITY_REPORT.md
```

Or if specified:
```
{output_path}/security-report-{date}.{format}
```

## Integration with CI/CD

Exit codes:
- 0: No critical/high findings
- 1: High findings present
- 2: Critical findings present

JSON output for CI/CD parsing:
```json
{
  "summary": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 10
  },
  "findings": [...],
  "scan_metadata": {...}
}
```

## Error Handling

- **Package manager not found:** Skip that audit, note in report
- **Permission denied:** Log and continue
- **Large files:** Skip files > 1MB, note in report
- **Binary files:** Skip, not applicable
