# Quality Gate Documentation Index

<!-- File UUID: a4f3e2d1-c0b9-8a7e-6f5d-4c3b2a1f0e9d -->

Quick reference to all quality gate documentation.

---

## 🚀 Getting Started (Read First)

**Start here if you're new to the quality gate:**

1. **Installation Summary** - `QUALITY_GATE_INSTALLATION.md`
   - 5 minute read
   - What's installed, how to use it, quick examples

---

## 📚 Core Documentation

### For Users

| Document | Purpose | Read Time |
|----------|---------|-----------|
| `QUALITY_GATE_GUIDE.md` | Comprehensive usage guide | 15 min |
| `Makefile.quality-gate` | Makefile targets to copy | 2 min |
| `unified-quality-gate.py` | Main script (reference) | - |

### For Reference

| Document | Purpose |
|----------|---------|
| `../docs/QUALITY_GATE_DOCUMENTATION.md` | Complete system documentation (500+ lines) |
| `readme.md` | Tool ecosystem overview (includes quality gate section) |
| `../standards/README.md` | Standards and patterns overview |

---

## 📖 Documentation by Use Case

### I want to...

**Run the quality gate on my project**
→ See `QUALITY_GATE_INSTALLATION.md` (Quick Start section)

**Understand what checks are run**
→ See `QUALITY_GATE_GUIDE.md` (What It Checks section)

**Integrate with CI/CD**
→ See `QUALITY_GATE_GUIDE.md` (Integration Patterns section)

**Customize thresholds**
→ See `QUALITY_GATE_GUIDE.md` (Threshold Customization section)

**Add to my Makefile**
→ Copy from `Makefile.quality-gate`

**Understand the architecture**
→ See `../docs/QUALITY_GATE_DOCUMENTATION.md` (Architecture section)

**Troubleshoot issues**
→ See `QUALITY_GATE_GUIDE.md` (Troubleshooting section)

---

## 🔧 Tools & Scripts

| File | Purpose | Type |
|------|---------|------|
| `unified-quality-gate.py` | Main orchestrator | Python script |
| `software-quality-check.py` | Individual checker (8 dimensions) | Python script |
| `Makefile.quality-gate` | Reusable Makefile targets | Makefile |

---

## 📊 Supporting Documentation

| Document | Purpose |
|----------|---------|
| `.claude/commands/evaluate-architecture.md` | Manual architecture evaluation (optional) |
| `../standards/PROJECT_HEALTH_REPORT.md` | Health monitoring template |
| `../standards/testing/BDD_TESTING_GUIDE.md` | BDD testing with Cucumber |
| `../standards/testing/SMOKE_TEST_PATTERN.md` | Post-deployment smoke tests |

---

## 🎯 Quick Links by Topic

### Installation
- `QUALITY_GATE_INSTALLATION.md` - Installation summary
- `QUALITY_GATE_GUIDE.md` (Configuration section) - Tool setup

### Usage
- `QUALITY_GATE_GUIDE.md` (Quick Start section) - Basic usage
- `Makefile.quality-gate` - Makefile targets
- `unified-quality-gate.py --help` - CLI options

### Integration
- `QUALITY_GATE_GUIDE.md` (CI/CD Integration section) - GitHub Actions, pre-commit hooks
- `../docs/QUALITY_GATE_DOCUMENTATION.md` (SDLC Integration section) - Phase transitions

### Coverage
- `../docs/QUALITY_GATE_DOCUMENTATION.md` (Quality Dimensions section) - 10 dimensions
- `../docs/QUALITY_GATE_DOCUMENTATION.md` (Architecture Principles section) - Principle mapping
- `../standards/README.md` (Coverage Matrix) - Tool mapping

---

## 📁 File Locations

All quality gate files are in `shared/tools/`:

```
shared/tools/
├── unified-quality-gate.py           # Main script (677 lines)
├── software-quality-check.py         # Individual checker
├── QUALITY_GATE_GUIDE.md             # Usage guide (400+ lines)
├── QUALITY_GATE_INSTALLATION.md      # Installation summary (300+ lines)
├── QUALITY_GATE_INDEX.md             # This file
├── Makefile.quality-gate             # Makefile targets
└── readme.md                         # Tool ecosystem overview

../docs/
└── QUALITY_GATE_DOCUMENTATION.md     # Comprehensive reference (500+ lines)

../standards/
└── README.md                         # Standards overview (updated)
```

---

## 🔄 Documentation Updates

**Last Updated:** 2026-03-09
**Version:** 1.0.0

### Changelog

| Date | Document | Changes |
|------|----------|---------|
| 2026-03-09 | All | Initial creation and documentation |
| 2026-03-09 | `readme.md` | Added quality gate section |
| 2026-03-09 | `../standards/README.md` | Comprehensive rewrite |

---

## 💡 Recommended Reading Order

1. **First Time Setup:**
   1. `QUALITY_GATE_INSTALLATION.md` (5 min)
   2. `QUALITY_GATE_GUIDE.md` (15 min)
   3. Try it: `make quality-gate`

2. **Daily Use:**
   - Quick reference: `Makefile.quality-gate`
   - Troubleshooting: `QUALITY_GATE_GUIDE.md` (Troubleshooting section)

3. **Deep Dive:**
   - `../docs/QUALITY_GATE_DOCUMENTATION.md` (comprehensive reference)
   - `unified-quality-gate.py` (source code)

---

**Start here: `QUALITY_GATE_INSTALLATION.md`**
