# Code Standards & Quality

<!-- File UUID: c6b5a4f3-e2d1-0c9b-8a7e-6f5d4c3b2a1f -->

## Overview

This directory contains code standards, best practices, and quality measurement tools for the monorepo.

**Purpose:** Define what "good code" looks like so AI and humans can replicate it consistently.

---

## Directory Structure

```
shared/standards/
├── code/                      # Language-specific coding standards
│   ├── python/
│   ├── typescript/
│   ├── react/
│   ├── fastapi/
│   ├── nodejs/
│   ├── pydantic/
│   ├── pydantic-ai/
│   ├── vite/
│   ├── baml/
│   └── react-email/
├── testing/                   # Testing patterns and frameworks
│   ├── BDD_TESTING_GUIDE.md
│   ├── SMOKE_TEST_PATTERN.md
│   └── CICD_TESTING_GUIDE.md
├── deployment/                # Deployment standards
│   └── MAKEFILE_TEMPLATE.md
├── design/                    # Design standards (flowcharts, diagrams)
├── writing/                   # Documentation standards
├── PROJECT_HEALTH_REPORT.md   # Health monitoring template
├── PROJECT_VERIFICATION_CHECKLIST.md  # Pre-deployment checklist
└── SAFE_CLI_COMMANDS.md       # Safe command patterns
```

---

## Quality Measurement Tools

### 1. Unified Quality Gate ⭐

**Location:** \`../tools/unified-quality-gate.py\`
**Docs:** \`../tools/QUALITY_GATE_GUIDE.md\`

Comprehensive quality validation combining multiple tools.

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
\`\`\`bash
# Run on current project
python ~/dev/lab/shared/tools/unified-quality-gate.py --project .

# Or use Makefile targets
make quality-gate          # Standard checks
make quality-gate-quick    # Fast checks (pre-commit)
make quality-gate-strict   # Strict mode (pre-deploy)
\`\`\`

**See:** \`../tools/QUALITY_GATE_GUIDE.md\` for full documentation

---

## Code Standards by Technology

| Technology | Location |
|------------|----------|
| **Python** | \`code/python/README.md\` |
| **TypeScript** | \`code/typescript/README.md\` |
| **React** | \`code/react/README.md\` |
| **FastAPI** | \`code/fastapi/README.md\` |
| **Node.js** | \`code/nodejs/README.md\` |
| **Pydantic** | \`code/pydantic/README.md\` |
| **Pydantic AI** | \`code/pydantic-ai/README.md\` |
| **Vite** | \`code/vite/README.md\` |
| **BAML** | \`code/baml/README.md\` |
| **React Email** | \`code/react-email/README.md\` |

---

## Coverage Matrix

| Principle | Tool | Location |
|-----------|------|----------|
| **Separation of Concerns** | Unified Quality Gate | \`../tools/unified-quality-gate.py\` |
| **Modularity** | Unified Quality Gate + /evaluate-architecture | \`../tools/\` + \`.claude/commands/\` |
| **DRY** | pylint + /evaluate-architecture | Integrated in quality gate |
| **Externalized Config** | Config abstraction check | Integrated in quality gate |
| **Decoupling** | /evaluate-architecture | \`.claude/commands/evaluate-architecture.md\` |
| **Testability** | Test presence + /evaluate-architecture | Integrated in quality gate |
| **Type Safety** | Software quality check | Integrated in quality gate |
| **Security** | Software quality check | Integrated in quality gate |
| **Cyclomatic Complexity** | radon | Integrated in quality gate |
| **Circular Dependencies** | madge | Integrated in quality gate |

---

## Related Documentation

- **Quality Gate Guide:** \`../tools/QUALITY_GATE_GUIDE.md\`
- **Quality Gate Installation:** \`../tools/QUALITY_GATE_INSTALLATION.md\`
- **Golden Repos:** \`../golden-repos/\`
- **Domain Models:** \`../semantic/domains/\`
- **Design System:** \`../design-system/\`

---

**This is what good code looks like. Copy it.**
