# Brownfield Entry: Working with Existing Code

<!-- File UUID: bf1e3a2c-9d4f-4b8e-a1c5-7f2e8d3b6a9c -->

**What is Brownfield?** Development work on existing codebases, including bug fixes, new features, refactoring, and maintenance.

**When to use:**
- Fixing bugs in production code
- Adding features to existing projects
- Refactoring or improving existing code
- Technical debt reduction
- Performance optimization
- Security patches

**Comparison to Greenfield:**

| Aspect | Greenfield | Brownfield |
|--------|------------|------------|
| Starting point | Blank slate | Existing code |
| Phases required | All 9 phases | Abbreviated (0→8→9) |
| SEED phase | Required | Skip or abbreviated |
| Architecture | Design from scratch | Work within existing |
| Tests | Write all new | Wrap + extend existing |

---

## Work Types

| Work Type | Description | Typical Duration | Phases Used |
|-----------|-------------|------------------|-------------|
| **HOTFIX** | Critical production issue | Minutes to hours | 0 → 8 → 9 |
| **BUG_FIX** | Standard bug resolution | Hours to 2 days | 0 → 7 → 8 → 9 |
| **FEATURE** | New capability on existing code | 2-10 days | 0 → 3 → 5 → 6 → 7 → 8 → 9 |
| **REFACTOR** | Improve without changing behavior | 1-5 days | 0 → 7 → 8 → 9 |
| **OPTIMIZATION** | Performance improvements | 1-5 days | 0 → 7 → 8 → 9 |
| **SECURITY** | Security patches/hardening | Hours to days | 0 → 7 → 8 → 9 |

---

## Phase 0: ASSESSMENT (Brownfield Entry Point)

**Purpose:** Understand existing code before making changes

**Duration:** 15 minutes to 2 hours (scales with complexity)

**Deliverables:**
1. Understanding of affected code areas
2. Impact analysis (what could break)
3. Test coverage assessment
4. Work type classification

### Assessment Template

```markdown
## Brownfield Assessment

**Project:** {project-name}
**Work Type:** HOTFIX | BUG_FIX | FEATURE | REFACTOR | OPTIMIZATION | SECURITY
**Date:** {date}

### Problem Statement
{What needs to be fixed/added/improved?}

### Affected Areas
| File/Component | Impact | Test Coverage |
|----------------|--------|---------------|
| {file.ts} | High | 80% |

### Risk Assessment
- [ ] Breaking changes possible
- [ ] Database migrations needed
- [ ] External API changes
- [ ] User-facing impact

### Approach
{Brief description of fix/feature approach}
```

---

## Brownfield Workflow Selection

After Phase 0 Assessment, route to appropriate workflow:

```
Phase 0 (ASSESSMENT)
        │
        ├─→ HOTFIX?     → Skip to Phase 8 (expedited)
        │                 See: HOTFIX_WORKFLOW.md
        │
        ├─→ BUG_FIX?    → Phase 7 → 8 → 9 (abbreviated)
        │                 Write regression test, fix, validate
        │
        ├─→ FEATURE?    → Phase 3 → 5 → 6 → 7 → 8 → 9 (light SDLC)
        │                 Design within constraints, then implement
        │
        ├─→ REFACTOR?   → Phase 7 → 8 → 9 (wrap-first)
        │                 Wrap with tests, refactor, validate
        │
        └─→ SECURITY?   → Phase 7 → 8 → 9 (audit-first)
                          Audit, patch, verify, document
```

---

## Brownfield-Specific Rules

### 1. Code Allowed After Phase 0

Unlike greenfield (code at Phase 8), brownfield allows code after Phase 0:

| Work Type | Code Allowed After |
|-----------|-------------------|
| HOTFIX | Phase 0 (immediate) |
| BUG_FIX | Phase 0 (with regression test) |
| FEATURE | Phase 6 (after design) |
| REFACTOR | Phase 7 (after wrapping tests) |

### 2. Test-Wrap Before Refactor

Before refactoring existing code:
1. Identify untested code paths
2. Add "characterization tests" that capture current behavior
3. Only then refactor
4. Tests verify behavior unchanged

### 3. Minimal Disruption Principle

- Prefer small, focused changes
- Avoid scope creep ("while I'm here...")
- One concern per PR/commit
- Don't refactor unrelated code

### 4. Existing Architecture Respect

- Work within existing patterns
- Don't introduce new frameworks without approval
- Match existing code style
- Use existing abstractions

---

## .project File for Brownfield

```yaml
uuid: {existing-project-uuid}
name: {project-name}
work_type: brownfield
brownfield_mode: hotfix | bug_fix | feature | refactor | optimization | security
current_phase: 0
original_phase: 9

brownfield:
  issue_ref: "GH-123"
  affected_files:
    - src/components/Auth.tsx
  impact: low | medium | high | critical
  estimated_hours: 4
  regression_test_added: false
```

---

## Intent Detection Triggers

**Route to Brownfield when user says:**

| Pattern | Work Type |
|---------|-----------|
| "fix bug in...", "bug in...", "broken..." | BUG_FIX |
| "hotfix needed", "production down", "critical bug" | HOTFIX |
| "add feature to existing...", "enhance..." | FEATURE |
| "refactor...", "clean up...", "improve..." | REFACTOR |
| "optimize...", "performance issue", "slow..." | OPTIMIZATION |
| "security issue", "vulnerability", "patch..." | SECURITY |

---

## Brownfield vs New Project Detection

**Decision Tree:**

```
User request
     │
     ├─→ References existing project? ──Yes──→ BROWNFIELD
     │         │
     │        No
     │         │
     ├─→ .project file exists? ──Yes──→ Check phase
     │         │                           │
     │        No                     Phase 8+? ──Yes──→ BROWNFIELD
     │         │                           │
     │         │                          No
     │         │                           │
     ├─→ Code exists in dir? ────────────→ Ask: "Existing project?"
     │         │
     │        No
     │         │
     └─→ GREENFIELD (standard SDLC)
```

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Skip Phase 0 Assessment | Always understand before changing |
| Refactor without tests | Wrap with characterization tests first |
| Expand scope mid-fix | One concern per change |
| Ignore existing patterns | Match existing code style |
| Skip regression tests | Always add test that reproduces bug |
| Deploy without validation | Always test in staging first |

---

## Related Documentation

- **HOTFIX_WORKFLOW.md** - Expedited critical fixes
- **MAINTENANCE_TRIAGE.md** - Classify and prioritize issues
- **SDLC_OVERVIEW.md** - Standard greenfield process
