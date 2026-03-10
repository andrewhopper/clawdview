---
name: send-email
description: Send emails using Resend API via the agent-email prototype
version: 1.0.0
---

# Send Email Skill

**Send emails using Resend API**

## Execution Flow

1. **Parse input** → extract recipient, subject, body from arguments
2. **Validate** → ensure required fields present
3. **Send email** → execute agent-email CLI
4. **Return result** → display success/error to user

## Usage

Invoke with `/send-email` slash command or trigger this skill directly.

```
/send-email to@example.com "Subject line" "Email body"
/send-email to@example.com "Subject" "Body" --html
/send-email to@example.com "Subject" "Body" --attachment ./file.pdf
```

## Implementation

### Step 1: Parse Arguments

Arguments format:
- `$1` - Recipient email address (required)
- `$2` - Subject line (required)
- `$3` - Body text (required)
- `--html` - Treat body as HTML
- `--attachment <path>` - Attach a file

### Step 2: Execute Email Send

```bash
cd /home/user/protoflow/projects/unspecified/active/tool-resend-email-sender-ezrcn

# Plain text email
./bin/run send -t "$TO" -s "$SUBJECT" -b "$BODY"

# HTML email
./bin/run send -t "$TO" -s "$SUBJECT" -h "$BODY"

# With attachment
./bin/run send -t "$TO" -s "$SUBJECT" -b "$BODY" -a "$ATTACHMENT"
```

### Step 3: Handle Result

- Success: Display email ID and confirmation
- Error: Show error message and suggest fixes

## Examples

**Simple email:**
```
/send-email john@example.com "Meeting Tomorrow" "Hi John, just confirming our meeting at 2pm tomorrow."
```

**HTML email:**
```
/send-email john@example.com "Weekly Report" "<h1>Report</h1><p>See details below...</p>" --html
```

**With attachment:**
```
/send-email john@example.com "Contract" "Please find the contract attached." --attachment ./contract.pdf
```

## Configuration

The skill uses environment variables from the prototype's `.env` file:

| Variable | Description |
|----------|-------------|
| `RESEND_API_KEY` | Resend API key |
| `DEFAULT_FROM_EMAIL` | Sender address |

## Error Handling

| Error | Action |
|-------|--------|
| Missing API key | Guide user to set RESEND_API_KEY in prototype .env |
| Invalid recipient | Show email format requirements |
| Send failed | Display Resend error message |
| Attachment not found | Show file path error |

## Dependencies

- `tool-resend-email-sender-ezrcn` - Email sending tool
- Environment: `RESEND_API_KEY` configured in prototype

## Notes

- Default sender: `onboarding@resend.dev` (Resend test domain)
- To use custom domain: verify domain in Resend dashboard
- Rate limits apply per Resend plan
