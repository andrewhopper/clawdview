---
name: plan-project
description: Create Commander's Intent and Work Back Plan for any project. Activate when user says "I want to build", "I want to launch", "I'm planning to", "help me plan", or describes a new project/goal. CRITICAL - NEVER infers requirements without explicit user approval.
version: 1.1.0
uuid: 3aa4eb0a-41ee-41ca-ae69-a98d10c047bd
---

# Plan Project - Universal Planning Framework

**Automatically activated when user describes a new project or goal.**

This skill guides users through creating a Commander's Intent and Work Back Plan for any project using military-derived planning patterns.

## Trigger Phrases

This skill activates when the user says:
- "I want to build [project]"
- "I want to launch [project]"
- "I'm planning to [goal]"
- "help me plan [project]"
- "I need to organize [event]"
- "I'm thinking about [project]"
- "I want to create [thing]"

## Pattern Overview

Uses two complementary patterns:

**Commander's Intent** - Defines WHAT and WHY
- Purpose: The "why" behind the project
- Key Tasks: Critical outcomes that must be achieved
- End State: Observable success criteria
- Constraints: Boundaries and limits
- Decision Authority: What can be decided autonomously vs. requires approval

**Work Back Plan** - Defines WHEN and HOW
- End State: Target completion date/time
- Milestones: Working backward from end to start
- Critical Path: Longest chain of dependencies
- Risks: What could go wrong at each milestone
- Slack Buffer: Time cushion for unexpected delays

## ⚠️ CRITICAL RULE: NO INFERENCE WITHOUT APPROVAL

**NEVER infer, assume, or guess requirements.**

**ALWAYS:**
- ✅ Ask explicit questions and wait for answers
- ✅ Present options and let user choose
- ✅ Confirm every section before moving to next
- ✅ Show what you're about to write and get approval

**NEVER:**
- ❌ Assume technical choices (frameworks, platforms, tools)
- ❌ Infer constraints that weren't stated
- ❌ Fill in blanks with "reasonable" assumptions
- ❌ Skip questions because answer "seems obvious"

**Example - WRONG:**
```
User: "I want to build a blog"
AI: [Creates intent with "Must use React, Must deploy to Vercel"]
    ^^^ VIOLATION - Never inferred these requirements
```

**Example - CORRECT:**
```
User: "I want to build a blog"
AI: "What platform or technology were you thinking of using?
     [1] Static site (Hugo, Jekyll)
     [2] Modern framework (React, Next.js)
     [3] CMS (WordPress, Ghost)
     [4] Not sure yet / doesn't matter"
```

**When in doubt:** ASK. Never assume.

## Execution Flow

### Phase 1: Understand the Project

**CRITICAL: Ask explicit questions. NEVER assume or infer answers.**

Ask clarifying questions (ONE at a time, WAIT for answer before next):

1. **What are you building/planning?**
   - Get explicit description from user
   - DO NOT assume scope, scale, or technical details
   - If vague, ask follow-up: "Can you describe it in more detail?"

2. **Why are you doing this?**
   - Get explicit purpose from user
   - DO NOT infer motivation
   - If unclear, ask: "What problem does this solve?" or "What's your goal?"

3. **What does success look like?**
   - Get explicit end state from user
   - DO NOT assume success criteria
   - If vague, ask: "How will you know you're 100% done?"

4. **Do you have a deadline?**
   - Get explicit date OR explicit "no deadline"
   - DO NOT assume urgency
   - If YES → Ask: "What's the target date?"
   - If NO → Will create Commander's Intent only

5. **Are there any constraints I should know about?**
   - Get explicit constraints from user
   - DO NOT assume budget, platform, technology, or limitations
   - If unsure, ask specific follow-ups (see Phase 2, Step 2.4)

### Phase 2: Build Commander's Intent

#### Step 2.1: Purpose (The "Why")
```
Based on what you've told me, here's the PURPOSE:

"[One sentence describing the overarching reason]"

Does this capture your 'why'? [Y/n/edit]
```

#### Step 2.2: Key Tasks (The "What")
Ask: "What are the 3-5 critical things that MUST happen for this to succeed?"

Listen for outcomes, not implementations:
- ❌ "Build React frontend" → ✅ "Users can interact via web interface"
- ❌ "Set up database" → ✅ "Data persists reliably across sessions"
- ❌ "Deploy to AWS" → ✅ "System is accessible to target users"

**For each key task, ask: "How will you know this task is complete? What's the expected result or measurable outcome?"**

```
KEY TASKS:

KT-1: [Outcome 1]
Expected Result: [How to verify completion]

KT-2: [Outcome 2]
Expected Result: [How to verify completion]

KT-3: [Outcome 3]
Expected Result: [How to verify completion]

KT-4: [Outcome 4] (if applicable)
Expected Result: [How to verify completion]

KT-5: [Outcome 5] (if applicable)
Expected Result: [How to verify completion]

These are the critical outcomes. Sound right? [Y/n/edit]
```

#### Step 2.3: End State (The "Done")
Ask: "How will you know you're 100% done? What should exist? What should NOT exist?"

```
END STATE:

ES-1: [Observable condition 1]

ES-2: [Observable condition 2]

ES-3: [Observable condition 3]

ES-4: [What should NOT exist]

This describes 'done'? [Y/n/edit]
```

#### Step 2.4: Constraints (The "Boundaries")

**CRITICAL: Ask explicit questions. DO NOT assume ANY constraints.**

Ask ONE question at a time, WAIT for answer:

**Proscriptive (Must Do):**
"Are there things you MUST include or MUST use?"
- If user says "no" or "not sure" → Record as "None specified"
- If user mentions technology → Ask: "Any specific version or requirement?"
- DO NOT fill in with "reasonable defaults"
- Examples from user: "Must use existing hosting", "Must support mobile", "Must be free"

**Prohibitive (Cannot Do):**
"Are there things you absolutely CANNOT do?"
- If user says "no" or "not sure" → Record as "None specified"
- DO NOT infer restrictions based on project type
- Ask: "Any budget limits, platform restrictions, or forbidden approaches?"
- Examples from user: "Cannot exceed $X budget", "Cannot require signup", "Cannot store PII"

**Resource:**
"What are your budget, time, and resource limits?"
- Ask explicitly: "What's your budget? (or is it flexible/unlimited?)"
- Ask explicitly: "Are you working solo or with a team?"
- Ask explicitly: "How much time can you dedicate per week?"
- DO NOT assume "solo" or "evenings/weekends"
- If user says "flexible" → Record exactly that, don't convert to a number

**Temporal:**
"Are there time constraints beyond the deadline?"
- Ask: "Any blackout dates, seasonal requirements, or competitive pressures?"
- If user says "no" → Record as "None specified"
- DO NOT infer urgency or competitive pressure

```
CONSTRAINTS:
Proscriptive (Must Do):
- [Exactly what user said, or "None specified"]
- [User's requirement 2, if provided]

Prohibitive (Cannot Do):
- [Exactly what user said, or "None specified"]
- [User's restriction 2, if provided]

Resource:
- Budget: [User's answer - "flexible", "$X", "unlimited", etc.]
- Team: [User's answer - "solo", "2 people", "TBD", etc.]
- Infrastructure: [User's answer or "Not specified"]

Temporal:
- [Exactly what user said, or "None beyond deadline"]

⚠️ These are ONLY the constraints YOU stated. Nothing assumed.

Are these correct? [Y/n/edit]
```

#### Step 2.5: Decision Authority

Ask: "What decisions can you make yourself vs. need approval/help?"

```
DECISION AUTHORITY:
Autonomous (You decide):
- [Decision type 1]
- [Decision type 2]

Requires Approval/Help:
- [Decision type 1]
- [Decision type 2]

This splits decision-making correctly? [Y/n/edit]
```

### Phase 3: Create Work Back Plan (If Deadline Exists)

If user has a deadline, work backward from it.

#### Step 3.1: Confirm End State & Date
```
END STATE: [from Commander's Intent]
TARGET DATE: [user's deadline]

Let's work backward from this date to figure out when to start.
Ready? [Y/n]
```

#### Step 3.2: Identify Major Milestones

Ask: "What are the major phases or checkpoints between now and done?"

Guide them to think backward:
- "Right before launch, what must be complete?"
- "Before that milestone, what's needed?"
- "Keep going backward... what's the first step?"

```
Working backward from [DATE]:

M[N]: [Final milestone] ([DATE])
M[N-1]: [Previous milestone] ([DATE - duration])
M[N-2]: [Previous milestone] ([DATE - duration])
...
M1: [First milestone] ([Start date])

Total duration: [X weeks/months]

Does this sequence make sense? [Y/n/edit]
```

#### Step 3.3: Identify Risks

For each major milestone, ask: "What could go wrong here?"

```
RISKS:
M[N]: [Milestone name]
  - Risk: [What could fail]
    Probability: [low/medium/high]
    Impact: [low/medium/high]
    Mitigation: [How to prevent]
    Contingency: [What to do if it happens]

Should we add more risks? [Y/n]
```

#### Step 3.4: Calculate Buffer

```
TIMELINE ANALYSIS:
Total time available: [weeks/months]
Critical path duration: [weeks/months]
Available buffer: [difference]

Recommended buffer allocation:
- [Risky milestone]: +[X days]
- [Complex milestone]: +[X days]

This leaves [X days] unallocated buffer for unknowns.

Looks reasonable? [Y/n/edit]
```

### Phase 4: Final Validation

**BEFORE generating documents, show complete summary and get approval:**

```
==============================================================
FINAL REVIEW - Please confirm before I generate documents
==============================================================

Commander's Intent:
  Purpose: [exact wording]
  Key Tasks: [list all]
  End State: [list all]
  Constraints: [list all, including "None specified"]
  Decision Authority: [list all]

Work Back Plan: [if applicable]
  Target Date: [date]
  Milestones: [count]
  Start Date: [calculated]
  Buffer: [days]

This is what will be written to the files.

Is everything correct? [Y/n/edit]

If you say 'edit', I'll ask what needs to change.
==============================================================
```

**ONLY proceed to document generation after user confirms "Y".**

If user says "n" or "edit":
- Ask: "What would you like to change?"
- Go back to specific section
- Re-confirm after changes

### Phase 5: Generate Documents

Create two files in current directory ONLY AFTER user approval:

**File 1: `intent-doc.md`**
```markdown
# Commander's Intent: [Project Name]

**Created:** [Date]
**Status:** Planning

## Purpose
[One sentence - the "why"]

## Key Tasks

**KT-1:** [Critical outcome 1]
Expected Result: [How to verify completion]

**KT-2:** [Critical outcome 2]
Expected Result: [How to verify completion]

**KT-3:** [Critical outcome 3]
Expected Result: [How to verify completion]

**KT-4:** [Critical outcome 4]
Expected Result: [How to verify completion]

**KT-5:** [Critical outcome 5]
Expected Result: [How to verify completion]

## End State

**ES-1:** [Observable condition 1]

**ES-2:** [Observable condition 2]

**ES-3:** [Observable condition 3]

**ES-4:** [What should NOT exist]

## Constraints

### Proscriptive (Must Do)
- [Required element 1]
- [Required element 2]

### Prohibitive (Cannot Do)
- [Forbidden action 1]
- [Forbidden action 2]

### Resource
- Budget: [amount]
- Team: [size/composition]
- Infrastructure: [constraints]

### Temporal
- [Time constraint 1]
- [Time constraint 2]

## Decision Authority

### Autonomous (You Decide)
- [Decision type 1]
- [Decision type 2]

### Requires Approval/Help
- [Decision type 1]
- [Decision type 2]

---

**Pattern Source:** `hmode/docs/patterns/COMMANDER_INTENT.md`
```

**File 2: `work-back-plan.md` (if deadline exists)**
```markdown
# Work Back Plan: [Project Name]

**Created:** [Date]
**Target Date:** [Deadline]
**Status:** Planning

## End State
[Copy from Commander's Intent]

## Critical Path

### M[N]: [Final Milestone]
- **Target Date:** [DATE]
- **Duration:** [time]
- **Dependencies:** [M[N-1]]
- **Owner:** [Who]
- **Description:** [What must be true]

### M[N-1]: [Previous Milestone]
- **Target Date:** [DATE]
- **Duration:** [time]
- **Dependencies:** [M[N-2]]
- **Owner:** [Who]
- **Potential Issues:**
  - Issue: [What could fail]
    - Probability: [low/medium/high]
    - Impact: [low/medium/high]
    - Mitigation: [Prevention plan]
    - Contingency: [If it happens]

[... repeat for all milestones ...]

### M1: [First Milestone]
- **Target Date:** [START DATE]
- **Duration:** 0d
- **Description:** [Initial step]

## Timeline Summary

- **Total Duration:** [X weeks/months]
- **Critical Path:** [X weeks/months]
- **Buffer Available:** [X days/weeks]
- **Start Date Needed:** [DATE]

## Risk Summary

| Risk | Probability | Impact | Score | Mitigation |
|------|-------------|--------|-------|------------|
| [Risk 1] | [P] | [I] | [P×I] | [Action] |
| [Risk 2] | [P] | [I] | [P×I] | [Action] |

## Buffer Allocation

- M[X]: +[Y days] (reason: [high risk/complexity])
- M[Z]: +[Y days] (reason: [external dependencies])
- Unallocated: [Y days] (for unknowns)

---

**Pattern Source:** `hmode/docs/patterns/WORK_BACK_PLAN.md`
```

### Phase 6: Next Steps

After generating documents:

```
✅ Planning documents created:
   - intent-doc.md
   - work-back-plan.md (if applicable)

NEXT STEPS:

[1] Review and refine the documents
[2] Share with team/collaborators/contractors
[3] Start executing the first milestone
[4] Track progress by marking milestones complete

Want me to help with any of these? [1-4/n]
```

## Example Workflows

### Example 1: Personal Portfolio Blog

```
User: "I want to launch a personal portfolio blog"

AI: Great! Let's create a plan for your portfolio blog.

What's your main reason for creating this blog?
(e.g., showcase work, attract clients, share knowledge, build audience)

User: "showcase my work and attract potential clients"

AI: Perfect. What does success look like for this blog?

User: "People can see my projects, read about my skills, and contact me easily"

AI: Do you have a deadline for launching this?

User: "I want it live in 3 weeks"

AI: Got it. Here's your PURPOSE:

"Showcase professional work to attract potential clients"

Sound good? [Y/n]

User: Y

AI: What are the 3-5 critical things that MUST happen for this to succeed?

User: "Need a nice looking site, portfolio examples, contact form, and it needs to be fast"

AI: Let me convert those to outcomes:

KEY TASKS:
1. Site presents professional, polished first impression
2. Visitors can view portfolio examples with descriptions
3. Potential clients can easily contact you
4. Site loads quickly on all devices

Sound right? [Y/n]

User: Y

AI: How will you know you're 100% done?

User: "Site is live, all my projects are shown, contact form works, looks good on mobile"

AI: END STATE:
- Portfolio site is publicly accessible
- At least 5 projects displayed with descriptions
- Contact form successfully delivers messages
- Site loads in <3 seconds on mobile
- Zero broken links or images

This describes 'done'? [Y/n]

User: Y

AI: Are there things you MUST use or MUST include?

User: "It has to be free hosting, and I want to use a static site generator"

AI: Are there things you absolutely CANNOT do?

User: "Can't spend money, can't use a CMS that requires maintenance"

AI: What's your time/resource situation?

User: "Just me, working evenings and weekends"

AI: CONSTRAINTS:

Proscriptive (Must Do):
- Must use free hosting platform
- Must use static site generator

Prohibitive (Cannot Do):
- Cannot incur hosting costs
- Cannot use platforms requiring ongoing maintenance

Resource:
- Budget: $0
- Team: Solo (evenings/weekends only)
- Infrastructure: Must use free tier services

Temporal:
- Must launch within 3 weeks

These are your boundaries? [Y/n]

User: Y

AI: What decisions can you make yourself vs. need help with?

User: "I can pick colors and layout myself, but might need help with deployment"

AI: DECISION AUTHORITY:

Autonomous (You Decide):
- Design choices (colors, fonts, layout)
- Content and project descriptions
- Portfolio project selection

Requires Approval/Help:
- Hosting platform selection
- Deployment configuration
- Domain name setup

This splits decision-making correctly? [Y/n]

User: Y

AI: Perfect! Now let's work backward from your 3-week deadline...

END STATE: Portfolio site publicly accessible
TARGET DATE: 2025-03-05

What are the major phases between now and launch?

User: "Design the site, build it, add content, deploy"

AI: Working backward from Mar 5:

M4: Site Live (Mar 5)
M3: Content Added (Mar 3) - 2 days before
M2: Site Built (Feb 28) - 3 days before that
M1: Design Finalized (Feb 23) - 5 days before that

Total: 10 days of work
Start needed: Feb 23 (2 weeks from now)

Does this sequence make sense? [Y/n]

User: Y

AI: What could go wrong at each phase?

User: "Deployment might be tricky, and writing project descriptions takes longer than expected"

AI: RISKS:

M3: Content Added
  - Risk: Writing descriptions takes longer than planned
    Probability: medium
    Impact: medium
    Mitigation: Start drafting descriptions now
    Contingency: Launch with 3 projects, add more later

M4: Site Live
  - Risk: Deployment issues with free hosting
    Probability: medium
    Impact: high
    Mitigation: Test deployment early with dummy site
    Contingency: Have 2 backup hosting options ready

TIMELINE ANALYSIS:
Total time available: 21 days (3 weeks)
Critical path duration: 10 days
Available buffer: 11 days

Recommended buffer allocation:
- M2 (Build): +2 days (technical complexity)
- M3 (Content): +3 days (high risk)
- M4 (Deploy): +2 days (high impact)

This leaves 4 days unallocated buffer.

Looks reasonable? [Y/n]

User: Y

AI: ✅ Planning documents created:
   - intent-doc.md
   - work-back-plan.md

NEXT STEPS:

[1] Review documents and refine
[2] Start designing (M1 begins Feb 23)
[3] Test deployment early to reduce M4 risk
[4] Start drafting project descriptions now

Want help with any of these? [1-4/n]
```

### Example 2: Voice Notes App

```
User: "I want to build a voice notes app"

AI: Excellent! Let's plan your voice notes app.

What's your main motivation for building this?

User: "I want to capture ideas quickly while walking or driving"

AI: Perfect. What does success look like for this app?

User: "I can record a voice note hands-free, it transcribes it, and I can search my notes later"

AI: Do you have a deadline?

User: "Not really, just want it working eventually"

AI: Got it - we'll create Commander's Intent only then.

Here's your PURPOSE:

"Enable hands-free idea capture during activities"

Sound good? [Y/n]

User: Y

AI: What are the 3-5 critical things that MUST happen for this to succeed?

User: "Record audio easily, transcribe accurately, search works, syncs across devices"

AI: KEY TASKS:
1. Users can record audio with minimal interaction
2. Audio is transcribed accurately to text
3. Users can search notes by content
4. Notes sync reliably across devices

Sound right? [Y/n]

User: Y

AI: How will you know you're 100% done?

User: "I can record a note while driving, find it later on my computer, search for keywords"

AI: END STATE:
- Audio recording works hands-free (voice activation)
- Transcription accuracy exceeds 90%
- Full-text search returns relevant notes
- Notes available on all user devices within 30 seconds
- Zero data loss during sync

This describes 'done'? [Y/n]

User: Y

AI: Are there things you MUST use or MUST include?

User: "Has to work on iPhone first, needs to be private - no cloud services reading my notes"

AI: Are there things you absolutely CANNOT do?

User: "Can't send audio to third-party services for transcription, can't require internet connection for basic recording"

AI: What's your budget and time situation?

User: "Can spend maybe $100, working on it solo in my spare time"

AI: CONSTRAINTS:

Proscriptive (Must Do):
- Must work on iPhone platform first
- Must keep audio/transcripts private
- Must function offline for recording

Prohibitive (Cannot Do):
- Cannot use third-party transcription services
- Cannot require internet connection for core functionality
- Cannot share data with external services

Resource:
- Budget: $100 maximum
- Team: Solo developer
- Time: Spare time only

This captures your boundaries? [Y/n]

User: Y

AI: What decisions can you make yourself vs. need help/approval with?

User: "I can decide UI and features, might need help picking the transcription model"

AI: DECISION AUTHORITY:

Autonomous (You Decide):
- User interface design
- Feature prioritization
- Recording format and quality settings

Requires Approval/Help:
- Speech-to-text model selection
- On-device ML implementation approach
- Sync architecture design

This splits decision-making correctly? [Y/n]

User: Y

AI: ✅ Planning document created:
   - intent-doc.md

NEXT STEPS:

[1] Research on-device transcription options (CoreML, WhisperKit)
[2] Create UI mockups for recording flow
[3] Prototype basic recording functionality
[4] Would you like to add a Work Back Plan when you have a deadline?

Want help with any of these? [1-4/n]
```

### Example 3: Audio-First Personal Assistant

```
User: "I want to build an audio first personal assistant"

AI: Interesting! Let's plan your audio-first assistant.

What's the main problem you're trying to solve?

User: "I want to talk to my computer naturally instead of typing commands"

AI: What does success look like for this assistant?

User: "I can speak to it, it understands context, executes tasks, and responds with voice"

AI: Do you have a target launch date?

User: "I want a working prototype in 2 months"

AI: Great! Here's your PURPOSE:

"Enable natural voice interaction with computer systems"

Sound good? [Y/n]

User: Y

AI: What are the 3-5 critical things that MUST happen for this to succeed?

User: "Voice recognition works well, understands commands in context, executes actions on my computer, responds naturally"

AI: KEY TASKS:
1. Users can speak naturally and be understood accurately
2. System interprets commands with contextual awareness
3. System executes actions on user's computer
4. System responds via natural-sounding voice

Sound right? [Y/n]

User: Y

AI: How will you know you're 100% done with the prototype?

User: "I can ask it to open apps, summarize emails, set reminders, and it does all that via voice"

AI: END STATE:
- Voice recognition accuracy >95% in quiet environment
- Assistant executes at least 10 command types
- Responses sound natural (not robotic)
- System maintains conversation context
- Works with existing desktop applications

This describes 'done'? [Y/n]

User: Y

AI: Are there things you MUST use or MUST include?

User: "Has to work offline for privacy, needs to run on Mac, should use modern LLM for intelligence"

AI: Are there things you absolutely CANNOT do?

User: "Can't send voice to cloud, can't require internet, can't cost more than $200 total"

AI: What's your resource situation?

User: "Just me, have about 15 hours per week to work on it"

AI: CONSTRAINTS:

Proscriptive (Must Do):
- Must function completely offline
- Must run on macOS
- Must use modern LLM for understanding

Prohibitive (Cannot Do):
- Cannot transmit voice data to cloud services
- Cannot require internet connection
- Cannot exceed $200 total cost

Resource:
- Budget: $200 maximum
- Team: Solo (15 hours/week)
- Platform: macOS only (for now)

Temporal:
- Prototype complete within 2 months

These are your boundaries? [Y/n]

User: Y

AI: What can you decide yourself vs. need help with?

User: "I can decide features and UI, but need help choosing the local LLM and voice models"

AI: DECISION AUTHORITY:

Autonomous (You Decide):
- Feature set and prioritization
- User interface design
- Command syntax and patterns

Requires Approval/Help:
- Local LLM selection (Ollama, LM Studio, etc.)
- Speech-to-text model choice
- Text-to-speech system selection

This splits decision-making correctly? [Y/n]

User: Y

AI: Perfect! Now let's work backward from your 2-month deadline...

END STATE: Working prototype with 10+ command types
TARGET DATE: 2025-04-12 (2 months from today)

What are the major phases between now and done?

User: "Research models, build voice pipeline, integrate LLM, add commands, test"

AI: Working backward from Apr 12:

M6: Prototype Complete (Apr 12)
M5: Testing & Refinement (Apr 5) - 1 week before
M4: Command Integration (Mar 22) - 2 weeks before
M3: LLM Integration (Mar 8) - 2 weeks before
M2: Voice Pipeline (Feb 23) - 2 weeks before
M1: Model Selection (Feb 16) - 1 week before

Total: 8 weeks work
Start: Feb 16 (now)

Does this sequence make sense? [Y/n]

User: Y

AI: What could go wrong at each phase?

User: "Local LLM might be too slow, voice recognition might not work well, integrating everything might be harder than expected"

AI: RISKS:

M2: Voice Pipeline
  - Risk: Speech-to-text accuracy insufficient
    Probability: medium
    Impact: critical
    Mitigation: Test 3 different models in week 1
    Contingency: Adjust requirements to 85% accuracy

M3: LLM Integration
  - Risk: Local LLM too slow for real-time responses
    Probability: high
    Impact: high
    Mitigation: Benchmark performance requirements early
    Contingency: Use smaller/faster model, reduce context window

M4: Command Integration
  - Risk: System integration more complex than expected
    Probability: medium
    Impact: medium
    Mitigation: Start with 3 simple commands to prove pattern
    Contingency: Reduce scope to 5 commands instead of 10

TIMELINE ANALYSIS:
Total time available: 8 weeks
Critical path duration: 8 weeks
Available buffer: 0 weeks (tight!)

Recommendation: Start immediately, allocate 2 extra weeks buffer by moving deadline to Apr 26

Accept new deadline? [Y/n/keep original]

User: Y

AI: Updated target: Apr 26 (gives you 2-week buffer)

Buffer allocation:
- M3 (LLM): +1 week (high risk)
- M4 (Commands): +1 week (complexity)

✅ Planning documents created:
   - intent-doc.md
   - work-back-plan.md

NEXT STEPS:

[1] Start model research THIS WEEK (M1)
[2] Test 3 speech-to-text options for accuracy
[3] Benchmark 3 local LLMs for speed
[4] Create proof-of-concept with 1 command

Want help with any of these? [1-4/n]
```

## Implementation Notes

### Conversation Style

- Ask **ONE question at a time** (never batch questions)
- **NEVER infer or assume requirements** - always ask explicitly
- Use outcome-based language ("users can X" not "build feature Y")
- Validate each section before moving to next
- Offer examples when user seems stuck, but let THEM choose
- Keep responses concise and focused
- If answer is vague, ask follow-up - don't fill in blanks
- Record "None specified" or "Flexible" rather than inventing constraints
- Show final summary and get explicit approval before generating files

### Document Naming

- `intent-doc.md` - Always this name
- `work-back-plan.md` - Always this name (if deadline exists)
- Save in current working directory
- Include creation date and status in frontmatter

### Follow-Up Actions

After creating documents, offer:
1. Review/refinement assistance
2. Help starting first milestone
3. Guidance on risk mitigation
4. Suggestions for tools/approaches

### Integration with SDLC

If this is a new software project:
- Commander's Intent becomes Phase 1 (SEED) input
- Work Back Plan informs Phase 6 (Design) timeline
- Constraints feed into Phase 6 tech stack decisions
- Can reference: `hmode/docs/patterns/COMMANDER_INTENT.md`
- Can reference: `hmode/docs/patterns/WORK_BACK_PLAN.md`

### Universal Applicability

This skill works for:
- Software projects (apps, websites, tools)
- Personal projects (blogs, portfolios, side businesses)
- Events (conferences, weddings, launches)
- Creative work (books, courses, content)
- Life goals (fitness, learning, career)

The patterns are domain-agnostic - focus on outcomes, not implementations.

## Technical Details

### Pattern Sources

- Commander's Intent: `hmode/docs/patterns/COMMANDER_INTENT.md`
- Work Back Plan: `hmode/docs/patterns/WORK_BACK_PLAN.md`

### File Format

Both documents are Markdown with YAML-style sections for easy parsing and editing.

### State Management

Track conversation state:
- Current phase (1-5)
- Current section being built
- Pending confirmations
- User's answers

### Validation

Before generating documents:
- ✅ Verify all required sections completed
- ✅ Check for outcome-based language in Key Tasks
- ✅ Ensure End State is observable
- ✅ Validate timeline logic in WBP
- ✅ **Confirm NO inferred requirements** - everything came from user
- ✅ Review constraints section for "None specified" if user didn't provide
- ✅ Show complete summary and get explicit "Y" approval
- ⚠️ **If anything was assumed - STOP and ask user first**

## Summary

This skill transforms casual project ideas into structured, actionable plans using military-grade planning frameworks:

1. **Commander's Intent** - Clear mission with boundaries
2. **Work Back Plan** - Realistic timeline with risk awareness

The combination gives users:
- Clarity on what they're building and why
- Concrete success criteria
- Realistic timeline (if deadline exists)
- Risk awareness before starting
- Decision boundaries for delegation

Perfect for anyone starting a new project who wants to plan properly before diving into execution.
