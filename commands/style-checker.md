---
uuid: cmd-style-1y2z3a4b
version: 1.0.0
last_updated: 2025-11-10
description: Path to style guide (default: WRITING_STYLE_GUIDE.md or STYLE_GUIDE.md in repo root)
---

# Style Checker + Interactive Defect Workflow

Check if `{file_path}` follows your project's writing standards with an interactive fix workflow.

## Style Guide Detection

1. **If style_guide parameter provided**: Use specified file
2. **If not provided, check for**:
   - `WRITING_STYLE_GUIDE.md` in repo root
   - `STYLE_GUIDE.md` in repo root
   - `.claude/STYLE_GUIDE.md`
3. **If no style guide found**: Use general best practices (active voice, specificity, citations)

## Instructions

### Phase 1: Detect Issues

1. **Load style guide**: Read the style guide file to understand standards

2. **Read the document**: Use Read tool to load `{file_path}`

3. **Scan for violations**:
   - Active vs passive voice
   - Vague language (recently, many, several)
   - Missing citations
   - Style guide-specific rules
   - Terminology consistency
   - Metric quantification

4. **Present numbered defects with proposed changes**:

```markdown
# Style Defects: {file_path}

Style Guide: {path or "General best practices"}

Found {N} issues:

## Defects

**#1** [CRITICAL] Line 23: Missing citation
- Current: "The company recently raised significant funding"
- Proposed: "The company raised $50M Series B on May 15, 2024 [1]"
- Change: Added quantification + citation

**#2** [WARNING] Line 45: Passive voice
- Current: "A partnership was announced"
- Proposed: "Company X announced a partnership with Y on June 1, 2024 [2]"
- Change: Active voice + specificity

**#3** [SUGGESTION] Line 67: Vague language
- Current: "Large company"
- Proposed: "Company with 800 employees across 12 countries [3]"
- Change: Quantified scale

**#4** [WARNING] Line 89: Missing quantification
- Current: "recently launched"
- Proposed: "launched Q2 2024"
- Change: Added timeframe

---

## Summary
- 🔴 Critical: 1
- ⚠️ Warnings: 2
- 💡 Suggestions: 1
```

### Phase 2: User Decision

5. **Prompt user with DSL options**:

```
Review proposed changes. Choose action:

• accept all          - Apply all fixes as-is
• reject all          - Skip all fixes
• accept: 1,2,4       - Apply fixes #1, #2, #4
• reject: 3           - Skip fix #3 (apply rest)
• edit: 2,3           - Manually edit fixes #2, #3 before applying
• e: 1                - Shorthand for edit

Combine commands: "accept: 1,4  edit: 2,3"

What would you like to do?
```

6. **Wait for user response** - DO NOT proceed until user provides input

### Phase 3: Handle Edits (if requested)

7. **If user requests edits** (e.g., `edit: 2,3`):
   - Present each defect for manual editing
   - Show current and proposed side-by-side
   - Ask user to provide their custom fix
   - Update the fix list with user's version

Example interaction:
```
📝 Edit mode for defect #2:

Current:  "A partnership was announced"
Proposed: "Company X announced a partnership with Y on June 1, 2024 [2]"

Enter your preferred fix (or press Enter to keep proposed):
> Company X announced partnership with Y (June 2024) [2]

✅ Updated fix #2
```

8. **After edits complete**, re-prompt for final acceptance

### Phase 4: Apply Fixes

9. **Parse user DSL input**:
   - `accept all` → apply all fixes
   - `reject all` → exit without changes
   - `accept: 1,2,4` → apply only #1, #2, #4
   - `reject: 3` → apply all except #3
   - `edit: 2,3` → enter edit mode for #2, #3

10. **Apply accepted fixes**:
   - Use Edit tool to replace current text with fixed text (or user's custom version)
   - Track which defects were fixed
   - Report completion

11. **Show fix summary**:

```markdown
✅ Applied fixes: #1, #2, #4
⏭️  Skipped: #3

File updated: {file_path}

## Applied Changes:
  #1: Added citation and quantification (line 23)
  #2: Changed to active voice with specificity (line 45) [custom edit]
  #4: Added specific timeframe (line 89)

## Next Steps:
- Run /quality-control to validate all fixes
- Run /writing-quality for final style check
- Review [3] reference and ensure citation is complete
```

## Common Style Violations

### Active Voice
❌ "The feature was implemented by the team"
✅ "The team implemented the feature"

### Specificity
❌ "Recently launched"
✅ "Launched Q2 2024"

❌ "Large company"
✅ "800 employees across 12 countries"

❌ "Significant funding"
✅ "$50M Series B"

### Citations
❌ "The company raised funding"
✅ "The company raised $50M Series B on May 15, 2024 [1]"

### Vague Language
❌ "Many customers", "several partners", "growing rapidly"
✅ "500+ customers", "3 strategic partners", "150% YoY growth"

## Example Flow

**Original document** (example.md):
```
Our metrics show we're improving. Customer satisfaction has increased
recently and users are generally happy. We need to continue focusing on
delivering great experiences.
```

**Step 1: Defects presented**
```
# Style Defects: example.md

Style Guide: WRITING_STYLE_GUIDE.md

Found 4 issues:

**#1** [WARNING] Line 1: Vague improvement claim
- Current: "we're improving"
- Proposed: "increased from 78% to 85%"
- Change: Added quantification

**#2** [WARNING] Line 2: Missing specificity
- Current: "increased recently"
- Proposed: "increased Q1→Q2 2024"
- Change: Added specific timeframe

**#3** [WARNING] Line 2: Vague language
- Current: "generally happy"
- Proposed: "satisfaction score >80%"
- Change: Quantified satisfaction

**#4** [SUGGESTION] Line 3: Passive construction
- Current: "we need to continue focusing"
- Proposed: "we focus on"
- Change: More direct, active

---
What would you like to do?
```

**Step 2: User responds**
```
accept: 1,2  edit: 3  reject: 4
```

**Step 3: Edit mode for #3**
```
📝 Edit mode for defect #3:

Current:  "generally happy"
Proposed: "satisfaction score >80%"

Enter your preferred fix (or press Enter to keep proposed):
> satisfaction rating of 85%

✅ Updated fix #3
```

**Step 4: Fixes applied**
```
✅ Applied fixes:
  #1: "we're improving" → "increased from 78% to 85%"
  #2: "increased recently" → "increased Q1→Q2 2024"
  #3: "generally happy" → "satisfaction rating of 85%" [custom]
⏭️  Skipped: #4

File updated: example.md
```

## DSL Syntax Rules

**Supported commands:**
- `accept all` or `accept: all` → Apply all fixes as-is
- `reject all` or `reject: all` → Skip all, exit
- `accept: 1,2,3` → Apply only #1, #2, #3
- `reject: 2,4` → Apply all EXCEPT #2, #4
- `accept: 1-5` → Apply range #1 through #5
- `accept: 1,3-5,7` → Combine ranges and individual
- `edit: 2,3` or `e: 2,3` → Manually edit proposed fixes for #2, #3
- `accept: 1,4  edit: 2,3` → Combine commands (accept some, edit others)

**Case insensitive**: Accept, ACCEPT, accept all work

**Edit mode workflow:**
1. User requests `edit: 2,3`
2. System presents each defect's current/proposed text
3. User provides custom fix
4. System updates fix list
5. After all edits, optionally re-prompt for acceptance of remaining

## Style Guide Integration

### Default Checks (if no style guide)
- Active voice >80%
- All facts cited with [1], [2], etc.
- Specific language (no "recently", "many", "large")
- Paragraph length <6 sentences
- No jargon/buzzwords without definition

### Custom Style Guide Rules
If style guide exists, extract and enforce:
- Project-specific terminology
- Required sections/structure
- Citation format requirements
- Domain-specific conventions
- Metric formatting standards

## Workflow Summary

1. Load style guide (or use defaults)
2. Scan document → find issues with proposed fixes
3. Present numbered defects (show Current → Proposed for each)
4. Prompt user with DSL options
5. **WAIT** for user input
6. If user requests edits → enter edit mode
7. Present each requested defect for manual editing
8. Collect custom fixes from user
9. Parse DSL → determine which to fix (with custom fixes if provided)
10. Apply fixes using Edit tool
11. Report what was fixed/skipped
12. Suggest next steps (/quality-control, /writing-quality)

## Key Points

1. **Number all defects**: Each issue gets unique ID (#1, #2, etc.)
2. **Wait for user**: DO NOT auto-fix without user acceptance
3. **Parse DSL carefully**: Support all formats (accept all, accept: 1,2,3, reject: 2)
4. **Apply selectively**: Only fix accepted defects
5. **Line numbers**: Include line references for all defects
6. **Preserve meaning**: Don't change technical content, only style
7. **Interactive**: User controls what gets fixed and how

## Integration with Other Tools

**Before style-checker:**
- /writing-quality (identifies issues, no fixes)

**After style-checker:**
- /quality-control (validate all fixes applied correctly)
- /densify (if document is still verbose after fixes)

**Workflow:**
```
1. /writing-quality docs/file.md     → Identifies issues
2. /style-checker docs/file.md       → Interactive fix workflow
3. /quality-control docs/file.md     → Final validation
```

Be precise, interactive, and standards-focused.
