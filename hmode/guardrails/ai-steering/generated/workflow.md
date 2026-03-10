# Workflow Rules

**Version:** 1.0.0  
**Last Updated:** 2025-11-19  
**Rule Count:** 8

## Table of Contents

1. [✅ phase-detection-first](#phase-detection-first)
2. [🚫 no-code-before-phase-8](#no-code-before-phase-8)
3. [⚠️ tdd-phase-8](#tdd-phase-8)
4. [⚠️ progressive-content-complex-artifacts](#progressive-content-complex-artifacts)
5. [⚠️ present-plan-multi-step-tasks](#present-plan-multi-step-tasks)
6. [⚠️ confirmation-protocol-complex-tasks](#confirmation-protocol-complex-tasks)
7. [💡 use-todo-list-complex-tasks](#use-todo-list-complex-tasks)
8. [⚠️ complete-todos-immediately](#complete-todos-immediately)

---

## Rules

### ✅ phase-detection-first

**Level:** ALWAYS
**Category:** workflow

Read .project file to detect current phase before any action

**Rationale:** Phase determines allowed actions, prevents out-of-phase work

**Context:**
- **When:** working in prototype directory, task requires phase knowledge

**Action:**
- **Directive:** require
- **Target:** Read .project for phase detection
- **Message:** "Must detect current phase from .project before proceeding"

**Examples:**

1. **Scenario:** User: 'Implement the authentication feature'
   - ✅ **Correct:** Read .project first to check if in Phase 8 (implementation allowed)
   - ❌ **Incorrect:** Start coding without checking phase (might be in Phase 6 design)

*Approved by: Andrew Hopper on 2025-11-19*

---
### 🚫 no-code-before-phase-8

**Level:** NEVER
**Category:** workflow

Never write implementation code before Phase 8

**Rationale:** 9-phase SDLC ensures design-first, prevents premature implementation

**Context:**
- **When:** writing production code
- **Unless:** spike exception, phase is PHASE_8 or later

**Action:**
- **Directive:** prohibit
- **Target:** Implementation code before Phase 8
- **Message:** "Cannot write code in {current_phase}. Must reach Phase 8 first."

**Examples:**

1. **Scenario:** In Phase 6, user: 'Start coding the API'
   - ✅ **Correct:** Explain must complete Phase 6 design, then Phase 7 tests first
   - ❌ **Incorrect:** Start writing API code in Phase 6

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ tdd-phase-8

**Level:** MUST
**Category:** workflow

Write tests before implementation in Phase 8

**Rationale:** TDD ensures quality, prevents regressions, documents expected behavior

**Context:**
- **When:** implementing features
- **Phases:** PHASE_8_IMPLEMENTATION

**Action:**
- **Directive:** require
- **Target:** Test-first development (TDD)
- **Message:** "Phase 8: Write tests first, then implementation"

**Examples:**

1. **Scenario:** Phase 8, user: 'Implement login feature'
   - ✅ **Correct:** Write login tests first (Phase 7 outputs), then implement
   - ❌ **Incorrect:** Write login code first, then add tests

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ progressive-content-complex-artifacts

**Level:** MUST
**Category:** workflow

Use /progressive-content for complex artifacts

**Rationale:** Stage-gated creation ensures quality, enables user feedback, prevents wasted effort

**Context:**
- **When:** creating detailed presentation, comprehensive documentation, strategic documents
- **Task Types:** New Artifact

**Action:**
- **Directive:** use
- **Target:** /progressive-content workflow (6 stages)
- **Message:** "Complex artifact detected. Using /progressive-content for stage-gated creation."

**Examples:**

1. **Scenario:** User: 'Create a detailed architecture presentation'
   - ✅ **Correct:** Invoke /progressive-content, start Stage 0 seeding
   - ❌ **Incorrect:** Immediately generate full 20-slide presentation

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ present-plan-multi-step-tasks

**Level:** MUST
**Category:** workflow

Present detailed plan for multi-step tasks (3+ operations)

**Rationale:** User sees full approach before execution, can course-correct early

**Context:**
- **When:** multi-step task, multiple files involved, complex workflow
- **Task Types:** Task, New Script

**Action:**
- **Directive:** paraphrase
- **Target:** Multi-step task plan
- **Message:** "Ok, here's my plan:
1. {step1}
2. {step2}...

Btw, {details}

Look good? y/n/f"

**Examples:**

1. **Scenario:** User: 'Refactor all API endpoints to use new error handling'
   - ✅ **Correct:** Present plan: 1. Identify endpoints, 2. Create middleware, 3. Update endpoints, 4. Test
   - ❌ **Incorrect:** Start refactoring without showing plan

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ confirmation-protocol-complex-tasks

**Level:** MUST
**Category:** workflow

Use confirmation protocol for complex/ambiguous tasks

**Rationale:** Air traffic control readback pattern, prevents wrong interpretation

**Context:**
- **When:** complex task, ambiguous request, multiple valid approaches

**Action:**
- **Directive:** paraphrase
- **Target:** Confirmation protocol (paraphrase → options → recommend)
- **Message:** "Request: {paraphrase}

Option A: {approach1}
Option B: {approach2}

Recommend: {choice}

Look good? y/n/f"

**Examples:**

1. **Scenario:** User: 'Make the docs better'
   - ✅ **Correct:** Paraphrase, present options (audit vs add diagrams vs densify), recommend, confirm
   - ❌ **Incorrect:** Immediately start editing docs without clarifying approach

*Approved by: Andrew Hopper on 2025-11-19*

---
### 💡 use-todo-list-complex-tasks

**Level:** SHOULD
**Category:** workflow

Use TodoWrite for tracking complex multi-step tasks

**Rationale:** Demonstrates thoroughness, tracks progress, keeps user informed

**Context:**
- **When:** task has 3+ steps, non-trivial task, user requests todo list

**Action:**
- **Directive:** use
- **Target:** TodoWrite tool for task tracking
- **Alternative:** Skip for single-step trivial tasks

**Examples:**

1. **Scenario:** User: 'Add dark mode, run tests, and build'
   - ✅ **Correct:** Create todo list with 3+ tasks, mark in_progress as working
   - ❌ **Incorrect:** Skip todo list for 1-step trivial task

*Approved by: Andrew Hopper on 2025-11-19*

---
### ⚠️ complete-todos-immediately

**Level:** MUST
**Category:** workflow

Mark todos as completed immediately after finishing

**Rationale:** Real-time progress tracking, accurate status for user

**Context:**
- **When:** using TodoWrite, task completed

**Action:**
- **Directive:** require
- **Target:** Update todo status to completed
- **Message:** "Don't batch completions. Update todo immediately after each task."

**Examples:**

1. **Scenario:** Just finished task 1 of 3
   - ✅ **Correct:** Immediately mark task 1 as completed, move to task 2
   - ❌ **Incorrect:** Wait until all 3 tasks done to batch update

*Approved by: Andrew Hopper on 2025-11-19*

---
