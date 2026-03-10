# ProtoFlow Plugin

<!-- File UUID: a7f8e9c1-4b2d-3e5f-6a7b-8c9d0e1f2a3b -->

**Official plugin for ProtoFlow monorepo management and collaboration**

## Overview

ProtoFlow is a Claude Code plugin that provides specialized skills for managing the ProtoFlow monorepo, including configuration management, contribution workflows, and development assistance.

## Plugin Structure

```
hmode/skills/protoflow/
├── README.md                    # This file
├── config/                      # Configuration management skill
│   ├── skill.py
│   ├── skill.yaml
│   ├── handlers/
│   └── README.md
└── contribute/                  # External contribution workflow
    ├── contribute.md
    ├── skill.json
    ├── handler.py
    └── README.md
```

## Available Skills

### 1. Configuration Management (`/protoflow:config`)

Unified interface for managing monorepo configuration:

- **Guardrails** - Tech/arch preferences, AI steering rules
- **Golden Repos** - Project templates and starters
- **Design System** - Design tokens, UI components, guidelines
- **Domain Models** - Semantic domain registry
- **Code Standards** - Language-specific patterns

**Usage:**
```bash
/protoflow:config                          # Interactive menu
/protoflow:config --section=guardrails     # Jump to section
/protoflow:config --add-tech fastapi backend
```

**Aliases:**
- `/guardrails` → `/protoflow:config --section=guardrails`
- `/golden-repo` → `/protoflow:config --section=golden-repos`
- `/design-system` → `/protoflow:config --section=design-system`

**Documentation:** [config/README.md](./config/README.md)

### 2. Contribution Workflow (`/protoflow:contribute`)

External contribution workflow via GitLab:

- **Sandbox Creation** - Isolated workspace for each contribution
- **GitLab Integration** - Auto-fork, clone, and create merge requests
- **Guided Changes** - Step-by-step assistance
- **MCP Integration** - Uses GitLab MCP for API operations

**Usage:**
```bash
/protoflow:contribute                                      # Interactive mode
/protoflow:contribute --description "Fix timeout" --type bug-fix
/protoflow:contribute --type docs --issue 1234
```

**Quick Start:**
```bash
cd hmode/skills/protoflow/contribute
cat QUICKSTART.md  # 5-minute setup guide
```

**Documentation:**
- [contribute/QUICKSTART.md](./contribute/QUICKSTART.md) - 5-minute getting started
- [contribute/SETUP.md](./contribute/SETUP.md) - GitLab MCP configuration
- [contribute/README.md](./contribute/README.md) - Full documentation

## Installation

### For Claude Code Desktop

The plugin is already part of the ProtoFlow repository. Skills are auto-discovered from `hmode/skills/protoflow/`.

Verify skills are loaded:
```bash
# In Claude Code
"List available skills"
```

Should show:
- `protoflow:config`
- `protoflow:contribute`

### For Claude Code Web

Skills should work automatically. If not, check:
```bash
ls -la hmode/skills/protoflow/
```

## Plugin Naming Convention

All skills in this plugin use the `protoflow:` namespace:

- `protoflow:contribute` (not just `contribute`)
- `protoflow:config` (not just `config`)

This prevents naming conflicts with other plugins or built-in skills.

## Prerequisites

### GitLab MCP (for `/protoflow:contribute`)

1. **Get GitLab Token**
   - URL: https://gitlab.com/-/profile/personal_access_tokens
   - Scopes: `api`, `read_repository`, `write_repository`

2. **Configure MCP**
   ```bash
   claude mcp add
   ```

   Settings:
   - Server name: `gitlab`
   - Command: `uvx`
   - Args: `["mcp-server-gitlab"]`
   - Environment:
     - `GITLAB_PERSONAL_ACCESS_TOKEN`: `<your-token>`
     - `GITLAB_URL`: `https://gitlab.com`

3. **Verify**
   ```bash
   claude mcp list
   # Should show: gitlab (uvx mcp-server-gitlab)
   ```

See [contribute/SETUP.md](./contribute/SETUP.md) for detailed instructions.

## Development

### Adding New Skills to Plugin

1. **Create skill directory**
   ```bash
   mkdir -p hmode/skills/protoflow/my-skill
   ```

2. **Create skill files**
   ```bash
   cd hmode/skills/protoflow/my-skill
   touch skill.json handler.py README.md
   ```

3. **Update skill.json**
   ```json
   {
     "name": "protoflow:my-skill",
     "description": "Description of skill",
     "version": "1.0.0",
     "plugin": "protoflow",
     "handler": "handler.py"
   }
   ```

4. **Update plugin README**
   Add new skill to "Available Skills" section above.

### Testing Skills

```bash
# Test handler directly
cd hmode/skills/protoflow/my-skill
python3 handler.py

# Test via Claude Code
# In Claude Code:
"/protoflow:my-skill"
```

### Plugin Standards

All skills in this plugin should follow:

1. **Naming:** Use `protoflow:` prefix
2. **Documentation:** Include README.md, QUICKSTART.md for complex skills
3. **Testing:** Provide test scripts (e.g., `test_handler.py`)
4. **UUIDs:** Include File UUID comments in all files
5. **Error Handling:** Graceful error messages with troubleshooting steps

## Version History

### 1.0.0 (2026-02-04)

**Initial Release:**
- `protoflow:config` - Configuration management skill
- `protoflow:contribute` - External contribution workflow
- Plugin infrastructure and documentation

## Support

### Issues

For bugs or feature requests:
1. Check existing documentation
2. Open issue on GitLab with `protoflow-plugin` label
3. Contact: @andyhop

### Documentation

- **Plugin Overview:** This file
- **Config Skill:** [config/README.md](./config/README.md)
- **Contribute Skill:** [contribute/README.md](./contribute/README.md)

## Related

- **Main CLAUDE.md:** `/Users/andyhop/dev/hl-protoflow/CLAUDE.md`
- **SDLC Docs:** `hmode/docs/processes/`
- **Guardrails:** `hmode/guardrails/`
- **Golden Repos:** `hmode/shared/golden-repos/`
- **Design System:** `hmode/shared/design-system/`

## Future Skills

Potential additions to the plugin:

- `protoflow:domain-search` - Search semantic domain registry
- `protoflow:prototype-new` - Create new prototype with full SDLC setup
- `protoflow:deploy` - Deploy prototypes to AWS
- `protoflow:quality-gate` - Run quality checks before phase advancement
- `protoflow:observability` - Add monitoring to prototypes

## License

Part of the ProtoFlow monorepo. See repository LICENSE file.
