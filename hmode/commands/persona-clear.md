---
version: 1.0.0
last_updated: 2025-11-19
description: Clear active persona and return to default Claude mode
---

# Clear Active Persona

Deactivate the current persona and return to default Claude interaction mode.

## Purpose

Remove persona context applied via `/persona-select` and restore standard Claude Code behavior.

## Usage

```bash
/persona-clear
```

## Instructions

1. **Check for active persona**:
   - If no persona active → inform user
   - If persona active → proceed with clearing

2. **Clear persona context**:
   - Remove persona-specific system instructions
   - Clear stored persona state
   - Return to default Claude Code mode

3. **Confirm deactivation**:
   ```
   ✅ Persona cleared

   Previously active: {Role} ({Attitude}) - {Name}
   Now using: Default Claude Code mode

   Ready for your next request.
   ```

## Example Output

### When persona is active
```
User: /persona-clear

✅ Persona cleared

Previously active: CTO (Anti-AI) - Michael Kenwood
Now using: Default Claude Code mode

Ready for your next request.
```

### When no persona active
```
User: /persona-clear

ℹ️ No active persona

Already using default Claude Code mode.

Use /persona-select to activate a persona.
```

## Related Commands

- `/persona-select` - Interactive persona selection through filtering
- `/persona-list` - Browse all available personas
- `/persona-describe {name}` - View details of a specific persona

---

**Goal**: Quick reset to default Claude behavior
