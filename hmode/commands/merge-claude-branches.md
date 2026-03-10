---
version: 1.0.0
last_updated: 2025-12-14
description: Merge all remote claude/* branches into current branch
---

# Merge Claude Branches

Merge all remote `claude/*` branches into the current branch. Useful for consolidating work before creating a PR or updating documentation.

## Parameter Handling

**Provided arguments**:
- Exclude: $ARGUMENTS (optional) - Branch patterns to exclude (comma-separated)

## Overview

This command:
1. Fetches latest remote branches
2. Lists all `claude/*` branches (excluding current)
3. Merges each branch sequentially
4. Resolves conflicts using sensible defaults
5. Reports merge status

**Different from `/auto-merge`**: This merges INTO the current branch, not into main.

## Instructions

### Step 1: Fetch and List Branches

```bash
git fetch origin
git branch -r | grep 'origin/claude/' | grep -v "$(git branch --show-current)"
```

Report found branches:
```
Found N claude/* branches to merge:
- origin/claude/branch-1
- origin/claude/branch-2
...
```

### Step 2: Merge Each Branch

For each branch, attempt merge:

```bash
git merge --no-edit origin/claude/<branch-name>
```

**If merge succeeds**: Continue to next branch

**If merge conflicts**: See Step 3

### Step 3: Resolve Conflicts

#### Common Conflict Patterns

**CLAUDE.md version conflicts**:
- Combine version descriptions (e.g., "Feature A + Feature B")
- Use the more recent date
- Keep all new rules from both sides

**YAML/JSON conflicts** (registry, config):
- Merge arrays: Keep ALL items from both sides
- Objects: Deep merge, newer values win
- Version numbers: Take HIGHER version

**Code conflicts** (add/add):
- For test files: Accept `--theirs` (incoming)
- For config files: Accept `--theirs` (incoming)
- For core logic: Manual review required

**Resolution commands**:
```bash
# Accept incoming version (theirs)
git checkout --theirs <file>
git add <file>

# Accept current version (ours)
git checkout --ours <file>
git add <file>

# Complete merge after resolution
git commit --no-edit
```

### Step 4: Handle Failures

If a merge cannot be resolved:

1. Abort the merge: `git merge --abort`
2. Log the failed branch
3. Continue with remaining branches
4. Report failures at end

### Step 5: Report Results

After all merges complete:

```
## Merge Results

**Successfully merged:**
- ✅ claude/branch-1 (clean merge)
- ✅ claude/branch-2 (resolved 2 conflicts)

**Skipped (already merged):**
- ⏭️ claude/branch-3

**Failed (needs manual intervention):**
- ❌ claude/branch-4 - Complex conflict in src/core.py

**Current branch:** claude/feature-xyz
**Total commits added:** 47
```

## Conflict Resolution Priority

1. **Auto-resolve** (safe):
   - Log files (`.jsonl`, `.log`)
   - Lock files (`uv.lock`, `package-lock.json`)
   - Generated files (`.d.ts`, compiled output)

2. **Accept theirs** (usually safe):
   - Test files (`*.spec.ts`, `*.test.py`)
   - Mockups/docs (`*.html` in docs/)
   - Config files when add/add conflict

3. **Manual review** (always):
   - Core business logic
   - Security-related files
   - CLAUDE.md structural changes
   - `hmode/guardrails/*` files

## Usage Examples

**Merge all claude branches:**
```
/merge-claude-branches
```

**Exclude specific branches:**
```
/merge-claude-branches old-experiment,wip-feature
```

## Post-Merge Actions

After successful merge, you may want to:

1. **Update documentation**:
   ```
   /diagram  # Regenerate architecture diagrams
   ```

2. **Run inventory** (if tools changed):
   ```
   Review and update docs/TOOLS_INVENTORY.md
   ```

3. **Push consolidated branch**:
   ```bash
   git push -u origin <current-branch>
   ```

4. **Create PR** (if ready):
   ```bash
   gh pr create --title "Consolidate claude/* branches" --body "Merged N branches..."
   ```

## Safety Notes

- Always on a feature branch (never run on main directly)
- Conflicts in `hmode/guardrails/` require careful review
- Use `git log --oneline -20` to verify merge history
- If unsure, `git reflog` can help recover from mistakes
