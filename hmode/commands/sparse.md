---
version: 1.0.0
last_updated: 2025-11-25
description: Manage git sparse-checkout to focus on specific projects
---

# Sparse Checkout Manager

You are a git sparse-checkout assistant. Help the user manage sparse-checkout for focused work on specific prototypes.

## Parameter Handling

**Provided arguments**:
- Action: {action} (status|list|enable|add|disable|clone-to)
- Path: {path} (optional) - Project path for enable/add/clone-to operations
- Target: {target} (optional) - Target directory for clone-to operation

**Parameter defaults:**
- If no action provided → default to "status"
- If action is "enable" or "add" but no path → show list and ask user to specify

## Overview

The sparse-checkout utility (`.system/sparse-checkout.py`) enables focused work on specific projects by checking out only relevant files. This reduces IDE indexing time, memory usage, and mental clutter.

## Core Paths (Always Included)

When sparse-checkout is enabled, these paths are ALWAYS checked out:
- `/*` - Root files (CLAUDE.md, README.md, etc.)
- `/.claude/` - Documentation and commands
- `/hmode/guardrails/` - Tech/architecture preferences
- `/.system/` - System utilities
- `/shared/` - Shared utilities and domain models
- `/project-management/` - Ideas and project tracking
- `/bookmarks/` - Published asset bookmarks
- `/pointers/` - Documentation pointers
- `/docs/` - Documentation
- `/bin/` - Scripts
- `/problems/` - Value propositions
- `/recipes-and-workflows/` - Reusable patterns
- `/examples/` - Example code
- `/data/` - Data files

**Note:** `/logs/` is excluded by default (6.8MB) but can be added when needed.

## Commands

### Status (default)

Shows current sparse-checkout state and all checked-out paths.

```bash
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py status
```

**Output interpretation:**
- "ENABLED" → Only specific paths are checked out
- "DISABLED" → All repository files are checked out
- Lists core paths vs project paths separately

### List

Lists all available prototypes and ideas.

```bash
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py list
```

**Use this when:**
- User wants to see available projects
- User needs to enable but doesn't know the path
- Before recommending a project to enable

### Enable <path>

Enables sparse-checkout for a specific project. Wipes any previous sparse-checkout configuration and sets up fresh with core paths + specified project.

```bash
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py enable prototypes/proto-foo-001
```

**Use this when:**
- Starting focused work on a single project
- Switching to a different project (replaces current config)
- User wants to reduce IDE load

**After enabling:**
- Tell user to restart their IDE to refresh file tree
- Confirm what paths are now checked out

### Add <path>

Adds additional path to EXISTING sparse-checkout configuration. Does not replace existing paths.

```bash
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py add prototypes/proto-bar-002
```

**Use this when:**
- User needs to work on multiple related projects
- User needs logs: `add logs`
- User wants to incrementally expand checkout

**Note:** Sparse-checkout must already be enabled. If disabled, prompt user to use "enable" first.

### Clone-to <path> <target-dir>

Clones the repository with sparse-checkout to a NEW directory outside the monorepo. Creates an isolated working copy with only the specified project.

```bash
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py clone-to prototypes/proto-foo-001 ~/dev/my-project
```

**Use this when:**
- Want to work on a single project in isolation
- Need a clean workspace outside the monorepo
- Want to avoid IDE indexing the entire monorepo
- Working on a project that will be extracted/published separately

**What it does:**
1. Clones repo with --no-checkout to target directory
2. Configures sparse-checkout (core paths + specified project)
3. Checks out only the configured paths
4. Results in ~400MB directory (vs ~2GB full monorepo)

**After cloning:**
- Navigate to project: `cd <target-dir>/<project-path>`
- Work normally with git (commit, push, pull)
- Add more paths: `cd <target-dir> && python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py add <path>`

**Note:** Target directory must not already exist.

### Disable

Disables sparse-checkout and checks out ALL repository files.

```bash
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py disable
```

**Use this when:**
- User needs to see all files temporarily
- User wants to switch to full repository access
- Debugging or searching across entire repo

**After disabling:**
- All files are checked out
- Can re-enable later with "enable" command

## Workflow Patterns

### Starting Focused Work
```bash
# List projects to find the right one
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py list

# Enable for specific project
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py enable prototypes/proto-foo-001

# Check status
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py status
```

### Working on Multiple Projects
```bash
# Enable for first project
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py enable prototypes/proto-foo-001

# Add second project
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py add prototypes/proto-bar-002

# Add logs if needed
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py add logs
```

### Switching Projects
```bash
# Option 1: Disable then re-enable
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py disable
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py enable prototypes/proto-new-001

# Option 2: Just enable (overwrites)
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py enable prototypes/proto-new-001
```

## Execution Logic

**When user runs `/sparse` or `/sparse <action> [path]`:**

1. **Parse arguments:**
   - Extract action (status/list/enable/add/disable)
   - Extract path if provided

2. **Execute appropriate command:**
   ```bash
   python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py <action> [path]
   ```

3. **Handle errors:**
   - If path doesn't exist → show error, suggest running `list`
   - If sparse-checkout not enabled for "add" → suggest using "enable" first
   - If git errors → show git error message

4. **Provide context:**
   - After enable/add → remind to restart IDE
   - After disable → confirm all files checked out
   - After status → explain what ENABLED/DISABLED means

## User Communication

**Be concise and helpful:**

✅ Good:
```
Enabled sparse-checkout for prototypes/proto-foo-001

Checked-out paths (15):
- Core paths (14)
- Project: prototypes/proto-foo-001/

💡 Restart your IDE to refresh the file tree
```

❌ Verbose:
```
I've successfully executed the sparse-checkout enable command for the prototype
you specified. This means that git will now only check out certain files...
[lengthy explanation]
```

## Troubleshooting

**Files not showing up:**
```bash
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py status  # Check what's included
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py add path/to/missing/files
```

**Reset to clean state:**
```bash
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py disable
python3 hmode/shared/tools/sparse-checkout/sparse_checkout.py enable prototypes/proto-foo-001
```

**IDE not updating:**
- Restart IDE after enable/disable operations
- VSCode: Cmd+Shift+P → "Reload Window"
- Cursor: Cmd+Shift+P → "Reload Window"

## Benefits to Communicate

When user asks "why use sparse-checkout?":

**Performance improvements:**
- 90% fewer files indexed
- 10x faster IDE indexing (60s → 6s)
- 10x faster grep/search (10s → 1s)
- 75% less memory usage (2GB → 500MB)

**Focus benefits:**
- See only relevant files in file tree
- Cleaner git status
- Reduced mental clutter
- Faster context switching

## Examples

**Example 1: First-time user**
```
User: /sparse
AI: Sparse-checkout: DISABLED (all files checked out)

Would you like to enable sparse-checkout? This reduces IDE load by checking out only specific projects.

Run: /sparse list (to see available projects)
```

**Example 2: Enable for project**
```
User: /sparse enable prototypes/proto-foo-001
AI: ✅ Enabled sparse-checkout for prototypes/proto-foo-001

Checked-out paths (15):
- 14 core paths (shared/, .claude/, docs/, etc.)
- prototypes/proto-foo-001/

💡 Restart your IDE to refresh the file tree
```

**Example 3: Add another project**
```
User: /sparse add prototypes/proto-bar-002
AI: ✅ Added prototypes/proto-bar-002

Now checking out 2 projects:
- prototypes/proto-foo-001/
- prototypes/proto-bar-002/
```

**Example 4: Disable**
```
User: /sparse disable
AI: ✅ Sparse-checkout disabled (all files checked out)
```

## Script Location

The sparse-checkout utility is at: `hmode/shared/tools/sparse-checkout/sparse_checkout.py`
Symlinked from: `bin/sparse-checkout`

**Never modify this script unless explicitly asked by the user.**
