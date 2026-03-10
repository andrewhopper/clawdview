# UAT Validation Framework

**Location:** `projects/unspecified/active/tool-uat-validation-framework-a4idz/`

**Purpose:** QA validation for assets. Auto-loads tests from YAML (declarative) and Python (complex logic).

## Usage

```bash
cd projects/unspecified/active/tool-uat-validation-framework-a4idz
./bin/run --list                    # List all tests
./bin/run file.html                 # Run all tests
./bin/run -c web file.html          # Web tests only
./bin/run -c code file.py           # Code tests only
./bin/run -c structure file.py      # Structure tests only
./bin/run --json file.html          # JSON output
```

## Test Categories

| Category | Tests | Focus |
|----------|-------|-------|
| **web/** | 11 | Git hash, analytics, responsive, shadcn, React/Vite, color scheme |
| **code/** | 6 | Hardcoded paths/URLs, API keys, TODO/FIXME, debug code, TypeScript |
| **python/** | 3 | uv vs pip, pyproject.toml, type hints |
| **structure/** | 3 | .project files, run scripts, cruft detection |

## Adding Tests

- **YAML rules:** Drop `rules.yaml` in `validation_tests/<category>/`
- **Python tests:** Drop `.py` with `validate()` function in `validation_tests/<category>/`

## YAML Rule Format

```yaml
rules:
  - id: my-rule
    name: My Rule Name
    type: content_match  # or content_absence
    patterns:
      - regex: "pattern-to-find"
    match_any: true      # Pass if ANY pattern matches
    file_types: [".html", ".js"]
    severity: warning    # or error
```

## Python Test Format

```python
TEST_ID = "my-test"
TEST_NAME = "My Test Name"
TEST_SEVERITY = "warning"
TEST_FILE_TYPES = [".py"]

def validate(content: str, file_path: str, context: dict) -> dict:
    return {"passed": True, "message": "OK", "details": []}
```
