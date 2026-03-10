# Response Format Validation Guide

**File UUID:** b4c8d9e2-5f7a-4d8b-9c3e-6f8a9b2c4d7e
**Created:** 2026-02-02
**Purpose:** Enforce communication standards from CLAUDE.md Section 3.4

## 1.0 Overview

The `response_format_validator.py` script enforces the rule:

> **ALL choices presented to users MUST be numbered [1], [2], [3], etc.**

This validator detects when AI responses contain choice indicators (e.g., "Would you like to...") but fail to provide properly numbered options.

## 2.0 Architecture

### 2.1 Current Limitation

**Claude Code's hook system** (frontgate.py) validates **tool calls** (Write, Edit, etc.) but NOT text responses.

```
┌─────────────────────────────────────────────────────────┐
│  Current Hook Coverage                                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PreToolUse  ──> Phase checker ✅                       │
│  PostToolUse ──> Design validator ✅                    │
│                                                         │
│  ❌ NO HOOK FOR AI TEXT RESPONSES                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Integration Options

**Option A: Manual Validation**
```bash
# Copy AI response to clipboard, then:
pbpaste | uv run python .guardrails/ai-steering/response_format_validator.py check
```

**Option B: Post-Conversation Hook** (Future Enhancement)
```python
# If Claude Code adds PostResponseGeneration event:
if hook_event == "PostResponseGeneration":
    result = subprocess.run(
        ["uv", "run", "python", str(RESPONSE_VALIDATOR), "check"],
        input=response_text,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stdout)  # Show warning
        # NOTE: Cannot block (response already sent)
```

**Option C: User Feedback Loop** (Current Best Practice)
```bash
# User catches violation and uses /error command
/error you didn't give me a numbered list

# This trains the AI via RLHF signal
# Logged for future model improvements
```

## 3.0 Usage Examples

### 3.1 Valid Response (Pass)

**Input:**
```
I found three deployment strategies. Which would you prefer?

[1] AWS Amplify - Fastest for SPAs
[2] CloudFront + S3 - More control
[3] ECS Fargate - Full container support
```

**Validation:**
```bash
$ echo "$response" | uv run python response_format_validator.py check
$ echo $?
0  # Pass
```

### 3.2 Invalid Response (Fail)

**Input:**
```
I found three deployment strategies. Which would you prefer?

- AWS Amplify for quick deploys
- CloudFront + S3 for static sites
- ECS Fargate for containers
```

**Validation:**
```bash
$ echo "$response" | uv run python response_format_validator.py check

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  COMMUNICATION STANDARD VIOLATION

Rule: Section 3.4 "Numbered Options"
ALL choices presented to users MUST be numbered.

Detected: Response contains choice indicators but no [1], [2], [3] format.

Last paragraph:
- AWS Amplify for quick deploys
- CloudFront + S3 for static sites
...

Required format:
[1] First option - brief description
[2] Second option - brief description
[3] Third option - brief description

Reference: CLAUDE.md Section 3.4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ echo $?
1  # Fail
```

### 3.3 No Choice Needed (Pass)

**Input:**
```
I've completed the deployment successfully. The site is now live at https://example.com.
```

**Validation:**
```bash
$ echo "$response" | uv run python response_format_validator.py check
$ echo $?
0  # Pass (no choice indicators detected)
```

## 4.0 Detection Patterns

### 4.1 Choice Indicators (Trigger Validation)

The validator looks for these patterns:
- "would you like to"
- "would you like me to"
- "should I"
- "do you want"
- "which one" / "which option"
- "what would you prefer"
- "how would you like"
- "select one"
- "choose"
- "options:"
- "alternatives:"
- "you can:"

### 4.2 False Positives (Excluded)

These patterns are NOT considered choice situations:
- "would you like to see" (yes/no question, not multiple choice)
- "would you like more details"
- "should I continue"
- "should I proceed"

### 4.3 Numbered Option Pattern

Valid format: `[N] Option text`
- Must start with `[number]`
- Must be followed by space
- Must have at least 2 options
- Numbers should be sequential (1, 2, 3...)

## 5.0 Integration with Frontgate Hook

### 5.1 Current Hook Flow

```python
# .claude/hooks/frontgate.py (current)

def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    hook_event = input_data.get("hook_event_name", "")

    # PreToolUse: Block file writes if phase < 8
    if hook_event == "PreToolUse" and tool_name in FILE_TOOLS:
        file_path = extract_file_path_from_args(tool_args)
        allowed, message = check_phase_gate(file_path)

        if not allowed:
            print(message)
            sys.exit(1)  # BLOCK

    # PostToolUse: Validate design system compliance
    if hook_event == "PostToolUse" and tool_name in FILE_TOOLS:
        handle_file_tool(tool_result, tool_args)
```

### 5.2 Proposed Enhancement (If Supported)

```python
# .claude/hooks/frontgate.py (future enhancement)

RESPONSE_VALIDATOR = GUARDRAILS_DIR / "response_format_validator.py"

def check_response_format(response_text: str) -> tuple[bool, str]:
    """
    Check if response follows numbered list rule.

    Returns: (is_valid, warning_message)
    """
    try:
        result = subprocess.run(
            ["uv", "run", "python", str(RESPONSE_VALIDATOR), "check"],
            input=response_text,
            capture_output=True,
            text=True,
            timeout=3,
            cwd=REPO_ROOT
        )

        if result.returncode != 0:
            # Violation detected - return warning
            return False, result.stdout + result.stderr

        return True, ""

    except Exception as e:
        log(f"Response validation error: {e}")
        return True, ""  # Allow on error


def main():
    input_data = json.load(sys.stdin)
    hook_event = input_data.get("hook_event_name", "")

    # ... existing PreToolUse and PostToolUse handlers ...

    # NEW: PostResponseGeneration event (if supported)
    if hook_event == "PostResponseGeneration":
        response_text = input_data.get("response_text", "")

        is_valid, warning = check_response_format(response_text)

        if not is_valid:
            # NOTE: Cannot block (response already generated)
            # Show warning to user instead
            print_boxed(warning)
            log("WARNED: Response format violation")

        sys.exit(0)  # Never block responses
```

## 6.0 Makefile Targets

Add these convenience targets to project Makefiles:

```makefile
# Validate last AI response (from clipboard)
.PHONY: validate-response
validate-response:
	@pbpaste | uv run python $(REPO_ROOT)/.guardrails/ai-steering/response_format_validator.py check

# Watch for violations during development
.PHONY: watch-responses
watch-responses:
	@echo "📋 Paste AI responses below (Ctrl+D to check):"
	@uv run python $(REPO_ROOT)/.guardrails/ai-steering/response_format_validator.py check

# Show validation stats
.PHONY: response-stats
response-stats:
	@tail -20 $(REPO_ROOT)/.guardrails/.response_validator-*.log
```

## 7.0 Testing the Validator

### 7.1 Test Cases

```bash
# Test 1: Valid numbered options
echo "Would you like to: [1] Deploy [2] Test [3] Skip" | \
  uv run python response_format_validator.py check

# Test 2: Invalid (bullets instead of numbers)
echo "Would you like to: - Deploy - Test - Skip" | \
  uv run python response_format_validator.py check

# Test 3: No choice needed (should pass)
echo "Deployment complete. Check the logs." | \
  uv run python response_format_validator.py check

# Test 4: False positive (yes/no question, should pass)
echo "Would you like to see the full output?" | \
  uv run python response_format_validator.py check
```

### 7.2 Expected Results

```
Test 1: Exit 0 (Pass)
Test 2: Exit 1 (Fail) + Warning message
Test 3: Exit 0 (Pass)
Test 4: Exit 0 (Pass)
```

## 8.0 Limitations & Future Work

### 8.1 Current Limitations

1. **No automatic enforcement** - Requires manual validation or user feedback
2. **Cannot block responses** - Only warns after generation
3. **Pattern matching** - May have false positives/negatives
4. **No context awareness** - Doesn't know if choices are implied vs explicit

### 8.2 Future Enhancements

**A. LLM-based validation**
```python
# Use lightweight model to detect if response requires numbered options
from anthropic import Anthropic

def validate_with_llm(response_text: str) -> bool:
    """Ask Claude Haiku if response needs numbered options."""
    client = Anthropic()
    result = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"Does this response present multiple choices to the user? Answer only yes or no.\n\n{response_text}"
        }]
    )
    return "yes" in result.content[0].text.lower()
```

**B. Semantic rule integration**
- Add to `.guardrails/ai-steering/generated/communication-rules.md`
- Load at Claude Code startup as MUST constraint
- AI internalizes rule without needing post-validation

**C. Hook enhancement request**
- Request `PostResponseGeneration` hook event from Claude Code team
- Enable real-time validation before response is shown to user

**D. IDE integration**
- VSCode/Cursor extension that validates responses in real-time
- Highlights violations in AI response pane
- One-click "Regenerate with proper format" button

## 9.0 Related Documentation

- **CLAUDE.md Section 3.4** - Numbered Options rule definition
- **CLAUDE.md Section 3.2** - One Question at a Time rule
- **frontgate.py** - Current hook implementation for tool validation
- **phase_checker.py** - Example of blocking validation
- **response_format_validator.py** - Implementation code

## 10.0 Quick Reference

**Validate response manually:**
```bash
pbpaste | uv run python .guardrails/ai-steering/response_format_validator.py check
```

**Report violation to AI:**
```bash
/error you didn't give me a numbered list
```

**Valid format:**
```
[1] First option - description
[2] Second option - description
[3] Third option - description
```

**Invalid formats:**
```
- Bullet point option          ❌
* Asterisk option              ❌
1. Numbered list (not brackets) ❌
Option A / Option B            ❌
```
