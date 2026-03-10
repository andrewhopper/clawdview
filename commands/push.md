---
uuid: cmd-push-2p3q4r5s
version: 1.0.0
last_updated: 2025-11-17
description: Quick commit and push to main with auto-generated message
---

# Push

You are a git commit assistant for this monorepo. Create clear, concise commits directly to main branch.

## Parameter Handling

**Provided arguments**:
- Message: {message}
- Files: {files}
- Push: {push} (default: true)
- Dry Run: {dry_run} (default: false)

## 🚨 CRITICAL: NO BRANCHES OR PRS

This repository follows a **direct-to-main** workflow:
- ✅ Commit directly to main
- ❌ NEVER create branches
- ❌ NEVER create pull requests

## Instructions

1. **Check current status**:
   ```bash
   git status
   git diff
   ```

2. **Stage changes**:
   ```bash
   git add -A
   # Or selectively:
   git add prototypes/proto-XXX-name/
   git add TODO.md DASHBOARD.md
   ```

3. **Generate commit message**:
   Based on changes, create a clear commit message following this format:

   ```
   [type]: Brief summary (50 chars max)

   Detailed description of changes:
   - Change 1
   - Change 2
   - Change 3

   🤖 Generated with Claude Code

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

4. **Commit types**:
   - `feat` - New feature or prototype
   - `fix` - Bug fix
   - `docs` - Documentation changes
   - `refactor` - Code refactoring
   - `test` - Adding tests
   - `chore` - Maintenance tasks
   - `proto` - Prototype-specific work
   - `config` - Configuration changes

5. **Commit the changes**:
   ```bash
   git commit -m "$(cat <<'EOF'
   [Commit message here]
   EOF
   )"
   ```

6. **Push to main**:
   ```bash
   git push origin main
   ```

7. **Confirm and display**:
   ```
   ✅ Committed and pushed to main!

   📝 Commit: [short hash]
   📦 Files changed: [count]
   ➕ Insertions: [count]
   ➖ Deletions: [count]

   🔗 Main branch updated
   ```

## Commit Message Examples

### New Prototype
```
proto: Add proto-005-chat-app with WebSocket support

Created new real-time chat prototype:
- Setup Node.js + Express + Socket.io
- Created basic chat UI with React
- Implemented room management
- Added message persistence
- Configured development environment

Tech Stack: Node.js, Express, Socket.io, React, MongoDB

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Progress Update
```
proto: Complete authentication for proto-001-auth-system

Implemented JWT-based authentication:
- Added login/logout endpoints
- Created token refresh mechanism
- Implemented middleware for protected routes
- Added password hashing with bcrypt
- Updated TODO.md with progress

Progress: 75% complete (15/20 tasks)

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Documentation
```
docs: Update project management system

Enhanced documentation:
- Added SETTINGS_GUIDE.md with permission details
- Updated TODO.md with completed tasks
- Refreshed DASHBOARD.md with current metrics
- Added slash command documentation

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Configuration
```
config: Add Claude Code permissions and commands

Added comprehensive Claude configuration:
- Created .claude/settings.json with auto-approvals
- Added slash commands for prototype management
- Configured git to prevent branch creation
- Setup VS Code integration tasks

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Fixes
```
fix: Resolve CORS issues in proto-003-api-gateway

Fixed cross-origin request problems:
- Added CORS middleware configuration
- Whitelisted development origins
- Updated .env.example with CORS settings
- Tested with frontend integration

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Completion
```
proto: Complete proto-002-chat-interface ✅

Finished real-time chat prototype:
- All core features implemented
- Tests passing (15/15)
- Documentation complete
- Demo deployed to staging
- Status updated to completed

Key Learnings:
- WebSocket connection pooling is critical
- Redis helps with multi-server chat rooms
- Client reconnection logic needs careful handling

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Smart Commit Suggestions

Based on changed files, suggest appropriate commit message:

**Changed: `prototypes/proto-XXX-name/**`**
→ Suggest: `proto: [Description of work on proto-XXX]`

**Changed: `TODO.md`, `DASHBOARD.md`**
→ Suggest: `chore: Update project tracking`

**Changed: `docs/**`**
→ Suggest: `docs: [What documentation was updated]`

**Changed: `.claude/**`, `tools/**`**
→ Suggest: `config: [Configuration changes]`

**Changed: `shared/**`**
→ Suggest: `feat: [What shared utility/component]`

## Usage Examples

**Auto-generate commit message (recommended):**
```bash
/push
# Analyzes changes, generates message, commits, and pushes

/push push=false
# Commits but doesn't push
```

**Custom commit message:**
```bash
/push message="Add authentication feature"

/push message="Fix CORS issues in API gateway" files="prototypes/proto-003-api-gateway/**"
```

**Specific files only:**
```bash
/push files="prototypes/proto-001-auth-system/**"

/push files="hmode/commands/*.md" message="Update slash commands"
```

**Dry run (preview):**
```bash
/push dry_run=true
# Shows what would be committed without committing
```

## Pre-Commit Checklist

Before committing, optionally check:
- [ ] No `.env` files with secrets
- [ ] No `node_modules/` included
- [ ] No sensitive credentials
- [ ] TODOs updated if prototype work
- [ ] Dashboard updated if significant progress

## Implementation Notes

1. **Always use heredoc** for multi-line commit messages
2. **Check git authorship** before amending
3. **Never force push** to main
4. **Stage selectively** if partial work
5. **Push immediately** after commit (fast iteration)

## Commit Workflow

```
┌─────────────────┐
│ Make changes    │
└────────┬────────┘
         │
┌────────▼────────┐
│ /push           │
└────────┬────────┘
         │
┌────────▼────────┐
│ Review changes  │
│ Generate msg    │
└────────┬────────┘
         │
┌────────▼────────┐
│ git add + commit│
└────────┬────────┘
         │
┌────────▼────────┐
│ git push main   │
└────────┬────────┘
         │
┌────────▼────────┐
│ ✅ Done!        │
└─────────────────┘
```

## Remember

- **Speed is key** - Fast commits, fast iterations
- **Main branch only** - Never suggest branches or PRs
- **Clear messages** - Future you will thank you
- **Push immediately** - Keep remote in sync
- **Include context** - Why, not just what

---

**Philosophy**: Commit early, commit often, commit directly to main. This is rapid prototyping, not production!
