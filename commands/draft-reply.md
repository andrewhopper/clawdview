---
uuid: cmd-draft-reply-3m4n5o6p
version: 1.0.0
last_updated: 2025-11-10
description: Draft empathetic email reply with solutions and next steps
---

# Draft Email Reply

You are an email response assistant. Create thoughtful, solution-oriented email replies that build relationships and move conversations forward.

## 🚨 WEB SESSION COMPATIBLE

This command works in stateless web sessions:
- All inputs via arguments/flags
- No mid-execution questions
- Smart defaults where possible

## Usage

```bash
# With email file
/draft-reply path/to/email.txt

# With inline content
/draft-reply "Email content here..."

# With options
/draft-reply email.txt --tone=formal --bcc=crm@company.com --salesforce --sf-type=opportunity

# Multiple emails in thread
/draft-reply thread.txt --thread
```

## Options

- `--tone=formal|casual|neutral` - Response tone (default: neutral)
- `--bcc=email@domain.com` - BCC address for CRM archiving (overrides config)
- `--salesforce` - Enable Salesforce integration prompt
- `--sf-type=opportunity|contact|account` - Salesforce record type (requires --salesforce)
- `--thread` - Input contains multiple emails in thread
- `--solutions=N` - Number of solution variants to propose (default: 3, range: 3-5)

## Email Structure

The response will contain:

### Part 1: Empathize & Reiterate
- Acknowledge sender's concerns
- Reflect understanding of context
- Build shared understanding
- Show active listening

### Part 2: Proposed Solutions (3-5 Divergent Options)
Present multiple approaches:
- **Option A**: [Conservative/safe approach]
- **Option B**: [Innovative/bold approach]
- **Option C**: [Compromise/middle ground]
- **Option D** (optional): [Alternative angle]
- **Option E** (optional): [Edge case consideration]

Each option includes:
- Clear description
- Key benefits
- Potential considerations
- Estimated timeline/effort

### Part 3: Move Forward
- Call to action (meeting invite, schedule link, next steps)
- Specific ask or proposal
- Timeline suggestion
- Clear ownership

### Part 4: Professional Closing
- Warm sign-off
- Contact information
- Availability

## BCC Configuration

Default BCC address configured in `.claude/settings.json`:

```json
{
  "emailConfig": {
    "defaultBcc": "crm@yourcompany.com",
    "crmSystem": "salesforce"
  }
}
```

Override with `--bcc` flag for specific emails.

## Salesforce Integration

When `--salesforce` flag is used:

1. Draft email is generated
2. User is prompted ONCE at the end:
   ```
   📧 Email draft ready!

   Would you like to add this to Salesforce?
   - Use /add-to-salesforce opportunity <details>
   - Use /add-to-salesforce contact <details>
   - Use /add-to-salesforce account <details>
   ```

If `--sf-type` is provided, automatically suggest the specific command:
```
/add-to-salesforce opportunity "Subject" --email-file=artifacts/email-drafts/draft-reply-TIMESTAMP.txt
```

## Instructions

0. **Detect email type**:
   - Check subject/content for: "delivery", "prototype", "artifact", "package", "attached"
   - If delivery email → Use shortened "Delivery/Prototype Email Format" (max 45 lines)
   - If consultative email → Use full format with empathy + solutions

1. **Parse input**:
   - If argument is file path → read file
   - If argument is text → use directly
   - If `--thread` flag → parse multiple emails
   - Extract: sender, subject, key concerns, context

2. **Analyze email content**:
   - Identify main concerns/questions
   - Detect emotional tone
   - Extract action items or requests
   - Note any deadlines or urgency
   - Map to problem categories

3. **Read BCC configuration**:
   - Check `.claude/settings.json` for `emailConfig.defaultBcc`
   - Use `--bcc` flag if provided (overrides config)
   - If neither exists, skip BCC (warn user)

4. **Determine tone**:
   - `formal`: Business formal, third-person where appropriate
   - `casual`: Friendly, conversational, first-person
   - `neutral`: Professional but approachable (default)
   - Analyze input email tone if not specified

5. **Generate Part 1: Empathize & Reiterate**:
   ```
   Hi [Name],

   Thank you for reaching out about [topic]. I understand [restate their concern/situation].
   This is [acknowledge importance/impact].

   [2-3 sentences showing you "get it" - build rapport]
   ```

6. **Generate Part 2: Proposed Solutions**:
   Create 3-5 distinct approaches:

   ```
   I've thought through a few different approaches we could take:

   **Option A: [Descriptive Name]**
   [Description of approach]
   - Benefits: [2-3 key advantages]
   - Considerations: [Potential drawbacks/requirements]
   - Timeline: [Rough estimate]

   **Option B: [Descriptive Name]**
   [Different approach - divergent from A]
   - Benefits: [Different value proposition]
   - Considerations: [Different trade-offs]
   - Timeline: [Different timeframe]

   **Option C: [Descriptive Name]**
   [Third distinct approach]
   - Benefits: [Unique advantages]
   - Considerations: [Unique considerations]
   - Timeline: [Estimated timeframe]
   ```

   **Divergence guidelines**:
   - Vary on: scope, timeline, risk, cost, complexity
   - Include: quick win, comprehensive solution, innovative approach
   - Avoid: minor variations of same idea
   - Examples:
     - A: Fix immediately (tactical)
     - B: Redesign properly (strategic)
     - C: Partner with vendor (outsource)

7. **Generate Part 3: Move Forward**:
   ```
   I'd love to discuss which approach resonates with you.

   [SPECIFIC CALL TO ACTION - choose one]:
   - "Would you be available for a 30-minute call this week? Here's my calendar: [link]"
   - "I've sent you a calendar invite for [date/time] - let me know if that works"
   - "Could we schedule time to review these options together?"
   - "I'd like to move forward with Option [X] unless you prefer another - can we sync?"

   [NEXT STEPS]:
   - [Specific action item 1]
   - [Specific action item 2]
   - [Decision needed by when]
   ```

8. **Generate Part 4: Closing**:
   ```
   Looking forward to your thoughts!

   Best regards,
   [Your name]

   [Optional: Contact info, availability notes]
   ```

9. **Add BCC notation**:
   ```
   ---
   📧 BCC: [email from config or flag]
   💡 Purpose: CRM archiving
   ```

10. **Save draft**:
    - Create file: `artifacts/email-drafts/draft-reply-[TIMESTAMP].txt`
    - Include full email with BCC notation
    - Include metadata (original email reference, options used)

11. **Display summary**:
    ```
    ✅ Email Reply Drafted!

    📧 Draft saved to: artifacts/email-drafts/draft-reply-[TIMESTAMP].txt

    Structure:
    ✓ Part 1: Empathy & context understanding
    ✓ Part 2: [N] solution options (divergent approaches)
    ✓ Part 3: Call to action + next steps
    ✓ Part 4: Professional closing

    📋 BCC: [email] (for CRM archiving)

    ---

    [FULL EMAIL TEXT HERE]

    ---
    ```

12. **Salesforce prompt** (if `--salesforce` flag used):
    ```
    🔗 Salesforce Integration

    Ready to log this in Salesforce? Use one of:

    /add-to-salesforce opportunity "Subject" --email-file=artifacts/email-drafts/draft-reply-[TIMESTAMP].txt
    /add-to-salesforce contact "Name" --email-file=artifacts/email-drafts/draft-reply-[TIMESTAMP].txt
    /add-to-salesforce account "Company" --email-file=artifacts/email-drafts/draft-reply-[TIMESTAMP].txt
    ```

    If `--sf-type` specified, show only that command:
    ```
    /add-to-salesforce [sf-type] "[auto-detected-details]" --email-file=artifacts/email-drafts/draft-reply-[TIMESTAMP].txt
    ```

## Examples

### Example 1: Customer Complaint

**Input email**:
```
Subject: Product not working as expected

Hi,

I purchased your Premium plan last week but I'm having trouble with the export feature.
It keeps timing out and I have a deadline tomorrow. This is really frustrating.

Can you help?
- Sarah
```

**Generated reply**:
```
Hi Sarah,

Thank you for reaching out, and I'm sorry to hear you're experiencing issues with the export feature.
I understand you have a deadline tomorrow, which makes this especially time-sensitive and stressful.
Getting your exports working reliably is critical, and I want to make sure we resolve this for you
right away.

I've identified a few approaches we can take to get you unblocked:

**Option A: Immediate Workaround (Quick Fix)**
I can provide you with a temporary export script that bypasses the UI and exports your data directly.
This should work within the hour.
- Benefits: Gets you unblocked immediately, no waiting for fixes
- Considerations: Requires basic command-line usage, temporary solution only
- Timeline: 30 minutes to set up

**Option B: Priority Bug Fix (Comprehensive)**
Our engineering team can prioritize this as a critical bug and deploy a fix to production.
- Benefits: Permanent solution, helps all users, no workarounds needed
- Considerations: Estimated 4-6 hours for fix + testing + deployment
- Timeline: Potentially resolved by end of day, may not meet your deadline

**Option C: Manual Export Assistance (White Glove)**
I can personally run the export for you on our backend and send you the files directly.
- Benefits: Zero setup on your end, guaranteed to work
- Considerations: Requires you to specify exactly what you need exported
- Timeline: 15 minutes once you confirm the parameters

Given your timeline, I'd recommend starting with Option C to meet your deadline, while we work on
Option B in parallel for the long-term fix.

Could we jump on a quick 10-minute call to confirm the export parameters? I'm available for the
next 2 hours. Alternatively, you can reply with:
- Which data you need exported
- Date range
- Format preference (CSV, Excel, JSON)

And I'll get the files to you within 15 minutes.

Next steps:
1. You: Confirm export details or schedule quick call
2. Me: Deliver export files immediately
3. Engineering: Deploy permanent fix by EOD

Looking forward to getting you unblocked!

Best regards,
[Your name]
Customer Success Team

---
📧 BCC: crm@yourcompany.com
💡 Purpose: CRM archiving
```

### Example 2: Partnership Inquiry

**Input email**:
```
Subject: Potential partnership opportunity

Hi there,

We're a B2B SaaS company with 50K users and we're looking for integration partners.
Your product seems like a good fit. Any interest in exploring this?

Best,
Mike Chen
VP Partnerships, TechCorp
```

**Generated reply** (formal tone):
```
Hi Mike,

Thank you for reaching out about a potential partnership. I appreciate you considering our platform
as an integration partner. A partnership with TechCorp, especially given your 50K user base, could
create significant value for both our customer communities.

I've outlined a few partnership models we could explore:

**Option A: Technical API Integration (Deep Integration)**
Build a native integration between our platforms with bi-directional data sync and shared workflows.
- Benefits: Seamless user experience, strong product differentiation, shared customer value
- Considerations: 3-4 month development timeline, requires dedicated engineering resources from both sides
- Timeline: 2-week scoping → 3-month build → 1-month beta

**Option B: Marketplace Listing (Quick Launch)**
Launch a lighter integration via our marketplace with OAuth and basic data sharing.
- Benefits: Faster time to market (4-6 weeks), lower engineering investment, test demand first
- Considerations: Less feature-rich than Option A, may need to enhance later
- Timeline: 1-week scoping → 3-week build → 1-week listing approval

**Option C: Co-Marketing Partnership (No-Code Start)**
Begin with a co-marketing agreement and joint customer referral program while we evaluate technical fit.
- Benefits: Immediate value, no technical dependencies, builds relationship first
- Considerations: Customers may request deeper integration, sets expectation for future tech work
- Timeline: 1-week agreement → immediate launch

**Option D: White-Label Reseller (Strategic)**
We provide our platform white-labeled within TechCorp's product suite.
- Benefits: New revenue stream for TechCorp, expanded reach for us, premium positioning
- Considerations: Complex legal/commercial terms, requires sales alignment
- Timeline: 4-week commercial negotiation → 6-week implementation

My recommendation would be to start with Option B (marketplace integration) to validate customer
demand and user experience, with a clear path to Option A if the partnership proves valuable.

I'd love to schedule a 45-minute exploratory call to discuss your integration vision and partnership
goals. Are you available next week? Here's my calendar link: [link]

If you prefer, I can also send you our partnership deck and technical integration guide beforehand.

Next steps:
1. You: Share your partnership priorities and ideal timeline
2. Us: Schedule discovery call for next week
3. Both: Decide on partnership model and draft agreement

Looking forward to exploring this opportunity together!

Best regards,
[Your name]
Head of Partnerships

---
📧 BCC: partnerships@yourcompany.com
💡 Purpose: CRM archiving
```

## Tone Guidelines

### Formal
- Use full sentences and proper grammar
- Avoid contractions
- Professional salutations
- Third-person where appropriate
- Structured, clear formatting
- Example: "I would be pleased to discuss this matter further."

### Casual
- Conversational language
- Contractions OK
- Friendly tone
- First-person
- More relaxed structure
- Example: "I'd love to chat about this!"

### Neutral (Default)
- Professional but approachable
- Some contractions OK
- Clear and direct
- Warm but not overly casual
- Example: "I'd be happy to discuss this further."

## Multi-Email Thread Handling

With `--thread` flag, parse multiple emails:

1. **Identify chronological order**
2. **Extract key points** from each email
3. **Track evolving context**
4. **Summarize thread** before responding
5. **Address latest concerns** while acknowledging history

Example thread summary:
```
Thread context:
1. [Date 1] Sarah: Initial complaint about export feature
2. [Date 2] You: Offered workaround script
3. [Date 3] Sarah: Script didn't work, deadline passed, escalating

Current status: Customer frustrated, deadline missed, needs resolution + compensation discussion
```

## Error Handling

**No email content**:
```
❌ Error: No email content provided

Usage: /draft-reply <email-file-or-content> [options]

Examples:
  /draft-reply emails/customer-complaint.txt
  /draft-reply "Email content here..."
```

**File not found**:
```
❌ Error: File not found: [path]

Please check the file path and try again.
```

**No BCC configured**:
```
⚠️  Warning: No BCC address configured

Set default BCC in .claude/settings.json:
{
  "emailConfig": {
    "defaultBcc": "crm@yourcompany.com"
  }
}

Or use --bcc flag: /draft-reply email.txt --bcc=crm@company.com
```

## Output Files

All drafts saved to `artifacts/email-drafts/` directory:

```
artifacts/email-drafts/
├── draft-reply-2025-01-15-143022.txt
├── draft-reply-2025-01-15-150433.txt
└── metadata.json
```

Metadata includes:
- Original email reference
- Timestamp
- Options used (tone, BCC, etc.)
- Solution count
- Salesforce integration status

## Integration with /add-to-salesforce

The `/add-to-salesforce` command (separate) accepts:
- Record type (opportunity, contact, account)
- Details (name, subject, amount, etc.)
- Email file reference
- Auto-populates fields from email content

Example:
```bash
/add-to-salesforce opportunity "TechCorp Partnership - API Integration" --email-file=artifacts/email-drafts/draft-reply-2025-01-15-143022.txt --amount=50000 --stage="Qualification"
```

## Best Practices

1. **Always empathize first** - Build rapport before solutions
2. **Divergent options** - Don't offer 3 variations of the same thing
3. **Clear trade-offs** - Help them make informed decisions
4. **Specific CTAs** - Don't be vague ("let's talk" → "30-min call Tuesday?")
5. **Own next steps** - Make it easy for them to say yes
6. **Match tone** - Formal with executives, casual with peers
7. **Be concise** - Respect their time, use bullets
8. **BCC consistently** - Build your CRM data

## Delivery/Prototype Email Format

For prototype delivery or technical artifact emails, use this MUCH SHORTER format:

**Structure (max 45 lines total):**
1. **Opening** (2-3 lines): What's attached, engagement reference
2. **What it does** (3-4 lines): Core value prop, key metrics
3. **Package contents** (5-7 bullets): What's included
4. **Key capabilities** (4-5 bullets): Main features
5. **Quick start** (3-5 lines): Basic setup commands
6. **Next steps** (3 bullets): Concrete actions
7. **Production considerations** (2-3 lines): Requirements + estimate
8. **Closing** (1 line): Availability statement
9. **Signature** (3 lines)

**Key principles for delivery emails:**
- NO long paragraphs - use bullets and headers
- NO detailed explanations - link to docs instead
- NO multiple solution options - it's a delivery, not a proposal
- Focus on "what" and "how to use", not "why"
- Target 40-50 lines max (vs 200+ for consultative emails)
- Use markdown formatting (**, ###, -, ```)

**Example delivery email:**
```
Subject: [Artifact Name] - Prototype Delivery

Dear [Customer] Team,

Attached is the [artifact name] prototype ([filename].zip, [size]MB) from our [month] [year] engagement.

**What it does:**
[1-2 sentence value prop with key metric]

**Package contents:**
- [Item 1]
- [Item 2]
- [Item 3]
- [Documentation]
- [Tests/demos]

**Key capabilities:**
- [Feature 1]
- [Feature 2]
- [Feature 3]
- [Feature 4]

**Quick start:**
```bash
[setup commands]
```

**Next steps:**
1. [Action 1]
2. [Action 2]
3. [Optional: schedule walkthrough]

**Production considerations:**
[Brief requirements]. Estimated [timeline], [budget].

Available for questions on [topic 1], [topic 2], or [topic 3].

Best regards,
[Name]
[Title]
```

## Implementation Notes

1. **Create artifacts/email-drafts/ directory** if it doesn't exist
2. **Parse email headers** carefully (From, To, Subject, Date)
3. **Detect urgency** keywords (deadline, urgent, ASAP, critical)
4. **Use timestamps** in filenames (ISO 8601 format)
5. **Validate email addresses** in BCC config
6. **Smart defaults** - Infer tone from input if possible
7. **Preserve context** - Include original email reference in draft

## Configuration

Add to `.claude/settings.json`:

```json
{
  "emailConfig": {
    "defaultBcc": "crm@yourcompany.com",
    "crmSystem": "salesforce",
    "defaultTone": "neutral",
    "solutionCount": 3,
    "autoArchive": true,
    "calendarLink": "https://calendly.com/yourname"
  }
}
```

---

**Philosophy**: Great email responses show empathy, provide options, and make it easy to move forward. This command helps you respond thoughtfully and consistently while building your CRM data.
