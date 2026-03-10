---
description: Interactive workflow menu - manage todos, bugs, and improvements
tags: [workflow, menu, interactive, todos, bugs, improvements]
args:
  - name: action
    description: "Optional: add/view/done/bug/improve or item text"
    required: false
---

# Flow - Task Management Menu

Unified interface for managing todos, bugs, and improvements.

**Store:** `.system/todostore.json` (global) or `{project}/.todostore.json` (per-project)
**Schema:** `hmode/hmode/shared/semantic/domains/task-management/schema.yaml`

## Parse Arguments

Check `$ARGUMENTS` for action:

| Input | Action |
|-------|--------|
| (empty) | Show main menu |
| `add <text>` | Add todo |
| `bug <text>` | Add bug |
| `improve <text>` | Add improvement |
| `view` | View all items |
| `done <#>` | Mark item complete |

## Store Location

1. Check if `.project` exists in current directory → use `{project-dir}/.todostore.json`
2. Otherwise → use `.system/todostore.json` (global)

## Tag UUIDs (from todostore.json)

| Type | Tag ID | Color |
|------|--------|-------|
| TODO | `a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d` | #3B82F6 (blue) |
| BUG | `b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e` | #EF4444 (red) |
| IMPROVE | `c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f` | #8B5CF6 (purple) |

## Main Menu (No Arguments)

Use `AskUserQuestion` with these options:

**Question:** "What would you like to do?"
**Header:** "Flow"
**Options:**
1. **View all** - "See todos, bugs, and improvements"
2. **Add todo** - "Add a new task"
3. **Add bug** - "Report a bug to fix"
4. **Add improvement** - "Suggest an enhancement"
5. **Mark done** - "Complete an item"

## jq Operations

### View All Items
```bash
jq -r '.global.todos[] | "\(.status) | \(.tags[0]) | \(.title)"' .system/todostore.json
```

### Add Todo
Generate UUID, then:
```bash
jq --arg id "$(uuidgen)" \
   --arg title "Fix the header" \
   --arg tag "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d" \
   --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   '.global.todos += [{
     id: $id,
     title: $title,
     status: "pending",
     priority: "medium",
     tags: [$tag],
     createdAt: $now,
     updatedAt: $now
   }]' .system/todostore.json > /tmp/todostore.json && mv /tmp/todostore.json .system/todostore.json
```

### Add Bug
Same as todo but use bug tag: `b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e`

### Add Improvement
Same as todo but use improve tag: `c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f`

### Mark Done
```bash
jq --arg id "TARGET_UUID" \
   --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   '(.global.todos[] | select(.id == $id)) |= . + {status: "completed", completedAt: $now, updatedAt: $now}' \
   .system/todostore.json > /tmp/todostore.json && mv /tmp/todostore.json .system/todostore.json
```

### Query by Type
```bash
# All bugs
jq '.global.todos[] | select(.tags[] == "b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e")' .system/todostore.json

# Pending items only
jq '.global.todos[] | select(.status == "pending")' .system/todostore.json
```

## Action Handlers

### View All
1. Read `.system/todostore.json` via jq
2. Group by tag type (TODO/BUG/IMPROVE)
3. Display with status icons:

```
📋 TODOS
  1. ⏳ Implement user authentication
  2. 🔄 Write unit tests
  3. ✅ Setup project structure

🐛 BUGS
  4. ⏳ Login fails on Safari
  5. 🔄 Memory leak in dashboard

💡 IMPROVEMENTS
  6. ⏳ Add dark mode toggle
  7. ⏳ Improve load time
```

Status icons: ⏳ pending | 🔄 in_progress | ✅ completed

After viewing, ask: "What next?" with options:
- **Add item** - "Add todo, bug, or improvement"
- **Mark done** - "Complete an item by number"
- **Exit** - "Return to conversation"

### Add Todo
1. If text provided in args, use it
2. Otherwise ask: "What needs to be done?"
3. Generate UUID via `uuidgen`
4. Add to store via jq with TODO tag
5. Confirm: `✓ Added todo: "<text>"`
6. Return to menu

### Add Bug
1. If text provided in args, use it
2. Otherwise ask: "Describe the bug:"
3. Generate UUID via `uuidgen`
4. Add to store via jq with BUG tag
5. Confirm: `✓ Added bug: "<text>"`
6. Return to menu

### Add Improvement
1. If text provided in args, use it
2. Otherwise ask: "What improvement?"
3. Generate UUID via `uuidgen`
4. Add to store via jq with IMPROVE tag
5. Confirm: `✓ Added improvement: "<text>"`
6. Return to menu

### Mark Done
1. Read store and show numbered list of pending/in_progress items
2. Ask: "Which item to complete? (enter number)"
3. Update status to `completed` and set `completedAt` via jq
4. Confirm: `✓ Completed: "<text>"`
5. Return to menu

## Quick Commands

```bash
/flow                        # Interactive menu
/flow add Fix the header     # Quick add todo
/flow bug Button not working # Quick add bug
/flow improve Add caching    # Quick add improvement
/flow view                   # View all items
/flow done 3                 # Mark item #3 complete
```

## Menu Loop

After each action, return to menu unless user selects Exit.

Use this flow:
1. Execute action
2. Show confirmation
3. Ask "What next?" (View all / Add item / Mark done / Exit)
4. Repeat until Exit selected

## Per-Project Store

When working within a project directory (has `.project` file):

1. Check for `{project-dir}/.todostore.json`
2. If not exists, create with same schema
3. All operations target project-local store
4. Use `/flow --global` to force global store

---

**Version**: 2.0.0
**Store**: `.system/todostore.json` (jq-based, persistent)
**Schema**: `hmode/hmode/shared/semantic/domains/task-management/schema.yaml`
**Created**: 2025-11-26
**Updated**: 2025-12-01
