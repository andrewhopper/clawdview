# Unified Quality Gate Guide

<!-- File UUID: e8d7c6b5-a4f3-2e1d-0c9b-8a7e6f5d4c3b -->

## Overview

The unified quality gate combines multiple code quality tools into a single, comprehensive validation system.

## Tools Integrated

| Tool | What It Checks | Thresholds |
|------|----------------|------------|
| **software-quality-check** | Config abstraction, shared models, decomposition, tests, types, security, design system, domain models | 8 checks, errors fail gate |
| **radon** | Cyclomatic complexity | >10 = error, >5 = warning |
| **madge** | Circular dependencies (TypeScript/JavaScript) | Any circular = error |
| **pylint** | Code duplication (Python) | >5 blocks = error, >0 = warning |
| **evaluate-architecture** | Modularity, decoupling, DRY, testability | Optional, manual only |

---

## Quick Start

```bash
# Standard gate (all checks except architecture)
cd /path/to/project
python ~/dev/lab/shared/tools/unified-quality-gate.py --project .

# Pre-deployment (strict mode)
python ~/dev/lab/shared/tools/unified-quality-gate.py --project . --strict

# Quick check (skip slow checks)
python ~/dev/lab/shared/tools/unified-quality-gate.py --project . --skip code-duplication

# JSON report for CI/CD
python ~/dev/lab/shared/tools/unified-quality-gate.py \
  --project . \
  --format json \
  --output quality-report.json
```

---

## Usage Patterns

### 1. Pre-Commit Check (Fast)
```bash
# Skip slow checks, only essentials
python unified-quality-gate.py \
  --project . \
  --skip code-duplication cyclomatic-complexity
```

### 2. Pre-Deployment Check (Comprehensive)
```bash
# All checks, strict mode
python unified-quality-gate.py \
  --project . \
  --mode strict \
  --verbose
```

### 3. CI/CD Integration
```bash
# JSON output for parsing
python unified-quality-gate.py \
  --project . \
  --format json \
  --output quality-report.json

# Exit code: 0 = pass, 1 = fail
```

### 4. Architecture Deep Dive
```bash
# After passing automated checks, run manual architecture evaluation
python unified-quality-gate.py --project . --verbose

# Then manually run (requires Claude agent)
/evaluate-architecture . standard
```

---

## Exit Codes

| Code | Meaning | When |
|------|---------|------|
| **0** | PASS | All checks passed (or only warnings in non-strict mode) |
| **1** | FAIL | Critical issues found, or warnings in strict mode |
| **2** | ERROR | Tool execution failed |

---

## Output Format

### Text Output (Default)

```
================================================================================
  🛡️  UNIFIED QUALITY GATE
  Project: my-project
  Mode: STANDARD
================================================================================

────────────────────────────────────────────────────────────────────────────────
🔍 Running: Software Quality Check
────────────────────────────────────────────────────────────────────────────────
✅ software-quality-check: PASS

────────────────────────────────────────────────────────────────────────────────
🔍 Running: Cyclomatic Complexity
────────────────────────────────────────────────────────────────────────────────
⚠️  cyclomatic-complexity: PASS WITH WARNINGS (3 warnings)

────────────────────────────────────────────────────────────────────────────────
🔍 Running: Circular Dependencies
────────────────────────────────────────────────────────────────────────────────
✅ circular-dependencies: PASS

────────────────────────────────────────────────────────────────────────────────
🔍 Running: Code Duplication
────────────────────────────────────────────────────────────────────────────────
⚠️  code-duplication: PASS WITH WARNINGS (2 warnings)

================================================================================
  📊 QUALITY GATE REPORT
================================================================================

Overall Status: ⚠️  PASS WITH WARNINGS
Project: my-project
Mode: STANDARD
Duration: 45.3s

Checks Summary:
Check                          Status               Errors     Warnings
────────────────────────────────────────────────────────────────────────────────
Software Quality Check         ✅ PASS              0          0
Cyclomatic Complexity          ⚠️  WARNING          0          3
Circular Dependencies          ✅ PASS              0          0
Code Duplication               ⚠️  WARNING          0          2

Total Errors:   0
Total Warnings: 5
Total Info:     0

⚠️  Quality gate PASSED with warnings - consider fixing
```

### JSON Output (CI/CD)

```json
{
  "project": "/Users/andyhop/dev/lab/projects/my-project",
  "timestamp": "2026-03-09T14:30:00",
  "mode": "standard",
  "overall_status": "pass_with_warnings",
  "duration_seconds": 45.3,
  "summary": {
    "errors": 0,
    "warnings": 5,
    "info": 0
  },
  "checks": [
    {
      "name": "software-quality-check",
      "status": "pass",
      "errors": 0,
      "warnings": 0,
      "info": 0,
      "duration_seconds": 15.2,
      "message": null,
      "details": {}
    },
    {
      "name": "cyclomatic-complexity",
      "status": "warning",
      "errors": 0,
      "warnings": 3,
      "info": 0,
      "duration_seconds": 10.5,
      "message": "High complexity: 0, Medium: 3",
      "details": {
        "high_complexity": [],
        "medium_complexity": [
          ["src/server.py", "process_request", 7],
          ["src/filters.py", "apply_rules", 6],
          ["src/config.py", "load_config", 6]
        ]
      }
    }
  ]
}
```

---

## Configuration

### Skip Specific Checks

If your project doesn't have TypeScript:
```bash
python unified-quality-gate.py \
  --project . \
  --skip circular-dependencies
```

### Adjust Strict Mode

By default, warnings don't fail the gate. Enable strict mode for pre-deployment:
```bash
python unified-quality-gate.py --project . --strict
```

---

## Integration with SDLC

### Phase 7 → Phase 8 Transition
```
Phase 7 (Tests) → Quality Gate → Phase 8 (Implementation)
                      ↓
              Must PASS all checks
              (warnings OK)
```

### Phase 8 → Phase 9 Transition
```
Phase 8 (Implementation) → Quality Gate (strict) → Phase 9 (Refinement)
                               ↓
                       Must PASS with 0 warnings
```

### Pre-Deployment Gate
```
make build → Quality Gate (strict) → Deploy
                  ↓
          Exit code 0 required
```

---

## CI/CD Integration Examples

### GitHub Actions

```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate

on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install radon pylint
          npm install -g madge

      - name: Run Quality Gate
        run: |
          python shared/tools/unified-quality-gate.py \
            --project . \
            --format json \
            --output quality-report.json

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-report.json

      - name: Comment PR
        if: github.event_name == 'pull_request'
        run: |
          # Parse quality-report.json and post comment
          # (use GitHub CLI or API)
```

### Pre-Commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running quality gate..."
python shared/tools/unified-quality-gate.py \
  --project . \
  --skip code-duplication cyclomatic-complexity

if [ $? -ne 0 ]; then
  echo "❌ Quality gate failed. Fix issues before committing."
  exit 1
fi

echo "✅ Quality gate passed"
exit 0
```

### Makefile Target

```makefile
# Add to project Makefile
.PHONY: quality-gate
quality-gate:
	@echo "Running unified quality gate..."
	@python $(HOPPERLABS_ROOT)/shared/tools/unified-quality-gate.py \
		--project . \
		--mode standard

.PHONY: quality-gate-strict
quality-gate-strict:
	@echo "Running strict quality gate..."
	@python $(HOPPERLABS_ROOT)/shared/tools/unified-quality-gate.py \
		--project . \
		--strict

.PHONY: quality-report
quality-report:
	@echo "Generating quality report..."
	@python $(HOPPERLABS_ROOT)/shared/tools/unified-quality-gate.py \
		--project . \
		--format json \
		--output quality-report.json \
		--verbose
	@echo "Report saved to quality-report.json"
```

---

## Threshold Customization

To adjust thresholds, edit `unified-quality-gate.py`:

```python
# Cyclomatic complexity thresholds
if complexity > 10:  # High complexity
    high_complexity.append(...)
elif complexity > 5:  # Medium complexity
    medium_complexity.append(...)

# Code duplication thresholds
if warnings > 5:  # Too many duplicates
    status = "fail"
    errors = warnings
```

---

## Troubleshooting

### Tool Not Found

```bash
# Install missing tools
uv pip install radon pylint
npm install -g madge
```

### Timeout Errors

Increase timeout in `unified-quality-gate.py`:
```python
timeout=120  # Increase to 240 for large projects
```

### False Positives

Skip specific checks or files:
```bash
# Skip problematic checks
python unified-quality-gate.py --project . --skip code-duplication

# Or configure skip patterns in the script
```

---

## Related Tools

- `software-quality-check.py` - Individual quality checker
- `/evaluate-architecture` - Manual architecture evaluation (Claude skill)
- `PROJECT_HEALTH_REPORT.md` - Health monitoring template
- `shared/standards/code/` - Language-specific standards

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-09 | Initial unified quality gate with 5 tools |

---

**Next Steps:**
1. Run on your project: `python unified-quality-gate.py --project .`
2. Review findings and fix errors
3. Integrate into CI/CD pipeline
4. Add to Makefile for easy access
