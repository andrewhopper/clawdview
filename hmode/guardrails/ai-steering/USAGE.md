# Smart Auto-Fix Usage Guide

## Overview

The smart auto-fix system handles violations based on severity:

- **LOW**: Auto-fix silently (e.g., URL formatting)
- **MEDIUM**: Remind AI to handle it (e.g., S3 publishing prompts)
- **HIGH**: Notify user (e.g., unapproved dependencies, shared model violations)
- **CRITICAL**: Block until resolved

## Quick Start

### Check a File

```bash
python3 .guardrails/ai-steering/smart_autofix.py check path/to/file.html
```

**Output Examples:**

**Low Severity (Auto-Fixed):**
```
✅ Auto-fixed: S3 URL not in clickable markdown format in README.md
```

**Medium Severity (AI Reminder):**
```
📋 AI Reminders (to be injected into context):
  ⚠️ REMINDER: File 'cat-site.html' is publishable but not published to S3.
     Prompt user: 'Publish cat-site.html to S3? [1] Public [2] Temp [3] Private [4] Skip'
```

**High Severity (User Notification):**
```
🚨 Type 'Cat' defined locally but exists in shared/semantic/domains/pet/

Use shared model: import { Cat } from '@shared/semantic/domains/pet'
```

### Get AI Context Injection

Get all active reminders to inject into AI's context:

```bash
python3 .guardrails/ai-steering/smart_autofix.py context
```

**Output:**
```
🤖 ACTIVE GUARDRAIL REMINDERS:
  1. ⚠️ REMINDER: File 'index.html' is publishable but not published to S3.
     Prompt user: 'Publish index.html to S3? [1] Public [2] Temp [3] Private [4] Skip'
  2. ⚠️ REMINDER: File 'report.pdf' is publishable but not published to S3.
     Prompt user: 'Publish report.pdf to S3? [1] Public [2] Temp [3] Private [4] Skip'

Please address these reminders in your response.
```

### Clear Reminders

```bash
# Clear reminders for specific file
python3 .guardrails/ai-steering/smart_autofix.py clear path/to/file.html

# Clear all reminders
python3 .guardrails/ai-steering/smart_autofix.py clear
```

## Integration Workflow

### In Claude Code Session

**After AI creates/modifies files:**

```bash
# 1. Check the file
python3 .guardrails/ai-steering/smart_autofix.py check prototypes/proto-cat-site/index.html

# 2. If reminders generated, inject into AI context
CONTEXT=$(python3 .guardrails/ai-steering/smart_autofix.py context)

# 3. AI sees reminders and addresses them in next response
```

### Example Flow

```
User: "Create a cat lovers website"

AI: Creates index.html

[smart_autofix runs]
→ Detects: index.html is publishable
→ Severity: MEDIUM
→ Action: REMIND_AI
→ Adds reminder to .guardrails/.ai_reminders.json

[Next AI turn, context injected]
AI sees: "⚠️ REMINDER: File 'index.html' is publishable but not published to S3..."

AI responds: "I've created the cat website. Would you like to publish it to S3?
  [1] Public [2] Temp [3] Private [4] Skip"
```

## Severity Configuration

Edit `smart_autofix.py` to adjust severity levels:

```python
VIOLATION_RULES = {
    "s3_publish_missing": ViolationRule(
        severity=Severity.MEDIUM,    # Change to LOW, HIGH, or CRITICAL
        action=ActionType.REMIND_AI, # Change to AUTO_FIX, NOTIFY_USER, or BLOCK
    ),
}
```

## Violation Rules

### S3 Publishing Missing
- **Severity**: MEDIUM
- **Action**: REMIND_AI
- **Behavior**: AI gets reminder to prompt user for S3 publishing

### Shared Model Not Used
- **Severity**: HIGH
- **Action**: NOTIFY_USER
- **Behavior**: User sees notification about using shared models
- **Auto-fix**: Can generate import automatically

### URL Not Clickable
- **Severity**: LOW
- **Action**: AUTO_FIX
- **Behavior**: Silently converts plain URLs to markdown format

### Tech Not Approved
- **Severity**: HIGH
- **Action**: NOTIFY_USER
- **Behavior**: User sees notification about unapproved dependency

## AI Context Injection

Reminders are stored in `.guardrails/.ai_reminders.json`:

```json
[
  {
    "rule_id": "s3_publish_missing",
    "file": "prototypes/proto-cat-site/index.html",
    "reminder": "⚠️ REMINDER: File 'index.html' is publishable but not published to S3...",
    "timestamp": "2025-11-24T10:30:00"
  }
]
```

This file is read on each AI turn and injected into context.

## Hook Integration

### Option 1: After File Write (Recommended)

Create `.claude/hooks/post-file-write.sh`:

```bash
#!/bin/bash
FILE_PATH="$1"

python3 .guardrails/ai-steering/smart_autofix.py check "$FILE_PATH"
```

### Option 2: Before AI Response

Create `.claude/hooks/pre-ai-response.sh`:

```bash
#!/bin/bash

# Inject reminders into AI context
python3 .guardrails/ai-steering/smart_autofix.py context
```

## Examples

### Example 1: Create HTML File

```bash
$ echo "<html>Cat Site</html>" > cat-site.html

$ python3 .guardrails/ai-steering/smart_autofix.py check cat-site.html

📋 AI Reminders (to be injected into context):
  ⚠️ REMINDER: File 'cat-site.html' is publishable but not published to S3.
     Prompt user: 'Publish cat-site.html to S3? [1] Public [2] Temp [3] Private [4] Skip'
```

### Example 2: Local Type Definition

```bash
$ cat > Cat.ts <<EOF
interface Cat {
  name: string;
  age: number;
}
EOF

$ python3 .guardrails/ai-steering/smart_autofix.py check Cat.ts

🚨 Type 'Cat' defined locally but exists in shared/semantic/domains/pet/

Use shared model: import { Cat } from '@shared/semantic/domains/pet'

✅ Auto-fixed: Local type definition exists in shared domains in Cat.ts
```

### Example 3: Plain S3 URL

```bash
$ cat > README.md <<EOF
Download: https://bucket.s3.us-east-1.amazonaws.com/file.pdf
EOF

$ python3 .guardrails/ai-steering/smart_autofix.py check README.md

✅ Auto-fixed: S3 URL not in clickable markdown format in README.md

$ cat README.md
Download: [file.pdf](https://bucket.s3.us-east-1.amazonaws.com/file.pdf)
```

## Troubleshooting

### Reminders Not Clearing

```bash
# Check current reminders
python3 .guardrails/ai-steering/smart_autofix.py context

# Clear all
python3 .guardrails/ai-steering/smart_autofix.py clear
```

### Auto-Fix Not Working

Check file permissions and ensure script is executable:
```bash
chmod +x .guardrails/ai-steering/smart_autofix.py
```

### Domain Registry Not Found

Ensure registry exists:
```bash
ls shared/semantic/domains/registry.yaml
```

## Next Steps

1. **Test the system:**
   ```bash
   python3 .guardrails/ai-steering/smart_autofix.py check <file>
   ```

2. **Integrate with hooks** (when Claude Code supports them)

3. **Adjust severity levels** to match your preferences

4. **Monitor AI reminders:**
   ```bash
   python3 .guardrails/ai-steering/smart_autofix.py context
   ```
