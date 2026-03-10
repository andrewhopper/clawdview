<!-- File UUID: 71bcc7ab-66dd-47a1-8d6d-9a1bf2dd176f -->
# Maintenance Triage: Classifying Incoming Work

<!-- File UUID: mt3f5c6e-7b8a-4d9f-c3e2-9a4b8c7d6e5f -->

**Purpose:** Rapidly classify incoming maintenance requests to route to the correct workflow.

---

## Triage Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAINTENANCE TRIAGE                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                    Is production impacted?
                              │
                    ┌─────────┴─────────┐
                   Yes                  No
                    │                    │
           Is it critical?         Is it a bug?
                    │                    │
              ┌─────┴─────┐        ┌─────┴─────┐
             Yes         No       Yes         No
              │           │        │           │
           HOTFIX     BUG_FIX   BUG_FIX    Is it new
           (P0/P1)    (P2)      (P3)     functionality?
                                              │
                                        ┌─────┴─────┐
                                       Yes         No
                                        │           │
                                    FEATURE    REFACTOR/
                                              OPTIMIZATION
```

---

## Classification Matrix

| Signal | HOTFIX | BUG_FIX | FEATURE | REFACTOR | OPTIMIZATION |
|--------|--------|---------|---------|----------|--------------|
| Production down | Yes | - | - | - | - |
| Users blocked | Maybe | Yes | - | - | - |
| Wrong behavior | - | Yes | - | - | - |
| Missing capability | - | - | Yes | - | - |
| Code quality issue | - | - | - | Yes | - |
| Performance slow | - | Maybe | - | - | Yes |
| Security vuln | Maybe | Maybe | - | - | - |
| Tech debt | - | - | - | Yes | - |

---

## Priority Levels

| Priority | Response Time | Examples |
|----------|---------------|----------|
| **P0** | Immediate | Production down, data loss, security breach |
| **P1** | < 4 hours | Major feature broken, significant user impact |
| **P2** | < 24 hours | Bug affecting some users, workaround exists |
| **P3** | < 1 week | Minor bug, cosmetic issue |
| **P4** | Backlog | Nice-to-have, low impact |

---

## Triage Prompts

**AI MUST ask if unclear:**

```markdown
## Triage Questions

1. **Is this affecting production right now?** [Y/n]
2. **Are users blocked from completing tasks?** [Y/n/partial]
3. **Is there a workaround?** [Y/n]
4. **Is this a security issue?** [Y/n]
5. **Is this new functionality or fixing existing?** [new/fix]
6. **What's the urgency?** [immediate/today/this week/backlog]
```

---

## Quick Classification

**Keyword Detection:**

| Keywords | Classification |
|----------|----------------|
| "production down", "critical", "urgent", "P0" | HOTFIX |
| "broken", "not working", "error", "exception" | BUG_FIX |
| "add", "new feature", "implement", "create" | FEATURE |
| "refactor", "clean up", "restructure", "simplify" | REFACTOR |
| "slow", "performance", "latency", "optimize" | OPTIMIZATION |
| "security", "vulnerability", "CVE", "patch" | SECURITY |

---

## Triage Output Template

```markdown
## Triage Result

**Request:** {one-line summary}
**Classification:** HOTFIX | BUG_FIX | FEATURE | REFACTOR | OPTIMIZATION | SECURITY
**Priority:** P0 | P1 | P2 | P3 | P4
**Workflow:** → {link to workflow}

**Rationale:**
{Why this classification}

**Proceed?** [Y/n/discuss]
```

---

## Escalation Criteria

**Escalate to human when:**
- Classification unclear after questions
- Multiple classifications apply equally
- Priority disputed
- Scope larger than expected
- Security implications uncertain

---

## Integration with Brownfield Entry

After triage → Route to BROWNFIELD_ENTRY.md with:
```yaml
work_type: brownfield
brownfield_mode: {classification}
priority: {P0-P4}
```

---

## Examples

**Example 1: Clear Hotfix**
```
User: "Production API is returning 500 errors for all requests"

Triage:
- Production impacted: Yes
- Users blocked: Yes
- Workaround: No

→ Classification: HOTFIX (P0)
→ Route to: HOTFIX_WORKFLOW.md
```

**Example 2: Standard Bug**
```
User: "The date picker shows wrong format on Safari"

Triage:
- Production impacted: Partial
- Users blocked: No (workaround: use Chrome)
- Security: No

→ Classification: BUG_FIX (P3)
→ Route to: BROWNFIELD_ENTRY.md
```

**Example 3: Feature Request**
```
User: "Add export to CSV functionality"

Triage:
- New functionality: Yes
- Existing behavior broken: No

→ Classification: FEATURE
→ Route to: BROWNFIELD_ENTRY.md (light SDLC)
```

---

## Related Documentation

- **BROWNFIELD_ENTRY.md** - Brownfield workflow overview
- **HOTFIX_WORKFLOW.md** - Critical fix process
- **SDLC_OVERVIEW.md** - Full greenfield process
