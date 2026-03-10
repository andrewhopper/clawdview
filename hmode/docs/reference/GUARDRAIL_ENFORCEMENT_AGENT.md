# Guardrail Enforcement Agent

<!-- File UUID: a7b4c9d2-e3f6-4a1b-8c5d-2e7f9a3b6c1d -->

**Purpose:** Proactive enforcement agent that monitors and validates adherence to guardrail rules, preventing violations BEFORE they occur rather than auditing after the fact.

**Last Updated:** 2026-02-04

---

## 1.0 OVERVIEW

The Guardrail Enforcement Agent is a preventive system that intercepts AI actions and validates them against the comprehensive rule system in `hmode/guardrails/` before execution. Unlike auditing tools that check after the fact, this agent acts as a gatekeeper, blocking operations that violate guardrails.

**Key Responsibilities:**
1. Validate tech stack choices against approved preferences
2. Verify architectural pattern approvals before use
3. Enforce AI steering rules (NEVER/ALWAYS/MUST constraints)
4. Protect `hmode/guardrails/` files from unauthorized modification
5. Check phase gates before code generation
6. Validate file operations against directory policies
7. Generate preventive warnings with actionable alternatives

**Enforcement Model:** **Gate-Based Prevention** (not post-hoc audit)

---

## 2.0 WHEN TO INVOKE

### 2.1 Trigger Conditions

**Automatic Invocation (Preventive Gates):**
- Before using any library/framework not in tech-preferences
- Before implementing architectural pattern not in architecture-preferences
- Before writing any production code (phase check)
- Before modifying any file in `hmode/guardrails/`
- Before creating files in protected directories
- Before executing destructive operations (delete, force push)

**Manual Invocation:**
- User requests: "check guardrails", "validate rules", "is X approved?"
- Pre-commit validation
- Project initialization (bootstrap guardrails)
- Periodic compliance checks

### 2.2 Invocation Patterns

**Pattern 1: Technology Check (Before Import/Install)**
```python
# Before: npm install prisma
# Check: Is Prisma approved in tech-preferences?

from shared.tools.guardrail_enforce import GuardrailEnforcer

enforcer = GuardrailEnforcer()
result = enforcer.check_technology(
    tech_name="prisma",
    category="orm_query_builders"
)

if result.approved:
    # Proceed with npm install prisma
else:
    # Block and request approval
    enforcer.request_approval(result)
```

**Pattern 2: Architecture Pattern Check**
```python
# Before: Implement event-driven architecture
# Check: Is this pattern approved?

result = enforcer.check_architecture_pattern(
    pattern_name="event-driven-microservices",
    category="architecture_patterns"
)

if not result.approved:
    enforcer.suggest_alternatives(result)
```

**Pattern 3: Phase Gate Check**
```python
# Before: Write implementation code
# Check: Are we in Phase 8+?

result = enforcer.check_phase_gate(
    current_phase=6,
    requested_action="write_code"
)

if result.blocked:
    enforcer.explain_phase_requirements(result)
```

**Pattern 4: File Protection Check**
```python
# Before: Modify hmode/guardrails/tech-preferences/backend.json
# Check: Is modification authorized?

result = enforcer.check_file_protection(
    file_path="hmode/guardrails/tech-preferences/backend.json",
    operation="modify"
)

if result.protected:
    enforcer.request_human_approval(result)
```

---

## 3.0 GUARDRAIL CHECKS

### 3.1 Technology Preferences

**Rule:** Only use approved technologies from `hmode/guardrails/tech-preferences/`.

**Checks:**
- ✅ Technology exists in category file (frontend.json, backend.json, etc.)
- ✅ Technology status is "approved" (not "deprecated" or "experimental")
- ❌ Technology not found in any category file
- ⚠️ Technology marked as "experimental" (warn but allow with confirmation)

**Validation Process:**
1. Load `hmode/guardrails/tech-preferences/index.json` to find category files
2. Search all category files for technology name (fuzzy match)
3. Check status field: approved | deprecated | experimental
4. If not found: Block and request approval
5. If deprecated: Suggest approved alternative
6. If experimental: Warn and require confirmation

**Exit Criteria:** Technology is approved OR human approves exception

**Examples:**
```
REQUEST: "Use Prisma for database access"
CHECK: hmode/guardrails/tech-preferences/backend.json → orm_query_builders
RESULT: ✅ Approved (Prisma listed with status: approved)
ACTION: Proceed

REQUEST: "Install Mongoose for MongoDB"
CHECK: hmode/guardrails/tech-preferences/backend.json → databases
RESULT: ❌ Not found
ACTION: Block, request approval workflow
```

---

### 3.2 Architecture Patterns

**Rule:** Only use approved architectural patterns from `hmode/guardrails/architecture-preferences/`.

**Checks:**
- ✅ Pattern exists in category file (process-patterns.json, design-patterns.json, etc.)
- ✅ Pattern has rank ≥ 1 (approved for use)
- ❌ Pattern not found in any category file
- ⚠️ Pattern has notes/warnings (inform user)

**Validation Process:**
1. Load `hmode/guardrails/architecture-preferences/index.json`
2. Search category files for pattern name (semantic match)
3. Check rank and status fields
4. If not found: Block and suggest similar approved patterns
5. If found: Check for usage notes or constraints

**Exit Criteria:** Pattern is approved OR human approves new pattern

**Examples:**
```
REQUEST: "Use Claude Code CLI child processes for multi-agent orchestration"
CHECK: hmode/guardrails/architecture-preferences/process-patterns.json
RESULT: ✅ Approved (Rank 1, in quickReference)
ACTION: Proceed

REQUEST: "Implement CQRS pattern for event sourcing"
CHECK: hmode/guardrails/architecture-preferences/data-patterns.json
RESULT: ❌ Not found
ACTION: Block, suggest Repository Pattern (approved alternative)
```

---

### 3.3 AI Steering Rules

**Rule:** Enforce NEVER/ALWAYS/MUST/SHOULD rules from `hmode/guardrails/ai-steering/rules/`.

**Constraint Hierarchy (Priority Order):**
1. **NEVER** - Absolute prohibition, no exceptions
2. **ALWAYS** - Absolute requirement, no exceptions
3. **MUST** - Required unless exception conditions met
4. **MUST_NOT** - Prohibited unless exception conditions met
5. **SHOULD** - Recommended, violations trigger warning
6. **SHOULD_NOT** - Discouraged, violations trigger warning
7. **PREFER** - Preferred approach, informational
8. **AVOID** - Discouraged approach, informational

**Validation Process:**
1. Load all rule files from `hmode/guardrails/ai-steering/rules/`
2. Match rules by context (phase, taskType, filePattern, toolInvolved)
3. Evaluate `when` conditions (AND logic)
4. Check `unless` exceptions
5. Apply constraint level priority
6. Generate enforcement action based on directive

**Rule Matching:**
```python
def match_rules(action_context):
    """
    Match AI steering rules to current action context.

    Args:
        action_context: {
            "phase": "PHASE_6_DESIGN",
            "taskType": "Task",
            "operation": "write_code",
            "toolInvolved": "Write",
            "filePattern": "src/**/*.ts"
        }

    Returns:
        List of applicable rules sorted by constraint priority
    """
    matched_rules = []

    for rule in load_all_rules():
        if rule_matches_context(rule, action_context):
            matched_rules.append(rule)

    # Sort by constraint level priority (NEVER → ALWAYS → MUST → ...)
    return sorted(matched_rules, key=constraint_priority)
```

**Exit Criteria:** No NEVER violations, all MUST requirements satisfied

**Examples:**
```
RULE: "no-code-before-phase-8" (NEVER)
ACTION: Write implementation code in Phase 6
RESULT: ❌ BLOCKED
MESSAGE: "Cannot write code in Phase 6 (Design). Must reach Phase 8 first."
OPTIONS: [1] Continue Phase 6 design [2] Advance to Phase 8 [3] Declare SPIKE

RULE: "phase-detection-first" (ALWAYS)
ACTION: Start working on task without reading .project
RESULT: ❌ BLOCKED
MESSAGE: "Must read .project file to detect current phase before proceeding"

RULE: "use-todo-list-complex-tasks" (SHOULD)
ACTION: Start 5-step task without creating todo list
RESULT: ⚠️  WARNING
MESSAGE: "Multi-step task detected. Consider using TodoWrite for progress tracking."
```

---

### 3.4 File Protection

**Rule:** Protect `hmode/guardrails/` directory from unauthorized modification.

**Protected Files/Directories:**
- `hmode/guardrails/tech-preferences/` - All JSON files
- `hmode/guardrails/architecture-preferences/` - All JSON files
- `hmode/guardrails/WRITING_STYLE_GUIDE.md`
- `hmode/guardrails/ai-steering/rules/` - All JSON rule files
- `hmode/guardrails/ai-steering/schema.json` - Rule schema definition
- `CLAUDE.md` (repo root) - Core AI instructions

**Operations Protected:**
- ✅ READ - Always allowed
- ❌ WRITE/MODIFY - Requires human approval
- ❌ DELETE - Requires human approval
- ❌ CREATE (new file) - Requires human approval

**Validation Process:**
1. Intercept all Write/Edit operations
2. Check if target path matches protected patterns
3. If protected: Block and request human approval
4. If approved: Log change in audit trail
5. If denied: Suggest alternative approach

**Approval Workflow:**
```
AI: "Need to add TailwindCSS to frontend.json.

     Change: Add TailwindCSS to frontend.json → styling category
     Rationale: Project requires utility-first CSS framework
     Impact: All future projects can use TailwindCSS without approval

     Approval required to proceed. y/n?"

User: "y"

AI: [Updates file, logs to hmode/guardrails/architecture-preferences/approval-log.json]
```

**Exit Criteria:** Human explicitly approves modification

---

### 3.5 Phase Gates

**Rule:** Enforce SDLC phase gates before phase-specific actions.

**Key Gates:**
1. **Code Writing Gate** - No code before Phase 8 (unless SPIKE)
2. **Persona Gate** - Must confirm persona before Phase 2
3. **Requirements Gate** - Requirements must exist before Phase 8
4. **Design Gate** - Design artifacts before implementation
5. **Test Gate** - Tests before code (TDD in Phase 8)

**Validation Process:**
1. Read `.project` file to detect current phase
2. Load phase requirements from `hmode/docs/processes/PHASE_{N}_{NAME}.md`
3. Check if requested action is allowed in current phase
4. If blocked: Explain why, show phase requirements, offer alternatives
5. If allowed: Check for prerequisite artifacts

**Phase-Action Matrix:**
```
┌──────────┬─────────────────────────────────────────────────┐
│ Phase    │ Allowed Actions                                 │
├──────────┼─────────────────────────────────────────────────┤
│ 1-SEED   │ Ideation, problem definition                    │
│ 2-RSRCH  │ Research, persona inference                     │
│ 3-EXPAN  │ Solution exploration, architecture research     │
│ 4-ANAL   │ Analysis, feasibility checks                    │
│ 5-SELECT │ Solution selection, PRD creation                │
│ 6-DESIGN │ UI/UX design, mockups, architecture diagrams    │
│ 7-TEST   │ Test design, acceptance criteria               │
│ 8-IMPL   │ ✅ CODE WRITING ALLOWED (TDD: tests first)     │
│ 9-REFINE │ Polish, optimization, documentation             │
└──────────┴─────────────────────────────────────────────────┘
```

**Exit Criteria:** Phase requirements satisfied OR SPIKE exception declared

---

### 3.6 Directory Policy

**Rule:** Enforce directory-level policies from `hmode/guardrails/dir_policy.yml`.

**Policies:**
- Root directory hygiene (no loose files)
- Project structure requirements
- File naming conventions
- Protected directory restrictions

**Validation Process:**
1. Load `hmode/guardrails/dir_policy.yml`
2. Check operation against directory rules
3. Enforce file placement restrictions
4. Validate naming conventions

**Exit Criteria:** Operation complies with directory policy

---

## 4.0 ENFORCEMENT WORKFLOW

### 4.1 Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│              GUARDRAIL ENFORCEMENT WORKFLOW                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Intercept Action                                        │
│     - Detect AI operation about to execute                  │
│     - Extract context (phase, tech, pattern, file, etc.)    │
│                                                             │
│  2. Load Applicable Rules                                   │
│     - Tech preferences (if tech selection)                  │
│     - Architecture patterns (if pattern usage)              │
│     - AI steering rules (context matching)                  │
│     - File protection rules (if file operation)             │
│     - Phase gates (if phase-specific action)                │
│                                                             │
│  3. Evaluate Rules                                          │
│     - Match rules by context (when/unless conditions)       │
│     - Sort by constraint level priority                     │
│     - Check for NEVER/ALWAYS violations                     │
│     - Check for MUST requirements                           │
│                                                             │
│  4. Determine Action                                        │
│     ┌────────────────┬────────────────────────────────────┐│
│     │ If NEVER hit   │ ❌ BLOCK - Cannot proceed          ││
│     │ If MUST unmet  │ ❌ BLOCK - Requirements missing    ││
│     │ If SHOULD warn │ ⚠️  WARN - Proceed with caution   ││
│     │ If approved    │ ✅ ALLOW - Proceed                 ││
│     └────────────────┴────────────────────────────────────┘│
│                                                             │
│  5. Generate Response                                       │
│     - BLOCK: Explain violation, show alternatives          │
│     - WARN: Show warning, ask for confirmation             │
│     - ALLOW: Proceed silently or with info message         │
│                                                             │
│  6. Execute or Request Approval                             │
│     - If blocked: Present approval workflow                │
│     - If allowed: Let action proceed                       │
│     - Log decision in audit trail                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Response Formats

**BLOCKED - Technology Not Approved:**
```
❌ BLOCKED: Technology not approved

Requested: Mongoose (MongoDB ODM)
Category: databases → orm_query_builders
Status: Not found in tech-preferences

Approved alternatives:
  [1] Prisma - Universal ORM (RECOMMENDED)
  [2] Drizzle - TypeScript ORM
  [3] Request approval for Mongoose

Options:
  [1] Use Prisma instead
  [2] Use Drizzle instead
  [3] Request human approval for Mongoose
  [4] Cancel operation

Your choice:
```

**BLOCKED - Phase Gate Violation:**
```
❌ BLOCKED: Code writing not allowed in Phase 6

Current Phase: 6 (Design)
Requested Action: Write implementation code
Requirement: Must reach Phase 8 (Implementation)

Phase 6 Activities:
  ✅ Create UI mockups
  ✅ Design architecture diagrams
  ✅ Define component hierarchy
  ❌ Write implementation code (Phase 8 only)

Options:
  [1] Continue Phase 6 design work
  [2] Complete Phase 6 and advance to Phase 7
  [3] Declare SPIKE mode (bypass phases, throwaway code)
  [4] Cancel operation

Your choice:
```

**BLOCKED - File Protection Violation:**
```
❌ BLOCKED: Protected file modification requires approval

File: hmode/guardrails/tech-preferences/backend.json
Operation: MODIFY (add new technology)
Reason: Guardrail files require explicit human approval

Proposed Change:
  Add: "supabase" to backend.json → databases category

Approval Workflow:
  1. Explain rationale for adding Supabase
  2. Present alternatives (PostgreSQL, MySQL already approved)
  3. Request human approval
  4. If approved: Update file + log change
  5. If denied: Use approved alternative

Request approval? y/n:
```

**WARNING - SHOULD Violation:**
```
⚠️  WARNING: Best practice recommendation

Rule: use-todo-list-complex-tasks (SHOULD)
Action: Starting multi-step task without todo list
Severity: WARNING (not blocking)

Detected: Task with 5+ steps
Recommendation: Use TodoWrite tool for progress tracking

Benefits:
  - Demonstrates thoroughness
  - Tracks progress in real-time
  - Keeps user informed of status

Options:
  [1] Create todo list (RECOMMENDED)
  [2] Proceed without todo list
  [3] Skip this warning in future

Your choice:
```

---

## 5.0 INTEGRATION

### 5.1 SDLC Integration

**Phase Transitions:**
```
Before each phase transition:
  1. Run guardrail enforcement check
  2. Verify all phase requirements met
  3. Check for prerequisite artifacts
  4. Only advance if all gates pass
```

**Critical Checkpoints:**
- **Phase 1 → 2:** Persona must be inferred (not TBD)
- **Phase 2 → 3:** Persona must be confirmed by human
- **Phase 6 → 7:** Design artifacts must exist
- **Phase 7 → 8:** Test design must exist
- **Phase 8 → 9:** Code quality gate must pass

### 5.2 Gate Sequence Integration

The guardrail enforcement agent runs BEFORE other gates to ensure foundational compliance:

```
┌─────────────────────────────────────────────────────────────┐
│                    GATE EXECUTION ORDER                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Gate 0: Guardrail Enforcement (FIRST - Preventive)         │
│         - Check tech preferences                            │
│         - Check architecture patterns                       │
│         - Check AI steering rules                           │
│         - Check file protection                             │
│         - Check phase gates                                 │
│                                                             │
│         ⬇️  If approved                                     │
│                                                             │
│  Gate 1: Artifact Library                                   │
│  Gate 2: Golden Repo                                        │
│  Gate 3: Tech Preferences (detailed selection)              │
│  Gate 4: Domain Models                                      │
│  Gate 5: Code Standards                                     │
│  Gate 6: Design System                                      │
│  Gate 7: Information Architecture                           │
│  Gate 8: UX Composition                                     │
│  Gate 9: Infrastructure/SRE                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Principle:** Guardrail enforcement is Gate 0 - it validates BEFORE other gates execute.

### 5.3 Tool Integration

**Pre-action Validation:**
```python
# Before using Write tool
from shared.tools.guardrail_enforce import validate_before_write

@pre_action_hook
def before_write(file_path: str, content: str):
    result = validate_before_write(file_path, content)

    if result.blocked:
        raise GuardrailViolation(result.message)

    if result.warning:
        confirm = ask_user(result.message)
        if not confirm:
            raise UserCancelled()

    # Proceed with write
```

**Pre-commit Integration:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run guardrail enforcement
python hmode/shared/tools/guardrail-enforce.py --pre-commit

if [ $? -ne 0 ]; then
    echo "❌ Guardrail violations detected. Commit blocked."
    exit 1
fi
```

---

## 6.0 AUDIT TRAIL

### 6.1 Logging

**Audit Log Location:** `hmode/guardrails/enforcement-audit.jsonl`

**Log Entry Format:**
```json
{
  "timestamp": "2026-02-04T10:30:00Z",
  "action": "technology_check",
  "technology": "prisma",
  "category": "orm_query_builders",
  "result": "approved",
  "rule_matched": "tech-preferences/backend.json",
  "phase": "PHASE_8_IMPLEMENTATION",
  "project": "proto-001-starbucks-online-ordering"
}
```

**Violation Log Entry:**
```json
{
  "timestamp": "2026-02-04T10:35:00Z",
  "action": "code_write_attempt",
  "phase": "PHASE_6_DESIGN",
  "result": "blocked",
  "rule_violated": "no-code-before-phase-8",
  "severity": "NEVER",
  "message": "Cannot write code in Phase 6",
  "user_choice": "continue_phase_6"
}
```

### 6.2 Approval Tracking

**Approval Log Location:** `hmode/guardrails/architecture-preferences/approval-log.json`

**Approval Entry:**
```json
{
  "timestamp": "2026-02-04T11:00:00Z",
  "type": "technology_addition",
  "technology": "supabase",
  "category": "databases",
  "approved_by": "Andrew Hopper",
  "rationale": "PostgreSQL-based BaaS with auth and real-time built-in",
  "impact": "Available for all future projects",
  "status": "approved"
}
```

---

## 7.0 TOOLS & SCRIPTS

### 7.1 Core Script

**Location:** `hmode/shared/tools/guardrail-enforce.py`

**Usage:**
```bash
# Check technology approval
python hmode/shared/tools/guardrail-enforce.py check-tech --name prisma --category orm

# Check architecture pattern
python hmode/shared/tools/guardrail-enforce.py check-pattern --name event-driven

# Check phase gate
python hmode/shared/tools/guardrail-enforce.py check-phase --phase 6 --action write_code

# Check file protection
python hmode/shared/tools/guardrail-enforce.py check-file --path hmode/guardrails/tech-preferences/backend.json --operation modify

# Pre-commit validation
python hmode/shared/tools/guardrail-enforce.py --pre-commit

# Full project validation
python hmode/shared/tools/guardrail-enforce.py validate --project .
```

### 7.2 Python API

```python
from shared.tools.guardrail_enforce import GuardrailEnforcer

enforcer = GuardrailEnforcer()

# Check technology
result = enforcer.check_technology("prisma", "orm_query_builders")
if not result.approved:
    enforcer.request_approval(result)

# Check architecture pattern
result = enforcer.check_architecture_pattern("event-driven-microservices")
if not result.approved:
    alternatives = enforcer.get_approved_alternatives(result)

# Check AI steering rules
result = enforcer.check_ai_steering_rules(
    context={
        "phase": "PHASE_6_DESIGN",
        "operation": "write_code",
        "toolInvolved": "Write"
    }
)

# Check file protection
result = enforcer.check_file_protection(
    "hmode/guardrails/tech-preferences/backend.json",
    operation="modify"
)
```

---

## 8.0 EXIT CRITERIA

### 8.1 Pass Conditions

**ALLOWED:** Action complies with all guardrails
- ✅ Technology approved OR not tech-related
- ✅ Architecture pattern approved OR not pattern-related
- ✅ No NEVER rule violations
- ✅ All MUST requirements satisfied
- ✅ File operation allowed OR approved
- ✅ Phase gate passed

**ALLOWED WITH WARNING:** Minor violations present
- ✅ Core requirements met
- ⚠️ SHOULD violations present (warnings logged)
- ✅ User confirmed despite warnings

**BLOCKED:** Critical guardrail violation
- ❌ Technology not approved
- ❌ Architecture pattern not approved
- ❌ NEVER rule violated
- ❌ MUST requirement unmet
- ❌ Protected file modification without approval
- ❌ Phase gate failed

### 8.2 Severity Definitions

| Severity | Constraint | Action Required |
|----------|------------|-----------------|
| **NEVER** | Absolute prohibition | Must stop, cannot proceed |
| **ALWAYS** | Absolute requirement | Must satisfy, cannot skip |
| **MUST** | Required unless exception | Must satisfy OR explain exception |
| **SHOULD** | Recommended | Warning logged, can proceed |
| **INFO** | Informational | Informational message only |

---

## 9.0 EXAMPLES

### 9.1 Technology Check Flow

```
USER: "Let's use Prisma for the database layer"

AGENT: [Intercepts before npm install]

GUARDRAIL CHECK:
  1. Load hmode/guardrails/tech-preferences/backend.json
  2. Search orm_query_builders category
  3. Find "prisma" with status: "approved"
  4. Result: ✅ APPROVED

RESPONSE: "✅ Prisma is approved. Proceeding with installation."

ACTION: Continue with npm install prisma
```

### 9.2 Phase Gate Violation

```
USER: "Start implementing the authentication feature"

AGENT: [Intercepts before writing code]

GUARDRAIL CHECK:
  1. Read .project file → phase: 6 (Design)
  2. Check if code writing allowed in Phase 6
  3. Load AI steering rule: no-code-before-phase-8
  4. Result: ❌ BLOCKED

RESPONSE:
  "❌ BLOCKED: Cannot write code in Phase 6 (Design).

   Current Phase: 6 (Design)
   Code Allowed: Phase 8 (Implementation)

   Phase 6 Activities:
     ✅ Design authentication flow diagram
     ✅ Create login/signup mockups
     ✅ Define auth state management
     ❌ Write implementation code (Phase 8 only)

   Options:
     [1] Continue Phase 6 design work
     [2] Advance to Phase 7 (Test Design)
     [3] Declare SPIKE mode (bypass phases)
     [4] Cancel operation

   Your choice:"

USER: "1"

AGENT: "Continuing Phase 6 design work. Let's start with the authentication flow diagram."
```

### 9.3 Protected File Modification

```
USER: "Add Supabase to backend.json"

AGENT: [Intercepts before Write operation]

GUARDRAIL CHECK:
  1. Detect target: hmode/guardrails/tech-preferences/backend.json
  2. Check file protection rules
  3. Result: ❌ PROTECTED - Requires human approval

RESPONSE:
  "❌ BLOCKED: Guardrail file requires approval

   File: hmode/guardrails/tech-preferences/backend.json
   Operation: ADD new technology

   Proposed Change:
     Add: 'supabase' to databases category
     Status: approved
     Rank: 2

   Rationale: PostgreSQL-based BaaS with auth and real-time

   Approval required to proceed. y/n:"

USER: "y"

AGENT:
  1. Update backend.json
  2. Log approval to approval-log.json
  3. Confirm: "✅ Added Supabase to approved technologies."
```

---

## 10.0 RELATED DOCUMENTATION

**Guardrail Files:**
- `hmode/guardrails/README.md` - Guardrails overview
- `hmode/guardrails/tech-preferences/` - Approved technologies
- `hmode/guardrails/architecture-preferences/` - Approved patterns
- `hmode/guardrails/ai-steering/rules/` - AI steering rules
- `hmode/guardrails/ai-steering/schema.json` - Rule schema

**Core Documentation:**
- `hmode/docs/core/GUARDRAILS.md` - Guardrail workflow
- `hmode/docs/core/CRITICAL_RULES.md` - Critical rules (1-4)
- `hmode/docs/core/CONFIRMATION_PROTOCOL.md` - Approval workflow

**Related Agents:**
- `hmode/docs/reference/SOFTWARE_QUALITY_AGENT.md` - Post-hoc quality audit
- `hmode/docs/reference/DESIGN_SYSTEM_SELECTION.md` - Design system enforcement

**Tools:**
- `hmode/shared/tools/guardrail-enforce.py` - Enforcement script (THIS)
- `hmode/shared/tools/pre_code_gate.py` - Pre-code artifact gate
- `hmode/guardrails/ai-steering/rule_engine.py` - Rule matching engine

---

## 11.0 VERSION HISTORY

**v1.0.0** (2026-02-04):
- Initial guardrail enforcement agent specification
- Technology preferences validation
- Architecture pattern enforcement
- AI steering rule engine
- File protection system
- Phase gate enforcement
- Preventive (not audit) model

---

**Status:** Active
**Owner:** AI/Human Partnership
**Review Frequency:** Quarterly or when guardrails evolve
**Integration:** Gate 0 (runs before all other gates)
