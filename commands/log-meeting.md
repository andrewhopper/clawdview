---
description: Log meeting from calendar entry, find account and opportunities to link
tags: [sales, salesforce, calendar, meetings]
---

# Log Meeting from Calendar Entry

You are helping the user log a meeting to Salesforce using the aws-sentral MCP server.

## Workflow

1. **Parse Calendar Entry**
   - User will paste a raw calendar entry
   - Extract: subject, date/time, attendees, location, description
   - Detect partners: domains that are neither customer nor @amazon.com

2. **Find Account**
   - Extract email domain from attendees (e.g., customer@example.com → example.com)
   - Search Salesforce using search_accounts with domain name first
   - If no results, search again using company name from subject/body
   - Present top 3 matches with:
     ```
     [1] Account Name
         ID: {account-id}
         Owner: {owner-name}
         Territory: {territory}
     ```
   - Ask user to select [1/2/3/s] (s = search with different term)

3. **Find Opportunities**
   - Use get_opportunities_for_account with selected account
   - Present top 5 open opportunities:
     ```
     [1] Opportunity Name
         Amount: ${amount}
         Stage: {stage}
         Close Date: {date}

     [2] Another Opportunity
         ...

     [s] Skip (log to account only)
     ```
   - Ask user to select [1/2/3/4/5/s]

4. **Detect SA Activity Type**
   - Analyze meeting subject and description for keywords:
     - Architecture Review: "architecture", "design", "technical review", "POC", "proof of concept", "benchmark"
     - Demo: "demo", "demonstration", "showcase"
     - Prototype/PoC/Pilot: "prototype", "pilot", "POC", "proof of concept"
     - Well Architected: "well architected", "WAFR", "WAR"
     - Meeting / Office Hours: default for general meetings
   - Suggest the most relevant SA activity type based on detection

5. **Create Tech Activity**
   - **Always use create_tech_activity** (never create_task)
   - Set subject to meeting subject
   - Set status to "Completed"
   - Link to parentRecord (opportunity ID or account ID)
   - Set activityDate to meeting date
   - Set isVirtual to true (always default)
   - Set saActivity (suggest based on keyword detection)
   - Set services (AWS services mentioned in meeting)
   - Set domains (technical domains from context)
   - Include meeting description and attendees

6. **Confirm**
   - Show Salesforce URL for created activity/task
   - Note any partner involvement detected
   - Offer to log another meeting

## Search Strategy

Primary: Extract domain from external attendee emails (skip @amazon.com)
Fallback: Extract company name from meeting subject or location

## Partner Detection

- Extract non-customer, non-Amazon email domains from attendees
- Example: meeting with john@customer.com, partner@loka.com → detect "Loka" as partner
- Note partner involvement in confirmation message
- Partner info is captured in meeting description and opportunity context

## Activity Type Detection

Keywords for automatic suggestion:
- **Architecture Review**: architecture, design, technical review, POC, proof of concept, benchmark
- **Demo**: demo, demonstration, showcase, presentation
- **Prototype/PoC/Pilot**: prototype, pilot, POC, PoC, proof of concept
- **Well Architected**: well architected, WAFR, WAR, architecture review
- **Meeting / Office Hours**: check-in, sync, status, update (default)

## Default Behaviors

- **Activity Type**: Always create Tech Activity (create_tech_activity), never regular task
- **isVirtual**: Always defaults to `true` (most meetings are Zoom/Teams)
- **status**: Always "Completed" (logging past meetings)

## Error Handling

- If no accounts found: ask user to provide account name or ID directly
- If no opportunities found: offer to log to account only
- If activity creation fails: show error and ask user to verify details

## Example Flow

```
User: [pastes calendar entry with attendees: john@acme.com, partner@loka.com]

You: Found meeting "Acme Corp - Architecture Review"
     Date: 2025-12-10 10:00 AM
     Attendees: john@acme.com, partner@loka.com
     Partner detected: Loka (loka.com)

     Searching for account using domain: acme.com

     [1] Acme Corporation
         ID: 001xx000003DGb9AAG
         Owner: John Smith
         Territory: Enterprise West

     Select account [1/s]:

User: 1

You: Found 3 open opportunities:

     [1] Acme Corp - Cloud Migration ($500K)
         Stage: Qualification
         Close: 2026-03-15

     [2] Acme Corp - Data Analytics ($250K)
         Stage: Proposal
         Close: 2026-01-30

     [s] Skip (log to account only)

     Select opportunity [1/2/s]:

User: 1

You: Select SA Activity:
     [1] Architecture Review [Architecture] (suggested)
     [2] Demo [Architecture]
     [3] Prototype/PoC/Pilot [Architecture]
     [4] Meeting / Office Hours [Management]

User: 1

You: AWS Services mentioned (optional):
     [Enter service names, comma-separated, or press Enter to skip]

User: EC2, S3, Lambda

You: Technical Domains (optional):
     [Enter domains, comma-separated, or press Enter to skip]

User: Compute, Storage

You: ✓ Meeting logged to Salesforce
     Task ID: 00Txx000001ABC123
     Type: Tech Activity (Architecture Review)
     Virtual: Yes
     Partner: Loka

     View: https://aws-crm.lightning.force.com/lightning/r/Task/00Txx000001ABC123/view

     Log another meeting? [Y/n]
```

## Implementation Notes

- Use aws-sentral MCP tools (search_accounts, get_opportunities_for_account, create_tech_activity)
- **NEVER use create_task** - always use create_tech_activity
- Parse calendar entries flexibly (handle iCalendar, Outlook, Google formats)
- Extract domains from non-Amazon email addresses
- Detect partners automatically from attendee domains
- Suggest SA activity type based on keywords in subject/description
- Default isVirtual to true for all meetings
- Keep interaction conversational but efficient
- Use AskUserQuestion tool for multiple choice selections when appropriate
