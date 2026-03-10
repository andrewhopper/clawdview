### Phase 5: CANDIDATE SELECTION 🎯 (NO CODE)
**Goal:** Choose ONE approach from Phase 4 analysis + validate output/audience alignment
**Output:** `project-management/ideas/proto-name-xxxxx-NNN-selection.md` (1 page max)
**Title:** `# Stage 5 - Candidate Selection`

---

## 🎯 PURPOSE: DECISION POINT - CHOOSE ONE APPROACH

**This is where we commit to a single approach for implementation.**

**Input:** Scored approaches from Phase 4 Analysis
**Output:** Single selected approach with rationale
**Critical:** Everything after this phase builds on this ONE choice

---

## 📋 DELIVERABLES

**Selected Approach:**
- **Approach name:** [Which approach from Phase 3/4]
- **One-sentence summary:** [What this approach does]
- **Rationale:** [Why this was chosen over alternatives]
- **Score from Phase 4:** [Total score]

**Trade-offs Accepted:**
- **Accepting:** [What benefits this approach brings]
- **Sacrificing:** [What we're giving up from other approaches]
- **Risks acknowledged:** [Known risks we're taking on]

**MVP Scope Definition:**
- **Must-have features:** [Core features for first version]
- **Nice-to-have features:** [Can be added later]
- **Out-of-scope features:** [Explicitly not doing]

---

## 🎭 OUTPUT/AUDIENCE VALIDATION (AI generates 3 options)

**After approach selection, validate how we'll deliver it to target audience:**

| Option | Output Format | Audience Fit | Trade-offs |
|--------|---------------|--------------|------------|
| A | CLI + config files | SRE-friendly: scriptable, CI/CD ready | No GUI, requires terminal |
| B | Web dashboard + API | Accessible to non-technical | Hosting required, more complex |
| C | Slack bot + CLI | Hybrid: chat + automation | Two interfaces to maintain |

**AI Recommendation:** [Which delivery option best fits target audience from Phase 2]

**User actions:** `accept`, `reject-regenerate`, `reject-comment: <feedback>`

---

## 🔄 PHASE FLOW CLARIFICATION

```
Phase 4 (ANALYSIS)
  ↓
  All approaches scored and ranked
  ↓
Phase 5 (SELECTION) ← YOU ARE HERE
  ↓
  Human chooses ONE approach
  Define MVP scope
  Validate delivery format
  ↓
Phase 6 (DESIGN)
  ↓
  Design detailed architecture for SELECTED approach ONLY
  No more exploring alternatives
```

---

**Exit:** Single approach selected with clear rationale, MVP scope defined, output/audience alignment validated

