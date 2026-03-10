---
name: quality-control
description: Repository stability checker with interactive fixes
version: 1.0.0
---

# Quality Control Skill

**Run stability checks, present fixes 3 at a time (2 lines max)**

## Execution Flow

1. **Scan repo** → collect issues
2. **Categorize** → CRITICAL, WARNING, INFO
3. **Present 3 fixes** → numeric IDs, 2-line descriptions
4. **Get user approval** → comma-separated IDs, 'all', 'skip'
5. **Apply fixes** → show results
6. **Repeat** → next 3 fixes
7. **Generate report** → stability score

## Issue Detection

### Critical Issues
- Loose code files in root (`.py`, `.js`, `.ts`)
- Prototypes missing `.project`
- Phase ≥7 projects in `ideas/`
- Phase <7 projects in `prototypes/`

### Warnings
- Missing `README.md`
- Non-standard folders in `prototypes/`
- Naming convention violations

### Info
- Empty directories
- Outdated timestamps in `.project`
- Documentation suggestions

## Fix Presentation Format

**2 lines max per fix:**

```
[ID] FILE/FOLDER → ACTION
    Context: Brief reason (optional, if needed)
```

**Examples:**
```
[1] flight_scraper.py → Move to proto-016-flight-scraper/src/
[2] proto-001-loan/.project → Fix phase field (7→IMPLEMENTATION)
[3] artifacts/delivery/ → Move to prototypes/proto-XXX-artifacts/delivery/
    Context: Non-standard folder in prototypes root
```

## Interactive Prompts

**After each 3-fix batch:**
```
Accept fixes? Options:
  - Comma-separated: 1,3
  - 'all': Apply all 3
  - 'skip': Skip all 3
  - 'quit': Stop and generate report

Your choice:
```

## Fix Categories

### Auto-safe (no approval needed if --auto flag)
- Create missing `README.md` (from template)
- Fix `.project` phase field mismatches

### Requires approval (always prompt)
- Move code files
- Rename folders
- Delete code files
- Modify `.project` structure

### Manual only (report but don't fix)
- Phase transitions (user must run phase commands)
- Merge duplicate prototypes
- Complex refactors

## Implementation Rules

1. **Batch fixes** → Execute all approved fixes from current batch together
2. **Validate before apply** → Check file exists, target dir exists
3. **Rollback on error** → If one fix fails, rollback batch
4. **Log all actions** → Append to `.claude/quality-control.log`
5. **Update report** → Show before/after stats

## Report Format

```markdown
# Stability Report - 2025-11-11T14:30:00Z

## 📊 Score: 85/100 (Good)

## ✅ PASS (12 checks)
- Prototype .project files: 17/17
- Ideas .project files: 20/20
- Phase consistency: 100%

## ⚠️  WARNINGS (3)
- [PENDING] proto-022/README.md: Missing
- [SKIPPED] proto-016: Not in standard location

## ❌ CRITICAL (2)
- [FIXED] flight_scraper.py: Moved to proto-016/src/
- [FIXED] modal_flight_scraper.py: Moved to proto-016/src/

## 🔧 Fixes Applied: 5/8
- Auto: 0
- Interactive: 5 (file moves)
- Skipped: 3 (user declined)

## 📈 Improvement: 65 → 85 (+20 points)

## Remaining Issues (3)
1. proto-022/README.md: Create missing doc
2. artifacts/delivery/: Move to prototypes/proto-XXX-artifacts/delivery/
3. 12 loose files in root: Organize into prototypes

## Next Steps
- Run /quality-control again to address remaining issues
- Consider moving artifacts/delivery/ to proper prototype structure
- Archive or organize root-level experiment files
```

## CLI Arguments

```bash
# Interactive mode (default)
/quality-control

# Report only, no fixes
/quality-control --report-only

# Auto-fix safe issues, prompt for others
/quality-control --auto-safe

# Check specific path
/quality-control prototypes/proto-015-claude-power-tools

# Verbose output
/quality-control --verbose
```

## Error Handling

**Permission denied:** Skip fix, note in report
**File not found:** Skip fix, mark as already resolved
**Invalid target:** Prompt user for correct target
**Git conflicts:** Abort fix, warn user

## Success Criteria

- All CRITICAL issues addressed (fixed or documented why not)
- Warnings reduced to <5
- Stability score ≥90
- All prototypes have `.project` + `README.md`
- No loose code files in root
- Phase consistency 100%
