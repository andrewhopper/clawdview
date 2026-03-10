#!/bin/bash
#
# Install Global Python Tools
#
# Installs globally useful CLI tools across all environments.
# Safe to run multiple times (idempotent).
#
# Usage:
#   ./install-global-tools.sh           # Install all tools
#   ./install-global-tools.sh --dry-run # Show what would be installed
#   ./install-global-tools.sh --update  # Update existing tools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS_FILE="$SCRIPT_DIR/global-requirements.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
DRY_RUN=false
UPDATE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --update)
            UPDATE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dry-run    Show what would be installed without installing"
            echo "  --update     Update existing tools to latest versions"
            echo "  -h, --help   Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check if requirements file exists
if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
    echo -e "${RED}Error: Requirements file not found: $REQUIREMENTS_FILE${NC}"
    exit 1
fi

# Detect Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo -e "${RED}Error: Python not found. Please install Python first.${NC}"
    exit 1
fi

# Check pip
if ! $PYTHON -m pip --version &> /dev/null; then
    echo -e "${RED}Error: pip not found. Please install pip first.${NC}"
    exit 1
fi

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Global Python Tools Installer${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo "Python: $($PYTHON --version)"
echo "pip: $($PYTHON -m pip --version | head -1)"
echo ""

# Detect environment (optional integration with detect_environment.py)
if [[ -f "$SCRIPT_DIR/../scripts/detect_environment.py" ]]; then
    ENV_INFO=$($PYTHON "$SCRIPT_DIR/../scripts/detect_environment.py" 2>/dev/null | grep "Environment:" | cut -d' ' -f2 || echo "unknown")
    echo -e "Environment: ${GREEN}$ENV_INFO${NC}"
    echo ""
fi

# Parse requirements file and extract package names
echo -e "${BLUE}Checking installed packages...${NC}"
echo ""

# Store packages to install
declare -a TO_INSTALL=()
declare -a ALREADY_INSTALLED=()

while IFS= read -r line; do
    # Skip comments and empty lines
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "$line" ]] && continue

    # Extract package name (before >= or ==)
    pkg_name=$(echo "$line" | sed -E 's/([a-zA-Z0-9_-]+).*/\1/')

    # Check if already installed
    if $PYTHON -m pip show "$pkg_name" &> /dev/null; then
        ALREADY_INSTALLED+=("$pkg_name")
        echo -e "  ${GREEN}✓${NC} $pkg_name (already installed)"
    else
        TO_INSTALL+=("$pkg_name")
        echo -e "  ${YELLOW}○${NC} $pkg_name (needs installation)"
    fi
done < "$REQUIREMENTS_FILE"

echo ""
echo -e "${BLUE}Summary:${NC}"
echo "  Already installed: ${#ALREADY_INSTALLED[@]}"
echo "  To install: ${#TO_INSTALL[@]}"
echo ""

# Dry run mode
if $DRY_RUN; then
    echo -e "${YELLOW}DRY RUN MODE - No changes will be made${NC}"
    echo ""

    if [[ ${#TO_INSTALL[@]} -gt 0 ]]; then
        echo "Would install the following packages:"
        for pkg in "${TO_INSTALL[@]}"; do
            echo "  - $pkg"
        done
    else
        echo "All packages already installed!"
    fi

    exit 0
fi

# Install or update packages
if $UPDATE; then
    echo -e "${BLUE}Updating all packages...${NC}"
    echo ""

    $PYTHON -m pip install --upgrade -r "$REQUIREMENTS_FILE"

    echo ""
    echo -e "${GREEN}✓ All packages updated successfully!${NC}"
else
    # Install only missing packages
    if [[ ${#TO_INSTALL[@]} -eq 0 ]]; then
        echo -e "${GREEN}✓ All packages already installed!${NC}"
        echo ""
        echo "Run with --update to upgrade existing packages."
        exit 0
    fi

    echo -e "${BLUE}Installing ${#TO_INSTALL[@]} packages...${NC}"
    echo ""

    # Install from requirements file (pip will skip already installed)
    $PYTHON -m pip install -r "$REQUIREMENTS_FILE"

    echo ""
    echo -e "${GREEN}✓ Installation complete!${NC}"
fi

echo ""
echo -e "${BLUE}Installed tools:${NC}"

# Show versions of installed tools
while IFS= read -r line; do
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "$line" ]] && continue

    pkg_name=$(echo "$line" | sed -E 's/([a-zA-Z0-9_-]+).*/\1/')
    version=$($PYTHON -m pip show "$pkg_name" 2>/dev/null | grep "^Version:" | cut -d' ' -f2 || echo "unknown")

    echo "  $pkg_name: $version"
done < "$REQUIREMENTS_FILE"

echo ""
echo -e "${GREEN}Done!${NC}"
echo ""
echo "Next steps:"
echo "  1. Verify installations: python3 -m pip list"
echo "  2. Check capabilities: python3 $SCRIPT_DIR/../scripts/detect_capabilities.py --force"
echo "  3. Test a tool: aws --version"
