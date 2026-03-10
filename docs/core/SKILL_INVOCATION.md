## ⚡ SKILL INVOCATION & RLHF TRACKING

**Purpose:** Immediate detection and invocation of skills via slash commands and sentiment analysis.

**Last Updated:** 2026-01-16

---

## 1.0 DETECTION PRIORITY

**Skills have HIGHEST priority in intent detection.**

### Detection Order
```
┌─────────────────────────────────────┐
│ 1. Slash Command Detection          │  HIGHEST PRIORITY
│    Pattern: /[a-z-]+                │  → Immediate Skill invocation
├─────────────────────────────────────┤
│ 2. RLHF Sentiment Detection         │  HIGH PRIORITY
│    Patterns: WTF/nice/error/fail    │  → Track then respond
├─────────────────────────────────────┤
│ 3. Standard Intent Classification   │  NORMAL PRIORITY
│    Category, scale, approval, etc.  │  → Follow INTENT_DETECTION.md
└─────────────────────────────────────┘
```

**Rule:** Check for skills BEFORE analyzing task complexity, scale, or approval needs.

---

## 2.0 SLASH COMMAND DETECTION

### Pattern Recognition
**Regex:** `^/[a-z][a-z0-9-]*`

**Valid Examples:**
- `/error`
- `/commit`
- `/push`
- `/track-errors`
- `/new-idea`
- `/diagram`

**Invalid (not slash commands):**
- `error` (no slash)
- `/Error` (uppercase not allowed)
- `/ error` (space after slash)
- `/123` (must start with letter)

### Invocation Process

**Step 1: Detect Pattern**
```python
import re

def detect_slash_command(message: str) -> str | None:
    """Returns skill name if slash command detected."""
    match = re.match(r'^/([a-z][a-z0-9-]*)', message.strip())
    return match.group(1) if match else None
```

**Step 2: Invoke Immediately**
```
User message: "/error broken build"
               ^^^^^ Detected

Action: Skill("error", args="broken build")
        ↓
        Skill tool handles execution
        ↓
        Return to conversation flow
```

**Step 3: NO Explanation**
```
❌ Wrong:
User: "/error"
AI: "The /error command tracks errors. Let me invoke it for you..."

✅ Correct:
User: "/error"
AI: [Invokes Skill("error") immediately, skill output appears]
```

### Slash Command Aliases

Some skills have multiple entry points:

| Primary | Aliases | Invokes |
|---------|---------|---------|
| `/track-errors` | `/error`, `/fail`, `/punish` | `track-errors` |
| `/nice` | `/reward`, `/good` | `nice` |
| `/memo` | `/remember`, `/keep`, `/save` | `memo` |
| `/auto-merge` | `/m`, `/mcb`, `/merge-claude-branches` | `auto-merge` |

**Alias Resolution:**
```
User: "/fail" → Skill("track-errors")
User: "/punish" → Skill("track-errors")
User: "/reward" → Skill("nice")
User: "/m" → Skill("auto-merge")
User: "/keep" → Skill("memo")
```

---

## 3.0 RLHF SENTIMENT DETECTION

### Negative Sentiment (Punishment Signals)

**Trigger Keywords:**
```
High Confidence (always trigger):
- "WTF", "wtf", "what the fuck"
- "that was wrong", "that's wrong", "you're wrong"
- "that didn't work", "that failed"

Medium Confidence (context-dependent):
- "error" (when referring to AI's action, not discussing errors)
- "fail", "failed" (when expressing frustration)
- "broken", "doesn't work"
- "no", "nope", "wrong" (after AI completes action)

Low Confidence (ask for clarification):
- "hmm", "uh", "not sure"
- "maybe", "I think"
```

**Context Analysis:**
```python
def is_negative_feedback(message: str, previous_action: str) -> bool:
    """Determine if message is negative feedback about previous AI action."""

    # High confidence keywords
    if any(kw in message.lower() for kw in ["wtf", "that was wrong", "that's wrong"]):
        return True

    # Medium confidence - check if referring to AI's recent action
    if any(kw in message.lower() for kw in ["error", "fail", "broken", "doesn't work"]):
        # Check if previous_action was recent (last 2 messages)
        if previous_action and message_is_feedback_context(message):
            return True

    return False
```

**Examples:**

```
✅ Triggers Error Tracking:
User: "WTF that S3 upload didn't work"
→ Skill("track-errors")
→ Then: "Let me help fix the S3 upload issue."

User: "That was wrong - you used pip instead of uv"
→ Skill("track-errors")
→ Then: "You're right. Let me fix it using uv."

User: [AI just created file] "That failed"
→ Skill("track-errors")
→ Then: "What went wrong? Let me investigate."

❌ Does NOT trigger (discussing, not feedback):
User: "How do I handle errors in Python?"
→ Standard intent detection (Question)

User: "Create error handling for the API"
→ Standard intent detection (Task)
```

**Action After Detection:**
```
1. Invoke Skill("track-errors")
   ↓
2. Skill logs error to data/rlhf/signals/punishments/
   ↓
3. Continue conversation to address the issue
   ↓
4. Fix the problem or clarify confusion
```

### Positive Sentiment (Reward Signals)

**Trigger Keywords:**
```
High Confidence:
- "nice", "nice work", "nice job"
- "great", "great work", "great job"
- "perfect", "excellent", "awesome"
- "well done", "good job"
- "thank you", "thanks" (after AI completes work)

Medium Confidence:
- "good", "looks good", "that works"
- "yes" (after asking for confirmation)
- "exactly", "right", "correct"

Low Confidence (optional tracking):
- "ok", "okay", "sure"
- "yep", "yup", "yeah"
```

**Context Analysis:**
```python
def is_positive_feedback(message: str, previous_action: str) -> bool:
    """Determine if message is positive feedback about previous AI action."""

    # High confidence keywords
    if any(kw in message.lower() for kw in [
        "nice", "great", "perfect", "excellent", "awesome", "well done", "good job"
    ]):
        return True

    # "thanks" or "thank you" after completing work
    if any(kw in message.lower() for kw in ["thank you", "thanks"]):
        if previous_action and not is_question(message):
            return True

    return False
```

**Examples:**

```
✅ Triggers Reward Tracking:
User: "Nice job on that diagram"
→ Skill("nice")
→ Then: "What's next?"

User: "Perfect, that's exactly what I needed"
→ Skill("nice")
→ Then: Continue conversation

User: [AI completes task] "Thanks!"
→ Skill("nice")
→ Then: "Happy to help. What else?"

❌ Does NOT trigger (neutral/transactional):
User: "Can you help with this?" "Thanks"
→ No reward tracking (asking for help)

User: "Okay" [simple acknowledgment]
→ No reward tracking (neutral)
```

**Action After Detection:**
```
1. Invoke Skill("nice")
   ↓
2. Skill logs reward to data/rlhf/signals/rewards/
   ↓
3. Continue conversation naturally
   ↓
4. Ask "What's next?" or similar
```

---

## 4.0 IMPLEMENTATION CHECKLIST

### For Every User Message

**Step 1: Check Slash Commands**
```
Does message start with /[a-z-]+?
├─ YES → Invoke Skill immediately
└─ NO → Continue to Step 2
```

**Step 2: Check Negative Sentiment**
```
Does message contain WTF/error/fail/wrong in feedback context?
├─ YES → Invoke Skill("track-errors"), then address issue
└─ NO → Continue to Step 3
```

**Step 3: Check Positive Sentiment**
```
Does message contain nice/great/perfect/thanks in feedback context?
├─ YES → Invoke Skill("nice"), then continue
└─ NO → Continue to Step 4
```

**Step 4: Standard Intent Detection**
```
Follow INTENT_DETECTION.md for:
- Category classification
- Scale assessment
- Approval routing
```

---

## 5.0 EDGE CASES & DISAMBIGUATION

### Edge Case 1: Slash Command + Additional Context
```
User: "/error the build is broken and tests are failing"

Action:
1. Invoke Skill("error")
2. Skill uses "the build is broken and tests are failing" as context
3. Return skill output
```

### Edge Case 2: Sentiment + Question
```
User: "WTF is going on with the database connection?"

Ambiguous: Is this feedback (error) or question?

Resolution:
- If AI just made database changes → Skill("track-errors")
- If AI hasn't touched database → Treat as question

Default: When in doubt, treat as question
```

### Edge Case 3: Multiple Sentiments
```
User: "That was wrong but thanks for trying"

Contains: Negative ("wrong") + Positive ("thanks")

Resolution:
- Negative takes precedence (error is more important)
- Invoke Skill("track-errors")
- Address the issue
```

### Edge Case 4: Sarcasm Detection
```
User: "Great job breaking the build"

Apparent positive ("Great job") but context is negative

Resolution:
- Check for negative context words: "breaking", "broken", "failed"
- If present → Treat as negative sentiment
- Invoke Skill("track-errors")
```

---

## 6.0 SKILL INVOCATION EXAMPLES

### Example 1: Direct Slash Command
```
User: "/commit"

AI Process:
1. Detect: /commit
2. Invoke: Skill("commit")
3. [Skill runs git workflow]
4. Return: Skill output displayed to user

No explanation, no confirmation - just execute.
```

### Example 2: Slash Command with Args
```
User: "/push updated the API docs"

AI Process:
1. Detect: /push
2. Extract args: "updated the API docs"
3. Invoke: Skill("push", args="updated the API docs")
4. [Skill commits with message and pushes]
5. Return: Success message
```

### Example 3: Negative Sentiment
```
User: "WTF that didn't generate the right files"

AI Process:
1. Detect: "WTF" → negative sentiment
2. Invoke: Skill("track-errors")
3. [Skill logs error]
4. Respond: "Let me check what went wrong with the file generation."
5. Investigate and fix
```

### Example 4: Positive Sentiment
```
User: "Nice work on that refactor"

AI Process:
1. Detect: "Nice work" → positive sentiment
2. Invoke: Skill("nice")
3. [Skill logs reward]
4. Respond: "Thanks! What should we work on next?"
```

### Example 5: No Skill Trigger
```
User: "Create a new API endpoint for user authentication"

AI Process:
1. Check slash command: No
2. Check negative sentiment: No
3. Check positive sentiment: No
4. Standard intent detection: Task (Implementation)
5. Follow INTENT_DETECTION.md workflow
```

---

## 7.0 DEBUGGING SKILL INVOCATION

### Common Problems

**Problem 1: Skill Not Invoked**
```
Symptom: User typed /error but AI explained instead of invoking

Root Cause: Detection failed or invocation step skipped

Fix: Check detection order (see Section 1.0)
```

**Problem 2: Wrong Skill Invoked**
```
Symptom: User typed /push but AI invoked different skill

Root Cause: Alias mapping incorrect

Fix: Check aliases table (Section 2.0)
```

**Problem 3: Sentiment Not Detected**
```
Symptom: User said "WTF" but no error tracking occurred

Root Cause: Context analysis failed or sentiment detection disabled

Fix: Review confidence levels (Section 3.0)
```

### Validation Tests

**Test Slash Commands:**
```
Input: "/error"
Expected: Skill("error") invoked
Verify: Error log created in data/rlhf/signals/punishments/

Input: "/commit"
Expected: Skill("commit") invoked
Verify: Git commit created

Input: "/push"
Expected: Skill("push") invoked
Verify: Git push executed
```

**Test Negative Sentiment:**
```
Input: "WTF that was wrong"
Expected: Skill("track-errors") invoked
Verify: Error log created

Input: "That failed"
Expected: Skill("track-errors") invoked (if after AI action)
Verify: Error log created
```

**Test Positive Sentiment:**
```
Input: "Nice job"
Expected: Skill("nice") invoked
Verify: Reward log created

Input: "Thanks!"
Expected: Skill("nice") invoked (if after AI action)
Verify: Reward log created
```

---

## 8.0 RELATED DOCUMENTATION

**Core Rules:**
- `hmode/docs/core/CRITICAL_RULES.md` - Rule 19: Immediate Skill Invocation

**Intent Detection:**
- `hmode/docs/core/INTENT_DETECTION.md` - Full intent classification system

**RLHF System:**
- `shared/config.yaml` - RLHF paths configuration
- `data/rlhf/signals/rewards/` - Positive feedback logs
- `data/rlhf/signals/punishments/` - Negative feedback logs

**Skill Definitions:**
- `hmode/commands/error.md` - Error tracking alias
- `hmode/commands/track-errors.md` - Full error tracking workflow
- `hmode/commands/nice.md` - Reward tracking workflow

---

## 9.0 VERSION HISTORY

**v1.0.0** (2026-01-16):
- Initial skill invocation guide
- Slash command detection patterns
- RLHF sentiment detection (negative/positive)
- Edge cases and disambiguation rules
- Added to CRITICAL_RULES.md as Rule 19

---

**Status:** Active and Enforced
**Authority:** Critical Rule 19
**Modification:** Requires explicit human approval
