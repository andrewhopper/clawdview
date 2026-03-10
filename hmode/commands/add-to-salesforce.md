---
uuid: cmd-add-salesforce-2b3c4d5e
version: 1.0.0
last_updated: 2025-11-10
description: Add email interaction to Salesforce (Opportunity, Contact, or Account)
---

# Add to Salesforce

You are a Salesforce integration assistant. Help users log email interactions to Salesforce records quickly and accurately.

## 🚨 WEB SESSION COMPATIBLE

This command works in stateless web sessions:
- All inputs via arguments/flags
- No mid-execution questions
- Auto-detects record details from email content

## Usage

```bash
# Add to Opportunity
/add-to-salesforce opportunity "Partnership Discussion - TechCorp"

# Add to Contact
/add-to-salesforce contact "Mike Chen" --company="TechCorp"

# Add to Account
/add-to-salesforce account "TechCorp"

# With email file reference
/add-to-salesforce opportunity "API Integration Deal" --email-file=draft-reply-2025-01-15.txt

# With additional metadata
/add-to-salesforce opportunity "Premium Plan Upgrade" --amount=50000 --stage="Qualification" --close-date="2025-02-15"
```

## Record Types

### Opportunity
Create or update a sales opportunity.

**Required**:
- Name/Subject

**Optional**:
- `--amount=N` - Deal amount ($)
- `--stage=X` - Sales stage (Qualification, Proposal, Negotiation, Closed Won, etc.)
- `--close-date=YYYY-MM-DD` - Expected close date
- `--probability=N` - Win probability (0-100)
- `--account=X` - Associated account name
- `--contact=X` - Primary contact name

### Contact
Create or update a contact record.

**Required**:
- Name

**Optional**:
- `--company=X` - Company/Account name
- `--title=X` - Job title
- `--email=X` - Email address
- `--phone=X` - Phone number
- `--status=X` - Lead status (if converting from lead)

### Account
Create or update an account (company) record.

**Required**:
- Name

**Optional**:
- `--industry=X` - Industry
- `--employees=N` - Number of employees
- `--revenue=N` - Annual revenue
- `--website=X` - Company website
- `--type=X` - Account type (Customer, Prospect, Partner, etc.)

## Common Options (All Types)

- `--email-file=path` - Reference to email draft file (auto-populates context)
- `--notes="text"` - Additional notes to add to activity log
- `--task="text"` - Create follow-up task
- `--task-date=YYYY-MM-DD` - Follow-up task due date
- `--owner=X` - Salesforce record owner (defaults to you)
- `--campaign=X` - Link to marketing campaign
- `--source=X` - Lead source (Web, Referral, Event, etc.)

## Instructions

1. **Parse command arguments**:
   ```
   /add-to-salesforce <record-type> <name/subject> [options]
   ```
   - Record type: opportunity, contact, account (required)
   - Name/Subject: Record identifier (required)
   - Options: All flags (optional)

2. **Read email file if provided**:
   - If `--email-file` specified, read the file
   - Extract: sender, recipient, subject, content, date
   - Auto-populate fields from email content
   - Use as activity description

3. **Auto-detect fields from email** (when --email-file provided):

   **From email headers**:
   - Contact name: From sender name
   - Contact email: From sender email
   - Subject: Use as opportunity name or activity subject
   - Date: Timestamp for activity

   **From email content** (smart parsing):
   - Company name: Look for "from [Company]", email domain, signature
   - Deal amount: Look for $X, pricing mentions
   - Timeline: Look for deadline, "by [date]", urgency keywords
   - Stage: Infer from content (inquiry→Qualification, proposal→Proposal, etc.)

4. **Validate required fields**:
   - Record type must be: opportunity, contact, or account
   - Name/subject must be provided
   - Email format validation (if --email provided)
   - Date format validation (if dates provided)

5. **Determine if record exists or create new**:
   ```
   🔍 Searching Salesforce for existing records...

   Found: 1 matching Contact: "Mike Chen" at TechCorp
   Would you like to:
   1. Update existing record (recommended)
   2. Create new record
   3. Cancel

   [In web sessions, default to #1 with notification]
   ```

   **Web session behavior**:
   - Always update if exact match found
   - Create new if no match
   - Display what was done

6. **Create/Update Salesforce record**:

   **Opportunity**:
   ```json
   {
     "Name": "[subject]",
     "Amount": [amount],
     "StageName": "[stage]",
     "CloseDate": "[close-date]",
     "Probability": [probability],
     "AccountId": "[account-id]",
     "ContactId": "[contact-id]",
     "OwnerId": "[owner-id]",
     "LeadSource": "[source]",
     "CampaignId": "[campaign-id]"
   }
   ```

   **Contact**:
   ```json
   {
     "FirstName": "[first]",
     "LastName": "[last]",
     "Email": "[email]",
     "Phone": "[phone]",
     "Title": "[title]",
     "AccountId": "[account-id]",
     "LeadSource": "[source]",
     "OwnerId": "[owner-id]"
   }
   ```

   **Account**:
   ```json
   {
     "Name": "[name]",
     "Industry": "[industry]",
     "NumberOfEmployees": [employees],
     "AnnualRevenue": [revenue],
     "Website": "[website]",
     "Type": "[type]",
     "OwnerId": "[owner-id]"
   }
   ```

7. **Log email activity**:
   Create Task/Activity record:
   ```json
   {
     "Subject": "Email: [email-subject]",
     "Description": "[email-content]",
     "ActivityDate": "[date]",
     "Status": "Completed",
     "Type": "Email",
     "WhoId": "[contact-id]",
     "WhatId": "[opportunity/account-id]",
     "OwnerId": "[owner-id]"
   }
   ```

8. **Create follow-up task** (if --task provided):
   ```json
   {
     "Subject": "[task]",
     "Description": "Follow-up from email: [email-subject]",
     "ActivityDate": "[task-date]",
     "Status": "Not Started",
     "Priority": "Normal",
     "WhoId": "[contact-id]",
     "WhatId": "[opportunity/account-id]",
     "OwnerId": "[owner-id]"
   }
   ```

9. **Display summary**:
   ```
   ✅ Added to Salesforce!

   📊 Record Type: Opportunity
   📝 Name: Partnership Discussion - TechCorp
   🆔 Salesforce ID: 006XXXXXXXXXXXX
   💰 Amount: $50,000
   📈 Stage: Qualification
   📅 Close Date: 2025-02-15

   📧 Email Activity Logged:
   - Subject: Re: Partnership opportunity
   - Date: 2025-01-15 14:30
   - Direction: Outbound
   - Content: [First 100 chars of email]

   ✅ Follow-up Task Created:
   - Task: Schedule discovery call with Mike
   - Due: 2025-01-18
   - Owner: You

   🔗 View in Salesforce:
   https://yourinstance.salesforce.com/006XXXXXXXXXXXX

   📊 Related Records:
   - Account: TechCorp (001XXXXXXXXXXXX)
   - Contact: Mike Chen (003XXXXXXXXXXXX)
   ```

## Examples

### Example 1: Partnership Opportunity

```bash
/add-to-salesforce opportunity "TechCorp Partnership - API Integration" \
  --email-file=draft-reply-2025-01-15-143022.txt \
  --amount=50000 \
  --stage="Qualification" \
  --close-date="2025-03-31" \
  --task="Schedule technical discovery call" \
  --task-date="2025-01-18"
```

**Output**:
```
✅ Salesforce Opportunity Created!

📊 Opportunity: TechCorp Partnership - API Integration
🆔 ID: 006XXXXXXXXXXXX
💰 Amount: $50,000
📈 Stage: Qualification
📅 Expected Close: March 31, 2025
🎯 Probability: 20% (auto-set based on stage)

📧 Email Activity:
✓ Logged outbound email response
✓ Attached email content to opportunity
✓ Linked to Contact: Mike Chen (VP Partnerships)
✓ Linked to Account: TechCorp

📋 Follow-up Task:
✓ Task: Schedule technical discovery call
✓ Due: January 18, 2025
✓ Owner: You

🔗 View in Salesforce:
https://yourinstance.salesforce.com/006XXXXXXXXXXXX

Next steps:
1. Review opportunity details in Salesforce
2. Complete discovery call by Jan 18
3. Update stage after call
```

### Example 2: New Contact from Email

```bash
/add-to-salesforce contact "Sarah Johnson" \
  --email-file=draft-reply-2025-01-15-150433.txt \
  --company="DataTech Solutions" \
  --title="Product Manager" \
  --source="Website"
```

**Output**:
```
✅ Salesforce Contact Created!

👤 Contact: Sarah Johnson
🆔 ID: 003XXXXXXXXXXXX
🏢 Account: DataTech Solutions (001XXXXXXXXXXXX)
💼 Title: Product Manager
📧 Email: sarah.j@datatech.com (from email file)
📞 Phone: (extracted if in signature)
🎯 Lead Source: Website

📧 Email Activity:
✓ Logged email: "Re: Product not working as expected"
✓ Direction: Outbound (customer support)
✓ Status: Completed

🔗 View in Salesforce:
https://yourinstance.salesforce.com/003XXXXXXXXXXXX

💡 Suggested next step:
Consider creating an Opportunity if this becomes a sales discussion:
/add-to-salesforce opportunity "DataTech - Premium Plan Upgrade" --contact="Sarah Johnson"
```

### Example 3: Update Account Record

```bash
/add-to-salesforce account "TechCorp" \
  --industry="Software" \
  --employees=250 \
  --revenue=25000000 \
  --website="https://techcorp.com" \
  --type="Prospect" \
  --notes="Inbound partnership inquiry - high priority"
```

**Output**:
```
✅ Salesforce Account Updated!

🏢 Account: TechCorp
🆔 ID: 001XXXXXXXXXXXX
🏭 Industry: Software
👥 Employees: 250
💰 Annual Revenue: $25M
🌐 Website: techcorp.com
📊 Type: Prospect

📝 Notes Added:
"Inbound partnership inquiry - high priority"

🔗 View in Salesforce:
https://yourinstance.salesforce.com/001XXXXXXXXXXXX

📊 Related Records:
- 3 Contacts
- 1 Open Opportunity ($50K)
- 5 Closed Activities
```

## Salesforce API Integration

This command uses the Salesforce REST API:

**Authentication**:
- OAuth 2.0 flow
- Store credentials in `.env` (never commit!)
- Refresh token automatically

**Required Environment Variables**:
```bash
SALESFORCE_INSTANCE_URL=https://yourinstance.salesforce.com
SALESFORCE_ACCESS_TOKEN=your-access-token
SALESFORCE_REFRESH_TOKEN=your-refresh-token
SALESFORCE_CLIENT_ID=your-client-id
SALESFORCE_CLIENT_SECRET=your-client-secret
```

**API Endpoints Used**:
- Create: `POST /services/data/v59.0/sobjects/{ObjectType}`
- Update: `PATCH /services/data/v59.0/sobjects/{ObjectType}/{Id}`
- Query: `GET /services/data/v59.0/query?q={SOQL}`
- Search: `GET /services/data/v59.0/search?q={SOSL}`

## Field Mapping

### Email Content → Salesforce Fields

**Opportunity**:
- Email subject → Opportunity Name
- $ mentions → Amount
- "by [date]" → Close Date
- Content tone → Stage (inquiry=Qualification, pricing=Proposal)
- Urgency keywords → Priority/Next Step Date

**Contact**:
- From name → FirstName, LastName
- From email → Email
- Email domain → Account (if matches existing)
- Signature → Title, Phone, Company

**Account**:
- Email domain → Website
- Signature company → Name
- LinkedIn mentions → Industry, Size

## Stage Auto-Detection

Based on email content, suggest stage:

**Keywords → Stage mapping**:
- "interested in", "exploring", "looking into" → Qualification
- "proposal", "quote", "pricing" → Proposal
- "reviewing", "discussing terms", "contract" → Negotiation
- "approved", "moving forward", "signed" → Closed Won
- "unfortunately", "passing", "not right now" → Closed Lost

## Error Handling

**Missing required fields**:
```
❌ Error: Missing required field

/add-to-salesforce <record-type> <name> [options]

Required:
- record-type: opportunity, contact, or account
- name: Record name or subject

Example:
/add-to-salesforce opportunity "Deal Name" --amount=50000
```

**Invalid record type**:
```
❌ Error: Invalid record type: "lead"

Valid types:
- opportunity
- contact
- account

Usage:
/add-to-salesforce contact "John Doe" --company="Acme Corp"
```

**Salesforce API error**:
```
❌ Salesforce API Error

Error: REQUIRED_FIELD_MISSING
Field: CloseDate
Message: Close Date is required for Opportunity

Fix:
/add-to-salesforce opportunity "Deal" --close-date="2025-02-28"
```

**Authentication failure**:
```
❌ Salesforce Authentication Failed

Please check your credentials in .env:
- SALESFORCE_INSTANCE_URL
- SALESFORCE_ACCESS_TOKEN
- SALESFORCE_REFRESH_TOKEN

To re-authenticate:
1. Go to: https://login.salesforce.com
2. Authorize this app
3. Update .env with new tokens
```

## Configuration

Add to `.env`:
```bash
# Salesforce Configuration
SALESFORCE_INSTANCE_URL=https://yourcompany.salesforce.com
SALESFORCE_ACCESS_TOKEN=00D...
SALESFORCE_REFRESH_TOKEN=your-refresh-token
SALESFORCE_CLIENT_ID=your-connected-app-client-id
SALESFORCE_CLIENT_SECRET=your-connected-app-secret
SALESFORCE_DEFAULT_OWNER_ID=005XXXXXXXXXXXX
```

## Smart Defaults

If not specified, use:
- **Opportunity Stage**: Qualification (first touch)
- **Opportunity Probability**: Based on stage (Qualification=20%, Proposal=50%, etc.)
- **Close Date**: 90 days from today (if not provided)
- **Lead Source**: Email (if from email file)
- **Owner**: Current user (from auth token)
- **Priority**: Normal

## Security

**Never commit**:
- `.env` files with Salesforce credentials
- Access tokens
- API keys
- Customer email content to public repos

**Best practices**:
- Rotate tokens regularly
- Use OAuth refresh tokens
- Limit API permissions to minimum needed
- Audit Salesforce API usage

## Integration with /draft-reply

The `/draft-reply` command calls this command:

**Workflow**:
1. User: `/draft-reply email.txt --salesforce --sf-type=opportunity`
2. System: Drafts email response
3. System: Shows Salesforce command to run
4. User: Runs `/add-to-salesforce` command (or system auto-runs if flag present)
5. System: Logs activity, creates records

**Auto-population**:
- Email file path passed via `--email-file`
- Record type inferred from `--sf-type` flag
- Fields auto-extracted from email content

## Future Enhancements

**Planned features**:
- Multi-email thread → Campaign creation
- Attachment handling (save to Files)
- Email-to-Case conversion
- Lead assignment rules
- Duplicate detection/merging
- Bulk operations
- Custom object support
- Integration with Gmail/Outlook

## Implementation Notes

1. **Use Salesforce REST API** (not SOAP - simpler)
2. **Handle token refresh** automatically
3. **Validate all inputs** before API calls
4. **Parse email intelligently** - use regex for common patterns
5. **Default to update** if record exists (avoid duplicates)
6. **Log all API calls** for debugging
7. **Graceful error handling** with actionable messages
8. **Show Salesforce URLs** for quick access

---

**Philosophy**: Make Salesforce data entry effortless by auto-extracting context from email interactions. Keep your CRM up-to-date without manual copying.
