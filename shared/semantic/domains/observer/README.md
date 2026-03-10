# Observer Domain Model

Deterministic validation system for AI outputs - like ECC RAM for LLMs.

## Overview

The Observer domain provides a rule-based validation system that checks Claude outputs against deterministic rules using regex patterns and custom validators. Zero LLM inference required.

## Core Entities

### Rule
A deterministic validation rule with regex pattern or validator function.

| Field | Type | Description |
|-------|------|-------------|
| uuid | string | Unique identifier (UUID v4) |
| id | string | Short rule ID (e.g., DOC-001) |
| name | string | Human-readable rule name |
| description | string | What the rule checks for |
| version | SemanticVersion | Rule version (semver) |
| category | RuleCategory | Rule category |
| tags | string[] | Tags for filtering |
| severity | Severity | Violation severity |
| enforcement | EnforcementLevel | How to handle violations |
| enabled | boolean | Rule active state |
| pattern | string? | Regex that SHOULD match |
| anti_pattern | string? | Regex that should NOT match |
| validator_name | string? | Custom validator function name |
| asset_types | AssetType[] | Which asset types to check |
| file_patterns | string[] | Glob patterns for file matching |
| fix_hint | string | How to fix violations |

### Violation
A detected rule violation.

| Field | Type | Description |
|-------|------|-------------|
| rule_id | string | ID of violated rule |
| rule_name | string | Name of violated rule |
| severity | Severity | Violation severity |
| enforcement | EnforcementLevel | How violation is handled |
| file_path | string | File where violation occurred |
| line_number | int? | Line number of violation |
| context | string | Additional context |
| matched_text | string | Text that triggered violation |
| fix_hint | string | How to fix |

### CheckResult
Result of checking content against rules.

| Field | Type | Description |
|-------|------|-------------|
| violations | Violation[] | List of violations |
| rules_checked | int | Number of rules checked |
| rules_skipped | int | Number of rules skipped |
| blocked | boolean | Was execution blocked? |
| block_reason | string? | Why blocked |
| duration_ms | float | Check duration |

## Enums

### Severity
- `critical` - Must fix immediately
- `error` - Uncorrectable, blocks
- `warning` - Correctable, doesn't block
- `info` - Informational

### EnforcementLevel
- `block` - Log error, block execution
- `warn` - Log warning, don't block
- `allow` - Log only, never block

### RuleCategory
- `documentation`
- `code_quality`
- `security`
- `style`
- `architecture`
- `testing`
- `performance`
- `accessibility`
- `compliance`

### AssetType
- `markdown`
- `python`
- `typescript`
- `javascript`
- `json`
- `yaml`
- `any`

## Rule Definitions

Rules are defined in YAML files in `schema/rules/`:

```yaml
rules:
  - id: DOC-001
    name: Date Required
    description: Documentation must include a date
    category: documentation
    tags: [date, metadata, audit]
    validator_name: has_date_in_document
    severity: warning
    enforcement: warn
    fix_hint: "Add 'Last Updated: YYYY-MM-DD'"
    asset_types: [markdown]
```

## Usage

```python
from shared.observers import Observer, create_default_observer, quick_check

# Quick check
result = quick_check(content, "file.md")

# Full observer
observer = create_default_observer()
result = observer.check_file("document.md")

if result.blocked:
    print(f"Blocked: {result.block_reason}")
```

## Design Principles

1. **Zero LLM inference** - Pure regex/code validation
2. **Immediate feedback** - Real-time violation detection
3. **Observable** - Configurable logging levels
4. **Minimal cost** - Compiled regex, early exit optimization
5. **Data-driven** - Rules as YAML, validators as Python
