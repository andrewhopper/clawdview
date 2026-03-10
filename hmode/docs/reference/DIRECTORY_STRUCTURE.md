## 📁 STRUCTURE

**Standard Mode:**
```
protoflow/
├── project-management/
│   └── ideas/proto-name-xxxxx-NNN-name/    # Ideas (phases 1-6)
│       ├── README.md            # REQUIRED - Summary, status, timeline
│       ├── seed.md, research.md, expansion.md, etc.
│       └── design/              # Phase 6 technical docs
├── problems/                                # Value Proposition Canvas registry
│   ├── README.md                            # Framework overview
│   ├── TEMPLATE.md                          # Reusable template
│   ├── customer-description-{6char}.md     # Customer segments (WHO)
│   ├── job-description-{6char}.md          # Customer jobs (WHAT)
│   ├── pain-description-{6char}.md         # Customer pains (OBSTACLES)
│   └── gain-description-{6char}.md         # Customer gains (DESIRES)
├── prototypes/proto-name-xxxxx-NNN-name/   # Prototypes (phases 7-9)
│   ├── README.md                # REQUIRED - Purpose, setup, tech stack, test commands
│   ├── references/              # Downloaded reference materials (Phase 7 - Git-ignored)
│   │   ├── library-examples/    # External reference code
│   │   └── REFERENCES.md        # Reference catalog with sources and patterns
│   ├── tests/                   # Playwright tests (Phase 7 - written FIRST)
│   │   ├── e2e/                 # End-to-end tests
│   │   ├── integration/         # Integration tests
│   │   └── uat/                 # UAT automation (Phase 9)
│   ├── src/                     # Source code (Phase 8 - written to pass tests)
│   └── playwright.config.ts     # Playwright configuration
├── standards/                   # Quality standards
│   ├── code/                    # Gold standard code examples
│   │   ├── typescript/          # TypeScript reference
│   │   ├── react/               # React + TypeScript
│   │   ├── nodejs/              # Node.js + Express
│   │   ├── vite/                # Vite configuration
│   │   ├── python/              # Python patterns
│   │   ├── fastapi/             # FastAPI reference
│   │   ├── pydantic/            # Pydantic validation
│   │   ├── pydantic-ai/         # Pydantic AI agents
│   │   ├── baml/                # BoundaryML BAML
│   │   └── README.md            # Overview and guidelines
│   └── writing/
│       └── WRITING_STYLE_GUIDE.md  # Writing standards
├── shared/                      # Shared utils/components/types
├── packages/                    # Shared npm packages
└── docs/                        # Documentation
```

**Divergent Mode:**
```
protoflow/
├── prototypes/proto-name-xxxxx-NNN-name/              # Parent (shared tests only)
│   ├── tests/                              # Shared test suite
│   ├── README.md                           # Variant comparison
│   ├── .project                            # Parent metadata
│   └── DIVERGENT_SPEC.md                   # Variant proposals
├── prototypes/proto-name-xxxxx-NNN-name-variant-A/   # Variant A
│   ├── src/                                # Implementation A
│   ├── README.md                           # Variant-specific
│   ├── .project                            # Links to parent
│   └── VARIANT_NOTES.md                    # Design decisions
├── prototypes/proto-name-xxxxx-NNN-name-variant-B/   # Variant B
│   └── ...                                 # (maximally different)
├── prototypes/proto-name-xxxxx-NNN-name-variant-C/   # Variant C
│   └── ...                                 # (maximally different)
└── prototypes/proto-name-xxxxx-NNN-name-evaluation/  # Phase 9D
    ├── BENCHMARKS.md                       # Performance data
    ├── MAINTAINABILITY.md                  # Code quality
    ├── TRADE_OFFS.md                       # Comparison matrix
    └── RECOMMENDATION.md                   # AI recommendation
```

**Naming:**
- Standard: `{name}-{5char}` (e.g., `tool-s3-publish-vayfd`)
- Divergent: `{name}-{5char}-variant-{A,B,C,...}`
- Allowed prefixes: `tool-`, `lib-`, `service-`, `protocol-`, `poc-`

### Directory Structure Rules

**CRITICAL: No Nested Duplicate Directories**

**❌ FORBIDDEN:**
- `prototypes/prototypes/` (nested prototypes)
- `ideas/ideas/` (nested ideas)
- `prototypes/delivery/prototypes/` (nested prototypes in subdirs)
- Any duplicate directory names at different nesting levels

**✅ CORRECT:**
- `prototypes/proto-name-xxxxx-NNN-name/` (flat structure under prototypes/)
- `prototypes/delivery/proto-name-xxxxx-NNN-name/` (subdir for organization OK, but NO duplicate folder names)

**Validation:**
Before creating directories, verify structure:
```bash
# Check for nested duplicates
find prototypes/ -type d -name "prototypes"
find ideas/ -type d -name "ideas"
```

**Why:** Prevents accidental nesting, confusion about correct locations, and duplicate content.

### Script Organization

**Main script location:** `projects/{classification}/active/{name}-{5char}/`
**Symlink from:** `hmode/commands/` or `shared/`

**Pattern:**
- Keep source code/scripts with their project
- Symlink from `hmode/commands/` or `shared/` for sharing
- Enables reusability while maintaining project ownership

**✅ CORRECT:**
```
projects/shared/active/tools-claude-power-tools-commands-skills-4fskn/commands/densify.md  # Main script
hmode/commands/densify.md → ../../projects/shared/active/.../commands/densify.md  # Symlink

projects/unspecified/active/tool-s3-publish-cli-vayfd/s3_publish.py  # Main script
shared/scripts/s3_publish.py → projects/unspecified/active/tool-s3-publish-cli-vayfd/s3_publish.py  # Symlink
```

**❌ INCORRECT:**
```
hmode/commands/densify.md                                      # Main script directly in .claude/
shared/scripts/process.sh                                        # Main script directly in shared/
```

**Why:**
- Projects remain self-contained and portable
- Clear ownership of scripts
- Easy to extract projects into standalone repos
- Shared functionality accessible via symlinks



## 📂 DIRECTORY ORGANIZATION

**Phases 1-6:** `project-management/ideas/active/{name}-{5char}/` (.project, seed.md, research.md, expansion.md, analysis.md, selection.md, design/)

**Phase 6 (Simple Design):** `design/` contains base docs only (SPECIFICATION.md, ARCHITECTURE.md, etc.)

**Phase 6 (Complex/Component-Based Design):**
```
design/
├── SPECIFICATION.md           # System-level spec
├── ARCHITECTURE.md            # High-level architecture
├── COMPONENT_INDEX.md         # Component catalog + dependencies
├── IMPLEMENTATION_PLAN.md     # Cross-component integration
├── TECH_STACK.md
├── RISKS.md
└── specs/                     # Component specifications
    ├── authentication/        # Descriptive component names
    │   ├── SPECIFICATION.md
    │   ├── ARCHITECTURE.md
    │   └── IMPLEMENTATION_STRATEGY.md
    ├── data-processing/
    │   └── ...
    └── api-gateway/
        └── ...
```

**Phase 7:** `projects/{classification}/active/{name}-{5char}/` (.project, references/, REFERENCES.md, tests/, playwright.config.ts, package.json) - **References downloaded, tests written FIRST**
**Phase 8:** `projects/{classification}/active/{name}-{5char}/` (.project, references/, tests/, src/, **startup script**, docs/)
**Phase 8.5 (Web/UI):** Add validation-report.md, tests/screenshots/, seed data files
**Phase 9:** `projects/{classification}/active/{name}-{5char}/` (.project, references/, tests/, tests/uat/, src/, docs/)
**Phase 6→7:** Move .project + docs (including component specs if exist) from project-management/ideas/ to projects/, create test structure, download references
**Phase 7→8:** Add src/ directory, write implementation to pass tests using reference patterns from hmode/shared/standards/code/ and component specs, **create startup script**
**Phase 8→8.5 (Web/UI):** Run startup script, create seed data, execute Playwright validation, generate report with screenshots
**Phase 8→9 (Non-visual):** Skip Phase 8.5, proceed to refinement (document skip in `.project`)
**Phase 8.5→9:** Fix critical issues from validation, proceed to UAT and polish
**Phase 9→COMPLETE:** Add tests/uat/, polish code and tests, resolve Phase 8.5 issues

