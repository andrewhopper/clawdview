<!-- File UUID: 439b00bd-2cf8-4cde-8494-f37535b377da -->
# Hotfix Workflow: Critical Production Fixes

<!-- File UUID: hf2e4b3d-8c5a-4f9e-b2d1-6a3c7e8f9d0a -->

**What is a Hotfix?** An expedited fix for critical production issues that bypasses standard phases.

**When to use:**
- Production system down
- Critical security vulnerability
- Data corruption or loss occurring
- Major revenue-impacting bug
- Blocking issue affecting all users

**NOT for:**
- Minor bugs (use BUG_FIX workflow)
- Features (use FEATURE workflow)
- Performance improvements (use OPTIMIZATION)
- Anything that can wait 24+ hours

---

## Hotfix Criteria

**At least ONE must be true:**
- [ ] Production unavailable or severely degraded
- [ ] Active security breach or critical vulnerability
- [ ] Data loss occurring
- [ ] Revenue loss exceeding $X/hour (define per org)
- [ ] Legal/compliance deadline imminent

**If none apply:** Use standard BUG_FIX workflow instead.

---

## Hotfix Workflow

```
CRITICAL ISSUE
      │
      ▼
┌─────────────────┐
│ RAPID ASSESS    │  ← 5-15 minutes max
│ (Phase 0 lite)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ IMPLEMENT FIX   │  ← Minimal viable fix
│ (Phase 8)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ VALIDATE        │  ← Smoke test only
│ (Phase 9 lite)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ DEPLOY          │  ← To production
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ POST-MORTEM     │  ← Schedule follow-up
└─────────────────┘
```

---

## Phase 0: Rapid Assessment (5-15 min)

**Goal:** Understand just enough to fix safely

**Template:**
```markdown
## Hotfix Assessment

**Incident:** {one-line description}
**Severity:** P0 (Critical) | P1 (High)
**Impact:** {who/what is affected}
**Root Cause Hypothesis:** {best guess}
**Proposed Fix:** {minimal change to resolve}
**Rollback Plan:** {if fix fails}

**Files to Change:**
- {file1.ts}
- {file2.ts}

**Risk:** {what could go wrong}
```

**DO NOT:**
- Spend more than 15 minutes on assessment
- Create detailed documentation
- Research alternative approaches
- Wait for perfect understanding

---

## Phase 8: Implementation (Minimal Fix)

**Rules:**
1. **Smallest possible change** - Fix the bug, nothing else
2. **No refactoring** - Even if code is ugly
3. **No new features** - Even if "easy to add"
4. **No dependency updates** - Unless required for fix
5. **Document the hack** - If fix is temporary

**Code Comments for Temporary Fixes:**
```typescript
// HOTFIX: {date} - {ticket}
// This is a temporary fix. Proper solution in {future-ticket}
// Reason: {why this hack was necessary}
```

**Testing:**
- Run existing tests (must pass)
- Manual smoke test the fix
- Skip comprehensive testing (do post-deploy)

---

## Phase 9: Validation (Smoke Only)

**Minimum Validation:**
1. [ ] Fix resolves the immediate issue
2. [ ] No obvious new errors introduced
3. [ ] Core happy path works
4. [ ] Rollback procedure tested/ready

**Skip:**
- Full regression suite (run async after deploy)
- Performance testing
- Comprehensive edge case testing

---

## Deployment

**Hotfix Deployment Checklist:**
1. [ ] Rollback procedure documented
2. [ ] On-call/incident team notified
3. [ ] Deploy to staging (if fast) or skip
4. [ ] Deploy to production
5. [ ] Verify fix in production
6. [ ] Monitor for 15-30 minutes
7. [ ] Update incident status

---

## Post-Mortem (Required)

**Schedule within 48 hours:**

```markdown
## Hotfix Post-Mortem

**Incident:** {description}
**Date:** {date}
**Duration:** {time to resolution}
**Impact:** {users/revenue affected}

### Timeline
- HH:MM - Issue detected
- HH:MM - Investigation started
- HH:MM - Root cause identified
- HH:MM - Fix deployed
- HH:MM - Issue resolved

### Root Cause
{What actually caused the issue}

### Fix Applied
{What was the hotfix}

### Follow-up Required
- [ ] Proper fix (if hotfix was temporary): {ticket}
- [ ] Add regression test: {ticket}
- [ ] Update documentation: {ticket}
- [ ] Process improvement: {ticket}

### Prevention
{How to prevent similar issues}
```

---

## .project File for Hotfix

```yaml
uuid: {project-uuid}
name: {project-name}
work_type: brownfield
brownfield_mode: hotfix
current_phase: 8

hotfix:
  incident_id: "INC-123"
  severity: P0 | P1
  started_at: 2026-01-28T10:00:00Z
  resolved_at: null
  is_temporary: true
  follow_up_ticket: "JIRA-456"
  rollback_commit: "abc123"
```

---

## Hotfix vs Bug Fix Decision

```
Is production down/degraded? ──Yes──→ HOTFIX
         │
        No
         │
Is there active data loss? ──Yes──→ HOTFIX
         │
        No
         │
Is it a security breach? ──Yes──→ HOTFIX
         │
        No
         │
Can it wait 24 hours? ──No──→ HOTFIX
         │
        Yes
         │
         └──→ BUG_FIX (standard workflow)
```

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Scope creep during hotfix | Fix one thing only |
| Skip rollback plan | Always have rollback ready |
| Forget post-mortem | Schedule it immediately |
| Leave temporary fix forever | Create follow-up ticket |
| Test extensively before deploy | Smoke test, deploy fast |
| Deploy without monitoring | Watch for 15-30 min post-deploy |

---

## Communication Template

**During Incident:**
```
[STATUS UPDATE]
Issue: {description}
Impact: {who affected}
Status: Investigating / Fix in progress / Deploying / Resolved
ETA: {if known}
Next update: {time}
```

**Resolution:**
```
[RESOLVED]
Issue: {description}
Impact: {duration, users affected}
Resolution: {what was done}
Post-mortem: Scheduled for {date}
```

---

## Related Documentation

- **BROWNFIELD_ENTRY.md** - General brownfield overview
- **MAINTENANCE_TRIAGE.md** - Issue classification
- **INCIDENT_RESPONSE.md** - Full incident process
