---
version: 1.0.0
last_updated: 2025-11-19
description: Show numbered list of actions taken in session (7-10 words each, max 25)
args: []
---

# Session Status Summary

Generate a concise numbered list of all significant actions taken during this conversation session.

## Purpose

Provide a quick scannable summary of work completed, perfect for handoffs, progress reviews, or session recaps.

## Instructions

1. **Review conversation history**: Analyze all tool calls, file operations, and decisions made

2. **Extract significant actions**: Include:
   - File reads, writes, edits
   - Git operations (commit, push, branch creation)
   - Directory/file creation
   - Code implementation
   - Design decisions
   - Research performed
   - Commands executed
   - Todo list updates

3. **Format requirements**:
   - Numbered list (1, 2, 3, etc.)
   - **7-10 words per line** (strict limit)
   - **Maximum 25 actions** (most recent/important)
   - Past tense, active voice
   - Start with action verb
   - Include file paths when relevant (abbreviated if needed)

4. **Action priority** (when limiting to 25):
   - Git operations (commits, pushes) - highest priority
   - File creation/modification - high priority
   - Design decisions - high priority
   - File reads - lower priority (only include if significant)
   - Todo updates - lowest priority

5. **Example format**:
   ```
   1. Read proto-068 README and reverse index implementation
   2. Created REVERSE_INDEX_V2_DESIGN.md with tree-sitter architecture
   3. Updated proto-068 README with Feature #10 description
   4. Added success criteria for v2 implementation phases
   5. Committed Enhanced Reverse Index v2 design changes
   6. Pushed changes to claude/add-search-index branch successfully
   ```

6. **Output format**:
   - Start with "## Actions Taken" header
   - Numbered list only (no additional commentary)
   - If >25 actions, include only most recent 25
   - End with count: "(X actions total)" if truncated

## Example Output

```markdown
## Actions Taken

1. Read proto-068 Claude Turbo features README file
2. Analyzed current regex-based reverse index implementation
3. Created REVERSE_INDEX_V2_DESIGN.md with comprehensive technical spec
4. Added tree-sitter + SQLite architecture design
5. Defined four implementation phases with deliverables
6. Updated proto-068 README with Feature #10
7. Added performance targets and success criteria
8. Updated Next Steps section with v2 priority
9. Marked Enhanced Reverse Index design as complete
10. Committed changes with detailed commit message
11. Pushed to claude/add-search-index-01AiMM8WC8oBppAiVL3c7XR3 branch

(11 actions total)
```

## Notes

- Focus on **what was done**, not what was discussed
- Omit meta-actions (e.g., "loaded documentation", "searched for files")
- Keep descriptions concrete and specific
- Use standard abbreviations (e.g., "proto-068" not "prototype 068")
