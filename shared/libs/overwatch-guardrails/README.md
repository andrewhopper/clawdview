# Overwatch Guardrails

<!-- File UUID: 7e3d9f2a-4b8c-4e1d-9a5f-3c8b7d2e6f1a -->

**Status:** Phase 2 - Research
**Type:** Shared Library
**Purpose:** Reusable guardrails enforcement for Overwatch ecosystem

## Overview

Standardized enforcement framework providing 4 modes (LOG, WARN, APPROVAL_REQUIRED, BLOCK) with ranking-aware tech preference validation.

## Problem Statement

**Current State:**
- Validation logic scattered across frontgate.py, approval_tracker.py, validators
- No consistent enforcement model
- Tech preferences exist but not systematically enforced
- Rankings defined but not used in enforcement decisions

**Desired State:**
- Single reusable library for all guardrail enforcement
- Clear 4-mode system aligned with logging levels
- Ranking-aware validation (rank 1 = preferred, unlisted = requires approval)
- Context-based strictness (phase, environment, project type)

## Core Concepts

### 1. Enforcement Modes

| Mode | Behavior | User Experience |
|------|----------|----------------|
| LOG | Silent logging | No interruption |
| WARN | Show warning, allow | Warning message displayed |
| APPROVAL_REQUIRED | Block until approved | Requires y/n response |
| BLOCK | Hard block | Action rejected |

### 2. Ranking System

| Rank | Status | Default Mode |
|------|--------|--------------|
| 1 | Preferred | LOG |
| 2-3 | Allowed | WARN |
| 4+ | Discouraged | WARN |
| Unlisted | Unapproved | APPROVAL_REQUIRED |

### 3. Context-Based Strictness

```yaml
spike: relaxed
phase_1_to_3: relaxed
phase_8_to_9: standard
production: strict
```

## Documentation

- `docs/ENFORCEMENT_MODES.md` - Detailed mode documentation
- `docs/RANKING_SYSTEM.md` - How rankings affect enforcement
- `docs/CONFIGURATION.md` - Configuration schema and examples
- `docs/INTEGRATION.md` - Integration with frontgate, overwatch, hooks
- `docs/CONVERSATION_ARCHIVE.md` - Original design discussion

## Usage (Future)

```python
from overwatch_guardrails import GuardrailEnforcer, Violation

enforcer = GuardrailEnforcer(".guardrails/enforcement-config.yaml")

result = enforcer.enforce(
    rule_id="unapproved-dependency",
    violation=Violation(...),
    context={"phase": "phase_8", "project_type": "prototype"}
)

if not result.allowed:
    print(result.message)
```

## Project Status

**Current Phase:** Phase 2 - Research

**Next Steps:**
1. Research existing guardrail systems (Python, Rust, Go ecosystems)
2. Document integration patterns with existing .guardrails/ infrastructure
3. Define Python API surface
4. Create configuration schema
5. Advance to Phase 3 (Expansion) for detailed design
