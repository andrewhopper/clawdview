#!/bin/bash
#
# Install Global Node.js/TypeScript Tools
#
# Installs globally useful Node.js CLI tools and TypeScript utilities
# across all environments.
#
# Usage:
#   ./install-node-tools.sh              # Install core tools
#   ./install-node-tools.sh --all        # Install core + optional tools
#   ./install-node-tools.sh --dry-run    # Show what would be installed
#   ./install-node-tools.sh --update     # Update existing tools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGES_FILE="$SCRIPT_DIR/global-node-packages.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
DRY_RUN=false
UPDATE=false
INSTALL_OPTIONAL=false

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
        --all)
            INSTALL_OPTIONAL=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dry-run    Show what would be installed without installing"
            echo "  --update     Update existing tools to latest versions"
            echo "  --all        Install optional packages in addition to core"
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

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js not found. Please install Node.js first.${NC}"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm not found. Please install npm first.${NC}"
    exit 1
fi

# Check if packages file exists
if [[ ! -f "$PACKAGES_FILE" ]]; then
    echo -e "${RED}Error: Packages file not found: $PACKAGES_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Global Node.js Tools Installer${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo "Node.js: $(node --version)"
echo "npm: $(npm --version)"
echo ""

# Detect environment (optional)
if [[ -f "$SCRIPT_DIR/../scripts/detect_environment.py" ]] && command -v python3 &> /dev/null; then
    ENV_INFO=$(python3 "$SCRIPT_DIR/../scripts/detect_environment.py" 2>/dev/null | grep "Environment:" | cut -d' ' -f2 || echo "unknown")
    echo -e "Environment: ${GREEN}$ENV_INFO${NC}"
    echo ""
fi

# Parse packages using Node.js
echo -e "${BLUE}Parsing packages...${NC}"
echo ""

# Extract package names and versions using node
CORE_PACKAGES=$(node -e "
const pkg = require('$PACKAGES_FILE');
const packages = pkg.globalPackages || {};
for (const [name, version] of Object.entries(packages)) {
    console.log(\`\${name}@\${version}\`);
}
")

OPTIONAL_PACKAGES=""
if $INSTALL_OPTIONAL; then
    OPTIONAL_PACKAGES=$(node -e "
const pkg = require('$PACKAGES_FILE');
const packages = pkg.optionalPackages || {};
for (const [name, version] of Object.entries(packages)) {
    console.log(\`\${name}@\${version}\`);
}
")
fi

# Combine packages
ALL_PACKAGES="$CORE_PACKAGES"
if [[ -n "$OPTIONAL_PACKAGES" ]]; then
    ALL_PACKAGES="$ALL_PACKAGES
$OPTIONAL_PACKAGES"
fi

# Check which packages are already installed
declare -a TO_INSTALL=()
declare -a ALREADY_INSTALLED=()

echo -e "${BLUE}Checking installed packages...${NC}"
echo ""

while IFS= read -r pkg_spec; do
    [[ -z "$pkg_spec" ]] && continue

    # Extract package name (before @version)
    pkg_name=$(echo "$pkg_spec" | sed 's/@.*//' | sed 's/^@//' | cut -d'@' -f1)

    # Handle scoped packages (e.g., @types/node)
    if [[ "$pkg_spec" =~ ^@ ]]; then
        pkg_name=$(echo "$pkg_spec" | cut -d'@' -f1,2)
    fi

    # Check if globally installed
    if npm list -g --depth=0 "$pkg_name" &> /dev/null; then
        installed_version=$(npm list -g --depth=0 "$pkg_name" 2>/dev/null | grep "$pkg_name@" | sed 's/.*@//' || echo "unknown")
        ALREADY_INSTALLED+=("$pkg_name@$installed_version")
        echo -e "  ${GREEN}✓${NC} $pkg_name ($installed_version)"
    else
        TO_INSTALL+=("$pkg_spec")
        echo -e "  ${YELLOW}○${NC} $pkg_name (needs installation)"
    fi
done <<< "$ALL_PACKAGES"

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

    # Update packages
    while IFS= read -r pkg_spec; do
        [[ -z "$pkg_spec" ]] && continue
        echo "Updating $pkg_spec..."
        npm install -g "$pkg_spec"
    done <<< "$ALL_PACKAGES"

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

    for pkg in "${TO_INSTALL[@]}"; do
        echo "Installing $pkg..."
        npm install -g "$pkg"
    done

    echo ""
    echo -e "${GREEN}✓ Installation complete!${NC}"
fi

echo ""
echo -e "${BLUE}Installed tools (global):${NC}"

# Show globally installed packages
npm list -g --depth=0 2>/dev/null | grep -E "$(echo "$ALL_PACKAGES" | sed 's/@.*//' | tr '\n' '|' | sed 's/|$//')" || true

echo ""
echo -e "${GREEN}Done!${NC}"
echo ""
echo "Next steps:"
echo "  1. Verify installations: npm list -g --depth=0"
echo "  2. Check capabilities: python3 $SCRIPT_DIR/../scripts/detect_capabilities.py --force"
echo "  3. Test TypeScript: tsc --version"
echo "  4. Test MCP SDK: node -e \"console.log(require('@modelcontextprotocol/sdk').version)\""
