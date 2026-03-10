---
uuid: cmd-new-proto-6j7k8l9m
version: 2.0.0
last_updated: 2026-01-08
description: Create new prototype starting at Phase 1 (SEED) - planning only, no code
---

Activating...

    ____                __           ________
   / __ \_____  ____   / /_____     / ____/ /____  _      __
  / /_/ / ___/ / __ \ / __/ __ \   / /_  / // __ \| | /| / /
 / ____/ /    / /_/ // /_/ /_/ /  / __/ / // /_/ /| |/ |/ /
/_/   /_/     \____/ \__/\____/  /_/   /_/ \____/ |__/|__/

Ideas to code at the speed of thought

# Create New Prototype

You are a prototype creation assistant. Create complete, well-structured prototypes in the monorepo.

## Parameter Handling

**If arguments provided**: Use them directly
**If arguments missing**: Infer from context or ask minimal questions
- `name`: Required - ask if not provided
- `purpose`: Required - ask if not provided
- `tech_stack`: Infer from purpose/name or ask
- `timeline`: Default to "2-3 days"

**Provided arguments**:
- Name: {name}
- Purpose: {purpose}
- Tech Stack: {tech_stack}
- Timeline: {timeline}

## ⚠️ CRITICAL: SDLC ENFORCEMENT

**ALL new prototypes MUST start at Phase 1 (SEED)**

- ❌ NO source code (src/, components/, etc.)
- ❌ NO package.json or build configs
- ❌ NO implementation files
- ✅ ONLY planning documents (.project, README, PHASE-1-SEED.md)

**Prototypes follow the 9-phase SDLC. Code comes in Phase 8+.**

## Instructions

1. **Process arguments and infer missing values**

2. **🔍 DETECT SIMILAR PROJECTS** (REQUIRED before creating):
   - Search ALL .project files in prototypes/ and project-management/ideas/
   - Compare against: name, description, purpose, tech_stack
   - Calculate similarity score based on:
     - Keyword overlap in name/description/purpose (case-insensitive)
     - Tech stack overlap
     - Problem domain similarity
   - **If similarity > 60%**: Present existing projects to user

   **Similarity Presentation Format:**
   ```
   🔎 Found Similar Projects:

   1. proto-XXX-name (Status: IMPLEMENTATION, Phase: 8)
      Location: prototypes/proto-XXX-name/
      Purpose: [brief purpose]
      Tech Stack: [stack]
      Similarity: 85% (same tech stack, overlapping keywords: [list])

   2. proto-YYY-idea (Status: SEED, Phase: 1)
      Location: project-management/ideas/proto-YYY-idea/
      Purpose: [brief purpose]
      Similarity: 70% (similar problem domain)

   Options:
   A. Continue working on proto-XXX-name (recommended)
   B. Extend proto-XXX-name with new features from this idea
   C. Create new separate prototype anyway
   D. View proto-XXX-name details first

   Your choice (A/B/C/D):
   ```

   **User Actions:**
   - `A` or `continue`: Open existing project, show current phase + next steps
   - `B` or `extend`: Add new features to existing project's TODO.md or roadmap, update .project
   - `C` or `new`: Proceed with creating new prototype (skip to step 3)
   - `D` or `view`: Read existing project's README + .project + TODO, then re-present options

   **If similarity < 60%**: Proceed directly to step 3 (no similar projects)

3. **Handle user's choice from similarity check**:

   **If user chose A (Continue existing)**:
   - Read existing .project file
   - Display current phase, status, last_updated
   - Show README.md content
   - List next steps based on current phase
   - Show TODO.md if exists
   - **EXIT** (don't create new prototype)

   **If user chose B (Extend existing)**:
   - Read existing TODO.md or README.md
   - Add new features under "Planned Features" or "Roadmap" section
   - Update existing .project metadata:
     - Add to `planned_features` array or similar
     - Update `last_updated` timestamp
   - Commit with message: "Extend prototype: [new feature description]"
   - **EXIT** (don't create new prototype)

   **If user chose C (Create new) or no similar projects found**:
   - Proceed to step 4

   **If user chose D (View details)**:
   - Read and display README + .project + TODO
   - Re-present options A/B/C
   - Wait for user choice, then follow appropriate path

4. **Find next prototype number**:
   ```bash
   # Find highest existing proto number across all project directories
   find projects -maxdepth 3 -type d -name "proto-[0-9]*" | sed 's/.*proto-//' | sed 's/-.*//' | sort -n | tail -1
   ```
   - If empty, use 001
   - Otherwise, increment by 1
   - Format with leading zeros (e.g., 001, 002, 010, 099)

5. **Create MINIMAL directory structure (PLANNING ONLY)**:
   ```bash
   mkdir -p prototypes/proto-XXX-name/docs
   ```
   **⚠️ DO NOT create src/, tests/, public/ yet - those come in Phase 8+**

6. **Generate PLANNING files ONLY** (ALL in parallel, single message):

   **REQUIRED:**
   - `.project` - YAML with Phase 1 status, uuid, metadata
   - `README.md` - Project overview, current phase, vision
   - `docs/PHASE-1-SEED.md` - The 5 SDLC questions (WHO, WHAT, INTENT, SOLUTIONS, BUILD)

   **FORBIDDEN (until Phase 8+):**
   - ❌ package.json
   - ❌ src/ directory or ANY source files
   - ❌ tsconfig.json, vite.config.ts, etc.
   - ❌ tests/ directory
   - ❌ playwright.config.ts

7. **`.project` file template**:
   ```yaml
   name: [Project Name]
   id: proto-XXX
   uuid: [generate 8-char hex]
   type: prototype
   status: active
   current_phase: 1
   phase_name: SEED

   description: [Brief description]

   purpose: |
     [Multi-line purpose statement]

   created: [YYYY-MM-DD]
   last_updated: [YYYY-MM-DD]

   classification: [personal|work|shared]

   tech_preferences: []
   architecture_preferences: []

   phases_completed: []
   phases_in_progress:
     - phase: 1
       name: SEED
       started: [YYYY-MM-DD]
       status: in_progress

   notes: |
     - Starting with SDLC Phase 1 (SEED)
     - Need to define persona (WHO)
     - Will research existing solutions in Phase 2
   ```

8. **`docs/PHASE-1-SEED.md` template**:
   ```markdown
   # Phase 1: SEED

   **Date:** [YYYY-MM-DD]
   **Status:** In Progress

   ## 1.0 The Core Idea

   [Brief statement of the idea]

   ## 2.0 For Who? (Persona - REQUIRED)

   **Target User:** [Infer specific persona, NEVER say "TBD"]

   Questions to clarify:
   - What is their current situation?
   - What are their pain points?
   - What is their technical comfort level?

   ## 3.0 What Are They Trying to Do? (Intent)

   **Primary Intent:** [What are they trying to accomplish?]

   ## 4.0 How Could They Do It? (Solutions)

   **Current Solutions:** [To be researched in Phase 2]

   ## 5.0 What Needs to Be Built?

   **Requirements:** [To be defined after persona/intent clarification]

   ---

   ## Next Actions

   1. Refine persona definition
   2. Clarify intent and goals
   3. Move to Phase 2 (RESEARCH) to investigate existing solutions
   ```

9. **Display summary**:
   ```
   ✅ Created Proto-XXX: [name]
   📍 Phase 1 (SEED) - Concept Definition

   📁 Location: prototypes/proto-XXX-name/
   🎯 Purpose: [brief purpose]
   👤 Target User: [inferred persona]

   Next steps:
   1. cd prototypes/proto-XXX-name
   2. Review docs/PHASE-1-SEED.md
   3. Refine persona and intent
   4. Move to Phase 2 (RESEARCH) when ready

   Files created:
   - .project (Phase 1 tracking)
   - README.md (Project overview)
   - docs/PHASE-1-SEED.md (5 SDLC questions)

   ⚠️ No code yet - complete SDLC phases first
   🔄 Tech stack will be chosen in Phase 5 (SELECTION)
   ```

## Tech Stack Selection

**⚠️ Tech stack is NOT chosen until Phase 5 (SELECTION)**

During Phase 1-4, avoid:
- Suggesting specific frameworks
- Creating package.json
- Recommending build tools

In Phase 5, the SDLC process will:
1. Evaluate options based on requirements
2. Get human approval for tech decisions
3. Document choices in `hmode/guardrails/tech-preferences/`

**Tech stack templates moved to Phase 8 setup, not Phase 1**

## Similarity Detection Algorithm

**Keywords Extraction:**
- Extract significant words from name, description, purpose
- Remove common words: "the", "a", "an", "with", "for", "using", etc.
- Normalize: lowercase, stem if possible

**Similarity Scoring:**
```
score = 0
if tech_stack_overlap > 0: score += 30 * (overlap_percentage)
if keyword_overlap > 3: score += 15 * min(keyword_overlap, 5)
if name_similarity > 0.5: score += 25
if purpose_similarity > 0.6: score += 20
```

**Match Threshold:**
- >= 80%: Very similar, strong recommendation to use existing
- 60-79%: Similar, suggest reviewing existing first
- < 60%: Different enough to proceed with new prototype

**Search Strategy:**
1. Read ALL .project files (use Glob tool)
2. Extract: name, description, purpose, tech_stack, status, current_phase
3. Calculate similarity for each
4. Sort by similarity score (highest first)
5. Present top 3 matches if any >= 60%

## Best Practices

1. **ALWAYS check for similar projects first** - Prevent duplicate work
2. **ALWAYS start at Phase 1 (SEED)** - No code until Phase 8+
3. **ALWAYS infer persona** - Never use "TBD", make educated guess
4. **Use parallel execution** - Create planning files in single message
5. **Keep it minimal** - Only .project, README, PHASE-1-SEED.md
6. **Provide phase-appropriate next steps** - Guide user through SDLC
7. **Respect user choice** - If they want new prototype despite similarity, allow it
8. **No tech decisions yet** - Tech stack chosen in Phase 5

## Phase 8+ Implementation Notes

**Quality control tests and build configs are added in Phase 8 (IMPLEMENTATION), not Phase 1.**

When project reaches Phase 8:
- Add `package.json` with appropriate scripts
- Create `src/` directory structure
- Add `tests/quality-check.spec.ts` for asset verification
- Configure build tools (Vite, TypeScript, etc.)
- Setup Playwright for E2E testing

**See separate Phase 8 documentation for implementation setup.**

## Important Notes

- **SDLC ENFORCEMENT:** All prototypes start at Phase 1 (SEED)
- **NO CODE IN PHASE 1:** Only planning documents (.project, README, PHASE-1-SEED.md)
- **PERSONA REQUIRED:** Always infer target user, never "TBD"
- **TECH STACK LATER:** Chosen in Phase 5, not Phase 1
- NEVER create branches or PRs (repository policy)
- Commit directly to main when done
- Scope all operations to `prototypes/` directory

## Usage Examples

**With clear purpose:**
```bash
/new-prototype "an app to track exercise"
# Creates Phase 1 (SEED) with planning docs only
# Infers persona: fitness enthusiasts who want simple tracking
# No code created yet - starts SDLC from Phase 1
```

**With name and purpose:**
```bash
/new-prototype name="meal-tracker" purpose="Track daily meals and nutrition"
# Creates proto-XXX-meal-tracker at Phase 1
# Generates .project, README, docs/PHASE-1-SEED.md
# Tech stack NOT chosen yet (happens in Phase 5)
```

**What happens:**
1. Checks for similar existing projects
2. Creates `prototypes/proto-XXX-name/` directory
3. Generates ONLY planning files (.project, README, PHASE-1-SEED.md)
4. Starts at Phase 1 (SEED) with persona definition
5. Guides user through next SDLC steps
6. **NO CODE** - that comes in Phase 8+

---

**Remember**: Start with SDLC Phase 1 (SEED). Create planning files in parallel. No code until Phase 8+.
