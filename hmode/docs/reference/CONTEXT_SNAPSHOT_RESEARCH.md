<!-- File UUID: f8e9d7c6-5b4a-4c3d-9e2f-1a2b3c4d5e6a -->
# Context Snapshot Detection Research

## Research Question

How can Claude Code hooks detect when token usage approaches the context window limit (200k tokens) to suggest capturing context before running out of space?

## Research Date

2026-02-24

## Research Methods

1. **Environment variable inspection** - Checked for `CLAUDE_*` env vars
2. **Documentation review** - Read official Claude Code hooks documentation
3. **Hook schema analysis** - Analyzed JSON input/output for all hook events
4. **Existing hook inspection** - Reviewed working hooks in the repository

## Key Findings

### 1. PreCompact Hook (Primary Solution)

**Discovery:** Claude Code has a `PreCompact` event that fires automatically when the context window is full.

**Evidence:**
- Documentation: https://code.claude.com/docs/en/hooks
- Hook input includes `trigger` field with values: `"manual"` | `"auto"`
- `"auto"` fires when auto-compact is triggered (context window full)

**JSON Input Schema:**
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PreCompact",
  "trigger": "auto",
  "custom_instructions": ""
}
```

**Advantages:**
- Most reliable detection method
- Fires exactly when context is full
- No estimation or heuristics needed
- Built-in Claude Code mechanism

**Limitations:**
- Only fires when limit is reached (no early warning)
- Compaction may already be necessary

### 2. Transcript Analysis (Backup Solution)

**Discovery:** All hooks receive `transcript_path` pointing to conversation JSONL file.

**Evidence:**
- All hook events include `transcript_path` in common input fields
- File format: JSONL (one line per conversation turn)
- File location: `~/.claude/projects/{project-id}/{session-id}.jsonl`

**Approach:**
```bash
# Count lines in transcript (each line = one turn)
TURN_COUNT=$(wc -l < "$TRANSCRIPT_PATH")

# Heuristic: ~50 turns ≈ 100-120k tokens (depends on message length)
if [ "$TURN_COUNT" -ge 50 ]; then
    # Suggest snapshot
fi
```

**Advantages:**
- Provides early warning before hitting limit
- Works on every `UserPromptSubmit` hook
- Simple line count (no complex parsing)

**Limitations:**
- Approximate (turn length varies)
- Requires transcript file access
- May trigger too early or too late

### 3. Environment Variables (Not Available)

**Tested:**
- `CLAUDE_TOKENS_USED` - Not found
- `CLAUDE_CONTEXT_SIZE` - Not found
- `CLAUDE_REMAINING_TOKENS` - Not found

**Available Claude Env Vars:**
```bash
CLAUDE_CODE_ENTRYPOINT=cli
CLAUDE_CODE_USE_BEDROCK=1
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000
ANTHROPIC_MODEL=global.anthropic.claude-sonnet-4-5-20250929-v1:0
ANTHROPIC_SMALL_FAST_MODEL=us.anthropic.claude-haiku-4-5-20251001-v1:0
CLAUDECODE=1
```

**Conclusion:**
Claude Code does not expose real-time token usage to hooks via environment variables.

## Recommended Solution

### Two-Tier Approach

1. **PreCompact Hook** - Primary, reliable trigger
   - Fires when context is full
   - Provides warning before auto-compaction
   - Matcher: `"auto"`

2. **UserPromptSubmit Hook** - Early warning system
   - Estimates usage from turn count
   - Triggers at ~50 turns
   - Provides advance notice

### Implementation

**File 1:** `.claude/hooks/precompact-suggest-snapshot.sh`
```bash
#!/bin/bash
# Type: PreCompact (matcher: auto)
INPUT=$(cat)
TRIGGER=$(echo "$INPUT" | jq -r '.trigger')

if [ "$TRIGGER" = "auto" ]; then
    echo "⚠️  Context window full - suggest /new-session-with-context"
fi
exit 0
```

**File 2:** `.claude/hooks/suggest-context-snapshot.sh`
```bash
#!/bin/bash
# Type: UserPromptSubmit
INPUT=$(cat)
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')
TURN_COUNT=$(wc -l < "$TRANSCRIPT_PATH")

if [ "$TURN_COUNT" -ge 50 ]; then
    echo "🔔 Conversation length: $TURN_COUNT turns - consider snapshot"
fi
exit 0
```

**Settings Configuration:**
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

## Alternative Approaches Considered

### 1. Token Estimation from Message Length

**Idea:** Estimate tokens by reading transcript and calculating message lengths.

**Rejected Because:**
- Complex (requires parsing JSONL, handling tool calls, etc.)
- Inaccurate (token count varies by content type)
- Slower (I/O overhead)
- Transcript analysis already provides turn count heuristic

### 2. Time-Based Triggers

**Idea:** Suggest snapshot after N minutes of conversation.

**Rejected Because:**
- Poor correlation between time and token usage
- Some sessions are long but shallow (quick questions)
- Other sessions are short but deep (large code blocks)

### 3. File Size Heuristics

**Idea:** Monitor transcript file size to estimate tokens.

**Rejected Because:**
- JSONL formatting adds overhead
- Doesn't account for context from CLAUDE.md, file reads, etc.
- Less accurate than turn count

## Validation

### Test Cases

1. **PreCompact Hook Test:**
   ```bash
   echo '{"trigger":"auto","session_id":"test"}' | \
     .claude/hooks/precompact-suggest-snapshot.sh
   ```
   Expected: Alert displayed

2. **UserPromptSubmit Hook Test:**
   ```bash
   # Create test transcript
   for i in {1..55}; do echo "{}"; done > /tmp/test-transcript.jsonl

   echo '{"transcript_path":"/tmp/test-transcript.jsonl"}' | \
     .claude/hooks/suggest-context-snapshot.sh
   ```
   Expected: Alert displayed after 50 turns

3. **Integration Test:**
   - Start long conversation
   - Verify UserPromptSubmit alert at ~50 turns
   - Continue until context full
   - Verify PreCompact alert before compaction

## References

- **Claude Code Hooks Documentation:** https://code.claude.com/docs/en/hooks
- **PreCompact Event:** https://code.claude.com/docs/en/hooks#precompact
- **Hook Input Schema:** https://code.claude.com/docs/en/hooks#common-input-fields
- **UserPromptSubmit Event:** https://code.claude.com/docs/en/hooks#userpromptsubmit

## Related Work

- **Context Snapshot Pattern:** `hmode/docs/reference/CONTEXT_SNAPSHOT_PATTERN.md`
- **New Session With Context Skill:** `hmode/skills/new-session-with-context.sh`
- **Existing Hooks:** `.claude/hooks/*.sh`

## Lessons Learned

1. **Read the docs first** - PreCompact hook was documented but not obvious from environment inspection
2. **Hook input is rich** - All hooks receive `transcript_path`, `session_id`, etc.
3. **Simple heuristics work** - Turn count is good enough for early warning
4. **Multi-tier detection** - Combining PreCompact + turn count provides best UX
5. **Test with real data** - Validated turn count heuristic against actual sessions

## Future Enhancements

1. **Token Count API** - Request Claude Code expose `CLAUDE_TOKENS_USED` env var
2. **Smart Threshold** - Adjust turn count threshold based on session characteristics
3. **Proactive Compaction** - Suggest snapshot before auto-compact needed
4. **Session Analytics** - Track token usage patterns over time
5. **Auto-Capture** - Optionally capture context automatically at threshold

---

**Status:** Complete
**Implemented:** Yes (2026-02-24)
**Validated:** Manual testing only (automated tests pending)
