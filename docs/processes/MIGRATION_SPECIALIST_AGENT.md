<!-- File UUID: 8f9e2a4c-1d3b-4e7f-9a2c-5d6e8f9a0b1c -->

# Migration Specialist Agent

**Agent Type:** `migration-specialist`

**Purpose:** Orchestrate migrations of projects, files, and code between git repositories while preserving history, metadata, and references.

## Repository Structure Knowledge

### Primary Repositories

**1. ~/dev/lab** - Main monorepo (hopperlabs)
- 500+ projects across personal, work, OSS, shared
- Semantic domains library (127 domains)
- Golden repo templates (14 templates)
- Shared standards, tools, and infrastructure
- Primary working environment

**2. ~/dev/awstools** - AWS tooling monorepo
- AWS-specific utilities and scripts
- Cloud infrastructure helpers
- AWS SDK wrappers and extensions
- Deployment automation

**3. ~/dev/hl-protoflow** - Claude Code Plugin
- Plugin architecture and extensions
- Custom agents and commands
- Workflow automation
- SDLC process tooling

**4. ~/dev/hl-gocoder** - Go development tools
- Go-based tooling and utilities
- CLI applications and services
- Go language specific projects

**5. ~/dev/hl-voicenotes** - Voice notes system
- Voice recording and transcription tools
- Audio processing utilities
- Voice-to-text applications

**6. ~/dev/hl-semantic-models** - Semantic domain models
- Shared semantic domain models
- Ontology definitions and SHACL validation
- Reusable data model primitives
- Cross-project domain specifications

### Submodule Relationships
- awstools can be submodule of lab
- hl-protoflow, hl-gocoder, hl-voicenotes, hl-semantic-models can be independent or linked
- Check `.gitmodules` for current configuration

## Agent Capabilities

### 1. Migration Analysis
- Scan source and target repositories
- Identify dependencies and references
- Map file UUIDs and metadata
- Detect potential conflicts
- Estimate migration complexity

### 2. Git-Safe Migration
- Preserve git history (use `git filter-repo` or `git subtree`)
- Maintain file UUIDs
- Update `.gitmodules` if needed
- Create migration branches
- Generate rollback scripts

### 3. Reference Updates
- Update import paths
- Fix relative file references
- Update documentation links
- Modify build configurations
- Update deployment scripts

### 4. Metadata Preservation
- Maintain file UUID comments
- Preserve YAML frontmatter
- Update `.project` files
- Transfer git commit history
- Maintain file timestamps

### 5. Validation
- Verify all files migrated
- Check build/test still passes
- Validate git history
- Confirm reference updates
- Test deployments

### 6. Project Rename
- In-place folder rename with `git mv` (preserves history)
- Scan monorepo for all references to old name
- Update `.project` file fields
- Update DASHBOARD.md entries
- Update related_prototypes in other projects
- Update deployment configs and Makefiles
- Update import statements if shared library
- Generate rollback script

## ASCII Workflow Visualizations

### Overall Migration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    MIGRATION SPECIALIST WORKFLOW                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Request: "Move proto-xyz from lab to awstools"           │
│       │                                                         │
│       ▼                                                         │
│  ┌──────────────────────────────────────┐                      │
│  │  1. ANALYSIS PHASE                   │                      │
│  │  - Scan source repo structure        │                      │
│  │  - Identify dependencies             │                      │
│  │  - Map file UUIDs                    │                      │
│  │  - Check for conflicts               │                      │
│  │  - Estimate complexity               │                      │
│  └────────────┬─────────────────────────┘                      │
│               │                                                 │
│               ▼                                                 │
│  ┌──────────────────────────────────────┐                      │
│  │  2. PLANNING PHASE                   │                      │
│  │  - Select migration type             │                      │
│  │  - Create git strategy               │                      │
│  │  - List reference updates            │                      │
│  │  - Draft rollback plan               │                      │
│  └────────────┬─────────────────────────┘                      │
│               │                                                 │
│               ▼                                                 │
│  ┌──────────────────────────────────────┐                      │
│  │  3. HUMAN APPROVAL ⚠️                 │                      │
│  │  Present plan for review             │                      │
│  │  [Approve / Modify / Cancel]         │                      │
│  └────────────┬─────────────────────────┘                      │
│               │ (approved)                                      │
│               ▼                                                 │
│  ┌──────────────────────────────────────┐                      │
│  │  4. EXECUTION PHASE                  │                      │
│  │  - Create migration branches         │                      │
│  │  - Execute git operations            │                      │
│  │  - Preserve file UUIDs               │                      │
│  │  - Update references/imports         │                      │
│  │  - Update .gitmodules                │                      │
│  └────────────┬─────────────────────────┘                      │
│               │                                                 │
│               ▼                                                 │
│  ┌──────────────────────────────────────┐                      │
│  │  5. VALIDATION PHASE                 │                      │
│  │  - Run tests in both repos           │                      │
│  │  - Verify builds                     │                      │
│  │  - Check git history intact          │                      │
│  │  - Test deployments                  │                      │
│  └────────────┬─────────────────────────┘                      │
│               │                                                 │
│               ▼                                                 │
│  ┌──────────────────────────────────────┐                      │
│  │  6. DOCUMENTATION PHASE              │                      │
│  │  - Generate rollback script          │                      │
│  │  - Update CHANGELOG.md               │                      │
│  │  - Update README.md                  │                      │
│  │  - Create migration report           │                      │
│  └────────────┬─────────────────────────┘                      │
│               │                                                 │
│               ▼                                                 │
│           ✅ Complete                                           │
│                                                                 │
│  Monitor for 1 week → Archive source (optional)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Repository Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      REPOSITORY ECOSYSTEM                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────┐                │
│  │  ~/dev/lab (Main Monorepo)                 │                │
│  │  ┌──────────────────────────────────────┐  │                │
│  │  │  projects/                           │  │                │
│  │  │    ├─ personal/                      │  │                │
│  │  │    ├─ work/                          │  │◀────┐          │
│  │  │    ├─ oss/                           │  │     │          │
│  │  │    └─ shared/                        │  │     │          │
│  │  ├──────────────────────────────────────┤  │     │          │
│  │  │  shared/                             │  │     │          │
│  │  │    ├─ golden-repos/ (14)            │  │     │          │
│  │  │    ├─ semantic/domains/ (127)       │  │     │          │
│  │  │    ├─ standards/                     │  │     │          │
│  │  │    ├─ tools/  ──────────────────────┼──┼─────┤          │
│  │  │    └─ infra-providers/              │  │     │ MIGRATE  │
│  │  └──────────────────────────────────────┘  │     │          │
│  └────────────────────────────────────────────┘     │          │
│                      │                              │          │
│                      │ submodule?                   │          │
│                      ▼                              │          │
│  ┌────────────────────────────────────────────┐    │          │
│  │  ~/dev/awstools (AWS Tooling Monorepo)     │◀───┘          │
│  │  ┌──────────────────────────────────────┐  │               │
│  │  │  tools/                              │  │               │
│  │  │  core/                               │  │               │
│  │  │  publishing/                         │  │               │
│  │  │  infrastructure/                     │  │               │
│  │  │  deployment/                         │  │               │
│  │  └──────────────────────────────────────┘  │               │
│  └────────────────────────────────────────────┘               │
│                      │                                         │
│                      │ plugin reference                        │
│                      ▼                                         │
│  ┌────────────────────────────────────────────┐               │
│  │  ~/dev/hl-protoflow (Claude Code Plugin)   │               │
│  │  ┌──────────────────────────────────────┐  │               │
│  │  │  agents/                             │  │               │
│  │  │  commands/                           │  │               │
│  │  │  workflows/                          │  │               │
│  │  │  sdlc/                               │  │               │
│  │  └──────────────────────────────────────┘  │               │
│  └────────────────────────────────────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Migration Types

### Type 1: Project Migration (Full Directory)
**Use Case:** Move entire project between repos

**Example:** `lab/projects/work/proto-xyz` → `awstools/tools/xyz`

```
┌─────────────────────────────────────────────────────────────────┐
│              TYPE 1: PROJECT MIGRATION FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SOURCE: ~/dev/lab/projects/work/proto-xyz/                    │
│  ┌──────────────────────────────────┐                          │
│  │  proto-xyz/                      │                          │
│  │    ├─ .project                   │                          │
│  │    ├─ src/                       │                          │
│  │    ├─ tests/                     │                          │
│  │    ├─ package.json               │                          │
│  │    └─ README.md                  │                          │
│  └──────────────┬───────────────────┘                          │
│                 │                                               │
│                 │ git subtree split                             │
│                 │ --prefix=projects/work/proto-xyz              │
│                 │ --branch=migration/proto-xyz                  │
│                 │ (preserves full git history)                  │
│                 │                                               │
│                 ▼                                               │
│  ┌─────────────────────────────────┐                           │
│  │  Isolated branch with history   │                           │
│  │  migration/proto-xyz            │                           │
│  │  - 157 commits preserved        │                           │
│  │  - All authors preserved        │                           │
│  │  - All timestamps preserved     │                           │
│  └─────────────┬───────────────────┘                           │
│                │                                                │
│                │ git subtree add                                │
│                │ ~/dev/awstools tools/xyz                       │
│                │ --squash (optional)                            │
│                │                                                │
│                ▼                                                │
│  TARGET: ~/dev/awstools/tools/xyz/                             │
│  ┌──────────────────────────────────┐                          │
│  │  tools/xyz/                      │                          │
│  │    ├─ .project (updated paths)   │                          │
│  │    ├─ src/                       │                          │
│  │    ├─ tests/                     │                          │
│  │    ├─ package.json               │                          │
│  │    └─ README.md                  │                          │
│  └──────────────────────────────────┘                          │
│                                                                 │
│  POST-MIGRATION:                                                │
│  1. Update imports in awstools consumers                        │
│  2. Update .gitmodules if needed                                │
│  3. Archive lab/projects/work/proto-xyz with pointer            │
│  4. Update documentation                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Steps:**
1. Create migration branch in target repo
2. Use `git subtree split` to extract history
3. Merge into target repo with `git subtree add`
4. Update all references
5. Archive or delete source (after verification)
6. Update submodules if needed

### Type 2: File Migration (Individual Files)
**Use Case:** Move specific files or modules

**Example:** `lab/hmode/shared/tools/aws-helper.py` → `awstools/core/aws-helper.py`

```
┌─────────────────────────────────────────────────────────────────┐
│              TYPE 2: FILE MIGRATION FLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SOURCE: ~/dev/lab/hmode/shared/tools/aws-helper.py                  │
│  ┌──────────────────────────────────┐                          │
│  │  # File UUID: 8f9e2a4c-1d3b...  │                          │
│  │                                  │                          │
│  │  import boto3                    │                          │
│  │  def upload_to_s3(...):          │                          │
│  │      ...                         │                          │
│  └──────────────┬───────────────────┘                          │
│                 │                                               │
│                 │ Copy file                                     │
│                 │ (preserve UUID comment)                       │
│                 │                                               │
│                 ▼                                               │
│  TARGET: ~/dev/awstools/core/aws-helper.py                     │
│  ┌──────────────────────────────────┐                          │
│  │  # File UUID: 8f9e2a4c-1d3b...  │  ← Same UUID             │
│  │                                  │                          │
│  │  import boto3                    │                          │
│  │  def upload_to_s3(...):          │                          │
│  │      ...                         │                          │
│  └──────────────────────────────────┘                          │
│                                                                 │
│  UPDATE CONSUMERS:                                              │
│  ┌──────────────────────────────────┐                          │
│  │  lab/projects/work/app.py        │                          │
│  │                                  │                          │
│  │  # BEFORE:                       │                          │
│  │  from shared.tools import        │                          │
│  │      aws_helper                  │                          │
│  │                                  │                          │
│  │  # AFTER:                        │                          │
│  │  from awstools.core import       │                          │
│  │      aws_helper                  │                          │
│  └──────────────────────────────────┘                          │
│                                                                 │
│  ARCHIVE SOURCE:                                                │
│  ┌──────────────────────────────────┐                          │
│  │  lab/hmode/shared/tools/aws-helper.py  │                          │
│  │                                  │                          │
│  │  # MIGRATED: 2026-02-10          │                          │
│  │  # New location:                 │                          │
│  │  # awstools/core/aws-helper.py   │                          │
│  │  # UUID: 8f9e2a4c-1d3b...        │                          │
│  └──────────────────────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Steps:**
1. Copy file with UUID preservation
2. Commit to target repo
3. Update all import statements
4. Archive source with pointer comment
5. Update documentation

### Type 3: Shared Library Extraction
**Use Case:** Extract reusable code to shared location

**Example:** Plugin logic from lab → hl-protoflow

```
┌─────────────────────────────────────────────────────────────────┐
│           TYPE 3: SHARED LIBRARY EXTRACTION FLOW                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  IDENTIFY SHARED CODE:                                          │
│  ┌──────────────────────────────────────────────┐              │
│  │  lab/hmode/agents/                         │              │
│  │    ├─ domain-modeling-specialist.md          │ ─┐           │
│  │    ├─ ux-component-agent.md                  │  │           │
│  │    ├─ information-architecture-agent.md      │  │ Extract   │
│  │    └─ migration-specialist.md                │  │ these     │
│  └──────────────────────────────────────────────┘  │           │
│                                                     │           │
│                  git filter-repo                    │           │
│                  --path hmode/agents/             │           │
│                  --path-rename hmode/agents/:agents/          │
│                  (creates new repo with history)    │           │
│                                                     │           │
│                                                     ▼           │
│  ┌──────────────────────────────────────────────┐              │
│  │  hl-protoflow/agents/                        │              │
│  │    ├─ domain-modeling-specialist.md          │              │
│  │    ├─ ux-component-agent.md                  │              │
│  │    ├─ information-architecture-agent.md      │              │
│  │    └─ migration-specialist.md                │              │
│  │                                              │              │
│  │  + Full git history from lab                 │              │
│  │  + All UUIDs preserved                       │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  UPDATE SOURCE REPO (OPTION A: Submodule):                     │
│  ┌──────────────────────────────────────────────┐              │
│  │  lab/.gitmodules                             │              │
│  │                                              │              │
│  │  [submodule ".claude/agents"]                │              │
│  │    path = .claude/agents                     │              │
│  │    url = ~/dev/hl-protoflow/agents           │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  UPDATE SOURCE REPO (OPTION B: Import):                        │
│  ┌──────────────────────────────────────────────┐              │
│  │  lab/package.json (or pyproject.toml)        │              │
│  │                                              │              │
│  │  "dependencies": {                           │              │
│  │    "hl-protoflow": "file:../hl-protoflow"    │              │
│  │  }                                           │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Steps:**
1. Identify shared code
2. Create new package structure in target
3. Extract with history using `git filter-repo`
4. Update dependencies in source repo
5. Add as git submodule if needed

### Type 4: Consolidation
**Use Case:** Merge multiple repos or projects

**Example:** Combine scattered AWS tools into awstools

```
┌─────────────────────────────────────────────────────────────────┐
│              TYPE 4: CONSOLIDATION FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BEFORE: Scattered AWS tools across lab                        │
│                                                                 │
│  ┌────────────────────────────────┐                            │
│  │  lab/hmode/shared/tools/             │                            │
│  │    ├─ s3publish.py   ─────┐    │                            │
│  │    ├─ aws-helper.py  ─────┤    │                            │
│  │    └─ cdk-deploy.py  ─────┤    │                            │
│  └───────────────────────────┼────┘                            │
│                               │                                 │
│  ┌────────────────────────────┼───┐                            │
│  │  lab/projects/work/        │   │                            │
│  │    ├─ proto-cdk-stack-a/ ─┤   │                            │
│  │    ├─ proto-cdk-stack-b/ ─┤   │                            │
│  │    └─ proto-aws-monitor/ ─┤   │  CONSOLIDATE               │
│  └────────────────────────────┼───┘       │                    │
│                               │           │                    │
│  ┌────────────────────────────┼───┐       │                    │
│  │  lab/shared/infra/         │   │       │                    │
│  │    ├─ cloudwatch-setup.py ┤   │       │                    │
│  │    └─ iam-policies.py ─────┘   │       │                    │
│  └────────────────────────────────┘       │                    │
│                                           │                    │
│                                           ▼                    │
│  AFTER: Organized awstools structure                           │
│                                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │  awstools/                                   │              │
│  │                                              │              │
│  │  ├─ publishing/                              │              │
│  │  │    └─ s3publish.py      (from shared)     │              │
│  │  │                                           │              │
│  │  ├─ core/                                    │              │
│  │  │    ├─ aws-helper.py     (from shared)     │              │
│  │  │    └─ iam-policies.py   (from infra)      │              │
│  │  │                                           │              │
│  │  ├─ deployment/                              │              │
│  │  │    └─ cdk-deploy.py     (from shared)     │              │
│  │  │                                           │              │
│  │  ├─ infrastructure/                          │              │
│  │  │    ├─ stack-a/          (from projects)   │              │
│  │  │    ├─ stack-b/          (from projects)   │              │
│  │  │    └─ monitoring/       (from projects)   │              │
│  │  │                                           │              │
│  │  └─ observability/                           │              │
│  │       └─ cloudwatch-setup.py (from infra)    │              │
│  │                                              │              │
│  │  Each with full git history preserved        │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  DEDUPLICATION:                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │  Found duplicates:                           │              │
│  │  - s3upload() in 3 locations                 │              │
│  │  - CloudWatch setup in 2 locations           │              │
│  │                                              │              │
│  │  Resolution:                                 │              │
│  │  - Merge into single implementation          │              │
│  │  - Use best version from each                │              │
│  │  - Update all consumers                      │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Steps:**
1. Map all source locations
2. Define target structure
3. Batch migrate with history preservation
4. Deduplicate and refactor
5. Update all consumers

### Type 5: External Project Import (Submodule)
**Use Case:** Bring external projects into lab as submodules

**Example:** External GitHub project → `lab/projects/oss/external-project`

```
┌─────────────────────────────────────────────────────────────────┐
│           TYPE 5: EXTERNAL PROJECT IMPORT FLOW                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  EXTERNAL SOURCE:                                               │
│  ┌──────────────────────────────────────────────┐              │
│  │  https://github.com/user/awesome-tool        │              │
│  │                                              │              │
│  │  ├─ src/                                     │              │
│  │  ├─ tests/                                   │              │
│  │  ├─ README.md                                │              │
│  │  └─ package.json                             │              │
│  │                                              │              │
│  │  + Full git history (500+ commits)           │              │
│  │  + Active development                        │              │
│  │  + Want to track upstream changes            │              │
│  └──────────────────────────────────────────────┘              │
│                      │                                          │
│                      │ git submodule add                        │
│                      │ https://github.com/user/awesome-tool     │
│                      │ projects/oss/external/awesome-tool       │
│                      │                                          │
│                      ▼                                          │
│  LAB STRUCTURE:                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │  lab/projects/oss/external/                  │              │
│  │    └─ awesome-tool/  (submodule)             │              │
│  │         ├─ src/                              │              │
│  │         ├─ tests/                            │              │
│  │         ├─ README.md                         │              │
│  │         └─ package.json                      │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  LAB .gitmodules:                                               │
│  ┌──────────────────────────────────────────────┐              │
│  │  [submodule "projects/oss/external/awesome-tool"]           │
│  │    path = projects/oss/external/awesome-tool │              │
│  │    url = https://github.com/user/awesome-tool│              │
│  │    branch = main                             │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  CREATE LAB WRAPPER:                                            │
│  ┌──────────────────────────────────────────────┐              │
│  │  lab/projects/oss/external/awesome-tool-wrapper/            │
│  │                                              │              │
│  │  ├─ .project  (lab metadata)                 │              │
│  │  ├─ README.md (lab-specific notes)           │              │
│  │  ├─ integration/ (lab-specific code)         │              │
│  │  └─ submodule → ../awesome-tool/             │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  BENEFITS:                                                      │
│  ┌──────────────────────────────────────────────┐              │
│  │  ✓ Track upstream changes                    │              │
│  │  ✓ Easy updates: git submodule update        │              │
│  │  ✓ Pin to specific commit/tag                │              │
│  │  ✓ Local modifications in separate branch    │              │
│  │  ✓ Full history without duplication          │              │
│  │  ✓ Can contribute back upstream              │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  UPDATE WORKFLOW:                                               │
│  ┌──────────────────────────────────────────────┐              │
│  │  # Update to latest upstream                 │              │
│  │  cd projects/oss/external/awesome-tool       │              │
│  │  git fetch origin                            │              │
│  │  git checkout main                           │              │
│  │  git pull origin main                        │              │
│  │                                              │              │
│  │  # Back to lab root, commit submodule update │              │
│  │  cd ~/dev/lab                                │              │
│  │  git add projects/oss/external/awesome-tool  │              │
│  │  git commit -m "Update awesome-tool to v2.1" │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  ALTERNATIVE: Fork + Submodule                                  │
│  ┌──────────────────────────────────────────────┐              │
│  │  1. Fork repo to your GitHub                 │              │
│  │  2. Add YOUR fork as submodule               │              │
│  │  3. Add upstream as remote                   │              │
│  │  4. Can make local changes + push to fork    │              │
│  │  5. Can still sync from upstream             │              │
│  │  6. Can submit PRs back to upstream          │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**When to Use Submodules:**
- ✓ External project with active upstream development
- ✓ Want to track upstream changes easily
- ✓ Need to pin to specific versions/commits
- ✓ Plan to contribute changes back upstream
- ✓ Don't want to fork/duplicate full history

**When NOT to Use Submodules:**
- ✗ One-time import with no upstream tracking
- ✗ Heavily modifying for your use case (fork instead)
- ✗ Upstream is abandoned/archived
- ✗ Simple file/snippet copy (use regular import)

**Steps:**
1. Identify external project URL and branch
2. Add as git submodule: `git submodule add <url> <path>`
3. Create wrapper directory with lab metadata
4. Document integration points
5. Test build/deployment with submodule
6. Commit .gitmodules and submodule pointer

### Type 7: Project Rename (In-Place)
**Use Case:** Rename a project folder and update all references

**Example:** `gocoder-t9x2k` → `gocoder-t9x2k`

```
┌─────────────────────────────────────────────────────────────────┐
│              TYPE 7: PROJECT RENAME FLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BEFORE: Long verbose project name                              │
│  ┌──────────────────────────────────────────────┐              │
│  │  projects/personal/active/                   │              │
│  │    └─ tool-gocoder-web-agentic-coding-...    │              │
│  │         t9x2k/                               │ ← Too long   │
│  │         ├─ .project                          │              │
│  │         ├─ intent-doc.md                     │              │
│  │         ├─ src/                              │              │
│  │         └─ ...                               │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│                                                                 │
│  RENAME WORKFLOW:                                               │
│  ┌──────────────────────────────────────────────┐              │
│  │  1. SCAN PHASE                               │              │
│  │     - Read .project file                     │              │
│  │     - Find all references to this project:   │              │
│  │       • DASHBOARD.md                         │              │
│  │       • Other projects' .project files       │              │
│  │       • Intent docs                          │              │
│  │       • Deployment configs                   │              │
│  │       • Makefile paths                       │              │
│  │       • Import statements                    │              │
│  └────────────┬─────────────────────────────────┘              │
│               │                                                 │
│               ▼                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │  2. PLAN PHASE                               │              │
│  │     - Generate new folder name               │              │
│  │     - List all files to update               │              │
│  │     - Show diff preview                      │              │
│  │     - Human approval required                │              │
│  └────────────┬─────────────────────────────────┘              │
│               │ (approved)                                      │
│               ▼                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │  3. EXECUTE PHASE                            │              │
│  │     - git mv old-folder new-folder           │              │
│  │       (preserves git history!)               │              │
│  │     - Update .project file (id, if needed)   │              │
│  │     - Update all references found in scan    │              │
│  │     - Commit changes atomically              │              │
│  └────────────┬─────────────────────────────────┘              │
│               │                                                 │
│               ▼                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │  4. VALIDATE PHASE                           │              │
│  │     - Verify git history preserved           │              │
│  │     - Check all references updated           │              │
│  │     - Run tests if available                 │              │
│  │     - Generate rollback script               │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│                                                                 │
│  AFTER: Clean short project name                                │
│  ┌──────────────────────────────────────────────┐              │
│  │  projects/personal/active/                   │              │
│  │    └─ gocoder-t9x2k/                         │ ← Clean!    │
│  │         ├─ .project (updated)                │              │
│  │         ├─ intent-doc.md                     │              │
│  │         ├─ src/                              │              │
│  │         └─ ...                               │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Reference Update Patterns:**

```
┌─────────────────────────────────────────────────────────────────┐
│  REFERENCE TYPES TO UPDATE                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DASHBOARD.md                                                │
│  ┌──────────────────────────────────────────────┐              │
│  │  BEFORE:                                     │              │
│  │  | tool-gocoder-web-agentic-... | Phase 8 |  │              │
│  │                                              │              │
│  │  AFTER:                                      │              │
│  │  | gocoder-t9x2k | Phase 8 |                 │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  2. Other .project files (related_prototypes)                  │
│  ┌──────────────────────────────────────────────┐              │
│  │  BEFORE:                                     │              │
│  │  "related_prototypes": [                     │              │
│  │    "tool-gocoder-web-agentic-coding-..."     │              │
│  │  ]                                           │              │
│  │                                              │              │
│  │  AFTER:                                      │              │
│  │  "related_prototypes": [                     │              │
│  │    "gocoder-t9x2k"                           │              │
│  │  ]                                           │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  3. Intent docs / Documentation                                │
│  ┌──────────────────────────────────────────────┐              │
│  │  Search & replace in markdown files:         │              │
│  │  - Absolute paths to project                 │              │
│  │  - Relative references                       │              │
│  │  - Links to project docs                     │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  4. Deployment configs (amplify.yml, Makefile, etc.)           │
│  ┌──────────────────────────────────────────────┐              │
│  │  - Build paths                               │              │
│  │  - Artifact directories                      │              │
│  │  - Environment variables with paths          │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  5. Import statements (if project is shared library)           │
│  ┌──────────────────────────────────────────────┐              │
│  │  Search in Python/TypeScript files:          │              │
│  │  - from tool_gocoder_web... import X         │              │
│  │  - import { X } from 'tool-gocoder-web...'   │              │
│  │                                              │              │
│  │  Update to:                                  │              │
│  │  - from gocoder_t9x2k import X               │              │
│  │  - import { X } from 'gocoder-t9x2k'         │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Naming Convention Rules:**

```
┌─────────────────────────────────────────────────────────────────┐
│  RENAME NAMING RULES                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Standard Format: {short-name}-{id-suffix}                      │
│                                                                 │
│  Examples:                                                      │
│  ┌──────────────────────────────────────────────┐              │
│  │  BEFORE                      │  AFTER        │              │
│  ├──────────────────────────────┼───────────────┤              │
│  │  tool-gocoder-web-agentic-   │  gocoder-t9x2k│              │
│  │  coding-ui-like-claude-code- │               │              │
│  │  web-t9x2k                   │               │              │
│  ├──────────────────────────────┼───────────────┤              │
│  │  proto-voice-assistant-with- │  voice-agent- │              │
│  │  transcription-and-tts-v3j8m │  v3j8m        │              │
│  ├──────────────────────────────┼───────────────┤              │
│  │  internet-switch-device-     │  netswitch-   │              │
│  │  management-app-0sv5e        │  0sv5e        │              │
│  └──────────────────────────────┴───────────────┘              │
│                                                                 │
│  Rules:                                                         │
│  1. Preserve ID suffix (t9x2k, v3j8m, 0sv5e) - ALWAYS          │
│  2. Use short_name from .project if available                  │
│  3. If no short_name, extract core concept (2-3 words max)     │
│  4. Lowercase, hyphenated                                      │
│  5. Max 30 characters total                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Steps:**
1. Read `.project` file to extract `short_name` and `id`
2. Generate new folder name: `{short_name}-{id_suffix}`
3. Scan all files in monorepo for references to old name
4. Show rename plan and get human approval
5. Execute `git mv` to preserve history
6. Update `.project` file fields if needed
7. Update all references found in scan
8. Commit atomically with descriptive message
9. Generate rollback script
10. Validate (test builds, check references)

### Type 6: Sparse Checkout (Partial Clone)
**Use Case:** Work on subset of large monorepo without checking out everything

**Example:** Only checkout specific projects from lab

```
┌─────────────────────────────────────────────────────────────────┐
│              TYPE 6: SPARSE CHECKOUT FLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PROBLEM: Large monorepo (lab = 500+ projects, 10GB+)          │
│  ┌──────────────────────────────────────────────┐              │
│  │  ~/dev/lab (Full Clone)                      │              │
│  │  ┌────────────────────────────────────────┐  │              │
│  │  │  projects/                             │  │              │
│  │  │    ├─ personal/ (150 projects)         │  │ Too much!   │
│  │  │    ├─ work/ (200 projects)             │  │ Slow clone  │
│  │  │    ├─ oss/ (100 projects)              │  │ Large disk  │
│  │  │    └─ shared/ (50 projects)            │  │ usage       │
│  │  ├─ shared/ (golden repos, domains, etc) │  │              │
│  │  ├─ .claude/ (commands, docs, agents)    │  │              │
│  │  └─ ... (all other directories)           │  │              │
│  │  └────────────────────────────────────────┘  │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│                                                                 │
│  SOLUTION: Sparse checkout only what you need                  │
│                                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │  ~/dev/lab-sparse (Sparse Clone)             │              │
│  │  ┌────────────────────────────────────────┐  │              │
│  │  │  projects/                             │  │              │
│  │  │    └─ work/                            │  │ Only what   │
│  │  │         ├─ proto-xyz/  ✓               │  │ you need!   │
│  │  │         └─ proto-abc/  ✓               │  │ Fast clone  │
│  │  ├─ shared/                                │  │ Small disk  │
│  │  │    ├─ tools/ ✓                         │  │ usage       │
│  │  │    └─ standards/ ✓                     │  │              │
│  │  ├─ .claude/ ✓                            │  │              │
│  │  └─ ... (other needed directories)        │  │              │
│  │  └────────────────────────────────────────┘  │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│                                                                 │
│  SETUP WORKFLOW:                                                │
│  ┌──────────────────────────────────────────────┐              │
│  │  # 1. Clone with sparse checkout enabled     │              │
│  │  git clone --filter=blob:none --sparse \     │              │
│  │    ~/dev/lab ~/dev/lab-sparse                │              │
│  │                                              │              │
│  │  cd ~/dev/lab-sparse                         │              │
│  │                                              │              │
│  │  # 2. Initialize sparse checkout             │              │
│  │  git sparse-checkout init --cone            │              │
│  │                                              │              │
│  │  # 3. Add directories you need               │              │
│  │  git sparse-checkout set \                   │              │
│  │    projects/work/proto-xyz \                 │              │
│  │    projects/work/proto-abc \                 │              │
│  │    shared/tools \                            │              │
│  │    shared/standards \                        │              │
│  │    .claude                                   │              │
│  │                                              │              │
│  │  # 4. Files automatically checked out        │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│                                                                 │
│  DYNAMIC UPDATES:                                               │
│  ┌──────────────────────────────────────────────┐              │
│  │  # Add more directories as needed            │              │
│  │  git sparse-checkout add \                   │              │
│  │    projects/personal/my-app \                │              │
│  │    hmode/shared/golden-repos/typescript-nextjs     │              │
│  │                                              │              │
│  │  # Remove directories no longer needed       │              │
│  │  git sparse-checkout set \                   │              │
│  │    projects/work/proto-xyz \                 │              │
│  │    shared/tools \                            │              │
│  │    .claude                                   │              │
│  │  # (proto-abc removed)                       │              │
│  │                                              │              │
│  │  # List current sparse patterns              │              │
│  │  git sparse-checkout list                    │              │
│  │                                              │              │
│  │  # Disable sparse checkout (revert to full)  │              │
│  │  git sparse-checkout disable                 │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Cone Mode vs Non-Cone Mode:**

```
┌─────────────────────────────────────────────────────────────────┐
│  CONE MODE (Recommended - faster, simpler)                      │
│  ┌──────────────────────────────────────────────┐              │
│  │  git sparse-checkout init --cone             │              │
│  │  git sparse-checkout set projects/work       │              │
│  │                                              │              │
│  │  Checks out:                                 │              │
│  │  ✓ projects/work/ (entire directory tree)   │              │
│  │  ✓ All files at root (CLAUDE.md, etc.)      │              │
│  │                                              │              │
│  │  Benefits:                                   │              │
│  │  - Faster performance                        │              │
│  │  - Simpler patterns                          │              │
│  │  - Better git tooling support                │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  NON-CONE MODE (Flexible - complex patterns)                   │
│  ┌──────────────────────────────────────────────┐              │
│  │  git sparse-checkout init --no-cone          │              │
│  │  git sparse-checkout set \                   │              │
│  │    'projects/work/proto-*' \                 │              │
│  │    'hmode/shared/tools/*.py'                       │              │
│  │                                              │              │
│  │  Checks out:                                 │              │
│  │  ✓ projects/work/proto-xyz/                  │              │
│  │  ✓ projects/work/proto-abc/                  │              │
│  │  ✓ hmode/shared/tools/s3publish.py                 │              │
│  │  ✓ hmode/shared/tools/aws-helper.py                │              │
│  │                                              │              │
│  │  Benefits:                                   │              │
│  │  - Glob patterns supported                   │              │
│  │  - File-level granularity                    │              │
│  │  - Cherry-pick specific files                │              │
│  └──────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

**Integration with Submodules:**

```
┌─────────────────────────────────────────────────────────────────┐
│  SPARSE CHECKOUT + SUBMODULES = Power Combo                     │
│                                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │  lab-sparse/                                 │              │
│  │    ├─ projects/work/proto-xyz/ (sparse)      │              │
│  │    ├─ hmode/shared/tools/ (sparse)                 │              │
│  │    └─ awstools/ (submodule)                  │              │
│  │         └─ core/ (also sparse!)              │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  Setup:                                                         │
│  ┌──────────────────────────────────────────────┐              │
│  │  # 1. Main repo sparse checkout              │              │
│  │  git clone --filter=blob:none --sparse \     │              │
│  │    ~/dev/lab ~/dev/lab-sparse                │              │
│  │  cd ~/dev/lab-sparse                         │              │
│  │  git sparse-checkout set projects/work       │              │
│  │                                              │              │
│  │  # 2. Add submodule                          │              │
│  │  git submodule add ~/dev/awstools awstools   │              │
│  │                                              │              │
│  │  # 3. Sparse checkout in submodule           │              │
│  │  cd awstools                                 │              │
│  │  git sparse-checkout init --cone             │              │
│  │  git sparse-checkout set core deployment    │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Common Sparse Checkout Patterns:**

```
┌─────────────────────────────────────────────────────────────────┐
│  PATTERN 1: Work on single project + shared tools               │
│  ┌──────────────────────────────────────────────┐              │
│  │  git sparse-checkout set \                   │              │
│  │    projects/work/my-current-project \        │              │
│  │    shared/tools \                            │              │
│  │    shared/standards \                        │              │
│  │    .claude                                   │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  PATTERN 2: Work on category of projects                       │
│  ┌──────────────────────────────────────────────┐              │
│  │  git sparse-checkout set \                   │              │
│  │    projects/work \                           │              │
│  │    shared                                    │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  PATTERN 3: Infrastructure work only                           │
│  ┌──────────────────────────────────────────────┐              │
│  │  git sparse-checkout set \                   │              │
│  │    infra \                                   │              │
│  │    shared/infra-providers \                  │              │
│  │    .github/workflows                         │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
│  PATTERN 4: Documentation and config only                      │
│  ┌──────────────────────────────────────────────┐              │
│  │  git sparse-checkout set \                   │              │
│  │    .claude \                                 │              │
│  │    .guardrails \                             │              │
│  │    CLAUDE.md \                               │              │
│  │    README.md                                 │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Sparse Checkout Helper Script:**

```bash
#!/bin/bash
# sparse-lab - Helper for sparse checkout management
# Usage: sparse-lab [command] [args...]

case "$1" in
  init)
    # Initialize sparse checkout with common files
    git sparse-checkout init --cone
    git sparse-checkout set .claude .guardrails shared/tools
    echo "✓ Sparse checkout initialized"
    ;;

  add)
    # Add directory to sparse checkout
    shift
    git sparse-checkout add "$@"
    echo "✓ Added: $@"
    ;;

  work-on)
    # Quick setup for working on a project
    PROJECT=$2
    git sparse-checkout set \
      "projects/work/$PROJECT" \
      shared/tools \
      shared/standards \
      .claude
    echo "✓ Ready to work on: $PROJECT"
    ;;

  list)
    # List current sparse patterns
    git sparse-checkout list
    ;;

  full)
    # Disable sparse checkout (go back to full)
    git sparse-checkout disable
    echo "✓ Sparse checkout disabled - full repo checked out"
    ;;

  *)
    echo "Usage: sparse-lab {init|add|work-on|list|full}"
    exit 1
    ;;
esac
```

**When to Use Sparse Checkout:**
- ✓ Large monorepo (1GB+)
- ✓ Only need to work on specific projects
- ✓ Limited disk space
- ✓ Faster clone and checkout operations
- ✓ CI/CD pipelines (only build what changed)
- ✓ Multiple workspaces for different projects

**When NOT to Use Sparse Checkout:**
- ✗ Small repo (<100MB)
- ✗ Need to search/grep across entire codebase
- ✗ Frequent cross-project refactoring
- ✗ Tools that assume full checkout

**Steps:**
1. Clone with `--filter=blob:none --sparse` (partial clone)
2. Initialize sparse checkout: `git sparse-checkout init --cone`
3. Set directories: `git sparse-checkout set <paths>`
4. Dynamically add/remove as needed
5. Can disable anytime with `git sparse-checkout disable`

## Usage Patterns

### Interactive Migration
```bash
# Spawn migration agent
claude --agent migration-specialist

# Provide migration request
User: "Move proto-aws-deployer-xyz from lab to awstools"

# Agent analyzes, plans, confirms, executes
```

### Automated Migration (via orchestrator)
```python
from pathlib import Path
import asyncio

async def migrate_project(source_repo, target_repo, project_path):
    """Orchestrate migration using Claude subprocess"""

    prompt = f"""
    Migration Request:
    - Source: {source_repo}/{project_path}
    - Target: {target_repo}/

    Steps:
    1. Analyze project structure and dependencies
    2. Create migration plan
    3. Execute git-safe migration with history
    4. Update all references
    5. Validate and test
    6. Generate rollback script

    Preserve: UUIDs, metadata, git history, submodules
    """

    # Spawn migration agent subprocess
    process = await asyncio.create_subprocess_exec(
        'claude',
        '--permission-mode', 'bypassPermissions',
        '--model', 'sonnet',
        '--print',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    process.stdin.write(prompt.encode('utf-8'))
    await process.stdin.drain()
    process.stdin.close()

    # Stream progress
    async for line in process.stdout:
        print(line.decode('utf-8').strip())

    await process.wait()
    return process.returncode == 0
```

## Migration Checklist

**Pre-Migration:**
- [ ] Verify clean working directory (no uncommitted changes)
- [ ] Create backup branches in both repos
- [ ] Document current state (file paths, UUIDs, references)
- [ ] Identify all dependencies and consumers
- [ ] Plan rollback strategy

**During Migration:**
- [ ] Preserve file UUIDs in all migrated files
- [ ] Maintain git commit history
- [ ] Update all import paths
- [ ] Fix relative file references
- [ ] Update `.gitmodules` if using submodules
- [ ] Commit migration in atomic steps
- [ ] Document migration in commit messages

**Post-Migration:**
- [ ] Run tests in both repos
- [ ] Verify builds succeed
- [ ] Check all references resolve
- [ ] Test deployments
- [ ] Update documentation
- [ ] Archive source (don't delete immediately)
- [ ] Create rollback instructions
- [ ] Monitor for issues (1 week minimum)

## Safety Mechanisms

### 1. Dry Run Mode
```bash
# Agent simulates migration without changes
--dry-run flag
```

### 2. Rollback Script Generation
```bash
#!/bin/bash
# Generated by migration-specialist
# Rollback migration of proto-xyz from awstools to lab
# Created: 2026-02-10

cd ~/dev/awstools
git checkout main
git branch -D migration/proto-xyz
git clean -fd tools/xyz/

cd ~/dev/lab
git checkout main
git branch -D archive/proto-xyz
# Restore from backup...
```

### 3. Validation Gates
- Git status check before starting
- Test suite execution before finalizing
- Manual approval for destructive operations
- Staged commits (not all-at-once)

### 4. Conflict Resolution
- Detect file name collisions
- Identify duplicate UUIDs
- Flag incompatible dependencies
- Prompt for resolution strategy

## Integration with SDLC

**Migration as Phase 0.5 (Brownfield Prep):**
- Migrate before starting brownfield work
- Consolidate scattered codebases
- Extract shared libraries
- Prepare for Phase 8 implementation

**Migration Documentation:**
- Update ARCHITECTURE.md with new locations
- Document migration rationale
- Update CHANGELOG.md
- Add migration notes to README.md

## Example Migrations

### Example 1: AWS Tool from Lab to Awstools
```
Source: ~/dev/lab/hmode/shared/tools/s3publish.py
Target: ~/dev/awstools/publishing/s3publish.py

Steps:
1. Copy file with UUID (8f9e2a4c...)
2. Update imports in lab consumers
3. Add as git submodule: lab/hmode/shared/tools/s3publish.py → awstools submodule
4. Or: Keep in lab, reference from awstools via relative path
5. Commit to both repos with linked commit messages
```

### Example 2: Plugin Agent to hl-protoflow
```
Source: ~/dev/lab/hmode/agents/domain-modeling-specialist.md
Target: ~/dev/hl-protoflow/agents/domain-modeling-specialist.md

Steps:
1. Extract agent logic with git history
2. Update hl-protoflow agent registry
3. Update lab to reference plugin agent (if plugin installed)
4. Test agent invocation from lab
5. Document plugin dependency
```

### Example 3: Consolidate AWS Infrastructure
```
Sources:
- ~/dev/lab/projects/work/proto-cdk-stack-a/
- ~/dev/lab/projects/work/proto-cdk-stack-b/
- ~/dev/lab/hmode/shared/infra-providers/aws/

Target: ~/dev/awstools/infrastructure/

Steps:
1. Map all CDK stacks and shared code
2. Define consolidated structure
3. Migrate with history using git subtree
4. Deduplicate common patterns
5. Update all deployments to use awstools
6. Archive old locations with pointers
```

### Example 4: Project Rename (Type 7)
```
Source: ~/dev/lab/projects/personal/active/gocoder-t9x2k/
Target: ~/dev/lab/projects/personal/active/gocoder-t9x2k/

Steps:
1. Read .project file - extract short_name: "gocoder", id suffix: "t9x2k"
2. Scan monorepo for references:
   - Found: 0 references in DASHBOARD.md
   - Found: 0 related_prototypes in other .project files
   - Found: 2 deployment config references
3. Show plan to human, get approval
4. Execute: git mv tool-gocoder-web-agentic-... gocoder-t9x2k
5. Update .project file if needed (name field already clean)
6. Update deployment configs with new path
7. Commit: "refactor: rename tool-gocoder-web-... to gocoder-t9x2k"
8. Generate rollback script: rollback-rename-gocoder-t9x2k.sh
9. Validate: check git log --follow shows history preserved
```

## Agent Invocation

**Add to CLAUDE.md Section 5.1 Gate Trigger Matrix:**

```markdown
| Action Type              | ... | Migration |
|--------------------------|-----|-----------|
| Move project between repos|     |     ✓     |
| Extract shared library    |     |     ✓     |
| Consolidate repos         |     |     ✓     |
| File migration            |     |     ✓     |
```

**Add to Task Tool Description:**

```markdown
- migration-specialist: Use this agent when you need to migrate projects, files, or code between git repositories. This includes:

**Migration scenarios:**
- Moving entire projects between ~/dev/lab, ~/dev/awstools, ~/dev/hl-protoflow
- Extracting shared libraries to dedicated repos
- Consolidating scattered code into monorepos
- Migrating files while preserving git history and metadata
- Updating submodules and cross-repo references

**Example interactions:**

<example>
Context: User wants to move AWS utility from lab to awstools
user: "Move the s3publish.py tool from lab/shared/tools to awstools"
assistant: "I'll use the migration-specialist agent to safely migrate this file with history preservation."
<Uses Task tool to spawn migration-specialist>
Commentary: The agent handles git history, UUID preservation, and reference updates.
</example>

**Proactive usage:**
When Claude Code detects migration keywords ("move to", "consolidate", "extract to"), it should proactively use this agent.

(Tools: All tools)
```

## Performance & Cost

**Typical Migration:**
- Analysis: 30 seconds (Haiku)
- Execution: 2-5 minutes (Sonnet)
- Validation: 1 minute (Haiku)
- Cost: $0.10 - $0.50 per migration

**Batch Migration:**
- Use orchestrator for multiple projects
- Parallel analysis, sequential execution
- Cost scales linearly with project count

## Future Enhancements

1. **Migration Playground:** Safe sandbox to test migrations
2. **History Visualization:** Show what will change before executing
3. **Dependency Graph:** Visualize cross-repo relationships
4. **Auto-Rollback:** Automatic revert on validation failure
5. **Migration Templates:** Pre-configured patterns for common migrations
6. **Integration Tests:** Verify migrations don't break consumers

## Related Documentation

- `@patterns/CHILD_PROCESSES` - Agent orchestration patterns
- `@core/GUARDRAILS` - Safety rules for migrations
- `@reference/DIRECTORY_STRUCTURE` - Repo organization
- Section 7.9 - File UUID standards
- Section 9.0 - File organization

## Summary

**migration-specialist** handles all aspects of moving and renaming code:
- Git-safe with history preservation
- UUID and metadata tracking
- Reference and import updates
- Validation and rollback
- Multi-repo awareness (lab, awstools, hl-protoflow)
- In-place project renaming with reference updates

**Migration Types:**
| Type | Use Case |
|------|----------|
| Type 1 | Project Migration (full directory between repos) |
| Type 2 | File Migration (individual files) |
| Type 3 | Shared Library Extraction |
| Type 4 | Consolidation (merge multiple sources) |
| Type 5 | External Project Import (submodule) |
| Type 6 | Sparse Checkout (partial clone) |
| Type 7 | Project Rename (in-place with ref updates) |

**Invoke when:** User requests project/file migration, consolidation, extraction, or **rename**.
**Trigger keywords:** "move to", "consolidate", "extract to", "rename", "shorten name"
**Model:** Sonnet (balanced quality and cost for git operations)
**Safety:** Always creates rollback scripts and validation gates
