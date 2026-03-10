---
uuid: cmd-scan-sec-0x1y2z3a
version: 1.0.0
last_updated: 2025-11-11
description: Scan for security issues (credentials, keys, secrets)
---

# Scan Security

Scan `{directory}` for security issues: credentials, API keys, passwords, secrets, tokens.

## Usage

```bash
/scan-security prototypes/proto-027-semantic-schema-mapper [--fix] [--report=./SECURITY_SCAN.md]
```

**Arguments:**
- `{directory}`: Path to directory to scan
- `--fix`: Automatically remove/redact found secrets (creates backup)
- `--report=./SECURITY_SCAN.md`: Output report path (default: SECURITY_SCAN.md)

## What It Detects

### High-Risk Secrets

**AWS Credentials:**
- AWS Access Key ID (AKIA...)
- AWS Secret Access Key
- AWS Session Token
- AWS Account ID in sensitive contexts

**API Keys:**
- OpenAI API keys (sk-...)
- Anthropic API keys (sk-ant-...)
- GitHub Personal Access Tokens (ghp_...)
- Stripe keys (sk_live_..., sk_test_...)
- Google API keys (AIza...)
- Slack tokens (xox...)
- JWT tokens (eyJ...)

**Database Credentials:**
- Connection strings with passwords
- PostgreSQL URLs (postgres://user:pass@...)
- MongoDB URLs (mongodb://user:pass@...)
- MySQL connection strings
- Redis URLs with auth

**Private Keys:**
- RSA/SSH private keys (`-----BEGIN [TYPE] KEY-----` format)
- PEM files with private keys
- `.p12`, `.pfx` certificate files
- GPG private keys

**Passwords:**
- Password variables (password=, pwd=)
- Basic auth headers (Authorization: Basic ...)
- Hardcoded passwords in code

**Tokens:**
- OAuth tokens
- Bearer tokens
- Session tokens
- API authentication tokens

### Medium-Risk Patterns

**Environment Variables:**
- Sensitive env vars without `.env` in `.gitignore`
- Hardcoded values that should be env vars

**URLs with Credentials:**
- HTTP URLs with embedded credentials
- FTP URLs with passwords

**Email/Username Patterns:**
- Admin credentials
- Default passwords
- Test accounts with real-looking passwords

### Configuration Issues

**Git Issues:**
- `.env` not in `.gitignore`
- `.aws/credentials` tracked
- `secrets.json` tracked
- Private keys in git history

**File Permissions:**
- World-readable `.env` files
- Exposed credentials in public directories

## Workflow

### Step 1: Scan Directory

1. **Find all relevant files**:
   ```bash
   # Use Glob to find files to scan
   **/*.{js,ts,py,go,java,rb,php,json,yaml,yml,env,config,txt,md}
   ```

2. **Exclude safe paths**:
   - `node_modules/`, `venv/`, `.venv/`, `vendor/`
   - `.git/` (but scan for tracked sensitive files)
   - `dist/`, `build/`, `out/`
   - Binary files (`.zip`, `.tar`, `.exe`, etc.)

### Step 2: Pattern Matching

3. **Regex patterns for detection**:

**AWS Credentials:**
```regex
# AWS Access Key ID
AKIA[0-9A-Z]{16}

# AWS Secret Access Key
[A-Za-z0-9/+=]{40}

# AWS Account ID (in sensitive contexts)
aws[_-]?account[_-]?id.*[0-9]{12}
```

**OpenAI/Anthropic Keys:**
```regex
# OpenAI
sk-[A-Za-z0-9]{32,}

# Anthropic
sk-ant-[A-Za-z0-9\-_]{95}
```

**GitHub Tokens:**
```regex
# Personal Access Token
ghp_[A-Za-z0-9]{36}

# OAuth Token
gho_[A-Za-z0-9]{36}

# Fine-grained PAT
github_pat_[A-Za-z0-9_]{82}
```

**Database Connection Strings:**
```regex
# PostgreSQL
postgres://[^:]+:[^@]+@[^/]+

# MongoDB
mongodb(\+srv)?://[^:]+:[^@]+@

# MySQL
mysql://[^:]+:[^@]+@
```

**Private Keys:**
```regex
-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----
```

**Generic Secrets:**
```regex
# Password assignments
(password|passwd|pwd)["\s]*[:=]["\s]*[^"\s]{8,}

# API key assignments
(api[_-]?key|apikey)["\s]*[:=]["\s]*["'][^"']{16,}

# Tokens
(token|auth[_-]?token)["\s]*[:=]["\s]*["'][^"']{20,}

# Bearer tokens
Authorization:\s*Bearer\s+[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_=]*
```

4. **Scan each file** with Grep:
   ```bash
   # Use Grep tool with patterns
   /scan-security uses Grep with multiple patterns
   ```

### Step 3: Analyze Results

5. **Classify findings** by severity:

**CRITICAL** (immediate action required):
- AWS credentials
- Private keys
- Production API keys
- Database passwords in connection strings

**HIGH** (should fix before delivery):
- API keys (test/dev)
- Hardcoded passwords
- OAuth tokens
- JWT tokens

**MEDIUM** (review and consider):
- `.env` not in `.gitignore`
- Sensitive files tracked in git
- Email addresses in sensitive contexts

**LOW** (informational):
- Example credentials in docs
- Commented-out secrets
- Test/mock credentials clearly labeled

6. **Filter false positives**:
   - Exclude if in comments clearly marked as examples
   - Exclude placeholder values ("YOUR_API_KEY_HERE", "REPLACE_ME")
   - Exclude if file is in `examples/`, `docs/`, `tests/` with clear test data
   - Exclude variable declarations without actual values

### Step 4: Generate Report

7. **Create security scan report**:

```markdown
# Security Scan Report

**Directory**: {directory}
**Scan Date**: {timestamp}
**Files Scanned**: {file_count}
**Issues Found**: {total_count}

---

## Summary

- 🔴 **Critical**: {critical_count} (immediate action required)
- 🟠 **High**: {high_count} (fix before delivery)
- 🟡 **Medium**: {medium_count} (review)
- 🟢 **Low**: {low_count} (informational)

---

## Critical Issues

### 🔴 #1: AWS Access Key Exposed

**File**: `src/config/aws.js:15`
**Pattern**: AWS Access Key ID
**Finding**:
\`\`\`javascript
const AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
\`\`\`

**Risk**: Full AWS account access if key is valid
**Recommendation**:
- Remove hardcoded key immediately
- Use AWS IAM roles or environment variables
- Rotate key if committed to git history
- Check CloudTrail for unauthorized access

---

### 🔴 #2: Private Key in Repository

**File**: `.ssh/id_rsa:1`
**Pattern**: RSA Private Key
**Finding**:
\`\`\`
-----BEGIN [RSA PRIVATE KEY]-----
MIIEpAIBAAKCAQEA...
\`\`\`

**Risk**: Unauthorized SSH access to servers
**Recommendation**:
- Remove private key from repository
- Add `*.pem`, `*.key` to `.gitignore`
- Regenerate key pair
- Update authorized_keys on affected servers

---

## High Priority Issues

### 🟠 #3: Database Password in Connection String

**File**: `config/database.yml:8`
**Pattern**: PostgreSQL connection string
**Finding**:
\`\`\`yaml
production:
  url: postgres://admin:MySecretPass123@prod-db.example.com/maindb
\`\`\`

**Risk**: Database access if file exposed
**Recommendation**:
- Use environment variables: `DATABASE_URL`
- Store in AWS Secrets Manager or Parameter Store
- Rotate password immediately

---

{Continue for all findings...}

---

## Configuration Issues

### `.gitignore` Missing Entries

The following sensitive files/patterns are not in `.gitignore`:

- `.env`
- `.env.local`
- `*.pem`
- `*.key`
- `config/secrets.json`

**Recommended `.gitignore` additions:**
\`\`\`gitignore
# Environment variables
.env
.env.local
.env.*.local

# Secrets
secrets.json
*.secret

# Private keys
*.pem
*.key
*.p12
*.pfx

# AWS credentials
.aws/credentials

# SSH keys
id_rsa
id_dsa
id_ed25519
\`\`\`

---

## Recommended Actions

### Immediate (Critical)

1. ❌ **Remove AWS keys** from `src/config/aws.js`
2. ❌ **Delete private key** `.ssh/id_rsa` from repository
3. ❌ **Rotate all exposed credentials**

### Before Delivery (High)

1. ⚠️ **Move database passwords** to environment variables
2. ⚠️ **Add sensitive patterns** to `.gitignore`
3. ⚠️ **Scan git history** for committed secrets

### Review (Medium)

1. 💡 Implement AWS IAM roles for service credentials
2. 💡 Use AWS Secrets Manager for production secrets
3. 💡 Set up pre-commit hooks to prevent future commits

---

## Clean Git History

If secrets were committed to git:

\`\`\`bash
# WARNING: This rewrites git history
# Coordinate with team before running

# Remove specific file from history
git filter-branch --force --index-filter \\
  "git rm --cached --ignore-unmatch {file_path}" \\
  --prune-empty --tag-name-filter cat -- --all

# Force push (if absolutely necessary)
# git push --force --all
\`\`\`

**Safer alternative**: Use `git filter-repo` or `BFG Repo-Cleaner`

---

## Prevention

### Pre-commit Hook

Install pre-commit hook to catch secrets:

\`\`\`bash
# Install gitleaks
brew install gitleaks  # macOS
# or
curl -sSfL https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks-linux-amd64 -o gitleaks

# Add to .git/hooks/pre-commit
#!/bin/sh
gitleaks detect --source . --verbose --no-git
\`\`\`

### Environment Variables

Use `.env.example` template:

\`\`\`bash
# .env.example
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
DATABASE_URL=postgres://user:pass@localhost/db
OPENAI_API_KEY=sk-...
\`\`\`

Instructions in README:
\`\`\`bash
cp .env.example .env
# Edit .env with your actual credentials
\`\`\`

---

## Scan Statistics

- **Total files scanned**: {file_count}
- **Files with issues**: {affected_file_count}
- **Total patterns checked**: {pattern_count}
- **Scan duration**: {duration_ms}ms

---

*Generated by /scan-security*
*Next scan: Before every delivery package creation*
```

### Step 5: Auto-Fix (if --fix flag)

8. **If --fix flag provided**:

   a. **Create backup**:
   ```bash
   cp -r {directory} {directory}.backup-{timestamp}
   ```

   b. **Redact secrets**:
   - Replace AWS keys with `REDACTED_AWS_KEY`
   - Replace API keys with `REDACTED_API_KEY`
   - Replace passwords with `REDACTED_PASSWORD`
   - Comment out connection strings with embedded credentials

   c. **Add to .gitignore**:
   - Append missing patterns to `.gitignore`
   - Create `.gitignore` if doesn't exist

   d. **Report fixes**:
   ```markdown
   ## Auto-Fix Applied

   ✅ Backup created: `{directory}.backup-{timestamp}/`
   ✅ Redacted {count} secrets
   ✅ Updated `.gitignore` with {count} patterns

   **Files modified:**
   - `src/config/aws.js` - Redacted AWS credentials
   - `config/database.yml` - Redacted database password
   - `.gitignore` - Added sensitive file patterns
   ```

### Step 6: Integration with /prepare-delivery

9. **Automatic scan before delivery**:
   - `/prepare-delivery` calls `/scan-security` automatically
   - Blocks delivery if CRITICAL issues found
   - Warns for HIGH issues
   - Includes scan report in delivery package

10. **Delivery gate**:
    ```
    🔴 CRITICAL SECURITY ISSUES FOUND

    Cannot proceed with delivery package creation.
    Found 2 critical issues in prototype:
    - AWS credentials in src/config/aws.js
    - Private key in .ssh/id_rsa

    Action required:
    1. Run: /scan-security {proto_dir} --fix
    2. Review auto-fixes
    3. Retry delivery: /prepare-delivery {proto_name}
    ```

## Detection Accuracy

**High confidence** (auto-flag):
- Well-known patterns (AWS keys, GitHub tokens)
- Private key headers
- Connection strings with passwords

**Medium confidence** (review required):
- Generic "password=" patterns
- API key variables
- Suspicious file names

**Low confidence** (informational):
- Comments with "TODO: add key"
- Example credentials in docs
- Test data clearly marked

## False Positive Handling

**Common false positives:**
- Documentation examples
- Test fixtures with mock data
- Placeholder values
- Generated sample code

**Filtering rules:**
- Skip if line contains "example", "sample", "placeholder", "YOUR_", "REPLACE_"
- Skip if in `docs/`, `examples/`, clearly marked test files
- Skip if value is obviously fake ("password123", "test@example.com")

## Best Practices

1. **Scan before delivery**: Always run before creating delivery package
2. **Review findings**: Don't blindly trust auto-detection
3. **Rotate exposed secrets**: If committed to git, assume compromised
4. **Use secrets management**: AWS Secrets Manager, Parameter Store, env vars
5. **Git history**: Check history for committed secrets
6. **Prevent recurrence**: Pre-commit hooks, CI/CD integration

## Integration

Works with:
- `/prepare-delivery` - Automatic security gate before packaging
- `/check-for-leaks` - Uses similar patterns (leverage existing)
- CI/CD pipelines - Can run as automated check

## Error Handling

**Large directory:**
```
Warning: Directory contains 10,000+ files
Scan may take several minutes
Progress: [=====>    ] 50% (5000/10000 files)
```

**Permission denied:**
```
Warning: Cannot read file: {file_path}
Reason: Permission denied
Skipping...
```

**Binary files:**
```
Info: Skipping binary files (5 files)
Binary files cannot contain readable secrets
```

---

Be thorough, accurate, and security-focused.
