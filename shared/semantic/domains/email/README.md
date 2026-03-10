<!-- File UUID: 9fbfbbe0-3aac-4763-a3b4-db172ec2fc26 -->
# Email Domain Model

Canonical email domain model based on W3C RDF/OWL standards. Reusable across email clients, CRM systems, workflow automation, and AI agents.

## 1.0 Overview

**Domain:** Email communication (messages, folders, attachments, actions)

**Version:** 1.0.0

**Standards:** W3C RDF, OWL, SHACL, RFC 5322 (email format), RFC 2822 (subject length)

**Languages:** TypeScript, Rust, Python

## 2.0 Entities

### 2.1 Email

Electronic mail message.

**Properties:**
- `id` (string) - Unique identifier
- `subject` (string) - Subject line (1-998 chars per RFC 2822)
- `body` (string) - Message body (plain text or HTML)
- `recipients` (string[]) - To addresses (RFC 5322 format)
- `cc` (string[], optional) - Carbon copy recipients
- `bcc` (string[], optional) - Blind carbon copy recipients
- `sender` (Person) - Message sender
- `status` (EmailStatus) - Current status
- `isRead` (boolean) - Read flag
- `sentAt` (DateTime, optional) - Sent timestamp
- `readAt` (DateTime, optional) - Read timestamp
- `deletedAt` (DateTime, optional) - Deletion timestamp
- `attachments` (Attachment[], optional) - File attachments

**Constraints:**
- Subject required, 1-998 characters
- At least one recipient required
- Recipients must match RFC 5322 email format
- Sent emails must have sentAt timestamp
- Read emails (isRead=true) must have readAt timestamp

### 2.2 Folder

Organizational folder for emails.

**Properties:**
- `id` (string) - Unique identifier
- `name` (FolderName) - Folder name (inbox, sent, drafts, trash, archive)
- `emails` (Email[]) - Emails in folder

**Constraints:**
- Name must be one of predefined values

### 2.3 Attachment

File attached to email.

**Properties:**
- `filename` (string) - File name (1-255 chars)
- `contentType` (string) - MIME type
- `size` (integer) - Size in bytes (1 byte - 25MB)
- `url` (string, optional) - Download URL

**Constraints:**
- Filename required, 1-255 characters
- Content type must be valid MIME type
- Size must be 1 byte to 25MB (most email provider limits)

### 2.4 Thread

Conversation thread of related emails.

**Properties:**
- `id` (string) - Unique identifier
- `subject` (string) - Thread subject
- `emails` (Email[]) - Emails in thread

**Constraints:**
- Must contain at least one email

## 3.0 Enums

### 3.1 EmailStatus

```
Draft     - Composed but not sent
Sent      - Delivered to recipients
Deleted   - Moved to trash
Archived  - Long-term storage
```

### 3.2 FolderName

```
inbox     - Received messages
sent      - Sent messages
drafts    - Unsent drafts
trash     - Deleted messages
archive   - Archived messages
```

## 4.0 Actions

### 4.1 SendEmailAction

Send email message to recipients via SMTP.

**Type:** CreateAction (non-idempotent)

**Parameters:**
- `to` (string[], required) - Recipients
- `subject` (string, required) - Subject line
- `body` (string, required) - Message body
- `cc` (string[], optional) - CC recipients
- `bcc` (string[], optional) - BCC recipients
- `attachments` (Attachment[], optional) - Files

**Returns:** Email (with id, sentAt, messageId)

**Permissions:** email:send

**Side Effects:**
- Creates email record in sent folder
- Sends via SMTP
- Updates status to Sent
- Sets sentAt timestamp

**Error Conditions:**
- INVALID_RECIPIENT - Invalid email address format
- SMTP_CONNECTION_ERROR - Cannot connect to mail server
- QUOTA_EXCEEDED - Account storage quota exceeded
- ATTACHMENT_TOO_LARGE - Attachment exceeds size limit

### 4.2 DeleteEmailAction

Move email to trash or permanently delete.

**Type:** DeleteAction (idempotent)

**Parameters:**
- `emailId` (string, required) - Email to delete
- `permanent` (boolean, optional, default: false) - Permanent deletion flag

**Returns:** void

**Permissions:** email:delete

**Side Effects:**
- If permanent=false: Updates status to Deleted, moves to Trash
- If permanent=true: Permanently removes from storage

**Error Conditions:**
- EMAIL_NOT_FOUND - Email does not exist
- INSUFFICIENT_PERMISSIONS - User cannot delete this email

### 4.3 ForwardEmailAction

Forward existing email to new recipients.

**Type:** CreateAction (non-idempotent)

**Parameters:**
- `emailId` (string, required) - Email to forward
- `to` (string[], required) - New recipients
- `message` (string, optional) - Prepended message

**Returns:** Email (forwarded message)

**Permissions:** email:send

**Side Effects:**
- Creates new email with original content quoted
- Sends to new recipients
- Preserves original attachments

**Error Conditions:**
- EMAIL_NOT_FOUND - Original email not found
- INVALID_RECIPIENT - Invalid recipient format
- SMTP_CONNECTION_ERROR - Cannot send

### 4.4 MarkAsReadAction

Update email read status.

**Type:** UpdateAction (idempotent)

**Parameters:**
- `emailId` (string, required) - Email to mark

**Returns:** Email (updated)

**Permissions:** email:read

**Side Effects:**
- Sets isRead to true
- Records readAt timestamp

**Error Conditions:**
- EMAIL_NOT_FOUND - Email does not exist

### 4.5 ArchiveEmailAction

Move email to archive folder.

**Type:** UpdateAction (idempotent)

**Parameters:**
- `emailId` (string, required) - Email to archive

**Returns:** Email (archived)

**Permissions:** email:archive

**Side Effects:**
- Updates status to Archived
- Moves to Archive folder

**Error Conditions:**
- EMAIL_NOT_FOUND - Email does not exist

### 4.6 SearchEmailsAction

Search emails by keywords, sender, date range.

**Type:** ReadAction (idempotent)

**Parameters:**
- `query` (string, required) - Search query
- `folder` (string, optional) - Limit to folder
- `dateFrom` (Date, optional) - Start date
- `dateTo` (Date, optional) - End date

**Returns:** Email[] (matching results, sorted by relevance)

**Permissions:** email:read

**Side Effects:** None (read-only)

**Error Conditions:**
- INVALID_QUERY_SYNTAX - Malformed search query

## 5.0 Business Rules

**Rule 1: Sent emails require timestamp**
- Emails with status=Sent MUST have sentAt timestamp
- Enforced via SHACL constraint

**Rule 2: Read emails require timestamp**
- Emails with isRead=true MUST have readAt timestamp
- Enforced via SHACL constraint

**Rule 3: Email address validation**
- All recipient addresses (to, cc, bcc) MUST match RFC 5322 format
- Regex: `^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$`
- Enforced via SHACL pattern constraint

**Rule 4: Subject length limits**
- Subject line MUST be 1-998 characters per RFC 2822
- Enforced via SHACL minLength/maxLength

**Rule 5: Attachment size limits**
- Attachments MUST be 1 byte to 25MB (26,214,400 bytes)
- Matches most email provider limits (Gmail, Outlook, etc.)
- Enforced via SHACL minInclusive/maxInclusive

**Rule 6: Thread minimum**
- Threads MUST contain at least one email
- Enforced via SHACL minCount

**Rule 7: Folder name restrictions**
- Folder name MUST be one of: inbox, sent, drafts, trash, archive
- Enforced via SHACL enumeration

## 6.0 Use Cases

### 6.1 Email Client Application

```typescript
import { Email, EmailStatus, sendEmail } from '@shared/domain-models/email/generated/typescript';

// Send email
const email = await sendEmail({
  to: ['user@example.com'],
  subject: 'Meeting Notes',
  body: 'Please review the attached slides.',
  attachments: [{ filename: 'slides.pdf', contentType: 'application/pdf', size: 1024000 }],
});

// Search inbox
const results = await searchEmails({
  query: 'project alpha',
  folder: 'inbox',
  dateFrom: new Date('2025-11-01'),
});
```

### 6.2 CRM with Email Integration

```rust
use shared::semantic::domains::email::*;

// Forward customer email to team
let forwarded = forward_email(ForwardEmailInput {
    email_id: "msg-123",
    to: vec!["sales@company.com", "support@company.com"],
    message: Some("Customer inquiry - please follow up"),
});

// Archive resolved customer emails
archive_email("msg-456");
```

### 6.3 Workflow Automation

```python
from shared.semantic.domains.email import send_email, EmailStatus

# Automated weekly report
send_email(
    to=["manager@company.com"],
    subject="Weekly Status Report",
    body=generate_report(),
    attachments=[create_chart_attachment()],
)
```

## 7.0 Integration with Other Domains

**CRM Domain:**
- Link Email to Contact (sender/recipient mapping)
- Link Email to Account (customer communication)
- Link Email to Opportunity (sales correspondence)

**Calendar Domain:**
- Extract meeting invites from email
- Create calendar events from email

**Task Domain:**
- Create tasks from email action items
- Link email to task context

**AI Agent Domain:**
- Email as input to agent (process customer inquiry)
- Email as agent output (send response)

## 8.0 Files

```
email/
├── ontology.ttl         # W3C RDF/OWL canonical model
├── rules.shacl.ttl      # SHACL validation constraints
├── version.json         # Semantic version metadata
├── README.md            # This file
└── generated/           # Auto-generated types
    ├── typescript/
    │   └── email.types.ts
    ├── rust/
    │   └── email.rs
    └── python/
        └── email.py
```

## 9.0 Standards References

**W3C:**
- RDF: https://www.w3.org/RDF/
- OWL: https://www.w3.org/OWL/
- SHACL: https://www.w3.org/TR/shacl/

**IETF RFC:**
- RFC 5322: Internet Message Format
- RFC 2822: Email subject line length limits

**MIME:**
- RFC 2045: MIME Part One (content types)

## 10.0 Version History

**1.0.0** (2025-11-21)
- Initial release
- Entities: Email, Folder, Attachment, Thread
- Actions: Send, Delete, Forward, MarkAsRead, Archive, Search
- SHACL business rules
- TypeScript, Rust, Python type generation

## 11.0 Future Enhancements

**Planned:**
- Email templates (reusable message formats)
- Email signatures (automatic signature insertion)
- Email filters (rule-based organization)
- Spam detection (classify spam vs legitimate)
- Encryption support (PGP, S/MIME)

**Research:**
- AI-powered email categorization
- Smart reply suggestions
- Meeting detection and calendar integration
- Attachment preview generation
