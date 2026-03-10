<!-- File UUID: 9078423c-6914-4a1a-a27f-5d8f1c81c8ed -->
# Claude Code: hmode Shared Methodology

## 1.0 OVERVIEW & ARCHITECTURE

**This file is a central orchestration point with pointers to detailed documentation.**

### 1.1 Performance Optimization
- Original CLAUDE.md: 2,000+ lines (~30K tokens)
- This orchestrator: ~500 lines (~7K tokens)
- **75% token reduction per interaction**

### 1.2 Path Aliases
Short notation for external docs (defined once, used throughout):

- `@core/` → `hmode/docs/core/`
- `@processes/` → `hmode/docs/processes/`
- `@patterns/` → `hmode/docs/patterns/`
- `@reference/` → `hmode/docs/reference/`
- `@design-system/` → `hmode/shared/design-system/`

Example: `@core/CRITICAL_RULES` = `hmode/docs/core/CRITICAL_RULES.md`
Example: `@design-system/MANAGEMENT_GUIDELINES` = `hmode/shared/design-system/MANAGEMENT_GUIDELINES.md`

### 1.3 Author Context
<!-- [PROJECT-SPECIFIC: override in .claude/CLAUDE.md] -->
<!-- Add your background, focus areas, and team context here -->

### 1.4 Environment Constraints & Quick Rules

**Claude Code Web Limitations:**
| Constraint | Workaround | Details |
|------------|------------|---------|
| S3 uploads | Use `ASSET_DIST_AWS_*` env vars (NOT `AWS_*`) | Section 7.1 |
| Docker builds | Use AWS CodeBuild | `@reference/CODEBUILD_DOCKER_SOP` |
| Slash commands | Skip invocation (desktop only) | Section 8.0 |
| Installation check | Suppress on web | Check `.system/install-state.yml` on desktop |

**Always Required:**
| Rule | When | Details |
|------|------|---------|
| File UUIDs | Every file creation | Section 7.9 |
| File analysis | Analyzing PDFs/images | Use `hmode/shared/tools/file_analyzer.py` |
| AWS guard check | Before ANY AWS command | Run `hmode/bin/claude-aws-guard-check current` |
| AWS verification | Before claiming infrastructure missing | Use correct profile, verify with AWS CLI, check `@reference/LEARNINGS` |
| Reuse check | Before building new | Search `hmode/shared/` first (golden repos, domains, tools) |
| RLHF signals | User feedback detected | Auto-log positive/negative sentiment |
| Branch preservation | NEVER delete branches | Switch instead of delete |

**Code Writing Gate (MANDATORY):**
| Check | Requirement | Action |
|-------|-------------|--------|
| Phase verification | Read `.project` file FIRST | Must be Phase 8+ to write code |
| Phase 1-7 detected | NO CODE - planning/research only | Refuse code, explain SDLC, offer Phase 8 advancement |
| No `.project` file | Ask: "Is this new project?" | Route to Phase 1 (SEED) workflow |
| SPIKE mode | Confirm throwaway code, max 3 days | Skip phases 2-7, prototype only |
| BROWNFIELD mode | Phase 0 assessment, then code allowed | Route to brownfield workflow based on work type |

**Publishing Rules:**
- ❌ NEVER `aws s3 cp` → ✅ Use `hmode/shared/tools/s3publish.py`
- ❌ NEVER CloudFront + S3 for microsites → ✅ Use AWS Amplify
- ✅ ALWAYS commit & push before deploying

**AWS Credentials:**
<!-- [PROJECT-SPECIFIC: override in .claude/CLAUDE.md] -->
<!-- Add AWS profiles, account IDs, and regions here -->
| Profile | Account | Purpose |
|---------|---------|---------|
| (configure in .claude/CLAUDE.md) | | |

**See Section 7.0 for complete technical standards.**

### 1.5 Quick Reference Table

#### Core Documentation (Load early/often)
| File | When to Load |
|------|--------------|
| `@core/CRITICAL_RULES` | All interactions |
| `@core/CONFIRMATION_PROTOCOL` | Complex/ambiguous tasks |
| `@core/INTENT_DETECTION` | Classify request type |
| `@core/EFFORT_LEVELS` | Research/analysis tasks |
| `@core/WRITING_STANDARDS` | Creating documentation |
| `@core/GUARDRAILS` | Tech/arch decisions |
| `@core/HACP` | When `/comms` protocol activated |

#### Process Files (Load by phase)
| Phase | File |
|-------|------|
| **Overview** | `@processes/SDLC_OVERVIEW` |
| **Phases 1-9** | `@processes/PHASE_{N}_{NAME}` |
| **Phase 6 Design** | `@processes/PHASE_6_DESIGN_GUIDELINES` (MANDATORY for Phase 6 work) |
| **Domain Models** | `@processes/DOMAIN_MODEL_SOP` |
| **Brownfield** | `@processes/BROWNFIELD_ENTRY`, `@processes/HOTFIX_WORKFLOW` |

#### Pattern Files (Load when pattern invoked)
| Pattern | File |
|---------|------|
| **Multi-agent** | `@patterns/CHILD_PROCESSES` |
| **Batch ops** | `@patterns/PARALLEL_EXECUTION` |
| **Complex design** | `@patterns/COMPONENT_DECOMPOSITION` |
| **Migration** | `@processes/MIGRATION_SPECIALIST_AGENT` |
| **Local Dev** | `@processes/LOCAL_DEV_AGENT` |

#### Design System Files (Load for visual assets)
| File | When to Load |
|------|--------------|
| `@design-system/MANAGEMENT_GUIDELINES` | Creating ANY visual asset (HTML, mockup, diagram) |
| `@design-system/ENFORCEMENT_GUIDE` | React/Vite projects |
| `@design-system/templates/mockup.html` | Starting new HTML mockup |
| `@design-system/examples/VALIDATION_REPORT` | Validating asset compliance |

#### AWS Reference Files
| File | When to Load |
|------|--------------|
| `@reference/AWS_SECRETS` | Working with secrets, credentials, or AWS infrastructure |
| `@reference/LEARNINGS` | **MANDATORY** - Before AWS infrastructure claims, after user corrections, when investigating failures |

#### Testing Standards
| File | When to Load |
|------|--------------|
| `hmode/shared/standards/testing/README.md` | Testing framework selection |
| `hmode/shared/standards/testing/BDD_TESTING_GUIDE.md` | Adding Cucumber BDD tests with natural language + S3 reports |

---

## 2.0 INTENT & ROUTING

### 2.1 Request Classification
On every request, classify intent AND announce mode explicitly:

**MANDATORY MODE ANNOUNCEMENT:** Every response MUST begin with a verbose mode banner:
```
═══════════════════════════════════════════════════════════
  ENTERING [MODE NAME] MODE
  [One-line description of what this mode does]
═══════════════════════════════════════════════════════════
```

**Available Modes:**
| Mode | Trigger Keywords |
|------|-----------------|
| BUG FIX | fix, bug, broken, error |
| NEW FEATURE | add feature, implement, new capability |
| NEW PROTOTYPE | new project, build, prototype, new idea |
| RESEARCH | research, investigate, explore, compare |
| REFACTOR | refactor, clean up, restructure |
| ENHANCEMENT | improve, optimize, enhance |
| QUESTION | what, how, why, explain |
| CHORE | rename, move, delete, organize |
| MIGRATION | move project, migrate, consolidate repos, extract library |
| UNDETERMINED | Ambiguous → ask for clarification |
| BROWNFIELD | existing project, fix bug, add feature, refactor, maintenance |
| HOTFIX | production down, critical bug, P0, urgent |
| LOCAL DEV | run locally, test locally, sam local, docker-compose, local api |

```
┌─────────────────┬────────────────────────────────────────┐
│ Intent Type     │ Route To                               │
├─────────────────┼────────────────────────────────────────┤
│ Idea            │ 4.1 Ideas workflow                     │
│ Research        │ 4.2 Research workflow                  │
│ Asset request   │ 4.3 Asset generation workflow          │
│ Implementation  │ 4.4 SDLC workflow                      │
│ Spike           │ 4.5 Spike workflow                     │
│ Quick task      │ 4.6 Quick task workflow                │
│ Work on project │ 4.7 Project finder workflow            │
│ Brownfield work │ 4.8 Brownfield workflow                │
│ Hotfix          │ 4.8 Brownfield workflow (expedited)   │
│ Migration       │ 4.9 Migration workflow                 │
└─────────────────┴────────────────────────────────────────┘
```

**CRITICAL: Before ANY code generation, execute phase check:**
1. Check if `.project` file exists in current directory
2. If YES → Read file and extract current phase number
3. If phase < 8 → REFUSE code writing:
   - Response: "Cannot write code in Phase {N}. Current phase: {phase_name}. Options: [1] Continue {phase_activity} [2] Advance to Phase 8 [3] Declare SPIKE mode"
   - Explain what Phase {N} is for (planning/research/design)
   - Offer to help with current phase activities
4. If phase >= 8 OR SPIKE → Proceed with code generation
5. If NO `.project` file → Ask: "Is this a new project or quick task in existing project?"
   - New project → Route to 4.1 Ideas workflow (Phase 1)
   - Quick task → Confirm current working directory, proceed with caution

### 2.2 Phase Detection
1. Read `.project` file to determine current phase
2. **If Phase 6 (DESIGN)**: IMMEDIATELY check `hmode/guardrails/tech-preferences/` (see Section 6.25)
3. Load corresponding `@processes/PHASE_{N}_{NAME}`
4. Apply phase-specific rules

### 2.3 Dynamic Loading
```
User request → Classify intent → Check gates → Load relevant docs → Execute
```

**Full Details:** See `@core/INTENT_DETECTION`

### 2.4 "Work On" Detection
**Trigger phrases** (fuzzy match):
- "let's work on..."
- "continue working on..."
- "I want to work on..."
- "keep working on..."
- "resume work on..."

When detected → Route to 4.7 Project Finder workflow

---

## 3.0 COMMUNICATION STANDARDS

### 3.1 Writing Format
1. Decimal outline (1.0, 1.1, 1.2, 2.0, etc.)
2. Stage titles (# Stage N - Phase Name)
3. Numbered lists (NOT bullets, except checkmarks)
4. ASCII diagrams (10-second visual scan)
5. 50% fewer words (densified)

### 3.2 One Question at a Time
NEVER batch multiple questions. Ask ONE, wait for response, then next.

### 3.3 Asset Menus
When generating ANY file/resource, present:
```
Open: [1] file.xlsx [2] file.md [3] skip
```

### 3.4 Numbered Options
ALL choices MUST be numbered:
```
[1] Option A - brief description
[2] Option B - brief description
[3] Option C - brief description
```

### 3.5 Brevity Gate
Before outputting content > 20 lines:
1. Summarize in 3-5 lines first
2. Ask: "Show full? [Y/n]"

### 3.6 Effort Calibration
For research/analysis:
1. Show 3 items
2. Ask: "Continue? [1] brief [2] standard [3] comprehensive [4] ultra"

### 3.7 AI/Human Partnership

**AI's Role:**
- Classify requests (question/task/idea/project)
- Detect current phase from `.project`
- Run gates before execution
- Confirm complex/ambiguous tasks
- Execute approved actions

**Human's Role:**
- Approve technology decisions
- Confirm complex operations
- Define output constraints when no template exists
- Provide feedback for improvements

### 3.8 Confirmation Protocol
For complex tasks: Paraphrase → Options → Confirm

**Full Standards:** See `@core/WRITING_STANDARDS`

---

## 4.0 WORKFLOWS

### 4.1 Ideas Workflow
**Trigger:** User shares any idea (even brief/casual)
**Gates:** None
**Action:** IMMEDIATELY save to `project-management/ideas/active/`

- **Filename:** `{descriptive-slug}-{first-8-uuid-chars}.md`
- **YAML Frontmatter:** uuid, id, captured, status, tags
- **Content:** Condensed summary with core idea, problem, vision
- **Template:** Use `project-management/ideas/.template.md`

### 4.2 Research Workflow
**Trigger:** Research/analysis request
**Gates:** Artifact Library (scope/format/depth)
**Action:** Execute research with defined constraints

1. Check artifact library for research template
2. If no match → prompt user for output constraints
3. Apply effort calibration
4. Execute research with citations
5. Flag for potential library addition

### 4.3 Asset Generation Workflow
**Trigger:** Generate image, document, mockup, etc.
**Gates:** Artifact Library, Golden Repo, Design System, **Domain Agent**, **IA Agent**, **UX Agent**
**Action:** Generate with specs from gates

1. Check artifact library for template
2. If no match → prompt user for output constraints
3. Check golden repo for starting point
4. **Design System Gate** (for visual assets):
   - Load `@design-system/MANAGEMENT_GUIDELINES` (sections 12-16)
   - Use template from `hmode/shared/design-system/templates/`
   - Apply design tokens (NO raw hex colors)
   - Follow atomic design classification
5. **Domain Models Gate** (for data-driven assets):
   - Spawn `domain-modeling-specialist` if data models needed
   - Discover/create domain models with external research
   - Require human approval for new domains
   - Skip if no data modeling required
6. **IA Agent Gate** (for navigation/flow/structure):
   - Spawn `information-architecture-agent`
   - Design navigation hierarchy, user flows, content structure
   - Output IA specification for UX agent
   - Skip if simple component or IA already defined
7. **UX Agent Gate** (for visual composition):
   - Spawn `ux-component-agent`
   - Compose components from design library (atomic design)
   - Apply design tokens and visual hierarchy
   - Generate asset with metadata header
8. **Validate** against design system checklist (section 15.7)
9. Publish (S3 if applicable)
10. Flag for potential library addition

### 4.4 SDLC Workflow
**Trigger:** New implementation or feature
**Gates:** ALL gates (full check)
**Action:** Follow 9-phase SDLC

**Phase 6 (Design) Entry Requirements:**

**🚨 Phase 6 has TWO distinct sub-phases (MUST complete both):**
- **6A: Application Design** - What the app does (features, UI, business logic, APIs)
- **6B: Infrastructure Design** - How to deploy it (AWS, CDK, monitoring, CI/CD)

**Workflow:**
1. **ASK which phase:** "Phase 6A (Application) or 6B (Infrastructure)?"
2. **MANDATORY**: Use Plan agent if creating 3+ design documents
3. Plan agent responsibilities:
   - **For 6A:** Outline application design docs (features, UI, APIs, data models)
   - **For 6B:** Outline infrastructure design docs (AWS architecture, CDK, monitoring)
   - Check `hmode/guardrails/tech-preferences/` for ALL relevant categories
   - Define document dependencies and creation sequence
4. After planning complete → Execute with human approval
5. **Sequential:** Complete 6A before starting 6B (infrastructure depends on application)
6. See Section 6.25 for complete Phase 6 Design Checklist

See Section 6.0 for full SDLC process.

### 4.5 Spike Workflow
**Trigger:** Explicit spike request
**Gates:** Minimal (tech prefs only)
**Action:** Skip phases 2-7, throwaway code, max 3 days

### 4.6 Quick Task Workflow
**Trigger:** Simple execution within existing project
**Gates:** None (already passed when entering phase)
**Action:** Execute directly

### 4.7 Project Finder Workflow
**Trigger:** "let's work on...", "continue working on...", "I want to work on..."
**Gates:** None
**Action:** Search projects & ideas, present top 3 matches

1. Extract search term from user request
2. Search `projects/**/.project` files (name, description, id, folder)
3. Search `project-management/ideas/active/*.md` files
4. Score matches: exact name (100) > contains (80) > description (60) > path (50)
5. Present top 3 with format:
   ```
   [1] project-name-id
       📁 path/to/project
       📝 Brief description
       🛠️ Next.js, FastAPI, etc.
       🔄 Phase N | active
   ```
6. User selects [1/2/3/n]
7. On selection: cd to project, load `.project`, show context

**See:** `/workon` command for details

### 4.8 Brownfield Workflow
**Trigger:** Bug fixes, features on existing code, refactoring, maintenance
**Gates:** Minimal (respect existing architecture)
**Action:** Follow abbreviated phases based on work type

**Work Types:**
| Type | Description | Phases |
|------|-------------|--------|
| HOTFIX | Critical production fix | 0 → 8 → 9 |
| BUG_FIX | Standard bug | 0 → 7 → 8 → 9 |
| FEATURE | New capability | 0 → 3 → 5 → 6 → 7 → 8 → 9 |
| REFACTOR | Code improvement | 0 → 7 → 8 → 9 |

**Key Differences from Greenfield SDLC:**
- Code allowed after Phase 0 (not Phase 8)
- Tests wrap existing code, not all new
- Work within existing architecture
- Skip SEED phase (project exists)

**Detection:** Route to brownfield when:
1. User references existing project
2. `.project` file exists and phase >= 8
3. Code already exists in directory

**See:** `@processes/BROWNFIELD_ENTRY`, `@processes/HOTFIX_WORKFLOW`, `@processes/MAINTENANCE_TRIAGE`

### 4.9 Migration Workflow
**Trigger:** Moving projects/files between repos, consolidation, extraction
**Gates:** Migration Agent (Gate 10)
**Action:** Git-safe migration with history preservation

**Repository Targets:**
- ~/dev/lab → Main monorepo (500+ projects)
- ~/dev/awstools → AWS tooling monorepo
- ~/dev/hl-protoflow → Claude Code plugin

**Migration Types:**
1. **Project Migration:** Full directory with git history
2. **File Migration:** Individual files with UUID preservation
3. **Library Extraction:** Shared code to dedicated repo
4. **Consolidation:** Merge scattered code into monorepo

**Workflow Steps:**
1. Spawn `migration-specialist` agent
2. Agent analyzes dependencies and creates plan
3. Human approval required
4. Execute git-safe migration (git subtree/filter-repo)
5. Update references, imports, .gitmodules
6. Generate rollback script
7. Validate (tests, builds)
8. Document migration (CHANGELOG, README)
9. Monitor for 1 week before archiving source

**Safety Mechanisms:**
- Dry run mode available
- Rollback scripts auto-generated
- Validation gates (git status, tests, builds)
- Manual approval for destructive operations
- Staged commits (not all-at-once)

**See:** `@processes/MIGRATION_SPECIALIST_AGENT` for full details

---

## 5.0 GATES & CHECKPOINTS

### 5.1 Gate Trigger Matrix

```
┌─────────────────────────┬───────────┬───────────┬────────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┐
│ Action Type             │ Artifact  │ Golden    │ Tech       │ Domain    │ Code      │ Design    │ Info      │ UX        │ Domain    │ Infra/SRE │ Amplify   │ Migration │ CDK QA    │
│                         │ Library   │ Repo      │ Prefs      │ Models    │ Standards │ System    │ Arch      │ Compose   │ Agent     │ Agent     │ Deploy    │ Agent     │ Agent     │
├─────────────────────────┼───────────┼───────────┼────────────┼───────────┼───────────┼───────────┼───────────┼───────────┼───────────┼───────────┼───────────┼───────────┼───────────┤
│ Visual asset (HTML/SVG) │     ✓     │     ✓     │     -      │     -     │     -     │     ✓     │     -     │     ✓     │     -     │     -     │     -     │     -     │     -     │
│ React component         │     -     │     -     │     ✓      │     -     │     ✓     │     ✓     │     -     │     ✓     │     -     │     -     │     -     │     -     │     -     │
│ Research                │     ✓     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │
│ New feature (data model)│     ✓     │     ✓     │     ✓      │     ✓     │     ✓     │     -     │     -     │     -     │     ✓     │     -     │     -     │     -     │     -     │
│ New implementation      │     ✓     │     ✓     │     ✓      │     ✓     │     ✓     │     ✓     │     ✓     │     ✓     │     ✓     │     -     │     -     │     -     │     -     │
│ Entering Phase 8        │     ✓     │     ✓     │     ✓      │     ✓     │     ✓     │     ✓     │     ✓     │     ✓     │     ✓     │     -     │     -     │     -     │     -     │
│ Navigation/flow design  │     -     │     -     │     -      │     -     │     -     │     -     │     ✓     │     -     │     -     │     -     │     -     │     -     │     -     │
│ UI mockup/prototype     │     ✓     │     ✓     │     -      │     -     │     -     │     ✓     │     -     │     ✓     │     -     │     -     │     -     │     -     │     -     │
│ Infrastructure work     │     -     │     ✓     │     ✓      │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │     -     │     -     │     -     │
│ Monitoring/observability│     -     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │     -     │     -     │     -     │
│ CI/CD pipeline setup    │     -     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │     -     │     -     │     -     │
│ CDK/Terraform deployment│     -     │     ✓     │     ✓      │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │     -     │     -     │     -     │
│ CDK code review         │     -     │     -     │     ✓      │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │
│ Pre-CDK deployment      │     -     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │
│ Amplify deployment      │     -     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │     -     │     -     │
│ Idea capture            │     -     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │
│ Quick task (in-phase)   │     -     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │
│ Project migration       │     -     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │     -     │
│ File/library extraction │     -     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │     -     │
│ Repository consolidation│     -     │     -     │     -      │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     -     │     ✓     │     -     │
└─────────────────────────┴───────────┴───────────┴────────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘
```

### 5.2 Gate Sequence (when triggered)

**Gate 1: Artifact Library** → Check `hmode/shared/artifact-library/catalog/`
```
If match      → "Use template? [Y/n/m]" → Load specs/scope
If no match   → Prompt user to define output constraints:
                • Format? (HTML/PDF/PNG/MD/etc.)
                • Scope? (brief/standard/comprehensive)
                • Style? (formal/casual/technical)
                • Dimensions? (if visual)
                • Other requirements?
              → Flag for potential addition to library after
```

**Gate 2: Golden Repo** → Check `hmode/shared/golden-repos/`
```
If match      → Copy as starting point
If no match   → "[1] Create from GitHub best practice [2] Skip"
If creating   → Search GitHub for exemplar → Propose structure → Save to golden-repos/
```

**Gate 3: Tech Preferences** → Read `hmode/guardrails/tech-preferences/`
```
If found      → Confirm tech stack is approved
If not found  → Ask user before proceeding
```

**Gate 4: Domain Models** → Spawn `domain-modeling-specialist`
```
TRIGGER: Creating data models, needing domain discovery, domain evolution

INVOKE WHEN:
  - New feature requires data models
  - Need to discover applicable existing domains
  - Creating new domain with external research
  - Evolving existing domain (version management)
  - Extracting shared primitives to core domain
  - Managing domain dependencies

AGENT RESPONSIBILITIES:
  1. Read hmode/shared/semantic/domains/registry.yaml
  2. Discover applicable existing domains
  3. Research external sources (schema.org, GitHub, APIs)
  4. Propose data models in YAML format
  5. Manage domain versioning and evolution
  6. Extract shared primitives to core domain
  7. Handle domain composition and dependencies

WORKFLOW:
  If match      → Import from hmode/shared/semantic/domains/{domain}/
  If no match   → Spawn agent to research and propose new domain
  If creating   → Agent generates YAML → REQUIRE human approval before implementation
  If evolving   → Agent proposes version bump → Human approval required

OUTPUT FORMAT:
  - Domain YAML files in hmode/shared/semantic/domains/{domain}/
  - Registry updates with domain metadata
  - Approval request with rationale
```

**Gate 5: Code Standards** → Read `hmode/shared/standards/code/{tech}/`
```
If match      → Load patterns, naming conventions, structure
If no match   → Propose adding after implementation
```

**Gate 6: Design System** → Read `hmode/shared/design-system/MANAGEMENT_GUIDELINES.md`
```
TRIGGER: ANY visual asset (HTML, mockup, diagram, landing page, React component)

BEFORE GENERATION:
  1. Check for template in hmode/shared/design-system/templates/
  2. Load design tokens from globals.css
  3. Determine atomic level (atom/molecule/organism/template/page)
  4. Generate asset UUID (8-char)

DURING GENERATION:
  ❌ NEVER use raw hex colors (#1a1a2e) → ✅ Use hsl(var(--background))
  ❌ NEVER use magic spacing (17px)    → ✅ Use token scale (1rem, 1.5rem)
  ❌ NEVER exceed 3 hierarchy levels   → ✅ H1 > H2 > Body only
  ❌ NEVER have multiple primary CTAs  → ✅ Single focal point

AFTER GENERATION:
  1. Add metadata comment header
  2. Validate against checklist (section 15.7)
  3. Announce atomic classification
```

**Gate 7: Information Architecture** → Spawn `information-architecture-agent`
```
TRIGGER: Navigation design, user flows, content hierarchy, sitemap creation

INVOKE WHEN:
  - Designing navigation structure for new app/site
  - Creating user flow diagrams
  - Organizing content hierarchy
  - Building sitemap or wireframe structure
  - Phase 3 (Expansion) or Phase 6 (Design) with UI component

AGENT RESPONSIBILITIES:
  1. Analyze user goals and tasks
  2. Design navigation hierarchy (max 3 levels deep)
  3. Map user flows and decision points
  4. Define content groupings and taxonomy
  5. Create sitemap with page relationships
  6. Output IA specification for UX Composition gate

OUTPUT FORMAT:
  - Navigation tree (YAML or diagram)
  - User flow diagram (Mermaid or ASCII)
  - Content hierarchy specification
  - Handoff notes for UX agent

HANDOFF TO GATE 8:
  When IA is complete → Pass specification to UX Composition gate
```

**Gate 8: UX Composition** → Spawn `ux-component-agent`
```
TRIGGER: Visual asset creation, component composition, mockup generation

INVOKE WHEN:
  - Creating mockups or prototypes
  - Composing UI components from design library
  - Building React components with shadcn/ui
  - Applying themes or design tokens
  - Translating IA specification to visual components

AGENT RESPONSIBILITIES:
  1. Select appropriate template from hmode/shared/design-system/templates/
  2. Compose components using atomic design (atoms → molecules → organisms)
  3. Apply design tokens (NEVER raw hex/magic numbers)
  4. Implement visual hierarchy from IA specification
  5. Generate asset with proper metadata header
  6. Validate against design system checklist

INPUT SOURCES:
  - Direct user request for mockup/component
  - IA specification from Gate 7
  - Design brief from Phase 6

OUTPUT FORMAT:
  - HTML mockup (Tailwind CDN, no build step)
  - React component (shadcn/ui compliant)
  - Asset metadata (UUID, atomic level, tokens used)
```

**Gate 9: Infrastructure/SRE** → Spawn `infra-sre`
```
TRIGGER: Infrastructure, deployment, monitoring, scaling, CI/CD, security tasks

INVOKE WHEN:
  - Creating/modifying CDK stacks or Terraform configs
  - Setting up CI/CD pipelines (GitHub Actions, CodePipeline)
  - Configuring monitoring/alarms (CloudWatch, X-Ray)
  - Implementing auto-scaling or health checks
  - Managing secrets (Secrets Manager, Parameter Store)
  - Reviewing IAM policies or security groups
  - Deploying infrastructure (non-Amplify)
  - Troubleshooting deployment issues

AGENT RESPONSIBILITIES:
  1. Design and implement AWS infrastructure (CDK preferred)
  2. Configure CI/CD pipelines and deployment workflows
  3. Set up monitoring, logging, and tracing
  4. Implement auto-scaling and reliability patterns
  5. Manage secrets and IAM policies securely
  6. Follow standard Makefile deployment pattern
  7. Document deployment procedures and runbooks
  8. Verify deployments with smoke tests

WORKFLOW:
  If Amplify deployment     → Spawn amplify-deploy-specialist
  If CDK/Terraform/other    → Spawn infra-sre agent
  If monitoring needed      → Spawn infra-sre agent
  If CI/CD setup needed     → Spawn infra-sre agent

OUTPUT FORMAT:
  - CDK stacks (TypeScript)
  - Terraform configurations (HCL)
  - GitHub Actions workflows (YAML)
  - CloudWatch alarms and dashboards
  - Deployment documentation (Markdown)
  - Infrastructure diagrams

COORDINATION:
  - Hands off to amplify-deploy-specialist for Amplify apps
  - Hands off to ux-component-agent for frontend changes
  - Receives infrastructure requirements from main workflow
```

**Gate 10: Migration Agent** → Spawn `migration-specialist`
```
TRIGGER: Moving projects/files between repositories, consolidation, extraction, or RENAME

INVOKE WHEN:
  - Moving projects between ~/dev/lab, ~/dev/awstools, ~/dev/hl-protoflow
  - Extracting shared libraries to dedicated repos
  - Consolidating scattered code into monorepos
  - Migrating files while preserving git history and metadata
  - Updating submodules and cross-repo references
  - **RENAMING projects** (shortening long folder names, updating all references)

TRIGGER KEYWORDS: "move to", "consolidate", "extract to", "rename", "shorten name"

AGENT RESPONSIBILITIES:
  1. Analyze source/target repositories and dependencies
  2. Preserve git history (git filter-repo, git subtree, git mv)
  3. Maintain file UUIDs and metadata
  4. Update import paths and references
  5. Update .gitmodules if using submodules
  6. Generate rollback scripts
  7. Validate migrations with tests
  8. Document migration rationale
  9. **For renames:** Update DASHBOARD.md, related_prototypes, deployment configs

REPOSITORY AWARENESS:
  - ~/dev/lab: Main monorepo (500+ projects, semantic domains, shared tools)
  - ~/dev/awstools: AWS tooling monorepo
  - ~/dev/hl-protoflow: Claude Code plugin repository

WORKFLOW:
  If project migration    → Git subtree split + merge with history
  If file migration       → Copy with UUID preservation + update references
  If extraction          → Git filter-repo + submodule setup
  If consolidation       → Batch migrate + deduplicate + refactor
  If rename              → Git mv + scan/update all references (Type 7)

SAFETY MECHANISMS:
  - Dry run mode
  - Rollback script generation
  - Validation gates (git status, tests, builds)
  - Manual approval for destructive operations
  - Staged commits (not all-at-once)

OUTPUT FORMAT:
  - Migrated files with preserved UUIDs
  - Updated import statements and references
  - Migration documentation (CHANGELOG, README updates)
  - Rollback script (bash)
  - Validation report (tests passed, builds succeeded)

FULL DETAILS: @processes/MIGRATION_SPECIALIST_AGENT
```

**Gate 11: CDK QA Agent** → Spawn `cdk-qa-specialist`
```
TRIGGER: CDK code written, reviewed, or before deployment

INVOKE WHEN:
  - Reviewing CDK stack definitions (Phase 6 or Phase 8)
  - Before deploying CDK stacks to any environment
  - After significant CDK refactoring
  - During code reviews of infrastructure changes
  - Adding new CDK constructs or stacks

AGENT RESPONSIBILITIES:
  1. Layer & Construct Validation
     - Verify L1/L2/L3 construct usage patterns
     - Check for proper abstraction levels
     - Ensure custom L3 constructs are reusable

  2. Stack Decomposition Analysis
     - Validate single responsibility principle
     - Check stack dependencies (no cycles)
     - Verify stack size (<500 lines)
     - Confirm proper separation of concerns

  3. Assumption Validation
     - VPC lookups with fallbacks
     - Domain/certificate existence checks
     - Security group references
     - IAM role assumptions
     - Resource tagging completeness

  4. Configuration Management
     - Environment-specific configs properly separated
     - No hardcoded values (use props/context)
     - Secrets in Secrets Manager/Parameter Store

  5. Monitoring & Observability
     - CloudWatch alarms for critical resources
     - X-Ray tracing enabled (per tech preferences)
     - Log retention configured
     - Cost allocation tags present

  6. Security Best Practices
     - Encryption at rest/in transit
     - Least privilege IAM policies
     - No hardcoded credentials
     - Justified public resources

  7. Dependency Analysis
     - Cross-stack references properly handled
     - No circular dependencies
     - Stack deployment order documented

WORKFLOW:
  If Phase 6 (Design)     → Validate architecture approach
  If Phase 8 (Implementation) → Validate actual CDK code
  If pre-deployment       → Full validation with assumption checks

OUTPUT FORMAT:
  - QA Report (Markdown)
    - Critical issues (must fix)
    - Warnings (should fix)
    - Recommendations
    - Assumption checklist
  - Issue list (JSON for CI/CD)
  - Dependency graph (Mermaid diagram)
  - Architecture validation summary

VALIDATION PHASES:
  1. Static Analysis: Parse TypeScript AST, identify patterns
  2. Configuration Validation: Check environment configs
  3. Best Practice Verification: Stack decomposition, monitoring
  4. Assumption Testing: Identify external dependencies
  5. Report Generation: Comprehensive QA report with fixes

FULL DETAILS: @processes/CDK_QA_AGENT
```

### 5.4 Gate Execution Order

Gates execute in dependency order based on task type:

**For UI/Visual Work:**
```
┌─────────────────────────────────────────────────────────────┐
│                    GATE EXECUTION FLOW                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Gates 1-3 (Artifact, Golden Repo, Tech Prefs)              │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                           │
│  │   Gate 4    │  Domain Agent (if data models needed)     │
│  │ (optional)  │                                           │
│  └──────┬──────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │   Gate 6    │  Design System (tokens, templates)        │
│  │   (always)  │                                           │
│  └──────┬──────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐     ┌─────────────┐                       │
│  │   Gate 7    │────▶│   Gate 8    │                       │
│  │   IA Agent  │     │  UX Agent   │                       │
│  │ (structure) │     │  (visuals)  │                       │
│  └─────────────┘     └──────┬──────┘                       │
│                             │                               │
│                             ▼                               │
│                      Asset Generated                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**For Data-Driven Features:**
```
┌─────────────────────────────────────────────────────────────┐
│  Gates 1-3 (Artifact, Golden Repo, Tech Prefs)              │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                           │
│  │   Gate 4    │  Domain Agent                             │
│  │  (required) │  - Discover domains                       │
│  │             │  - Propose models                         │
│  │             │  - Human approval                         │
│  └──────┬──────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │   Gate 5    │  Code Standards                           │
│  └──────┬──────┘                                           │
│         │                                                   │
│         ▼                                                   │
│    Implementation                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**For Infrastructure/Deployment Work:**
```
┌─────────────────────────────────────────────────────────────┐
│  User requests infrastructure/deployment task               │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────┐                              │
│  │  Router: Check app type  │                              │
│  └────┬──────────────────┬──┘                              │
│       │                  │                                  │
│   NextJS/Vite        CDK/Terraform/                         │
│   to Amplify         Other Infrastructure                   │
│       │                  │                                  │
│       ▼                  ▼                                  │
│  ┌──────────────┐    ┌──────────────┐                      │
│  │   Amplify    │    │  Infra/SRE   │                      │
│  │   Deploy     │    │    Agent     │                      │
│  │  Specialist  │    │              │                      │
│  └──────┬───────┘    └──────┬───────┘                      │
│         │                   │                               │
│         ▼                   ▼                               │
│    Amplify App         Infrastructure                       │
│    Deployed            Deployed                             │
│         │                   │                               │
│         └────────┬──────────┘                               │
│                  │                                          │
│                  ▼                                          │
│            Smoke Tests                                      │
│                  │                                          │
│                  ▼                                          │
│          Deployment Complete                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**For Monitoring/Observability Work:**
```
┌─────────────────────────────────────────────────────────────┐
│  User requests monitoring/alarms/observability              │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────┐                       │
│  │  Infra/SRE Agent                │                       │
│  │  - Configure CloudWatch alarms  │                       │
│  │  - Set up X-Ray tracing         │                       │
│  │  - Create dashboards            │                       │
│  │  - Write runbooks               │                       │
│  └──────┬──────────────────────────┘                       │
│         │                                                   │
│         ▼                                                   │
│    Observability Complete                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**For Migration Work:**
```
┌─────────────────────────────────────────────────────────────┐
│  User requests migration between repos                      │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────┐                      │
│  │  Gate 10: Migration Specialist   │                      │
│  │  - Analyze dependencies          │                      │
│  │  - Create migration plan         │                      │
│  │  - Human approval                │                      │
│  └────┬─────────────────────────────┘                      │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────┐                      │
│  │  Execute Git-Safe Migration      │                      │
│  │  - Preserve history (git subtree)│                      │
│  │  - Maintain file UUIDs           │                      │
│  │  - Update references/imports     │                      │
│  │  - Update .gitmodules            │                      │
│  └────┬─────────────────────────────┘                      │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────┐                      │
│  │  Validation & Rollback Scripts   │                      │
│  │  - Run tests                     │                      │
│  │  - Verify builds                 │                      │
│  │  - Generate rollback.sh          │                      │
│  │  - Document changes              │                      │
│  └────┬─────────────────────────────┘                      │
│       │                                                     │
│       ▼                                                     │
│  Migration Complete                                         │
│  (Monitor for 1 week before archiving source)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**For CDK Code Review:**
```
┌─────────────────────────────────────────────────────────────┐
│  CDK code written or being reviewed                         │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────┐                      │
│  │  Gate 11: CDK QA Specialist      │                      │
│  │  - Layer validation (L1/L2/L3)   │                      │
│  │  - Stack decomposition check     │                      │
│  │  │  - Assumption validation       │                      │
│  │  - Best practices review         │                      │
│  └────┬─────────────────────────────┘                      │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────┐                      │
│  │  Generate QA Report              │                      │
│  │  - Critical issues (must fix)    │                      │
│  │  - Warnings (should fix)         │                      │
│  │  - Recommendations               │                      │
│  │  - Assumption checklist          │                      │
│  └────┬─────────────────────────────┘                      │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────┐                      │
│  │  Human Review                    │                      │
│  │  - Fix critical issues           │                      │
│  │  - Address warnings              │                      │
│  │  - Validate assumptions          │                      │
│  └────┬─────────────────────────────┘                      │
│       │                                                     │
│       ▼                                                     │
│  CDK Review Complete                                        │
│  (Ready for deployment)                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Skip Conditions:**
- Gate 4 (Domain Agent): Skip if no data modeling required
- Gate 7 (IA Agent): Skip for simple components or when IA already defined
- Gate 8 (UX Agent): Skip for pure IA work or non-visual tasks
- Gate 9 (Infra/SRE): Only invoke for infrastructure/deployment/monitoring tasks
- Amplify Deploy Agent: Only invoke for NextJS/Vite deployments to Amplify
- Gate 10 (Migration): Only invoke when explicitly moving code between repos or **renaming projects**
```

### 5.5 Protected Files (Guardrails)
NEVER modify without human approval:
- `hmode/guardrails/tech-preferences/`
- `hmode/guardrails/architecture-preferences/`
- `hmode/guardrails/WRITING_STYLE_GUIDE.md`
- `CLAUDE.md`

---

## 6.0 SDLC PROCESS ⚠️ NO CODE BEFORE PHASE 8 ⚠️

### 6.1 Conceptual Model (5 Questions)

> **Everything we build is for a human with an intent.**

```
1. SEED         → What's the idea?
2. FOR WHO      → Who is this for? (REQUIRED - infer, don't TBD)
   2a. PERSONA  → What are attributes of that person?
3. INTENT       → What are they trying to do?
4. SOLUTIONS    → How could they do it? (MULTIPLE approaches, not one)
5. BUILD        → What needs to be built? (After choosing ONE approach)
```

### 6.2 Phase Flow

```
Project Types: exploration | prototype | production

SEED → RESEARCH → [FEASIBILITY] → EXPANSION → ANALYSIS → SELECTION → [PRD] → APP DESIGN → INFRA DESIGN → TEST → IMPL → REFINE
  1       2           2.5            3           4           5         5.5       6A          6B          7      8       9
        ↑                      (Explore 5-10   (Compare    (Choose     (What app  (How to
   PERSONA REQUIRED             approaches)    approaches)  ONE)        does)      deploy)
   Infer → Confirm → Proceed

Phase 2.5 (production only): Go/no-go gate
Phase 3 (Expansion): Divergent thinking - explore MULTIPLE approaches (5-10 different strategies)
Phase 4 (Analysis): Convergent analysis - score and compare all approaches
Phase 5 (Selection): Decision point - choose ONE approach to implement
Phase 5.5 (production required): PRD, requirements, acceptance criteria
Phase 6A (Application Design): What the app does - features, UI, business logic, APIs, data models
Phase 6B (Infrastructure Design): How to deploy it - AWS services, CDK stacks, monitoring, CI/CD
Phase 8 variants: Standard | Web/UI (8.5 QA) | Divergent (8.1-8.3)
Special: SPIKE (skip 2-7, throwaway code, max 3 days)
```

### 6.25 Phase 6 Design Checklist (MANDATORY)

**🚨 CRITICAL: Phase 6 has TWO distinct sub-phases that MUST be completed separately:**
- **Phase 6A: Application Design** - What the app does (features, UI, business logic)
- **Phase 6B: Infrastructure Design** - How to deploy and run it (AWS, CDK, monitoring)

**AI MUST ask which phase before starting any Phase 6 work.**

Before creating ANY Phase 6 design document, verify ALL of the following:

**Planning:**
- [ ] Clarify if this is Phase 6A (Application) or 6B (Infrastructure)
- [ ] Use Plan agent if creating 3+ design documents
- [ ] Plan agent outlines: document structure, dependencies, creation sequence
- [ ] Load `@processes/PHASE_6_DESIGN_GUIDELINES` for comprehensive checklist

**Phase 6A Application Design Checklist:**
- [ ] Define features and functionality
- [ ] Document user flows and interactions
- [ ] Design application APIs (endpoints, contracts)
- [ ] Define data models and business entities
- [ ] Design UI/UX wireframes (if applicable)
- [ ] Document business logic and validation rules
- [ ] Specify application I/O contracts

**Phase 6B Infrastructure Design Checklist:**
- [ ] Design AWS architecture (services, components, data flow)
- [ ] Define CDK stacks or Terraform modules
- [ ] Design networking (VPC, security groups, load balancers)
- [ ] Configure monitoring and alarms (CloudWatch, X-Ray)
- [ ] Design CI/CD pipeline (GitHub Actions, CodePipeline)
- [ ] Document security controls (IAM, encryption, secrets)

**Tech Stack Verification:**
- [ ] Read `hmode/guardrails/tech-preferences/` for ALL relevant categories:
  - infrastructure.json (AWS services, IaC, monitoring, CI/CD)
  - ai-ml.json (LLMs, embeddings, ASR, TTS, OCR)
  - frontend.json (frameworks, UI libraries, styling)
  - backend.json (APIs, databases, auth)
- [ ] Use EXACT versions from guardrails (e.g., "Claude Sonnet 4.5" not "Claude 3.5")
- [ ] Use rank 1 preferences unless specific use case requires alternative
- [ ] If no guardrail exists → ask human for approval FIRST

**Architecture Alignment:**
- [ ] Check `hmode/guardrails/architecture-preferences/` for patterns
- [ ] Verify AWS monitoring requirements (CloudWatch + X-Ray REQUIRED per infrastructure.json:92-108)
- [ ] Confirm IaC tool is AWS CDK (not SAM/CloudFormation per infrastructure.json:421)

**Violation Response:**
If ANY checkbox unchecked → STOP and fix before continuing.

**Common Violations to Avoid:**
- ❌ Using older model versions (Claude 3.5 instead of Sonnet 4.5)
- ❌ Using non-preferred IaC (SAM instead of CDK)
- ❌ Using outdated framework versions (Next.js 14 instead of 15.x)
- ❌ Missing required monitoring (CloudWatch + X-Ray mandatory for AWS)

**Full Guidelines:** See `@processes/PHASE_6_DESIGN_GUIDELINES`

### 6.3 Pre-Code Checklist (MANDATORY)

Before writing ANY code (imports, functions, classes, configs), verify ALL of the following:

**Phase Verification:**
- [ ] `.project` file exists in current directory
- [ ] Phase number is 8, 9, or explicitly declared SPIKE
- [ ] If phase < 8: STOP - explain SDLC violation, offer phase advancement
- [ ] If SPIKE: Confirm with user this is throwaway/prototype code (max 3 days)

**Technical Approval:**
- [ ] Tech stack human-approved OR already in `hmode/guardrails/tech-preferences/`
- [ ] Architecture decisions confirmed (no assumptions on frameworks/patterns)
- [ ] Domain models checked against `hmode/shared/semantic/domains/registry.yaml`

**Test-Driven Development:**
- [ ] If Phase 7: Write tests ONLY (no implementation code)
- [ ] If Phase 8: Tests already exist from Phase 7 OR write tests first

**Persona Requirement:**
- [ ] Target user/persona identified (NEVER "TBD" - infer and confirm)

**Violation Response:**
If ANY checkbox unchecked → Refuse code writing with:
```
Cannot write code - checklist incomplete:
- Current phase: {phase_number}
- Missing: {unchecked_items}

Options:
[1] Continue current phase activities ({phase_name})
[2] Advance to Phase 8 (Implementation)
[3] Declare SPIKE mode (throwaway prototype, max 3 days)
```

**Full Flow:** See `@processes/SDLC_OVERVIEW`

---

## 7.0 TECHNICAL STANDARDS

### 7.1 Infrastructure
- **ALWAYS use AWS CDK** for infrastructure
- **ONLY use AWS CLI/boto3** when explicitly requested
- **NEVER use `aws s3 cp`** to publish files - use `hmode/shared/tools/s3publish.py`
- **NEVER publish microsites to CloudFront + S3** - always use **AWS Amplify**
- **ALWAYS include `--profile <profile>`** in every AWS CLI command — NEVER run `aws` commands without an explicit profile

### 7.2 Typing
- ALWAYS use type hints (Python)
- ALWAYS use TypeScript (not JavaScript)

### 7.3 Data Grounding
- NEVER invent contacts, library names, versions, technical details
- ALL domain models MUST include `created_at` and `updated_at` fields
- ALWAYS decompose domain models into atomic, reusable components

### 7.4 File Size
- Keep files under 300-500 lines
- Decompose larger files into modules

### 7.5 Testing
- ALWAYS test after creating something
- Use curl for APIs, Playwright MCP for web UIs
- Verify S3 URLs work after publishing

### 7.6 Tool Selection
- Evaluate GitHub stars, last commit, committers before adopting

### 7.7 Deployment Process

**CRITICAL: When user requests "deploy [project] to [context]:[env]", execute ALL phases below. NEVER stop after infrastructure - always complete full end-to-end deployment.**

#### 7.7.1 Amplify Deployment (AWS Amplify Apps)

**TRIGGER:** NextJS or Vite project deployment to AWS Amplify

**INVOKE:** Spawn `amplify-deploy-specialist` agent when:
- Deploying NextJS or Vite apps to Amplify
- Configuring amplify.yml or buildspecs
- Attaching custom domains via Route 53
- Troubleshooting Amplify build failures
- Reusing existing Amplify branches (main, prod, stage, dev)

**AGENT RESPONSIBILITIES:**
1. Initial Amplify app setup and configuration
2. Deploy to existing Amplify apps (reuse branches)
3. Configure buildspecs and amplify.yml
4. Attach custom domains via Route 53
5. Troubleshoot build failures using boto3/AWS API
6. Verify deployment success with smoke tests

**WORKFLOW:**
```
User requests Amplify deployment
     ↓
Spawn amplify-deploy-specialist
     ↓
Agent handles: setup → deploy → domain → verify
     ↓
Report deployment URL and status
```

**OUTPUT:**
- Deployed Amplify app URL
- Custom domain configuration (if applicable)
- Build logs and status
- Smoke test results

**DO NOT manually execute Amplify deployments - always delegate to this agent.**

#### 7.7.2 CDK/Terraform Deployment (Non-Amplify Infrastructure)

**TRIGGER:** CDK, Terraform, CloudFormation, or general infrastructure deployment

**INVOKE:** Spawn `infra-sre` agent when:
- Deploying CDK stacks
- Deploying Terraform configurations
- Setting up monitoring/alarms
- Configuring CI/CD pipelines
- Managing infrastructure lifecycle

**AGENT RESPONSIBILITIES:**
1. Follow standard Makefile deployment pattern
2. Implement Capistrano-style deployment history
3. Configure monitoring and alarms
4. Manage secrets securely
5. Document deployment procedures
6. Verify deployment with smoke tests

**Standard Makefile Targets:**
```makefile
make infra-bootstrap  # One-time bootstrap (CDK bootstrap, foundational resources)
make infra-deploy     # Deploy the stack (with Capistrano-style history)
make infra-destroy    # Destroy resources
```

**Key Features:**
- Capistrano-style deployment history with timestamped releases
- Atomic deploys via symlink switching
- Keep last 5 releases for easy rollback
- Git-tracked audit trail

**Full Makefile template, project structure, and usage:** `hmode/shared/standards/deployment/MAKEFILE_TEMPLATE.md`

**DO NOT manually execute CDK/Terraform deployments - delegate to infra-sre agent when possible.**

#### 7.7.3 Complete End-to-End Deployment Workflow

When user requests non-Amplify deployment AND manual execution is needed, execute ALL five phases sequentially. NEVER present as "complete" until all phases are done:

**Phase 1: Infrastructure Deployment**
- Update/create environment-specific config files
- Run `make infra-deploy CONTEXT=X ENV=Y`
- Capture stack outputs (URLs, ARNs, IDs)
- Verify CloudFormation stack is CREATE_COMPLETE

**Phase 2: DNS Configuration** (if custom domains exist)
- Extract domain names from stack outputs
- Use Route53 API to create/update A or CNAME records
- For Amplify apps: Point to Amplify default domain
- For CloudFront: Point to CloudFront distribution
- Verify DNS propagation with `dig` or `nslookup`

**Phase 3: Service Configuration Updates**
- Update Cognito callback URLs with new environment domains
- Update API Gateway custom domains (if applicable)
- Update CORS origins in API configs
- Update OAuth provider redirect URLs
- Verify all service configurations via AWS Console or CLI

**Phase 4: Frontend Build & Deployment** (if frontend exists)
- Create environment-specific `.env` file with stack outputs
- Run `npm run build` with correct env vars
- Deploy to Amplify via upload script or git push
- Wait for Amplify build to complete
- Capture deployment URL and build ID

**Phase 5: Verification & Testing**
- Test custom domain URLs (should return HTTP 200)
- Test Amplify default URLs (should return HTTP 200)
- Run smoke tests if available
- Test authentication flow end-to-end
- Verify deployed git hash matches expected version
- Report any failures immediately

**Deployment Completion Checklist:**
```
✅ Infrastructure deployed (CloudFormation stack exists)
✅ DNS records configured (custom domains resolve)
✅ Service configs updated (Cognito, API Gateway, etc.)
✅ Frontend deployed (Amplify build complete)
✅ URLs tested (all return HTTP 200)
✅ Authentication works (can sign in and get tokens)
```

**NEVER say "deployment complete" or "Would you like me to help with next steps?" until ALL boxes are checked.**

### 7.8 WebSocket Security
- **ALWAYS use `wss://`** (secure WebSocket) - NEVER use `ws://`
- This applies to ALL socket connections: client-side, server-side, and configuration
- Insecure `ws://` connections expose data to interception and MITM attacks

### 7.9 File UUID Standard
Every file MUST include a UUID comment for integrity tracking:

**Placement:** After file header/docstring, before imports/code

**Format by Language:**
| Language | Format |
|----------|--------|
| Python | `# File UUID: f47ac10b-58cc-4372-a567-0e02b2c3d479` |
| TypeScript/JS | `// File UUID: a3d8f912-6e4c-4b7f-9c2d-1e5a8b3c7d9f` |
| Markdown | `<!-- File UUID: 7b9e2f4c-1a3d-4e8b-9f2c-5d6a7e8f9b0c -->` |
| YAML | `# File UUID: c5e8a9f2-3d4b-4c7e-9a1f-2b3c4d5e6f7g` |

**Benefits:** Track files across renames, create stable links (`repo://f47ac10b`), enable automated tooling

### 7.10 Frontend Buildinfo Pattern
ALL deployed frontend apps (Vite, Next.js, React, static HTML) MUST include `buildinfo.json`:

**Quick Reference:**
- Use `hmode/shared/tools/generate-buildinfo.py` after build
- Includes: git metadata (hash, branch), infrastructure ARNs (CloudFront, S3, Cognito), deployment info
- Makefile targets: `make buildinfo` or `make build-with-info`

**Full documentation, JSON schema, and examples:** `hmode/shared/tools/BUILDINFO_PATTERN.md`

### 7.11 Post-Deploy Smoke Tests
Every deployed app MUST have a smoke test that runs after deployment.

**Required:**
- Git hash verification (expose via meta tag or /health endpoint)
- Verify deployed hash matches expected version

**Recommended:**
- Playwright test to verify page renders without errors

**Critical:**
- Use canonical domain (e.g., `mo.b.lfg.new`) NOT temporary CloudFront/Amplify URLs
- Catches wrong version deploys, CDN issues, DNS problems

**Full implementation pattern, examples, and Makefile targets:** `hmode/shared/standards/testing/SMOKE_TEST_PATTERN.md`

---

## 8.0 CAPABILITIES & TOOLS

### 8.1 Asset Generation
- XLSX, PDF, HTML, audio, images, SVG, diagrams
- When generating multiple: "Now generating [N] [type] files: [brief description]"

**Asset Metadata Standards:**
Every generated asset MUST include:
1. **Design System Alignment:** Use colors/styles from `hmode/shared/design-system/` (HSL variables)
2. **Project Context:** Project UUID (or component name for shared assets)
3. **Asset UUID:** Unique 8-char ID (e.g., `viz-pipeline-a7f3b2c1`)
4. **Date:** Creation date in ISO format
5. **Versioning:** Append `.v1`, `.v2`, `.v3` for new versions (e.g., `asset-a7f3b2c1.v2`)
6. **Diagram Element IDs:** Use decimal format (1.0, 1.1, 2.0, 2.1) for all diagram elements
7. **Atomic Level:** Classify as atom | molecule | organism | template | page
8. **Tokens Used:** List design tokens for colors, spacing, typography

**Asset Header Template (HTML/SVG):**
```html
<!--
  Asset: {descriptive-name}
  Project: {project-uuid}
  Asset ID: {asset-uuid}.v{N}
  Date: {YYYY-MM-DD}
  Design System: hmode/shared/design-system

  Atomic Level: {atom|molecule|organism|template|page}

  Tokens Used:
  - Colors: --background, --foreground, --primary, --muted
  - Spacing: space-4, space-6, space-8
  - Typography: text-base, text-lg, text-h2
-->
```

**Design System Enforcement:**
- See `@design-system/MANAGEMENT_GUIDELINES` for full rules
- See `@design-system/examples/compliant-mockup.html` for reference
- See `@design-system/examples/VALIDATION_REPORT` for checklist

### 8.2 Publishing
- S3 uploads with public URLs
- Asset bookmarks for quick access
- Phase reports with navigation

### 8.3 Integrations
- ElevenLabs (audio)
- Playwright MCP (web testing)
- AWS services
- Overwatch (local automation)

### 8.6 Local Automation (Optional)
<!-- [PROJECT-SPECIFIC: override in .claude/CLAUDE.md] -->
<!-- Add project-specific automation services here (file watchers, build daemons, etc.) -->

### 8.4 Testing
- curl for APIs
- Playwright for web UIs
- Immediate verification after creation

### 8.5 Sub-Agent Delegation
Aggressively delegate to minimize context window:
- Asset generation
- File uploads/publishing
- Research tasks
- Mockups/prototypes
- Batch operations
- Local development (SAM CLI, Docker Compose)

Launch multiple sub-agents in parallel when tasks are independent.

### 8.7 Local Development

**Agent:** `local-dev` | **Skill:** `/local-dev`

Manage local development environments for testing before deployment:

**SAM CLI Operations:**
- `sam build` - Build Lambda artifacts
- `sam local invoke` - Test function with event
- `sam local start-api` - Run local API Gateway
- `sam local generate-event` - Create sample events

**Docker Operations:**
- `docker-compose up/down` - Manage services
- Container logs and debugging
- Environment management

**Full Documentation:** `@processes/LOCAL_DEV_AGENT`

---

## 9.0 FILE & DIRECTORY ORGANIZATION

### 9.1 Monorepo Structure

```
your-project/
├── CLAUDE.md                   # Symlink → hmode/CLAUDE.md (shared methodology)
├── .claude/
│   ├── CLAUDE.md               # Local overrides (project-specific)
│   ├── commands/               # Symlink → ../hmode/commands/
│   ├── skills/                 # Symlink → ../hmode/skills/
│   ├── agents/                 # Symlink → ../hmode/agents/
│   ├── hooks/                  # Project-specific hooks (NOT symlinked)
│   └── settings.json           # Project-specific settings
├── hmode/                      # Git subtree (shared methodology)
│   ├── CLAUDE.md               # Full orchestrator
│   ├── bin/                    # CLI scripts (hmode-init, hmode-doctor, etc.)
│   ├── docs/                   # Core methodology documentation
│   │   ├── core/               # Fundamentals (9 files)
│   │   ├── processes/          # SDLC phases (20+ files)
│   │   ├── patterns/           # Design patterns (6 files)
│   │   └── reference/          # Reference info
│   ├── commands/               # Slash commands (154 files)
│   ├── skills/                 # Claude skills (28 items)
│   ├── agents/                 # Agent definitions (20 files)
│   ├── templates/              # SDLC templates
│   ├── guardrails/             # Tech/arch preferences
│   │   ├── tech-preferences/
│   │   ├── architecture-preferences/
│   │   └── ai-steering/
│   └── shared/                 # Shared resources
│       ├── golden-repos/       # Project templates (14)
│       ├── semantic/domains/   # Domain models (127+)
│       ├── standards/          # Code/testing/deployment standards
│       ├── design-system/      # Visual design system
│       ├── artifact-library/   # Reusable artifacts
│       ├── libs/               # Reusable libraries
│       ├── infra-providers/    # Cloud provider SOPs
│       └── tools/              # Utility scripts
└── (your project files)
```

### 9.2 Root Directory Hygiene
**FORBIDDEN in root:** Test files, temp files, scripts, loose doc files (*.md except core), config files
**ALLOWED in root:** Core files (CLAUDE.md, README.md, package.json, etc.) and organized directories (docs/, .claude/, etc.)

### 9.3 Naming Conventions
- **Ideas:** `{descriptive-slug}-{first-8-uuid-chars}.md`
- **Projects:** `{descriptive-name}-{5char-id}`
- **Domain models:** Lowercase, hyphenated

### 9.4 Classification
For new prototypes, ask: "work, personal, shared, unspecified, or oss?"

### 9.5 Available Golden Repo Templates

| Template | Tech Stack | Use Case |
|----------|------------|----------|
| `python-cli` | Click, Rich | CLI tools |
| `python-fastapi` | FastAPI, Pydantic | REST APIs |
| `python-general` | Python 3.13+ | General Python |
| `python-script` | Python | Single-file scripts |
| `typescript-cdk` | AWS CDK | Infrastructure |
| `typescript-email` | React Email | Email templates |
| `typescript-expo` | Expo, React Native | Mobile apps |
| `typescript-ink-cli` | Ink | Terminal UI apps |
| `typescript-nextjs` | Next.js, React | Full-stack web |
| `typescript-nodejs-api` | Express/Fastify | Node.js APIs |
| `typescript-nodejs-cli` | Commander | Node.js CLI |
| `typescript-react` | React, Vite | React SPAs |
| `typescript-vite` | Vite | Frontend apps |

### 9.6 Code Standards Available

| Standard | Location | Coverage |
|----------|----------|----------|
| Python | `hmode/shared/standards/code/python/` | Typing, structure, naming |
| TypeScript | `hmode/shared/standards/code/typescript/` | Types, ESLint, patterns |
| React | `hmode/shared/standards/code/react/` | Components, hooks, state |
| FastAPI | `hmode/shared/standards/code/fastapi/` | Routes, models, deps |
| Node.js | `hmode/shared/standards/code/nodejs/` | Express, async patterns |
| Pydantic | `hmode/shared/standards/code/pydantic/` | Models, validation |
| Pydantic AI | `hmode/shared/standards/code/pydantic-ai/` | AI agent patterns |
| Vite | `hmode/shared/standards/code/vite/` | Build, config |
| BAML | `hmode/shared/standards/code/baml/` | LLM prompts |
| React Email | `hmode/shared/standards/code/react-email/` | Email templates |

**Full Details:** See `@reference/DIRECTORY_STRUCTURE`

---

## 10.0 TROUBLESHOOTING & STATUS

### 10.1 Common Problems

**Problem: AI not loading correct file**
→ Check `.project` file for current phase
→ Verify phase name matches process file

**Problem: Missing context**
→ Explicitly request file: "Load @processes/DIVERGENT_MODE"
→ Or request: "Load all SDLC docs"

**Problem: Gates not firing**
→ Check intent classification in Section 2.0
→ Verify action type in Gate Trigger Matrix (5.1)

**Problem: Made incorrect claim about infrastructure**
→ Read `@reference/LEARNINGS` before making AWS infrastructure claims
→ ALWAYS verify with correct AWS profile before claiming something is missing
→ When user corrects you, immediately pivot and verify with correct credentials

### 10.15 Continuous Improvement & Learnings

**MANDATORY:** Read `@reference/LEARNINGS` in these situations:
- Before claiming AWS infrastructure doesn't exist
- After user corrects you about technical facts
- When investigating production failures
- Before making definitive statements about system state
- When adopting new patterns or avoiding past mistakes

**Key Learning Pattern:**
1. User corrects AI statement → High-signal feedback
2. Investigate root cause of incorrect claim
3. Document in `@reference/LEARNINGS`
4. Update CLAUDE.md if process change needed

**Recent Learnings (see `@reference/LEARNINGS` for full details):**
- AWS infrastructure verification: Always use correct profile from Section 1.4
- Parallel agent investigation: Effective for independent tasks
- Check existing code before claiming missing functionality
- Amplify zip structure: Files must be at root, not in dist/ folder
- Communication: Use uncertainty phrases when not verified

**Update Process:**
After significant mistakes or discoveries, update `@reference/LEARNINGS` with:
- What went wrong / What went right
- Root cause analysis
- Pattern to follow in future
- Verification checklist if applicable

### 10.2 Emergency Overrides
User can force full context:
- "Load all SDLC docs" - Load all process files
- "Load all patterns" - Load all pattern files
- "Load everything" - Load all doc files

### 10.3 Status
**Orchestrator Version:** 4.12.0 (Continuous Learning & Verification)
**Last Updated:** 2026-03-06
**Previous Version:** 4.11.0 (Local Dev Environment Agent)

**Version 4.12.0 Changes:**
- Added `@reference/LEARNINGS` for capturing real-world mistakes and patterns
- Added AWS verification rule in Section 1.4 "Always Required"
- Added Section 10.15 "Continuous Improvement & Learnings"
- Added learnings reference in Section 1.5 Quick Reference Table
- Updated Section 10.1 with infrastructure verification problem/solution
- Captures voice notes investigation learnings (AWS credentials, parallel agents, existing code checks)

**Version 4.11.0 Changes:**
- Added Local Dev Environment Agent for SAM CLI and Docker workflows
- Created `@processes/LOCAL_DEV_AGENT` comprehensive guide
- Created `/local-dev` skill for quick access
- Added LOCAL DEV mode to intent routing (Section 2.1)
- Updated Section 8.5 Sub-Agent Delegation with local dev
- Supports: sam build, sam local invoke, sam local start-api, docker-compose

**Version 4.10.0 Changes:**
- Added Gate 10: Migration Specialist Agent
- Created `@processes/MIGRATION_SPECIALIST_AGENT` comprehensive guide
- Updated Section 5.1 Gate Trigger Matrix with migration column
- Added migration workflow diagrams to Section 5.4
- Repository awareness: ~/dev/lab, ~/dev/awstools, ~/dev/hl-protoflow
- Git-safe migrations with history preservation, UUID tracking, rollback scripts

### 10.4 Repository Statistics
<!-- [PROJECT-SPECIFIC: override in .claude/CLAUDE.md] -->
<!-- Add project-specific stats here -->

---

## APPENDIX: CRITICAL RULES (Top 26)

**SDLC & Process:**
1. **9-Phase SDLC:** NO code until Phase 8
2. **Phase Detection:** ALWAYS read `.project` first
3. **Phase 6 Guardrails:** CHECK hmode/guardrails/tech-preferences/ BEFORE design docs (Section 6.25)
4. **Technology Approval:** Human-approved BEFORE implementing
5. **Confirmation Protocol:** Paraphrase → options → confirm
6. **Persona Inference:** NEVER TBD, always infer

**Data Integrity:**
7. **Data Grounding:** NEVER invent details
8. **Model Timestamps:** created_at, updated_at required
9. **Domain Reuse:** Check registry.yaml first
10. **Domain Decomposition:** Atomic, reusable components
11. **Reuse First:** Search hmode/shared/* before building (Section 1.4)

**Code Quality:**
12. **Strong Typing:** ALWAYS (Python hints, TypeScript)
13. **File Size:** 300-500 lines max
14. **Immediate Testing:** Test after creating
15. **Code Standards:** Check hmode/shared/standards/code/
16. **Path Abstraction:** Use config/env vars, not hardcoded paths

**Design System:**
17. **Design Tokens:** NEVER raw hex - use hsl(var(--token))
18. **Template First:** Start HTML from hmode/shared/design-system/templates/
19. **Visual Hierarchy:** MAX 3 levels (H1 > H2 > Body)
20. **Asset Metadata:** Include UUID, project, date, atomic level

**Infrastructure & Deployment:**
21. **AWS CDK First:** ALWAYS for infrastructure
22. **Standard Deployment:** Use make infra-bootstrap + infra-deploy
23. **Post-Deploy Smoke Tests:** Verify git hash matches deployed version
24. **WebSocket Security:** ALWAYS wss:// (never ws://)
25. **Frontend Buildinfo:** Include buildinfo.json with git metadata

**Workflow:**
26. **Sub-Agent Delegation:** Aggressively delegate to minimize context

**See Section 1.4 for environment constraints (S3, AWS guard, file UUIDs, publishing rules).**
**Full Details:** `@core/CRITICAL_RULES` and `@design-system/MANAGEMENT_GUIDELINES`

---

[END OF ORCHESTRATION HUB]
