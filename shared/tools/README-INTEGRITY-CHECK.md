# Repository Integrity Checker

## Overview

Pre-commit hook that validates project integrity to maintain repository quality.

## What It Checks

### 1. Project ID Management
- ✅ All folders have valid `{name}-{5char}` format
- ✅ No duplicate project IDs across projects/
- ✅ IDs are properly formatted (allowed prefixes: `tool-`, `lib-`, `service-`, `protocol-`, `poc-`)

### 2. Project State Validation
- ✅ Phase names match phase numbers (e.g., IMPLEMENTATION = 8)
- ✅ Status matches phase (COMPLETED requires phase 9+)
- ✅ Phase history is sequential and complete
- ✅ Current phase matches last phase in history
- ✅ ACTIVE projects shouldn't have completed current phase

### 3. File Consistency
- ✅ Directory name matches `.project` name field
- ✅ `.project` file exists for all projects
- ✅ Valid phase and status values
- ✅ Version and version_history fields present

### 4. Manifest Synchronization
- ✅ All filesystem projects exist in manifest
- ✅ All manifest projects exist in filesystem
- ✅ No orphaned entries

### 5. Portfolio Sync
- ✅ Portfolio prototype exists
- ✅ Portfolio is up to date with manifest changes

## Usage

### Automatic (Pre-commit Hook)

Runs automatically on every commit:

```bash
git add .
git commit -m "Your message"
# Integrity checks run automatically
```

### Manual Check

```bash
node tools/integrity-check.js
```

### Skip Checks (Not Recommended)

```bash
git commit --no-verify
```

## Error Types

### Critical Errors (Block Commit)

| Error | Description | Fix |
|-------|-------------|-----|
| `ID_COLLISION` | Two projects use same ID | Rename one project |
| `MISSING_PROJECT_ID` | Folder has no valid ID | Rename folder with proper ID |
| `INVALID_STATE` | Status/phase mismatch | Update status or phase |
| `PHASE_NUMBER_MISMATCH` | Phase name doesn't match number | Update phase_number field |
| `PHASE_HISTORY_MISMATCH` | Last history ≠ current phase | Fix phase_history or current_phase |
| `MISSING_PROJECT_FILE` | No `.project` file | Create `.project` file |
| `INVALID_JSON` | Malformed `.project` JSON | Fix JSON syntax |

### Warnings (Don't Block)

| Warning | Description | Action |
|---------|-------------|--------|
| `MISSING_FROM_MANIFEST` | Project not in manifest | Run `/update-manifest` |
| `MISSING_FROM_FILESYSTEM` | Manifest entry has no folder | Remove from manifest or restore folder |
| `PORTFOLIO_OUTDATED` | Portfolio needs update | Update portfolio prototype |
| `ACTIVE_WITH_COMPLETED_PHASE` | ACTIVE but phase complete | Transition to next phase or set ON_HOLD |
| `MISSING_VERSION` | No version field | Add semantic version |

## Phase Number Reference

| Phase | Number | Phase | Number |
|-------|--------|-------|--------|
| SEED | 1 | TEST_DESIGN | 7 |
| RESEARCH | 2 | IMPLEMENTATION | 8 |
| IDEA_EXPANSION | 3 | REFINEMENT | 9 |
| IDEA_ANALYSIS | 4 | DIVERGENT_IMPLEMENTATION | 8.1 |
| IDEA_CANDIDATE_SELECTION | 5 | DIVERGENT_EVALUATION | 8.2 |
| TECHNICAL_DESIGN | 6 | CONVERGENCE | 8.3 |

COMPLETED/GRADUATED/ARCHIVED also use phase_number 9.

## Common Fixes

### Fix ID Collision

```bash
# Rename one of the projects with unique ID
mv projects/personal/active/old-name-abc12 projects/personal/active/old-name-xyz34

# Update .project name field
# Edit: projects/personal/active/old-name-xyz34/.project
# Change: "name": "old-name-xyz34"
```

### Fix Phase Number Mismatch

```bash
# Edit .project file
{
  "current_phase": "IMPLEMENTATION",
  "phase_number": 8  // Was 6, now corrected
}
```

### Fix Invalid State

```bash
# If COMPLETED but not in phase 9:
{
  "current_phase": "REFINEMENT",  // Change from IMPLEMENTATION
  "phase_number": 9,               // Change from 8
  "status": "COMPLETED"
}
```

### Fix Missing Project ID

```bash
# Rename folder to include proper ID
mv projects/work/active/workflow-automation-docs projects/work/active/workflow-automation-docs-d9n0m

# Update .project name
{
  "name": "workflow-automation-docs-d9n0m"
}
```

## Automation

The pre-commit hook automatically:

1. **Security scanning** - Checks for secrets/credentials
2. **Integrity validation** - Runs this checker
3. **Manifest update** - Auto-updates manifest if `.project` files changed
4. **README update** - Regenerates root README with latest data

## Configuration

Hook location: `.git/hooks/pre-commit`
Script location: `tools/integrity-check.js`

To disable permanently (not recommended):
```bash
rm .git/hooks/pre-commit
```

## Exit Codes

- `0` - All checks passed
- `1` - Critical errors found (blocks commit)

## See Also

- `tools/fix-integrity-issues.js` - Automated fixer (coming soon)
- `/update-manifest` - Slash command to sync manifest
- `/prototype-status` - Check individual prototype status
