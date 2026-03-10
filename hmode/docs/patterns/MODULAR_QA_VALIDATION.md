# MODULAR QA VALIDATION PATTERN

**Pattern:** Natural language quality checks using curl/grep/filesystem tools

**When to use:**
- Fast technical validation during development
- CI/CD integration without browser overhead
- Pre-commit hooks for quick quality gates
- Complementing Playwright with infrastructure checks
- Command-line quality verification

**When NOT to use:**
- Visual/UI validation (use Playwright instead)
- User flow testing (use Playwright E2E tests)
- Accessibility audits (use Playwright with axe-core)
- Cross-browser testing (use Playwright)

---

## 1.0 Overview

Modular QA validator accepts natural language queries and maps them to technical verification steps using curl, grep, and filesystem tools. Provides fast, lightweight quality checks without browser automation overhead.

```
┌─────────────────────────────────────────────────┐
│         Natural Language Input                  │
│  "CSS working", "Fonts loaded", "All checks"    │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│           Fuzzy Matcher                         │
│  Maps input → registered check function         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│        Check Method (Technical)                 │
│  curl, grep, filesystem, subprocess             │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│         CheckResult (Structured)                │
│  passed: bool, message: str, details: str       │
└─────────────────────────────────────────────────┘
```

---

## 2.0 Core Components

### 2.1 QA Validator Class

```python
class QAValidator:
    """Modular validator supporting natural language checks"""

    def __init__(self, base_url: str = "http://localhost:5173"):
        self.base_url = base_url
        self.checks: Dict[str, callable] = {
            "css working": self.check_css_working,
            "javascript loading": self.check_javascript_loading,
            "fonts loaded": self.check_fonts_loaded,
            "color scheme": self.check_color_scheme,
            "dev server running": self.check_dev_server,
            # ... 18 total checks
        }

    def run_check(self, check_name: str) -> CheckResult:
        """Run quality check by natural language name"""
        # Fuzzy match natural language → check function
        # Execute check, return structured result
```

### 2.2 Check Result Dataclass

```python
@dataclass
class CheckResult:
    """Result of a quality check"""
    passed: bool        # Did check pass?
    message: str        # Human-readable result
    details: str = ""   # Technical details
```

### 2.3 Check Methods

Each check method:
1. Uses appropriate tool (curl, grep, filesystem)
2. Validates expected behavior
3. Returns structured CheckResult

**Example: CSS Working**
```python
def check_css_working(self) -> CheckResult:
    # curl CSS file
    result = subprocess.run(["curl", "-s", f"{self.base_url}/src/index.css"], ...)
    css_content = result.stdout

    # Check for raw Tailwind directives (BAD)
    if "@tailwind" in css_content and "bg-gray-900" not in css_content:
        return CheckResult(passed=False, message="❌ CSS not compiling")

    # Check for compiled classes (GOOD)
    if "bg-gray-900" in css_content:
        return CheckResult(passed=True, message="✅ CSS working")
```

---

## 3.0 Built-in Checks

| Category | Checks | Method |
|----------|--------|--------|
| **CSS** | CSS working/loaded/compiling | curl CSS file, grep for compiled classes |
| **JavaScript** | JavaScript loading/working, JS loading | curl HTML, check for script tags |
| **Assets** | Assets load, Tailwind working | curl assets, check HTTP status |
| **Server** | Dev server running, Page loads | curl with timeout, check HTTP 200 |
| **Design** | Color scheme, Fonts loaded, Typography | grep CSS for colors/fonts |
| **Forms** | Forms validate | grep source for validation attributes |
| **Responsive** | Responsive | grep for breakpoint classes (sm:/md:/lg:) |
| **Quality** | No errors | grep build output for error strings |

**Total:** 18 checks with natural language aliases

---

## 4.0 Usage Patterns

### 4.1 Development Workflow

```bash
# Quick dev check
python qa-validator.py "CSS working"

# Before commit
python qa-validator.py "All checks"

# Specific concern
python qa-validator.py "Fonts loaded"
python qa-validator.py "Color scheme"
```

### 4.2 CI/CD Integration

```yaml
# GitHub Actions
- name: Run QA Checks
  run: python qa-validator.py "All checks"
```

### 4.3 Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
python qa-validator.py "CSS working" || exit 1
python qa-validator.py "JavaScript loading" || exit 1
```

### 4.4 Package.json Scripts

```json
{
  "scripts": {
    "qa": "python qa-validator.py 'All checks'",
    "qa:css": "python qa-validator.py 'CSS working'",
    "qa:js": "python qa-validator.py 'JavaScript loading'",
    "qa:design": "python qa-validator.py 'Color scheme' && python qa-validator.py 'Fonts loaded'"
  }
}
```

---

## 5.0 Extension Pattern

### 5.1 Adding New Check

**Step 1: Define check method**
```python
def check_new_feature(self) -> CheckResult:
    """Verify new feature works"""
    try:
        # Your verification logic
        result = subprocess.run([...])

        if verification_passes:
            return CheckResult(passed=True, message="✅ Feature working")
        else:
            return CheckResult(passed=False, message="❌ Feature broken")
    except Exception as e:
        return CheckResult(passed=False, message="❌ Check failed", details=str(e))
```

**Step 2: Register aliases**
```python
self.checks = {
    # ... existing checks ...
    "new feature": self.check_new_feature,
    "new feature working": self.check_new_feature,
    "feature ok": self.check_new_feature,
}
```

**Step 3: Use it**
```bash
python qa-validator.py "new feature"
```

### 5.2 Project-Specific Checks

Create `qa-validator-custom.py`:
```python
from qa_validator import QAValidator, CheckResult

class CustomQAValidator(QAValidator):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        # Add custom checks
        self.checks["api responding"] = self.check_api_responding
        self.checks["database seeded"] = self.check_database_seeded

    def check_api_responding(self) -> CheckResult:
        # Custom API check
        ...
```

---

## 6.0 Integration with Phase 8.5

**Playwright (Browser) + QA Validator (CLI) = Comprehensive Validation**

```
Phase 8.5: Quality Validation
├── 1. CLI Validation (qa-validator.py)
│   ├── Fast technical checks
│   ├── CSS/JS/assets/fonts/colors
│   └── No browser required
│
├── 2. Playwright Validation
│   ├── Visual validation
│   ├── User flow testing
│   └── Accessibility audit
│
└── 3. Validation Report
    ├── CLI results (section 2.0)
    └── Playwright results (sections 3.0-5.0)
```

**Execution order:**
1. Run CLI validation first (fast, catches infrastructure issues)
2. If CLI passes → Run Playwright (slower, validates UI/UX)
3. Generate combined report

---

## 7.0 Real-World Example

**Moto Hub Prototype** (proto-moto-hub-531b-069-moto-hub):

**Problem:** CSS not loading in browser (PostCSS config missing)

**Investigation using QA validator:**
```bash
$ python qa-validator.py "CSS working"
❌ CSS not compiling - Tailwind directives not processed
↳ Found @tailwind directives but no compiled classes. Missing postcss.config.js?

$ python qa-validator.py "Tailwind working"
❌ Tailwind not configured - Missing postcss.config.js
↳ Create postcss.config.js with tailwindcss plugin
```

**Fix:** Created `postcss.config.js`, restarted dev server

**Verification:**
```bash
$ python qa-validator.py "CSS working"
✅ CSS working - Found 8 Tailwind color variants
↳ Classes found: bg-gray-, text-gray-, bg-blue-, text-blue-, bg-red-...

$ python qa-validator.py "All checks"
============================================================
Results: 16/18 checks passed (89%)
============================================================
```

**Benefits:**
- Caught issue immediately with natural language query
- Diagnosed root cause (missing PostCSS config)
- Verified fix without opening browser
- 10 seconds vs 2 minutes (Playwright startup time)

---

## 8.0 Comparison: QA Validator vs Playwright

| Aspect | QA Validator | Playwright |
|--------|--------------|------------|
| **Speed** | <1 second | 10-30 seconds (browser startup) |
| **Checks** | Technical (CSS, JS, assets, config) | Visual, UI, accessibility, user flows |
| **Tools** | curl, grep, filesystem | Browser automation |
| **Use case** | Fast dev checks, CI/CD, pre-commit | Comprehensive E2E, visual regression |
| **Dependencies** | Python, curl | Browser binaries (200MB+) |
| **When to use** | During development, quick validation | Before release, full testing |

**Both are complementary, not replacements**

---

## 9.0 Benefits

1. **Natural Language Interface** - Write "CSS working" not "curl | grep | awk"
2. **Fast Feedback** - Results in <1 second
3. **No Browser Overhead** - Runs anywhere with curl/grep
4. **Extensible** - Add new checks in minutes
5. **CI/CD Friendly** - Exit codes, structured output
6. **Developer Experience** - Ask questions, get answers
7. **Early Detection** - Catch infrastructure issues before visual testing

---

## 10.0 Enforcement

**Phase 8.5 Requirements:**
- CLI validation OPTIONAL but RECOMMENDED
- If used, results MUST be included in validation report (section 2.0)
- CLI validation SHOULD run before Playwright (fail fast)
- Custom checks SHOULD be added for project-specific requirements

**Best Practices:**
- Run "All checks" before committing
- Add project-specific checks to validator
- Include in CI/CD pipeline
- Use for quick dev feedback loops
- Complement (not replace) Playwright tests

---

## 11.0 Template Files

**Create in prototype:**
```
prototypes/proto-name-xxxxx-NNN/
├── qa-validator.py          # Modular validator (18 built-in checks)
├── QA_VALIDATOR_README.md   # Usage documentation
└── package.json             # Scripts: "qa", "qa:css", etc.
```

**See:** `prototypes/proto-moto-hub-531b-069-moto-hub/` for reference implementation

---

## 12.0 Philosophy

> "Quality checks should be as easy as asking a question"

Instead of remembering complex curl/grep commands, just ask:
- "CSS working?"
- "JavaScript loading?"
- "Fonts loaded?"

The validator translates natural language → technical verification → structured results.

**Code is fast, questions are faster.**
