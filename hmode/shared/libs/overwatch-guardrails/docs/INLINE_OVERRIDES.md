# Inline Override Syntax

<!-- File UUID: 7e8d9f2a-6c5b-4e3f-8a6d-9c7b5e4f3a2d -->

## 1.0 Overview

Inline overrides allow temporarily disabling specific guardrails in source files.

**Inspired by:** ESLint, Pylint, Clippy, Rust's `#[allow]`

## 2.0 Syntax

### 2.1 Python

```python
# guardrails: disable=unapproved-dependency
from create_react_app import Component  # Spike only

# guardrails: disable=raw-hex-colors
PRIMARY_COLOR = "#FF0000"  # TODO: Use design token in phase 8

# Multiple rules
# guardrails: disable=file-size-limit,missing-type-hints
def large_function():
    pass  # Legacy code, will refactor
```

### 2.2 TypeScript/JavaScript

```typescript
// guardrails: disable=unapproved-dependency
import angular from 'angular';  // Migrating from Angular

// guardrails: disable=raw-hex-colors
const color = "#1a1a2e";  // Hardcoded for demo
```

### 2.3 YAML

```yaml
# guardrails: disable=unapproved-aws-service
Resources:
  MyBucket:
    Type: AWS::S3::Bucket  # Using S3 for spike
```

## 3.0 Scope

### 3.1 Single Line (Next Line Only)

```python
# guardrails: disable-next-line=unapproved-dependency
from angular import Component
```

### 3.2 Block Scope

```python
# guardrails: disable=file-size-limit
# ... 1000 lines of legacy code ...
# guardrails: enable=file-size-limit
```

### 3.3 File Scope

```python
# File UUID: abc123
# guardrails: disable-file=all

# Entire file exempt (spike code, will be deleted)
```

## 4.0 Required Justification

For critical rules, require justification:

```python
# guardrails: disable=ws-protocol, reason="Local development only"
const ws = new WebSocket("ws://localhost:8080");
```

Configuration:

```yaml
rules:
  - id: ws-protocol
    mode: BLOCK
    require_justification_for_override: true
```

## 5.0 Expiration

Time-bound overrides:

```python
# guardrails: disable=unapproved-dependency, expires=2026-02-01
from angular import Component  # Remove after migration
```

After expiration, the override is invalid and violation triggers.

## 6.0 Parser API

```python
from overwatch_guardrails import InlineOverrideParser

parser = InlineOverrideParser()

# Parse file
overrides = parser.parse_file("src/app.py")

# Returns:
# [
#   {
#     "line": 5,
#     "rule_ids": ["unapproved-dependency"],
#     "scope": "next-line",  # or "block", "file"
#     "reason": "Spike only",
#     "expires": "2026-02-01"
#   }
# ]

# Check if rule is disabled at line
is_disabled = parser.is_rule_disabled(
    file_path="src/app.py",
    line_number=6,
    rule_id="unapproved-dependency"
)
```

## 7.0 Enforcement Integration

```python
def enforce_with_inline_overrides(file_path, line_number, rule_id, violation):
    parser = InlineOverrideParser()

    if parser.is_rule_disabled(file_path, line_number, rule_id):
        # Check if justification required
        override = parser.get_override(file_path, line_number, rule_id)

        if rule.require_justification_for_override and not override.reason:
            return EnforcementResult(
                allowed=False,
                mode=EnforcementMode.BLOCK,
                message="Justification required for override"
            )

        # Check expiration
        if override.expires and datetime.now() > override.expires:
            return EnforcementResult(
                allowed=False,
                mode=EnforcementMode.BLOCK,
                message=f"Override expired on {override.expires}"
            )

        # Override is valid
        return EnforcementResult(
            allowed=True,
            mode=EnforcementMode.LOG,
            message=f"Override: {override.reason}"
        )

    # No override, normal enforcement
    return enforcer.enforce(rule_id, violation, context)
```

## 8.0 Audit Trail

All inline overrides are logged:

```json
{
  "timestamp": "2026-01-15T15:30:00Z",
  "file": "src/app.py",
  "line": 5,
  "rule_id": "unapproved-dependency",
  "reason": "Spike only",
  "expires": "2026-02-01",
  "added_by": "andyhop"
}
```

## 9.0 Best Practices

1. **Always provide reason** - Explain why override is needed
2. **Set expiration** - Temporary overrides should expire
3. **Minimize scope** - Use `disable-next-line` over file-wide
4. **Review regularly** - Audit overrides in code reviews
5. **Track in issues** - Link to GitHub issue explaining override
