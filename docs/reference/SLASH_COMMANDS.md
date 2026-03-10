## ⚡ SLASH COMMANDS (Web Sessions)

**Context:** Claude Code web sessions are stateless. Each invocation is independent.

### Interactive Commands Problem
Traditional interactive slash commands (ask questions mid-execution) don't work in web sessions.

**❌ DON'T:** Design commands that ask follow-up questions
```bash
# Bad: /new-idea asks "What's the idea name?" mid-execution
/new-idea  # Then waits for user input → FAILS in web
```

**✅ DO:** Accept all inputs upfront OR use intelligent defaults
```bash
# Good: All inputs provided
/new-idea "API rate limiter" --detailed

# Good: Works with defaults, optional detail flag
/new-idea "API rate limiter"
```

### Design Principles

**1. All-Upfront Pattern:**
- Accept all required info as arguments
- Use flags for optional behaviors (--detailed, --skip-research, etc.)
- Example: `/new-idea <name> [--detailed] [--priority=high]`

**2. Smart Defaults Pattern:**
- Infer missing info from context (current directory, file names, etc.)
- Use sensible defaults (next proto number, current timestamp, etc.)
- Provide override flags when needed
- Example: `/list-prototypes` (no args needed, infers from repo structure)

**3. Hybrid Pattern:**
- Required args upfront, optional flags for customization
- Command works without flags (defaults), flags enable customization
- Example: `/push "message"` (message required, branch inferred)

### Migration Strategy

**Converting Interactive Commands:**

| Old (Interactive) | New (Web-Compatible) |
|------------------|---------------------|
| Ask for idea name | Require as first argument |
| Ask "detailed plan?" | Add `--detailed` flag |
| Ask for priority | Add `--priority=<level>` flag |
| Ask for tech stack | Infer from context or `--tech=<stack>` |

**Example: /new-idea Command**

**Before (Interactive):**
```
User: /new-idea
AI: "What's your idea name?"
User: "API rate limiter"
AI: "Want detailed planning doc? (y/n)"
User: "y"
```

**After (Web-Compatible):**
```
User: /new-idea "API rate limiter" --detailed
AI: Creates idea with full planning doc
```

**Implementation in hmode/commands/:**
```bash
#!/bin/bash
# new-idea.md command file

IDEA_NAME="${1:?Error: Idea name required. Usage: /new-idea \"name\" [--detailed]}"
DETAILED=false

# Parse flags
for arg in "$@"; do
  case $arg in
    --detailed) DETAILED=true ;;
  esac
done

# Execute with all info available upfront
```

### Rules for Web Sessions

1. **NEVER use AskUserQuestion** mid-slash-command execution
2. **ALWAYS accept critical inputs** as command arguments
3. **PROVIDE usage help** when args missing: `/new-idea → "Usage: /new-idea \"name\" [--detailed]"`
4. **USE flags liberally** for optional behaviors
5. **INFER context** when safe (repo state, current phase, file structure)

**Validation:** Test command works in single invocation with zero follow-ups.

