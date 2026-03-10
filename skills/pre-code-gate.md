---
name: pre-code-gate
description: Enforces requirements → mockups → data model → code sequence
version: 1.0.0
aliases:
  - requirements-first
  - no-code-yet
---
<!-- File UUID: 8b2d4f6a-9c1e-5a7b-3d9f-2e4a6b8c0d1e -->

# Pre-Code Gate Enforcement

**CRITICAL: This gate MUST trigger before ANY code is written.**

## Purpose

Prevents AI from jumping straight to code by enforcing this sequence:
1. ✅ Requirements documented
2. ✅ Low-fidelity mockups created
3. ✅ Data model defined
4. ✅ THEN code

## Trigger Detection

**Block code writing when ANY of these are detected:**

### Code Patterns to Block
```
- import statements (Python, JS, TS)
- function definitions
- class definitions
- React components
- API routes
- Database schemas (as code)
- Infrastructure as code (CDK, Terraform)
```

### Exceptions (Allow immediately)
```
- README files
- Documentation
- Requirements documents
- Design documents
- Low-fi mockups (HTML with placeholder content)
- Data model YAML (semantic domain models)
- Test files (Phase 7 only)
```

## Enforcement Flow

```
User requests feature/implementation
         ↓
    [GATE CHECK]
         ↓
    ┌─────────────────┐
    │ Phase Check     │
    │ Is phase >= 8?  │
    └────┬─────┬──────┘
         │     │
         NO   YES
         │     └─→ Check artifacts exist
         │             ↓
         │         ┌──────────────────────┐
         │         │ Artifact Check       │
         │         │ 1. Requirements doc? │
         │         │ 2. Mockups exist?    │
         │         │ 3. Data model def?   │
         │         └───┬──────────┬───────┘
         │             │          │
         │            ALL        MISSING
         │           EXIST       SOME
         │             │          │
         │             ↓          ↓
         │      [ALLOW CODE]  [BLOCK CODE]
         │                        │
         ↓                        ↓
    [BLOCK CODE]          [CREATE ARTIFACTS]
         │                        │
         ↓                        ↓
    Show phase sequence      Guide through phases
    Offer advancement        Create missing artifacts
```

## Blocking Response Template

When code is requested but phase < 8 or artifacts missing:

```
❌ Cannot write code yet - missing required artifacts

Current phase: {phase_number} ({phase_name})
Code allowed in: Phase 8 (Implementation)

Required before coding:
  [ ] Requirements documented
  [ ] Low-fidelity mockups
  [ ] Data model defined

What's missing:
  {list_missing_artifacts}

Options:
  [1] Create requirements document
  [2] Create low-fi mockups
  [3] Define data model
  [4] Complete all three in sequence
  [5] Declare SPIKE mode (skip phases, throwaway code)

Your choice:
```

## Artifact Requirements

### 1. Requirements Document

**What it must contain:**
- User stories (As a {user}, I want {goal}, so that {benefit})
- Acceptance criteria
- Functional requirements
- Non-functional requirements (performance, security)
- Out of scope (explicitly stated)

**Format:** Markdown file in project root or docs/
**File naming:** `REQUIREMENTS.md` or `requirements/{feature-name}.md`

**Example structure:**
```markdown
# Requirements: {Feature Name}

## User Stories
1. As a {user type}, I want to {action}, so that {benefit}

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Functional Requirements
FR1. System shall...
FR2. User can...

## Non-Functional Requirements
NFR1. Performance: Response time < 2s
NFR2. Security: Auth required for all endpoints

## Out of Scope
- Feature X (future phase)
- Integration Y (not needed yet)
```

### 2. Low-Fidelity Mockups

**What qualifies as low-fi:**
- Wireframes (boxes and labels, no styling)
- ASCII art diagrams
- Simple HTML with placeholder content
- Figma/Excalidraw sketches (exported as images)
- Paper sketches (photographed)

**What does NOT qualify:**
- High-fidelity designs (actual styling)
- Production-ready components
- Full React implementations

**Format:** HTML, PNG, ASCII in docs/ or mockups/
**File naming:** `mockups/{feature-name}-{view}.html` or `.png`

**Example low-fi HTML:**
```html
<!-- Low-fi mockup: User Dashboard -->
<!DOCTYPE html>
<html>
<head><title>Dashboard Mockup</title></head>
<body>
  <h1>User Dashboard</h1>

  <div style="border: 1px solid black; padding: 10px; margin: 10px;">
    <h2>User Profile Card</h2>
    <p>[Avatar placeholder]</p>
    <p>Name: [User Name]</p>
    <p>Email: [user@email.com]</p>
  </div>

  <div style="border: 1px solid black; padding: 10px; margin: 10px;">
    <h2>Activity Feed</h2>
    <ul>
      <li>[Activity item 1]</li>
      <li>[Activity item 2]</li>
    </ul>
  </div>

  <button>[Log Out Button]</button>
</body>
</html>
```

### 3. Data Model Definition

**What it must contain:**
- Entity definitions
- Field types
- Relationships
- Validation rules
- Timestamps (created_at, updated_at)

**Format:** YAML in `hmode/hmode/shared/semantic/domains/{domain}/`
**File naming:** `{entity-name}.yaml`

**Must follow:** `hmode/hmode/shared/semantic/domains/DOMAIN_MODEL_SOP.md`

**Example data model:**
```yaml
# hmode/hmode/shared/semantic/domains/user-management/user.yaml
entity: User
description: Application user with authentication

fields:
  id:
    type: uuid
    required: true
    primary_key: true

  email:
    type: email
    required: true
    unique: true
    validation: RFC5322

  name:
    type: string
    required: true
    max_length: 100

  role:
    type: enum
    values: [admin, user, guest]
    default: user

  created_at:
    type: timestamp
    required: true
    auto: true

  updated_at:
    type: timestamp
    required: true
    auto: true

relationships:
  posts:
    type: one_to_many
    target: Post
    cascade_delete: true

indices:
  - fields: [email]
    unique: true
  - fields: [created_at]
```

## Verification Checklist

Before allowing code, verify ALL of these:

```python
def can_write_code(project_path: Path) -> tuple[bool, list[str]]:
    """
    Check if all artifacts exist before allowing code.

    Returns:
        (can_proceed, missing_artifacts)
    """
    missing = []

    # 1. Check phase
    project_file = project_path / '.project'
    if not project_file.exists():
        missing.append("No .project file - unknown phase")
        return (False, missing)

    phase = parse_phase(project_file)
    if phase < 8:
        missing.append(f"Phase {phase} - code allowed in Phase 8+")

    # 2. Check requirements
    req_files = [
        project_path / 'REQUIREMENTS.md',
        project_path / 'docs' / 'requirements.md',
        project_path / 'requirements'
    ]
    if not any(f.exists() for f in req_files):
        missing.append("Requirements document")

    # 3. Check mockups
    mockup_dirs = [
        project_path / 'mockups',
        project_path / 'docs' / 'mockups',
        project_path / 'design'
    ]
    has_mockups = any(
        d.exists() and list(d.glob('*.[html|png|jpg]'))
        for d in mockup_dirs
    )
    if not has_mockups:
        missing.append("Low-fidelity mockups")

    # 4. Check data model
    domain_path = Path('hmode/shared/semantic/domains')
    # Check if project references any domains
    # OR has local data model definitions
    local_models = [
        project_path / 'data-model.yaml',
        project_path / 'models' / '*.yaml',
        project_path / 'docs' / 'data-model.yaml'
    ]
    has_model = (
        any(f.exists() for f in local_models) or
        check_domain_references(project_file)
    )
    if not has_model:
        missing.append("Data model definition")

    can_proceed = len(missing) == 0
    return (can_proceed, missing)
```

## Integration with SDLC Phases

### Phase Mapping
```
Phase 1 (SEED)          → Idea documented
Phase 2 (RESEARCH)      → Research existing solutions
Phase 3 (EXPANSION)     → ✅ REQUIREMENTS created here
Phase 4 (ANALYSIS)      → Analyze approaches
Phase 5 (SELECTION)     → Select approach
Phase 6 (DESIGN)        → ✅ MOCKUPS created here
                        → ✅ DATA MODEL created here
Phase 7 (TEST_DESIGN)   → Write tests (NOT implementation)
Phase 8 (IMPL)          → ✅ CODE allowed here
Phase 9 (REFINEMENT)    → Polish and refine
```

### Automatic Artifact Creation

When user advances to these phases, automatically create artifacts:

**Phase 3 (Expansion):**
```
→ Create REQUIREMENTS.md template
→ Fill in user stories from Phase 1-2 context
→ Prompt user to confirm/edit
→ Save before proceeding
```

**Phase 6 (Design):**
```
→ Create mockups/ directory
→ Generate low-fi HTML mockups from requirements
→ Prompt user to review
→ Create data model YAMLs
→ Save before proceeding
```

**Phase 7 (Test):**
```
→ Write tests based on acceptance criteria
→ NO implementation code yet
→ Tests should fail (no implementation exists)
```

**Phase 8 (Implementation):**
```
→ NOW code is allowed
→ Implement to make tests pass
→ Reference requirements & mockups
```

## Edge Cases

### User explicitly requests code

**User says:** "Just write the code, skip the planning"

**Response:**
```
I understand you want code quickly. Two options:

[1] SPIKE mode (fast but throwaway)
    - Skip phases 2-7
    - Max 3 days of work
    - Code will be prototype quality
    - Expect to rebuild later

[2] Proper SDLC (slower but quality)
    - Create requirements (~5 min)
    - Create mockups (~10 min)
    - Define data model (~10 min)
    - Then write code
    - Total: +25 min, but better outcome

Which do you prefer?
```

### Requirements already exist elsewhere

**User says:** "The requirements are in the Slack thread / email / doc"

**Response:**
```
I see requirements exist, but I need them in the repo.

Quick options:
[1] Copy-paste the Slack thread here
    → I'll extract requirements into REQUIREMENTS.md

[2] Share the Google Doc link
    → I'll read and convert to REQUIREMENTS.md

[3] You create REQUIREMENTS.md
    → I'll wait then proceed

Which works best?
```

### Simple changes to existing code

**User says:** "Just add a console.log for debugging"

**Response:**
```
✅ Small debug changes OK (no gate required)

[Proceeds with change]
```

**Criteria for bypassing gate:**
- < 5 lines of code
- Existing file (not creating new file)
- Debug/logging only (no logic changes)
- Explicitly requested by user

## Success Metrics

Track gate effectiveness:

```yaml
pre_code_gate_stats:
  total_code_requests: 100
  blocked_requests: 45
  spike_mode_chosen: 10
  proper_sdlc_followed: 35
  gate_bypassed_valid: 10  # Debug changes, etc.

  avg_time_to_artifacts: 15min  # Time to create req + mock + model

  quality_improvement:
    bugs_caught_in_design: 12  # Issues found during mockup review
    requirements_clarified: 8   # Unclear requirements discovered
    data_model_issues: 5        # Model problems caught early
```

## Configuration

### Per-Project (.project file)

```yaml
pre_code_gate:
  enabled: true
  strict_mode: true  # Never allow bypass

  artifact_locations:
    requirements: 'REQUIREMENTS.md'
    mockups: 'mockups/'
    data_model: 'models/'
```

### Global (~/.claude/settings.json)

```json
{
  "pre_code_gate": {
    "enabled": true,
    "strict_projects": ["production"],  # Never bypass for these
    "auto_create_artifacts": true,      # Auto-generate templates
    "require_user_approval": true       # User must approve artifacts
  }
}
```

## Examples

### Example 1: Blocked Code Request

```
User: "Build a user dashboard with profile and activity feed"

Claude: ❌ Cannot write code yet - missing required artifacts

        Current phase: Phase 1 (SEED)
        Code allowed in: Phase 8 (Implementation)

        Required before coding:
          [ ] Requirements documented
          [ ] Low-fidelity mockups
          [ ] Data model defined

        Options:
          [1] Create all artifacts in sequence (recommended)
          [2] Create requirements only
          [3] Declare SPIKE mode (skip to code)
          [4] Advance through phases normally

        Your choice:

User: 1

Claude: ✅ Starting artifact creation sequence

        Step 1/3: Requirements Document
        ════════════════════════════════════════

        Based on your request, here's a draft requirements doc:

        # Requirements: User Dashboard

        ## User Stories
        US1. As a user, I want to see my profile information,
             so that I can verify my account details

        US2. As a user, I want to see my recent activity,
             so that I can track my interactions

        ## Acceptance Criteria
        - [ ] Profile card displays avatar, name, email
        - [ ] Activity feed shows last 10 activities
        - [ ] Activities sorted by timestamp (newest first)
        - [ ] Log out button is accessible

        ## Functional Requirements
        FR1. Dashboard shall display user profile card
        FR2. Dashboard shall display activity feed
        FR3. Dashboard shall include logout functionality

        ## Non-Functional Requirements
        NFR1. Dashboard loads in < 2 seconds
        NFR2. Mobile-responsive design

        [Save to REQUIREMENTS.md?]
        [1] Save as-is [2] Edit first [3] Cancel

User: 1

Claude: ✅ Saved: REQUIREMENTS.md

        Step 2/3: Low-Fidelity Mockups
        ════════════════════════════════════════

        Creating wireframe mockup...

        [Generated mockups/dashboard.html]

        ┌─────────────────────────────┐
        │ User Dashboard              │
        ├─────────────────────────────┤
        │ ┌───────────────────────┐   │
        │ │  Profile Card         │   │
        │ │  [Avatar]             │   │
        │ │  Name: John Doe       │   │
        │ │  Email: john@ex.com   │   │
        │ └───────────────────────┘   │
        │                             │
        │ ┌───────────────────────┐   │
        │ │  Activity Feed        │   │
        │ │  • Activity 1         │   │
        │ │  • Activity 2         │   │
        │ │  • Activity 3         │   │
        │ └───────────────────────┘   │
        │                             │
        │ [Log Out]                   │
        └─────────────────────────────┘

        [Open in browser?]
        [1] Yes, open now [2] No, continue

User: 1

Claude: ✅ Opened mockups/dashboard.html in Chrome

        Step 3/3: Data Model
        ════════════════════════════════════════

        Defining entities based on requirements...

        Entities identified:
        1. User (profile data)
        2. Activity (activity feed items)

        Creating data models in hmode/hmode/shared/semantic/domains/...

        [Created user-management/user.yaml]
        [Created user-management/activity.yaml]

        ✅ All artifacts created!

        Artifacts:
          ✅ REQUIREMENTS.md
          ✅ mockups/dashboard.html
          ✅ hmode/hmode/shared/semantic/domains/user-management/

        Review artifacts, then we can proceed to Phase 8.

        Next steps:
          [1] Review and approve artifacts
          [2] Advance to Phase 8 (Implementation)
          [3] Make changes to artifacts first

        Your choice:

User: 2

Claude: ✅ Advancing to Phase 8 (Implementation)

        Now I can write code! Starting implementation...
```

### Example 2: Proper SDLC Flow

```
User: "I want to build a task management app"

Claude: Let me follow proper SDLC phases for this.

        Phase 1: SEED
        ════════════════════════════════════════
        Capturing idea...

        Idea: Task management application
        Problem: Users need to organize and track tasks
        Vision: Simple, intuitive task manager

        ✅ SEED complete

        → Phase 2: RESEARCH
          [Y] Proceed [S] Skip [?] Details

User: Y

Claude: Phase 2: RESEARCH
        ════════════════════════════════════════
        Researching existing solutions...

        Found: Todoist, Trello, Asana, Linear
        Gap: All are team-focused, need individual version

        ✅ RESEARCH complete

        → Phase 3: EXPANSION
          This is where we document REQUIREMENTS
          [Y] Proceed [S] Skip [?] Details

User: Y

Claude: Phase 3: EXPANSION
        ════════════════════════════════════════

        Creating requirements document...

        [Generated REQUIREMENTS.md with user stories]
        [Includes acceptance criteria]
        [Includes functional & non-functional requirements]

        ✅ EXPANSION complete

        → Phase 4-5: ANALYSIS & SELECTION
          [Y] Proceed [S] Skip

User: S

Claude: ✅ Skipped Phase 4-5 (single approach scenario)

        → Phase 6: DESIGN
          This is where we create MOCKUPS and DATA MODEL
          [Y] Proceed

User: Y

Claude: Phase 6: DESIGN
        ════════════════════════════════════════

        Creating low-fidelity mockups...
        [Generated mockups/task-list.html]
        [Generated mockups/task-detail.html]

        Defining data model...
        [Created hmode/hmode/shared/semantic/domains/task-mgmt/task.yaml]
        [Created hmode/hmode/shared/semantic/domains/task-mgmt/project.yaml]

        ✅ DESIGN complete
        ✅ All pre-code artifacts ready!

        → Phase 7: TEST_DESIGN
          Write tests (no implementation yet)
          [Y] Proceed [S] Skip

User: Y

Claude: Phase 7: TEST_DESIGN
        ════════════════════════════════════════

        Writing tests based on acceptance criteria...

        [Created tests/task.test.ts]
        [Created tests/project.test.ts]
        [Tests currently FAIL - no implementation yet]

        ✅ TEST_DESIGN complete

        → Phase 8: IMPLEMENTATION
          ✅ NOW I can write code!
          All prerequisites met:
            ✅ Requirements documented
            ✅ Mockups created
            ✅ Data model defined
            ✅ Tests written

          [Y] Proceed to implementation

User: Y

Claude: Phase 8: IMPLEMENTATION
        ════════════════════════════════════════

        NOW writing code...

        [Implements features to make tests pass]
        [References requirements & mockups]
        [Uses defined data models]
```

### Example 3: SPIKE Mode

```
User: "I just want to quickly test if WebSockets work with our setup"

Claude: This sounds like a SPIKE - quick technical validation.

        SPIKE mode options:
        [1] Full SPIKE (skip all phases, throwaway code, max 3 days)
        [2] Mini SPIKE (quick test, document findings, 1 hour)
        [3] Proper SDLC (requirements → mockups → model → code)

        Your choice:

User: 2

Claude: ✅ Mini SPIKE mode activated

        Bypassing pre-code gate for quick validation...

        [Writes minimal WebSocket test code]
        [Documents findings in spike-notes.md]

        Result: WebSockets work ✅
        Next: Archive spike code or promote to proper project

        [1] Archive spike
        [2] Promote to proper project (will need req + mockups + model)

User: 2

Claude: ✅ Promoting to proper project

        Now let's do it right. Starting Phase 1...

        Phase 1: SEED
        ════════════════════════════════════════
        Based on spike, documenting idea...

        [Creates proper SEED document]
        [Begins SDLC process from Phase 1]
```

## Best Practices

1. **Always show the sequence** - Requirements → Mockups → Data Model → Code
2. **Auto-generate templates** - Don't make user start from scratch
3. **Make it fast** - 15-25 minutes total for all artifacts
4. **Visual feedback** - Show progress through steps
5. **Allow edits** - User can refine generated artifacts
6. **Explain benefits** - "This catches issues before coding"
7. **SPIKE mode escape hatch** - For legitimate quick tests

## Anti-Patterns

❌ **Don't do:**
- "Let me just write a quick prototype first"
- "We can document it later"
- "The requirements are obvious"
- "Mockups aren't needed for simple features"
- "Just use the existing data model"

✅ **Do:**
- "Let's document requirements first (5 min)"
- "Quick mockup will clarify the design"
- "Data model will inform the implementation"
- "This prevents costly rewrites"

## See Also

- SDLC Overview: `hmode/docs/processes/SDLC_OVERVIEW.md`
- Phase 3 (Requirements): `hmode/docs/processes/PHASE_3_EXPANSION.md`
- Phase 6 (Design): `hmode/docs/processes/PHASE_6_DESIGN.md`
- Domain Model SOP: `hmode/hmode/shared/semantic/domains/DOMAIN_MODEL_SOP.md`
- Design System: `hmode/shared/design-system/MANAGEMENT_GUIDELINES.md`