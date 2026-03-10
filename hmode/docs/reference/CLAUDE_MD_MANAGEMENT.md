## 📂 CLAUDE.MD & .CLAUDE DIRECTORY MANAGEMENT

### Hierarchy & Purpose

**Root CLAUDE.md** (`/CLAUDE.md`):
- Monorepo-wide SDLC rules, standards, workflows
- 9-phase development process
- Shared conventions (git, writing style, structure)
- Default tech stack and tools
- **Applies to ALL prototypes** unless overridden

**Project CLAUDE.md** (`projects/{classification}/active/{name}-{5char}/CLAUDE.md`):
- Project-specific development guidelines
- Architecture decisions unique to this project
- Special workflows or agent configurations
- **Extends or overrides root** for this project only

### .claude Directory Structure

**Source of Truth:**
```
projects/shared/active/tools-claude-power-tools-commands-skills-4fskn/commands/
    └── 46 general-purpose commands
```

**Distribution:**
```
hmode/commands/
    └── 46 symlinks → power tools commands
```

**Project-Specific:**
```
projects/{classification}/active/{name}-{5char}/hmode/commands/
    └── Project-only commands (agents, workflows)
```

### Command Placement Rules

**Add to power-tools** (General):
- ✅ Reusable across projects
- ✅ SDLC workflows (/new-idea, /workon)
- ✅ Quality tools (/densify, /quality-control)
- ✅ Doc generators (/generate-project-presentation)
- ✅ Git/deploy helpers (/quick-commit, /publish)

**Keep in project/** (Specific):
- ✅ Domain agents (e.g., /company-agent for sales)
- ✅ Project-unique workflows
- ✅ Commands requiring project context
- ✅ Experimental/not-yet-generalized

### Installation

```bash
# Install power-tools commands (creates symlinks)
cd projects/shared/active/tools-claude-power-tools-commands-skills-4fskn
./install.sh
```

**Result:** All commands available as `/command-name` in Claude Code

### Updates

- Edit commands in `tools-claude-power-tools-commands-skills-4fskn/commands/` → changes propagate instantly via symlinks
- Version commands using YAML frontmatter (`version: 1.0.0`)
- Breaking changes require major version bump

### Examples

**Existing project-specific CLAUDE.md files:**
- `claude-person-searcher-iyauu/CLAUDE.md` - Sales intelligence agents
- `tool-aws-admin-weekly-progress-report-agent-3sw10/CLAUDE.md` - AWS report standards
- `poc-idp-ai-boundryml-self-refining-doc-to-rules-9xm65/CLAUDE.md` - Document parsing

