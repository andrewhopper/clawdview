# Spike Exception: Skip to Implementation

**What is a Spike?** Time-boxed technical exploration to answer specific question

**When to use:**
- Validate technical feasibility only (e.g., "Can Playwright test WebSockets?")
- Evaluate library/tool compatibility
- Prototype throwaway code to derisk technical approach
- Research phase (Phase 2) identifies critical unknown

**Requirements:**
- Max 3 days time-box
- Document as `prototype_type: "spike"` in `.project`
- Deliverables: Technical findings doc + go/no-go recommendation
- Code is THROWAWAY (deleted after learning)

---

## 🚦 SPIKE REQUIREMENTS CONFIRMATION (MANDATORY)

**BEFORE writing ANY spike code, AI MUST confirm requirements and approach.**

### Confirmation Gate Template

```markdown
## Spike Confirmation Gate

**Question to Answer:**
{What specific technical question are we trying to answer?}

**Proposed Approach:**
1. {Step 1 of investigation}
2. {Step 2 of investigation}
3. {Step 3 of investigation}

**Success Criteria:**
- [ ] {Criterion 1 - specific, measurable}
- [ ] {Criterion 2 - specific, measurable}

**Failure Criteria:**
- [ ] {What would make us abandon this approach?}

**Tech Stack for Spike:**
- Language: {e.g., TypeScript, Python}
- Framework: {e.g., Express, FastAPI}
- Key Libraries: {specific libs to test}

**Time Box:** {1-3 days max}

**Output Location:** `spikes/{spike-name}/`

---

**Confirm this spike plan?**
- [Y] Yes, proceed to code
- [R] Revise plan (specify changes)
- [A] Abandon - question not worth answering
```

### Post-Confirmation Workflow

**AI MUST NOT write code until human confirms spike plan.**

After Confirmation:
1. Create `spikes/{spike-name}/` directory
2. Create `spikes/{spike-name}/SPIKE_PLAN.md` with confirmed requirements
3. Use TodoWrite to track spike tasks:
   ```yaml
   - "Set up spike environment"
   - "Implement minimal test case"
   - "Validate hypothesis"
   - "Document findings"
   ```
4. Write throwaway code
5. Document findings in `spikes/{spike-name}/FINDINGS.md`

---

## Spike Workflow

```
User Request → SPIKE_PLAN Confirmation → Human Approval → Implementation → FINDINGS.md
                      ↑                        ↓
                      └── Revise if needed ────┘
```

**Phase shortcut:** SEED (Phase 1) → **SPIKE CONFIRMATION** → SPIKE IMPLEMENTATION → Findings doc
- Skip Phases 2-7
- No tests required (throwaway code)
- If spike succeeds → Start Phase 1 (new prototype) with proper SDLC

---

## Spike Deliverables

### SPIKE_PLAN.md (Pre-Implementation)

```markdown
# Spike Plan: {spike-name}

**Created:** {date}
**Time Box:** {1-3 days}
**Status:** IN_PROGRESS | COMPLETED | ABANDONED

## Question
{What are we trying to answer?}

## Approach
1. {Step 1}
2. {Step 2}
3. {Step 3}

## Success Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}

## Tech Stack
- {Language/Framework/Libraries}
```

### FINDINGS.md (Post-Implementation)

```markdown
# Spike Findings: {spike-name}

**Completed:** {date}
**Duration:** {actual time}
**Result:** SUCCESS | PARTIAL | FAILURE

## Question Answered
{Restate the question}

## Answer
{Clear answer to the question}

## Evidence
{Code snippets, test results, measurements}

## Recommendation
- [ ] Proceed to full implementation (new Phase 1)
- [ ] Need another spike with different approach
- [ ] Abandon - not feasible

## Learnings
{Key technical insights}

## Next Steps
{If proceeding, what's the recommended approach?}
```

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Jump straight to coding | Confirm spike plan first |
| Exceed 3-day time box | Time-box strictly, extend only with approval |
| Graduate spike to production | Start fresh at Phase 1 with TDD |
| Skip FINDINGS.md | Always document learnings |
| Assume spike answers all questions | Spike answers ONE specific question |

---

**🚨 CRITICAL:** Spikes CANNOT graduate to production. Must restart at Phase 1 with TDD if spike proves feasibility.
