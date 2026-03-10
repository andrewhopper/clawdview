## 📋 9-PHASE SDLC (with Phase 2.5 & 8.5 Validation Gates)

**Project Types:**
| Type | Phase 2.5 | Description |
|------|-----------|-------------|
| **exploration** | Skip | Learning, idea exploration, curiosity-driven |
| **prototype** | Skip | Quick validation, POC, small/hobby projects |
| **production** | Required | Serious projects intended for real use/users |
| **brownfield** | N/A | Bug fixes, features, refactoring on existing code |

---

### 🏢 BUSINESS MATURITY STAGE (MANDATORY)

**BEFORE Phase 1 or declaring any project type, AI MUST ask:**

```markdown
What is the business maturity stage for this project?

[1] POC (Proof of Concept) - Validating technical feasibility
[2] MVP (Minimum Viable Product) - First customer-ready version
[3] PMF (Product-Market Fit) - Validated, starting to scale
[4] Startup (Early-stage) - Seed to Series A, iterating fast
[5] Scaleup (Growth-stage) - Series B-D, proven model scaling
[6] Enterprise (Mature) - Large org (1000+ employees), formal processes
```

**Business Stage Impact on Process:**

| Stage | Phase 2.5 | Phase 5.5 PRD | Error Tracking | Monitoring | Documentation |
|-------|-----------|---------------|----------------|------------|---------------|
| POC | Optional | Skip | Optional | Basic | Minimal |
| MVP | Recommended | Lightweight | Required | Basic | Core docs |
| PMF | Required | Required | Required | Full | Full docs |
| Startup | Required | Required | Required | Full | Full docs |
| Scaleup | Required | Formal | Required | Full + SLAs | Comprehensive |
| Enterprise | Required | Formal | Required | Full + SLAs | Comprehensive |

**Store in `.project`:**
```yaml
business_stage: poc | mvp | pmf | startup | scaleup | enterprise
business_stage_selected_at: 2025-01-15T10:00:00Z
```

**NEVER skip this question - it determines process rigor throughout the project.**

---

### 🚀 FLEXIBLE PHASE SKIPPING

**At each phase transition, offer skip option:**

```
Phase {N} complete. → Phase {N+1}?
[Y] Yes, proceed
[S] Skip Phase {N+1}
[?] Explain Phase {N+1}
```

**Skip Tracking (store in `.project`):**
```yaml
phases_skipped: [2, 5.5]  # List of skipped phases
skip_reasons:
  phase_2: "Existing solution already researched"
  phase_5.5: "POC - formal PRD not needed"
```

**Skip Restrictions:**
| Phase | Skippable? | Condition |
|-------|------------|-----------|
| 1 SEED | ❌ No | Always required |
| 2 RESEARCH | ✅ Yes | If prior research exists |
| 2.5 FEASIBILITY | ✅ Yes | Non-production or POC |
| 3 EXPANSION | ✅ Yes | Only one obvious approach exists |
| 4 ANALYSIS | ✅ Yes | If only exploring one approach (skip 3 instead) |
| 5 SELECTION | ✅ Yes | Only one approach explored (skip 3 instead) |
| 5.5 PRD | ✅ Yes | POC/MVP or exploration |
| 6A APP DESIGN | ❌ No | MUST define what the app does |
| 6B INFRA DESIGN | ⚠️ Rare | Only if no deployment needed (very rare) |
| 7 TEST_DESIGN | ✅ Yes | POC only |
| 8 IMPL | ❌ No | Core phase |
| 8.5 VALIDATION | ✅ Yes | Non-web or POC |
| 9 REFINEMENT | ✅ Yes | If MVP sufficient |

---

### 📝 CONCISE PHASE SUMMARIES

**Keep phase transitions brief (3-5 lines max):**

```
✓ Phase {N} done: {1-line summary}
→ Phase {N+1}: {purpose in 5 words}
[Y] Proceed [S] Skip [?] Details
```

**Example:**
```
✓ Phase 2 done: Reviewed 3 alternatives, none fit.
→ Phase 3: Expand solution approaches
[Y] Proceed [S] Skip [?] Details
```

**Verbose mode:** User can request `[?] Details` for full explanation.

---

**Standard Path:**
```
1. SEED → 2. RESEARCH
   ↓
   ├─→ 2.5 FEASIBILITY (production only: go/no-go gate)
   │    ↓
   └─→ 3. EXPANSION (explore 5-10 approaches) → 4. ANALYSIS (compare approaches) → 5. SELECTION (choose ONE)
   ↓
   ├─→ 5.5 REQUIREMENTS & PRD (production only: formal documentation)
   │    ↓
   └─→ 6A. APPLICATION DESIGN (features, UI, business logic) → 6B. INFRASTRUCTURE DESIGN (AWS, deployment, monitoring) → 7. TEST_DESIGN
   ↓
8. IMPLEMENTATION (create startup script)
   ↓
   ├─→ 8.5 QUALITY_VALIDATION (Web/UI: screenshots + validation report)
   │    ↓
   └─→ 9. REFINEMENT (UAT + polish)

Skip 2.5 for: exploration, prototype project types
Skip 5.5 for: exploration, spike project types (optional for prototype)
Skip 6B for: pure application prototypes without deployment (rare)
Skip 8.5 for: CLIs, APIs, libraries, backend services
```

**Divergent Path:**
```
1-2 → (2.5 if production) → 3-5 → (5.5 if production) → 6A-6B-7 → 8.1 DIVERGENT_IMPL → 8.2 DIVERGENT_EVAL → 8.3 CONVERGENCE → (optional 8.5) → 9
```

**Key Requirements:**
- **Phase 2.5:** Production projects MUST validate feasibility before Phase 3
- **Phase 5.5:** Production projects MUST document requirements/PRD before Phase 6 (optional for prototype, skip for exploration/spike)
- **Phase 6A:** ALL projects MUST design application (features, UI, business logic) before Phase 6B
- **Phase 6B:** ALL projects MUST design infrastructure (AWS, deployment, monitoring) before Phase 7
- **Phase 8:** ALL projects create startup script (starts services + seeds data)
- **Phase 8.5:** Web/UI projects MUST validate with Playwright (screenshots + accessibility)
- **Phase 9:** Fix Phase 8.5 issues, UAT automation, polish

**Phase 2.5 Feasibility Criteria:**
1. Technical feasibility - Can this be built?
2. Effort justification - Build vs buy?
3. Differentiation - What's unique?
4. Longevity - Still useful in 1 year?
5. Target audience - Who benefits? TAM?
6. Risk assessment - Blockers/unknowns?

**Phase 2.5 Decisions:** PROCEED | CONDITIONAL | SPIKE | ABANDON

**Phase 5.5 Requirements & PRD:**
- **Purpose:** Document formal requirements, PRD, acceptance criteria
- **Skip:** exploration, spike (optional for prototype, required for production)
- **Deliverables:** PRD.md, REQUIREMENTS.md, ACCEPTANCE_CRITERIA.md
- **Duration:** 2-4 hours (production), 0 hours (skipped)
- **Gate:** Human approval before Phase 6

---

### 📊 SEMANTIC DOMAIN MODEL GATE (MANDATORY)

**EVERY project with data entities MUST check domain models at Phase 6.**

**🤖 USE DOMAIN-MODELING-SPECIALIST AGENT:**

For any domain modeling work, delegate to the specialized agent:
```bash
# Invoke the domain-modeling-specialist agent
Task(subagent_type="domain-modeling-specialist",
     prompt="Discover applicable domains and create data models for {project}")
```

**Domain Model Workflow:**

```
Phase 6 (DESIGN) Entry:
1. Invoke domain-modeling-specialist agent
2. Agent reads registry: hmode/hmode/shared/semantic/domains/registry.yaml
3. Agent presents domain menu with relevance scores
4. Wait for human selection
5. If new domain needed → agent researches (schema.org, GitHub, APIs)
6. Agent generates domain model YAML in shared/domain-models/{project}/
7. Wait for human approval
8. Agent AUTO-GENERATES documentation (UML diagrams)
9. ONLY then proceed to architecture design
```

**Mandatory Domain Check Prompt:**

```markdown
## Domain Model Gate - Phase 6

Before designing architecture, let's identify reusable domain models.

### Applicable Existing Domains:
| # | Domain | Version | Relevance | Key Entities |
|---|--------|---------|-----------|--------------|
| 1 | auth | 1.0.0 | High | User, Session, Permission |
| 2 | email | 1.0.0 | Medium | Email, Attachment |
| 3 | core | 1.0.0 | High | TimePoint, Money, Address |

**Select domains to use:** (e.g., "1,3" or "none")

**New domains needed?** [Y/n] - I'll research and propose
```

**If domain selected or created:**
1. Import from `@hopperlabs/semantic/domains/{domain}/`
2. Generate YAML models in `shared/domain-models/{project}/`
3. Present for human approval
4. **AUTO-GENERATE UML class diagram** → `docs/diagrams/domain-model.mmd`

**Auto-Documentation Output:**

```
✓ Domain model created: shared/domain-models/{project}/models.yaml
✓ UML class diagram generated: docs/diagrams/domain-model.mmd
✓ Domain registry updated with dependencies
```

**See:**
- `@processes/DOMAIN_MODEL_SOP` for detailed workflow documentation
- `hmode/agents/domain-modeling-specialist.md` for agent specification
- Use Task tool with `subagent_type="domain-modeling-specialist"` to invoke

---

### 📋 TASK MANAGEMENT INTEGRATION (REQUIRED)

**Use TodoWrite and /flow throughout SDLC to:**
1. Track phase deliverables as tasks
2. Write tasks to disk for session resumption
3. Identify parallelization opportunities

**Phase Task Templates:**

```yaml
# Phase 1 - SEED Tasks
- "Capture idea in seed.md"
- "Define problem statement"
- "Identify target audience"
- "Generate review site"

# Phase 6 - DESIGN Tasks (CAN PARALLELIZE)
- "Check domain registry for existing models"      # Parallel
- "Review golden repos for starting point"         # Parallel
- "Design component architecture"                  # Sequential (depends on above)
- "Generate UML class diagram"                     # Sequential (depends on domain)
- "Define API contracts"                           # Parallel with UML

# Phase 8 - IMPLEMENTATION Tasks (CAN PARALLELIZE)
- "Setup project structure from golden repo"       # First
- "Implement core domain logic"                    # Sequential
- "Implement API endpoints"                        # Parallel after core
- "Implement UI components"                        # Parallel after core
- "Add error tracking integration"                 # Parallel
- "Write unit tests"                              # Parallel with impl
```

**Session Resumption:**
- Tasks persist in `.todostore.json` (project-local) or `.system/todostore.json` (global)
- On session resume: read todostore, show pending tasks, continue

**Parallelization Hints:**
```
🔀 PARALLELIZABLE: Domain check + Golden repo search + Research
🔀 PARALLELIZABLE: API impl + UI impl + Error tracker integration
🔀 PARALLELIZABLE: Unit tests + Integration tests + E2E tests
⏳ SEQUENTIAL: Domain model → UML diagram → Architecture design
⏳ SEQUENTIAL: Core logic → Feature implementations
```

---

### 🔧 DEFAULT PROJECT REQUIREMENTS

**ALL web/UI projects (MVP+ business stage) MUST include:**

| Requirement | When | How |
|-------------|------|-----|
| **Error Tracking** | Phase 8 setup | `/add-observability --components=tracker` or skill `add-error-tracker` |
| **Buildinfo.json** | Build step | `hmode/shared/tools/generate-buildinfo.py` |
| **Smoke Tests** | Post-deploy | Verify git hash matches deployed version |

**Error Tracker Integration Checklist:**

```markdown
## Pre-Implementation Checklist (Phase 8 Entry)

- [ ] Project is web/UI type (React, Next.js, Vite, HTML)
- [ ] Business stage is MVP or higher
- [ ] Error tracker endpoint configured in .env
- [ ] Error tracker initialized in app entry point
- [ ] Error boundary component added (React projects)

**If checklist incomplete:**
"Error tracking is required for MVP+ web projects.
Run `/add-observability --components=tracker` or provide justification to skip."
```

---

## 📋 9-PHASE SDLC

### 🎭 SDLC AGENT TAXONOMY

**Purpose:** Define types of participants (human or AI) in development process

**Agent Types:**

| Type | Role | Responsibilities | Phase Activity | Example |
|------|------|-----------------|----------------|---------|
| **Planners** | Define roadmap, prioritize work | Create phase plans, sequence tasks, estimate effort | Phases 1-6 | AI generates implementation plan, human prioritizes features |
| **Designers** | Define solutions, make trade-offs | Explore approaches, evaluate options, select direction | Phases 3-5 | AI generates 5-10 approaches, human selects winner |
| **Architects** | Design systems, define structure | Create architecture, design APIs, plan data models | Phase 6 | AI drafts ARCHITECTURE.md, human approves strategy |
| **Evaluators** | Judge quality, score proposals | Evaluate through multiple lenses (persona, security, performance) | Phases 5-9 | `/eval` command with persona lens scores design at Phase 6→7 gate |
| **Approvers** | Gate-keep transitions, enforce quality | Block phase transitions if quality gates fail | Phase transitions | CISO persona must score ≥70 for Phase 6→7 |
| **Builders** | Implement code, write tests | Write implementation to pass tests (TDD) | Phases 7-8 | AI writes tests (Phase 7), then code (Phase 8) |
| **Observers** | Monitor progress, track metrics | Watch builds, test runs, deployments | Phases 7-9 | CI/CD monitors test pass rates, coverage |
| **Actors** | Execute workflows, run automation | Trigger builds, deploy code, run scripts | Phases 7-9 | GitHub Actions runs Playwright tests |

**Integration with proto-046 (LLM Judge):**
- **Evaluators** implemented via `/eval` command (proto-046)
- **Persona lens:** Simulate stakeholder feedback (PM, CISO, CFO) with 6D model
- **Stage gates:** Use evaluator scores (0-100) to block phase transitions
- **Multi-lens:** Security, performance, accessibility lenses beyond personas
- **Example:** Phase 6→7 gate requires security lens ≥80 AND CISO persona ≥70

**Human vs AI Assignment:**

| Agent Type | Human | AI | Hybrid |
|------------|-------|----|----|
| **Planners** | Prioritize business value | Generate task breakdowns | ✅ Human prioritizes, AI sequences |
| **Designers** | Make strategic choices | Generate approaches | ✅ AI expands, human selects |
| **Architects** | Approve strategies | Draft architectures | ✅ AI proposes, human approves |
| **Evaluators** | Define quality standards | Score against standards | ✅ AI judges via LLM, human sets thresholds |
| **Approvers** | Final sign-off | Automated gates | ✅ AI blocks on quality, human overrides |
| **Builders** | Review code | Write code + tests | ✅ AI implements, human reviews |
| **Observers** | Interpret metrics | Collect metrics | ✅ AI monitors, human reacts |
| **Actors** | Trigger workflows | Execute workflows | ✅ Human initiates, AI executes |

**Evaluator Workflow (proto-046):**

```bash
# Phase 6→7 gate: Evaluator (AI CISO persona) judges security design
/eval --lens=persona --role=ciso --adoption=early-adopter --lifecycle=early \
  --motivation=company --risk=low --thinking=detail --threshold=70 \
  "design/SECURITY_DESIGN.md"

# Output: {score: 85, status: "PASSED"} → Approver (AI gate) allows Phase 7
# If score < 70 → Approver blocks, requires fixes

# Phase 8→9 gate: Multi-evaluator (security + performance lenses)
/eval --lens=security --threshold=80 "src/"
/eval --lens=performance --threshold=75 "src/"

# Both must pass for Approver to allow Phase 9
```

**Why This Matters:**
- **Clarity:** Explicit roles prevent confusion (who judges vs who approves?)
- **Automation:** AI can fill roles systematically (Evaluators via `/eval`, Builders via code gen)
- **Quality:** Multiple evaluator lenses catch different issues (security, performance, personas)
- **Accountability:** Clear handoffs (Designer selects approach → Architect approves → Evaluator scores → Approver gates)

---

### ⚡ SPIKE EXCEPTION: Skip to Implementation

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

### 🚦 SPIKE REQUIREMENTS CONFIRMATION (MANDATORY)

**BEFORE writing ANY spike code, AI MUST confirm requirements and approach:**

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

**AI MUST NOT write code until human confirms spike plan.**

**After Confirmation:**
1. Create `spikes/{spike-name}/` directory
2. Create `spikes/{spike-name}/SPIKE_PLAN.md` with confirmed requirements
3. Use TodoWrite to track spike tasks
4. Write throwaway code
5. Document findings in `spikes/{spike-name}/FINDINGS.md`

---

**Phase shortcut:** SEED (Phase 1) → **SPIKE CONFIRMATION** → SPIKE IMPLEMENTATION → Findings doc
- Skip Phases 2-7
- No tests required (throwaway code)
- If spike succeeds → Start Phase 1 (new prototype) with proper SDLC

**🚨 CRITICAL:** Spikes CANNOT graduate to production. Must restart at Phase 1 with TDD if spike proves feasibility.

---


---

### 🔧 BROWNFIELD WORKFLOW (Existing Projects)

**What is Brownfield?** Development work on existing codebases, not new projects.

**When to use:**
- Bug fixes (standard or critical hotfix)
- New features on existing projects
- Refactoring/code improvement
- Technical debt reduction
- Performance optimization
- Security patches

**Phase Flow:**

```
Brownfield Phases (vs. Greenfield 9-phase SDLC):

HOTFIX:    0 (Assess) ──────────────────────→ 8 → 9
BUG_FIX:   0 (Assess) ────────────→ 7 (Test) → 8 → 9
FEATURE:   0 (Assess) → 3 → 5 → 6 → 7 (Test) → 8 → 9
REFACTOR:  0 (Assess) ────────────→ 7 (Test) → 8 → 9
```

**Phase 0: ASSESSMENT (Brownfield Entry)**
- Understand affected code areas
- Assess test coverage
- Identify impact and risks
- Classify work type

**Key Differences from Greenfield:**

| Aspect | Greenfield | Brownfield |
|--------|------------|------------|
| Starting point | Blank slate | Existing code |
| Code allowed | Phase 8 only | After Phase 0 |
| Tests | Write all new | Wrap existing + add new |
| Architecture | Design from scratch | Work within existing |
| SEED phase | Required | Skip |

**Routing to Brownfield:**
1. User references existing project name
2. `.project` file exists and phase >= 8 (production)
3. Code already exists in target directory
4. Keywords: "fix bug", "existing project", "add feature to", "refactor"

**See:**
- `@processes/BROWNFIELD_ENTRY` - Full brownfield workflow
- `@processes/HOTFIX_WORKFLOW` - Critical production fixes
- `@processes/MAINTENANCE_TRIAGE` - Issue classification

