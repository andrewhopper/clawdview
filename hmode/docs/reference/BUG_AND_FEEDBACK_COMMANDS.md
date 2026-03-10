# Bug and Feedback Tracking Commands

Track errors, capture improvements, and provide feedback using slash commands.

---

## Commands

| Command | Purpose |
|---------|---------|
| `/bug` | Quick error tracking (alias) |
| `/track-errors` | Full error logging with root cause |
| `/feedback` | Capture improvement suggestions |

---

## `/bug`

**File:** `hmode/commands/bug.md`

Quick alias for `/track-errors`. Use when you want to log an error.

**Usage:**
```bash
/bug                              # Track current error
/bug <UUID|ID> status=fixed       # Update error status
/bug <UUID|ID> note="Fixed it"    # Add note to error
```

---

## `/track-errors`

**File:** `hmode/commands/track-errors.md`

Full error tracking with root cause analysis and prevention strategies.

### What It Does

1. Analyzes conversation for errors/failures
2. Extracts root cause and context
3. Logs to text and YAML files
4. Proposes prevention strategies
5. Updates documentation

### Error Categories

| Category | Description |
|----------|-------------|
| `sdlc-violation` | Coded before Phase 8, skipped test design |
| `confirmation-protocol` | Skipped confirmation for complex tasks |
| `tech-standard` | Wrong tool (pip vs uv, avoided CDK) |
| `guardrails` | Modified protected files |
| `data-grounding` | Invented data/details |
| `parallel-execution` | Sequential when parallel possible |
| `git-workflow` | Created branches, used disallowed commands |
| `tool-selection` | Wrong tool for task |
| `domain-model` | Didn't check shared registry |
| `file-size` | Files over 500 lines |
| `testing` | Missing tests |
| `technical-error` | Runtime/build/logic error |
| `other` | Other issues |

### Output Files

Configured in `shared/config.yaml` under `error_tracking`:

```yaml
error_tracking:
  log_dir: logs
  error_log_text: logs/errors        # Human-readable
  error_log_yaml: logs/errors.yaml   # Structured YAML
```

### YAML Schema

```yaml
errors:
  - uuid: 550e8400-e29b-41d4-a716-446655440000
    id: ERR-20251126-0001
    date: "2025-11-26T10:30:00Z"
    error: "Brief description"
    error_type: "Classification"
    category:
      - sdlc-violation
      - confirmation-protocol
    context: |
      Detailed context
    root_cause: |
      Why it happened
    status: new              # new → fixed → verified
    notes: []
    artifact_urls: []
    prior_messages: []
    created_at: "2025-11-26T10:30:00Z"
    updated_at: "2025-11-26T10:30:00Z"
```

### Updating Errors

```bash
# Change status
/track-errors ERR-20251126-0001 status=fixed

# Add note
/track-errors ERR-20251126-0001 note="Resolved by adding validation"
```

---

## `/feedback`

**File:** `hmode/commands/feedback.md`

Capture interaction feedback to improve CLAUDE.md over time.

### Usage

```bash
/feedback "plan was good but step 3 vague"
/feedback "confirmation protocol feels repetitive"
/feedback "intent detection missed this was a chore"
```

### Interaction Types

- `plan_confirmation` - Feedback on "any changes? y/n"
- `intent_detection` - How AI classified the request
- `phase_transition` - SDLC phase transitions
- `confirmation_protocol` - Air Traffic Control pattern
- `sdlc_workflow` - 9-phase process
- `other` - Other interactions

### Output File

```
project-management/feedback/interaction-feedback.jsonl
```

One JSON object per line (JSONL format).

### JSONL Schema

```json
{
  "timestamp": "2025-11-26T10:30:00Z",
  "feedback": "User's feedback text",
  "context": {
    "interaction_type": "plan_confirmation",
    "phase": "IMPLEMENTATION",
    "ai_messages": ["Recent AI messages"],
    "user_messages": ["Recent user messages"]
  },
  "metadata": {
    "prototype": "proto-015",
    "command": null,
    "tags": ["plan_detail"]
  }
}
```

### Analysis Workflow

```
/feedback "observation"
    ↓
Stored in JSONL
    ↓
python shared/scripts/analyze-feedback.py
    ↓
Review: project-management/feedback/claude-md-suggestions-{date}.md
    ↓
Update CLAUDE.md
```

---

## File Locations Summary

| Purpose | Path |
|---------|------|
| Bug command | `hmode/commands/bug.md` |
| Track-errors command | `hmode/commands/track-errors.md` |
| Feedback command | `hmode/commands/feedback.md` |
| Error log (text) | `logs/errors` |
| Error log (YAML) | `logs/errors.yaml` |
| Feedback log | `project-management/feedback/interaction-feedback.jsonl` |
| Config | `shared/config.yaml` |

---

## Quick Reference

**Log an error:**
```bash
/bug
```

**Update error status:**
```bash
/bug ERR-20251126-0001 status=fixed
```

**Capture feedback:**
```bash
/feedback "your observation here"
```

**Analyze feedback:**
```bash
python shared/scripts/analyze-feedback.py
```

---

[END]
