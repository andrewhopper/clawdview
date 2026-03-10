# Guardrail Supervisor Pattern

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Supervisor Pattern                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐         IPC          ┌──────────────────┐
│   Supervisor    │◄──────────────────►  │   Main AI        │
│   (background)  │  Unix Socket/Pipe    │   Process        │
└─────────────────┘                      └──────────────────┘
      │
      ├─ Watches File System
      │  ├─ prototypes/
      │  └─ project-management/ideas/
      │
      ├─ Detects Violations
      │  ├─ S3 publish missing (MEDIUM → remind AI)
      │  ├─ Shared models not used (HIGH → notify user)
      │  ├─ URL format (LOW → auto-fix)
      │  └─ Tech not approved (HIGH → notify user)
      │
      └─ Sends Reminders via IPC
         └─ Main AI reads on each turn
```

## How It Works

### 1. Start Supervisor (Background)

```bash
# Install dependencies
pip install watchdog pyyaml

# Start as daemon
python3 .guardrails/ai-steering/supervisor.py daemon

# Or run in foreground (for debugging)
python3 .guardrails/ai-steering/supervisor.py start
```

### 2. Supervisor Monitors Files

When files are created/modified:
```
User creates: prototypes/proto-cat-site/index.html
     ↓
Supervisor detects file creation
     ↓
Checks: Is file publishable? (.html → yes)
     ↓
Has S3 evidence? (No .s3-skip, no bookmark)
     ↓
Severity: MEDIUM (remind AI, don't notify user)
     ↓
Queues reminder in IPC message queue
```

### 3. AI Reads Reminders

On each AI turn, read pending reminders:

```bash
# AI context injection hook
python3 .guardrails/ai-steering/supervisor.py read
```

**Output:**
```
🤖 ACTIVE GUARDRAIL REMINDERS:

1. [MEDIUM] reminder
   ⚠️ File 'index.html' is publishable but not published to S3.
   Prompt user: 'Publish index.html to S3? [1] Public [2] Temp [3] Private [4] Skip'
```

### 4. AI Addresses Reminders

AI sees reminder and acts:
```
AI: "I've created the cat website at prototypes/proto-cat-site/index.html.

     Would you like to publish it to S3?
       [1] Public (permanent URL)
       [2] Temporary (7 days)
       [3] Private (internal only)
       [4] Skip publishing"
```

## Severity-Based Actions

### LOW → Auto-Fix Silently
- **Example:** URL format (plain S3 URL → markdown)
- **Action:** Supervisor fixes automatically, no notification
- **IPC:** No message sent (handled in-process)

### MEDIUM → Remind AI
- **Example:** S3 publishing missing
- **Action:** Queue reminder for AI to address
- **IPC:** Send "reminder" message
- **User Impact:** None (AI handles it)

### HIGH → Notify User
- **Example:** Shared model not used, unapproved tech
- **Action:** Send notification to user immediately
- **IPC:** Send "violation" message with severity=high
- **User Impact:** Sees notification, can choose to fix or ignore

### CRITICAL → Block
- **Example:** Security violations, breaking changes
- **Action:** Block until resolved
- **IPC:** Send "violation" message with severity=critical
- **User Impact:** Cannot proceed until fixed

## IPC Protocol

### Message Format

```json
{
  "type": "reminder",
  "severity": "medium",
  "payload": {
    "rule": "s3_publish_missing",
    "file": "prototypes/proto-cat-site/index.html",
    "message": "⚠️ File 'index.html' is publishable but not published to S3..."
  },
  "timestamp": "2025-11-24T10:30:00"
}
```

### Client Usage

```python
from supervisor import IPCClient

client = IPCClient(Path(".guardrails/.supervisor.sock"))
reminders = client.get_reminders()

for reminder in reminders:
    if reminder['severity'] == 'medium':
        # Inject into AI context
        inject_reminder(reminder['payload']['message'])
    elif reminder['severity'] == 'high':
        # Show to user
        print(reminder['payload']['message'])
```

## Integration with AI Workflow

### Option 1: Hook-Based (Recommended)

Create `.claude/hooks/pre-ai-response.sh`:

```bash
#!/bin/bash
# Run before AI generates response

# Read pending reminders
REMINDERS=$(python3 .guardrails/ai-steering/supervisor.py read)

if [ -n "$REMINDERS" ]; then
    # Inject into AI context
    echo "$REMINDERS"
fi
```

### Option 2: Wrapper Script

```python
# ai_wrapper.py
def generate_ai_response(user_message):
    # Get reminders from supervisor
    reminders = get_reminders_from_supervisor()

    # Inject into AI context
    context = f"{user_message}\n\n{reminders}"

    # Generate response
    response = ai_model(context)

    return response
```

### Option 3: Polling (Simple)

```bash
# Every AI turn
python3 .guardrails/ai-steering/supervisor.py read >> ai_context.txt
```

## Examples

### Example 1: Create HTML File

```bash
# User creates file
$ echo "<html>Cat Site</html>" > prototypes/proto-cat-site/index.html

# Supervisor detects (background)
[Supervisor] File created: index.html
[Supervisor] Publishable extension detected
[Supervisor] No S3 evidence found
[Supervisor] Reminder queued: s3_publish_missing

# AI next turn
$ python3 .guardrails/ai-steering/supervisor.py read

🤖 ACTIVE GUARDRAIL REMINDERS:
1. [MEDIUM] reminder
   ⚠️ File 'index.html' is publishable but not published to S3.
   Prompt user: 'Publish index.html to S3? [1] Public [2] Temp [3] Private [4] Skip'

# AI responds
AI: "Would you like to publish the cat website to S3?
     [1] Public [2] Temp [3] Private [4] Skip"
```

### Example 2: Shared Model Violation

```bash
# User creates file with local type
$ cat > Cat.ts <<EOF
interface Cat {
  name: string;
}
EOF

# Supervisor detects (background)
[Supervisor] File created: Cat.ts
[Supervisor] Local type 'Cat' exists in shared/semantic/domains/pet
[Supervisor] Severity: HIGH
[Supervisor] Notification sent to user

# User sees immediately
🚨 Type 'Cat' defined locally but exists in shared/semantic/domains/pet/.
   Use shared model: import { Cat } from '@shared/semantic/domains/pet'

# Supervisor also queued reminder for AI
$ python3 .guardrails/ai-steering/supervisor.py read

🤖 ACTIVE GUARDRAIL REMINDERS:
1. [HIGH] violation
   🚨 Type 'Cat' defined locally but exists in shared/semantic/domains/pet/.
   Use shared model.
```

## Commands

### Start/Stop

```bash
# Start supervisor (foreground)
python3 .guardrails/ai-steering/supervisor.py start

# Start as daemon (background)
python3 .guardrails/ai-steering/supervisor.py daemon

# Stop supervisor
python3 .guardrails/ai-steering/supervisor.py stop

# Check status
python3 .guardrails/ai-steering/supervisor.py status
```

### Read Reminders

```bash
# Read all pending reminders (clears queue)
python3 .guardrails/ai-steering/supervisor.py read

# Check status
python3 .guardrails/ai-steering/supervisor.py status
```

## Configuration

Edit `supervisor.py` to configure:

```python
# Watch directories
watch_dirs = [
    REPO_ROOT / "prototypes",
    REPO_ROOT / "project-management" / "ideas",
]

# Publishable extensions
PUBLISHABLE_EXTENSIONS = {".html", ".pdf", ".svg", ".zip", ".mp3", ".mp4"}
```

## Monitoring

### Logs

```bash
# View supervisor logs
tail -f .guardrails/.supervisor.log

# Example output
[2025-11-24 10:30:00] Starting Guardrail Supervisor...
[2025-11-24 10:30:00] IPC server started on .guardrails/.supervisor.sock
[2025-11-24 10:30:01] Watching: prototypes
[2025-11-24 10:30:01] Watching: project-management/ideas
[2025-11-24 10:30:15] S3 publish reminder for: index.html
[2025-11-24 10:30:20] Reminder queued: File 'index.html' is publishable...
```

### Status

```bash
$ python3 .guardrails/ai-steering/supervisor.py status

Supervisor running (PID 12345)
Socket: .guardrails/.supervisor.sock
Log: .guardrails/.supervisor.log
```

## Troubleshooting

### Supervisor Not Starting

```bash
# Check if already running
python3 .guardrails/ai-steering/supervisor.py status

# Check logs
cat .guardrails/.supervisor.log

# Remove stale PID
rm .guardrails/.supervisor.pid
```

### IPC Not Working

```bash
# Check socket exists
ls -la .guardrails/.supervisor.sock

# Test IPC client
python3 -c "
from supervisor import IPCClient
from pathlib import Path
client = IPCClient(Path('.guardrails/.supervisor.sock'))
print(client.get_status())
"
```

### No Reminders Generated

```bash
# Check supervisor is running
python3 .guardrails/ai-steering/supervisor.py status

# Check logs for file events
tail -f .guardrails/.supervisor.log

# Manually test violation detection
python3 .guardrails/ai-steering/smart_autofix.py check <file>
```

## Benefits

1. **Non-Intrusive**: Runs in background, doesn't block AI
2. **Real-Time**: Detects violations immediately as files change
3. **Severity-Based**: Only notifies user for severe issues
4. **Efficient**: IPC is fast, minimal overhead
5. **Decoupled**: Supervisor independent of main AI process
6. **Scalable**: Can add more watchers, validators easily

## Next Steps

1. **Install dependencies:**
   ```bash
   pip install -r .guardrails/ai-steering/requirements.txt
   ```

2. **Start supervisor:**
   ```bash
   python3 .guardrails/ai-steering/supervisor.py daemon
   ```

3. **Integrate with AI workflow:**
   - Add hook to read reminders before AI response
   - Or poll periodically: `supervisor.py read`

4. **Monitor:**
   ```bash
   tail -f .guardrails/.supervisor.log
   ```

5. **Test:**
   ```bash
   # Create a publishable file
   echo "<html>Test</html>" > test.html

   # Check reminders
   python3 .guardrails/ai-steering/supervisor.py read
   ```
