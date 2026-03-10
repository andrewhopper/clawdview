---
version: 1.0.0
last_updated: 2025-11-23
description: Auto-merge stale claude/* branches (alias for /auto-merge)
---

# Merge (Alias)

This is a shortcut alias for `/auto-merge`.

## Instructions

Run the full auto-merge workflow as documented in `/auto-merge`:

1. Commit uncommitted tracking files
2. Run `bin/auto_merge_stale_branches.py` with `echo "y" | python3 bin/auto_merge_stale_branches.py`
3. Handle any merge conflicts
4. Merge manual-approval branches (guardrails changes)
5. Clean up merged remote branches
6. Report results

See `/auto-merge` for full documentation.
