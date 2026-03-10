# Brownfield Codebase Maintenance Checklist

**Purpose:** Comprehensive checklist for auditing and maintaining legacy/brownfield codebases.

**Last Updated:** 2025-12-05

---

## 1.0 Quick Reference

### 1.1 Critical Checks (Must Pass)

| # | Check | Command/Tool |
|---|-------|-------------|
| 1 | No secrets in git history | `gitleaks detect` or `/brownfield-audit --sections=secrets` |
| 2 | No critical CVEs | `pip-audit` or `npm audit` |
| 3 | README.md exists | `ls README.md` |
| 4 | example.env exists | `ls example.env .env.example` |
| 5 | make setup works | `make setup` |
| 6 | make run works | `make run` |
| 7 | License defined | `ls LICENSE*` |

### 1.2 High Priority Checks

| # | Check | Command/Tool |
|---|-------|-------------|
| 8 | Dependencies pinned | Check requirements.txt/package-lock.json |
| 9 | make test works | `make test` |
| 10 | Author defined | Check package.json/pyproject.toml |
| 11 | .gitignore covers secrets | Check for .env, *.pem, *.key |
| 12 | No outdated major versions | `pip list --outdated` / `npm outdated` |

---

## 2.0 Detailed Checklist

### 2.1 Dependencies

- [ ] **DEP-01**: Check for outdated packages
- [ ] **DEP-02**: Lock files exist (requirements.txt with versions, package-lock.json)
- [ ] **DEP-03**: No deprecated packages (nose, pycrypto, etc.)
- [ ] **DEP-04**: No major version gaps (e.g., Django 3.x when 5.x available)
- [ ] **DEP-05**: No unused dependencies
- [ ] **DEP-06**: Python version specified (if Python project)

### 2.2 Security

- [ ] **SEC-01**: Vulnerability scan passed (pip-audit/npm audit)
- [ ] **SEC-02**: No hardcoded secrets in code
- [ ] **SEC-03**: No dangerous function usage (eval, exec, innerHTML)
- [ ] **SEC-04**: Security headers configured (if web app)
- [ ] **SEC-05**: No SQL injection vulnerabilities

### 2.3 Secrets in Git History

- [ ] **SECRET-01**: No AWS keys in history (AKIA pattern)
- [ ] **SECRET-02**: No private keys in history (-----BEGIN)
- [ ] **SECRET-03**: No database URLs with credentials
- [ ] **SECRET-04**: Sensitive files not tracked (.env, *.pem, *.key)

### 2.4 Documentation

- [ ] **DOC-01**: README.md exists with:
  - [ ] Project title
  - [ ] Description
  - [ ] Setup instructions
  - [ ] Usage examples
- [ ] **DOC-02**: LICENSE file exists
- [ ] **DOC-03**: Author information defined
- [ ] **DOC-04**: CONTRIBUTING.md (for OSS projects)
- [ ] **DOC-05**: CHANGELOG.md exists
- [ ] **DOC-06**: API documentation (if applicable)
- [ ] **DOC-07**: Code comments/docstrings present

### 2.5 Project Setup

- [ ] **SETUP-01**: Makefile with standard targets:
  - [ ] `make setup` - Initial setup
  - [ ] `make run` - Run application
  - [ ] `make test` - Run tests
  - [ ] `make lint` - Run linters
  - [ ] `make clean` - Clean artifacts
  - [ ] `make build` - Production build
- [ ] **SETUP-02**: example.env or .env.example exists
- [ ] **SETUP-03**: requirements.txt (Python) with pinned versions
- [ ] **SETUP-04**: Database seeds/fixtures exist
- [ ] **SETUP-05**: Docker configuration (optional)
- [ ] **SETUP-06**: CI/CD configuration (GitHub Actions, etc.)
- [ ] **SETUP-07**: Pre-commit hooks configured
- [ ] **SETUP-08**: Code formatting configured (.editorconfig, prettier, etc.)

---

## 3.0 Tool Installation

### 3.1 Security Scanning Tools

```bash
# Python vulnerability scanning
pip install pip-audit

# Git secrets scanning
brew install gitleaks
# or
pip install trufflehog

# General security scanning
pip install bandit  # Python
npm install -g snyk  # Node.js
```

### 3.2 Dependency Tools

```bash
# Python
pip install pip-tools  # pip-compile for requirements
pip install pipreqs    # Find actually used packages

# Node.js
npm install -g npm-check-updates  # ncu

# Rust
cargo install cargo-outdated cargo-audit
```

---

## 4.0 Templates

### 4.1 Makefile Template

```makefile
.PHONY: setup run test lint clean build help

# Default target
.DEFAULT_GOAL := help

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup:  ## Initial project setup
	pip install -r requirements.txt
	cp example.env .env || true
	@echo "Edit .env with your configuration"

run:  ## Run the application
	python main.py

test:  ## Run tests
	pytest -v

lint:  ## Run linters
	ruff check .
	mypy .

clean:  ## Clean build artifacts
	rm -rf __pycache__ .pytest_cache *.pyc .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

build:  ## Build for production
	python -m build

seed:  ## Seed the database
	python scripts/seed.py
```

### 4.2 example.env Template

```bash
# Application
APP_NAME=my-app
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# External Services
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# AWS (if needed)
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1

# Third-party APIs
OPENAI_API_KEY=your_openai_key_here
```

### 4.3 .gitignore Template

```gitignore
# Environment files
.env
.env.local
.env.*.local
!example.env
!.env.example

# Secrets
*.pem
*.key
*.p12
credentials.json
secrets.json
service-account*.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
ENV/
.pytest_cache/
.mypy_cache/
*.egg-info/
dist/
build/

# Node.js
node_modules/
npm-debug.log
yarn-error.log

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Testing
coverage/
.coverage
htmlcov/

# Build
dist/
build/
*.egg-info/
```

---

## 5.0 Common Fixes

### 5.1 Removing Secrets from Git History

```bash
# Using git filter-repo (recommended)
pip install git-filter-repo
git filter-repo --invert-paths --path secrets.json

# Or using BFG
brew install bfg
bfg --delete-files secrets.json
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (destructive!)
git push origin --force --all
```

### 5.2 Pinning Dependencies

```bash
# Python
pip freeze > requirements.txt

# Or with pip-tools
pip install pip-tools
pip-compile requirements.in > requirements.txt

# Node.js
npm install --package-lock-only
```

### 5.3 Adding License

```bash
# MIT License (common choice)
curl -o LICENSE https://raw.githubusercontent.com/licenses/license-templates/master/templates/mit.txt
# Edit to add your name and year
```

---

## 6.0 Automation

### 6.1 Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key
      - id: detect-aws-credentials

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
      - id: ruff-format
```

### 6.2 GitHub Actions Workflow

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pip-audit
          pip install -r requirements.txt

      - name: Vulnerability scan
        run: pip-audit
```

---

## 7.0 Related

- **Slash Command:** `/brownfield-audit`
- **Standards:** `hmode/shared/standards/code/`
- **Templates:** `shared/goldenrepos/`

---

## 8.0 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial checklist |
