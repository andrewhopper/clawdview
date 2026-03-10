#!/bin/bash
# File UUID: a8f9c2d4-3e5b-4c7f-9a1d-2b3c4d5e6f7a
# Skill: new-session-with-context
# Description: Capture current context to markdown, validate with user, then start fresh session
# Usage: /new-session-with-context [output-file]

set -euo pipefail

# Get session info
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Default output location
DEFAULT_OUTPUT="$PROJECT_DIR/.claude/context-snapshots/context-${TIMESTAMP}.md"
OUTPUT_FILE="${1:-$DEFAULT_OUTPUT}"

# Ensure directory exists
mkdir -p "$(dirname "$OUTPUT_FILE")"

cat <<PROMPT
You are being asked to capture the current conversation context before starting a fresh session.

**Task:**
1. Generate a comprehensive markdown file at: \`$OUTPUT_FILE\`
2. Include the following sections:
   - **Session Metadata:** Session ID, timestamp, working directory, git branch/status
   - **Conversation Summary:** Brief overview of what was discussed/accomplished (5-10 bullet points)
   - **Current State:** What files were created/modified, what decisions were made
   - **Open Questions:** Any unresolved issues or pending decisions
   - **Next Steps:** Recommended actions for the next session
   - **Context for Resume:** Key information needed to continue the work
3. After generating the file, present it to me for review with:
   - File path
   - Quick summary (3-5 lines)
   - Ask: "Approve context snapshot? [Y/n/edit]"
4. If approved, inform me that I should start a new session (you cannot clear the current one)
5. If "edit" is selected, ask what changes to make

**Current Working Directory:** $PROJECT_DIR
**Session ID:** $SESSION_ID
**Timestamp:** $TIMESTAMP

**Important Guidelines:**
- Keep summary concise but comprehensive
- Focus on decisions made and work completed
- Include enough context for seamless resume
- Don't include full conversation logs (summaries only)
- Capture any important URLs, file paths, or references
- Note any running processes or pending operations

Begin by generating the context snapshot markdown file now.
PROMPT
