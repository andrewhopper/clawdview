# Tmux Claude Code Session Picker

**Location:** `shared/tools/tmux-claude-picker`
**Symlink:** `~/bin/cc`

## Overview

Interactive picker for managing Claude Code tmux sessions. Shows active sessions with project context, allows reconnecting or creating new sessions.

## Features

- 📋 **List all tmux sessions** with visual status indicators
- 🤖 **Claude detection** - highlights sessions running Claude Code
- 📁 **Project context** - shows working directory/project name
- 🔢 **Quick selection** - use numbers or arrow keys
- ➕ **Create new** - start fresh sessions with custom names/paths
- 🎨 **Color-coded** - attached (green), detached (dim), Claude (robot)

## Installation

```bash
# Create symlink (already done)
ln -sf /Users/andyhop/dev/protoflow/shared/tools/tmux-claude-picker ~/bin/cc

# Add ~/bin to PATH (add to .zshrc or .bashrc)
export PATH="$HOME/bin:$PATH"
```

## Usage

```bash
# Launch picker
cc

# Or run directly
~/bin/cc
```

### Interactive Menu

```
📋 Active tmux sessions:

  1) ● 1     🤖 working on protoflow
  2) ○ 2     working on events
  3) ● 10    🤖 working on proto-xyz-001

  n) Create new session
  q) Quit

Select session (number/n/q):
```

### Status Indicators

| Symbol | Meaning |
|--------|---------|
| ● | Attached session (green) |
| ○ | Detached session (dim) |
| 🤖 | Running Claude Code (green robot) |

## Workflow

1. **Launch:** Type `cc` in terminal
2. **Browse:** Review active sessions with project context
3. **Select:** Enter number to attach to session
4. **Create:** Press `n` to start new session
5. **Switch:** If inside tmux, switches client; otherwise attaches

## Creating New Sessions

When selecting `n`:

1. Prompts for session name
2. Optionally asks for starting directory
3. Creates session and attaches automatically
4. If session exists, attaches to existing

## Examples

```bash
# Quick reconnect to Claude session
$ cc
📋 Active tmux sessions:
  1) ● claude 🤖 working on protoflow
Select: 1

# Create new session for prototype work
$ cc
Select: n
Enter session name: proto-testing
Starting directory: /Users/andyhop/dev/protoflow/prototypes/proto-xyz-001
```

## Integration

**Works seamlessly with:**
- Existing tmux sessions
- Claude Code CLI
- Multiple concurrent sessions
- Nested tmux (switches client vs attach)

## Future Enhancements

- [ ] Optional fzf integration for fuzzy search
- [ ] Show last activity timestamp
- [ ] Filter Claude-only sessions
- [ ] Batch operations (kill multiple sessions)
- [ ] Session templates (e.g., "claude-work", "claude-personal")
- [ ] Integration with `.project` file detection

## Troubleshooting

**"tmux is not installed"**
```bash
brew install tmux
```

**"No active tmux sessions"**
- Creates new session automatically
- Or start with `tmux new -s session-name`

**Symlink not working**
```bash
# Verify symlink
ls -l ~/bin/cc

# Re-create if needed
ln -sf /Users/andyhop/dev/protoflow/shared/tools/tmux-claude-picker ~/bin/cc
```

**~/bin not in PATH**
```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/bin:$PATH"

# Reload shell
source ~/.zshrc
```

## Related

- **proto-launcher** - Similar pattern for launching prototypes
- **semantic-run** - Semantic search for prototypes
- **.claude/hooks/** - Claude Code automation hooks
