---
version: 1.0.0
last_updated: 2025-11-24
description: Send email via Resend API (recipient, subject, body)
---

You are executing the send-email skill. Parse the user's command and send an email using the agent-email prototype.

**Command format:**
```
/send-email <recipient> "<subject>" "<body>" [options]
```

**Options:**
- `--html` - Treat body as HTML content
- `--attachment <path>` - Attach a file

**Execution steps:**

1. Parse the arguments:
   - First argument: recipient email
   - Second argument (quoted): subject line
   - Third argument (quoted): body text
   - Optional flags: --html, --attachment

2. Execute the CLI:
```bash
cd /home/user/protoflow/projects/unspecified/active/tool-resend-email-sender-ezrcn

# For plain text:
./bin/run send -t "<recipient>" -s "<subject>" -b "<body>"

# For HTML:
./bin/run send -t "<recipient>" -s "<subject>" -h "<body>"

# With attachment:
./bin/run send -t "<recipient>" -s "<subject>" -b "<body>" -a "<path>"
```

3. Report the result to the user

**Examples:**

User: `/send-email john@example.com "Hello" "How are you?"`
→ Execute: `./bin/run send -t "john@example.com" -s "Hello" -b "How are you?"`

User: `/send-email jane@example.com "Report" "<h1>Weekly Report</h1>" --html`
→ Execute: `./bin/run send -t "jane@example.com" -s "Report" -h "<h1>Weekly Report</h1>"`

**Error handling:**
- If dependencies not installed: Run `npm install` first
- If API key missing: Guide user to check `.env` file
- If send fails: Show the error message from Resend
