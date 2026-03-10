# tmux-claude-picker Installation Guide

Interactive tmux session picker for Claude Code with auto-SSH launch.

## Quick Install (Automated)

```bash
cd /Users/andyhop/dev/protoflow/shared/tools
./install-tmux-picker.sh
```

The installer will:
- ✅ Create `~/bin` directory
- ✅ Symlink `~/bin/cc` → `tmux-claude-picker`
- ✅ Add `~/bin` to PATH in `~/.zshrc`
- ✅ Optionally add SSH auto-run snippet

## Manual Install

### 1. Create ~/bin directory

```bash
mkdir -p ~/bin
```

### 2. Create symlink

```bash
ln -sf /Users/andyhop/dev/protoflow/shared/tools/tmux-claude-picker ~/bin/cc
```

### 3. Add ~/bin to PATH

Add to `~/.zshrc`:

```bash
export PATH="$HOME/bin:$PATH"
```

### 4. Optional: Enable SSH auto-run

Add to `~/.zshrc`:

```bash
# Auto-launch tmux session picker on SSH login
if [[ -n "$SSH_CONNECTION" ]] && [[ -z "$TMUX" ]] && [[ -x "$HOME/bin/cc" ]]; then
    "$HOME/bin/cc"
fi
```

### 5. Reload shell

```bash
source ~/.zshrc
```

## Verification

### Test the picker

```bash
cc
```

Should display:
```
📋 Active tmux sessions:

  1) ● session1  🤖 working on protoflow
  2) ○ session2     working on project-xyz

  n) Create new session
  q) Quit
```

### Test SSH auto-run

```bash
# SSH to localhost to test
ssh localhost

# Should auto-launch picker
```

### Verify symlink

```bash
ls -l ~/bin/cc
# Should show: /Users/andyhop/bin/cc -> /Users/andyhop/dev/protoflow/shared/tools/tmux-claude-picker

which cc
# Should show: /Users/andyhop/bin/cc
```

### Verify PATH

```bash
echo $PATH | grep "$HOME/bin"
# Should show ~/bin in PATH
```

## Features After Installation

### Auto-cd to protoflow
When you attach to any session:
- Automatically runs `cd ~/dev/protoflow`
- Keeps you in the main working directory

### SSH Auto-launch (if enabled)
When you SSH into the machine:
- Picker launches automatically
- Only if not already in tmux
- Only on SSH connections (not local terminals)

### Default Directory
New sessions default to `~/dev/protoflow`:
- Press `n` for new session
- Hit Enter to accept default
- Or type custom path

## Troubleshooting

### "cc: command not found"

**Check PATH:**
```bash
echo $PATH | grep "$HOME/bin"
```

**If not found, add to ~/.zshrc:**
```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Symlink broken

**Re-create symlink:**
```bash
ln -sf /Users/andyhop/dev/protoflow/shared/tools/tmux-claude-picker ~/bin/cc
```

### SSH auto-run not working

**Check SSH detection:**
```bash
# In SSH session
echo $SSH_CONNECTION
# Should output connection info

# In local terminal
echo $SSH_CONNECTION
# Should be empty
```

**Check if snippet is in .zshrc:**
```bash
grep "SSH_CONNECTION" ~/.zshrc
```

### Auto-cd not working

**Check if protoflow directory exists:**
```bash
ls -la ~/dev/protoflow
```

**Check tmux send-keys permissions:**
```bash
# The script uses: tmux send-keys -t "$session" "cd $dir" C-m
# This requires tmux server to be running
tmux info
```

### Script not executable

```bash
chmod +x /Users/andyhop/dev/protoflow/shared/tools/tmux-claude-picker
```

## Uninstall

### Remove symlink
```bash
rm ~/bin/cc
```

### Remove from PATH (optional)
Edit `~/.zshrc` and remove:
```bash
export PATH="$HOME/bin:$PATH"
```

### Remove SSH auto-run (optional)
Edit `~/.zshrc` and remove the SSH auto-run snippet.

## Custom Configuration

### Change default directory

Edit `shared/tools/tmux-claude-picker`:

```bash
# Line 102: Change default_dir
local default_dir="$HOME/your/custom/path"

# Line 121: Change protoflow_dir
local protoflow_dir="$HOME/your/custom/path"
```

### Change symlink name

```bash
# Use a different command name
ln -sf /Users/andyhop/dev/protoflow/shared/tools/tmux-claude-picker ~/bin/tmux-pick
```

### Disable auto-cd

Edit `shared/tools/tmux-claude-picker`, remove lines 130-133:

```bash
# Remove this block:
if [[ -d "$protoflow_dir" ]]; then
    tmux send-keys -t "$session" "cd $protoflow_dir" C-m
fi
```

## Integration

### With Claude Code

When using Claude Code in tmux:
- Sessions show 🤖 robot icon
- Easily switch between multiple Claude instances
- Auto-cd keeps you in the right directory

### With Git

Since you auto-cd to protoflow:
- Always in the git repo root
- Easy to run git commands
- Consistent working directory

### With Multiple Environments

Use different session names:
- `cc` → picker launches
- Select or create: `work`, `personal`, `prototype-123`
- Each session isolated, same base directory

## Advanced Usage

### Custom key binding (tmux)

Add to `~/.tmux.conf`:

```bash
# Prefix + c = Launch session picker
bind c run-shell "~/bin/cc"
```

### Alias variations

Add to `~/.zshrc`:

```bash
alias tmux-pick='cc'
alias tp='cc'
alias sessions='cc'
```

### Integration with fzf (future)

The script currently uses native bash menus. Future versions could integrate fzf for fuzzy finding.

## Files

| File | Purpose |
|------|---------|
| `tmux-claude-picker` | Main script |
| `tmux-claude-picker.md` | Full documentation |
| `tmux-claude-picker-INSTALL.md` | This file |
| `tmux-claude-picker-ssh-snippet.sh` | SSH auto-run snippet |
| `install-tmux-picker.sh` | Automated installer |

## Support

- **Documentation:** `shared/tools/tmux-claude-picker.md`
- **Issues:** Check git log for recent changes
- **Questions:** andrew@protoflow.dev

---

**Version:** 1.0.0
**Last Updated:** 2025-11-30
