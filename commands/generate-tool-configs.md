---
description: Generate multi-tool config files (.cursorrules, .clinerules) from CLAUDE.md
tags:
  - automation
  - configuration
  - multi-tool
version: 1.0.0
---

# Generate Multi-Tool Configuration Files

Generate `.cursorrules` and `.clinerules` configuration files from the canonical `CLAUDE.md` source.

## Purpose

Enable multi-tool AI compatibility by creating tool-specific configuration files that maintain consistency with the main CLAUDE.md guidelines while being optimized for Cursor AI and Cline AI.

## What This Does

1. Reads `CLAUDE.md` (canonical source of truth)
2. Extracts critical rules and workflows
3. Generates condensed, tool-specific versions:
   - `.cursorrules` - Cursor AI editor configuration
   - `.clinerules` - Cline AI assistant configuration
4. Preserves core behavior while optimizing for each tool's format

## Key Sections Included

**Critical Rules:**
- 9-phase SDLC with NO CODE enforcement (phases 1-6)
- Guardrails protection (human approval required)
- Technology approval workflow
- Confirmation protocol (ATC-style)
- Test-Driven Development (TDD)

**Workflow Guidance:**
- Phase transition rules
- .project file checking
- Reference examples usage
- Intent detection & scale assessment
- Parallel execution patterns

**Standards:**
- Writing style (brevity, decimal outline, ASCII diagrams)
- Data grounding (no invention)
- Git rules (direct-to-main)
- Semantic versioning

## Execution

Read CLAUDE.md and generate two condensed configuration files:

1. **`.cursorrules`** (Cursor AI format)
   - Condensed from ~4000 lines to ~400 lines
   - Preserves all critical enforcement rules
   - Optimized for Cursor's context window
   - Includes error prevention checklist

2. **`.clinerules`** (Cline AI format)
   - Similar to .cursorrules
   - Adapted for Cline's interaction model
   - Focuses on command execution patterns

## Source of Truth

**Canonical:** `CLAUDE.md` - Full, comprehensive guidelines
**Generated:** `.cursorrules`, `.clinerules` - Condensed, tool-specific

**Update workflow:**
1. Modify `CLAUDE.md` as needed
2. Run `/generate-tool-configs` to regenerate tool configs
3. Tool configs stay in sync with canonical source

## Output

After generation, confirm:
- ✅ `.cursorrules` created/updated
- ✅ `.clinerules` created/updated
- ✅ Both files reference CLAUDE.md as source
- ✅ Critical rules preserved (9-phase SDLC, guardrails, TDD)

## Benefits

**For Users:**
- Choose AI tool freely (Cursor, Cline, Claude Code)
- Consistent behavior across all tools
- No vendor lock-in

**For Maintainers:**
- Single source of truth (CLAUDE.md)
- Automated synchronization
- Easy updates via regeneration

## Notes

- Tool configs are regenerated, not manually edited
- All changes should go to CLAUDE.md first
- Configs optimize for each tool's token limits
- Core enforcement rules NEVER compromised in condensation

---

## Implementation

Generate both configuration files now.
