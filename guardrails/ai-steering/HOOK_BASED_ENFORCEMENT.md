# Hook-Based Guardrail Enforcement

## How It Actually Works with Claude Code

Claude Code doesn't support IPC or background process injection. Instead, we use **hooks** that run synchronously and append reminders to tool results.

## Architecture

```
User Request
     ↓
Claude processes
     ↓
Tool executed (Write/Edit)
     ↓
📍 tool-result.sh hook runs ← WE HOOK HERE
     ↓
Validation runs synchronously
     ↓
Reminders appended to tool output
     ↓
Claude sees tool result + reminders ← CLAUDE SEES THIS
     ↓
Claude addresses reminders in response
```

## Available Hooks

Claude Code supports these hooks:

1. **`session-start.sh`** ✅ Currently used for tool setup
2. **`tool-result.sh`** ⭐ NEW - Validate after tool execution
3. **`user-prompt-submit.sh`** (if available) - Run before AI processes message

## Implementation

### `tool-result.sh` Hook

Located: `.claude/hooks/tool-result.sh`

**What it does:**
1. Runs after EVERY tool execution (Write, Edit, NotebookEdit)
2. Extracts file path from tool result
3. Runs validation synchronously
4. Appends reminders to tool output
5. Claude sees reminders as part of tool result

**Example Flow:**

```bash
# User asks: "Create a cat website"

# AI uses Write tool
Write(file_path="index.html", content="<html>...")

# Tool executes
→ File created: index.html

# Hook runs immediately
→ tool-result.sh detects file creation
→ Validates: index.html is publishable
→ No S3 evidence found
→ Appends reminder to tool output

# Claude sees this output:
"""
File created successfully at: prototypes/proto-cat-site/index.html

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 GUARDRAIL REMINDERS:
📋 AI Reminders (to be injected into context):
  ⚠️ REMINDER: File 'index.html' is publishable but not published to S3.
     Prompt user: 'Publish index.html to S3? [1] Public [2] Temp [3] Private [4] Skip'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# Claude responds
"I've created the cat website. Would you like to publish it to S3?
 [1] Public [2] Temp [3] Private [4] Skip"
```

## How to Enable

### 1. Ensure Hook is Executable

```bash
chmod +x .claude/hooks/tool-result.sh
```

### 2. Test Manually

```bash
# Create a test file
echo "<html>Test</html>" > test.html

# Simulate hook execution
.claude/hooks/tool-result.sh Write "" "File created successfully at: test.html"

# Should output reminders if violations detected
```

### 3. Hook Runs Automatically

Once installed, the hook runs automatically after every file operation.

## Real-World Example

### Before Hook:

```
User: "Create a cat lovers website"

AI: [Creates index.html]

AI: "Done! I've created the website at prototypes/proto-cat-site/index.html"
```

**Problem:** No S3 publishing offered, user has to remember to ask.

### After Hook:

```
User: "Create a cat lovers website"

AI: [Creates index.html]

[Hook runs, appends reminder to tool output]

AI sees:
  "File created: index.html
   🤖 GUARDRAIL REMINDER: File 'index.html' is publishable..."

AI: "I've created the website. Would you like to publish it to S3?
     [1] Public [2] Temp [3] Private [4] Skip"
```

**Result:** AI automatically prompts for S3 publishing without user having to ask!

## Benefits

✅ **Works with Claude Code** - Uses supported hooks, not IPC
✅ **Synchronous** - No race conditions or timing issues
✅ **Reliable** - Runs every time a file is created/modified
✅ **Simple** - No background processes, no IPC complexity
✅ **Integrated** - Reminders appear as part of tool output

## Comparison: IPC vs Hook-Based

| Feature | IPC Supervisor | Hook-Based |
|---------|---------------|------------|
| Works with Claude Code | ❌ No | ✅ Yes |
| Background process | ✅ Yes | ❌ No |
| Real-time detection | ✅ Yes | ✅ Yes |
| Complexity | High | Low |
| Reliability | Medium | High |
| Maintenance | Complex | Simple |

## Current Status

✅ **Hook installed:** `.claude/hooks/tool-result.sh`
✅ **Validator ready:** `.guardrails/ai-steering/smart_autofix.py`
✅ **Ready to use:** Automatically runs on file operations

## Next Steps

The system is **ready to use** now. Every time you create/modify a file:

1. Hook runs automatically
2. Validates file
3. Appends reminders to tool output
4. Claude sees reminders and addresses them

No IPC, no background processes - just hooks that actually work with Claude Code!

## Testing

```bash
# Create a publishable file
echo "<html>Cat Site</html>" > test-site.html

# Check if validation runs
# (Should see reminder about S3 publishing in next AI response)
```

## Monitoring

```bash
# Check hook is executable
ls -la .claude/hooks/tool-result.sh

# Test hook manually
.claude/hooks/tool-result.sh Write "" "File created: test.html"

# View validation logs
cat .guardrails/.supervisor.log
```
