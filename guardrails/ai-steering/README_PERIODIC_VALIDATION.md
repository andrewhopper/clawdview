# Periodic Guardrail Validation System

**Automated enforcement of guardrails every N turns during development**

## Overview

This system runs guardrail validation checks periodically (every N turns) to ensure:
- ✅ S3 publishing offered for publishable files
- ✅ Shared domain models used (not local types)
- ✅ S3 URLs in clickable markdown format
- ✅ Tech dependencies approved in guardrails

**Key Features:**
- Configurable frequency (every N turns)
- Auto-fix capabilities for common violations
- ESLint-style output formatting
- Git pre-commit integration
- JSON output for CI/CD

---

## Quick Start

### 1. Test the Validator

```bash
# Run validation manually
python3 .guardrails/ai-steering/validate_periodic.py

# Run with auto-fix
python3 .guardrails/ai-steering/validate_periodic.py --fix

# JSON output (for CI/CD)
python3 .guardrails/ai-steering/validate_periodic.py --json
```

### 2. Start Periodic Runner

```bash
# Increment turn counter (run after each AI response)
python3 .guardrails/ai-steering/periodic_runner.py increment

# Check if validation should run
python3 .guardrails/ai-steering/periodic_runner.py check

# Force run validation now
python3 .guardrails/ai-steering/periodic_runner.py run

# Check status
python3 .guardrails/ai-steering/periodic_runner.py status
```

### 3. Configure Frequency

Edit `.guardrails/ai-steering/validate_periodic_config.yaml`:

```yaml
frequency:
  turns: 5  # Run validation every 5 turns (change to your preference)
```

---

## How It Works

### Turn-Based Validation

```
Turn 1: User asks question → AI responds
Turn 2: User requests feature → AI implements
Turn 3: User asks for changes → AI modifies
Turn 4: User adds new feature → AI creates files
Turn 5: ⏰ VALIDATION RUNS (turn % 5 == 0)
  - Check S3 publishing
  - Check shared models
  - Check URL format
  - Check tech preferences
  - Output: Warnings/Errors
Turn 6: Continue development...
```

### State Management

State stored in `.guardrails/.validation_state.json`:
```json
{
  "turn_count": 5,
  "last_validation": "2025-11-24T10:30:00",
  "last_validation_result": {
    "violations": 3,
    "warnings": 2,
    "errors": 1
  },
  "total_validations": 10,
  "total_violations": 15
}
```

---

## Validators

### 1. S3 Publishing Validator

**Rule:** `microsite-prompt-s3-publish` (MUST)

**Checks:**
- New `.html`, `.pdf`, `.svg`, `.zip`, `.mp3`, `.mp4` files
- Looks for evidence of S3 publishing:
  - `.s3-skip` marker file
  - `.s3-published` marker file
  - Bookmark file in `/bookmarks/`
  - Git commit message mentioning S3 publish

**Output Example:**
```
prototypes/proto-cat-site-001/index.html
  ❌ :1    Publishable file created without S3 publish evidence
     💡 Run: python3 prototypes/proto-s3-publish-vayfd-023/s3_publish.py --yes prototypes/proto-cat-site-001/index.html
```

### 2. Shared Models Validator

**Rule:** `microsite-use-existing-domain-models` (MUST)

**Checks:**
- Local type definitions in `.ts` and `.py` files
- Compares against `shared/semantic/domains/registry.yaml`
- Flags types that exist in registry but defined locally

**Output Example:**
```
src/types/Cat.ts
  ❌ :12   Type 'Cat' defined locally but exists in shared domains
     💡 Import from shared: import { Cat } from '@domains/pet'
```

**Auto-Fix:** Can generate import statements automatically

### 3. URL Format Validator

**Rule:** `s3-url-clickable-format` (SHOULD)

**Checks:**
- Plain S3 URLs in `.md`, `.ts`, `.py` files
- Ensures URLs are in markdown link format `[text](url)`

**Output Example:**
```
README.md
  ⚠️  :45   Plain S3 URL found (not clickable markdown)
     💡 Change to: [View file](https://bucket.s3.us-east-1.amazonaws.com/file.html)
```

**Auto-Fix:** Can convert plain URLs to markdown format

### 4. Tech Preferences Validator

**Rule:** `tech-preferences-validation` (SHOULD)

**Checks:**
- Dependencies in `package.json` (JavaScript/TypeScript)
- Dependencies in `pyproject.toml` (Python)
- Compares against `.guardrails/tech-preferences/*.json`

**Output Example:**
```
package.json
  ⚠️  :15   Dependency 'some-unknown-lib' not in approved tech list
     💡 Check .guardrails/tech-preferences/ or request approval
```

---

## Configuration

### Validator Settings

`.guardrails/ai-steering/validate_periodic_config.yaml`:

```yaml
# Frequency
frequency:
  turns: 5              # Every 5 turns (recommended)

# Strictness
strictness:
  level: moderate       # relaxed | moderate | strict
  failOnErrors: true    # Block on errors
  failOnWarnings: false # Don't block on warnings

# Auto-fix
autoFix:
  enabled: true
  requireConfirmation: true
  allowedTypes:
    - url_not_clickable
    - shared_model_not_used

# Individual validators
validators:
  s3_publish:
    enabled: true
    severity: error     # off | warn | error

  shared_models:
    enabled: true
    severity: error
    autoFix: true

  url_format:
    enabled: true
    severity: warn
    autoFix: true

  tech_preferences:
    enabled: true
    severity: warn
```

---

## Integration

### Git Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run guardrail validation before commits

python3 .guardrails/ai-steering/validate_periodic.py

if [ $? -eq 2 ]; then
    echo "❌ Guardrail violations found - commit blocked"
    echo "Run with --fix to auto-fix or add .validation-skip marker"
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Claude Code Hook (Future)

When Claude Code supports hooks, add to `.claude/hooks/tool-result.sh`:

```bash
#!/bin/bash
# Run after each tool execution

python3 .guardrails/ai-steering/periodic_runner.py increment
```

### GitHub Actions CI/CD

`.github/workflows/guardrails.yml`:

```yaml
name: Guardrails Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Dependencies
        run: pip install pyyaml

      - name: Run Validation
        run: |
          python3 .guardrails/ai-steering/validate_periodic.py \
            --strict \
            --json > validation-results.json

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-results
          path: validation-results.json
```

---

## Usage Examples

### Example 1: Manual Check During Development

```bash
# After making changes
$ python3 .guardrails/ai-steering/validate_periodic.py

prototypes/proto-cat-lovers-site-001/index.html
  ❌ :1    Publishable file created without S3 publish evidence
     💡 Run: python3 prototypes/proto-s3-publish-vayfd-023/s3_publish.py --yes ...

src/types/Cat.ts
  ❌ :12   Type 'Cat' defined locally but exists in shared domains
     💡 Import from shared: import { Cat } from '@domains/pet'

======================================================================
✅ 45 files checked
⚠️  2 warnings
❌ 2 errors
```

### Example 2: Auto-Fix Violations

```bash
$ python3 .guardrails/ai-steering/validate_periodic.py --fix

🔧 Auto-fixed 1 violations

README.md
  ✅ Fixed: Plain S3 URL converted to markdown link

src/types/Cat.ts
  ⚠️  Cannot auto-fix: Type 'Cat' - manual import required

======================================================================
✅ 45 files checked
⚠️  1 warnings (manual fix required)
❌ 0 errors
```

### Example 3: Periodic Runner

```bash
# Turn 1-4: Development continues
$ python3 .guardrails/ai-steering/periodic_runner.py increment
Turn 1/5

$ python3 .guardrails/ai-steering/periodic_runner.py increment
Turn 2/5

# ...

# Turn 5: Validation runs
$ python3 .guardrails/ai-steering/periodic_runner.py increment
Turn 5/5
⏰ Validation due - running check...
🔍 Running guardrail validation...

[Validation output...]

✅ All guardrails validated successfully
```

### Example 4: Check Status

```bash
$ python3 .guardrails/ai-steering/periodic_runner.py status

Validation Status
==================================================
Turn count:        3/5
Last validation:   2025-11-24T10:30:00
Total validations: 12
Total violations:  25

Last Result:
  Violations: 2
  Warnings:   1
  Errors:     1
```

---

## Exemptions and Skip Markers

### Skip Validation for Specific Files

Create `.validation-skip` marker:
```bash
touch prototypes/proto-test-001/.validation-skip
```

### Skip S3 Publishing Check

Create `.s3-skip` marker:
```bash
touch prototypes/proto-cat-site-001/.s3-skip
```

### Skip in Configuration

Edit `validate_periodic_config.yaml`:
```yaml
exemptions:
  paths:
    - archive/
    - backup/

  patterns:
    - "*.backup.*"
    - "*.old.*"

  prototypes:
    - proto-test-*
```

---

## Troubleshooting

### Issue: Validation Not Running

**Check:**
```bash
python3 .guardrails/ai-steering/periodic_runner.py status
```

**Fix:**
```bash
python3 .guardrails/ai-steering/periodic_runner.py reset
```

### Issue: False Positives

**S3 Publish Check:**
- Add `.s3-skip` marker file
- Or create bookmark file in `/bookmarks/`

**Shared Models Check:**
- Ensure `shared/semantic/domains/registry.yaml` is up to date
- Or add exemption in config

### Issue: Auto-Fix Not Working

**Check permissions:**
```bash
ls -la .guardrails/ai-steering/validate_periodic.py
chmod +x .guardrails/ai-steering/validate_periodic.py
```

**Check configuration:**
```yaml
autoFix:
  enabled: true
  requireConfirmation: false  # Set to false for non-interactive
```

---

## Architecture

### File Structure

```
.guardrails/ai-steering/
├── validate_periodic.py          # Main validator script
├── periodic_runner.py             # Turn-based runner
├── validate_periodic_config.yaml  # Configuration
├── README_PERIODIC_VALIDATION.md  # This file
└── .validation_state.json         # State (auto-generated)
```

### Validator Classes

```python
BaseValidator
  ├── S3PublishValidator
  ├── SharedModelsValidator
  ├── URLFormatValidator
  └── TechPreferencesValidator

GuardrailValidator (orchestrator)
  ├── run_all()
  ├── auto_fix()
  └── format_output()
```

### State Flow

```
User Request → AI Response → Tool Execution
                ↓
        Increment Turn Counter
                ↓
        Turn % Frequency == 0?
        ├─ No → Continue
        └─ Yes → Run Validation
                    ├─ Load Rules
                    ├─ Run Validators
                    ├─ Collect Violations
                    ├─ Apply Auto-Fixes (if enabled)
                    ├─ Output Results
                    └─ Update State
```

---

## Performance

**Typical Validation Times:**
- Small repo (< 100 files): < 1 second
- Medium repo (100-1000 files): 1-3 seconds
- Large repo (> 1000 files): 3-10 seconds

**Optimization Tips:**
- Increase frequency (`turns: 10`) for large repos
- Disable validators you don't need
- Add more exemptions for irrelevant directories

---

## Extending with Custom Validators

### Create Custom Validator

```python
# .guardrails/ai-steering/validators/custom_validator.py

from validate_periodic import BaseValidator, Violation, ViolationType, Severity

class CustomValidator(BaseValidator):
    def validate(self) -> List[Violation]:
        violations = []

        # Your validation logic here
        for file in self.repo_root.rglob("*.custom"):
            if not self._is_valid(file):
                violations.append(Violation(
                    type=ViolationType.CUSTOM,
                    severity=Severity.ERROR,
                    message="Custom validation failed",
                    file_path=file
                ))

        return violations
```

### Register Validator

Add to `validate_periodic.py`:
```python
from validators.custom_validator import CustomValidator

class GuardrailValidator:
    def __init__(self, repo_root: Path):
        self.validators = [
            S3PublishValidator(repo_root),
            SharedModelsValidator(repo_root),
            URLFormatValidator(repo_root),
            TechPreferencesValidator(repo_root),
            CustomValidator(repo_root),  # Add here
        ]
```

---

## FAQ

**Q: How do I change validation frequency?**
A: Edit `.guardrails/ai-steering/validate_periodic_config.yaml` and change `frequency.turns`

**Q: Can I disable specific validators?**
A: Yes, set `enabled: false` in config for any validator

**Q: What happens if validation fails?**
A: Depends on `strictness.failOnErrors` config. If true, blocks commits/pushes. If false, logs warnings.

**Q: Can I run validation manually?**
A: Yes: `python3 .guardrails/ai-steering/validate_periodic.py`

**Q: How do I add exemptions?**
A: Add to `exemptions` section in config, or create `.validation-skip` marker files

---

## Next Steps

1. **Test the system:**
   ```bash
   python3 .guardrails/ai-steering/validate_periodic.py
   ```

2. **Adjust configuration:**
   - Set `frequency.turns` to your preference
   - Enable/disable validators
   - Configure auto-fix settings

3. **Integrate with workflow:**
   - Add to git pre-commit hook
   - Add to CI/CD pipeline
   - Create Claude Code hook (when available)

4. **Monitor violations:**
   ```bash
   python3 .guardrails/ai-steering/periodic_runner.py status
   ```

---

**Status:** ✅ Ready for testing
**Version:** 1.0.0
**Last Updated:** 2025-11-24
