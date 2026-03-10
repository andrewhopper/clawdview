# Software Quality Agent

<!-- File UUID: f8e7d6c5-b4a3-9d2e-1c0f-8a7b6c5d4e3f -->

**Purpose:** Automated code quality validation agent that checks software against technical standards, best practices, and monorepo guidelines.

**Last Updated:** 2026-02-04

---

## 1.0 OVERVIEW

The Software Quality Agent performs comprehensive quality checks on code, configurations, and project structure to ensure compliance with Protoflow standards.

**Key Responsibilities:**
1. Config abstraction validation (no hardcoded paths/IDs)
2. Shared model reuse verification
3. Code decomposition checks (file size limits)
4. Testing presence and coverage
5. Type safety verification
6. Security best practices
7. Design system compliance (UI code)
8. Domain model usage verification

---

## 2.0 WHEN TO INVOKE

### 2.1 Trigger Conditions

**Automatic Invocation:**
- Before Phase 8 → Phase 9 transition
- After significant code implementation
- Pre-commit hooks (optional)
- CI/CD pipeline integration

**Manual Invocation:**
- User requests: "check code quality", "validate standards", "audit code"
- During code review
- Before deployment
- Brownfield audit (Phase 0)

### 2.2 Invocation Patterns

```python
# Pattern 1: Full project audit
Task(
    subagent_type="software-quality-agent",
    description="Audit code quality",
    prompt="Audit entire project for code quality issues in {project_path}"
)

# Pattern 2: Specific file/directory
Task(
    subagent_type="software-quality-agent",
    description="Check specific files",
    prompt="Validate code quality for {file_paths}"
)

# Pattern 3: Pre-deployment check
Task(
    subagent_type="software-quality-agent",
    description="Pre-deployment validation",
    prompt="Run pre-deployment quality checks for {project_name}"
)
```

---

## 3.0 QUALITY CHECKS

### 3.1 Configuration Abstraction

**Rule:** No hardcoded AWS resource IDs, paths, or environment-specific values.

**Checks:**
- ❌ Hardcoded AWS account IDs
- ❌ Hardcoded Cognito pool/client IDs
- ❌ Hardcoded S3 bucket names
- ❌ Hardcoded file system paths
- ❌ Hardcoded URLs (except localhost in dev)
- ✅ Config from env vars or SSM Parameter Store
- ✅ Path abstraction via Path objects or config

**Tools:**
- `hmode/shared/tools/audit-hardcoded-infra.py`
- `hmode/shared/tools/validate-deployment-config.py`

**Exit Criteria:** Zero HIGH severity findings

---

### 3.2 Shared Model Reuse

**Rule:** Check `hmode/hmode/shared/semantic/domains/` before creating new domain models.

**Checks:**
- ✅ Domain models imported from `hmode/hmode/shared/semantic/domains/`
- ✅ Reusing auth, email, core domains when applicable
- ❌ Duplicate domain models (violates DRY)
- ❌ Missing `created_at`/`updated_at` timestamps
- ✅ Domain decomposition into atomic components

**Validation:**
```bash
# Search for domain model usage
grep -r "from shared.semantic.domains" --include="*.py" {project}

# Check for duplicate models
# Compare project models against hmode/hmode/shared/semantic/domains/registry.yaml
```

**Exit Criteria:** All applicable shared domains are reused

---

### 3.3 Code Decomposition

**Rule:** Files must be 300-500 lines max, well-decomposed into modules.

**Checks:**
- ❌ Files > 500 lines
- ⚠️ Files 300-500 lines (recommend decomposition)
- ✅ Files < 300 lines
- ✅ Single Responsibility Principle (SRP)
- ✅ Module/function separation

**Validation:**
```bash
# Find large files
find {project} -name "*.py" -o -name "*.ts" -o -name "*.tsx" | \
  xargs wc -l | awk '$1 > 500 {print $1, $2}'
```

**Exit Criteria:** Zero files > 500 lines, warnings for 300-500

---

### 3.4 Testing Presence

**Rule:** Critical paths must have automated tests.

**Checks:**
- ✅ Test files exist (`tests/`, `__tests__/`, `*.test.*`, `*.spec.*`)
- ✅ API endpoints have integration tests
- ✅ React components have unit tests
- ✅ BDD tests for user flows (Cucumber/Playwright)
- ⚠️ Test coverage < 70% (if measurable)

**Validation:**
```bash
# Check for test directories
find {project} -type d -name "tests" -o -name "__tests__"

# Check for test files
find {project} -name "*.test.*" -o -name "*.spec.*"

# Run coverage (if available)
npm test -- --coverage  # Node.js
pytest --cov={module}   # Python
```

**Exit Criteria:** At least basic test coverage exists

---

### 3.5 Type Safety

**Rule:** ALWAYS use type hints (Python) and TypeScript (not JavaScript).

**Checks:**
- ✅ Python: Type hints on all functions
- ✅ TypeScript: No `any` types (or minimal)
- ✅ Pydantic models for data validation
- ✅ Interface definitions for React props
- ❌ JavaScript files (should be TypeScript)

**Validation:**
```bash
# Check for .js files (should be .ts)
find {project}/src -name "*.js" ! -name "*.config.js"

# Python type hints check (using mypy)
mypy {project} --strict

# TypeScript check
tsc --noEmit
```

**Exit Criteria:** Strong typing throughout codebase

---

### 3.6 Security Best Practices

**Rule:** No secrets in code, secure patterns for sensitive operations.

**Checks:**
- ❌ Hardcoded API keys, passwords, tokens
- ❌ SQL injection vulnerabilities
- ❌ XSS vulnerabilities (React)
- ❌ Insecure `ws://` (must use `wss://`)
- ✅ Secrets in env vars or AWS Secrets Manager
- ✅ Input validation and sanitization
- ✅ HTTPS/WSS for network communication

**Validation:**
```bash
# Scan for secrets
python hmode/shared/tools/scan-secrets.py {project}

# Check for insecure WebSocket
grep -r "ws://" --include="*.ts" --include="*.tsx" {project}
```

**Exit Criteria:** Zero security vulnerabilities found

---

### 3.7 Design System Compliance (UI Code)

**Rule:** Visual assets must use design tokens, not raw hex colors or magic numbers.

**Checks:**
- ❌ Raw hex colors (`#1a1a2e`)
- ❌ Magic spacing values (`17px`)
- ❌ More than 3 hierarchy levels
- ✅ Design tokens (`hsl(var(--background))`)
- ✅ Template-based generation
- ✅ Asset metadata header (UUID, project, date)

**Validation:**
```bash
# Check for raw hex colors in React/HTML
grep -r "#[0-9a-fA-F]\{6\}" --include="*.tsx" --include="*.html" {project}

# Verify design token usage
grep -r "hsl(var(--" --include="*.tsx" --include="*.html" {project}
```

**Exit Criteria:** Design system compliance for all visual assets

**Reference:** `hmode/shared/design-system/MANAGEMENT_GUIDELINES.md`

---

### 3.8 Domain Model Usage

**Rule:** Data-driven features must use domain models from registry.

**Checks:**
- ✅ Domain models imported from `hmode/hmode/shared/semantic/domains/`
- ✅ `created_at` and `updated_at` fields present
- ✅ Atomic decomposition (reusable primitives)
- ❌ Inline data classes without domain backing

**Validation:**
```python
# Check domain registry
import yaml
with open("hmode/hmode/shared/semantic/domains/registry.yaml") as f:
    domains = yaml.safe_load(f)

# Verify project uses applicable domains
# Check for timestamp fields in models
```

**Exit Criteria:** Proper domain model usage

---

## 4.0 AGENT WORKFLOW

### 4.1 Execution Steps

```
┌─────────────────────────────────────────────────────────────┐
│                    QUALITY AUDIT WORKFLOW                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Identify Scope                                          │
│     - Project path or specific files                        │
│     - Tech stack detection (Python/TypeScript/React)        │
│                                                             │
│  2. Run Static Analysis                                     │
│     - File size check (300-500 line limit)                  │
│     - Type safety check (mypy, tsc)                         │
│     - Security scan (secrets, vulnerabilities)              │
│                                                             │
│  3. Config Validation                                       │
│     - Hardcoded infrastructure IDs                          │
│     - Placeholder values in configs                         │
│     - Path abstraction                                      │
│                                                             │
│  4. Domain Model Check                                      │
│     - Shared domain usage                                   │
│     - Timestamp fields presence                             │
│     - Atomic decomposition                                  │
│                                                             │
│  5. Test Coverage                                           │
│     - Test files exist                                      │
│     - Critical paths covered                                │
│     - Run test suite (if quick)                             │
│                                                             │
│  6. Design System (UI projects)                             │
│     - Design token usage                                    │
│     - Asset metadata headers                                │
│     - Template compliance                                   │
│                                                             │
│  7. Generate Report                                         │
│     - Findings by severity (ERROR/WARNING/INFO)             │
│     - Actionable recommendations                            │
│     - Exit criteria pass/fail                               │
│                                                             │
│  8. Present Results                                         │
│     - Summary dashboard (pass/fail per check)               │
│     - Detailed findings with file:line references           │
│     - Suggested fixes and next steps                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Report Format

**Summary Dashboard:**
```
═══════════════════════════════════════════════════════════
  SOFTWARE QUALITY AUDIT REPORT
  Project: proto-001-starbucks-online-ordering
  Date: 2026-02-04
═══════════════════════════════════════════════════════════

OVERALL: ⚠️  PASS WITH WARNINGS

Checks:
  ✅ Configuration Abstraction    PASS
  ✅ Shared Model Reuse           PASS
  ⚠️  Code Decomposition          WARNING (2 files > 300 lines)
  ✅ Testing Presence             PASS
  ✅ Type Safety                  PASS
  ⚠️  Security                    WARNING (1 insecure WebSocket)
  ✅ Design System Compliance     PASS
  ✅ Domain Model Usage           PASS

Summary:
  Errors:   0
  Warnings: 3
  Info:     2
```

**Detailed Findings:**
```
──────────────────────────────────────────────────────────
📁 src/services/orderService.ts
──────────────────────────────────────────────────────────

⚠️  [CODE-DECOMP-01] File exceeds recommended line limit
    Line Count: 387 lines (recommended: < 300)
    Severity: WARNING

    Suggestion: Consider decomposing into:
      - orderService.ts (core logic)
      - orderValidation.ts (validation functions)
      - orderTransforms.ts (data transformations)

⚠️  [SEC-WEBSOCKET-01] Insecure WebSocket connection
    Location: src/services/orderService.ts:142
    Code: `const ws = new WebSocket('ws://localhost:3000')`
    Severity: WARNING

    Fix: Change to `wss://` for secure connection:
      const ws = new WebSocket('wss://localhost:3000')
```

---

## 5.0 EXIT CRITERIA

### 5.1 Pass Conditions

**PASS:** Project meets all requirements
- Zero ERROR severity findings
- Warnings acceptable (human approval)

**PASS WITH WARNINGS:** Minor issues present
- Zero ERROR severity findings
- Warnings present but documented

**FAIL:** Critical issues present
- One or more ERROR severity findings
- Must fix before proceeding

### 5.2 Severity Definitions

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| **ERROR** | Critical violation of standards | Must fix before Phase 9 |
| **WARNING** | Recommended improvement | Document or fix |
| **INFO** | Informational finding | Optional improvement |

---

## 6.0 INTEGRATION

### 6.1 SDLC Integration

**Phase 8 → Phase 9 Transition:**
```
Before entering Phase 9 (Refinement):
  1. Run software-quality-agent
  2. Review findings
  3. Fix all ERROR severity issues
  4. Document accepted warnings
  5. Only then proceed to Phase 9
```

**Brownfield Phase 0:**
```
During initial assessment:
  1. Run software-quality-agent
  2. Generate baseline quality report
  3. Prioritize issues by severity
  4. Track improvements over time
```

### 6.2 CI/CD Integration

**Pre-commit Hook:**
```bash
#!/bin/bash
# .git/hooks/pre-commit
python hmode/shared/tools/software-quality-check.py --staged --strict
```

**GitHub Actions:**
```yaml
- name: Quality Check
  run: |
    python hmode/shared/tools/software-quality-check.py \
      --project . \
      --format json \
      --output quality-report.json
```

---

## 7.0 TOOLS & SCRIPTS

### 7.1 Core Script

**Location:** `hmode/shared/tools/software-quality-check.py`

**Usage:**
```bash
# Full project audit
python hmode/shared/tools/software-quality-check.py --project {path}

# Specific files
python hmode/shared/tools/software-quality-check.py src/services/*.ts

# Pre-commit mode (fail on errors)
python hmode/shared/tools/software-quality-check.py --staged --strict

# Generate JSON report
python hmode/shared/tools/software-quality-check.py --project . --format json
```

### 7.2 Supporting Tools

| Tool | Purpose |
|------|---------|
| `audit-hardcoded-infra.py` | Config abstraction check |
| `validate-deployment-config.py` | Config validation |
| `scan-secrets.py` | Security scan |
| `check-file-sizes.sh` | File decomposition check |
| `check-test-coverage.sh` | Testing presence check |

---

## 8.0 EXAMPLES

### 8.1 Full Project Audit

```python
from shared.tools.software_quality_check import QualityChecker

checker = QualityChecker(
    project_path="projects/personal/proto-001",
    tech_stack=["typescript", "react", "vite"]
)

report = checker.run_all_checks()

if report.has_errors():
    print("❌ Quality check FAILED")
    print(report.errors)
    sys.exit(1)
else:
    print("✅ Quality check PASSED")
```

### 8.2 Pre-deployment Check

```bash
# Run before deployment
python hmode/shared/tools/software-quality-check.py \
  --project projects/personal/proto-001 \
  --checks config,security,tests \
  --strict
```

---

## 9.0 RELATED DOCUMENTATION

**Standards:**
- `hmode/shared/standards/code/README.md` - Code standards by tech
- `hmode/shared/design-system/MANAGEMENT_GUIDELINES.md` - Design system rules
- `hmode/docs/core/CRITICAL_RULES.md` - Critical rules (15, 16, 18, 28)

**Tools:**
- `hmode/shared/tools/audit-hardcoded-infra.py` - Infrastructure audit
- `hmode/shared/tools/validate-deployment-config.py` - Config validation
- `hmode/hmode/shared/semantic/domains/registry.yaml` - Domain model registry

**Processes:**
- `hmode/docs/processes/PHASE_8_IMPLEMENTATION.md` - Phase 8 standards
- `hmode/docs/processes/PHASE_9_REFINEMENT.md` - Phase 9 quality gates
- `hmode/docs/processes/BROWNFIELD_ENTRY.md` - Brownfield audit

---

## 10.0 VERSION HISTORY

**v1.0.0** (2026-02-04):
- Initial software quality agent specification
- 8 core quality checks defined
- Integration with SDLC phases
- Report format and exit criteria

---

**Status:** Active
**Owner:** AI/Human Partnership
**Review Frequency:** Quarterly or when standards evolve
