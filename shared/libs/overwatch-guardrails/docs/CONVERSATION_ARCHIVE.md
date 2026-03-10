# Design Conversation Archive

<!-- File UUID: 5e9c7f2a-8d4b-4e3f-9a6c-1b8d4e7f3a2c -->

## 1.0 Overview

This document archives the original design conversation that led to the Overwatch Guardrails library.

**Date:** 2026-01-15
**Context:** Discussing how to enforce .guardrails/tech-preferences/ through Overwatch

## 2.0 Key Design Questions

### 2.1 Initial Question
"Can I put a guardrail in monitor, ask, or block mode, what other modes should I have?"

### 2.2 Design Evolution

**Iteration 1:** Complex mode system
- monitor, warn, ask, block, suggest, autofix, defer, learn, throttle, escalate
- Too many modes, confusing mental model

**Iteration 2:** Logging-aligned modes
- TRACE, DEBUG, INFO, WARN, ERROR, FATAL
- Better, but too many levels for enforcement

**Iteration 3:** Final 4-mode system (adopted)
- LOG - Silent logging
- WARN - Show warning, allow
- APPROVAL_REQUIRED - Block until approved
- BLOCK - Hard block, no override

**Rationale for 4 modes:**
1. Simple mental model
2. Clear behavior for each
3. No overlap or confusion
4. Maps to common enforcement needs

### 2.3 Ranking Question
"How should I handle ranking things, like if a user starts with TypeScript which is permitted, but Python is preferred?"

**Solution:** Map existing `rank` fields to enforcement:
- Rank 1 → LOG (preferred, silent)
- Rank 2-3 → WARN (allowed alternatives)
- Rank 4+ → WARN (discouraged)
- Unlisted → APPROVAL_REQUIRED (unapproved)

**Key insight:** Rank determines severity, strictness determines mode

## 3.0 Design Principles

### 3.1 Simplicity
- Only 4 modes (not 8-12)
- Clear names that match behavior
- No ambiguous overlap

### 3.2 Flexibility
- Context-based overrides (phase, environment, project type)
- Strictness profiles (relaxed, standard, strict)
- Same rank can have different modes in different contexts

### 3.3 Reusability
- Use existing .guardrails/tech-preferences/*.json files
- Don't duplicate rank definitions
- Single library for all integrations

### 3.4 Observability
- All modes log to .guardrails/.enforcement.log
- Audit trail of all decisions
- Pattern detection for future rule creation

## 4.0 Key Design Decisions

### 4.1 Mode Hierarchy

```
LOG                   Silent, no user notification
  ↓
WARN                  Show warning, allow
  ↓
APPROVAL_REQUIRED     Block until y/n
  ↓
BLOCK                 Hard block, no override
```

### 4.2 Ranking to Mode Mapping

**Standard Strictness:**
```
Rank 1    → LOG
Rank 2-3  → WARN
Rank 4+   → WARN
Unlisted  → APPROVAL_REQUIRED
```

**Context Overrides:**
- Spike mode: Everything more relaxed
- Production: Everything more strict
- Phase 1-3: Relaxed (exploration)
- Phase 8-9: Standard (implementation)

### 4.3 Configuration Location

```
.guardrails/enforcement-config.yaml
```

**Rationale:**
- Grouped with other guardrail files
- YAML for readability
- Version controlled
- Can be customized per project

### 4.4 Integration Points

1. **Frontgate** - Real-time AI action enforcement
2. **Overwatch Subscriber** - Async file monitoring
3. **Git Hooks** - Pre-commit validation
4. **CLI Tools** - Manual validation

## 5.0 Example Scenarios

### 5.1 User adds Next.js (rank 1)
```
Mode: LOG
Message: (none)
Action: Allowed, silently logged
```

### 5.2 User adds Vite (rank 2)
```
Mode: WARN (standard strictness)
Message: "⚠️  Using Vite + React (rank 2). Preferred: Next.js 15.x"
Action: Allowed, warning shown
```

### 5.3 User adds Create React App (unlisted)
```
Mode: APPROVAL_REQUIRED (standard strictness)
Message: "🔒 Package 'create-react-app' not in approved list"
Alternatives: Next.js (1), Vite (2), Expo (3)
Action: Blocked until approved
```

### 5.4 User uses ws:// protocol
```
Mode: BLOCK
Message: "🚫 Blocked: Insecure ws:// protocol. Must use wss://"
Action: Hard blocked, no override
```

## 6.0 Open Questions (for Phase 3)

### 6.1 Autofix Integration
- Should WARN mode offer autofixes?
- How to make autofixes safe?
- When to apply vs. suggest?

### 6.2 Batch Operations
- How to handle batch file creation?
- Should violations aggregate?
- Grace period before enforcement?

### 6.3 Learning Mode
- Should system learn from approval decisions?
- Auto-create policies from repeated approvals?
- How to suggest new rules?

### 6.4 Team Coordination
- Multi-user approval workflows?
- Shared violation queue?
- Notification integrations?

## 7.0 Success Criteria

### 7.1 Phase 2 (Current)
- ✅ Document enforcement modes
- ✅ Document ranking system
- ✅ Define configuration schema
- ✅ Define integration patterns
- ⏳ Research existing systems

### 7.2 Phase 3 (Next)
- Expand design with research findings
- Define Python API
- Create usage examples
- Document edge cases

### 7.3 Phase 8 (Future)
- Implement core library
- Integrate with frontgate
- Write tests
- Deploy to production

## 8.0 References

### 8.1 Existing Systems
- `.guardrails/tech-preferences/*.json` - Ranked tech preferences
- `bin/overwatch/approval_tracker.py` - Tracks approval decisions
- `.claude/hooks/frontgate.py` - Post-tool validation
- `.guardrails/ai-steering/` - Existing validators

### 8.2 Related Docs
- `ENFORCEMENT_MODES.md` - Detailed mode documentation
- `RANKING_SYSTEM.md` - How rankings work
- `CONFIGURATION.md` - Config schema
- `INTEGRATION.md` - Integration patterns

## 9.0 Timeline

- **2026-01-15:** Initial design conversation
- **2026-01-15:** Project created in Phase 2
- **TBD:** Complete research (Phase 2)
- **TBD:** Advance to Phase 3 (Expansion)
- **TBD:** Advance to Phase 8 (Implementation)
