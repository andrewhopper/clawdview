---
version: 1.0.0
last_updated: 2025-11-16
description: Capture interaction feedback to improve CLAUDE.md
args:
  - name: feedback_text
    description: Your feedback on the interaction (required)
    required: true
---

# Feedback Capture

Capture feedback on AI plan presentations and confirmations to improve CLAUDE.md over time.

## Purpose

Track what works and what doesn't in plan confirmations, intent detection, and SDLC workflows. Feedback is stored in JSONL format for LLM-powered analysis to suggest specific CLAUDE.md improvements.

## Usage

```bash
# During plan confirmation
AI: "...any changes? y/n"
User: /feedback "looks good, but naming convention could be clearer"

# After any interaction
/feedback "confirmation protocol feels repetitive, consider simplifying"
/feedback "great job on the detailed plan, exactly what I needed"
/feedback "intent detection missed that this was a chore, not a task"
```

## Instructions

1. **Capture context**: Review the last 3-5 message pairs from the conversation to understand what the user is giving feedback about

2. **Structure the feedback entry**:
   ```json
   {
     "timestamp": "2025-11-16T14:30:00Z",
     "feedback": "user's feedback text",
     "context": {
       "interaction_type": "plan_confirmation|intent_detection|phase_transition|other",
       "phase": "current SDLC phase if applicable",
       "ai_messages": ["last 2-3 AI messages as context"],
       "user_messages": ["last 2-3 user messages as context"]
     },
     "metadata": {
       "prototype": "current prototype if applicable",
       "command": "slash command if applicable"
     }
   }
   ```

3. **Append to JSONL file**:
   - File: `project-management/feedback/interaction-feedback.jsonl`
   - Create directory if it doesn't exist
   - Append as single line (one JSON object per line)

4. **Confirm to user**:
   ```
   ✅ Feedback captured!

   📝 Saved to: project-management/feedback/interaction-feedback.jsonl
   💡 Run `python shared/scripts/analyze-feedback.py` to generate CLAUDE.md improvement suggestions
   ```

## Feedback Entry Schema

```json
{
  "timestamp": "ISO 8601 timestamp",
  "feedback": "User's feedback text",
  "context": {
    "interaction_type": "plan_confirmation | intent_detection | phase_transition | confirmation_protocol | sdlc_workflow | other",
    "phase": "SDLC phase or null",
    "ai_messages": ["Array of recent AI messages"],
    "user_messages": ["Array of recent user messages"]
  },
  "metadata": {
    "prototype": "Prototype name or null",
    "command": "Slash command or null",
    "tags": ["Array of relevant tags"]
  }
}
```

## Interaction Types

- **plan_confirmation**: Feedback on "any changes? y/n" confirmations
- **intent_detection**: Feedback on how AI classified the request
- **phase_transition**: Feedback on SDLC phase transitions
- **confirmation_protocol**: Feedback on Air Traffic Control confirmation pattern
- **sdlc_workflow**: Feedback on 9-phase SDLC process
- **other**: Other interactions

## Example Feedback Entries

**Plan confirmation feedback:**
```json
{
  "timestamp": "2025-11-16T14:30:00Z",
  "feedback": "Plan was good but step 3 implementation details were vague",
  "context": {
    "interaction_type": "plan_confirmation",
    "phase": "IMPLEMENTATION",
    "ai_messages": [
      "Ok, here's my plan:\n1. Create component\n2. Add tests\n3. Implement logic\n...",
      "Btw, will use React hooks pattern..."
    ],
    "user_messages": [
      "Add feedback feature",
      "/feedback \"step 3 vague\""
    ]
  },
  "metadata": {
    "prototype": "proto-015-claude-power-tools",
    "command": null,
    "tags": ["plan_detail", "implementation"]
  }
}
```

**Intent detection feedback:**
```json
{
  "timestamp": "2025-11-16T15:00:00Z",
  "feedback": "Should have been classified as chore not task - was simple file rename",
  "context": {
    "interaction_type": "intent_detection",
    "phase": null,
    "ai_messages": [
      "Category: Task | Scale: 1 file | Time: 5 min | Approval: Summary"
    ],
    "user_messages": [
      "Rename proto-014 folder to include xip tag"
    ]
  },
  "metadata": {
    "prototype": null,
    "command": null,
    "tags": ["intent_detection", "chore_vs_task"]
  }
}
```

## Analysis Workflow

1. **Capture**: Use `/feedback` throughout development sessions
2. **Accumulate**: Feedback stored in JSONL (append-only)
3. **Analyze**: Run `python shared/scripts/analyze-feedback.py` periodically
4. **Review**: Claude analyzes patterns, suggests CLAUDE.md changes
5. **Improve**: Update CLAUDE.md with accepted suggestions
6. **Archive**: Mark incorporated feedback or archive old entries

## File Location

- **Feedback file**: `project-management/feedback/interaction-feedback.jsonl`
- **Analysis script**: `shared/scripts/analyze-feedback.py`
- **Suggestions output**: `project-management/feedback/claude-md-suggestions-{date}.md`

## Implementation Notes

1. **Context capture**: Include enough AI/user messages to understand what's being evaluated
2. **Privacy**: JSONL files are gitignored (personal feedback, not committed)
3. **Format**: One JSON object per line (valid JSONL)
4. **Timestamps**: Use ISO 8601 format with timezone
5. **Null values**: Use `null` for optional fields, not empty strings

## Remember

- Feedback helps improve CLAUDE.md for everyone
- Be specific: "step 3 vague" > "plan unclear"
- Both positive and negative feedback valuable
- Context matters: capture enough to understand the situation

---

**Goal**: Continuous improvement of CLAUDE.md through real-world usage feedback
