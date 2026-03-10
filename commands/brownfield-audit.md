---
description: Audit and maintain brownfield codebases (deps, security, secrets, docs, setup)
version: 1.0.0
---

# Brownfield Audit

Comprehensive maintenance tool for existing codebases. Checks dependencies, security, secrets in git history, documentation, and project setup standards.

## Arguments

```
$ARGUMENTS = [options] [path]

Options:
  --sections=<list>   Comma-separated sections (deps,security,secrets,docs,setup,all)
  --fix               Attempt to auto-fix issues where possible
  --report            Generate full report (markdown)
  --severity=<level>  Filter by severity (critical,high,medium,low,info)

Path:
  Directory to audit (default: current directory)

Examples:
  /brownfield-audit
  /brownfield-audit ./projects/my-app
  /brownfield-audit --sections=deps,security
  /brownfield-audit --fix --sections=docs,setup
```

## Section Overview

| Section | Checks | Focus Area |
|---------|--------|------------|
| `deps` | 6 | Package updates, outdated dependencies |
| `security` | 5 | Vulnerability scanning, CVEs |
| `secrets` | 4 | Git history for leaked credentials |
| `docs` | 7 | README, setup instructions, licensing |
| `setup` | 8 | Makefile, env files, database seeds |
| **Total** | **30** | |

## Instructions

### Step 0: Parse Arguments

```python
import os
from pathlib import Path

args = "$ARGUMENTS"
sections_to_run = ["deps", "security", "secrets", "docs", "setup"]  # all by default
auto_fix = False
generate_report = True
severity_filter = None
target_path = "."

# Parse flags
if "--sections=" in args:
    sections_str = args.split("--sections=")[1].split()[0]
    sections_to_run = [s.strip() for s in sections_str.split(",")]
    args = args.replace(f"--sections={sections_str}", "").strip()

if "--fix" in args:
    auto_fix = True
    args = args.replace("--fix", "").strip()

if "--report" in args:
    generate_report = True
    args = args.replace("--report", "").strip()

if "--severity=" in args:
    severity_filter = args.split("--severity=")[1].split()[0]
    args = args.replace(f"--severity={severity_filter}", "").strip()

# Remaining arg is path
remaining = args.strip()
if remaining and not remaining.startswith("--"):
    target_path = remaining

TARGET = Path(target_path).resolve()
```

### Step 1: Detect Project Type

```bash
cd "$TARGET"

# Detect project types
PROJECT_TYPES=""

# Python
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "Pipfile" ]; then
    PROJECT_TYPES="${PROJECT_TYPES}python,"
fi

# Node.js
if [ -f "package.json" ]; then
    PROJECT_TYPES="${PROJECT_TYPES}nodejs,"
fi

# Rust
if [ -f "Cargo.toml" ]; then
    PROJECT_TYPES="${PROJECT_TYPES}rust,"
fi

# Go
if [ -f "go.mod" ]; then
    PROJECT_TYPES="${PROJECT_TYPES}go,"
fi

# Ruby
if [ -f "Gemfile" ]; then
    PROJECT_TYPES="${PROJECT_TYPES}ruby,"
fi

echo "Detected project types: $PROJECT_TYPES"
```

---

## Section: Dependencies (deps)

### DEP-01: Check for Outdated Packages

**Python:**
```bash
# pip-check-reqs or pip list --outdated
pip list --outdated --format=json 2>/dev/null | python -c "
import json, sys
data = json.load(sys.stdin)
for pkg in data:
    print(f\"  {pkg['name']}: {pkg['version']} → {pkg['latest_version']}\")
"
```

**Node.js:**
```bash
npm outdated --json 2>/dev/null | python -c "
import json, sys
data = json.load(sys.stdin)
for name, info in data.items():
    print(f\"  {name}: {info.get('current', '?')} → {info.get('latest', '?')}\")
"
```

**Rust:**
```bash
cargo outdated 2>/dev/null || echo "Install with: cargo install cargo-outdated"
```

### DEP-02: Check Dependency Lock Files

| Project Type | Expected Lock File | Severity |
|--------------|-------------------|----------|
| Python (pip) | requirements.txt (with versions) | high |
| Python (poetry) | poetry.lock | high |
| Python (pipenv) | Pipfile.lock | high |
| Node.js | package-lock.json or yarn.lock | high |
| Rust | Cargo.lock | high |
| Go | go.sum | high |

```bash
# Check for lock files
MISSING_LOCKS=""

if [ -f "requirements.txt" ]; then
    # Check if versions are pinned
    UNPINNED=$(grep -vE "==" requirements.txt | grep -v "^#" | grep -v "^$" | wc -l)
    if [ "$UNPINNED" -gt 0 ]; then
        echo "WARN: $UNPINNED packages without pinned versions"
    fi
fi

if [ -f "package.json" ] && [ ! -f "package-lock.json" ] && [ ! -f "yarn.lock" ]; then
    MISSING_LOCKS="${MISSING_LOCKS}package-lock.json,"
fi
```

### DEP-03: Check for Deprecated Packages

```bash
# Python - check for deprecated packages
pip list --format=json 2>/dev/null | python -c "
import json, sys
DEPRECATED = ['nose', 'mock', 'imp', 'optparse', 'pycrypto']
data = json.load(sys.stdin)
for pkg in data:
    if pkg['name'].lower() in [d.lower() for d in DEPRECATED]:
        print(f\"  DEPRECATED: {pkg['name']}\")
"
```

### DEP-04: Major Version Gap Detection

```bash
# Detect if major versions behind (e.g., Django 3.x when 5.x is available)
echo "Checking for major version gaps..."
```

### DEP-05: Unused Dependencies

**Python:**
```bash
# Check for unused imports (requires pipreqs or similar)
pip install pipreqs 2>/dev/null
pipreqs --print --force . 2>/dev/null | sort > /tmp/used_deps.txt
cat requirements.txt | grep -v "^#" | cut -d= -f1 | sort > /tmp/declared_deps.txt
comm -23 /tmp/declared_deps.txt /tmp/used_deps.txt
```

### DEP-06: Python Version Compatibility

```bash
# Check Python version classifiers
if [ -f "pyproject.toml" ]; then
    grep -A5 "python_requires" pyproject.toml
fi
if [ -f "setup.py" ]; then
    grep "python_requires" setup.py
fi
```

---

## Section: Security (security)

### SEC-01: Vulnerability Scan (Python)

```bash
# pip-audit (recommended)
pip install pip-audit 2>/dev/null
pip-audit --format=json 2>/dev/null | python -c "
import json, sys
data = json.load(sys.stdin)
for vuln in data.get('dependencies', []):
    for v in vuln.get('vulns', []):
        print(f\"  {vuln['name']}: {v['id']} - {v.get('fix_versions', 'no fix')}\")
"
```

### SEC-02: Vulnerability Scan (Node.js)

```bash
npm audit --json 2>/dev/null | python -c "
import json, sys
data = json.load(sys.stdin)
vulns = data.get('vulnerabilities', {})
for name, info in vulns.items():
    print(f\"  {name}: {info.get('severity', '?')} - {info.get('via', '?')}\")
"
```

### SEC-03: Check for Known Vulnerable Patterns

```bash
# Check for hardcoded secrets in code
echo "Scanning for hardcoded secrets patterns..."

# Common patterns
grep -rn --include="*.py" --include="*.js" --include="*.ts" \
    -E "(password|secret|api_key|apikey|token)\s*=\s*['\"][^'\"]+['\"]" \
    . 2>/dev/null | head -20

# AWS keys
grep -rn --include="*.py" --include="*.js" --include="*.ts" \
    -E "AKIA[0-9A-Z]{16}" \
    . 2>/dev/null | head -10
```

### SEC-04: Security Headers Check (if web project)

```bash
# Check for security-related configurations
if [ -f "package.json" ]; then
    grep -E "(helmet|cors|csrf)" package.json
fi
```

### SEC-05: Dangerous Function Usage

```bash
# Python
grep -rn --include="*.py" \
    -E "(eval\(|exec\(|pickle\.loads|subprocess\.call\(.*shell=True)" \
    . 2>/dev/null | head -10

# JavaScript/TypeScript
grep -rn --include="*.js" --include="*.ts" \
    -E "(eval\(|innerHTML\s*=|document\.write)" \
    . 2>/dev/null | head -10
```

---

## Section: Secrets in Git History (secrets)

### SECRET-01: Scan Git History for Keys

```bash
# Use trufflehog or gitleaks if available
if command -v gitleaks &> /dev/null; then
    gitleaks detect --source="$TARGET" --no-banner --report-format=json 2>/dev/null
elif command -v trufflehog &> /dev/null; then
    trufflehog filesystem "$TARGET" --json 2>/dev/null
else
    echo "WARN: Install gitleaks or trufflehog for comprehensive scanning"
    echo "  brew install gitleaks"
    echo "  pip install trufflehog"
fi
```

### SECRET-02: Manual Pattern Scan

```bash
# Scan git history for common secret patterns
echo "Scanning git history for secrets..."

# AWS Access Keys
git log -p --all 2>/dev/null | grep -E "AKIA[0-9A-Z]{16}" | head -5

# AWS Secret Keys
git log -p --all 2>/dev/null | grep -E "['\"][A-Za-z0-9/+=]{40}['\"]" | head -5

# Private keys
git log -p --all 2>/dev/null | grep -E "-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----" | head -5

# Generic API keys
git log -p --all 2>/dev/null | grep -iE "(api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"][^'\"]{20,}" | head -5

# Database URLs
git log -p --all 2>/dev/null | grep -E "(postgres|mysql|mongodb)://[^:]+:[^@]+@" | head -5
```

### SECRET-03: Check .gitignore Coverage

```bash
# Verify sensitive files are ignored
SHOULD_IGNORE=".env .env.local .env.*.local *.pem *.key credentials.json secrets.json"

echo "Checking .gitignore for sensitive patterns..."
for pattern in $SHOULD_IGNORE; do
    if ! grep -qF "$pattern" .gitignore 2>/dev/null; then
        echo "  MISSING: $pattern"
    fi
done
```

### SECRET-04: Check for Committed Sensitive Files

```bash
# Check if any sensitive files are tracked
SENSITIVE_FILES=$(git ls-files 2>/dev/null | grep -E "\.env$|\.pem$|\.key$|credentials|secrets" | head -10)
if [ -n "$SENSITIVE_FILES" ]; then
    echo "CRITICAL: Sensitive files in git history:"
    echo "$SENSITIVE_FILES"
fi
```

---

## Section: Documentation (docs)

### DOC-01: README.md Exists

| Check | Severity |
|-------|----------|
| README.md exists | critical |
| Has project title | high |
| Has description | high |
| Has setup instructions | high |
| Has usage examples | medium |

```bash
if [ -f "README.md" ]; then
    echo "PASS: README.md exists"

    # Check sections
    grep -q "^#" README.md && echo "  Has title"
    grep -qi "install\|setup\|getting started" README.md && echo "  Has setup section"
    grep -qi "usage\|example\|how to" README.md && echo "  Has usage section"
else
    echo "FAIL: README.md missing"
fi
```

### DOC-02: LICENSE File

```bash
if [ -f "LICENSE" ] || [ -f "LICENSE.txt" ] || [ -f "LICENSE.md" ]; then
    echo "PASS: License file exists"
    head -2 LICENSE* 2>/dev/null
else
    echo "WARN: No LICENSE file found"
    echo "  Create one at: https://choosealicense.com/"
fi
```

### DOC-03: Author Information

```bash
# Check various locations for author info
AUTHOR_FOUND=false

# package.json
if [ -f "package.json" ]; then
    if grep -q '"author"' package.json; then
        echo "PASS: Author in package.json"
        grep '"author"' package.json
        AUTHOR_FOUND=true
    fi
fi

# pyproject.toml
if [ -f "pyproject.toml" ]; then
    if grep -q 'authors' pyproject.toml; then
        echo "PASS: Author in pyproject.toml"
        grep -A2 'authors' pyproject.toml
        AUTHOR_FOUND=true
    fi
fi

# setup.py
if [ -f "setup.py" ]; then
    if grep -q 'author' setup.py; then
        echo "PASS: Author in setup.py"
        grep 'author' setup.py
        AUTHOR_FOUND=true
    fi
fi

# README
if grep -qi 'author\|maintainer\|created by\|built by' README.md 2>/dev/null; then
    echo "PASS: Author mentioned in README"
    AUTHOR_FOUND=true
fi

if [ "$AUTHOR_FOUND" = false ]; then
    echo "WARN: No author information found"
fi
```

### DOC-04: CONTRIBUTING.md (for OSS)

```bash
if [ -f "CONTRIBUTING.md" ] || [ -f ".github/CONTRIBUTING.md" ]; then
    echo "PASS: CONTRIBUTING.md exists"
else
    echo "INFO: No CONTRIBUTING.md (optional for non-OSS)"
fi
```

### DOC-05: CHANGELOG.md

```bash
if [ -f "CHANGELOG.md" ] || [ -f "HISTORY.md" ] || [ -f "NEWS.md" ]; then
    echo "PASS: Changelog exists"
else
    echo "INFO: No CHANGELOG.md"
fi
```

### DOC-06: API Documentation

```bash
# Check for API docs
if [ -d "docs" ] || [ -d "documentation" ]; then
    echo "PASS: /docs directory exists"
elif [ -f "docs/index.html" ] || [ -f "docs/README.md" ]; then
    echo "PASS: Documentation exists"
else
    echo "INFO: No /docs directory"
fi
```

### DOC-07: Code Comments Quality

```bash
# Check docstring coverage (Python)
if [ -f "*.py" ] 2>/dev/null || find . -name "*.py" -type f | head -1 | grep -q .; then
    TOTAL_FUNCS=$(grep -rn "^def " --include="*.py" . 2>/dev/null | wc -l)
    WITH_DOCS=$(grep -rn -A1 "^def " --include="*.py" . 2>/dev/null | grep '"""' | wc -l)
    echo "Python docstring coverage: $WITH_DOCS / $TOTAL_FUNCS functions"
fi
```

---

## Section: Project Setup (setup)

### SETUP-01: Makefile with Standard Targets

| Target | Purpose | Severity |
|--------|---------|----------|
| `make setup` | Initial project setup | critical |
| `make run` | Run the application | critical |
| `make test` | Run tests | high |
| `make lint` | Run linters | medium |
| `make clean` | Clean build artifacts | medium |
| `make build` | Build for production | medium |

```bash
if [ -f "Makefile" ]; then
    echo "PASS: Makefile exists"

    # Check for standard targets
    for target in setup run test lint clean build; do
        if grep -q "^${target}:" Makefile; then
            echo "  PASS: make $target"
        else
            echo "  MISSING: make $target"
        fi
    done
else
    echo "FAIL: No Makefile found"
    echo "  Create a Makefile with: setup, run, test, lint, clean, build targets"
fi
```

### SETUP-02: Example Environment File

```bash
if [ -f "example.env" ] || [ -f ".env.example" ] || [ -f "env.example" ] || [ -f ".env.sample" ]; then
    echo "PASS: Example env file exists"
    ENV_EXAMPLE=$(ls example.env .env.example env.example .env.sample 2>/dev/null | head -1)

    # Check if it has placeholder values (not real secrets)
    if grep -qE "(your_|xxx|placeholder|change_me|<.*>)" "$ENV_EXAMPLE"; then
        echo "  PASS: Has placeholder values"
    else
        echo "  WARN: May contain real values - verify placeholders"
    fi
else
    echo "FAIL: No example.env or .env.example file"
    echo "  Create one with: cp .env example.env && edit placeholders"
fi
```

### SETUP-03: Requirements File (Python)

```bash
# Python projects
if [ -f "requirements.txt" ]; then
    echo "PASS: requirements.txt exists"

    # Check if versions are pinned
    TOTAL=$(grep -v "^#" requirements.txt | grep -v "^$" | wc -l)
    PINNED=$(grep -E "==" requirements.txt | wc -l)

    echo "  Packages: $TOTAL total, $PINNED pinned"

    if [ "$PINNED" -lt "$TOTAL" ]; then
        echo "  WARN: $(($TOTAL - $PINNED)) packages without pinned versions"
    fi

    # Check for requirements-dev.txt
    if [ -f "requirements-dev.txt" ] || [ -f "requirements_dev.txt" ]; then
        echo "PASS: Dev requirements file exists"
    else
        echo "INFO: No separate dev requirements file"
    fi
elif [ -f "pyproject.toml" ]; then
    echo "PASS: Using pyproject.toml for dependencies"
elif [ -f "Pipfile" ]; then
    echo "PASS: Using Pipfile for dependencies"
else
    # Check if this is a Python project
    if find . -name "*.py" -type f | head -1 | grep -q .; then
        echo "FAIL: Python project without requirements.txt"
    fi
fi
```

### SETUP-04: Database Seeds/Migrations

```bash
# Check for database setup
SEEDS_FOUND=false
MIGRATIONS_FOUND=false

# Django
if [ -d "*/migrations" ] || find . -type d -name "migrations" 2>/dev/null | grep -q .; then
    MIGRATIONS_FOUND=true
    echo "PASS: Database migrations exist"
fi

# Seeds/fixtures
SEED_LOCATIONS=(
    "seeds"
    "fixtures"
    "db/seeds"
    "data/seeds"
    "*/fixtures"
)

for loc in "${SEED_LOCATIONS[@]}"; do
    if [ -d "$loc" ] || find . -type d -name "$(basename $loc)" 2>/dev/null | grep -q .; then
        SEEDS_FOUND=true
        echo "PASS: Database seeds found in $loc"
        break
    fi
done

# Check for seed script in Makefile or package.json
if grep -q "seed" Makefile 2>/dev/null; then
    SEEDS_FOUND=true
    echo "PASS: Seed command in Makefile"
fi

if grep -q '"seed"' package.json 2>/dev/null; then
    SEEDS_FOUND=true
    echo "PASS: Seed script in package.json"
fi

if [ "$SEEDS_FOUND" = false ]; then
    echo "WARN: No database seeds found"
    echo "  Create seeds in: seeds/ or fixtures/"
fi
```

### SETUP-05: Docker Configuration

```bash
if [ -f "Dockerfile" ] || [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
    echo "PASS: Docker configuration exists"
    [ -f "Dockerfile" ] && echo "  Dockerfile"
    [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ] && echo "  docker-compose"
    [ -f ".dockerignore" ] && echo "  .dockerignore"
else
    echo "INFO: No Docker configuration"
fi
```

### SETUP-06: CI/CD Configuration

```bash
CI_FOUND=false

# GitHub Actions
if [ -d ".github/workflows" ]; then
    CI_FOUND=true
    echo "PASS: GitHub Actions configured"
    ls .github/workflows/
fi

# GitLab CI
if [ -f ".gitlab-ci.yml" ]; then
    CI_FOUND=true
    echo "PASS: GitLab CI configured"
fi

# CircleCI
if [ -f ".circleci/config.yml" ]; then
    CI_FOUND=true
    echo "PASS: CircleCI configured"
fi

# Travis CI
if [ -f ".travis.yml" ]; then
    CI_FOUND=true
    echo "PASS: Travis CI configured"
fi

if [ "$CI_FOUND" = false ]; then
    echo "INFO: No CI/CD configuration found"
fi
```

### SETUP-07: Git Hooks (pre-commit)

```bash
if [ -f ".pre-commit-config.yaml" ]; then
    echo "PASS: pre-commit configured"
elif [ -d ".husky" ]; then
    echo "PASS: Husky hooks configured"
elif [ -f ".git/hooks/pre-commit" ]; then
    echo "PASS: Git pre-commit hook exists"
else
    echo "INFO: No pre-commit hooks configured"
fi
```

### SETUP-08: EditorConfig / Code Formatting

```bash
FORMAT_FOUND=false

if [ -f ".editorconfig" ]; then
    FORMAT_FOUND=true
    echo "PASS: .editorconfig exists"
fi

if [ -f ".prettierrc" ] || [ -f ".prettierrc.json" ] || [ -f "prettier.config.js" ]; then
    FORMAT_FOUND=true
    echo "PASS: Prettier configured"
fi

if [ -f "pyproject.toml" ] && grep -q "\[tool.black\]" pyproject.toml; then
    FORMAT_FOUND=true
    echo "PASS: Black configured"
fi

if [ -f ".eslintrc" ] || [ -f ".eslintrc.json" ] || [ -f "eslint.config.js" ]; then
    FORMAT_FOUND=true
    echo "PASS: ESLint configured"
fi

if [ "$FORMAT_FOUND" = false ]; then
    echo "INFO: No code formatting configuration"
fi
```

---

## Generate Report

### Report Template

```markdown
# Brownfield Audit Report

**Project**: {project_name}
**Path**: {target_path}
**Date**: {timestamp}
**Project Types**: {detected_types}

## Executive Summary

| Section | Passed | Total | Status | Severity Issues |
|---------|--------|-------|--------|-----------------|
| Dependencies | {X} | 6 | {status} | {critical_count} critical |
| Security | {X} | 5 | {status} | {critical_count} critical |
| Secrets | {X} | 4 | {status} | {critical_count} critical |
| Documentation | {X} | 7 | {status} | {critical_count} critical |
| Setup | {X} | 8 | {status} | {critical_count} critical |
| **TOTAL** | **{X}** | **30** | **{overall}** | |

## Critical Issues (Must Fix)

{List critical severity issues}

## High Priority Issues

{List high severity issues}

## Recommendations

### Immediate Actions
1. {action_1}
2. {action_2}
3. {action_3}

### Quick Wins
1. {quick_fix_1}
2. {quick_fix_2}

## Detailed Results

### Dependencies
{detailed_deps_results}

### Security
{detailed_security_results}

### Secrets
{detailed_secrets_results}

### Documentation
{detailed_docs_results}

### Setup
{detailed_setup_results}

## Fix Templates

### Missing Makefile
```makefile
.PHONY: setup run test lint clean build

setup:
	pip install -r requirements.txt

run:
	python main.py

test:
	pytest

lint:
	ruff check .

clean:
	rm -rf __pycache__ .pytest_cache *.pyc

build:
	python -m build
```

### Missing example.env
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Keys
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# External Services
AWS_ACCESS_KEY_ID=your_aws_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_here
```

### Missing .gitignore entries
```gitignore
# Environment
.env
.env.local
.env.*.local

# Secrets
*.pem
*.key
credentials.json
secrets.json

# Python
__pycache__/
*.pyc
.venv/
venv/

# Node
node_modules/
```

---

## Scoring

**Grade Calculation:**
- **A**: 27-30 checks pass (90%+), 0 critical issues
- **B**: 24-26 checks pass (80-89%), 0 critical issues
- **C**: 18-23 checks pass (60-79%), max 1 critical
- **D**: 12-17 checks pass (40-59%)
- **F**: <12 checks pass, or 2+ critical issues
```

---

## Auto-Fix Mode

When `--fix` is specified, attempt these automatic fixes:

| Issue | Auto-Fix Action |
|-------|-----------------|
| Missing .gitignore entries | Append missing patterns |
| Missing example.env | Create from .env (sanitize values) |
| Unpinned Python deps | Run pip freeze |
| Missing Makefile targets | Add minimal targets |
| Missing LICENSE | Prompt to select license |

### Auto-Fix Example

```bash
if [ "$AUTO_FIX" = true ]; then
    # Fix 1: Create example.env from .env
    if [ -f ".env" ] && [ ! -f "example.env" ]; then
        sed 's/=.*/=your_value_here/' .env > example.env
        echo "FIXED: Created example.env"
    fi

    # Fix 2: Add missing .gitignore entries
    GITIGNORE_ADDITIONS=""
    for pattern in ".env" "*.pem" "*.key"; do
        if ! grep -qF "$pattern" .gitignore 2>/dev/null; then
            GITIGNORE_ADDITIONS="${GITIGNORE_ADDITIONS}\n${pattern}"
        fi
    done
    if [ -n "$GITIGNORE_ADDITIONS" ]; then
        echo -e "$GITIGNORE_ADDITIONS" >> .gitignore
        echo "FIXED: Added patterns to .gitignore"
    fi

    # Fix 3: Pin Python requirements
    if [ -f "requirements.txt" ]; then
        UNPINNED=$(grep -vE "==" requirements.txt | grep -v "^#" | grep -v "^$")
        if [ -n "$UNPINNED" ]; then
            pip freeze > requirements.txt.new
            echo "FIXED: Pinned requirements (review requirements.txt.new)"
        fi
    fi
fi
```

---

## Integration

### Run After Cloning Legacy Project

```bash
# First steps with brownfield codebase
/brownfield-audit ./path/to/project
```

### Scheduled Maintenance

```bash
# Monthly maintenance check
/brownfield-audit --sections=deps,security --severity=critical
```

### Pre-Release Checklist

```bash
# Before major release
/brownfield-audit --report
```

---

## Related Commands

- `/website-qa-checklist` - QA for web applications
- `/qa-microsite` - Branding/copyright checks
- `/check-core` - Core infrastructure changes

---

## Notes

- Always run in target project directory or specify path
- Security scan may take longer on large git histories
- Some checks require external tools (gitleaks, pip-audit)
- Use `--fix` with caution on production codebases
- Review all fixes before committing
