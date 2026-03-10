# ProtoFlow Plugin Naming Conventions

<!-- File UUID: f3c8e2b7-9a1d-4f6e-8b2c-5d7a9e3f1b4c -->

**Version:** 1.0.0
**Last Updated:** 2026-02-04
**Status:** Active

## Overview

This document defines naming conventions for all ProtoFlow plugin components: agents, commands, skills, tools, and scripts. Consistent naming improves discoverability, reduces confusion, and establishes clear patterns for contribution.

## Quick Reference Table

| Component | Location | Convention | Example |
|-----------|----------|------------|---------|
| **Agent** | `hmode/agents/` | `{domain}-{role}.md` | `amplify-deploy-specialist.md` |
| **Command** | `hmode/commands/` | `{action}-{noun}.md` | `generate-domain.md` |
| **Skill** | `hmode/skills/protoflow/` | `protoflow:{action}` | `protoflow:contribute` |
| **Tool** | `hmode/shared/tools/` | `{verb}-{noun}.py` | `guardrail-enforce.py` |
| **Script** | `bin/` | `{verb}_{noun}.py` | `auto_merge_branches.py` |

## 1. Agent Naming

**Location:** `hmode/agents/*.md`

**Pattern:** `{domain}-{role}.md`

**Format:**
- Use kebab-case (lowercase with hyphens)
- Structure: `{domain}-{role}`
  - `domain`: Technology/service area (e.g., `amplify`, `cognito`, `infra`)
  - `role`: Agent's function (e.g., `specialist`, `expert`, `agent`)

**Role Suffixes:**
- `-specialist`: Deep expertise in specific technology (e.g., `amplify-deploy-specialist`)
- `-agent`: General-purpose autonomous agent (e.g., `ux-component-agent`)
- `-expert`: Advisory/consultative role (e.g., `cognito-expert-agent`)

**Examples:**
- ✅ `amplify-deploy-specialist.md` - Deploys to AWS Amplify
- ✅ `cognito-expert-agent.md` - Cognito configuration and troubleshooting
- ✅ `infra-sre.md` - Infrastructure and SRE operations
- ✅ `domain-modeling-specialist.md` - Domain model creation and evolution
- ✅ `ux-component-agent.md` - UI component composition
- ✅ `information-architecture-agent.md` - IA design and user flows

**Naming Rules:**
1. Agent name must match filename (without `.md`)
2. Use descriptive domain names (not abbreviations unless widely known)
3. Avoid redundant words (e.g., `aws-amplify-specialist` → `amplify-specialist`)
4. Keep under 40 characters total
5. No generic names (e.g., `helper-agent`, `utility-agent`)

**YAML Frontmatter:**
```yaml
---
name: amplify-deploy-specialist
description: Deploy and manage AWS Amplify applications
model: sonnet
color: red
uuid: <uuid>
---
```

## 2. Command Naming

**Location:** `hmode/commands/*.md`

**Pattern:** `{action}-{noun}.md`

**Format:**
- Use kebab-case (lowercase with hyphens)
- Structure: `{action}-{noun}` or `{action}-{noun1}-{noun2}`
  - `action`: Verb describing what the command does
  - `noun`: Target of the action

**Action Verbs (Preferred):**
- `generate` - Create new content (e.g., `generate-domain`, `generate-card`)
- `create` - Create new entity (e.g., `create-audiobook`)
- `add` - Add to existing (e.g., `add-observability`)
- `update` - Update existing (e.g., `update-dashboard`)
- `deliver` - Delivery operations (e.g., `deliver-assets`)
- `publish` - Publishing operations (e.g., `publish`, `upload`, `deploy`)
- `check` - Validation operations (e.g., `check-core`)
- `scan` - Security/audit operations (e.g., `scan-security`)
- `list` - Display operations (e.g., `list-prototypes`)
- `run` - Execution operations (e.g., `run`)
- `push` / `pull` - Git operations (e.g., `push-work`, `pull`)
- `merge` - Git merge operations (e.g., `auto-merge`)

**Examples:**
- ✅ `generate-domain.md` - Generate domain model types
- ✅ `arch-diagram.md` - Generate architecture diagrams
- ✅ `automate-test.md` - Automated browser testing
- ✅ `add-observability.md` - Add monitoring stack
- ✅ `deliver-assets.md` - Quick asset delivery
- ✅ `push-work.md` - Push to work remote
- ✅ `list-prototypes.md` - List all prototypes

**Shortcuts/Aliases:**
- Single-letter shortcuts should be symlinks: `a.md → architecture-research.md`
- Short aliases should be descriptive: `push.md`, `pull.md`
- Document shortcuts in command frontmatter

**YAML Frontmatter:**
```yaml
---
version: 1.0.0
last_updated: 2026-02-04
description: Brief description (shown in command listing)
tags: [category1, category2]
aliases: [/a, /arch]  # Optional shortcuts
---
```

## 3. Skill Naming

**Location:** `hmode/skills/protoflow/{skill-name}/`

**Pattern:** `protoflow:{action}` or `protoflow:{noun}`

**Format:**
- All skills MUST use `protoflow:` namespace prefix
- After prefix: use kebab-case action or noun
- Namespace prevents conflicts with other plugins

**Structure Types:**

**Type A: Simple Skill (Markdown file)**
```
hmode/skills/protoflow/
└── {skill-name}.md
```

**Type B: Complex Skill (Directory with handlers)**
```
hmode/skills/protoflow/{skill-name}/
├── README.md
├── skill.yaml
├── handler.py
├── handlers/
│   ├── __init__.py
│   └── {feature}.py
└── tests/
    └── test_{feature}.py
```

**Examples:**
- ✅ `protoflow:contribute` - External contribution workflow
- ✅ `protoflow:config` - Configuration management
- ✅ `protoflow:domain-search` - Search semantic domains (future)
- ✅ `protoflow:prototype-new` - Create new prototype (future)
- ✅ `protoflow:quality-gate` - Quality checks (future)

**Naming Rules:**
1. ALWAYS use `protoflow:` prefix
2. Use action verbs for workflow skills (`contribute`, `deploy`)
3. Use nouns for management skills (`config`, `domain-search`)
4. Keep under 30 characters (including prefix)
5. Avoid redundancy (e.g., `protoflow:protoflow-config` → `protoflow:config`)

**skill.yaml Format:**
```yaml
name: protoflow:contribute
description: External contribution workflow via GitLab
version: 1.0.0
plugin: protoflow
handler: handler.py  # Optional
dependencies:  # Optional
  - gitlab-mcp
tags: [contribution, gitlab, workflow]
```

## 4. Tool Naming

**Location:** `hmode/shared/tools/*.py`

**Pattern:** `{verb}-{noun}.py`

**Format:**
- Use kebab-case with hyphens
- Structure: `{verb}-{noun}.py`
- Tools are utilities that can be imported and used by other scripts

**Verb Categories:**
- `generate` - Create new content (e.g., `generate-buildinfo.py`)
- `audit` - Inspection/validation (e.g., `audit-hardcoded-infra.py`)
- `enforce` - Rule enforcement (e.g., `guardrail-enforce.py`)
- `validate` - Validation operations (e.g., `post-deploy-validate.py`)
- `sync` - Synchronization (e.g., `sync-amplify-to-ssm.py`)
- `bootstrap` - Initialization (e.g., `bootstrap-prototype.py`)

**Examples:**
- ✅ `guardrail-enforce.py` - Enforce guardrail rules
- ✅ `post-deploy-validate.py` - Post-deployment validation
- ✅ `generate-buildinfo.py` - Generate buildinfo.json
- ✅ `audit-hardcoded-infra.py` - Audit hardcoded infrastructure
- ✅ `add-file-uuids.py` - Add UUIDs to files
- ✅ `ask-human.py` - Human approval requests

**File Structure:**
```python
#!/usr/bin/env python3
"""
Tool Name - Brief description

Purpose: Detailed purpose
Usage: python {tool-name}.py [args]
"""
# File UUID: {uuid}

import sys
import argparse
from pathlib import Path

def main():
    """Main entry point"""
    pass

if __name__ == "__main__":
    main()
```

**Naming Rules:**
1. Use kebab-case (hyphens, not underscores)
2. Start with action verb
3. Be specific (e.g., `post-deploy-validate` not `validate`)
4. Keep under 40 characters
5. Avoid abbreviations unless widely known

## 5. Script Naming

**Location:** `bin/*.py`, `bin/*.sh`

**Pattern:** `{verb}_{noun}.py` or `{verb}_{noun}.sh`

**Format:**
- Use snake_case with underscores
- Structure: `{verb}_{noun}` or `{action}_{target}`
- Scripts are executables for automation

**Examples:**
- ✅ `auto_merge_stale_branches.py` - Auto-merge claude/* branches
- ✅ `infra-shadow.py` - Shadow deployment testing
- ✅ `aws-inventory.py` - AWS resource inventory
- ✅ `resolve_merge_conflicts.py` - Resolve merge conflicts
- ✅ `refresh-credentials.sh` - Refresh AWS credentials
- ✅ `verify-setup.sh` - Verify environment setup

**File Structure:**
```python
#!/usr/bin/env python3
"""
Script Name - Brief description

Automation script for {purpose}
"""
import sys
from pathlib import Path

def main():
    """Main entry point"""
    pass

if __name__ == "__main__":
    main()
```

**Naming Rules:**
1. Use snake_case for Python scripts
2. Use kebab-case for shell scripts (common convention)
3. Start with action verb
4. Be descriptive (automation purpose should be clear)
5. Keep under 40 characters

## 6. Multi-Word Component Guidelines

**When to use hyphens vs underscores:**

| Component | Separator | Example |
|-----------|-----------|---------|
| Agents (MD files) | Hyphens | `amplify-deploy-specialist.md` |
| Commands (MD files) | Hyphens | `generate-tool-configs.md` |
| Skills (namespace) | Hyphens after colon | `protoflow:domain-search` |
| Tools (Python) | Hyphens | `post-deploy-validate.py` |
| Scripts (Python) | Underscores | `auto_merge_stale_branches.py` |
| Scripts (Shell) | Hyphens | `refresh-credentials.sh` |

**Rationale:**
- Markdown files → kebab-case (web-friendly, readable URLs)
- Python executables in `hmode/shared/tools/` → kebab-case (library-like, importable)
- Python executables in `bin/` → snake_case (traditional script naming)
- Shell scripts → kebab-case (UNIX tradition)

## 7. Reserved Names & Conflicts

**Avoid These Names:**
- Generic: `helper`, `utility`, `manager`, `handler`
- Ambiguous: `tool`, `script`, `agent`, `command`
- Single words without context: `run`, `test`, `deploy` (unless aliasing specific command)

**Namespace Conflicts:**
- Always check existing names before creating new components
- Use `grep -r "name: {proposed-name}" .claude/` to check
- Plugin skills MUST use `protoflow:` prefix

## 8. Deprecation & Migration

**Marking as Deprecated:**
1. Add `[DEPRECATED]` prefix to filename
2. Update frontmatter with deprecation notice
3. Provide migration path in file header

**Example:**
```
[DEPRECATED] old-tool.py → migrate to guardrail-enforce.py
```

**Removal Process:**
1. Mark as deprecated (keep for 1 release cycle)
2. Move to `deprecated/` subdirectory
3. Remove after 2 release cycles

## 9. Documentation Requirements

**Every component MUST include:**
1. **File UUID** - Unique identifier comment
2. **Description** - Purpose and use case
3. **Usage Examples** - How to invoke/use
4. **Parameters/Arguments** - Expected inputs (if applicable)

**Markdown Components (Agents/Commands/Skills):**
```yaml
---
name: component-name
description: Brief description
version: 1.0.0
---

# Component Title

Detailed description...

## Usage
...

## Examples
...
```

**Python Components (Tools/Scripts):**
```python
#!/usr/bin/env python3
"""
Component Name - Brief description

Purpose: What it does
Usage: How to use it
Examples:
    python component.py arg1 arg2
"""
# File UUID: {uuid}
```

## 10. Validation & Testing

**Naming Validation Script:**
```bash
# Run naming convention checker
python hmode/shared/tools/validate-naming-conventions.py

# Check specific directory
python hmode/shared/tools/validate-naming-conventions.py hmode/agents/
```

**Pre-commit Hook:**
```bash
# Add to .git/hooks/pre-commit
python hmode/shared/tools/validate-naming-conventions.py --strict
```

## 11. Examples - Before & After

### Agents

| Before | After | Reason |
|--------|-------|--------|
| `amplify_specialist.md` | `amplify-deploy-specialist.md` | Use hyphens, add specific role |
| `CognitoAgent.md` | `cognito-expert-agent.md` | Lowercase, descriptive role |
| `infra.md` | `infra-sre.md` | Add role suffix |

### Commands

| Before | After | Reason |
|--------|-------|--------|
| `generateDomain.md` | `generate-domain.md` | Use kebab-case |
| `mkproto.md` | `new-prototype.md` | Descriptive, no abbreviations |
| `qa_microsite.md` | `qa-microsite.md` | Use hyphens |

### Skills

| Before | After | Reason |
|--------|-------|--------|
| `contribute.md` | `protoflow:contribute` | Add namespace |
| `config-manager.md` | `protoflow:config` | Namespace + simplify |

### Tools

| Before | After | Reason |
|--------|-------|--------|
| `guardrail_enforce.py` | `guardrail-enforce.py` | Use hyphens |
| `postDeployValidate.py` | `post-deploy-validate.py` | Kebab-case |
| `bootstrap.py` | `bootstrap-prototype.py` | Add noun for clarity |

### Scripts

| Before | After | Reason |
|--------|-------|--------|
| `auto-merge-branches.py` | `auto_merge_stale_branches.py` | Use underscores, add specificity |
| `infraShadow.py` | `infra-shadow.py` | Use hyphens for bin/ scripts |

## 12. Migration Plan

**Phase 1: Documentation (Week 1)**
- ✅ Create NAMING_CONVENTIONS.md
- Create validation script
- Update CONTRIBUTING.md

**Phase 2: Validation (Week 2)**
- Run validation script on all components
- Generate migration list
- Prioritize high-impact renames

**Phase 3: Rename (Week 3-4)**
- Rename agents (`hmode/agents/`)
- Rename commands (`hmode/commands/`)
- Update skill namespaces (`hmode/skills/protoflow/`)
- Rename tools (`hmode/shared/tools/`)
- Rename scripts (`bin/`)

**Phase 4: Update References (Week 5)**
- Update CLAUDE.md references
- Update documentation
- Update import statements
- Update command aliases

**Phase 5: Validation & Cleanup (Week 6)**
- Re-run validation script
- Test all renamed components
- Archive deprecated names
- Update changelog

## 13. Checklist for New Components

**Before creating a new component:**

- [ ] Check naming conventions for component type
- [ ] Verify no naming conflicts (`grep -r "name: {name}"`)
- [ ] Add appropriate prefix/suffix (agent role, skill namespace)
- [ ] Use correct case format (kebab-case or snake_case)
- [ ] Keep name under character limit
- [ ] Avoid reserved/generic names
- [ ] Include File UUID
- [ ] Add YAML frontmatter (if applicable)
- [ ] Write clear description
- [ ] Provide usage examples
- [ ] Add to README if creating new skill category

## Version History

**1.0.0** (2026-02-04)
- Initial naming conventions document
- Defined standards for agents, commands, skills, tools, scripts
- Created quick reference table and validation checklist
- Established migration plan

## Related Documentation

- **Plugin README:** `hmode/skills/protoflow/README.md`
- **Main Orchestrator:** `CLAUDE.md`
- **SDLC Processes:** `hmode/docs/processes/`
- **Contributing Guide:** `CONTRIBUTING.md` (to be created)

## Support

Questions about naming conventions?
- Check this document first
- Review examples in each section
- Open issue on GitLab with `naming-conventions` label
- Contact: @andyhop
