# Enforcement Modes

<!-- File UUID: 2a9f4e7b-3c6d-4f8e-9b2a-5d8c1e4f7a3b -->

## 1.0 Overview

Four enforcement modes aligned with software logging levels for intuitive understanding.

## 2.0 Mode Definitions

### 2.1 LOG
**Behavior:** Silent logging only
**User Experience:** No interruption or notification
**Use Cases:**
- Pattern detection
- Metrics collection
- Low-priority observations

**Example:**
```
User adds Next.js (rank 1) to package.json
→ Logged to .guardrails/.enforcement.log
→ No message shown to user
```

### 2.2 WARN
**Behavior:** Log + show warning, allow action
**User Experience:** Warning message displayed, action proceeds
**Use Cases:**
- Best practice violations
- Suboptimal choices (rank 2-3)
- File size warnings

**Example:**
```
User adds Vite (rank 2) to package.json
→ Logged to .guardrails/.enforcement.log
→ Message: "⚠️  Using Vite + React (rank 2). Preferred: Next.js 15.x (rank 1)"
→ Action proceeds
```

### 2.3 APPROVAL_REQUIRED
**Behavior:** Block until explicit user approval (y/n)
**User Experience:** Prompt for decision, wait for response
**Use Cases:**
- Unapproved dependencies
- Architecture pattern not in preferences
- Tech decisions requiring justification

**Example:**
```
User adds create-react-app (unlisted) to package.json
→ Logged to .guardrails/.enforcement.log
→ Message: "🔒 Approval Required: Package 'create-react-app' not in approved list"
→ Shows approved alternatives
→ Prompts: "Approve? [y/N]: "
→ Waits for user input
```

### 2.4 BLOCK
**Behavior:** Hard block, no override possible
**User Experience:** Error message, action rejected
**Use Cases:**
- Security violations (ws:// instead of wss://)
- Hardcoded secrets
- Critical policy violations

**Example:**
```
User writes code with ws:// protocol
→ Logged to .guardrails/.enforcement.log
→ Message: "🚫 Blocked: Insecure ws:// protocol. Must use wss://"
→ Action rejected, exit code 1
```

## 3.0 Mode Selection by Rule Type

```
┌─────────────────────┬──────┬──────┬───────────────────┬───────┐
│ Violation Type      │ LOG  │ WARN │ APPROVAL_REQUIRED │ BLOCK │
├─────────────────────┼──────┼──────┼───────────────────┼───────┤
│ Security            │  -   │  -   │        -          │   ✓   │
│ Unlisted Dependency │  -   │  -   │        ✓          │   -   │
│ Rank 4+ Dependency  │  -   │  ✓   │        -          │   -   │
│ Rank 2-3 Dependency │  -   │  ✓   │        -          │   -   │
│ File Size Limit     │  -   │  ✓   │        -          │   -   │
│ Pattern Detection   │  ✓   │  -   │        -          │   -   │
└─────────────────────┴──────┴──────┴───────────────────┴───────┘
```

## 4.0 Context Overrides

Modes can be overridden based on context:

### 4.1 By Environment
```yaml
environments:
  spike:
    unlisted_dependency: WARN  # Relaxed for prototyping
  production:
    unlisted_dependency: BLOCK  # Strict for production
```

### 4.2 By Phase
```yaml
phases:
  phase_1_to_3:  # Early planning
    unlisted_dependency: LOG
  phase_8_to_9:  # Implementation
    unlisted_dependency: APPROVAL_REQUIRED
```

### 4.3 By Project Type
```yaml
project_types:
  exploration:
    unlisted_dependency: WARN
  prototype:
    unlisted_dependency: APPROVAL_REQUIRED
  production:
    unlisted_dependency: BLOCK
```

## 5.0 Logging Format

All modes write to `.guardrails/.enforcement.log`:

```
[2026-01-15T15:30:00] [LOG] pattern-detected: Pattern 'event-driven' in api.py
[2026-01-15T15:32:15] [WARN] rank-2-dependency: Using Vite (rank 2), preferred: Next.js
[2026-01-15T15:35:42] [APPROVAL_REQUIRED] unlisted-dependency: Package 'angular' not approved - USER_APPROVED
[2026-01-15T15:40:10] [BLOCK] ws-protocol: Insecure ws:// detected in websocket.ts - REJECTED
```

## 6.0 Response Format

Enforcement functions return standardized result:

```python
@dataclass
class EnforcementResult:
    allowed: bool              # Can action proceed?
    mode: EnforcementMode      # Which mode was applied
    message: str               # User-facing message (empty for LOG)
    alternatives: List[str]    # Suggested alternatives
    requires_approval: bool    # Does this need y/n prompt?
    autofix_available: bool    # Can this be auto-fixed?
```
