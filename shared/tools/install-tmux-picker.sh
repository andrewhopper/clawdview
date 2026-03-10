#!/bin/bash
# Automated installer for tmux-claude-picker
# Usage: ./install-tmux-picker.sh [--ssh-auto-run] [--uninstall]

set -euo pipefail

# Colors
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
RESET='\033[0m'
DIM='\033[2m'

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PICKER_SCRIPT="$SCRIPT_DIR/tmux-claude-picker"
SSH_SNIPPET="$SCRIPT_DIR/tmux-claude-picker-ssh-snippet.sh"
BIN_DIR="$HOME/bin"
SYMLINK="$BIN_DIR/cc"
SHELL_RC="$HOME/.zshrc"

# Options
ENABLE_SSH_AUTO_RUN=false
UNINSTALL=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --ssh-auto-run)
            ENABLE_SSH_AUTO_RUN=true
            ;;
        --uninstall)
            UNINSTALL=true
            ;;
        --help|-h)
            cat <<EOF
tmux-claude-picker installer

Usage:
  ./install-tmux-picker.sh [OPTIONS]

Options:
  --ssh-auto-run    Enable SSH auto-run (adds snippet to .zshrc)
  --uninstall       Remove installation
  --help, -h        Show this help

Examples:
  # Basic install
  ./install-tmux-picker.sh

  # Install with SSH auto-run
  ./install-tmux-picker.sh --ssh-auto-run

  # Uninstall
  ./install-tmux-picker.sh --uninstall
EOF
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $arg${RESET}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Uninstall function
uninstall() {
    echo -e "${BOLD}🗑️  Uninstalling tmux-claude-picker...${RESET}\n"

    # Remove symlink
    if [[ -L "$SYMLINK" ]]; then
        rm "$SYMLINK"
        echo -e "${GREEN}✓${RESET} Removed symlink: ${DIM}$SYMLINK${RESET}"
    else
        echo -e "${DIM}⊘ Symlink not found: $SYMLINK${RESET}"
    fi

    # Note about .zshrc (don't auto-remove for safety)
    echo -e "\n${YELLOW}⚠${RESET}  Manual cleanup required:"
    echo -e "${DIM}  Edit ~/.zshrc to remove:${RESET}"
    echo -e "${DIM}    - PATH export for ~/bin${RESET}"
    echo -e "${DIM}    - SSH auto-run snippet${RESET}"

    echo -e "\n${GREEN}✓${RESET} Uninstall complete!"
    exit 0
}

# Main install function
install() {
    echo -e "${BOLD}🚀 Installing tmux-claude-picker...${RESET}\n"

    # Step 1: Check if picker script exists
    if [[ ! -f "$PICKER_SCRIPT" ]]; then
        echo -e "${RED}✗ Picker script not found: $PICKER_SCRIPT${RESET}"
        exit 1
    fi
    echo -e "${GREEN}✓${RESET} Found picker script: ${DIM}$PICKER_SCRIPT${RESET}"

    # Step 2: Make script executable
    if [[ ! -x "$PICKER_SCRIPT" ]]; then
        chmod +x "$PICKER_SCRIPT"
        echo -e "${GREEN}✓${RESET} Made script executable"
    else
        echo -e "${DIM}⊘ Script already executable${RESET}"
    fi

    # Step 3: Create ~/bin directory
    if [[ ! -d "$BIN_DIR" ]]; then
        mkdir -p "$BIN_DIR"
        echo -e "${GREEN}✓${RESET} Created directory: ${DIM}$BIN_DIR${RESET}"
    else
        echo -e "${DIM}⊘ Directory exists: $BIN_DIR${RESET}"
    fi

    # Step 4: Create symlink
    if [[ -L "$SYMLINK" ]]; then
        # Symlink exists - check if it points to correct location
        current_target=$(readlink "$SYMLINK")
        if [[ "$current_target" == "$PICKER_SCRIPT" ]]; then
            echo -e "${DIM}⊘ Symlink already correct: $SYMLINK${RESET}"
        else
            rm "$SYMLINK"
            ln -sf "$PICKER_SCRIPT" "$SYMLINK"
            echo -e "${YELLOW}↻${RESET} Updated symlink: ${DIM}$SYMLINK → $PICKER_SCRIPT${RESET}"
        fi
    else
        ln -sf "$PICKER_SCRIPT" "$SYMLINK"
        echo -e "${GREEN}✓${RESET} Created symlink: ${DIM}$SYMLINK → $PICKER_SCRIPT${RESET}"
    fi

    # Step 5: Add ~/bin to PATH
    if grep -q 'export PATH="$HOME/bin:$PATH"' "$SHELL_RC" 2>/dev/null; then
        echo -e "${DIM}⊘ PATH already configured in $SHELL_RC${RESET}"
    else
        echo -e "\n# tmux-claude-picker: Add ~/bin to PATH" >> "$SHELL_RC"
        echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_RC"
        echo -e "${GREEN}✓${RESET} Added ~/bin to PATH in ${DIM}$SHELL_RC${RESET}"
    fi

    # Step 6: Optionally add SSH auto-run
    if [[ "$ENABLE_SSH_AUTO_RUN" == true ]]; then
        if grep -q "SSH_CONNECTION.*TMUX.*cc" "$SHELL_RC" 2>/dev/null; then
            echo -e "${DIM}⊘ SSH auto-run already configured${RESET}"
        else
            echo -e "\n# tmux-claude-picker: Auto-launch on SSH" >> "$SHELL_RC"
            echo 'if [[ -n "$SSH_CONNECTION" ]] && [[ -z "$TMUX" ]] && [[ -x "$HOME/bin/cc" ]]; then' >> "$SHELL_RC"
            echo '    "$HOME/bin/cc"' >> "$SHELL_RC"
            echo 'fi' >> "$SHELL_RC"
            echo -e "${GREEN}✓${RESET} Added SSH auto-run to ${DIM}$SHELL_RC${RESET}"
        fi
    fi

    # Step 7: Verify installation
    echo -e "\n${BOLD}🔍 Verifying installation...${RESET}\n"

    if [[ -x "$SYMLINK" ]]; then
        echo -e "${GREEN}✓${RESET} Symlink is executable: ${DIM}$SYMLINK${RESET}"
    else
        echo -e "${RED}✗${RESET} Symlink not executable: ${DIM}$SYMLINK${RESET}"
    fi

    if grep -q "$HOME/bin" <<< "$PATH"; then
        echo -e "${GREEN}✓${RESET} ~/bin is in current PATH"
    else
        echo -e "${YELLOW}⚠${RESET}  ~/bin not in current PATH (will be after shell reload)"
    fi

    if command -v tmux &>/dev/null; then
        echo -e "${GREEN}✓${RESET} tmux is installed: ${DIM}$(tmux -V)${RESET}"
    else
        echo -e "${RED}✗${RESET} tmux not found ${DIM}(install with: brew install tmux)${RESET}"
    fi

    # Step 8: Success summary
    echo -e "\n${BOLD}${GREEN}✓ Installation complete!${RESET}\n"

    echo -e "${BOLD}Next steps:${RESET}"
    echo -e "  1. Reload your shell:"
    echo -e "     ${BLUE}source ~/.zshrc${RESET}\n"
    echo -e "  2. Test the picker:"
    echo -e "     ${BLUE}cc${RESET}\n"

    if [[ "$ENABLE_SSH_AUTO_RUN" == true ]]; then
        echo -e "  3. Test SSH auto-run:"
        echo -e "     ${BLUE}ssh localhost${RESET}\n"
    fi

    echo -e "${DIM}Documentation: $SCRIPT_DIR/tmux-claude-picker.md${RESET}"
}

# Main
if [[ "$UNINSTALL" == true ]]; then
    uninstall
else
    install
fi
