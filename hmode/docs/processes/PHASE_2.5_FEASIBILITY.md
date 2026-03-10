### Phase 2.5: FEASIBILITY VALIDATION 🎯 (Go/No-Go Gate)
**Goal:** Validate project is feasible and worth pursuing before investing in design/implementation
**Output:** `FEASIBILITY.md` with go/no-go decision and rationale
**Title:** `# Stage 2.5 - Feasibility Validation`

**Applies to:** `project_type: "production"` only
**Skip for:** `project_type: "exploration"` or `"prototype"` (proceed Phase 2→3 directly)

---

## 1.0 Project Types

| Type | Phase 2.5 | Description | Examples |
|------|-----------|-------------|----------|
| **exploration** | Skip | Learning, idea exploration, curiosity-driven | "What if...", learning new tech, hobby |
| **prototype** | Skip | Quick validation, POC, small/hobby projects | Weekend projects, demos, spikes |
| **production** | **Required** | Serious projects intended for real use/users | Tools for work, customer deliverables, products |

**Set in `.project` file:**
```yaml
project_type: "production"  # exploration | prototype | production
```

---

## 2.0 Validation Criteria

| # | Check | Question | Scoring |
|---|-------|----------|---------|
| 1 | **Technical Feasibility** | Can this be built with available tech/skills/time? | Yes / Partial / No |
| 2 | **Effort Justification** | Is building worth it vs existing solutions found in Phase 2? | Build / Buy / Abandon |
| 3 | **Differentiation** | Does this solve something existing tools don't? | Clear gap / Marginal / None |
| 4 | **Longevity** | Will this still be useful in 1 year? | Yes / Uncertain / No |
| 5 | **Target Audience** | Who benefits? What's the addressable market/user base? | Defined / Vague / Unknown |
| 6 | **Risk Assessment** | Are there blockers, unknowns, or dependencies? | Low / Medium / High |

---

## 3.0 Decision Matrix

**Scoring:**
- Each criterion: **+1** (positive), **0** (neutral), **-1** (negative)
- Total score range: -6 to +6

| Score | Decision | Action |
|-------|----------|--------|
| **+4 to +6** | ✅ **PROCEED** | Continue to Phase 3 (Expansion) |
| **+1 to +3** | 🔄 **CONDITIONAL** | Address concerns, may proceed with mitigations |
| **-2 to 0** | 🔬 **SPIKE** | Technical unknowns need exploration first |
| **-3 to -6** | ❌ **ABANDON** | Not worth pursuing, archive idea |

**Special case:** If "Effort Justification" = **Buy**, recommend existing solution and close.

---

## 4.0 Feasibility Report Template

```markdown
# Stage 2.5 - Feasibility Validation

## 1.0 Project Summary
- **Name:** [Project name]
- **Type:** production
- **One-liner:** [What it does]

## 2.0 Research Summary (from Phase 2)
- **Existing solutions evaluated:** [Count]
- **Best alternative:** [Name] - [Why not sufficient]
- **Gap identified:** [What's missing]

## 3.0 Feasibility Assessment

### 3.1 Technical Feasibility
- **Score:** [+1 / 0 / -1]
- **Assessment:** [Can be built with X, Y, Z technologies]
- **Risks:** [Any technical unknowns]

### 3.2 Effort Justification
- **Score:** [+1 / 0 / -1]
- **Build vs Buy:** [Rationale for building vs using existing]
- **Estimated effort:** [T-shirt size: S/M/L/XL]

### 3.3 Differentiation
- **Score:** [+1 / 0 / -1]
- **Unique value:** [What this does that alternatives don't]
- **Competitive advantage:** [Why users would choose this]

### 3.4 Longevity (1-Year Horizon)
- **Score:** [+1 / 0 / -1]
- **Durability:** [Will the problem/need still exist?]
- **Maintenance burden:** [Ongoing effort required]
- **Tech stability:** [Are dependencies stable?]

### 3.5 Target Audience & Market
- **Score:** [+1 / 0 / -1]
- **Primary audience:** [Who benefits most]
- **TAM estimate:** [Total addressable market / user base size]
- **Use cases:** [Top 2-3 use cases]

### 3.6 Risk Assessment
- **Score:** [+1 / 0 / -1]
- **Technical risks:** [List]
- **External dependencies:** [List]
- **Mitigation strategies:** [How to address]

## 4.0 Decision

| Criterion | Score |
|-----------|-------|
| Technical Feasibility | [+1/0/-1] |
| Effort Justification | [+1/0/-1] |
| Differentiation | [+1/0/-1] |
| Longevity | [+1/0/-1] |
| Target Audience | [+1/0/-1] |
| Risk Assessment | [+1/0/-1] |
| **TOTAL** | **[Sum]** |

**Decision:** [✅ PROCEED / 🔄 CONDITIONAL / 🔬 SPIKE / ❌ ABANDON]

**Rationale:** [1-2 sentences explaining decision]

**Next steps:**
- [ ] [Action item 1]
- [ ] [Action item 2]
```

---

## 5.0 Examples

**Example 1: PROCEED**
```
Project: Internal dashboard for team metrics
- Technical: +1 (standard web stack)
- Effort: +1 (nothing fits our specific workflow)
- Differentiation: +1 (custom metrics our team tracks)
- Longevity: +1 (team needs won't change)
- Audience: 0 (small team, but clear need)
- Risk: +1 (low complexity)
Total: +5 → PROCEED
```

**Example 2: ABANDON**
```
Project: Yet another todo app
- Technical: +1 (easy to build)
- Effort: -1 (hundreds of great alternatives)
- Differentiation: -1 (no unique value)
- Longevity: 0 (todos always needed, but so are alternatives)
- Audience: -1 (saturated market)
- Risk: +1 (low risk, but why bother)
Total: -1 → ABANDON (use Todoist instead)
```

**Example 3: SPIKE**
```
Project: Real-time collaborative whiteboard
- Technical: -1 (CRDT complexity unknown)
- Effort: 0 (alternatives expensive for teams)
- Differentiation: +1 (self-hosted, privacy-focused)
- Longevity: +1 (collaboration tools growing)
- Audience: +1 (remote teams, clear need)
- Risk: -1 (CRDT implementation risky)
Total: +1, but Technical=-1 → SPIKE (prototype CRDT first)
```

---

## 6.0 Workflow Integration

```
Phase 2 (RESEARCH) completes
    ↓
Check project_type in .project
    ↓
┌─────────────────────────────────────┐
│ exploration or prototype?           │
│   → Skip to Phase 3 (EXPANSION)     │
│                                     │
│ production?                         │
│   → Execute Phase 2.5               │
│   → Generate FEASIBILITY.md         │
│   → Make go/no-go decision          │
└─────────────────────────────────────┘
    ↓
Decision outcome:
  PROCEED → Phase 3 (EXPANSION)
  CONDITIONAL → Address concerns, then Phase 3
  SPIKE → Execute spike, return to Phase 2.5
  ABANDON → Archive in ideas/archived/
```

---

## 7.0 .project Schema Addition

```yaml
# Add to .project file
project_type: "production"  # exploration | prototype | production

# Phase 2.5 results (production projects only)
feasibility:
  decision: "proceed"  # proceed | conditional | spike | abandon
  score: 5
  date: "2025-01-15"
  blocking_concerns: []  # List any concerns that must be addressed
```

---

**🚨 ENFORCEMENT:**
- Production projects MUST complete Phase 2.5 before Phase 3
- Decision MUST be documented in `FEASIBILITY.md`
- ABANDON decisions archive the idea with rationale
- SPIKE decisions require time-boxed exploration (max 3 days)

**Exit:** Feasibility report complete, decision documented, ready for next phase (or archived)

---
