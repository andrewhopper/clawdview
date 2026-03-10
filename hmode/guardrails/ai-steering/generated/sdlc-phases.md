# Sdlc Phases Rules

**Version:** 2.0.0
**Last Updated:** 2026-01-15
**Rule Count:** 20

## Table of Contents

1. [🚫 never-skip-phases](#never-skip-phases)
2. [⚠️ phase-1-seed-requirements](#phase-1-seed-requirements)
3. [⚠️ phase-2-research-before-expansion](#phase-2-research-before-expansion)
4. [⚠️ phase-6-design-deliverables](#phase-6-design-deliverables)
5. [⚠️ phase-7-test-design-before-code](#phase-7-test-design-before-code)
6. [🚫 phase-8-implementation-only](#phase-8-implementation-only)
7. [⚠️ phase-8.5-web-ui-validation](#phase-8.5-web-ui-validation)
8. [⚠️ spike-max-3-days](#spike-max-3-days)
9. [⚠️ divergent-mode-confirmation](#divergent-mode-confirmation)
10. [⚠️ phase-transition-gate-approval](#phase-transition-gate-approval)
11. [✅ update-project-metadata-phase-transition](#update-project-metadata-phase-transition)
12. [🚫 business-stage-required](#business-stage-required)
13. [⚠️ domain-model-gate-phase-6](#domain-model-gate-phase-6)
14. [🚫 spike-requires-confirmation](#spike-requires-confirmation)
15. [⚠️ error-tracker-required-mvp](#error-tracker-required-mvp)
16. [✅ task-management-integration](#task-management-integration)
17. [✅ auto-generate-uml-diagrams](#auto-generate-uml-diagrams)
18. [✅ parallel-task-hints](#parallel-task-hints)
19. [✅ offer-phase-skip-option](#offer-phase-skip-option)
20. [✅ concise-phase-summaries](#concise-phase-summaries)

---

## Rules

### 🚫 never-skip-phases

**Level:** NEVER
**Category:** sdlc

Never skip SDLC phases (1→2→3→4→5→6→7→8→9)

**Rationale:** 9-phase SDLC ensures quality, design-first approach, prevents premature implementation

**Context:**
- **When:** transitioning phases
- **Unless:** spike exception explicitly approved

**Action:**
- **Directive:** prohibit
- **Target:** Phase skipping
- **Message:** "Must complete Phase {N} before Phase {N+1}. Current: {current_phase}"

**Examples:**

1. **Scenario:** User in Phase 3 wants to jump to Phase 8
   - ✅ **Correct:** Explain must complete Phases 4, 5, 6, 7 first. Offer to expedite if needed.
   - ❌ **Incorrect:** Move directly from Phase 3 to Phase 8

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ phase-1-seed-requirements

**Level:** MUST
**Category:** sdlc

Phase 1 SEED must include: concept, problem, opportunity, assumptions, constraints, success criteria

**Rationale:** Seed document ensures clear problem definition before research

**Context:**
- **When:** creating Phase 1 seed
- **Phases:** PHASE_1_SEED

**Action:**
- **Directive:** require
- **Target:** Complete seed.md with all sections
- **Message:** "Phase 1 deliverable: seed.md with 7 required sections"

**Examples:**

1. **Scenario:** User: 'Create new idea for CLI tool'
   - ✅ **Correct:** Generate seed.md with: 1.0 Concept, 2.0 Problem, 3.0 Opportunity, 4.0 Assumptions, 5.0 Constraints, 6.0 Success Criteria, 7.0 Initial Approach Ideas
   - ❌ **Incorrect:** Create incomplete seed with only concept section

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ phase-2-research-before-expansion

**Level:** MUST
**Category:** sdlc

Phase 2 RESEARCH existing solutions before designing new one

**Rationale:** Avoid reinventing wheel, learn from existing solutions, understand trade-offs

**Context:**
- **When:** starting new prototype
- **Phases:** PHASE_2_RESEARCH

**Action:**
- **Directive:** require
- **Target:** Research existing solutions, alternatives, prior art
- **Message:** "Phase 2: Research existing solutions before expanding design"

**Examples:**

1. **Scenario:** Phase 2, building semantic layer tool
   - ✅ **Correct:** Research: Cube.js, dbt, LookML, AWS Glue, existing semantic layer approaches
   - ❌ **Incorrect:** Skip research, immediately expand design in Phase 3

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ phase-6-design-deliverables

**Level:** MUST
**Category:** sdlc

Phase 6 DESIGN must produce: architecture diagram, component breakdown, data models, API contracts

**Rationale:** Detailed design prevents implementation surprises, enables accurate estimation

**Context:**
- **When:** completing Phase 6
- **Phases:** PHASE_6_DESIGN

**Action:**
- **Directive:** require
- **Target:** Complete technical design artifacts
- **Message:** "Phase 6 deliverables: TECHNICAL_DESIGN.md with diagrams, components, data models"

**Examples:**

1. **Scenario:** Completing Phase 6 for API service
   - ✅ **Correct:** Create: System diagram, component breakdown, database schema, API endpoint specs, error handling patterns
   - ❌ **Incorrect:** Skip to Phase 7 with only high-level architecture sketch

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ phase-7-test-design-before-code

**Level:** MUST
**Category:** sdlc

Phase 7 TEST_DESIGN: Write test specifications before implementation

**Rationale:** Test-first mindset ensures testability, clear acceptance criteria

**Context:**
- **When:** preparing for Phase 8
- **Phases:** PHASE_7_TEST_DESIGN

**Action:**
- **Directive:** require
- **Target:** Test specifications, test cases, test data
- **Message:** "Phase 7: Design tests first (what to test, expected behavior)"

**Examples:**

1. **Scenario:** Phase 7 for authentication feature
   - ✅ **Correct:** Write: Login test cases, session test cases, permission test cases, edge cases, test data fixtures
   - ❌ **Incorrect:** Skip Phase 7, write tests during Phase 8 implementation

*Approved by: Andrew Hopper on 2025-11-19*

---
### 🚫 phase-8-implementation-only

**Level:** NEVER
**Category:** sdlc

Never write production code outside Phase 8 (except spikes)

**Rationale:** Ensures design, testing planned before coding. Prevents premature implementation.

**Context:**
- **When:** writing production code
- **Unless:** spike exception, phase is PHASE_8 or later

**Action:**
- **Directive:** prohibit
- **Target:** Production code before Phase 8
- **Message:** "Cannot write production code in {current_phase}. Reach Phase 8 first."

**Examples:**

1. **Scenario:** Phase 6, user asks to 'start coding the API'
   - ✅ **Correct:** Explain: 'Phase 6 is design. Complete design, then Phase 7 tests, then Phase 8 code.'
   - ❌ **Incorrect:** Start writing API implementation code

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ phase-8.5-web-ui-validation

**Level:** MUST
**Category:** sdlc

Web/UI projects must complete Phase 8.5 VALIDATION (E2E tests, screenshots, QA)

**Rationale:** UI projects need visual/interaction validation beyond unit tests

**Context:**
- **When:** project involves web UI, completing Phase 8
- **Phases:** PHASE_8_IMPLEMENTATION

**Action:**
- **Directive:** require
- **Target:** Phase 8.5 validation step before Phase 9
- **Message:** "Web/UI project: Phase 8 → 8.5 (E2E, screenshots, QA) → Phase 9"

**Examples:**

1. **Scenario:** Completed React app implementation
   - ✅ **Correct:** Move to Phase 8.5: Run Playwright E2E tests, capture screenshots, manual QA checklist
   - ❌ **Incorrect:** Skip directly to Phase 9 refinement without validation

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ spike-max-3-days

**Level:** MUST
**Category:** sdlc

SPIKE exceptions limited to 3 days max, throwaway code only

**Rationale:** Spikes are learning tools, not production shortcuts. Time-box prevents scope creep.

**Context:**
- **When:** spike exception requested
- **Phases:** SPIKE

**Action:**
- **Directive:** require
- **Target:** 3-day max timeline, code not merged to main
- **Message:** "Spike: Max 3 days, throwaway code, findings inform design"

**Examples:**

1. **Scenario:** User: 'Quick spike to test feasibility'
   - ✅ **Correct:** Approve 3-day spike, create spike branch, document findings, don't merge code
   - ❌ **Incorrect:** Allow indefinite spike, merge spike code to production

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ divergent-mode-confirmation

**Level:** MUST
**Category:** sdlc

DIVERGENT mode requires confirmation: depth, width, evaluation criteria

**Rationale:** Divergent generates many variants, user must confirm scope and effort

**Context:**
- **When:** entering divergent mode
- **Phases:** DIVERGENT

**Action:**
- **Directive:** confirm
- **Target:** Divergent parameters (depth, width, clustering strategy)
- **Message:** "Divergent mode: Confirm depth (1-3), width (3-5), evaluation criteria"

**Examples:**

1. **Scenario:** User: 'Try 3 different architectures'
   - ✅ **Correct:** Confirm: depth=1, width=3, eval criteria (cost, performance, complexity). Show effort estimate.
   - ❌ **Incorrect:** Immediately generate variants without confirmation

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ phase-transition-gate-approval

**Level:** MUST
**Category:** sdlc

Major phase transitions (3→4, 5→6, 7→8) require user approval

**Rationale:** User approval at gates ensures quality, prevents rushing

**Context:**
- **When:** transitioning to next phase
- **Phases:** PHASE_3_EXPANSION, PHASE_5_SELECTION, PHASE_7_TEST_DESIGN

**Action:**
- **Directive:** confirm
- **Target:** Phase transition with deliverables summary
- **Message:** "Phase {N} complete. Deliverables: {list}. Move to Phase {N+1}? y/n"

**Examples:**

1. **Scenario:** Completed Phase 5 approach selection
   - ✅ **Correct:** Summary: 'Phase 5 complete. Selected: FastAPI + React. Move to Phase 6 design? y/n'
   - ❌ **Incorrect:** Automatically move to Phase 6 without user acknowledgment

*Approved by: Andrew Hopper on 2025-11-19*

---
### ✅ update-project-metadata-phase-transition

**Level:** ALWAYS
**Category:** sdlc

Update .project file on every phase transition

**Rationale:** Accurate .project metadata enables phase detection, tracking

**Context:**
- **When:** transitioning phases

**Action:**
- **Directive:** require
- **Target:** Update .project current_phase, phase_number, updated_at
- **Message:** "Updating .project metadata for phase transition"

**Examples:**

1. **Scenario:** Moving from Phase 6 to Phase 7
   - ✅ **Correct:** Edit .project: current_phase='TECHNICAL_DESIGN'→'TEST_DESIGN', phase_number=6→7, updated_at=now
   - ❌ **Incorrect:** Change phase without updating .project file

*Approved by: Andrew Hopper on 2025-11-19*

---
### 🚫 business-stage-required

**Level:** NEVER
**Category:** sdlc

Never start a project without asking business maturity stage first

**Rationale:** Business stage determines process rigor, documentation requirements, and error tracking needs

**Context:**
- **When:** starting any new project or idea
- **Phases:** PHASE_1_SEED

**Action:**
- **Directive:** prohibit
- **Target:** Skipping business stage question
- **Message:** "Must determine business maturity stage before proceeding. Options: POC, MVP, PMF, Startup, Scaleup, Enterprise"

**Examples:**

1. **Scenario:** User: 'I have an idea for a new app'
   - ✅ **Correct:** Ask: "What is the business maturity stage? [1] POC [2] MVP [3] PMF [4] Startup [5] Scaleup [6] Enterprise"
   - ❌ **Incorrect:** Jump straight to capturing the idea without asking business stage

*Approved by: Andrew Hopper on 2026-01-15*

---
### ⚠️ domain-model-gate-phase-6

**Level:** MUST
**Category:** sdlc

Phase 6 MUST check semantic domain registry before design work

**Rationale:** Reusable domain models ensure consistency, reduce duplication, and leverage existing work

**Context:**
- **When:** entering Phase 6 (Design)
- **Phases:** PHASE_6_DESIGN

**Action:**
- **Directive:** require
- **Target:** Read shared/semantic/domains/registry.yaml, present domain menu, wait for selection
- **Message:** "Phase 6 Entry: Check domain registry for reusable models before designing"

**Examples:**

1. **Scenario:** Starting Phase 6 for e-commerce project
   - ✅ **Correct:** Read registry, present: "Applicable domains: [1] auth (User, Session) [2] email [3] core. Select or create new?"
   - ❌ **Incorrect:** Start designing without checking existing domain models

*Approved by: Andrew Hopper on 2026-01-15*

---
### 🚫 spike-requires-confirmation

**Level:** NEVER
**Category:** sdlc

Never write spike code without confirming requirements and approach first

**Rationale:** Even throwaway code needs clear objectives and success criteria to be useful

**Context:**
- **When:** spike exception requested
- **Phases:** SPIKE

**Action:**
- **Directive:** prohibit
- **Target:** Writing spike code before confirmation
- **Message:** "Spike requires confirmation: Question to answer, proposed approach, success criteria, tech stack, time box"

**Examples:**

1. **Scenario:** User: 'Quick spike to test WebSocket performance'
   - ✅ **Correct:** Present spike plan: Question, approach, success criteria, tech stack, time box. Wait for approval.
   - ❌ **Incorrect:** Start writing WebSocket test code immediately

*Approved by: Andrew Hopper on 2026-01-15*

---
### ⚠️ error-tracker-required-mvp

**Level:** MUST
**Category:** sdlc

Web/UI projects at MVP+ business stage MUST include error tracking

**Rationale:** Production-bound projects need error visibility from day one

**Context:**
- **When:** Phase 8 setup for web projects
- **Phases:** PHASE_8_IMPLEMENTATION
- **Unless:** business_stage is POC

**Action:**
- **Directive:** require
- **Target:** Error tracker integration via /add-observability or skill add-error-tracker
- **Message:** "Error tracking required for MVP+ web projects. Run /add-observability --components=tracker"

**Examples:**

1. **Scenario:** Phase 8 for MVP React application
   - ✅ **Correct:** Include error tracker setup in implementation tasks, run /add-observability
   - ❌ **Incorrect:** Skip error tracking for MVP web project

*Approved by: Andrew Hopper on 2026-01-15*

---
### ✅ task-management-integration

**Level:** ALWAYS
**Category:** sdlc

Use TodoWrite and /flow to track phase deliverables for session resumption

**Rationale:** Persistent task tracking enables session resumption and progress visibility

**Context:**
- **When:** working on any phase deliverables

**Action:**
- **Directive:** require
- **Target:** Write tasks to todostore.json, mark complete as done
- **Message:** "Track phase deliverables with TodoWrite for session resumption"

**Examples:**

1. **Scenario:** Starting Phase 6 design work
   - ✅ **Correct:** Create todos: "Check domain registry", "Design architecture", "Generate UML diagram". Mark complete as done.
   - ❌ **Incorrect:** Work through phase without tracking tasks, lose progress on session end

*Approved by: Andrew Hopper on 2026-01-15*

---
### ✅ auto-generate-uml-diagrams

**Level:** ALWAYS
**Category:** sdlc

Auto-generate UML class diagram after domain model approval

**Rationale:** Visual documentation should be automatic, not manual effort

**Context:**
- **When:** domain model approved in Phase 6
- **Phases:** PHASE_6_DESIGN

**Action:**
- **Directive:** require
- **Target:** Generate docs/diagrams/domain-model.mmd from YAML
- **Message:** "Auto-generating UML class diagram from domain model"

**Examples:**

1. **Scenario:** Domain model approved for user management
   - ✅ **Correct:** Run yaml-to-mermaid.py, create docs/diagrams/domain-model.mmd, confirm generation
   - ❌ **Incorrect:** Proceed to architecture design without generating UML diagram

*Approved by: Andrew Hopper on 2026-01-15*

---
### ✅ parallel-task-hints

**Level:** ALWAYS
**Category:** sdlc

Provide parallelization hints when multiple tasks can run concurrently

**Rationale:** Parallel execution accelerates builds and maximizes efficiency

**Context:**
- **When:** breaking down phase tasks

**Action:**
- **Directive:** require
- **Target:** Mark tasks as PARALLEL or SEQUENTIAL with dependencies
- **Message:** "🔀 PARALLELIZABLE: {task1} + {task2} | ⏳ SEQUENTIAL: {task3} → {task4}"

**Examples:**

1. **Scenario:** Phase 8 implementation breakdown
   - ✅ **Correct:** "🔀 PARALLELIZABLE: API impl + UI impl + Error tracker | ⏳ SEQUENTIAL: Core logic → Feature implementations"
   - ❌ **Incorrect:** List all tasks without parallelization guidance

*Approved by: Andrew Hopper on 2026-01-15*

---
### ✅ offer-phase-skip-option

**Level:** ALWAYS
**Category:** sdlc

Offer skip option at each phase transition (except Phase 1 and 8)

**Rationale:** Flexible middle ground between full SDLC and spike mode

**Context:**
- **When:** transitioning between phases

**Action:**
- **Directive:** require
- **Target:** Present [Y] Proceed [S] Skip [?] Details options
- **Message:** "Phase {N} done. → Phase {N+1}? [Y] Proceed [S] Skip [?] Details"

**Examples:**

1. **Scenario:** Completing Phase 2 Research
   - ✅ **Correct:** "✓ Phase 2 done: Reviewed 3 alternatives. → Phase 3? [Y] [S] [?]"
   - ❌ **Incorrect:** Automatically proceed to Phase 3 without offering skip

*Approved by: Andrew Hopper on 2026-01-15*

---
### ✅ concise-phase-summaries

**Level:** ALWAYS
**Category:** sdlc

Keep phase transition summaries to 3-5 lines max

**Rationale:** Reduce screen clutter, faster progression, details on demand

**Context:**
- **When:** completing any phase

**Action:**
- **Directive:** require
- **Target:** Brief summary format with expand option
- **Message:** "✓ Phase {N} done: {1-line}. → Phase {N+1}: {5 words}. [Y] [S] [?]"

**Examples:**

1. **Scenario:** Completing Phase 6 Design
   - ✅ **Correct:** "✓ Phase 6 done: Architecture + API contracts defined. → Phase 7: Design test cases [Y] [S] [?]"
   - ❌ **Incorrect:** Multi-paragraph summary of all design decisions, full file listings, detailed explanations

*Approved by: Andrew Hopper on 2026-01-15*

---
