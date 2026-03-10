---
description: Interactive repo walkthrough for new team members
tags: [onboarding, documentation, training]
---

You are conducting an interactive repository walkthrough for a new developer joining the team.

## Context Detection

First, determine the scope:
1. Check if user specified a scope (e.g., "walkthrough .claude", "walkthrough SDLC", "walkthrough entire repo")
2. If no scope specified, offer menu:
   ```
   Walkthrough scope:
   [1] Full repo tour (45-60 min)
   [2] AI orchestration (.claude/) (15-20 min)
   [3] SDLC process (20-30 min)
   [4] Project structure (10-15 min)
   [5] Shared infrastructure (15-20 min)
   [6] Custom path
   ```

## Walkthrough Format

Use **progressive reveal** with checkpoints:

### Stage Format
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 STAGE N/M: [TOPIC NAME]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 What you'll learn:
- [Key concept 1]
- [Key concept 2]
- [Key concept 3]

📂 Files we'll explore:
- path/to/file1
- path/to/file2

⏱️ Time: [X] minutes

Ready? [y/n/skip]
```

### Explanation Style
- **2-3 paragraphs MAX** per concept
- **Visual aids:** ASCII diagrams, file trees, flow charts
- **Concrete examples** from actual repo code
- **"Why this matters"** section for each concept
- **Common pitfalls** section where relevant

### Interactive Elements
After each stage:
```
✓ Stage complete

Quick check:
Q: [Question to verify understanding]
A: [Expected answer]

Try it yourself:
[Hands-on task - 2-3 minutes]

Continue? [y/n/back/menu]
```

## Walkthrough Scripts by Scope

### [1] Full Repo Tour (7 stages)

**Stage 1/7: Overview & Philosophy**
- Show `tree -L 2`
- Explain AI-native monorepo concept
- Core principle: Test-Driven Development
- Key files: CLAUDE.md, .project, README.md
- **Try it:** Find your first `.project` file

**Stage 2/7: AI Orchestration (.claude/)**
- Show `.claude/` structure
- Explain dynamic documentation loading (80% token reduction)
- Walk through `commands/`, `docs/`, `hooks/`
- Show example: how `/push` command works
- **Try it:** Read one slash command file

**Stage 3/7: 9-Phase SDLC**
- Explain phases 1-9 with visual flow
- Show `.project` file structure
- Explain phase gates (2.5, 5.5, 8.5)
- **NO CODE until Phase 8** rule
- **Try it:** Identify current phase of an active prototype

**Stage 4/7: Project Lifecycle**
- Ideas vs Prototypes distinction
- Semantic versioning tied to phases (0.x → 1.x → 2.x)
- Manifest system (auto-updates)
- Git workflow (direct-to-main, no branches)
- **Try it:** Read a `.project` file, identify its phase

**Stage 5/7: Guardrails & Approval**
- Protected files in `hmode/guardrails/`
- Tech preferences workflow
- Human approval requirements
- Why this matters: consistency at scale
- **Try it:** Check what tech is approved in `tech-preferences/`

**Stage 6/7: Shared Infrastructure**
- Golden Repos (9 templates)
- Code Standards (`hmode/shared/standards/code/`)
- Domain Models (`hmode/hmode/shared/semantic/domains/`)
- Artifact Library
- **Try it:** Browse one golden repo

**Stage 7/7: Developer Workflow**
- Using slash commands
- Phase transitions
- Test-first development
- Commit workflow
- **Try it:** Use `/list-prototypes` command

### [2] AI Orchestration Tour (5 stages)

**Stage 1/5: The Orchestrator (CLAUDE.md)**
- 80% token reduction via modular docs
- Path aliases (@core/, @processes/, etc.)
- Dynamic loading based on context
- **Try it:** Find where INTENT_DETECTION is referenced

**Stage 2/5: Slash Commands**
- 46+ custom commands
- Categories: prototyping, git, QA, research, delivery
- How commands work (markdown + YAML frontmatter)
- **Try it:** Read `/push` command, explain what it does

**Stage 3/5: Modular Documentation**
- 4 directories: core/, processes/, patterns/, reference/
- Load on-demand based on phase
- Show CRITICAL_RULES.md (always active)
- Show INTENT_DETECTION.md (request classification)
- **Try it:** Navigate to a phase file, read the rules

**Stage 4/5: Hooks & Automation**
- Session lifecycle hooks
- Event publishing (ZeroMQ)
- Post-commit manifest updates
- **Try it:** Check `.claude/hooks/` directory

**Stage 5/5: Settings & Permissions**
- settings.json (auto-approvals)
- settings.local.json (local overrides)
- Tool permissions
- Git configuration
- **Try it:** Find auto-approved bash commands

### [3] SDLC Process Tour (6 stages)

**Stage 1/6: The 9 Phases**
- Visual flow diagram
- Phase 1-6: NO CODE (planning)
- Phase 7: Tests FIRST (TDD RED)
- Phase 8: Code to pass tests (TDD GREEN)
- Phase 9: Polish & UAT
- **Try it:** Name the 9 phases from memory

**Stage 2/6: Phase Gates**
- Phase 2.5: Feasibility (production only)
- Phase 5.5: PRD (production only)
- Phase 8.5: QA validation (web/UI only)
- Go/no-go decisions
- **Try it:** When would you use Phase 2.5?

**Stage 3/6: Project Types**
- exploration (learning)
- prototype (POC)
- production (real users)
- Which gates apply to each
- **Try it:** Classify a project as exploration/prototype/production

**Stage 4/6: The .project File**
- Single source of truth
- Required fields
- Semantic versioning (0.x → 1.x → 2.x)
- Phase history tracking
- **Try it:** Read a `.project` file, identify version

**Stage 5/6: Special Modes**
- SPIKE: Skip to code (max 3 days, throwaway)
- DIVERGENT: N parallel implementations (8.1 → 8.2 → 8.3)
- When to use each
- **Try it:** When would you use SPIKE mode?

**Stage 6/6: Test-First Development**
- Phase 7: Write tests (must fail)
- Phase 8: Write code (make tests pass)
- Track A (20-30% coverage) vs Track B (80%+ coverage)
- Reference examples in `hmode/shared/standards/code/`
- **Try it:** Explain TDD in 2 sentences

### [4] Project Structure Tour (4 stages)

**Stage 1/4: Directory Layout**
- Show `tree -L 2`
- Top-level directories explained
- Ideas vs Prototypes distinction
- Shared vs project-specific code
- **Try it:** Navigate to prototypes directory

**Stage 2/4: Naming Conventions**
- Format: `proto-name-xxxxx-NNN`
- UUID generation (5 chars)
- Sequential numbering
- XIP tagging for AWS IP
- **Try it:** Generate a 5-char UUID

**Stage 3/4: Metadata Flow**
- .project → manifest → README tables
- Auto-updates via git hooks
- Portfolio site integration
- **Try it:** Find the manifest file

**Stage 4/4: File Organization**
- Root hygiene rules
- Project subdirectories
- Shared resources
- Documentation structure
- **Try it:** Where would you put a new utility script?

### [5] Shared Infrastructure Tour (5 stages)

**Stage 1/5: Golden Repos**
- 9 production-ready templates
- Python (script, FastAPI, general)
- TypeScript (Next.js, React, Node, Vite, CDK, Email)
- Multi-environment config
- **Try it:** Browse one golden repo

**Stage 2/5: Code Standards**
- Reference patterns by tech stack
- Location: `hmode/shared/standards/code/`
- 10 tech stacks covered
- Always check before implementing
- **Try it:** Find the React code standards

**Stage 3/5: Domain Models**
- Typed models in `hmode/hmode/shared/semantic/domains/`
- 29+ models
- Reusable across projects
- Registry in `registry.yaml`
- **Try it:** Find one domain model

**Stage 4/5: Artifact Library**
- Document templates
- AI generation prompts
- Best-in-class examples
- Schema in `schema.yaml`
- **Try it:** Browse artifact catalog

**Stage 5/5: Tools & Scripts**
- Python utilities (`hmode/shared/tools/`)
- Node/TS scripts (`shared/scripts/`)
- Pub-Sub system (ZeroMQ)
- S3 publisher
- **Try it:** Find the S3 publish tool

## Command Execution

When user runs `/walkthrough [scope]`:

1. **Detect scope** (or show menu)
2. **Load appropriate script** from above
3. **Execute stage-by-stage** with pauses
4. **Wait for user input** after each stage (y/n/skip/back/menu)
5. **Track progress** (Stage N/M indicator)
6. **Provide hands-on tasks** for active learning
7. **Answer questions** inline when user asks
8. **Generate summary** at end with key takeaways

## Response to User Input

- **y** → Continue to next stage
- **n** → End walkthrough, provide summary of what was covered
- **skip** → Skip current stage, go to next
- **back** → Go back one stage
- **menu** → Return to scope selection menu
- **help** → Show keyboard shortcuts
- **?** → Answer clarifying question about current stage

## Example Interaction

```
User: /walkthrough SDLC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 STAGE 1/6: The 9 Phases
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 What you'll learn:
- The complete 9-phase SDLC flow
- Why "NO CODE until Phase 8" matters
- Test-Driven Development approach

📂 Files we'll explore:
- hmode/docs/processes/SDLC_OVERVIEW.md
- CLAUDE.md (section 6.2)

⏱️ Time: 5 minutes

Ready? [y/n/skip]

User: y

[Stage 1 content displayed]

✓ Stage complete

Quick check:
Q: At what phase do you write tests?
A: Phase 7

Try it yourself:
Open hmode/docs/processes/SDLC_OVERVIEW.md and identify the phase names

Continue? [y/n/back/menu]
```

## Summary Generation

At the end, provide:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 WALKTHROUGH COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 What we covered:
- [Bullet list of topics]

🔑 Key takeaways:
1. [Most important concept]
2. [Second most important]
3. [Third most important]

📚 Recommended next steps:
- [Suggested activity 1]
- [Suggested activity 2]

💡 Pro tip:
[One expert-level insight]

Questions? Ask me anything about what we covered.
```

## Error Handling

If user specifies invalid scope:
```
Scope "[user input]" not recognized.

Available scopes:
- full (entire repo)
- claude (AI orchestration)
- sdlc (9-phase process)
- structure (project layout)
- shared (infrastructure)
- Custom: /walkthrough path/to/directory
```

## Adaptive Pacing

Monitor user engagement:
- If user skips 3+ stages → Offer condensed version
- If user asks detailed questions → Offer deeper dive
- If user seems confused → Go back, re-explain with different example
- If user completes quickly → Suggest advanced walkthrough

## Final Notes

- **Keep it conversational** but structured
- **Use emojis** for visual landmarks
- **Provide concrete examples** from repo
- **Pause frequently** for questions
- **Make it actionable** with "Try it yourself" tasks
- **Celebrate completion** with summary + next steps
