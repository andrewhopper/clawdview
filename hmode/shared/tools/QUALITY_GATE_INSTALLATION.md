# Quality Gate Installation Summary

<!-- File UUID: d7c6b5a4-f3e2-1d0c-9b8a-7e6f5d4c3b2a -->

## ✅ Installation Complete

The unified quality gate has been successfully installed with all required tools.

---

## 📦 Installed Tools

| Tool | Version | Purpose | Installation Method |
|------|---------|---------|---------------------|
| **radon** | 6.0.1 | Cyclomatic complexity analysis (Python) | `uv pip install` |
| **pylint** | 4.0.5 | Code duplication detection (Python) | `uv pip install` |
| **madge** | 8.0.0 | Circular dependency detection (TypeScript/JS) | `npm install -g` |

---

## 🆕 New Files Created

| File | Purpose |
|------|---------|
| `shared/tools/unified-quality-gate.py` | Main quality gate script (combines all tools) |
| `shared/tools/QUALITY_GATE_GUIDE.md` | Comprehensive usage guide |
| `shared/tools/Makefile.quality-gate` | Makefile targets for easy access |
| `shared/tools/QUALITY_GATE_INSTALLATION.md` | This file |

---

## 🚀 Quick Start

### 1. Run on Current Project

```bash
cd /path/to/your/project
python ~/dev/lab/shared/tools/unified-quality-gate.py --project .
```

### 2. Add to Project Makefile

Add this line to your project's Makefile:
```makefile
include $(HOPPERLABS_ROOT)/shared/tools/Makefile.quality-gate
```

Then use convenient targets:
```bash
make quality-gate          # Standard checks
make quality-gate-quick    # Fast checks
make quality-gate-strict   # Strict mode (warnings = errors)
make quality-report        # Generate JSON report
```

### 3. Pre-Commit Hook (Optional)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
make quality-gate-quick
exit $?
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 📊 What Gets Checked

### 1. Software Quality Check (8 Dimensions)
- ❌ **Config abstraction** - No hardcoded IDs/paths/URLs
- ℹ️ **Shared model reuse** - Uses domain models
- ❌ **Code decomposition** - Files < 500 lines
- ❌ **Testing presence** - Test files exist
- ⚠️ **Type safety** - TypeScript, Python type hints
- ❌ **Security** - No insecure connections (ws://)
- ❌ **Design system** - No raw hex colors
- ⚠️ **Domain models** - Timestamps present

### 2. Cyclomatic Complexity (radon)
- ❌ **High complexity** - Functions > 10 complexity
- ⚠️ **Medium complexity** - Functions > 5 complexity

### 3. Circular Dependencies (madge)
- ❌ **Circular imports** - Any circular dependency detected

### 4. Code Duplication (pylint)
- ❌ **High duplication** - >5 duplicate blocks
- ⚠️ **Some duplication** - 1-5 duplicate blocks

---

## 🎯 Coverage Matrix

| Principle | Covered | Tool(s) |
|-----------|---------|---------|
| **Separation of Concerns** | ✅ | `software-quality-check`, `/evaluate-architecture` |
| **Modularity** | ✅ | File size limits, `/evaluate-architecture` |
| **DRY (Don't Repeat Yourself)** | ✅ | `pylint`, `/evaluate-architecture` |
| **Externalized Config** | ✅ | `software-quality-check` (config abstraction) |
| **Decoupling** | ✅ | `/evaluate-architecture` |
| **Testability** | ✅ | Test presence check, `/evaluate-architecture` |
| **Type Safety** | ✅ | `software-quality-check` |
| **Security** | ✅ | `software-quality-check` |
| **Cyclomatic Complexity** | ✅ | `radon` |
| **Circular Dependencies** | ✅ | `madge` |

---

## 🔧 Configuration

### Skip Specific Checks

```bash
# Skip slow checks for quick validation
python unified-quality-gate.py \
  --project . \
  --skip code-duplication cyclomatic-complexity

# Skip checks not applicable to your project
python unified-quality-gate.py \
  --project . \
  --skip circular-dependencies  # No TypeScript
```

### Adjust Thresholds

Edit `unified-quality-gate.py` to customize:

```python
# Cyclomatic complexity
if complexity > 10:  # High (change to 15 for looser threshold)
    high_complexity.append(...)

# Code duplication
if warnings > 5:  # Too many (change to 10)
    status = "fail"

# File size
if line_count > 500:  # Max (change to 1000)
    errors.append(...)
```

---

## 🔄 Integration Patterns

### GitHub Actions

```yaml
- name: Quality Gate
  run: make quality-gate-ci

- name: Upload Report
  uses: actions/upload-artifact@v3
  with:
    name: quality-report
    path: quality-report.json
```

### Pre-Deployment

```makefile
deploy: quality-gate-strict build
	@echo "Deploying..."
	# deployment commands
```

### Phase Transitions (SDLC)

```
Phase 7 (Tests) → make quality-gate → Phase 8 (Impl)
Phase 8 (Impl) → make quality-gate-strict → Phase 9 (Refine)
```

---

## 📖 Documentation

- **Full Guide**: `shared/tools/QUALITY_GATE_GUIDE.md`
- **Individual Tool**: `shared/tools/software-quality-check.py --help`
- **Architecture Eval**: `.claude/commands/evaluate-architecture.md`

---

## 🐛 Troubleshooting

### "radon not found"

The Python tools are installed via `uv` and need to be run with `uv run`:
```bash
uv run radon --version  # ✅ Works
radon --version         # ❌ Not in PATH
```

The unified script handles this automatically.

### "madge not found"

Install globally:
```bash
npm install -g madge
```

### Timeout Errors

For large projects, increase timeout in script:
```python
timeout=240  # Default is 120 seconds
```

---

## ✨ Next Steps

1. **Test on a project**:
   ```bash
   cd ~/dev/lab/projects/your-project
   make quality-gate
   ```

2. **Fix any errors** found

3. **Add to CI/CD**:
   - Copy GitHub Actions example from guide
   - Or add `make quality-gate-ci` to your pipeline

4. **Set up pre-commit hook** (optional but recommended)

5. **Run architecture evaluation** for deeper analysis:
   ```bash
   /evaluate-architecture . standard
   ```

---

## 📊 Example Output

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
⚠️  cyclomatic-complexity: PASS WITH WARNINGS (2 warnings)

────────────────────────────────────────────────────────────────────────────────
🔍 Running: Circular Dependencies
────────────────────────────────────────────────────────────────────────────────
✅ circular-dependencies: PASS

────────────────────────────────────────────────────────────────────────────────
🔍 Running: Code Duplication
────────────────────────────────────────────────────────────────────────────────
✅ code-duplication: PASS

================================================================================
  📊 QUALITY GATE REPORT
================================================================================

Overall Status: ⚠️  PASS WITH WARNINGS
Project: my-project
Mode: STANDARD
Duration: 32.5s

Checks Summary:
Check                          Status               Errors     Warnings
────────────────────────────────────────────────────────────────────────────────
Software Quality Check         ✅ PASS               0          0
Cyclomatic Complexity          ⚠️  WARNING          0          2
Circular Dependencies          ✅ PASS               0          0
Code Duplication               ✅ PASS               0          0

Total Errors:   0
Total Warnings: 2
Total Info:     0

⚠️  Quality gate PASSED with warnings - consider fixing
```

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-09 | Initial installation with radon, pylint, madge |

---

**Questions?** See `shared/tools/QUALITY_GATE_GUIDE.md` for detailed documentation.
