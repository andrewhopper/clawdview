---
name: cleanup
description: Clean up AI-generated code anti-patterns (hardcoded values, long files, tight coupling, DRY violations)
version: 1.0.0
aliases: [code-cleanup, refactor-ai]
---

# Code Cleanup Skill

**Invoke the code-cleanup-agent to fix AI code anti-patterns.**

## Quick Usage

```bash
/cleanup                    # Scan current directory
/cleanup src/               # Scan specific path
/cleanup --report-only      # Report without fixing
```

## What It Fixes

1. **Hardcoded values** → Extract to props/config/constants
2. **Long files (>300 lines)** → Decompose into modules
3. **Tight coupling** → Introduce interfaces + DI
4. **DRY violations** → Extract shared code
5. **Mixed concerns** → Separate layers

## Workflow

1. Spawn `code-cleanup-agent` (uses Opus)
2. Agent scans for anti-patterns
3. Generates prioritized report
4. Fixes incrementally with test verification

## Example

```
User: /cleanup infra/lib/

Agent Output:
## Code Cleanup Report

### Critical
- [ ] mo-backend-stack.ts:570 - hardcoded recordName: 'mo'
- [ ] mo-backend-stack.ts (623 lines) - needs decomposition

### Fixes Applied
✅ Extracted 12 hardcoded values to props interface
✅ Split stack into 3 modules (<200 lines each)
```
