# ProtoFlow Config Skill

<!-- File UUID: e5f6a7b8-9c0d-1e2f-3a4b-5c6d7e8f9a0b -->

Unified monorepo configuration manager for all system-level settings.

## Overview

The `/config` skill provides a single interface for managing:

1. **Guardrails** - Tech/arch preferences, AI steering rules
2. **Golden Repos** - Project templates and starters
3. **Design System** - Design tokens, UI components, guidelines
4. **Domain Models** - Semantic domain registry
5. **Code Standards** - Language-specific patterns

## Architecture

```
config/
├── skill.py                    # Main orchestrator
├── skill.yaml                  # Skill metadata
├── handlers/
│   ├── guardrails.py          # HIGH protection - requires approval
│   ├── golden_repos.py        # MEDIUM protection - verifies structure
│   ├── design_system.py       # MEDIUM protection - maintains consistency
│   ├── domain_models.py       # Delegates to domain-modeling-specialist
│   └── code_standards.py      # LOW protection - direct modifications
└── README.md                   # This file
```

## Usage Modes

### 1. Interactive Mode (No Arguments)

```bash
/config
```

Displays menu with all configuration sections. User selects section, then operation.

### 2. Section Mode (Jump to Section)

```bash
/config --section=guardrails
/guardrails                      # Alias
```

Jump directly to a specific configuration section.

### 3. Direct Mode (Execute Operation)

```bash
/config --add-tech fastapi backend
/config --add-color success
/config --add-golden-repo typescript-remix
```

Execute specific operation without menu navigation.

## Command Aliases

For convenience, common sections have dedicated aliases:

| Alias | Equivalent |
|-------|------------|
| `/guardrails` | `/config --section=guardrails` |
| `/golden-repo` | `/config --section=golden-repos` |
| `/design-system` | `/config --section=design-system` |

## Protection Levels

### HIGH - Guardrails

**Files:** `hmode/guardrails/*`

All changes require explicit human approval:
1. Show preview of change
2. Request confirmation
3. Only execute after approval

**Rationale:** Guardrails control AI behavior and tech stack decisions. Unauthorized changes could lead to inconsistent project setup or violate organizational standards.

### MEDIUM - Golden Repos & Design System

**Files:** `hmode/shared/golden-repos/*`, `hmode/shared/design-system/*`

Changes require structure validation:
1. Verify consistency with existing patterns
2. Check for conflicts or duplicates
3. Validate format and naming conventions
4. Request confirmation for significant changes

**Rationale:** These affect project consistency and visual identity. Changes should be validated but don't require same approval level as guardrails.

### LOW - Code Standards

**Files:** `hmode/shared/standards/code/*`

Direct modifications allowed with basic validation:
1. Check file format
2. Ensure required sections exist
3. No explicit approval needed

**Rationale:** Code standards are documentation. Mistakes are easily reversible and don't affect system behavior.

## Handler Patterns

Each handler implements these methods:

```python
class Handler:
    def get_stats(self) -> str:
        """Return stats for menu display"""

    def show_section_menu(self) -> dict:
        """Display section-specific menu"""

    def handle_<operation>(self, *args) -> dict:
        """Handle specific operation"""

    def confirm_<operation>(self, data: dict) -> dict:
        """Execute after approval (if needed)"""
```

## Response Format

All handlers return structured dictionaries:

```python
{
    "status": "success" | "error" | "awaiting_input" | "awaiting_confirmation" | "delegate",
    "message": "Human-readable message",
    "prompt": "Prompt text for user input (if applicable)",
    "operation": "operation_name (for multi-step flows)",
    "data": {...}  # Data for next step
}
```

## Delegation Pattern

Some operations delegate to specialized agents:

```python
{
    "status": "delegate",
    "agent": "domain-modeling-specialist",
    "prompt": "Task description for agent"
}
```

Example: Adding a new domain model spawns the `domain-modeling-specialist` agent to handle research, YAML generation, and human approval workflow.

## Examples

### Add Technology to Guardrails

```bash
# Interactive
$ /config
Select [1] Guardrails
Select [1] Add approved technology
Enter name: FastAPI
Enter category: backend
Confirm? [Y/n]

# Direct
$ /config --add-tech fastapi backend
```

### Add Design System Color

```bash
# Interactive
$ /design-system
Select [1] Add color token
Enter name: success
Adjust HSL? [Y/n/custom]
Proceed? [Y/n]

# Direct
$ /config --add-color success
```

### Create Golden Repo Template

```bash
# Interactive
$ /golden-repo
Select [1] Add new template
Enter name: typescript-remix
[1] Search GitHub / [2] From scratch / [3] Copy
Select [1]
Proceed? [Y/n]

# Direct
$ /config --add-golden-repo typescript-remix
```

## Testing

Test each handler independently:

```python
from handlers.guardrails import GuardrailsHandler

handler = GuardrailsHandler(Path.cwd())
result = handler.handle_add_tech("fastapi", "backend")
print(result)
```

## Extension

To add a new configuration section:

1. Create handler in `handlers/new_section.py`
2. Implement required methods (get_stats, show_section_menu, handle_*)
3. Register in `skill.py` handlers dict
4. Add to skill.yaml examples and help
5. Optionally add alias command

## Related Documentation

- `hmode/guardrails/` - Protection rules and approved technologies
- `hmode/shared/golden-repos/` - Project templates
- `hmode/shared/design-system/MANAGEMENT_GUIDELINES.md` - Design system rules
- `hmode/hmode/shared/semantic/domains/registry.yaml` - Domain model registry
- `hmode/shared/standards/code/` - Language-specific patterns
