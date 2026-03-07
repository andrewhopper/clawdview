# Asset Feedback Hooks - Design Document

## Problem

When Claude creates or modifies an asset (HTML page, React component, SVG, etc.),
the user previews it in ClawdView but has no structured way to send feedback
back into the Claude conversation. Today the user must alt-tab, type feedback
manually, and hope Claude understands which asset they're referring to.

## Goal

Let the user review an asset in ClawdView's browser UI, submit feedback
(approve, request changes, add comments), and have that feedback automatically
injected into the Claude Code conversation so Claude can act on it.

---

## Architecture Overview

```
┌─────────────────────┐       ┌──────────────────────┐
│   Claude Code CLI   │       │   ClawdView Browser  │
│                     │       │                      │
│  PostToolUse hook   │◄──────│  Feedback UI panel   │
│  (Write/Edit)       │       │  [Approve] [Revise]  │
│       │             │       │  [Comment textarea]  │
│       ▼             │       │         │            │
│  Opens browser /    │       │         ▼            │
│  notifies user      │       │  POST /api/feedback  │
│                     │       │         │            │
│  Stop hook ─────────│───────│◄────────┘            │
│  (reads feedback)   │       │  Stores feedback in  │
│       │             │       │  .clawdview/feedback/ │
│       ▼             │       └──────────────────────┘
│  Injects feedback   │
│  into conversation  │
└─────────────────────┘
```

---

## Hook Chain

### Hook 1: `PostToolUse` — Asset Change Notification

**When:** After Claude writes or edits a previewable file (`.html`, `.jsx`, `.svg`, etc.)

**What it does:**
1. Checks if the file extension is previewable by ClawdView
2. Writes a pending feedback request to `.clawdview/feedback/pending.json`
3. Optionally opens the browser or sends a desktop notification

**Config** (`.claude/settings.json`):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/post-asset-change.sh"
          }
        ]
      }
    ]
  }
}
```

**Script** (`.claude/hooks/post-asset-change.sh`):
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')
EXTENSION="${FILE_PATH##*.}"

PREVIEWABLE="html jsx svg md json css py"
if ! echo "$PREVIEWABLE" | grep -qw "$EXTENSION"; then
  exit 0  # Not a previewable asset, skip
fi

FEEDBACK_DIR=".clawdview/feedback"
mkdir -p "$FEEDBACK_DIR"

# Write pending feedback request
cat > "$FEEDBACK_DIR/pending.json" <<EOF
{
  "file": "$FILE_PATH",
  "timestamp": "$(date -Iseconds)",
  "status": "pending",
  "feedback": null
}
EOF

# Notify user (desktop notification)
if command -v notify-send &>/dev/null; then
  notify-send "ClawdView" "Asset updated: $FILE_PATH — review in browser"
fi

exit 0
```

---

### Hook 2: `Stop` — Pause for Feedback Before Finishing

**When:** Claude finishes its response (the `Stop` event fires)

**What it does:**
1. Checks if there's a pending feedback request in `.clawdview/feedback/pending.json`
2. If pending, blocks Claude from finishing (`exit 2`) and tells Claude to wait
3. Polls/waits for the user to submit feedback via ClawdView UI
4. Once feedback arrives, reads it and exits with code 0, injecting the feedback as context

**Config**:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/wait-for-feedback.sh",
            "timeout": 300000
          }
        ]
      }
    ]
  }
}
```

**Script** (`.claude/hooks/wait-for-feedback.sh`):
```bash
#!/bin/bash
FEEDBACK_DIR=".clawdview/feedback"
PENDING="$FEEDBACK_DIR/pending.json"

# No pending feedback request — let Claude finish normally
if [ ! -f "$PENDING" ]; then
  exit 0
fi

STATUS=$(jq -r '.status' "$PENDING" 2>/dev/null)
if [ "$STATUS" != "pending" ]; then
  exit 0
fi

# Check if feedback has been submitted (via ClawdView UI)
RESPONSE="$FEEDBACK_DIR/response.json"
if [ ! -f "$RESPONSE" ]; then
  # Block: tell Claude to wait for user feedback
  echo "Waiting for user feedback on asset: $(jq -r '.file' "$PENDING"). User is reviewing in ClawdView." >&2
  exit 2
fi

# Feedback received — inject it into conversation
FILE=$(jq -r '.file' "$PENDING")
VERDICT=$(jq -r '.verdict' "$RESPONSE")
COMMENT=$(jq -r '.comment' "$RESPONSE")

# Clean up
rm -f "$PENDING" "$RESPONSE"

# Output feedback as context for Claude
cat <<EOF
Asset feedback received for: $FILE
Verdict: $VERDICT
User comment: $COMMENT

Please address the user's feedback on this asset.
EOF

exit 0
```

---

### Alternative: Hook 2b — `UserPromptSubmit` for Feedback Injection

Instead of (or in addition to) the Stop hook, use `UserPromptSubmit` to
automatically augment the user's next message with any pending feedback:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/inject-feedback.sh"
          }
        ]
      }
    ]
  }
}
```

```bash
#!/bin/bash
FEEDBACK_DIR=".clawdview/feedback"
RESPONSE="$FEEDBACK_DIR/response.json"

if [ ! -f "$RESPONSE" ]; then
  exit 0
fi

FILE=$(jq -r '.file' "$RESPONSE")
VERDICT=$(jq -r '.verdict' "$RESPONSE")
COMMENT=$(jq -r '.comment' "$RESPONSE")

rm -f "$RESPONSE" "$FEEDBACK_DIR/pending.json"

# Inject as additional context alongside user's prompt
cat <<EOF
[ClawdView Feedback] Asset: $FILE | Verdict: $VERDICT
User says: $COMMENT
EOF

exit 0
```

This approach is simpler — it doesn't block Claude. The user reviews the asset
at their own pace, and the next time they send a message, the feedback is
automatically included.

---

## ClawdView Server Changes

### New API Endpoint: `POST /api/feedback`

Add a feedback submission route to the ClawdView server:

```js
// src/routes/feedback-routes.js
const express = require('express');
const fs = require('fs');
const path = require('path');

function createFeedbackRoutes(watchDir) {
  const router = express.Router();

  router.post('/feedback', express.json(), (req, res) => {
    const { file, verdict, comment } = req.body;

    if (!file || !verdict) {
      return res.status(400).json({ error: 'file and verdict are required' });
    }

    const feedbackDir = path.join(watchDir, '.clawdview', 'feedback');
    fs.mkdirSync(feedbackDir, { recursive: true });

    const response = {
      file,
      verdict,       // "approve" | "revise" | "reject"
      comment: comment || '',
      timestamp: new Date().toISOString()
    };

    fs.writeFileSync(
      path.join(feedbackDir, 'response.json'),
      JSON.stringify(response, null, 2)
    );

    res.json({ success: true, message: 'Feedback submitted' });
  });

  // GET current pending feedback request
  router.get('/feedback/pending', (req, res) => {
    const pendingPath = path.join(watchDir, '.clawdview', 'feedback', 'pending.json');
    if (fs.existsSync(pendingPath)) {
      const data = JSON.parse(fs.readFileSync(pendingPath, 'utf8'));
      res.json(data);
    } else {
      res.json({ status: 'none' });
    }
  });

  return router;
}

module.exports = createFeedbackRoutes;
```

### New UI: Feedback Panel

Add a feedback panel to the ClawdView browser UI that appears when a pending
feedback request exists:

```html
<!-- Feedback bar (appears at bottom of preview) -->
<div id="feedback-panel" class="hidden">
  <div class="feedback-header">
    Claude is waiting for your feedback on: <span id="feedback-file"></span>
  </div>
  <div class="feedback-actions">
    <button id="fb-approve" class="fb-btn fb-approve">Approve</button>
    <button id="fb-revise" class="fb-btn fb-revise">Request Changes</button>
    <button id="fb-reject" class="fb-btn fb-reject">Reject</button>
  </div>
  <textarea id="fb-comment" placeholder="Optional: describe what to change..."></textarea>
  <button id="fb-submit" class="fb-btn fb-submit">Send Feedback</button>
</div>
```

The client-side JS polls `GET /api/feedback/pending` and shows/hides the panel.
On submit, it POSTs to `/api/feedback` with the verdict and comment.

---

## Feedback Data Flow (Step by Step)

```
1. User: "Create a landing page"
2. Claude: Writes artifact-landing.html
3. PostToolUse hook fires:
   - Detects .html extension → previewable
   - Writes .clawdview/feedback/pending.json
   - Desktop notification: "Asset updated, review in ClawdView"
4. ClawdView auto-reloads the preview (existing file watcher)
5. ClawdView polls /api/feedback/pending → shows feedback panel
6. User reviews the page in the browser
7. User clicks "Request Changes" and types "Make the hero section bigger"
8. ClawdView POSTs to /api/feedback → writes response.json
9. User types next message in Claude (or Stop hook fires):
   - Hook reads response.json
   - Injects: "[ClawdView Feedback] Verdict: revise | Make the hero section bigger"
10. Claude reads the injected feedback and modifies the file
11. Cycle repeats
```

---

## Configuration Summary

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/post-asset-change.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/inject-feedback.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `.claude/hooks/post-asset-change.sh` | Create | Detect asset changes, write pending feedback |
| `.claude/hooks/inject-feedback.sh` | Create | Read feedback, inject into conversation |
| `.claude/hooks/wait-for-feedback.sh` | Create | (Optional) Block Stop until feedback received |
| `quickview-tool/src/routes/feedback-routes.js` | Create | API endpoint for feedback submission |
| `quickview-tool/server.js` | Modify | Register feedback routes |
| `quickview-tool/public/index.html` | Modify | Add feedback panel HTML |
| `quickview-tool/public/app.js` | Modify | Add feedback polling + submission logic |
| `quickview-tool/public/style.css` | Modify | Style feedback panel |
| `.clawdview/feedback/` | Created at runtime | Stores pending/response JSON |
| `.gitignore` | Modify | Ignore `.clawdview/feedback/` |

---

## Design Decisions

### Why file-based communication (not WebSocket)?
Hook scripts are short-lived shell processes — they can't maintain WebSocket
connections. File-based JSON is the simplest reliable bridge between the
ClawdView server and Claude Code hooks.

### Why `UserPromptSubmit` over `Stop`?
The `Stop` + block approach (`exit 2`) forces Claude to wait, which can feel
jarring. `UserPromptSubmit` is non-blocking — the user reviews at their pace and
feedback is attached to their next message naturally. Both options are provided;
teams can choose based on workflow preference.

### Why not a `prompt`-type hook?
A prompt hook uses an LLM to evaluate conditions. Here, the decision is binary
(is there feedback? what does it say?) — a simple shell script is faster and
cheaper.

### Feedback file cleanup
Response files are deleted after being read by the hook to prevent stale
feedback from being re-injected. The pending file is also cleaned up.
