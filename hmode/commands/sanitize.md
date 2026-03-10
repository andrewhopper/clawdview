---
description: Sanitize files by replacing PII, secrets, and sensitive content before sharing
---

Scan and sanitize files to remove API keys, emails, names, PII, profanity, and embarrassing content.

**Usage:**
```bash
/sanitize [--from DIR] [--audit-only] [--level LEVEL] [--custom-rules FILE]
/sanitize --git-history [--since DATE] [--sanitize]
```

**Examples:**
```bash
# Interactive sanitization of current directory
/sanitize

# Audit only (no changes) with HTML report
/sanitize --from ./demo-assets --audit-only

# Aggressive sanitization with custom rules
/sanitize --level aggressive --custom-rules .sanitize-rules.yml

# Sanitize specific file types only
/sanitize --from ./code --include "*.py,*.js,*.env"

# Dry run to preview changes
/sanitize --dry-run

# === GIT HISTORY SCANNING ===

# Scan entire git history for secrets (scan only)
/sanitize --git-history

# Scan git history since date
/sanitize --git-history --since "2024-01-01"

# Scan and sanitize git history (DANGEROUS - rewrites history)
/sanitize --git-history --sanitize

# Scan specific branch
/sanitize --git-history --branch develop
```

**Arguments:**

**File Sanitization:**
- `--from DIR` - Source directory to sanitize (default: current directory)
- `--audit-only` - Generate audit report without making changes
- `--level LEVEL` - Sanitization level: minimal, standard, aggressive (default: standard)
- `--custom-rules FILE` - YAML file with custom sanitization rules
- `--include PATTERNS` - Comma-separated file patterns to include (e.g., "*.py,*.md")
- `--exclude PATTERNS` - Comma-separated patterns to exclude (e.g., "*.min.js,node_modules")
- `--dry-run` - Preview changes without modifying files
- `--output-dir DIR` - Output directory for sanitized files (default: ./sanitized-{timestamp})
- `--skip-images` - Skip image analysis (faster but less thorough)
- `--yes` - Skip confirmations

**Git History Sanitization:**
- `--git-history` - Scan git history for secrets (instead of files)
- `--since DATE` - Only scan commits since date (e.g., "2024-01-01", "3 months ago")
- `--branch NAME` - Branch to scan (default: HEAD)
- `--sanitize` - Actually sanitize git history (DANGEROUS - rewrites history)
- `--force` - Skip confirmation prompts

**Detection Categories:**

1. **Secrets & API Keys:**
   - AWS credentials (AKIA*, aws_secret_access_key)
   - OpenAI/Anthropic API keys
   - GitHub tokens (ghp_*, gho_*, ghs_*)
   - JWT tokens
   - Private keys (-----BEGIN PRIVATE KEY-----)
   - Database connection strings
   - OAuth client secrets

2. **Personal Information:**
   - Email addresses (all domains)
   - Phone numbers (US, international formats)
   - Social Security Numbers
   - Credit card numbers
   - IP addresses
   - Physical addresses
   - Names (first/last from common name databases)

3. **Embarrassing Content:**
   - Profanity and swear words
   - Offensive language
   - TODO comments with embarrassing notes
   - Debug print statements with personal info
   - Silly variable names or test data

4. **Company Sensitive:**
   - Internal domains (@amazon.com, @company.com)
   - Project codenames
   - Internal tool names
   - Customer names (if provided in custom rules)

**Sanitization Levels:**

**Minimal** (safe for external demos):
- API keys → REDACTED_API_KEY
- Passwords → REDACTED_PASSWORD
- AWS account IDs → 000000000000

**Standard** (safe for public sharing):
- All minimal replacements
- Email addresses → demo@example.com, user1@example.com
- Names → John Doe, Jane Smith
- Phone numbers → +1-555-0100
- IP addresses → 192.0.2.1 (TEST-NET)

**Aggressive** (maximum privacy):
- All standard replacements
- Generic text patterns (urls, domains)
- Company-specific terms (from custom rules)
- All TODO/FIXME comments
- Git history references
- Profanity → [REDACTED]

**Interactive Workflow:**

1. **Scan Phase:**
   ```
   🔍 Scanning 47 files for sensitive content...

   Found issues:
   ✗ 12 API keys in 4 files
   ✗ 23 email addresses in 8 files
   ✗ 7 names in 5 files
   ✗ 3 phone numbers in 2 files
   ✗ 2 profanity instances in 1 file
   ⚠️ 5 images require manual review
   ```

2. **Interactive Configuration:**
   ```
   Replacement Options:

   [1] Use default replacements
   [2] Customize replacements
   [3] Review each replacement

   > 2

   Email replacements:
   andyhop@amazon.com → [1] demo@example.com [2] user@example.com [3] custom
   > 1

   Name replacements:
   Andy Hopper → [1] John Doe [2] Alex Smith [3] custom
   > 1
   ```

3. **Image Analysis** (using hmode/shared/tools/file_analyzer.py):
   ```
   📸 Analyzing images for sensitive content...

   screenshot.png:
   ⚠️ Contains email address in UI
   ⚠️ Shows AWS account ID in console
   ⚠️ Visible API key in terminal

   [1] Blur regions [2] Skip file [3] Manual review
   ```

4. **Preview Changes:**
   ```
   Changes to apply:

   config.yaml:
   - aws_access_key: AKIAI44QH8DHBEXAMPLE
   + aws_access_key: REDACTED_AWS_ACCESS_KEY

   - email: andyhop@amazon.com
   + email: demo@example.com

   Apply changes? [Y/n/review]
   ```

5. **Generate Outputs:**
   - Sanitized files in `./sanitized-{timestamp}/`
   - `sanitization-audit.html` - Interactive audit report
   - `sanitization-log.json` - Machine-readable change log
   - `sanitization-key.enc` - Reversible key (if --reversible)

**Audit Report (HTML):**

The audit report includes:
- Executive summary with issue counts by category
- File-by-file breakdown with line numbers
- Before/after diff viewer
- Risk scoring (Critical, High, Medium, Low)
- Image analysis results with thumbnails
- Compliance checklist (GDPR, HIPAA, SOC2)
- Recommended actions
- False positive marking interface

**Custom Rules File (.sanitize-rules.yml):**

```yaml
version: 1.0

# Custom patterns to detect
patterns:
  - name: project_codename
    regex: "Project-Phoenix"
    replacement: "Project-Demo"
    severity: medium

  - name: internal_domain
    regex: "@acmecorp\\.com"
    replacement: "@example.com"
    severity: high

# Custom word lists
wordlists:
  customer_names:
    - "AcmeCorp"
    - "TechStartup Inc"

  embarrassing_terms:
    - "hack"
    - "quick fix"
    - "don't show client"

# Name mappings (preserve relationships)
name_mappings:
  "Andy Hopper": "John Doe"
  "Sarah Chen": "Jane Smith"

# File-specific rules
file_rules:
  "*.env":
    level: aggressive
  "*.md":
    level: standard
    skip_code_blocks: true

# Image analysis settings
image_analysis:
  enabled: true
  check_for:
    - emails
    - api_keys
    - account_ids
    - names
  blur_sensitivity: medium
```

**Output Structure:**

```
sanitized-2025-12-22-143012/
├── files/                      # Sanitized files (mirrors source structure)
│   ├── config.yaml
│   ├── README.md
│   └── screenshots/
│       └── demo-blurred.png
├── sanitization-audit.html     # Interactive audit report
├── sanitization-log.json       # Machine-readable log
├── sanitization-key.enc        # Reversible key (if --reversible)
└── false-positives.txt         # User-marked false positives
```

**Audit Report Features:**
- Filterable table (by severity, category, file type)
- Search functionality
- Diff viewer with syntax highlighting
- Image comparison (original vs sanitized)
- Export to PDF
- Mark false positives (updates exclusion list)
- Risk heatmap visualization
- Timeline view of when sensitive data was introduced

**Reversible Sanitization:**

With `--reversible` flag:
1. Generate encryption key
2. Store original values in `sanitization-key.enc`
3. Apply replacements with UUID markers
4. Use `/unsanitize` command to restore

```bash
# Sanitize with reversible key
/sanitize --reversible

# Later, restore original values
/unsanitize --key sanitization-key.enc --from ./sanitized-output
```

**Pre-commit Integration:**

Generate pre-commit hook:
```bash
/sanitize --generate-hook

# Creates .git/hooks/pre-commit that:
# 1. Scans staged files
# 2. Blocks commit if secrets detected
# 3. Suggests /sanitize command
```

**Compliance Reports:**

Audit report includes compliance sections:
- **GDPR:** PII detection and handling summary
- **HIPAA:** PHI detection results
- **SOC2:** Access control and data handling
- **PCI-DSS:** Payment card data detection

---

## Git History Sanitization

Scan and sanitize secrets that were committed to git history.

**Why This Matters:**
Even if you remove secrets from current files, they remain in git history forever.
Anyone with repository access can view old commits and extract secrets.

**Workflow:**

1. **Scan Phase** (Safe - no changes):
   ```
   🔍 Scanning git history...
   Found 142 commits to scan

   Progress: 142/142 commits (100%)
   Files scanned: 1,247

   📋 Scan Results
   Commits scanned: 142
   Files scanned: 1,247
   Secrets found: 23

   By severity:
     ✗ Critical: 8 (AWS keys, private keys)
     ✗ High: 12 (API keys, tokens)
     ✗ Medium: 3 (emails, account IDs)

   Affected commits: 15
   ```

2. **Interactive Audit Report**:
   - Browse commits with secrets
   - See exact line numbers and files
   - View matched content
   - Export findings to JSON

3. **Sanitization Phase** (DANGEROUS):
   ```
   ⚠️ WARNING: Git History Sanitization

   This operation will:
   • REWRITE git history (destructive)
   • Require force push to remote
   • Require all collaborators to re-clone
   • NOT affect existing forks

   Type 'YES' to confirm: YES

   ✅ Created backup branch: backup/pre-sanitize-20251222-143012
   🔧 Rewriting git history...
   ✅ Git history sanitized successfully
   ```

**Technical Implementation:**

Uses `git-filter-repo` (modern, GitHub-recommended):
- Faster than BFG Repo-Cleaner
- Better handling of branches/tags
- Supports regex replacements
- Maintains commit metadata

**Safety Features:**

1. **Automatic Backup**: Creates backup branch before any changes
2. **Dry Run**: Preview what will be changed
3. **Confirmation**: Requires typing "YES" to proceed
4. **Audit Trail**: Full JSON log of all findings

**Remediation Checklist:**

After sanitizing git history:

```
□ Rotate all exposed secrets immediately
□ Force push to remote: git push --force-with-lease origin main
□ Notify all collaborators to re-clone (not pull!)
□ Update CI/CD pipelines with new credentials
□ Enable GitHub/GitLab secret scanning
□ Add pre-commit hooks to prevent future leaks
□ Check for public forks (they still have secrets!)
□ Consider making repo private if sensitive
```

**Common Scenarios:**

**Scenario 1: Pre-open-source check**
```bash
# Before open-sourcing a private repo
/sanitize --git-history
# Review audit report
# If clean, proceed with open source
# If secrets found, sanitize then open source
```

**Scenario 2: Leaked API key**
```bash
# Someone committed an API key 6 months ago
/sanitize --git-history --since "6 months ago"
# Review findings
/sanitize --git-history --sanitize
# Rotate the leaked key
# Force push
```

**Scenario 3: Pre-delivery to customer**
```bash
# Before sharing repo with customer
/sanitize --git-history
# Sanitize if needed
# Then use /deliver-assets to share
```

**Installation:**

Requires git-filter-repo:
```bash
pip3 install git-filter-repo
```

**Limitations:**

- Cannot sanitize public forks (they have their own history)
- Large repos take time (~1000 commits/minute)
- All collaborators must re-clone after force push
- Tags/releases may need manual recreation
- GitHub PRs may show broken diffs after rewrite

**Performance:**
- Scans ~1000 files/second (text)
- ~10 images/second (with analysis)
- Parallel processing for large directories
- Progress bar with ETA

**False Positive Handling:**

```
Mark as false positive:
example@example.com → Actually a test email (ok to keep)
[Y/n] y

Added to exclusion list: .sanitize-exclusions.txt
```

**Integration with /deliver:**

Sanitize before delivery:
```bash
# Sanitize and deliver in one command
/sanitize --from ./demo && /deliver-assets --from ./sanitized-{timestamp}
```

**Credentials:**
- Uses Anthropic API for image analysis (via file_analyzer.py)
- Secret ID: `anthropic-api-key` in AWS Secrets Manager

**Setup:**
```bash
# Install dependencies
pip3 install pyyaml pillow cryptography anthropic-sdk

# Optional: Create custom rules
cp shared/templates/sanitize-rules.example.yml .sanitize-rules.yml
```

Script location: `shared/scripts/sanitize_assets.py`

**Related Commands:**
- `/deliver-assets` - Deliver sanitized assets
- `/check-for-leaks` - Quick secret scan
- `/qa-microsite` - QA sanitized websites

---

Now executing sanitize command...

```bash
#!/bin/bash

# Get the repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Check if git history mode
if [[ "$*" == *"--git-history"* ]]; then
    SCRIPT_PATH="$REPO_ROOT/shared/scripts/sanitize_git_history.py"
else
    SCRIPT_PATH="$REPO_ROOT/shared/scripts/sanitize_assets.py"
fi

# Check if Python script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: Script not found at $SCRIPT_PATH"
    exit 1
fi

# Check if required packages are installed
python3 -c "import yaml" 2>/dev/null || {
    echo "📦 Installing pyyaml..."
    pip3 install pyyaml>=6.0
}

python3 -c "import PIL" 2>/dev/null || {
    echo "📦 Installing pillow..."
    pip3 install pillow>=10.0.0
}

# Execute the Python script with all arguments
python3 "$SCRIPT_PATH" "$@"
```
