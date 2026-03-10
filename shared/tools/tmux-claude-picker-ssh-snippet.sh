#!/bin/bash
# SSH Auto-run snippet for tmux-claude-picker
# Add this to your ~/.zshrc to auto-launch the picker on SSH login

# Add ~/bin to PATH for custom tools
export PATH="$HOME/bin:$PATH"

# Auto-launch tmux session picker on SSH login
# Conditions:
#   - Only run if connected via SSH (SSH_CONNECTION is set)
#   - Only run if not already inside tmux (TMUX is not set)
#   - Only run if the picker script exists and is executable
if [[ -n "$SSH_CONNECTION" ]] && [[ -z "$TMUX" ]] && [[ -x "$HOME/bin/cc" ]]; then
    "$HOME/bin/cc"
fi
