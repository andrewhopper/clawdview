# Config Skill Usage Guide

<!-- File UUID: a7b8c9d0-1e2f-3a4b-5c6d-7e8f9a0b1c2d -->

Practical guide for using `/config` in real-world scenarios.

## Quick Start

### First Time Setup

```bash
# Interactive mode - recommended for first-time users
/config

# See what's configured
/config --section=guardrails
/config --list-domains
```

### Common Operations

```bash
# Add approved technology
/config --add-tech nextjs frontend

# Add design system color
/config --add-color warning

# Add golden repo template
/config --add-golden-repo python-lambda

# List all domains
/config --list-domains
```

## Real-World Scenarios

### Scenario 1: Setting Up a New Tech Stack

**Context:** You're starting a new project with FastAPI + React + PostgreSQL.

**Steps:**

```bash
# 1. Add backend framework
/config --add-tech fastapi backend-framework

# 2. Add frontend framework
/config --add-tech react frontend-framework

# 3. Add database
/config --add-tech postgresql database

# 4. Add architecture pattern
/config --add-arch-pattern "API Gateway with microservices"

# 5. Verify guardrails
/config --section=guardrails
# Select [5] View current tech preferences
```

**Result:** FastAPI, React, and PostgreSQL are now auto-approved for all projects. AI won't prompt for approval when using these technologies.

---

### Scenario 2: Creating a New Golden Repo Template

**Context:** Your team frequently builds Python CLI tools. You want a reusable template.

**Steps:**

```bash
# Option A: Interactive (recommended)
/golden-repo
# Select [1] Add new template
# Enter name: python-cli-advanced
# Select [1] Search GitHub for exemplar
# Review and confirm

# Option B: Direct
/config --add-golden-repo python-cli-advanced
# Follow prompts to select GitHub exemplar or create from scratch
```

**Best Practices:**
- Search GitHub first for proven templates (look for 5k+ stars, recent activity)
- Include `.template-metadata.yaml` with tech stack and description
- Add comprehensive README with usage instructions
- Remove example code but keep structure and config files

---

### Scenario 3: Extending the Design System

**Context:** You need to add a "success" color and a notification component.

**Steps:**

```bash
# 1. Add color token
/config --add-color success
# Suggested HSL: 142 76% 36% (green)
# Confirm or adjust

# 2. Add notification component
/config --add-component notification molecule
# Creates: hmode/shared/design-system/molecules/notification.html
# Includes metadata header and token usage

# 3. Validate existing assets
/design-system
# Select [7] Validate compliance
# Enter file path to check for violations
```

**Design System Rules:**
- ❌ NEVER use raw hex colors (#22c55e)
- ✅ ALWAYS use tokens (hsl(var(--success)))
- ❌ NEVER use magic numbers (17px)
- ✅ ALWAYS use spacing tokens (var(--space-4))

---

### Scenario 4: Adding AI Steering Rules

**Context:** You want to enforce security best practices automatically.

**Steps:**

```bash
# NEVER allow insecure patterns
/config --add-steering-rule NEVER security "raw SQL queries without parameterization"

# ALWAYS require specific patterns
/config --add-steering-rule ALWAYS security "input validation at API boundaries"

# MUST do for production code
/config --add-steering-rule MUST testing "integration tests for critical paths"

# SHOULD recommend best practices
/config --add-steering-rule SHOULD performance "implement caching for expensive operations"
```

**Steering Levels:**
- `NEVER` - Absolute prohibition, AI cannot proceed
- `ALWAYS` - Absolute requirement, AI cannot skip
- `MUST` - Required unless explicit exception
- `SHOULD` - Recommended (warning only)

---

### Scenario 5: Working with Domain Models

**Context:** You're building an e-commerce app and need data models.

**Steps:**

```bash
# 1. Check existing domains
/config --list-domains

# 2. Search for relevant domains
# (This happens automatically via Claude, but you can check manually)

# 3. Add new domain (delegates to agent)
/config --add-domain ecommerce
# Spawns domain-modeling-specialist
# Agent researches schema.org, GitHub examples
# Generates YAML models
# Requests human approval before implementation
```

**Domain Model Best Practices:**
- Reuse existing primitives from core domain
- Include created_at and updated_at in all models
- Version domains when evolving (v1.0.0 → v1.1.0)
- Document relationships between domains

---

### Scenario 6: Code Standards for New Language

**Context:** Your team is adopting Go. You need code standards.

**Steps:**

```bash
# 1. Add Go code standard directory
/config --add-standard go naming-conventions

# 2. Add more standards
/config --add-standard go error-handling
/config --add-standard go concurrency-patterns

# 3. View all Go standards
/config --section=code-standards
# Select [3] View standard details
# Enter language: go
```

**Standard Template Includes:**
- Overview of pattern
- When to use / when NOT to use
- Code examples
- Anti-patterns to avoid
- Related standards
- External references

---

### Scenario 7: Removing Deprecated Technology

**Context:** Your org is phasing out a legacy framework.

**Steps:**

```bash
# Remove from approved list
/config --remove-tech angular frontend-framework

# Confirm removal
# [Y/n]: Y

# Add steering rule to prevent usage
/config --add-steering-rule NEVER tech "Angular framework (deprecated - use React)"
```

**Result:** Angular is no longer auto-approved. AI will block attempts to use it and suggest React instead.

---

## Tips & Best Practices

### Guardrails

**DO:**
- Add technologies after team consensus
- Document rationale in notes field
- Review quarterly and remove deprecated tech
- Use steering rules to enforce critical standards

**DON'T:**
- Add experimental tech without evaluation
- Remove guardrails without team discussion
- Bypass approval for "quick fixes"

### Golden Repos

**DO:**
- Start from proven GitHub exemplars
- Include comprehensive README
- Keep dependencies up to date
- Document non-obvious setup steps

**DON'T:**
- Copy entire apps (extract patterns only)
- Include sensitive data or credentials
- Forget to remove .git directory
- Skip .template-metadata.yaml

### Design System

**DO:**
- Use HSL format for all colors (better for themes)
- Define semantic tokens (--primary, --success)
- Include metadata header in all assets
- Classify components atomically (atom/molecule/organism)

**DON'T:**
- Use raw hex colors (#1a1a2e)
- Create one-off magic numbers (17px)
- Exceed 3 visual hierarchy levels
- Skip validation checklist

### Domain Models

**DO:**
- Search existing domains first
- Research external sources (schema.org)
- Get human approval before implementation
- Version when evolving domains

**DON'T:**
- Invent domain structure from scratch
- Skip prototype-specific extensions
- Forget created_at/updated_at fields
- Create duplicate primitives

### Code Standards

**DO:**
- Include real code examples
- Show anti-patterns to avoid
- Link to external references
- Update when patterns evolve

**DON'T:**
- Create standards without team buy-in
- Copy-paste from other repos blindly
- Forget to update README
- Make standards too prescriptive

---

## Troubleshooting

### Issue: Guardrail change not taking effect

**Solution:**
```bash
# 1. Verify file was updated
cat hmode/guardrails/tech-preferences/backend.yaml

# 2. Check guardrail enforcement
hmode/shared/tools/guardrail-enforce.py --check fastapi

# 3. Review enforcement audit log
cat hmode/guardrails/enforcement-audit.jsonl
```

### Issue: Design token not appearing

**Solution:**
```bash
# 1. Check globals.css syntax
cat hmode/shared/design-system/globals.css | grep "success"

# 2. Ensure HSL format (not hex)
# ✅ --success: 142 76% 36%;
# ❌ --success: #22c55e;

# 3. Validate with compliance checker
/design-system
# Select [7] Validate compliance
```

### Issue: Golden repo missing files

**Solution:**
```bash
# 1. Check .template-metadata.yaml
cat hmode/shared/golden-repos/python-cli/.template-metadata.yaml

# 2. Verify structure
ls -la hmode/shared/golden-repos/python-cli/

# 3. Re-clone from GitHub if corrupted
/config --update-golden-repo python-cli
# Select [1] Update from GitHub
```

### Issue: Domain not found in registry

**Solution:**
```bash
# 1. Check registry file
cat hmode/hmode/shared/semantic/domains/registry.yaml

# 2. Search for domain
/config --list-domains

# 3. Add if missing
/config --add-domain <domain-name>
```

---

## Advanced Usage

### Batch Operations

```bash
# Add multiple tech in sequence
/config --add-tech fastapi backend && \
/config --add-tech react frontend && \
/config --add-tech postgresql database
```

### Scripting

```python
from pathlib import Path
from claude.skills.protoflow.config.handlers import GuardrailsHandler

handler = GuardrailsHandler(Path.cwd())
result = handler.handle_add_tech("fastapi", "backend")

if result["status"] == "awaiting_confirmation":
    # Auto-approve for script
    confirmed = handler.confirm_add_tech(result["data"])
    print(f"Added: {confirmed['message']}")
```

### Custom Workflows

Create custom scripts that combine multiple config operations:

```python
def setup_new_project_stack(stack_name: str, technologies: list):
    """Set up entire stack at once."""
    for tech, category in technologies:
        result = handler.handle_add_tech(tech, category)
        if result["status"] == "awaiting_confirmation":
            handler.confirm_add_tech(result["data"])

# Usage
setup_new_project_stack("ecommerce", [
    ("nextjs", "frontend"),
    ("fastapi", "backend"),
    ("postgresql", "database"),
])
```

---

## Related Commands

- `/workon <project>` - Find and resume projects
- `/new-prototype` - Create new project (uses guardrails + golden repos)
- `/quality-control` - Validate code against standards
- `/design-system` - Alias for design system config
- `/guardrails` - Alias for guardrails config

---

## Getting Help

```bash
# Show help text
/config --help

# View examples
/config --examples

# Check version
/config --version
```

For issues or feature requests, see:
- `hmode/skills/protoflow/config/README.md`
- `hmode/skills/protoflow/config/examples/demo.py`
