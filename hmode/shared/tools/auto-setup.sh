#!/bin/bash
#
# Auto-Setup Global Tools
#
# Automatically detects environment and installs/updates global tools:
# - Claude Code web: Auto-install (non-interactive)
# - Work/Personal computer: Prompt user before installing
#
# Usage:
#   ./auto-setup.sh                  # Interactive mode
#   ./auto-setup.sh --auto           # Auto-install (Claude Code web)
#   ./auto-setup.sh --check-only     # Just check, don't install

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parse arguments
AUTO_INSTALL=false
CHECK_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --auto)
            AUTO_INSTALL=true
            shift
            ;;
        --check-only)
            CHECK_ONLY=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Automatically setup global tools based on detected environment"
            echo ""
            echo "Options:"
            echo "  --auto        Auto-install without prompting (for Claude Code web)"
            echo "  --check-only  Only check what's installed, don't install"
            echo "  -h, --help    Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}================================${NC}"
echo -e "${CYAN}Auto-Setup Global Tools${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

# Detect environment
echo -e "${BLUE}Detecting environment...${NC}"

ENV="unknown"
if command -v python3 &> /dev/null && [[ -f "$SCRIPT_DIR/../scripts/detect_environment.py" ]]; then
    ENV=$(python3 "$SCRIPT_DIR/../scripts/detect_environment.py" 2>/dev/null | grep "Environment:" | awk '{print $2}' || echo "unknown")
fi

echo -e "Environment: ${GREEN}$ENV${NC}"
echo ""

# If environment is claude_code_web, enable auto-install unless disabled
if [[ "$ENV" == "claude_code_web" ]] && [[ "$AUTO_INSTALL" == "false" ]]; then
    AUTO_INSTALL=true
    echo -e "${YELLOW}Claude Code web detected - enabling auto-install${NC}"
    echo ""
fi

# Check Python
echo -e "${BLUE}Checking Python tools...${NC}"
if command -v python3 &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Python $(python3 --version 2>&1 | cut -d' ' -f2)"

    # Run dry-run to check what needs installation
    PYTHON_DRY_RUN=$("$SCRIPT_DIR/install-global-tools.sh" --dry-run 2>&1)
    PYTHON_TO_INSTALL=$(echo "$PYTHON_DRY_RUN" | grep "To install:" | awk '{print $3}')

    if [[ "$PYTHON_TO_INSTALL" == "0" ]]; then
        echo -e "  ${GREEN}✓${NC} All Python tools installed"
    else
        echo -e "  ${YELLOW}!${NC} $PYTHON_TO_INSTALL Python tools need installation"

        if [[ "$CHECK_ONLY" == "false" ]]; then
            if [[ "$AUTO_INSTALL" == "true" ]]; then
                echo -e "  ${BLUE}→${NC} Auto-installing Python tools..."
                "$SCRIPT_DIR/install-global-tools.sh" 2>&1 | tail -5
                echo -e "  ${GREEN}✓${NC} Python tools installed"
            else
                echo ""
                read -p "Install Python tools now? [y/N] " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    "$SCRIPT_DIR/install-global-tools.sh"
                else
                    echo -e "  ${YELLOW}Skipped${NC} - Run manually: cd $SCRIPT_DIR && ./install-global-tools.sh"
                fi
            fi
        fi
    fi
else
    echo -e "  ${RED}✗${NC} Python not found - skipping Python tools"
fi

echo ""

# Check Node.js
echo -e "${BLUE}Checking Node.js tools...${NC}"
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Node.js $(node --version) / npm $(npm --version)"

    # Run dry-run to check what needs installation
    NODE_DRY_RUN=$("$SCRIPT_DIR/install-node-tools.sh" --dry-run 2>&1)
    NODE_TO_INSTALL=$(echo "$NODE_DRY_RUN" | grep "To install:" | awk '{print $3}')

    if [[ "$NODE_TO_INSTALL" == "0" ]]; then
        echo -e "  ${GREEN}✓${NC} All Node.js tools installed"
    else
        echo -e "  ${YELLOW}!${NC} $NODE_TO_INSTALL Node.js tools need installation"

        if [[ "$CHECK_ONLY" == "false" ]]; then
            if [[ "$AUTO_INSTALL" == "true" ]]; then
                echo -e "  ${BLUE}→${NC} Auto-installing Node.js tools..."
                "$SCRIPT_DIR/install-node-tools.sh" 2>&1 | tail -5
                echo -e "  ${GREEN}✓${NC} Node.js tools installed"
            else
                echo ""
                read -p "Install Node.js tools (core packages)? [y/N] " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    "$SCRIPT_DIR/install-node-tools.sh"

                    echo ""
                    read -p "Also install optional packages (vercel, aws-cdk, etc.)? [y/N] " -n 1 -r
                    echo
                    if [[ $REPLY =~ ^[Yy]$ ]]; then
                        "$SCRIPT_DIR/install-node-tools.sh" --all
                    fi
                else
                    echo -e "  ${YELLOW}Skipped${NC} - Run manually: cd $SCRIPT_DIR && ./install-node-tools.sh"
                fi
            fi
        fi
    fi
else
    echo -e "  ${RED}✗${NC} Node.js/npm not found - skipping Node.js tools"
fi

echo ""

# Update capability cache
if [[ "$CHECK_ONLY" == "false" ]]; then
    echo -e "${BLUE}Updating capability cache...${NC}"
    if command -v python3 &> /dev/null && [[ -f "$SCRIPT_DIR/../scripts/detect_capabilities.py" ]]; then
        python3 "$SCRIPT_DIR/../scripts/detect_capabilities.py" --force > /dev/null 2>&1
        echo -e "  ${GREEN}✓${NC} Capability cache updated"
    fi
fi

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Setup Complete${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Show summary
if command -v python3 &> /dev/null && [[ -f "$SCRIPT_DIR/../scripts/detect_capabilities.py" ]]; then
    echo -e "${BLUE}Available Tools:${NC}"

    # Check key tools
    python3 -c "
import sys
sys.path.append('$SCRIPT_DIR/../scripts')
from detect_capabilities import has_command

tools = [
    ('aws', 'AWS CLI'),
    ('tsc', 'TypeScript'),
    ('playwright', 'Playwright'),
    ('black', 'Black formatter'),
    ('ruff', 'Ruff linter'),
    ('pytest', 'pytest'),
]

for cmd, name in tools:
    from detect_capabilities import has_command
    status = '✓' if has_command(cmd) else '✗'
    color = '\033[0;32m' if has_command(cmd) else '\033[0;31m'
    reset = '\033[0m'
    print(f'  {color}{status}{reset} {name}')
"
fi

echo ""
echo "Next steps:"
echo "  1. Verify installations: python3 $SCRIPT_DIR/../scripts/detect_capabilities.py"
echo "  2. Test tools: aws --version, tsc --version, etc."

if [[ "$ENV" != "claude_code_web" ]]; then
    echo "  3. Update tools periodically: cd $SCRIPT_DIR && ./auto-setup.sh"
fi
