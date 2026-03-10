---
version: 1.0.0
last_updated: 2025-11-23
description: Auto-merge stale claude/* branches into main
---

# Auto-Merge

You are a git branch merge assistant. Automatically merge stale `claude/*` branches into main.

## Parameter Handling

**Provided arguments**:
- Force: {force} (default: false) - Skip manual approval prompts
- Threshold: {threshold} (default: 1.0) - Hours before branch is considered stale

## Overview

This command runs the auto-merge workflow:
1. Commits any uncommitted tracking files
2. Runs `bin/auto_merge_stale_branches.py`
3. Resolves merge conflicts when possible
4. Merges branches requiring manual approval (guardrails changes)
5. Cleans up merged remote branches

## Instructions

### Step 1: Prepare Working Directory

Check for uncommitted changes to tracking files:

```bash
git status
```

If `.auto_merge_audit.jsonl` or `.auto_merge_backups.json` are modified:

```bash
git add .auto_merge_audit.jsonl .auto_merge_backups.json
git commit -m "chore: Update auto-merge tracking files

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

### Step 2: Run Auto-Merge Script

```bash
echo "y" | python3 .system/auto_merge_stale_branches.py
```

The script categorizes branches:
- **Auto-merge (safe)**: No protected file changes
- **Already merged**: Just need branch deletion
- **Manual approval required**: Changes to `hmode/guardrails/` or `CLAUDE.md`

### Step 3: Handle Failures

If branches fail due to uncommitted changes:
1. Commit tracking files again
2. Re-run the script

If branches fail due to merge conflicts:
1. Delete the problematic local branch: `git branch -D <branch-name>`
2. Checkout fresh from remote: `git checkout -b <branch> origin/<branch>`
3. Merge main: `git merge origin/main`
4. Resolve conflicts (keep both changes when possible)
5. Commit and push the resolution
6. Merge to main and delete remote branch

### Step 4: Handle Manual Approval Branches

For branches that modify `hmode/guardrails/`:

1. Review what the branch changes:
   ```bash
   git diff main...origin/<branch-name> --stat
   ```

2. If changes are valid guardrails improvements, merge:
   ```bash
   git merge origin/<branch-name> -m "Merge: <description>"
   ```

3. Resolve any conflicts, preferring newer versions

4. Push and delete remote branch:
   ```bash
   git push
   git push origin --delete <branch-name>
   ```

### Step 5: Final Cleanup

After all merges complete:

```bash
git fetch origin
git branch -r | grep claude/
```

Report remaining branches (those not yet stale).

## Conflict Resolution Patterns

### YAML Registry Conflicts (`registry.yaml`)

When both branches add new domains:
- Keep ALL domains from both sides
- Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)

### JSON Index Conflicts (`index.json`)

For version numbers and counts:
- Take the HIGHER version number
- Take the LARGER counts (totalRules, totalCategories)

### File Location Conflicts

When files were added in renamed directories:
- Move files to the new location
- `mkdir -p <new-path> && mv <old-path>/* <new-path>/`

## Output Format

After completion, report:

```
**Auto-merge complete!**

**Merged:**
- ✅ branch-name-1 - Description
- ✅ branch-name-2 - Description (resolved conflict)

**Skipped (not stale):**
- ⏳ branch-name-3

**Failed (needs manual intervention):**
- ❌ branch-name-4 - Reason
```

## Script Location

The auto-merge script is at: `.system/auto_merge_stale_branches.py`

Key behaviors:
- Finds branches matching `claude/*` pattern
- Default stale threshold: 1 hour
- Backs up branch state before merging
- Audits all merge operations

## Safety Notes

- Script will NOT merge branches with uncommitted local changes
- Protected files (`hmode/guardrails/*`, `CLAUDE.md`) require explicit review
- Failed merges are logged to `.auto_merge_audit.jsonl`
- Branch state backed up to `.auto_merge_backups.json`

## Usage Examples

**Standard auto-merge:**
```bash
/auto-merge
```

**Force merge all (skip prompts):**
```bash
/auto-merge force=true
```

**Custom stale threshold (2 hours):**
```bash
/auto-merge threshold=2.0
```
