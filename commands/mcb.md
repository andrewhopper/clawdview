---
version: 1.0.0
last_updated: 2025-12-14
description: Merge claude branches (alias for /merge-claude-branches)
---

# MCB (Merge Claude Branches)

Short alias for `/merge-claude-branches`.

## Instructions

Run the full merge workflow:

1. Fetch all remote branches
2. List all `claude/*` branches (excluding current)
3. Merge each into current branch
4. Resolve conflicts using sensible defaults
5. Report results

See `/merge-claude-branches` for full documentation.

## Quick Reference

```
/mcb                          # Merge all claude/* branches
/mcb old-branch,wip-feature   # Exclude specific branches
```
