---
version: 1.0.0
last_updated: 2025-11-21
description: Preview changes to core infrastructure (CLAUDE.md, .claude, shared)
---

# Check Core Infrastructure Changes

You are a breaking change detection assistant. Review all pending changes to core infrastructure files and warn about potential breaking changes.

## Parameters

- `--full` - Show full diffs (default: summary only)
- `--staged` - Only show staged changes
- `--unstaged` - Only show unstaged changes
- `--summary` - Summary only (no diffs)

## Instructions

1. **Check git status** for core infrastructure files:
   ```bash
   git status CLAUDE.md .claude/ shared/ --short
   ```

2. **Identify changed files** in these categories:
   - `CLAUDE.md` - Main orchestration file
   - `hmode/docs/` - Modular documentation
   - `hmode/commands/` - Slash commands
   - `shared/` - Shared utilities and infrastructure

3. **For each changed file**, determine:
   - Change type: Modified (M), Added (A), Deleted (D), Renamed (R)
   - File category: orchestration, documentation, command, utility
   - Breaking change risk: 🔴 High, 🟡 Medium, 🟢 Low

4. **Show summary**:
   ```
   🔍 Core Infrastructure Changes
   ==============================

   📊 Summary:
   - CLAUDE.md: 1 file modified
   - hmode/docs/: 3 files modified, 1 added
   - hmode/commands/: 2 files modified
   - shared/: 5 files modified, 1 deleted

   Total: 13 files changed

   🔴 High Risk Changes:
   - CLAUDE.md (orchestration logic changed)
   - hmode/docs/core/CRITICAL_RULES.md (rules modified)
   - shared/aws/aws_auth.py (credential handling changed)

   🟡 Medium Risk Changes:
   - hmode/docs/processes/PHASE_8_IMPLEMENTATION.md
   - hmode/commands/new-prototype.md

   🟢 Low Risk Changes:
   - hmode/docs/reference/EXAMPLES.md
   - shared/utils/formatting.py
   ```

5. **Breaking change detection rules**:

   **🔴 High Risk (Breaking Changes Likely)**:
   - `CLAUDE.md` - Any changes to orchestration logic, rules, workflows
   - `hmode/docs/core/CRITICAL_RULES.md` - Rule changes
   - `hmode/docs/core/CONFIRMATION_PROTOCOL.md` - Protocol changes
   - `shared/aws/` - Credential handling, authentication
   - `hmode/shared/standards/` - Code standard changes
   - Deleted files in `shared/` or `hmode/docs/core/`

   **🟡 Medium Risk (May Affect Behavior)**:
   - `hmode/docs/processes/` - Phase behavior changes
   - `hmode/commands/` - Command behavior changes
   - `shared/utils/` - Utility function signature changes
   - Renamed files

   **🟢 Low Risk (Safe Changes)**:
   - `hmode/docs/reference/` - Documentation updates
   - `hmode/docs/patterns/` - Pattern additions
   - Comment changes
   - Formatting changes
   - New files added (non-breaking)

6. **For each high-risk change**, show:
   ```
   🔴 CLAUDE.md (Modified)
   ────────────────────────────
   Breaking Change Risk: HIGH
   Reason: Orchestration logic affects all AI interactions

   Changes:
   - Line 45: Modified SDLC phase detection logic
   - Line 123: Added new required rule (#18)
   - Line 200: Changed dynamic loading behavior

   Impact:
   - All sessions will use new detection logic
   - New rule must be followed immediately
   - File loading patterns may change

   Review Required: YES ⚠️
   ```

7. **Show diffs** (if --full flag):
   ```bash
   git diff CLAUDE.md
   git diff hmode/docs/core/CRITICAL_RULES.md
   # etc for each changed file
   ```

8. **Provide recommendations**:
   ```
   📋 Recommendations:

   ✅ Safe to commit:
   - Documentation updates in hmode/docs/reference/
   - New command additions in hmode/commands/

   ⚠️ Review before commit:
   - CLAUDE.md changes (orchestration)
   - shared/aws/aws_auth.py (credential handling)

   🚫 DO NOT commit without approval:
   - hmode/docs/core/CRITICAL_RULES.md (rule changes)

   💡 Next Steps:
   1. Review high-risk changes carefully
   2. Test orchestration changes in isolated session
   3. Get approval for rule changes
   4. Consider creating backup: cp CLAUDE.md CLAUDE.md.backup
   5. Update version numbers if breaking changes
   ```

9. **File-specific checks**:

   **CLAUDE.md**:
   - Check for changes to rules section
   - Check for changes to loading logic
   - Check for removed sections
   - Verify Quick Reference Table intact

   **hmode/docs/core/**:
   - Check for rule additions/deletions
   - Check for protocol changes
   - Check for deleted files

   **hmode/commands/**:
   - Check for changed command signatures
   - Check for deleted commands
   - Check for parameter changes

   **shared/aws/**:
   - Check for credential handling changes
   - Check for authentication logic changes
   - Check for breaking API changes

   **hmode/shared/standards/**:
   - Check for code standard changes
   - Check for linting rule changes

10. **Output format**:
    ```
    🔍 Core Infrastructure Changes
    ==============================

    [Summary section]

    [Breaking change detection]

    [Detailed change analysis]

    [Recommendations]

    [Action items]
    ```

## Implementation Notes

1. **Use git diff** to detect actual changes, not just file modifications
2. **Parse diff output** to identify specific line changes
3. **Categorize changes** by risk level automatically
4. **Highlight breaking changes** with clear warnings
5. **Provide actionable recommendations** for next steps

## Example Usage

```bash
/check-core                    # Summary of all changes
/check-core --full             # Show full diffs
/check-core --staged           # Only staged changes
/check-core --summary          # Just counts and file list
```

## Advanced Detection

1. **Detect removed sections** in CLAUDE.md:
   - Compare old vs new structure
   - Warn if critical sections removed

2. **Detect rule number changes**:
   - If CRITICAL_RULES.md changes rule numbers
   - Warn about potential documentation drift

3. **Detect credential pattern changes**:
   - If shared/aws/ changes env var names
   - Warn about breaking auth changes

4. **Detect command signature changes**:
   - If hmode/commands/ changes parameters
   - Warn about slash command breakage

## Use Cases

- **Pre-commit review** - Check changes before committing
- **Breaking change detection** - Identify risky changes
- **Infrastructure audit** - Review all core changes
- **Version bump decision** - Determine if major/minor/patch
- **Rollback planning** - Understand what changed for rollback

## Output Modes

### Summary (default):
```
13 files changed (7 modified, 4 added, 2 deleted)
🔴 3 high-risk | 🟡 5 medium-risk | 🟢 5 low-risk
```

### Full:
```
[Summary]
[Breaking change warnings]
[Full diffs for each file]
[Recommendations]
```

### JSON:
```json
{
  "total_files": 13,
  "high_risk": 3,
  "medium_risk": 5,
  "low_risk": 5,
  "breaking_changes": [
    {
      "file": "CLAUDE.md",
      "risk": "high",
      "reason": "Orchestration logic changed",
      "impact": "All AI sessions affected"
    }
  ]
}
```

---

**Remember**: This is a safety tool. Be conservative - when in doubt, mark as high-risk.
