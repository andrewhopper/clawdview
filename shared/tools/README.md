# Global Tools Installation

## Overview

Centralized management of globally useful tools across all environments (work computer, personal computer, Claude Code web).

**Problem:** Different environments have different tools installed, leading to inconsistent experiences and "command not found" errors.

**Solution:** Declare and install core tools globally to ensure consistency.

---

## Quick Start

```bash
# Install Python tools
cd shared/tools
./install-global-tools.sh

# Install Node.js tools (core)
./install-node-tools.sh

# Install Node.js tools (core + optional)
./install-node-tools.sh --all

# Update all tools
./install-global-tools.sh --update
./install-node-tools.sh --update
```

---

## Files

| File | Purpose |
|------|---------|
| `global-requirements.txt` | Python packages (pip) |
| `global-node-packages.json` | Node.js packages (npm) |
| `install-global-tools.sh` | Install Python tools |
| `install-node-tools.sh` | Install Node.js tools |
| `README.md` | This file |

---

## Python Tools (`global-requirements.txt`)

### AWS Tools
- **awscli** - AWS command line interface
- **boto3** - AWS SDK for Python (scripting)

### Development Tools
- **black** - Python code formatter
- **ruff** - Fast Python linter
- **pytest** - Testing framework
- **ipython** - Enhanced Python REPL

### File & Data Tools
- **httpie** - User-friendly HTTP client (curl alternative)
- **rich** - Rich terminal output library
- **jq** - JSON processor (Python wrapper)

### Utilities
- **pipx** - Install Python apps in isolated environments
- **uv** - Fast Python package installer (Rust-based)

### Installation

```bash
# Install all
./install-global-tools.sh

# Dry run (see what would be installed)
./install-global-tools.sh --dry-run

# Update existing packages
./install-global-tools.sh --update

# Manual install
pip install -r global-requirements.txt
```

---

## Node.js Tools (`global-node-packages.json`)

### TypeScript & Runtime
- **typescript** - TypeScript compiler
- **tsx** - TypeScript execute (fast ts-node alternative)
- **ts-node** - TypeScript execution engine
- **@types/node** - Node.js type definitions

### Package Management
- **npm-check-updates** - Update package.json versions
- **pnpm** - Fast package manager

### Code Quality
- **prettier** - Code formatter
- **eslint** - JavaScript/TypeScript linter
- **@typescript-eslint/** - ESLint TypeScript support

### Development
- **nodemon** - Auto-restart on file changes
- **concurrently** - Run multiple commands
- **dotenv-cli** - Load .env files
- **zx** - Write shell scripts in JavaScript

### Servers & Testing
- **http-server** - Simple HTTP server
- **serve** - Static file server
- **playwright** - Browser automation & testing
- **@playwright/test** - Playwright test runner

### MCP
- **@modelcontextprotocol/sdk** - Model Context Protocol SDK

### Optional Packages
- **vercel** - Vercel CLI (deployment)
- **netlify-cli** - Netlify CLI (deployment)
- **aws-cdk** - AWS Cloud Development Kit
- **serverless** - Serverless Framework
- **vite** - Fast build tool
- **vitest** - Vite-native testing
- **turbo** - Monorepo build system
- **nx** - Monorepo tools

### Installation

```bash
# Install core packages only
./install-node-tools.sh

# Install core + optional
./install-node-tools.sh --all

# Dry run
./install-node-tools.sh --dry-run

# Update existing packages
./install-node-tools.sh --update

# Manual install (core only)
npm install -g typescript tsx ts-node @types/node npm-check-updates pnpm prettier eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser nodemon concurrently dotenv-cli http-server serve playwright @playwright/test zx @modelcontextprotocol/sdk
```

---

## Environment-Specific Considerations

### Claude Code Web
- **Limited write access** - May need to install in user directory
- **Proxy restrictions** - Some packages may fail to install
- **Performance** - Use cached capability detection after install

```bash
# Install with --user flag if needed
pip install --user -r global-requirements.txt
```

### Work Computer (isengardcli)
- **Corporate proxy** - May need proxy configuration
- **AWS tools** - awscli likely already installed via isengardcli

```bash
# Configure npm proxy if needed
npm config set proxy http://proxy.corp.example.com:8080
npm config set https-proxy http://proxy.corp.example.com:8080
```

### Personal Computer (AWS SSO)
- **Full control** - Standard installations work
- **AWS CLI** - Install via pip or OS package manager

```bash
# Standard installation
./install-global-tools.sh
./install-node-tools.sh
```

---

## Verification

### After Installation

```bash
# Verify Python tools
pip list | grep -E "awscli|black|ruff|pytest"

# Verify Node.js tools
npm list -g --depth=0 | grep -E "typescript|tsx|playwright"

# Test AWS CLI
aws --version

# Test TypeScript
tsc --version

# Test Playwright
playwright --version

# Test MCP SDK
node -e "console.log(require('@modelcontextprotocol/sdk'))"
```

### Capability Detection

```bash
# Force refresh capability cache
python3 ../scripts/detect_capabilities.py --force

# Check specific commands
python3 ../scripts/detect_capabilities.py --check aws
python3 ../scripts/detect_capabilities.py --check tsc
python3 ../scripts/detect_capabilities.py --check playwright
```

---

## Integration with Capability Detection

After installing global tools, capability detection will automatically find them:

```python
from detect_capabilities import get_capabilities

# Force refresh to detect new tools
caps = get_capabilities(force_refresh=True)

# Check what's available
print(f"AWS CLI: {caps.aws_cli_version}")
print(f"Node.js: {caps.node_version}")
print(f"Python: {caps.python_version}")

# Check for specific tools
from detect_capabilities import has_command

if has_command('aws'):
    print("✓ AWS CLI available")

if has_command('tsc'):
    print("✓ TypeScript compiler available")

if has_command('playwright'):
    print("✓ Playwright available")
```

---

## Customization

### Adding Python Packages

Edit `global-requirements.txt`:

```bash
# Add your package with version constraint
my-package>=1.0.0
```

Then reinstall:

```bash
./install-global-tools.sh
```

### Adding Node.js Packages

Edit `global-node-packages.json`:

```json
{
  "globalPackages": {
    "my-package": "^1.0.0"
  }
}
```

Then reinstall:

```bash
./install-node-tools.sh
```

---

## Troubleshooting

### Issue: Permission Denied

**Python:**
```bash
# Install in user directory
pip install --user -r global-requirements.txt
```

**Node.js:**
```bash
# Fix npm permissions (Linux/Mac)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Then install
./install-node-tools.sh
```

### Issue: Proxy Blocking Installation

**Python:**
```bash
# Set pip proxy
pip install --proxy http://proxy.example.com:8080 -r global-requirements.txt
```

**Node.js:**
```bash
# Set npm proxy
npm config set proxy http://proxy.example.com:8080
npm config set https-proxy http://proxy.example.com:8080

# Install
./install-node-tools.sh

# Unset proxy after
npm config delete proxy
npm config delete https-proxy
```

### Issue: Tool Not Found After Installation

**Check PATH:**
```bash
# Python user packages
echo $PATH | grep -o "\.local/bin"

# Add to PATH if missing
export PATH="$HOME/.local/bin:$PATH"

# Node.js global packages
npm config get prefix
# Add $(npm config get prefix)/bin to PATH
```

**Verify installation:**
```bash
# Python
pip show awscli

# Node.js
npm list -g --depth=0 | grep typescript
```

### Issue: Version Conflicts

**Python:**
```bash
# Use virtual environment for project-specific versions
python3 -m venv venv
source venv/bin/activate
pip install specific-version==X.Y.Z
```

**Node.js:**
```bash
# Use npx to run specific versions without global install
npx typescript@4.9.0 --version

# Or use nvm/mise for Node.js version management
```

---

## Best Practices

**1. Regular Updates**
```bash
# Update monthly
./install-global-tools.sh --update
./install-node-tools.sh --update
```

**2. Minimal Global Install**
- Only install truly global tools
- Use virtual environments (Python) or local node_modules (Node.js) for project-specific dependencies

**3. Document Custom Additions**
- Add comments to requirements files explaining why a tool is needed
- Keep optional tools in separate section

**4. Test After Installation**
- Run capability detection
- Verify critical tools work
- Update documentation if tools change behavior

**5. Environment Consistency**
- Run installation on all your environments
- Use same version constraints across environments
- Keep requirements files in version control

---

## Shell Scripts & Utilities

### tmux-claude-picker

**Symlink:** `~/bin/cc`
**Location:** `shared/tools/tmux-claude-picker`
**Docs:** `shared/tools/tmux-claude-picker.md`

Interactive picker for managing Claude Code tmux sessions.

**Features:**
- List all active tmux sessions with project context
- Visual indicators for attached/detached sessions
- Detect and highlight Claude Code sessions
- Quick reconnect via numbers or create new sessions
- Color-coded display with working directory info

**Installation:**
```bash
# Create symlink
ln -sf ~/dev/protoflow/shared/tools/tmux-claude-picker ~/bin/cc

# Add ~/bin to PATH (if not already)
export PATH="$HOME/bin:$PATH"
```

**Usage:**
```bash
# Launch picker
cc

# Example output:
📋 Active tmux sessions:
  1) ● 1     🤖 working on protoflow
  2) ○ 2        working on events
  3) ● 10    🤖 working on tool-xyz-abc12

  n) Create new session
  q) Quit
```

**See:** `tmux-claude-picker.md` for full documentation

---

## Code Quality & Measurement Tools

### Unified Quality Gate

**Script:** `unified-quality-gate.py`
**Docs:** `QUALITY_GATE_GUIDE.md`
**Installation:** `QUALITY_GATE_INSTALLATION.md`
**Makefile:** `Makefile.quality-gate`

Comprehensive quality validation combining multiple tools to enforce code quality standards.

**Tools Integrated:**
- **software-quality-check.py** - 8-dimension quality checker
- **radon** - Cyclomatic complexity analysis (Python)
- **pylint** - Code duplication detection (Python)
- **madge** - Circular dependency detection (TypeScript/JS)
- **/evaluate-architecture** - Manual architecture evaluation (optional)

**What It Checks (10 Dimensions):**
1. Config abstraction (no hardcoded IDs/paths)
2. Shared model reuse (domain models)
3. Code decomposition (file size < 500 lines)
4. Testing presence (test files exist)
5. Type safety (TypeScript, Python hints)
6. Security (no insecure WebSockets)
7. Design system compliance (no raw hex colors)
8. Domain model usage (timestamps)
9. Cyclomatic complexity (< 10 per function)
10. Circular dependencies (imports)

**Quick Start:**
```bash
# Run on current project
python ~/dev/lab/shared/tools/unified-quality-gate.py --project .

# Add Makefile targets
echo 'include $(HOPPERLABS_ROOT)/shared/tools/Makefile.quality-gate' >> Makefile

# Use convenient commands
make quality-gate          # Standard checks (30-60s)
make quality-gate-quick    # Fast checks (2-5s) - pre-commit
make quality-gate-strict   # Strict mode - pre-deploy
make quality-report        # Generate JSON report
```

**Installation Requirements:**
```bash
# Install Python tools (via uv)
uv pip install radon pylint

# Install Node.js tools
npm install -g madge
```

**Coverage:**
- ✅ Separation of Concerns
- ✅ Modularity
- ✅ DRY (Don't Repeat Yourself)
- ✅ Externalized Config
- ✅ Decoupling
- ✅ Testability
- ✅ Type Safety
- ✅ Security
- ✅ Cyclomatic Complexity
- ✅ Circular Dependencies

**Exit Codes:**
- `0` - PASS (all checks passed)
- `1` - FAIL (errors found or warnings in strict mode)
- `2` - ERROR (tool execution failed)

**See:** `QUALITY_GATE_GUIDE.md` for full documentation
**See:** `QUALITY_GATE_INSTALLATION.md` for installation details

---

## Related Files

- `../scripts/detect_capabilities.py` - Capability detection
- `../scripts/detect_environment.py` - Environment detection
- `../scripts/CAPABILITY_DETECTION_README.md` - Capability docs
- `tmux-claude-picker.md` - Tmux session picker docs

---

## Questions

Contact: andrew@protoflow.dev

---

[END OF GLOBAL TOOLS README]
