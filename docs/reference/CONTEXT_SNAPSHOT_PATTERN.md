<!-- File UUID: d5e6f7a8-4b3c-4d5e-9f1a-2b3c4d5e6f7h -->
# Context Snapshot Pattern

## Overview

The **Context Snapshot Pattern** allows you to capture the current conversation context into a markdown file before starting a fresh session. This prevents losing important context while managing token budgets effectively.

## When to Use

- Token usage approaches 110k (out of 200k budget)
- Long-running sessions with multiple phases completed
- Before context switch to different project
- End of work session with intent to resume later
- After major milestone completion

## Usage

### Manual Trigger

```bash
/new-session-with-context [optional-output-file]
```

If no output file specified, defaults to:
```
.claude/context-snapshots/context-{YYYYMMDD-HHMMSS}.md
```

### Automatic Suggestion

A hook monitors token usage and suggests the snapshot at 110k tokens:

```
┌─────────────────────────────────────────────────────────────┐
│ 🔔 TOKEN USAGE ALERT                                        │
├─────────────────────────────────────────────────────────────┤
│  Current tokens: 110,000 / 200,000                          │
│  💡 Consider capturing context: /new-session-with-context   │
└─────────────────────────────────────────────────────────────┘
```

## Workflow

1. **Trigger:** User invokes `/new-session-with-context` or sees auto-suggestion
2. **Capture:** Claude generates markdown file with context summary
3. **Review:** User reviews and approves/edits the snapshot
4. **Save:** Context saved to `.claude/context-snapshots/`
5. **Resume:** User starts new session, references snapshot as needed

## Snapshot Structure

```markdown
# Context Snapshot - {YYYY-MM-DD HH:MM:SS}

## Session Metadata
- Session ID: {session-id}
- Timestamp: {timestamp}
- Working Directory: {path}
- Git Branch: {branch}
- Git Status: {status}

## Conversation Summary
- {bullet point summary of discussion}
- {key decisions made}
- {accomplishments}

## Current State
### Files Created/Modified
- {file paths with descriptions}

### Decisions Made
- {architectural choices}
- {technology selections}
- {approach decisions}

## Open Questions
- {unresolved issues}
- {pending decisions}
- {blockers}

## Next Steps
1. {recommended actions}
2. {priorities for next session}
3. {dependencies to resolve}

## Context for Resume
- {key information needed to continue}
- {important URLs, references}
- {running processes or pending ops}
```

## Integration with Hooks

### Context Monitoring Hooks

#### PreCompact Hook (Primary)

**File:** `.claude/hooks/precompact-suggest-snapshot.sh`
**Type:** `PreCompact` (matcher: `auto`)
**Trigger:** Automatic compaction when context window is full

The hook:
- Fires when Claude Code's context window is full
- Only triggers for auto-compact (not manual `/compact`)
- Most reliable detection method
- Provides warning before context is summarized/lost
- Never blocks compaction (always exits 0)

#### UserPromptSubmit Hook (Backup)

**File:** `.claude/hooks/suggest-context-snapshot.sh`
**Type:** `UserPromptSubmit`
**Trigger:** Conversation length >= 50 turns

The hook:
- Reads transcript file to count conversation turns
- Estimates context usage based on message count
- Suggests snapshot at ~50 turns (approximately 100-120k tokens)
- Only suggests once per session (uses temp file marker)
- Never blocks (always exits 0)

### Hook Configuration

Add to `.claude/settings.json` (if not auto-configured):

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "auto",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/precompact-suggest-snapshot.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/suggest-context-snapshot.sh"
          }
        ]
      }
    ]
  }
}
```

**Why Two Hooks?**

- **PreCompact**: Most reliable, fires exactly when context is full
- **UserPromptSubmit**: Provides early warning before hitting limit

## Best Practices

### When to Snapshot

- **Before phase transitions:** Capture context at end of Phase 6 before Phase 7
- **After major decisions:** Document architecture/tech choices
- **End of session:** Preserve work context for next time
- **Before delegation:** Capture context before spawning agents
- **Token budget:** Don't wait until 200k - snapshot at 110k

### What to Include

- **Decisions:** Technology, architecture, approach
- **Progress:** What was completed, what remains
- **Context:** Information needed to resume seamlessly
- **References:** URLs, file paths, external resources
- **Dependencies:** What's blocking or needed next

### What to Exclude

- **Full conversation logs:** Summaries only
- **Verbose debugging output:** Key findings only
- **Redundant information:** Focus on essentials
- **Sensitive data:** No credentials or PII

## Resuming from Snapshot

### In New Session

1. Start fresh Claude Code session
2. Reference snapshot file:
   ```
   Load context from .claude/context-snapshots/context-20260224-1530.md
   ```
3. Claude reads snapshot and resumes with context
4. Continue work seamlessly

### Snapshot Management

- Keep last 10 snapshots per project
- Archive older snapshots to `archive/` subdirectory
- Name snapshots descriptively if needed:
  ```
  context-20260224-phase6-complete.md
  context-20260224-pre-deployment.md
  ```

## Context Budget Strategy

```
┌─────────────────────────────────────────────────────────────┐
│ Context Window Management                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   0 turns ────────────────────────────────▶ Normal work    │
│                                                             │
│  30 turns ────────────────────────────────▶ Mid-session    │
│                                                             │
│  50 turns ──┬─────────────────────────────▶ 🔔 Early       │
│             │                                warning        │
│             │                               (UserPrompt    │
│             │                                hook)          │
│             │                                              │
│             └─────────────────────────────▶ Consider       │
│                                             capturing      │
│                                             context        │
│                                                             │
│ ~80 turns ────────────────────────────────▶ High usage     │
│                                             (nearing limit)│
│                                                             │
│ ~100 turns ──┬────────────────────────────▶ ⚠️  Context    │
│              │                               FULL          │
│              │                               (PreCompact   │
│              │                                hook fires)  │
│              │                                              │
│              └────────────────────────────▶ Auto-compact   │
│                                             OR capture     │
│                                             context        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Note: Turn counts are approximate. Actual limits depend on:
- Message length (code blocks, long outputs)
- Tool use frequency (each tool call adds tokens)
- Context size (CLAUDE.md, file reads, hook output)
```

## Technical Implementation

### Skill File

**Location:** `hmode/skills/new-session-with-context.sh`
**Type:** Bash script with embedded prompt
**Execution:** Invoked via `/new-session-with-context`

The skill:
1. Creates output directory if needed
2. Sends prompt to Claude with template structure
3. Claude generates markdown file
4. User reviews and approves
5. Claude confirms snapshot saved, suggests new session

### Hook File

**Location:** `.claude/hooks/suggest-context-snapshot.sh`
**Type:** `UserPromptSubmit` hook
**Execution:** Runs before each user prompt

The hook:
1. Reads `CLAUDE_TOKENS_USED` from environment
2. Compares to threshold (110k)
3. If exceeded and not already suggested: Display alert
4. Creates temp marker to prevent repeat suggestions
5. Always exits 0 (never blocks)

## Troubleshooting

### Hook Not Triggering

**Problem:** No suggestion when context is full

**Solutions:**
1. **Check PreCompact hook is configured:**
   - Verify `.claude/settings.json` has `PreCompact` section
   - Matcher should be `"auto"` (not `"manual"`)

2. **Check UserPromptSubmit hook:**
   - Verify hook is configured in settings
   - Check transcript file exists and is readable
   - Ensure `jq` command is installed (for JSON parsing)

3. **Verify permissions:**
   ```bash
   chmod +x .claude/hooks/precompact-suggest-snapshot.sh
   chmod +x .claude/hooks/suggest-context-snapshot.sh
   ```

4. **Test hooks manually:**
   ```bash
   # Test PreCompact hook
   echo '{"trigger":"auto","session_id":"test"}' | .claude/hooks/precompact-suggest-snapshot.sh

   # Test UserPromptSubmit hook
   echo '{"transcript_path":"'$(pwd)'/transcript.jsonl"}' | .claude/hooks/suggest-context-snapshot.sh
   ```

5. **Check Claude Code version:**
   - PreCompact hook requires Claude Code 2.1+
   - Run `claude --version` to check

### Skill Not Found

**Problem:** `/new-session-with-context` not recognized

**Solutions:**
1. Verify skill file exists and has execute permissions
2. Check `hmode/skills/` directory is scanned
3. Try absolute path: `/full/path/to/hmode/skills/new-session-with-context.sh`
4. Restart Claude Code to reload skills

### Context File Not Created

**Problem:** Markdown file not generated

**Solutions:**
1. Check directory permissions for `.claude/context-snapshots/`
2. Verify Claude has write access
3. Try explicit output path: `/new-session-with-context /tmp/context.md`
4. Check for disk space issues

## Related Patterns

- **Session Management:** Starting/stopping sessions with context preservation
- **Token Budget Optimization:** Aggressive delegation to sub-agents
- **Work Session Patterns:** Beginning/ending work sessions
- **Phase Transitions:** Capturing context between SDLC phases

## Future Enhancements

- **Auto-snapshot on exit:** Capture context when Claude Code exits
- **Snapshot diff:** Compare snapshots to show progress between sessions
- **Smart resume:** Auto-load latest snapshot on session start
- **Compression:** Summarize older snapshots to save space
- **Search:** Full-text search across all snapshots

---

**Version:** 1.0.0
**Last Updated:** 2026-02-24
**Status:** Active
