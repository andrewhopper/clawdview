# Integration Patterns

<!-- File UUID: 6c8f4a3e-7d9b-4e2f-8a5c-9b7d3e6f2a1b -->

## 1.0 Overview

Overwatch Guardrails can be integrated into multiple enforcement points:

1. **Frontgate** - Claude Code post-tool hooks
2. **Overwatch Subscribers** - File change automation
3. **Git Hooks** - Pre-commit validation
4. **CLI Tools** - Manual validation
5. **CI/CD** - Pipeline checks

## 2.0 Frontgate Integration

### 2.1 Current Architecture

```
.claude/hooks/frontgate.sh (wrapper)
  ↓
.claude/hooks/frontgate.py (orchestrator)
  ↓
.guardrails/ai-steering/
  ├── design_system_validator.py
  ├── grace_period_validator.py
  └── batch_detector.py
```

### 2.2 Adding Guardrails Library

```python
# .claude/hooks/frontgate.py

from overwatch_guardrails import GuardrailEnforcer, Violation

enforcer = GuardrailEnforcer(".guardrails/enforcement-config.yaml")

def validate_file(tool_name: str, file_path: str):
    """Validate file against guardrails"""

    # Check dependency files
    if file_path.endswith(("package.json", "requirements.txt")):
        violation = check_tech_preferences(file_path)
        if violation:
            result = enforcer.enforce(
                rule_id="unapproved-dependency",
                violation=violation,
                context=get_context()
            )

            if result.mode == EnforcementMode.APPROVAL_REQUIRED:
                if not prompt_user_approval(result):
                    sys.exit(1)  # Block

            elif result.mode == EnforcementMode.BLOCK:
                print(result.message)
                sys.exit(1)

            elif result.mode == EnforcementMode.WARN:
                print(result.message)

            # LOG mode is silent

def get_context() -> dict:
    """Build context from environment"""
    return {
        "phase": read_project_phase(),
        "project_type": detect_project_type(),
        "environment": "development"
    }
```

### 2.3 Benefits

- Runs on every Write/Edit tool use
- Real-time enforcement
- Can block before file is written
- User gets immediate feedback

## 3.0 Overwatch Subscriber Integration

### 3.1 New Subscriber Service

```yaml
# config/overwatch-services.yaml

subscribers:
  guardrails_enforcer:
    name: "Guardrails Enforcer"
    pattern: "guardrails_subscriber.py"
    log: "guardrails-enforcer.log"
    description: "Enforces tech preferences and standards"
    port: null
    command: "PYTHONPATH=\"$ZMQ_LIB/python\" \"$PYTHON\" -u \"$PROJECT_ROOT/bin/overwatch/guardrails_subscriber.py\""
    depends_on: ["zmq_bus", "file_watcher"]
    health_check:
      type: "process"
```

### 3.2 Subscriber Implementation

```python
# bin/overwatch/guardrails_subscriber.py

import zmq
from overwatch_guardrails import GuardrailEnforcer

enforcer = GuardrailEnforcer(".guardrails/enforcement-config.yaml")

def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://127.0.0.1:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "file.created")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "file.modified")

    while True:
        topic, payload = subscriber.recv_multipart()
        event = json.loads(payload)

        file_path = event["path"]

        # Check guardrails
        violations = check_file(file_path)
        for violation in violations:
            result = enforcer.enforce(
                rule_id=violation.rule_id,
                violation=violation,
                context=build_context(file_path)
            )

            if result.mode in [EnforcementMode.WARN, EnforcementMode.BLOCK]:
                # Send notification to user
                notify_user(result)
```

### 3.3 Benefits

- Async validation after file changes
- Can aggregate violations over time
- Non-blocking notifications
- Pattern detection across multiple files

## 4.0 Git Hook Integration

### 4.1 Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check staged files against guardrails
uv run python -m overwatch_guardrails check-staged \
  --config .guardrails/enforcement-config.yaml \
  --strict

exit $?
```

### 4.2 Implementation

```python
# overwatch_guardrails/cli.py

def check_staged(config_path: str, strict: bool = False):
    """Check all staged files against guardrails"""

    enforcer = GuardrailEnforcer(config_path)
    staged_files = get_staged_files()

    violations = []
    for file_path in staged_files:
        file_violations = check_file(file_path)
        violations.extend(file_violations)

    # Enforce all violations
    blocked = False
    for violation in violations:
        result = enforcer.enforce(violation.rule_id, violation, context)

        if result.mode == EnforcementMode.BLOCK:
            blocked = True
            print(result.message)

        elif result.mode == EnforcementMode.APPROVAL_REQUIRED:
            if not prompt_user_approval(result):
                blocked = True

    if blocked:
        sys.exit(1)
```

### 4.3 Benefits

- Catches violations before commit
- Prevents unapproved code from entering repo
- Batch checks all staged files
- Can be strict or lenient

## 5.0 CLI Tool Integration

### 5.1 Standalone Validation

```bash
# Check specific file
bin/guardrails check package.json

# Check all files in project
bin/guardrails check-all

# Show violations
bin/guardrails violations --mode BLOCK

# Set enforcement mode
bin/guardrails set-mode --category security BLOCK
```

### 5.2 Implementation

```python
# bin/guardrails (CLI wrapper)

import click
from overwatch_guardrails import GuardrailEnforcer

@click.group()
def cli():
    pass

@cli.command()
@click.argument("file_path")
def check(file_path):
    """Check file against guardrails"""
    enforcer = GuardrailEnforcer(".guardrails/enforcement-config.yaml")
    violations = check_file(file_path)

    for violation in violations:
        result = enforcer.enforce(violation.rule_id, violation, context)
        print(f"[{result.mode.value}] {result.message}")

@cli.command()
@click.option("--mode", type=click.Choice(["LOG", "WARN", "APPROVAL_REQUIRED", "BLOCK"]))
@click.option("--category")
def set_mode(mode, category):
    """Set enforcement mode"""
    update_config(category, mode)
    print(f"Set {category} to {mode}")
```

### 5.3 Benefits

- Manual validation on demand
- Configuration management
- Violation reporting
- Integration with scripts

## 6.0 Integration Points Summary

```
┌─────────────────────┬──────────────┬────────────┬─────────────┐
│ Integration Point   │ Timing       │ Blocking   │ Use Case    │
├─────────────────────┼──────────────┼────────────┼─────────────┤
│ Frontgate           │ Real-time    │ Yes        │ AI actions  │
│ Overwatch Subscriber│ Async        │ No         │ Monitoring  │
│ Git Pre-Commit      │ Pre-commit   │ Yes        │ Repo guard  │
│ CLI Tool            │ On-demand    │ Optional   │ Manual      │
│ CI/CD Pipeline      │ Pre-deploy   │ Yes        │ Gate check  │
└─────────────────────┴──────────────┴────────────┴─────────────┘
```

## 7.0 Recommended Integration Strategy

### 7.1 Phase 1: Monitoring

```yaml
# Start with LOG/WARN only
default_mode: LOG

categories:
  tech_preferences:
    mode: LOG

# Collect data for 1-2 weeks
# Understand violation patterns
```

### 7.2 Phase 2: Warnings

```yaml
# Enable warnings
default_mode: WARN

categories:
  tech_preferences:
    mode: WARN  # Show warnings but allow
  security:
    mode: BLOCK  # Security always blocked
```

### 7.3 Phase 3: Enforcement

```yaml
# Enable strict enforcement
default_mode: WARN

categories:
  tech_preferences:
    mode: APPROVAL_REQUIRED
  security:
    mode: BLOCK
```

## 8.0 Context Detection

All integrations need to detect context:

```python
def build_context() -> dict:
    """Build context from environment"""
    return {
        "phase": read_project_phase(),
        "project_type": detect_project_type(),
        "environment": os.getenv("ENV", "development"),
        "user": os.getenv("USER"),
        "timestamp": datetime.now().isoformat()
    }

def read_project_phase() -> str:
    """Read phase from .project file"""
    if Path(".project").exists():
        with open(".project") as f:
            for line in f:
                if line.startswith("phase:"):
                    return f"phase_{line.split(':')[1].strip()}"
    return "unknown"

def detect_project_type() -> str:
    """Detect project type from .project file"""
    if Path(".project").exists():
        with open(".project") as f:
            content = f.read()
            if "type: spike" in content:
                return "spike"
            if "type: production" in content:
                return "production"
    return "prototype"
```
