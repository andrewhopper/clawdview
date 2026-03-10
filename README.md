# hmode — Shared Claude Code Methodology

A portable, reusable methodology for Claude Code projects. Contains SDLC processes, slash commands, skills, agents, design system, code standards, golden repo templates, and guardrails.

## Quick Start

### Add to an existing project

```bash
# Add hmode as a git subtree
cd your-project
git subtree add --prefix=hmode git@github.com:andrewhopper/hmode.git main --squash

# Initialize symlinks
./hmode/bin/hmode-init
```

### What hmode-init does

1. Creates `./CLAUDE.md` symlink → `hmode/CLAUDE.md` (shared methodology)
2. Creates `.claude/commands` symlink → `../hmode/commands/` (154 slash commands)
3. Creates `.claude/skills` symlink → `../hmode/skills/` (28 skills)
4. Creates `.claude/agents` symlink → `../hmode/agents/` (20 agents)
5. Adds symlinks to `.gitignore`
6. Creates `.claude/CLAUDE.md` stub for project-specific overrides
7. Installs `post-checkout` git hook for symlink resilience

### CI/CD (copy mode)

Symlinks require `hmode-init` after clone. For CI/CD, use copy mode:

```bash
./hmode/bin/hmode-init --copy
```

## Three-Tier Loading

Claude Code loads CLAUDE.md in this order (later tiers override earlier):

1. **Global** — `~/.claude/CLAUDE.md` (user preferences)
2. **Project** — `./CLAUDE.md` → symlink to `hmode/CLAUDE.md` (shared methodology)
3. **Local** — `./.claude/CLAUDE.md` (project-specific overrides)

### Project-Specific Overrides

Put project-specific content in `.claude/CLAUDE.md`:

```markdown
# My Project Overrides

## AWS Credentials
| Profile | Account | Purpose |
|---------|---------|---------|
| my-profile | 123456789 | Production |

## Project Structure
- This is a Next.js monorepo with...

## Team Conventions
- We use Jira for tickets...
```

## Updating

```bash
# Pull latest changes
./hmode/bin/hmode-update

# Or manually:
git subtree pull --prefix=hmode git@github.com:andrewhopper/hmode.git main --squash
```

## Validation

```bash
./hmode/bin/hmode-doctor
```

Checks: symlinks, .gitignore entries, local override, post-checkout hook, freshness.

## Directory Structure

```
hmode/
├── CLAUDE.md               # Full orchestrator methodology
├── bin/                    # CLI scripts
│   ├── hmode-init          # Setup symlinks in host project
│   ├── hmode-doctor        # Validate installation
│   └── hmode-update        # Helper for subtree pull
├── docs/                   # Core methodology documentation
│   ├── core/               # Critical rules, intent detection, guardrails
│   ├── processes/          # 9-phase SDLC, brownfield, migration
│   ├── patterns/           # Design patterns, parallel execution
│   └── reference/          # AWS, learnings, directory structure
├── commands/               # 154 slash commands
├── skills/                 # 28 skills (Python + MD)
├── agents/                 # 20 agent definitions
├── templates/              # SDLC phase templates
├── guardrails/             # Tech & architecture preferences
│   ├── tech-preferences/   # Approved tech stacks by category
│   ├── architecture-preferences/
│   └── ai-steering/        # AI guidance rules
└── shared/                 # Shared resources
    ├── golden-repos/       # 14 project starter templates
    ├── standards/          # Code, testing, deployment standards
    ├── design-system/      # Tokens, templates, guidelines
    ├── semantic/domains/   # 127+ domain models
    ├── libs/               # Reusable libraries
    ├── artifact-library/   # Reusable artifacts
    ├── infra-providers/    # Cloud provider SOPs
    └── tools/              # Utility scripts
```

## What's Included

| Category | Count | Description |
|----------|-------|-------------|
| Slash Commands | 154 | From `/push` to `/workon` to `/research-phase` |
| Skills | 28 | Python handlers + MD definitions |
| Agents | 20 | Specialized agent definitions |
| Golden Repos | 14 | Project templates (Next.js, FastAPI, CDK, etc.) |
| Semantic Domains | 127+ | Reusable data models |
| Code Standards | 12 | Language/framework conventions |
| SDLC Phases | 9 | Full software development lifecycle |

## Contributing

Changes to hmode should be made in the standalone repo, then pulled into consumer projects:

```bash
# In the hmode repo
cd ~/dev/hmode
# Make changes, commit, push

# In consumer projects
cd ~/dev/my-project
./hmode/bin/hmode-update
```
