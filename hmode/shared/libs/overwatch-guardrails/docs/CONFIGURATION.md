# Configuration Schema

<!-- File UUID: 4d7e9a2f-5b8c-4e1d-9f3a-7c6b8d4e2f5a -->

## 1.0 Configuration File Location

```
.guardrails/enforcement-config.yaml
```

## 2.0 Full Schema

```yaml
# Global default mode (LOG, WARN, APPROVAL_REQUIRED, BLOCK)
default_mode: WARN

# Per-category modes
categories:
  security:
    mode: BLOCK
    description: "Security violations are never allowed"

  tech_preferences:
    mode: APPROVAL_REQUIRED
    description: "Tech decisions require approval"
    suggest_alternatives: true
    log_approval_decision: true

  design_system:
    mode: WARN
    description: "Design system violations warned"
    autofix_available: true

  code_quality:
    mode: LOG
    description: "Quality metrics silently logged"

# Individual rules (override category)
rules:
  - id: never-ws-protocol
    category: security
    mode: BLOCK
    message: "Insecure ws:// protocol. Must use wss://"

  - id: unapproved-dependency
    category: tech_preferences
    mode: APPROVAL_REQUIRED
    message: "Package '{package}' not in approved list"
    show_alternatives: true
    require_justification: true

  - id: raw-hex-colors
    category: design_system
    mode: WARN
    message: "Raw hex {color}. Use token: {token}"
    autofix_available: true

# Strictness profiles for ranking
strictness_profiles:
  relaxed:
    rank_1: LOG
    rank_2_3: LOG
    rank_4_plus: WARN
    not_listed: WARN

  standard:
    rank_1: LOG
    rank_2_3: WARN
    rank_4_plus: WARN
    not_listed: APPROVAL_REQUIRED

  strict:
    rank_1: LOG
    rank_2_3: APPROVAL_REQUIRED
    rank_4_plus: BLOCK
    not_listed: BLOCK

# Context-based overrides
environments:
  spike:
    default_mode: LOG
    categories:
      security:
        mode: WARN

  production:
    default_mode: APPROVAL_REQUIRED
    categories:
      security:
        mode: BLOCK
      tech_preferences:
        mode: BLOCK

phases:
  phase_1_to_3:
    strictness: relaxed

  phase_8_to_9:
    strictness: standard

project_types:
  exploration:
    strictness: relaxed

  prototype:
    strictness: standard

  production:
    strictness: strict
```

## 3.0 Minimal Configuration

```yaml
# .guardrails/enforcement-config.yaml (minimal)

default_mode: WARN

categories:
  security:
    mode: BLOCK
  tech_preferences:
    mode: APPROVAL_REQUIRED
  code_quality:
    mode: LOG
```

## 4.0 Configuration Properties

### 4.1 Global Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `default_mode` | enum | WARN | Default enforcement mode |

### 4.2 Category Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `mode` | enum | - | Enforcement mode for category |
| `description` | string | - | Human-readable description |
| `suggest_alternatives` | bool | false | Show approved alternatives |
| `log_approval_decision` | bool | false | Log user's approval decision |
| `autofix_available` | bool | false | Can violations be auto-fixed |

### 4.3 Rule Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `id` | string | - | Unique rule identifier |
| `category` | string | - | Category this rule belongs to |
| `mode` | enum | - | Enforcement mode (overrides category) |
| `message` | string | - | User-facing message (supports {placeholders}) |
| `show_alternatives` | bool | false | Show approved alternatives |
| `require_justification` | bool | false | Require reason when approved |
| `autofix_available` | bool | false | Can this be auto-fixed |

### 4.4 Strictness Profile Properties

| Property | Type | Description |
|----------|------|-------------|
| `rank_1` | enum | Mode for rank 1 (preferred) |
| `rank_2_3` | enum | Mode for ranks 2-3 (allowed) |
| `rank_4_plus` | enum | Mode for rank 4+ (discouraged) |
| `not_listed` | enum | Mode for unlisted items |

### 4.5 Context Override Properties

| Property | Type | Description |
|----------|------|-------------|
| `default_mode` | enum | Override global default |
| `strictness` | string | Which strictness profile to use |
| `categories` | object | Override category modes |

## 5.0 Example Configurations

### 5.1 Strict Production

```yaml
default_mode: APPROVAL_REQUIRED

categories:
  security:
    mode: BLOCK
  tech_preferences:
    mode: BLOCK
  design_system:
    mode: APPROVAL_REQUIRED
  code_quality:
    mode: WARN

strictness_profiles:
  strict:
    rank_1: LOG
    rank_2_3: APPROVAL_REQUIRED
    rank_4_plus: BLOCK
    not_listed: BLOCK
```

### 5.2 Relaxed Spike

```yaml
default_mode: LOG

categories:
  security:
    mode: WARN  # Even security is relaxed
  tech_preferences:
    mode: LOG
  design_system:
    mode: LOG
  code_quality:
    mode: LOG

strictness_profiles:
  relaxed:
    rank_1: LOG
    rank_2_3: LOG
    rank_4_plus: LOG
    not_listed: WARN
```

### 5.3 Context-Aware

```yaml
default_mode: WARN

# Base categories
categories:
  security:
    mode: BLOCK

# Override by phase
phases:
  phase_1:
    default_mode: LOG
    categories:
      security:
        mode: WARN

  phase_8_to_9:
    default_mode: WARN
    categories:
      security:
        mode: BLOCK
      tech_preferences:
        mode: APPROVAL_REQUIRED

# Override by project type
project_types:
  spike:
    strictness: relaxed
  production:
    strictness: strict
```

## 6.0 Loading Configuration

```python
import yaml
from pathlib import Path

class ConfigLoader:
    def load(self, config_path: str) -> dict:
        with open(config_path) as f:
            return yaml.safe_load(f)

    def get_mode(self, rule_id: str, context: dict) -> EnforcementMode:
        config = self.load(".guardrails/enforcement-config.yaml")

        # Start with rule mode
        rule = self.find_rule(config, rule_id)
        mode = rule.get("mode")

        # Check context overrides
        mode = self.apply_context_overrides(config, mode, context)

        return EnforcementMode(mode)
```

## 7.0 Validation

Configuration should be validated on load:

```python
def validate_config(config: dict):
    # Check required fields
    assert "default_mode" in config
    assert config["default_mode"] in ["LOG", "WARN", "APPROVAL_REQUIRED", "BLOCK"]

    # Check categories
    for cat_name, cat_config in config.get("categories", {}).items():
        assert "mode" in cat_config
        assert cat_config["mode"] in VALID_MODES

    # Check rules
    for rule in config.get("rules", []):
        assert "id" in rule
        assert "category" in rule
        assert "mode" in rule
        assert "message" in rule
```
