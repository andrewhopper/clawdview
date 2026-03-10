# API Design

<!-- File UUID: 9e4b7f2a-5c8d-4e3f-9a6b-8d7c4e5f3a2b -->

## 1.0 Core API

### 1.1 Main Enforcer Class

```python
from overwatch_guardrails import GuardrailEnforcer, EnforcementMode, Violation

# Initialize enforcer
enforcer = GuardrailEnforcer(config_path=".guardrails/enforcement-config.yaml")

# Check a violation
result = enforcer.enforce(
    rule_id="unapproved-dependency",
    violation=Violation(
        message="Package 'angular' not approved",
        file_path="package.json",
        alternatives=["Next.js", "Vite", "Expo"]
    ),
    context={"phase": "phase_8", "project_type": "prototype"}
)

# Handle result
if not result.allowed:
    if result.requires_approval:
        approved = prompt_user(result.message)
        if not approved:
            sys.exit(1)
    else:
        print(result.message)
        sys.exit(1)
```

### 1.2 Data Classes

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

class EnforcementMode(Enum):
    LOG = "log"
    WARN = "warn"
    APPROVAL_REQUIRED = "approval_required"
    BLOCK = "block"

@dataclass
class Violation:
    rule_id: str
    message: str
    file_path: Optional[str] = None
    alternatives: Optional[List[str]] = None
    autofix_available: bool = False
    severity: str = "unknown"  # rank_1, rank_2_3, rank_4_plus, not_listed

@dataclass
class EnforcementResult:
    allowed: bool
    mode: EnforcementMode
    message: str
    alternatives: Optional[List[str]] = None
    requires_approval: bool = False
    autofix_available: bool = False
    logged: bool = True
```

### 1.3 Tech Preference Validator

```python
from overwatch_guardrails import TechPreferenceValidator

validator = TechPreferenceValidator(prefs_dir=".guardrails/tech-preferences")

# Check a package
rank, all_options = validator.check_package("vite", category="frontend_frameworks")

if rank == 1:
    # Preferred, no action needed
    pass
elif rank in [2, 3]:
    # Allowed alternative, may warn
    preferred = validator.get_preferred_alternatives("frontend_frameworks", max_rank=1)
    print(f"Using rank {rank}. Preferred: {preferred[0]['name']}")
elif rank is None:
    # Not listed, needs approval
    print(f"Package not in approved list")
```

## 2.0 Configuration API

```python
from overwatch_guardrails import ConfigLoader, ConfigValidator

# Load configuration
loader = ConfigLoader()
config = loader.load(".guardrails/enforcement-config.yaml")

# Validate configuration
validator = ConfigValidator()
errors = validator.validate(config)
if errors:
    for error in errors:
        print(f"Config error: {error}")

# Get mode for rule with context
mode = loader.get_mode(
    rule_id="unapproved-dependency",
    context={"phase": "phase_8", "environment": "production"}
)
```

## 3.0 CLI Interface

```python
# Command-line usage
from overwatch_guardrails.cli import cli

if __name__ == "__main__":
    cli()
```

```bash
# Check file
guardrails check package.json

# Check all files
guardrails check-all

# Show violations
guardrails violations --mode BLOCK --today

# Set mode
guardrails set-mode --category security BLOCK

# Show config
guardrails config
```

## 4.0 Inline Override Support

```python
# In source files
# guardrails: disable=unapproved-dependency
from angular import Component

# guardrails: disable=raw-hex-colors
color = "#FF0000"  # Spike only, will fix in phase 8
```

Parser API:

```python
from overwatch_guardrails import InlineOverrideParser

parser = InlineOverrideParser()
overrides = parser.parse_file("src/app.py")

# Returns: [{"line": 5, "rule_id": "unapproved-dependency", "disabled": True}]
```

## 5.0 Full API Reference

See `docs/API_REFERENCE.md` for complete API documentation.
