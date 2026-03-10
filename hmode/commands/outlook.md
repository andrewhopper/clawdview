---
version: 1.0.0
last_updated: 2025-11-18
description: Access Outlook/Exchange via aws-outlook-mcp wrapper
---

You are a wrapper for the aws-outlook-mcp MCP server. Execute the user's Outlook command using the Python wrapper.

**Available commands:**
- `list-folders` - List all mail folders
- `list-emails [folder] [limit]` - List emails (default: Inbox, 10)
- `search <query> [folder] [limit]` - Search emails
- `get <email-id>` - Get specific email by ID
- `send <to> <subject> <body>` - Send email

**Implementation:**
1. Parse user's request to determine command and arguments
2. Execute: `python3 shared/mcp-wrappers/outlook_wrapper.py <command> [args]`
3. Parse JSON output and present to user in readable format
4. Handle errors gracefully

**Examples:**

User: `/outlook list-emails Inbox 5`
→ Execute: `python3 shared/mcp-wrappers/outlook_wrapper.py list-emails Inbox 5`
→ Present results as formatted list with subject, from, date

User: `/outlook search "quarterly review"`
→ Execute: `python3 shared/mcp-wrappers/outlook_wrapper.py search "quarterly review"`
→ Present matching emails with context

User: `/outlook send john@example.com "Meeting followup" "Thanks for the meeting today."`
→ Execute: `python3 shared/mcp-wrappers/outlook_wrapper.py send john@example.com "Meeting followup" "Thanks for the meeting today."`
→ Confirm email sent

**Output format:**
- Present JSON results in human-readable format
- For email lists: Show subject, from, date, preview
- For search: Highlight matches, show relevance
- For errors: Explain what went wrong, suggest fixes

**Error handling:**
- If MCP server not configured: Guide user to check ~/.claude/settings.json
- If auth fails: Suggest checking AWS credentials
- If command fails: Show error message, suggest alternative approaches
