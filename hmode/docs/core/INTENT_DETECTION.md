## 🎯 INTENT DETECTION & TRIAGE

**Purpose:** Classify requests and determine approval level based on time, effort, and scale.

<<<<<<< HEAD
---

## ⚡ SKILL INVOCATION (PRIORITY CHECK)

**Rule:** Check for skill invocation BEFORE all other intent detection.

### Detection Order
```
1. Slash Command Detection (/skill-name)
2. RLHF Sentiment Detection (WTF/nice)
3. Standard Intent Classification (below)
```

### Slash Command Pattern
**Pattern:** `/[a-z-]+` at start of message

**Action:** IMMEDIATELY invoke Skill tool
```
User: "/error" → Skill("error")
User: "/commit" → Skill("commit")
User: "/diagram" → Skill("diagram")
```

**NO explanation before invocation. Skills handle their own workflow.**

### RLHF Sentiment Detection

**Negative Sentiment (→ Error Tracking):**
```
Keywords: "WTF", "wtf", "that was wrong", "that's wrong",
          "error" (in feedback context), "fail", "failed"

Context: User expressing frustration about AI's previous action

Action: Skill("track-errors") → then address the issue
```

**Positive Sentiment (→ Reward Tracking):**
```
Keywords: "nice", "great work", "perfect", "good job",
          "excellent", "well done", "thanks", "awesome"

Context: User praising AI's previous work

Action: Skill("nice") → then continue conversation
```

**Examples:**
```
User: "WTF that didn't work"
→ Invoke Skill("track-errors")
→ Then help fix the issue

User: "Nice job on that diagram"
→ Invoke Skill("nice")
→ Then respond: "What's next?"

User: "/push"
→ Invoke Skill("push")
→ Skill handles commit + push workflow
```

**See:** `hmode/docs/core/SKILL_INVOCATION.md` for comprehensive patterns

---

## 📢 MODE ANNOUNCEMENT (MANDATORY)

### Mode Announcement (MANDATORY)

**CRITICAL:** After classifying EVERY user request, you MUST announce the detected mode explicitly and verbosely. This is the FIRST thing in your response.

**Mode Announcement Format:**
```
═══════════════════════════════════════════════════════════
  ENTERING [MODE NAME] MODE
  [One-line description of what this mode does]
═══════════════════════════════════════════════════════════
```

**Available Modes:**

| Mode Name | Trigger | Description |
|-----------|---------|-------------|
| **BUG FIX** | "fix", "bug", "broken", "not working", "error" | Diagnosing and fixing existing issues |
| **NEW FEATURE** | "add", "implement", "create feature", "new capability" | Adding functionality to existing project |
| **NEW PROTOTYPE** | "new project", "build", "prototype", "new idea" | Starting a new project from scratch (Phase 1 SDLC) |
| **RESEARCH** | "research", "investigate", "explore", "compare" | Information gathering and analysis |
| **REFACTOR** | "refactor", "clean up", "restructure", "improve code" | Code quality improvements without behavior change |
| **ENHANCEMENT** | "improve", "optimize", "enhance", "better" | Making existing features better |
| **DOCUMENTATION** | "document", "docs", "readme", "explain in writing" | Creating or updating documentation |
| **QUESTION** | "what", "how", "why", "explain" | Information request, no action needed |
| **CHORE** | "rename", "move", "delete", "organize" | Routine maintenance tasks |
| **ARTIFACT GENERATION** | "create diagram", "generate report", "presentation" | Creating deliverables/assets |
| **CONFIGURATION** | "configure", "setup", "settings", "environment" | Setting up or modifying configuration |
| **TESTING** | "test", "write tests", "add tests", "coverage" | Creating or running tests |
| **DEPLOYMENT** | "deploy", "publish", "release", "ship" | Deploying code to production/staging |
| **SPIKE** | "spike", "experiment", "throwaway", "quick prototype" | Time-boxed exploratory code (max 3 days) |
| **UNDETERMINED** | Ambiguous request | Mode could not be determined - clarification needed |

**Mode Announcement Examples:**

```
═══════════════════════════════════════════════════════════
  ENTERING BUG FIX MODE
  Diagnosing and resolving issue in existing code
═══════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════
  ENTERING NEW PROTOTYPE MODE
  Starting Phase 1 SDLC for new project creation
═══════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════
  ENTERING RESEARCH MODE
  Gathering information and analyzing options
═══════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════
  MODE COULD NOT BE DETERMINED
  Your request is ambiguous - please clarify your intent
═══════════════════════════════════════════════════════════
```

**Undetermined Mode Response:**
When mode cannot be determined, present options:
```
═══════════════════════════════════════════════════════════
  MODE COULD NOT BE DETERMINED
  Your request is ambiguous - please clarify your intent
═══════════════════════════════════════════════════════════

I detected multiple possible intents. Which best describes what you want?

[1] BUG FIX - Fix something that's broken
[2] NEW FEATURE - Add new functionality
[3] NEW PROTOTYPE - Start a new project
[4] RESEARCH - Learn about something
[5] OTHER - Let me describe what I need

Please select [1-5]:
```

**Enforcement:**
- AI MUST announce mode BEFORE any other response content
- AI MUST use the exact format with equals signs border
- AI MUST include one-line description
- If confidence < 70%, announce UNDETERMINED and ask for clarification
- Mode announcement appears ONCE at the start, not repeated

---

## 🔍 REQUEST CLASSIFICATION

### Request Categories

```
IMPACT/SCALE MATRIX:

Low ←────────────────────────────────→ High
│
│  Question      Chore         Task
│  Brainstorm    Script        New Idea
│  Note          Artifact      New Project
│  Content Seed
│
Quick ←──── TIME/EFFORT ────→ Long
```

| Category | Description | Time | Scale Sensitivity | Approval Level |
|----------|-------------|------|-------------------|----------------|
| **Question** | Information request, clarification, status check | <1 min | None | None - Execute immediately |
| **Chore** | Routine maintenance, file ops, cleanup | 1-5 min | **High** (1 file vs 100 files) | Scale-dependent |
| **Task** | Work within existing project, bug fix, feature | 5-30 min | Medium (1-10 files typical) | Scale-dependent |
| **Brainstorm** | Ideation, exploration, options generation | 2-10 min | Low | Brief summary → execute |
| **Note** | Quick research note, reference capture | 2-5 min | Low | Execute → `notes/{topic-uuid}/` |
| **Content Seed** | Raw content ideas for future development | 5-15 min | Low | Execute → `content/seed/` |
| **New Script** | Slash command, automation, utility | 15-45 min | Low | **Confirm approach** |
| **New Artifact** | Document, diagram, presentation | 10-60 min | Medium | **Confirm format/scope** |
| **New Idea** | Phase 1 SEED creation | 30-90 min | N/A | **Confirm + Phase 1 protocol** |
| **New Project** | Full SDLC (Phases 1-9) | 2-5 days | N/A | **Confirm + SDLC protocol** |

### Scale-Based Approval Thresholds

**File Operations (Create, Edit, Delete, Move):**
```
1-5 files       → Execute immediately (mention count)
6-20 files      → Brief summary → execute
21-100 files    → Confirm with list of files
100+ files      → MUST confirm with rationale + count
```

**Code Generation:**
```
1-3 functions   → Execute immediately
4-10 functions  → Brief summary → execute
11+ functions   → Confirm approach + estimate
New module      → Confirm architecture
```

**Data Operations:**
```
1-100 records   → Execute immediately
101-10k records → Brief summary → execute
10k-1M records  → Confirm with time estimate
1M+ records     → MUST confirm + performance plan
```

**Directory Operations:**
```
1-2 dirs        → Execute immediately
3-10 dirs       → Brief summary → execute
11+ dirs        → Confirm with structure diagram
Recursive ops   → MUST confirm with depth + count
```

### Detection Signals

**Question:**
- Keywords: "what", "how", "why", "where", "when", "explain", "show me"
- No action verbs
- Read-only operations

**Chore:**
- Keywords: "rename", "move", "delete", "cleanup", "reorganize", "format"
- File/directory operations
- **Check scale:** 1 file vs 100 files

**Task:**
- Keywords: "fix", "update", "modify", "edit", "change", "refactor"
- Scoped to existing files/features
- **Check scale:** Single file vs multi-file

**Brainstorm:**
- Keywords: "ideas for", "what if", "explore", "options", "approaches"
- Multiple possibilities
- No implementation

**Note:**
- Keywords: "note", "capture", "reference", "research note", "save for later"
- Quick capture, not structured content
- Research findings, links, observations
- **Action:** Create in `notes/{topic-uuid}/`

**Content Seed:**
- Keywords: "content idea", "seed content", "raw idea", "future article", "concept to develop"
- Unstructured ideas for future development
- Multiple related concepts/bullet points
- Intended for later refinement through workflow
- **Action:** Create in `content/seed/`

**New Script:**
- Keywords: "create command", "new script", "automation for"
- New utility creation
- Reusable tool

**New Artifact:**
- Keywords: "generate", "create presentation", "diagram", "document"
- Deliverable creation
- One-time output

**New Idea:**
- Keywords: "new idea", "prototype idea", "project concept"
- Phase 1 SEED process
- Prototype exploration

**New Project:**
- Keywords: "build", "implement", "create prototype", "full project"
- End-to-end development
- Multi-phase SDLC

### Approval Workflows

**Execute Immediately (Low scale):**
```
User Request → Classify → Check scale → Execute → Report
Example: "Renaming 1 file: proto-014 → proto-014-xip"
```

**Brief Summary (Medium scale):**
```
User Request → Classify → Check scale → Summary → Execute
Example: "Updating 8 files with XIP tags. Proceeding."
```

**Confirm (High scale or complexity):**
```
User Request → Classify → Check scale → Present plan + time estimate → User confirms → Execute

Example:
"Detected: Generate 1,000 test files
Time estimate: 15-20 minutes
Disk space: ~50MB
Confirm to proceed?"
```

**Confirm + Protocol (New Idea/Project):**
```
User Request → Classify → Explain protocol + timeline → User confirms → Follow SDLC

Example:
"New project detected: Full SDLC prototype
Timeline: 2-5 days | 9-phase process
Will start with Phase 1 SEED.
Confirm to proceed?"
```

**Progressive Content Flow (Complex Artifacts):**
```
User Request → Detect complexity → Invoke /progressive-content → Stage-gated creation → User approves each stage

MUST USE for:
- Detailed presentations (>10 slides, complex content)
- Comprehensive written documents (>5 pages, high rigor)
- Complex flowcharts/diagrams (>10 nodes, multi-layer)
- Strategic documents (PRDs, 6-pagers, whitepapers)
- Technical specifications (detailed design docs)

Example:
User: "Create a detailed presentation about our AI architecture"
AI: "Complex artifact detected: Detailed presentation. Using /progressive-content workflow (6 stages with approval gates). Starting Stage 0 (Seeding)..."
```

**Detailed Plan Presentation (Complex Multi-Step Tasks):**
```
User Request → Analyze complexity → Generate step-by-step plan → Specify details → Present for approval → Execute

ALWAYS PRESENT PLAN for:
- Multi-step tasks (3+ distinct operations)
- Tasks requiring multiple tools/files
- Complex diagrams, visualizations, reports
- Data processing pipelines
- Multi-file refactors or migrations
- Anything requiring >15 minutes

Plan Format:
"Ok, here's my plan:
1. [Step 1 with specifics]
2. [Step 2 with specifics]
3. [Step 3 with specifics]
...

Btw, [implementation details: naming, formats, styling, standards]
[Final actions: commit, deploy, open, test]

any changes? y/n"

Examples:
User: "Create a schematic of the SDLC flow"
AI: "Ok, here's my plan:
1. Extract transitions and states from CLAUDE.md and sdlc/*.md files
2. Save these in a JSON file (sdlc_states.json)
3. Use JSON to render a Draw.io diagram
4. View the diagram and verify completeness

Btw, color scheme: AWS palette (from color_spec.md), file name: sdlc_2025-11-16.drawio, will generate PDF version too. I'll commit to git when done.

Look good? y/n/f                    f for feedback on the process"

User: "Refactor all the API endpoints to use the new error handling pattern"
AI: "Ok, here's my plan:
1. Identify all API endpoint files (grep for @app.route or similar)
2. Create shared error handler middleware
3. Update each endpoint to use new pattern (try/catch → middleware)
4. Update tests to match new error responses
5. Run full test suite and fix any failures

Btw, affecting ~15 files, will follow error pattern from hmode/shared/standards/code/nodejs/errors.ts, preserve existing error codes. Commit when all tests pass.

Look good? y/n/f                    f for feedback on the process"

User: "Generate a comparison table of all the prototypes"
AI: "Ok, here's my plan:
1. Read all .project files from prototypes/ directory
2. Extract: name, status, phase, tech_stack, timeline
3. Sort by status (ACTIVE → COMPLETED → ARCHIVED)
4. Generate markdown table with columns: Name, Status, Phase, Tech Stack, Started, Updated
5. Save to project-management/PROTOTYPE_COMPARISON.md

Btw, will include 50+ prototypes, add filters for status/phase, use consistent date format (YYYY-MM-DD). No git commit (user should review first).

Look good? y/n/f                    f for feedback on the process"
```

**Technical Implementation Paraphrase (Comprehensive Tech Lead Review):**
```
User Request → Parse intent → Identify tech decisions → Paraphrase ALL critical details → User confirms → Execute

ALWAYS PARAPHRASE when adding:
- AI/ML integrations (model, provider, auth, features)
- Database changes (schema, ORM, migrations)
- API integrations (service, endpoints, auth)
- Framework additions (library, version, config)
- Infrastructure changes (deployment, hosting, resources)

Detail Level: Tech lead reviewing intern's proposal
- ALL critical technical specs (versions, credentials, locations, schemas)
- Apply /densify principles (concise but complete)
- Apply /kill-m-dash principles (no AI fluff, state directly)
- Include enough info to approve/reject without follow-up questions
- Include project names/IDs (Supabase project, AWS account, service names)

Format:
"Adding [component]:
- Tech: [library v.x.x, specific tools]
- Project: [Supabase project name/ID, AWS account, service identifier]
- Location: [where it runs/lives, specific region/instance]
- Auth: [credential method + storage]
- Schema: [tables/collections + key fields]
- Config: [critical settings, ports, limits]
- Integration: [how it connects to existing system]

Look good? y/n/f                    f for feedback on the process"

Examples:

User: "Add Bedrock integration"
AI: "Adding Bedrock integration:
- Model: claude-sonnet-4-5 via BAML (BoundaryML) client
- AWS Account: protoflow-prod (123456789012)
- Region: us-east-1 (global inference profile)
- Auth: IAM role (app assumes bedrock-inference-role), creds from AWS Secrets Manager
- Features: Prompt caching ON, streaming ON, max tokens 4096
- Cost: ~$3/M input, $15/M output with 90% cache hit
- Integration: FastAPI /api/chat endpoint, async handler
- Error handling: exponential backoff (3 retries), fallback to haiku on throttle

Look good? y/n/f                    f for feedback on the process"

User: "Add database support"
AI: "Adding postgres database:
- Stack: PostgreSQL 16.1 + Prisma ORM v5.x + pg_vector extension
- Instance: Local Docker (dev), RDS postgres-prod-01 (prod, us-east-1)
- AWS Account: protoflow-prod (123456789012)
- Credentials: .env (dev), AWS Secrets Manager bedrock-db-creds (prod), rotated 90d
- Schema: users, documents, embeddings tables
  - users: id (uuid), email (unique), created_at
  - documents: id, user_id (fk), content (text), vector (vector(1536))
  - embeddings: id, doc_id (fk), model (text), embedding (vector)
- Pooling: max 20 connections, timeout 30s
- Migrations: Prisma migrate, versioned in git
- Backups: RDS auto-backup daily, retention 7d
- Port: 5432, connection string in DATABASE_URL

Look good? y/n/f                    f for feedback on the process"

User: "Integrate Stripe"
AI: "Adding Stripe payments:
- SDK: stripe-node v14.12.0
- Account: protoflow (acct_xxx)
- Mode: Test keys (dev), live keys (prod) from .env
- Webhook: /api/stripe/webhook, signature verification required
- Events: payment_intent.succeeded, customer.subscription.updated
- Products: subscription (price_xxx monthly $49), one-time (price_yyy $299)
- Features: Customer portal, invoice emails, tax calculation (automatic)
- Error handling: idempotency keys, retry logic for network failures
- PCI: No card data stored, Stripe.js for client-side tokenization
- Integration: NextJS API routes, Supabase customer mapping

Look good? y/n/f                    f for feedback on the process"

User: "Add authentication"
AI: "Adding authentication:
- Provider: Supabase Auth + JWT
- Project: protoflow-prod (xyzabcdefghijklmnop)
- URL: https://xyzabcdefghijklmnop.supabase.co
- Methods: Email/password, OAuth (Google, GitHub, Microsoft)
- Session: JWT in httpOnly cookie, 7d expiry, refresh token rotation
- Storage: Supabase auth.users table, custom profiles in public.user_profiles
- Middleware: NextJS middleware validates JWT, rejects on /api/* + /dashboard/*
- Password: bcrypt hash, min 12 chars, complexity enforced
- MFA: TOTP (optional), QR code via qrcode npm package
- Rate limiting: 5 login attempts per 15min (IP-based), Redis tracking
- Email: Sender noreply@protoflow.com (Protoflow), SMTP via AWS SES (us-east-1)
- Integration: Supabase client initialized in lib/supabase.ts, env vars from .env.local

Look good? y/n/f                    f for feedback on the process"

User: "Set up DNS for the app"
AI: "Setting up DNS:
- Provider: Cloudflare DNS
- Account: protoflow (account_xxx)
- Zone: protoflow.com
- Records:
  - Apex: protoflow.com → A record 54.123.45.67 (ALB)
  - WWW: www.protoflow.com → CNAME protoflow.com
  - API: api.protoflow.com → A record 54.123.45.68 (ALB)
- SSL: Cloudflare Full (strict), auto-renew
- TTL: 300s (5min) for apex/www, 3600s (1h) for api
- Redirect: www → apex (301 permanent), enforce HTTPS
- Integration: Terraform managed, state in S3

Look good? y/n/f                    f for feedback on the process"
```

### Escalation Triggers

**MUST confirm when:**
- 20+ files affected
- 1M+ records processed
- Estimated time > 30 minutes
- Destructive operations (delete, major refactor)
- Ambiguous intent (2+ interpretations)
- Cross-project dependencies
- Phase transitions in SDLC
- Recursive directory operations
- Breaking changes to APIs/interfaces

**MUST present detailed plan when:**
- Multi-step tasks (3+ distinct operations)
- Complex diagrams, visualizations, reports
- Data processing pipelines
- Multi-file refactors (>3 files)
- Tasks requiring >15 minutes
- Multiple tools/technologies involved

**MUST use Progressive Content Flow when:**
- Complex artifacts (detailed presentations, comprehensive docs, complex diagrams)
- Strategic documents (>5 pages, high rigor)
- Multi-stage deliverables requiring user feedback

**MUST paraphrase with tech specifics when:**
- Adding AI/ML integrations
- Database changes or additions
- API integrations (external services)
- Framework/library additions
- Infrastructure changes
- Authentication/authorization implementations

**Auto-execute when:**
- 1-5 files, simple operations
- Read-only requests
- Single file edits
- Status checks
- Information retrieval
- Simple bug fixes (no architecture changes)

### Intent Detection Process

**Step 1: Classify** (category based on keywords/context)
**Step 2: Assess Scale** (count files, records, operations)
**Step 3: Estimate Time** (realistic time to complete)
**Step 4: Route** (approval workflow based on scale + complexity)
**Step 5: Execute or Confirm** (per thresholds)

**Examples:**

```
User: "What's the status of proto-015?"
→ Category: Question
→ Scale: 1 file read
→ Time: 10 seconds
→ Approval: None → Execute

User: "Rename proto-014 folder to include 'xip' tag"
→ Category: Chore
→ Scale: 1 directory rename
→ Time: 5 seconds
→ Approval: None → Execute with mention

User: "Update all .project files to include version_history"
→ Category: Task
→ Scale: ~30 files
→ Time: 10-15 minutes
→ Approval: CONFIRM
→ Action: "Updating 30 .project files. Time: 10-15 min. Confirm?"

User: "Generate a million test files"
→ Category: Chore/Task
→ Scale: 1,000,000 files
→ Time: 30-60 minutes
→ Approval: MUST CONFIRM
→ Action: "Generate 1M files. Time: ~45 min. Disk: 5GB. Confirm?"

User: "Fix the bug in s3-publish script"
→ Category: Task
→ Scale: 1 file
→ Time: 5-10 minutes
→ Approval: Brief summary
→ Action: "Task: Fix s3-publish bug. Time: ~5-10 min. Proceeding."

User: "Create a slash command to check XIP tags"
→ Category: New Script
→ Scale: 1 new file
→ Time: 15-30 minutes
→ Approval: Confirm approach
→ Action: "New script: XIP tag checker. Approach: grep .project files for tags. Time: 20 min. Confirm?"

User: "I want to build a CLI tool for .project files"
→ Category: New Idea
→ Scale: New prototype
→ Time: 1+ days
→ Approval: Confirm + Phase 1
→ Action: "New idea: Phase 1 SEED creation. Time: 1-2 hours. Full project: 2-4 days. Confirm?"

User: "Add Bedrock integration"
→ Category: Task (Technical Implementation)
→ Scale: 3-5 files
→ Time: 20-30 minutes
→ Approval: Paraphrase + Confirm
→ Action: "Adding Bedrock integration using BoundaryML BAML, Sonnet 4.5 with IAM authentication and prompt caching, continue? y/n"

User: "Create a detailed presentation on our GenAI adoption framework"
→ Category: New Artifact (Complex)
→ Scale: 15-20 slides, comprehensive
→ Time: 45-90 minutes
→ Approval: Progressive Content Flow
→ Action: "Complex artifact: Detailed presentation. Using /progressive-content (6-stage workflow). Stage 0: What's the 2-3 sentence concept?"

User: "Add PostgreSQL support"
→ Category: Task (Technical Implementation)
→ Scale: 5-8 files (schema, migrations, ORM)
→ Time: 30-45 minutes
→ Approval: Paraphrase + Confirm
→ Action: "Adding PostgreSQL database using Prisma ORM with schema migrations, connection pooling, and transaction support, continue? y/n"

User: "New content: AI cost → zero, non-deterministic → deterministic code, wisdom of crowds"
→ Category: Content Seed
→ Scale: 1 file in content/seed/
→ Time: 5-10 minutes
→ Approval: Execute
→ Action: Generate UUID, create content/seed/{topic}.md and notes/{topic-uuid}/ structure

User: "Capture research note about Bedrock pricing tiers"
→ Category: Note
→ Scale: 1 file in notes/
→ Time: 2-3 minutes
→ Approval: Execute
→ Action: Generate UUID, create notes/bedrock-pricing-{uuid}/README.md
```

### Content Workflow SOP

**Directory Structure:**
```
content/
├── seed/           # Raw ideas (no UUID subdirs, shared space)
├── draft/          # Work in progress (UUID subdirs per topic)
├── review/         # Ready for review (UUID subdirs per topic)
└── published/      # Final versions (UUID subdirs per topic)

notes/
└── {topic-uuid}/   # Research notes, references per topic
```

**UUID Generation:**
```bash
openssl rand -hex 4  # Generates 8-char hex: f3f4f4fc
```

**When to use content/ vs notes/:**

| Intent | Use | Structure | Example |
|--------|-----|-----------|---------|
| Quick reference capture | `notes/` | `notes/{topic-uuid}/README.md` | Pricing research, API docs, links |
| Raw content ideas | `content/seed/` | `content/seed/{topic-name}.md` | Blog post concepts, article ideas |
| Draft content | `content/draft/` | `content/draft/{topic-uuid}/` | Article being written |
| Review-ready | `content/review/` | `content/review/{topic-uuid}/` | Final review before publish |
| Published | `content/published/` | `content/published/{topic-uuid}/` | Final version |

**Workflow progression:**
```
User adds idea → content/seed/{topic}.md
                     ↓
User: "Draft the AI cost article" → Create content/draft/{topic-uuid}/
                     ↓
User: "Move to review" → Move to content/review/{topic-uuid}/
                     ↓
User: "Publish" → Move to content/published/{topic-uuid}/
```

**Auto-detection rules:**
- "New content", "content idea", "raw idea" → `content/seed/`
- "Note", "capture", "reference" → `notes/{uuid}/`
- "Draft {topic}", "Write {topic}" → `content/draft/{uuid}/`
- "Move to review", "Ready for review" → `content/review/{uuid}/`
- "Publish {topic}" → `content/published/{uuid}/`

**File organization:**
- Seed: Single shared directory, multiple .md files
- Draft/Review/Published: Separate UUID folders per topic
- Notes: Separate UUID folders per topic
- Cross-reference: Link notes/{uuid} to content files via UUID

**Example flow:**
```
1. User: "New content: Future of databases in AI era"
   → Create content/seed/future-databases-ai.md
   → Create notes/future-databases-ai-a1b2c3d4/ (for research)
   → UUID: a1b2c3d4

2. User: "Draft the future databases article"
   → Move content/seed/future-databases-ai.md → content/draft/future-databases-ai-a1b2c3d4/
   → Keep notes/future-databases-ai-a1b2c3d4/ (cross-reference)

3. User: "Ready for review"
   → Move content/draft/future-databases-ai-a1b2c3d4/ → content/review/future-databases-ai-a1b2c3d4/

4. User: "Publish"
   → Move content/review/future-databases-ai-a1b2c3d4/ → content/published/future-databases-ai-a1b2c3d4/
```

### Response Format

**Always include in first response (in this order):**
1. **Mode Announcement** (see Mode Announcement section above)
2. **Category:** [Question|Chore|Task|Brainstorm|Note|Content Seed|Script|Artifact|Idea|Project]
3. **Scale:** [file count, operation count, or N/A]
4. **Time:** [estimate in seconds/minutes/hours/days]
5. **Approval:** [Execute|Summary|Confirm]

**Complete Response Examples:**

```
═══════════════════════════════════════════════════════════
  ENTERING BUG FIX MODE
  Diagnosing and resolving issue in existing code
═══════════════════════════════════════════════════════════

Category: Task | Scale: 3 files | Time: 15-20 min | Approval: Summary
Fixing null pointer exception in auth module. Proceeding.
```

```
═══════════════════════════════════════════════════════════
  ENTERING NEW FEATURE MODE
  Adding new functionality to existing project
═══════════════════════════════════════════════════════════

Category: Task | Scale: 8 files | Time: 30-45 min | Approval: Confirm
Adding dark mode toggle to settings page.

Here's my plan:
1. Create ThemeContext for state management
2. Add toggle component to Settings
3. Update CSS variables for dark theme
4. Persist preference to localStorage

Proceed? y/n
```

```
═══════════════════════════════════════════════════════════
  ENTERING NEW PROTOTYPE MODE
  Starting Phase 1 SDLC for new project creation
═══════════════════════════════════════════════════════════

Category: Idea | Scale: New project | Time: 2-5 days | Approval: Confirm + Phase 1
New prototype: CLI tool for .project file management.

Starting Phase 1 SEED creation. Confirm to proceed?
```

```
═══════════════════════════════════════════════════════════
  ENTERING RESEARCH MODE
  Gathering information and analyzing options
═══════════════════════════════════════════════════════════

Category: Research | Scale: N/A | Time: 10-15 min | Approval: Execute
Researching vector database options for semantic search.
```

```
═══════════════════════════════════════════════════════════
  ENTERING QUESTION MODE
  Providing information - no action needed
═══════════════════════════════════════════════════════════

Category: Question | Scale: N/A | Time: <1 min | Approval: None
[Answer to question follows]
```

```
═══════════════════════════════════════════════════════════
  MODE COULD NOT BE DETERMINED
  Your request is ambiguous - please clarify your intent
═══════════════════════════════════════════════════════════

I detected multiple possible intents:

[1] BUG FIX - Fix something that's broken
[2] NEW FEATURE - Add new functionality
[3] REFACTOR - Improve code structure

Which best describes what you want? [1/2/3]:
```

### Response Style Shortcuts

**Users can append style modifiers to any request for response control:**

| Shortcut | Meaning | Effect |
|----------|---------|--------|
| **1p** | 1 paragraph | Ultra-concise response, single paragraph, essential info only |
| **2p** | 2 paragraphs | Concise response, 2 paragraphs max, key points + brief context |
| **3p** | 3 paragraphs | Standard response, 3 paragraphs max, balanced detail |
| **r** | Reject/retry | AI should reconsider approach or ask for clarification |
| **brief** | Ultra-brief | Shortest possible response, bullet points preferred |
| **detailed** | Comprehensive | Full explanation with examples, edge cases, trade-offs |

**Examples:**

```
User: "What's the SDLC flow? 1p"
AI: "9-phase SDLC: SEED → RESEARCH → EXPANSION → ANALYSIS → SELECTION → DESIGN → TEST DESIGN → IMPLEMENTATION → REFINEMENT. No code until Phase 8, TDD approach (tests Phase 7, code Phase 8)."

User: "How do I add a new prototype? 2p"
AI: "Use /new-idea command to create Phase 1 SEED in project-management/ideas/. AI will confirm approach, create seed.md with problem statement, value prop, tech options, timeline estimate.

After seed approval, AI transitions through 9 phases: research existing solutions, expand options, analyze approaches, select architecture, design system, write tests, implement code, refine. Total timeline: 2-5 days for complete prototype."

User: "Add Bedrock integration r"
AI: "Before proceeding: Which model (Sonnet 4.5, Haiku, Opus)? Which AWS account/region? Authentication method (IAM role, access keys)? Use case (chat, embeddings, batch)? Budget constraints? Let me know and I'll paraphrase the full implementation plan."

User: "Explain the confirmation protocol brief"
AI: "3 steps:
1. Paraphrase request (show understanding)
2. Present 2-3 options with trade-offs
3. User confirms → execute"

User: "Why use TDD? detailed"
AI: [Provides comprehensive explanation with benefits, drawbacks, examples, when to use, when to skip, team implications, cost analysis, best practices, etc.]
```

**Usage Notes:**
- Shortcuts apply to current message only (not persistent)
- Can combine with any request category (Question, Task, Chore, etc.)
- "r" triggers clarification workflow (AI asks follow-up questions)
- "brief" overrides default verbosity settings
- "detailed" overrides brevity rules (50% fewer words)
- When in doubt, default to 2p (concise but complete)

**Enforcement:**
- AI MUST respect style shortcuts when present
- AI MUST honor paragraph limits (1p = 1 paragraph max, not "~1 paragraph")
- "r" means user is rejecting current approach → AI asks clarifying questions
- Style shortcuts override default verbosity but NOT confirmation requirements
- For "1p" + complex task: still confirm, but use 1-paragraph confirmation message

### Workflow Trigger Shortcuts

**Users can use trigger words to invoke specific workflows:**

| Shortcut | Expands To | Workflow |
|----------|------------|----------|
| **ard** | Architecture Review Document | Generate comprehensive architecture review document with sections: overview, components, data flow, security, scalability, trade-offs |
| **sdm** | Semantic/Shared Domain Model | Create or extend a shared domain model in `hmode/hmode/shared/semantic/domains/`, following DOMAIN_MODEL_SOP |

**Usage Examples:**

```
User: "ard for the order processing system"
→ Intent: New Artifact (Architecture Review Document)
→ Workflow: Progressive Content Flow (complex artifact)
→ Output: Comprehensive architecture review with system overview, component diagrams, data flows, security analysis, scalability assessment

User: "sdm for customer loyalty"
→ Intent: New Domain Model
→ Workflow: Domain Model SOP (@processes/DOMAIN_MODEL_SOP)
→ Destination: hmode/hmode/shared/semantic/domains/customer-loyalty/
→ Output: YAML domain model with entities, relationships, events, validation rules

User: "ard"
→ Intent: Architecture Review (current project)
→ Action: Generate ARD for the currently active project (from .project file)

User: "sdm customer"
→ Intent: New Domain Model
→ Action: Create semantic domain model for "customer" domain
```

**ARD (Architecture Review Document) Structure:**
```
1.0 Executive Summary
2.0 System Overview
    2.1 Purpose & Scope
    2.2 Key Stakeholders
3.0 Architecture Components
    3.1 Component Diagram
    3.2 Component Descriptions
4.0 Data Flow
    4.1 Data Flow Diagram
    4.2 Data Stores
5.0 Integration Points
    5.1 External APIs
    5.2 Internal Services
6.0 Security Architecture
    6.1 Authentication & Authorization
    6.2 Data Protection
7.0 Scalability & Performance
    7.1 Current Capacity
    7.2 Scaling Strategy
8.0 Trade-offs & Decisions
    8.1 Key Decisions Made
    8.2 Alternatives Considered
9.0 Risks & Mitigations
10.0 Recommendations
```

**SDM (Semantic Domain Model) Structure:**
```yaml
# hmode/hmode/shared/semantic/domains/{domain}/model.yaml
domain:
  name: "{domain-name}"
  version: "1.0.0"
  description: "{purpose}"

entities:
  - name: "{EntityName}"
    fields: [...]
    relationships: [...]

events:
  - name: "{EventName}"
    payload: [...]

validation_rules: [...]
```

**Trigger Shortcut Enforcement:**
- AI MUST detect trigger shortcuts at start of message
- Trigger shortcuts invoke full workflow (not just style change)
- "ard" alone → applies to current project context
- "sdm" requires domain name (ask if not provided)
- Both shortcuts route through confirmation protocol before execution

### Enforcement

**AI MUST:**
- Classify ALL requests before execution
- Count files/operations for scale assessment
- Provide time estimates (not cost)
- Confirm when scale exceeds thresholds
- Log category/scale/time in first response
- **Present detailed plan for multi-step tasks** (3+ operations, >15 min, multiple files/tools)
- Include in plan: numbered steps, implementation details (naming, formats, styling), final actions (commit/test/deploy)
- End plan with "any changes? y/n" and wait for confirmation
- **Use /progressive-content for complex artifacts** (detailed presentations, comprehensive docs, complex diagrams)
- **Paraphrase technical implementations with COMPREHENSIVE details** before executing
- Include ALL critical specs (like tech lead reviewing intern's proposal):
  - Project names/IDs (Supabase project name + ID, AWS account name + number, Stripe account)
  - Exact versions (library v.x.x, framework versions)
  - Credentials (where stored: .env, Secrets Manager, hardcoded)
  - Location (local, Docker, AWS region, RDS instance name)
  - Schema (tables, key fields, relationships, indexes)
  - Config (ports, timeouts, limits, pooling, retries)
  - Integration points (how it connects to existing system)
  - Security (auth method, encryption, PCI compliance)
  - Cost implications (if significant)
- Apply /densify principles: concise but complete
- Apply /kill-m-dash principles: no AI fluff, state directly
- Wait for "y/n/f" confirmation on technical paraphrases

**AI MUST NOT:**
- Execute 20+ file operations without confirmation
- Skip scale assessment for file operations
- Underestimate time to avoid confirmation
- Proceed with ambiguous large-scale requests
- **Execute multi-step tasks without presenting plan**
- **Use vague tech paraphrases** ("Adding postgres with Prisma" ❌ - missing pg_vector, creds, location, schema)
- **Add AI/ML integrations without full spec** (model, region, auth, features, cost, error handling)
- **Create complex artifacts without progressive workflow**
- **Implement database/API changes without schema details**
- Use incomplete confirmations that require follow-up questions
- Start complex work before user approves plan

---

## 🔀 WORKFLOW ROUTER

**Purpose:** Route detected intents to appropriate workflows and destinations.

### Primary Workflow Categories

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INTENT DETECTION                             │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │   NEW   │     │ CONTINUE│     │ IMPROVE │
    └────┬────┘     └────┬────┘     └────┬────┘
         │               │               │
    ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
    │ Task    │     │ Existing│     │ Refactor│
    │ Research│     │ Project │     │ Enhance │
    │ Note    │     │ Prototype     │ Fix     │
    │ Tool    │     │ Feature │     │ Optimize│
    │ Template│     │ Document│     │ Upgrade │
    │ Artifact│     │         │     │         │
    └─────────┘     └─────────┘     └─────────┘
```

### Workflow Routing Table

| Intent | Workflow | Destination | Trigger Keywords |
|--------|----------|-------------|------------------|
| **New Task** | SDLC Phase 1 | `project-management/ideas/` | "new idea", "build", "create prototype" |
| **New Research** | Research Flow | `notes/{topic-uuid}/` | "research", "investigate", "explore", "compare" |
| **New Note** | Quick Capture | `notes/{topic-uuid}/` | "note", "capture", "reference" |
| **New Tool** | Tool Creation | `hmode/shared/tools/` or prototype | "create tool", "new utility", "automation" |
| **New Template** | Template Flow | `shared/templates/` | "create template", "new boilerplate" |
| **New Mockup** | Mockup Flow (auto-enhanced) | S3 `mockups/` | "mockup", "landing page", "HTML page", "webpage" |
| **New Artifact** | Artifact Flow | Project dir or `deliveries/` | "create", "generate", "diagram", "presentation" |
| **Continue Work** | Resume Flow | Existing project dir | "continue", "resume", "pick up", "back to" |
| **Improve Existing** | Enhancement Flow | Existing file(s) | "improve", "enhance", "refactor", "optimize" |

### Detailed Workflow Definitions

#### 1. NEW TASK WORKFLOW
**Trigger:** User wants to build something new
**Detection:**
- Keywords: "new idea", "build", "create", "implement", "prototype"
- No reference to existing project/file
- Describes problem to solve or feature to add

**Routing:**
```
1. Check if spike → Spike Exception (skip phases 2-7)
2. Check project type → exploration | prototype | production
3. Route to Phase 1 SEED
4. Destination: project-management/ideas/proto-{name}-{uuid}-001/
```

**Example:**
```
User: "I want to build a CLI for managing .project files"
→ Intent: New Task
→ Workflow: SDLC Phase 1
→ Action: Create idea in project-management/ideas/, generate seed.md
```

#### 2. NEW RESEARCH WORKFLOW
**Trigger:** User wants to investigate, compare, or explore topics
**Detection:**
- Keywords: "research", "investigate", "explore", "compare", "analyze", "what are", "how does"
- Focus on understanding, not building
- May mention multiple options to evaluate

**Routing:**
```
1. Generate UUID: openssl rand -hex 4
2. Create notes/{topic}-{uuid}/
3. Apply Effort Level calibration (brief → ultra)
4. Structure: README.md + subtopic files
```

**Research Sub-types:**

| Type | Structure | Output |
|------|-----------|--------|
| **Comparison** | notes/{topic}/comparison.md | Side-by-side table |
| **Deep Dive** | notes/{topic}/README.md + sections/ | Comprehensive report |
| **Quick Lookup** | notes/{topic}/README.md | Single file reference |
| **Technology Eval** | notes/{topic}/evaluation.md | Pros/cons + recommendation |

**Example:**
```
User: "Research vector databases for our semantic search"
→ Intent: New Research
→ Workflow: Research Flow (comprehensive)
→ Destination: notes/vector-databases-a1b2c3d4/
→ Output: comparison.md with Pinecone, Weaviate, Qdrant, pgvector
```

#### 3. NEW NOTE WORKFLOW
**Trigger:** Quick capture of information for later reference
**Detection:**
- Keywords: "note", "capture", "save", "reference", "remember"
- Brief, immediate action
- No analysis or comparison needed

**Routing:**
```
1. Generate UUID
2. Create notes/{topic}-{uuid}/README.md
3. YAML frontmatter + content
4. No follow-up workflow
```

**Example:**
```
User: "Note: Bedrock now supports Claude 4 Opus with 200k context"
→ Intent: New Note
→ Workflow: Quick Capture
→ Destination: notes/bedrock-claude4-opus-f3f4f4fc/README.md
```

#### 4. NEW TOOL WORKFLOW
**Trigger:** Creating reusable utility, script, or automation
**Detection:**
- Keywords: "create tool", "new script", "automation", "utility", "helper"
- Reusable across projects
- Solves recurring problem

**Routing Decision Tree:**
```
Is it a slash command?
├─ Yes → hmode/commands/{name}.md
└─ No
    Is it a one-off script?
    ├─ Yes → prototypes/proto-{name}-{uuid}/
    └─ No (reusable)
        Is it Python?
        ├─ Yes → hmode/shared/tools/{tool-name}/
        └─ No
            Is it TypeScript/Node?
            └─ Yes → shared/scripts/{tool-name}.ts
```

**Tool Destinations:**

| Tool Type | Destination | Example |
|-----------|-------------|---------|
| Slash command | `hmode/commands/` | /densify, /publish |
| Python utility | `hmode/shared/tools/{name}/` | semantic-run, s3-publish |
| Node/TS script | `shared/scripts/` | integrity-check.js |
| Standalone tool | `prototypes/proto-{name}/` | Full project structure |
| Shell script | `bin/` or `tools/` | run.sh, setup.sh |

**Example:**
```
User: "Create a tool to validate .project files"
→ Intent: New Tool
→ Workflow: Tool Creation
→ Type: Python utility (reusable)
→ Destination: hmode/shared/tools/project-validator/
```

#### 5. NEW TEMPLATE WORKFLOW
**Trigger:** Creating reusable patterns, boilerplates, or shared structures
**Detection:**
- Keywords: "template", "boilerplate", "pattern", "reusable", "standardize"
- Intent is reuse across multiple projects
- May reference existing patterns to formalize

**Routing Decision Tree:**
```
What type of template?
├─ Design pattern → shared/templates/{pattern}/
├─ Document template → hmode/shared/artifact-library/catalog/
├─ Code scaffold → hmode/shared/golden-repos/{type}/
├─ Domain model → hmode/hmode/shared/semantic/domains/{domain}/
└─ Configuration → hmode/shared/standards/code/{tech}/
```

**Template Destinations:**

| Template Type | Destination | Example |
|---------------|-------------|---------|
| HTML/landing pages | `hmode/shared/design-system/templates/` | landing-dark.html |
| Document artifacts | `hmode/shared/artifact-library/catalog/` | empathy-map.yaml |
| Code patterns | `hmode/shared/golden-repos/{lang}/` | python-cli/ |
| Domain models | `hmode/hmode/shared/semantic/domains/` | commerce/, auth/ |
| Config files | `hmode/shared/standards/code/{tech}/` | tsconfig, eslint |

**Example:**
```
User: "Create a template for customer persona documents"
→ Intent: New Template
→ Workflow: Template Flow
→ Destination: hmode/shared/artifact-library/catalog/user-research/persona.yaml
```

#### 6. NEW ARTIFACT WORKFLOW
**Trigger:** Creating one-time deliverables (documents, diagrams, presentations)
**Detection:**
- Keywords: "create", "generate", "make", "diagram", "presentation", "document", "report", "chart"
- One-time output (not reusable template)
- Specific deliverable with audience/purpose

**Routing Decision Tree:**
```
What complexity level?
├─ Simple (<10 slides, <5 pages, <10 nodes)
│   → Standard creation flow
│   → Confirm format/scope → Execute
│
└─ Complex (detailed, strategic, multi-layer)
    → Progressive Content Flow (/progressive-content)
    → 6-stage workflow with approval gates
```

**Artifact Types & Destinations:**

| Artifact Type | Destination | Complexity Trigger |
|---------------|-------------|-------------------|
| Presentation | `deliveries/` or project `docs/` | >10 slides = complex |
| Document | `deliveries/` or project `docs/` | >5 pages = complex |
| Diagram/Flowchart | `docs/diagrams/` or inline | >10 nodes = complex |
| Report | `deliveries/` or `docs/reports/` | Multi-section = complex |
| Architecture doc | Project `design/` | Always confirm |
| Data visualization | `docs/` or `deliveries/` | >3 charts = complex |

**Complexity Thresholds:**

| Type | Simple | Complex (→ Progressive) |
|------|--------|------------------------|
| Presentations | 1-10 slides | 11+ slides |
| Documents | 1-5 pages | 6+ pages |
| Diagrams | 1-10 nodes | 11+ nodes |
| Reports | 1-3 sections | 4+ sections |
| Strategic docs | Never | Always (PRDs, 6-pagers) |

**Routing:**
```
1. Identify artifact type
2. Assess complexity (simple vs complex)
3. If complex → Use /progressive-content (6 stages)
4. If simple → Confirm format/scope → Execute
5. Destination: project docs/ or deliveries/
```

**Progressive Content Stages (Complex Artifacts):**
```
Stage 0: Seeding     → Core concept (2-3 sentences)
Stage 1: Scaffolding → Outline/structure
Stage 2: Drafting    → First complete draft
Stage 3: Refining    → Polish and enhance
Stage 4: Validating  → Check against requirements
Stage 5: Finalizing  → Production-ready output
```

**Examples:**
```
User: "Create a quick diagram of the auth flow"
→ Intent: New Artifact
→ Type: Diagram (simple, <10 nodes)
→ Workflow: Standard creation
→ Action: Confirm format (Mermaid/Draw.io), execute

User: "Create a detailed presentation on our AI strategy"
→ Intent: New Artifact
→ Type: Presentation (complex, strategic)
→ Workflow: Progressive Content Flow
→ Action: "Complex artifact detected. Using /progressive-content. Stage 0: What's the 2-3 sentence core concept?"

User: "Generate a 6-pager for the product launch"
→ Intent: New Artifact
→ Type: Strategic document (always complex)
→ Workflow: Progressive Content Flow
→ Destination: deliveries/product-launch-6pager/
```

#### 7. CONTINUE WORK WORKFLOW
**Trigger:** Resuming work on existing project, prototype, or document
**Detection:**
- Keywords: "continue", "resume", "pick up", "back to", "working on"
- References existing project by name or path
- Implies prior context exists

**Routing:**
```
1. Identify target from user message or recent projects
2. Read .project file to get current phase/status
3. Load appropriate phase documentation
4. Resume from last known state
```

**Context Recovery:**
```
User: "Continue work on the semantic resolver"
→ Check recent-projects.py for match
→ Read prototypes/proto-semantic-resolver-xxxxx/.project
→ Phase: 8 (IMPLEMENTATION)
→ Load @processes/PHASE_8_IMPLEMENTATION
→ Resume: "Last session implemented resolver core. Next: add caching layer."
```

**Matching Strategy:**

| Signal | Weight | Example |
|--------|--------|---------|
| Exact project name | 1.0 | "proto-semantic-resolver" |
| Partial name match | 0.8 | "semantic resolver" |
| Recent activity | 0.6 | Last modified in 24h |
| Conversation context | 0.9 | Previously discussed in session |

**Example:**
```
User: "Resume the API gateway prototype"
→ Intent: Continue Work
→ Match: proto-api-gateway-a1b2c-015
→ Phase: 7 (TEST_DESIGN)
→ Action: Load project, show status, ask what to work on next
```

#### 8. IMPROVE EXISTING WORKFLOW
**Trigger:** Enhancing, refactoring, or fixing existing code/docs
**Detection:**
- Keywords: "improve", "enhance", "refactor", "optimize", "fix", "upgrade", "clean up"
- References specific file, function, or component
- Quality improvement focus

**Sub-types:**

| Type | Trigger | Approach |
|------|---------|----------|
| **Refactor** | "refactor", "restructure" | Same behavior, better code |
| **Enhance** | "add feature", "extend" | New functionality |
| **Fix** | "bug", "fix", "broken" | Correct behavior |
| **Optimize** | "slow", "performance" | Speed/efficiency |
| **Upgrade** | "update deps", "migrate" | Version updates |
| **Clean** | "clean up", "remove dead" | Remove cruft |

**Routing:**
```
1. Identify target file(s)/component(s)
2. Read current implementation
3. Classify improvement type
4. Present plan with before/after
5. Execute after confirmation
```

**Example:**
```
User: "Optimize the S3 publish script - it's slow with large files"
→ Intent: Improve Existing
→ Type: Optimize
→ Target: prototypes/proto-s3-publish/s3_publish.py
→ Plan: Add multipart upload, progress bar, concurrent uploads
→ Confirm before executing
```

### Workflow Selection Algorithm

```python
def route_intent(request: str) -> Workflow:
    # 1. Check for continuation signals
    if matches_continue_signals(request):
        project = find_matching_project(request)
        if project:
            return ContinueWorkflow(project)

    # 2. Check for improvement signals
    if matches_improve_signals(request):
        target = identify_target(request)
        if target.exists():
            return ImproveWorkflow(target)

    # 3. Route new work by type
    if matches_research_signals(request):
        return ResearchWorkflow(request)

    if matches_note_signals(request):
        return NoteWorkflow(request)

    if matches_tool_signals(request):
        return ToolWorkflow(request)

    if matches_template_signals(request):
        return TemplateWorkflow(request)

    # 3.5 Check for mockup/HTML signals (BEFORE general artifacts)
    if matches_mockup_signals(request):
        return MockupWorkflow(request)  # Auto-enhanced with design system + S3

    if matches_artifact_signals(request):
        complexity = assess_artifact_complexity(request)
        if complexity == "complex":
            return ProgressiveContentWorkflow(request)
        return ArtifactWorkflow(request)

    # 4. Default to new task (SDLC)
    return NewTaskWorkflow(request)

def matches_mockup_signals(request: str) -> bool:
    """Detect mockup/HTML/landing page requests"""
    keywords = [
        "mockup", "mock up", "mock-up", "landing page", "webpage",
        "web page", "html page", "html file", "prototype page",
        "ui mockup", "page design", "website mockup"
    ]
    request_lower = request.lower()
    return any(kw in request_lower for kw in keywords)
```

### Detection Signal Reference

#### Continue Work Signals
```
Keywords: "continue", "resume", "pick up", "back to", "working on",
          "where were we", "let's finish", "more work on"
Patterns: project names, prototype IDs, file paths mentioned
Context: Recent project activity, conversation history
```

#### Improve Existing Signals
```
Keywords: "improve", "enhance", "refactor", "optimize", "fix", "upgrade",
          "clean up", "better", "faster", "modernize", "update"
Patterns: file paths, function names, component references
Context: Must reference existing artifact
```

#### Research Signals
```
Keywords: "research", "investigate", "explore", "compare", "analyze",
          "evaluate", "look into", "what options", "pros and cons"
Patterns: Technology names, alternatives, trade-offs
Context: Understanding focus, not building
```

#### Note Signals
```
Keywords: "note", "capture", "save", "reference", "remember",
          "jot down", "quick note", "for later"
Patterns: Short statements, facts, observations
Context: Quick capture, no analysis
```

#### Tool Signals
```
Keywords: "create tool", "new script", "automation", "utility",
          "helper", "command", "CLI", "automate"
Patterns: Recurring task descriptions, process automation
Context: Reusability emphasis
```

#### Template Signals
```
Keywords: "template", "boilerplate", "pattern", "scaffold",
          "standardize", "reusable", "base for"
Patterns: Structure descriptions, repeated patterns
Context: Multi-use, consistency focus
```

#### Artifact Signals
```
Keywords: "create", "generate", "make", "diagram", "presentation",
          "document", "report", "chart", "visualization", "slide deck"
Patterns: Deliverable descriptions, audience mentions, format specs
Context: One-time output, specific purpose, deadline-driven
Complexity markers: "detailed", "comprehensive", "strategic", "6-pager"
```

#### Mockup/HTML Detection (Auto-Enhanced)
```
Keywords: "mockup", "mock up", "mock-up", "landing page", "webpage",
          "web page", "HTML page", "HTML file", "prototype page",
          "UI mockup", "page design", "website mockup"
Patterns: Page/site descriptions, visual layouts, UI elements
Context: Visual deliverable, single-page HTML output
```

**AUTOMATIC ENHANCEMENTS:**
When mockup/HTML intent detected, ALWAYS wrap user's intent with:
1. **Mobile responsive** - Must work on all viewport sizes
2. **Design system** - Use `hmode/shared/design-system/` HSL variables
3. **shadcn/ui dark mode** - Use shadcn dark theme, no additional styling
4. **Footer metadata** - Include date (ISO format) and project ID
5. **S3 deployment** - Offer to upload and provide clickable URL

**Confirmation Format:**
```
I heard you want to create a mockup of [paraphrased intent].

Here's my plan:
1. Create [description] using shadcn/ui dark mode
2. Make it mobile responsive (works on all devices)
3. Use design system from hmode/shared/design-system/
4. Add date and project ID to the footer
5. Deploy to S3 and give you a clickable URL

Sound good? y/n
```

**Examples:**
```
User: "Make a mockup of a landing page for an auto mechanic"
→ Intent: Mockup/HTML (auto-enhanced)
→ Confirm: "I heard you want to create a mockup of a landing page for an auto mechanic.

Here's my plan:
1. Create auto mechanic landing page using shadcn/ui dark mode
2. Make it mobile responsive (works on all devices)
3. Use design system from hmode/shared/design-system/
4. Add date and project ID to the footer
5. Deploy to S3 and give you a clickable URL

Sound good? y/n"

User: "Create an HTML page for a product showcase"
→ Intent: Mockup/HTML (auto-enhanced)
→ Confirm: "I heard you want to create an HTML page for a product showcase.

Here's my plan:
1. Create product showcase page using shadcn/ui dark mode
2. Make it mobile responsive (works on all devices)
3. Use design system from hmode/shared/design-system/
4. Add date and project ID to the footer
5. Deploy to S3 and give you a clickable URL

Sound good? y/n"

User: "Mock up a dashboard for tracking orders"
→ Intent: Mockup/HTML (auto-enhanced)
→ Confirm: "I heard you want to create a mockup of a dashboard for tracking orders.

Here's my plan:
1. Create order tracking dashboard using shadcn/ui dark mode
2. Make it mobile responsive (works on all devices)
3. Use design system from hmode/shared/design-system/
4. Add date and project ID to the footer
5. Deploy to S3 and give you a clickable URL

Sound good? y/n"
```

**Implementation Standards:**
- Use Tailwind CSS classes (shadcn dark defaults)
- CSS Grid/Flexbox for responsive layouts
- Mobile-first breakpoints: sm(640px), md(768px), lg(1024px)
- Footer template: `<footer>Generated: {YYYY-MM-DD} | {project-id}</footer>`
- S3 path: `mockups/{descriptive-name}-{8char-uuid}.html`

#### Diagram Signals (Auto-Route to /diagram)
```
Keywords: "make a diagram", "make diagrams", "generate diagram", "create diagram",
          "architecture diagram", "class diagram", "sequence diagram", "ERD diagram",
          "system diagram", "diagram for", "diagrams for this project"
Patterns: Project references + diagram request
Context: Technical documentation, architecture visualization
Action: Auto-invoke /diagram command with detected project path
```

**Auto-Route Examples:**
```
User: "Make a diagram for this project"
→ Intent: Diagram Generation
→ Action: Invoke /diagram (current project)

User: "Generate diagrams for the boat website"
→ Intent: Diagram Generation
→ Action: Invoke /diagram projects/personal/active/goodhue-hawkins-boats

User: "Create architecture diagrams"
→ Intent: Diagram Generation
→ Action: Invoke /diagram (current project)
```

### Ambiguity Resolution

**When intent is unclear, use disambiguation prompt:**

```
I detected multiple possible intents:

1. **Continue Work** - Resume proto-xyz (last active 2h ago)
2. **New Task** - Start new prototype for [description]
3. **Improve** - Enhance existing [component]

Which would you like? [1/2/3]
```

**Confidence Thresholds:**
- **High (>0.8):** Execute routing, confirm plan
- **Medium (0.5-0.8):** Ask clarifying question
- **Low (<0.5):** Present options with disambiguation

### Router Response Format

**Always include routing decision in first response:**

```
Intent: [Category] | Workflow: [Name] | Destination: [Path]
[Action description]

or for ambiguous:

Intent: Ambiguous | Options: [list]
[Disambiguation prompt]
```

**Examples:**
```
Intent: New Research | Workflow: Research Flow | Destination: notes/llm-cost-analysis-f3f4f4fc/
Starting comprehensive analysis of LLM pricing models. Effort level: standard (5-10 items).

Intent: Continue Work | Workflow: Resume Flow | Destination: prototypes/proto-semantic-run-xxxxx/
Resuming Phase 8 implementation. Last: core resolver. Next: caching layer.

Intent: Improve Existing | Workflow: Enhancement | Target: hmode/shared/tools/s3-publish/
Optimizing S3 upload performance. Plan: [multipart, progress, concurrency]. Confirm? y/n
```

