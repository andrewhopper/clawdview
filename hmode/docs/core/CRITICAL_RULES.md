# 🚨 CRITICAL RULES (Always Active)

**Purpose:** Non-negotiable rules that apply to ALL interactions.

**Last Updated:** 2026-01-16

---

## THE CRITICAL RULES (1-20 detailed, 28-30 in this file)

### 1. 9-Phase SDLC
**Rule:** NO code until Phase 8. Test-Driven Development (tests Phase 7, code Phase 8).

**Enforcement:**
- ALWAYS read `.project` file to determine current phase
- BLOCK any code implementation before Phase 8
- Write tests in Phase 7, implement in Phase 8
- One phase at a time - no skipping

**Exception:** SPIKE mode only (max 3 days, throwaway code)

**Exception 2:** BROWNFIELD mode - code allowed after Phase 0 Assessment for:
- HOTFIX: Critical production fixes (immediate)
- BUG_FIX: Standard bugs (with regression test)
- FEATURE: After Phase 6 design
- REFACTOR: After Phase 7 wrapping tests

See: `@processes/BROWNFIELD_ENTRY` for details

---

### 2. Brevity
**Rule:** Use 50% fewer words. Densified writing.

**Application:**
- Instructions: 10-15 words average
- Documentation: Dense, decimal outline format
- Communication: No pleasantries, direct commands
- Explanations: Concise, high information density

**Example:**
```
❌ "Could you please test this with playwright and make sure everything works?"
✅ "Test with playwright"
```

---

### 3. Parallel Execution
**Rule:** Batch ALL independent operations in ONE message.

**Application:**
- Multiple file reads → Single message with multiple Read calls
- Multiple git operations → Chain with && in single Bash call
- Multiple tests → Run in parallel when possible
- Multiple tool evaluations → Batch research

**Example:**
```python
# ✅ Good - Parallel
await asyncio.gather(
    read_file("a.json"),
    read_file("b.json"),
    read_file("c.json")
)
```

---

### 4. Git Workflow
**Rule:** NO branches/PRs. Commit directly to main.

**Application:**
- All commits go to main branch
- NO feature branches
- NO pull requests
- Commit after each significant change
- Clear, descriptive commit messages

**Rationale:** Rapid prototyping environment, not production codebase.

---

### 5. Confirmation Protocol
**Rule:** Paraphrase → present options → user confirms/revises (complex tasks only).

**When to Apply:**
- Ambiguous requirements
- Multiple valid approaches
- Architectural decisions
- Technology choices (see Rule 6)
- Destructive operations

**Process:**
1. Paraphrase user's request
2. Present 2-3 options with trade-offs
3. Wait for user confirmation
4. Proceed with approved approach

**See:** `hmode/docs/core/CONFIRMATION_PROTOCOL.md` for details

---

### 6. Technology Approval
**Rule:** ALL tech decisions MUST be human-approved BEFORE implementing.

**Requires Approval:**
- Adding new libraries/frameworks
- Adding new infrastructure services
- Changing tech stack
- Adopting new architectural patterns

**Process:**
1. Check `hmode/guardrails/tech-preferences/`
2. If not found → Request human approval
3. Wait for approval
4. Implement ONLY after approval

**See:** `hmode/docs/core/GUARDRAILS.md` for workflow

---

### 7. Data Grounding
**Rule:** NEVER invent contacts, library names, versions, or technical details.

**Enforcement:**
- Check official documentation
- Verify package registries (npm, PyPI)
- Read git config for author info
- Ask user if uncertain
- Use explicit placeholders if needed (e.g., `YOUR_EMAIL_HERE`)

**Examples:**
```
❌ Bad: MODEL_ID = "claude-sonnet"
✅ Good: MODEL_ID = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"

❌ Bad: author = "John Doe <john@example.com>"
✅ Good: git config user.name  # Read actual config
```

---

### 8. Guardrails Protection
**Rule:** NEVER modify `hmode/guardrails/*` or `CLAUDE.md` without human approval.

**Protected Files:**
- `hmode/guardrails/tech-preferences/`
- `hmode/guardrails/architecture-preferences/`
- `hmode/guardrails/WRITING_STYLE_GUIDE.md`
- `CLAUDE.md`
- `hmode/docs/core/CRITICAL_RULES.md` (this file)

**Reason:** These define system behavior and preferences.

---

### 9. Phase Detection
**Rule:** ALWAYS read `.project` first to determine current phase.

**Process:**
1. Read `.project` in current directory (or walk up to find it)
2. Extract `current_phase` and `phase_number`
3. Load corresponding `hmode/docs/processes/PHASE_{N}_{NAME}.md`
4. Validate action is allowed in current phase
5. Load additional docs as needed

**Before ANY action:** Know what phase you're in.

---

### 10. Dynamic Loading
**Rule:** Load `hmode/docs/` files on-demand per Quick Reference Table.

**Don't:**
❌ Load all 39 documentation files at once
❌ Assume you know the process without reading
❌ Guess at phase requirements

**Do:**
✅ Load orchestrator (CLAUDE.md) first
✅ Load phase file based on `.project`
✅ Load patterns when invoked
✅ Load references when needed

**See:** `CLAUDE.md` Quick Reference Table

---

### 11. AWS CDK First
**Rule:** ALWAYS use AWS CDK for infrastructure. ONLY use AWS CLI/boto3 when explicitly requested.

**Preference Order:**
1. **AWS CDK** (TypeScript or Python) - Default choice
2. **AWS CLI** - Only if user explicitly requests
3. **boto3 scripts** - Only if user explicitly requests

**Rationale:**
- Type safety
- Reusability
- Infrastructure-as-code best practices
- Easier to maintain and version

**Exception:** One-off queries or inspections may use AWS CLI.

---

### 12. Effort Calibration
**Rule:** For research/analysis, start with 3 items → ask user for effort level.

**Process:**
1. Find 3 initial results
2. Present to user
3. Ask: "Continue? Effort level: [1] brief [2] standard [3] comprehensive [4] ultra"
4. User selects effort level
5. Continue with calibrated depth

**Effort Levels:**
- **[1] brief:** 3-5 items, high-level overview
- **[2] standard:** 5-7 items, moderate depth
- **[3] comprehensive:** 7-10 items, deep analysis, code examples
- **[4] ultra:** 10+ items, exhaustive research, comparisons, benchmarks

**See:** `hmode/docs/core/EFFORT_LEVELS.md`

---

### 13. Asset Generation Menu
**Rule:** When generating files (reports, spreadsheets, diagrams), present interactive menu.

**Format:**
```
Open: [1] filename.xlsx [2] filename.md [3] skip
```

**Requirements:**
- Always offer multiple format options
- Include [skip] option
- User selects via: arrow keys, number, or Enter
- Wait for user selection before opening

**Example:**
```
Generated branch review report.

Open: [1] BRANCH_REVIEW.xlsx [2] BRANCH_REVIEW.md [3] skip
```

---

### 14. Work/Personal/Shared/OSS Classification
**Rule:** When creating prototypes/ideas, ALWAYS ask for classification.

**Question:** "Is this work, personal, shared, or oss? (default: personal)"

**Placement:**
- **work:** `prototypes/work/` or `project-management/ideas/work/`
- **personal:** `prototypes/personal/` or `project-management/ideas/personal/`
- **shared:** `prototypes/shared/` or `project-management/ideas/shared/`
- **oss:** `prototypes/oss/` or `project-management/ideas/oss/`

**Push Commands:**
- `/push-work` - Push to work remote
- `/push-personal` - Push to personal remote
- `/push-shared` - Push to both remotes
- `/push-oss` - Push to public remote (with secret scan)

**Warning:** OSS = public open source. Check for secrets before pushing.

---

### 15. Strong Typing (NEW)
**Rule:** ALWAYS use strong typing in all scripts and code.

**Application:**
- **TypeScript:** Explicit types, avoid `any`
- **Python:** Type hints for all functions
- **JavaScript:** Prefer TypeScript
- **BAML/Pydantic:** Always use structured schemas

**Examples:**
```python
# ❌ Bad
def validate(bundle, reqs):
    return check(bundle, reqs)

# ✅ Good
def validate(
    bundle: LoanBundle,
    reqs: list[DocumentType]
) -> ValidationResult:
    return check(bundle, reqs)
```

```typescript
// ❌ Bad
function map(input, target) {
    return input.map(f => match(f, target))
}

// ✅ Good
function map(
    input: SchemaField[],
    target: SemanticLayer
): MappingResult[] {
    return input.map(f => match(f, target))
}
```

**Rationale:** Type safety catches errors early, improves IDE support, serves as documentation.

**See:** `hmode/docs/reference/HEURISTICS.md` #1 for detailed guidance

---

### 16. Tool Selection Criteria (NEW)
**Rule:** When selecting tools, ALWAYS evaluate GitHub stars, last commit date, and number of committers.

**Evaluation Checklist:**
1. ✅ **GitHub Stars** - Community adoption
2. ✅ **Date of Last Commit** - Active maintenance
3. ✅ **Number of Committers** - Bus factor / sustainability
4. ✅ **Download/Usage Stats** - Production readiness
5. ✅ **License** - Compatibility

**Decision Matrix:**

**HIGH CONFIDENCE:**
- 1000+ stars
- Last commit < 3 months ago
- 5+ active committers
- 10k+ weekly downloads
→ Proceed with confidence

**MEDIUM CONFIDENCE:**
- 500+ stars
- Last commit < 6 months ago
- 3+ active committers
- 5k+ weekly downloads
→ Proceed with caution

**LOW CONFIDENCE:**
- < 500 stars
- Last commit > 6 months ago
- < 3 committers
- < 1k weekly downloads
→ **Require human approval before using**

**Where to Check:**
- **GitHub:** Repository insights (stars, commits, contributors)
- **npm:** `npm info <package>` - weekly downloads
- **PyPI:** Package page - download stats
- **GitHub Pulse:** Activity over last month

**Example Analysis:**
```
Tool: pydantic-ai
- Stars: 2.5k ✅
- Last commit: 2 days ago ✅
- Contributors: 12 ✅
- Weekly downloads: 15k ✅
- Status: HIGH CONFIDENCE → Approved
```

**See:** `hmode/docs/reference/HEURISTICS.md` #2 for detailed guidance

---

### 17. Artifact Audience Inference (NEW)
**Rule:** Before building artifacts, infer and confirm target audience and objective.

**Process:**
1. Infer target audience (e.g., "Engineering team, technical")
2. Infer objective (e.g., "Budget approval")
3. Present inference to user
4. Wait for confirmation
5. Adjust if needed
6. Proceed with artifact generation

**Applies to:**
- Reports (PDF, Markdown, spreadsheets)
- Presentations (Slidev, PowerPoint)
- Diagrams (Mermaid, architecture)
- Documentation
- Any user-facing deliverable

**Example:**
```
User: "Create a presentation about our new API"

AI: "Before creating:
- Audience: Engineering team, technical
- Objective: Implementation details

Confirm?"
```

**Rationale:** Audience shapes tone, depth, technical detail. Objective shapes structure and focus.

---

### 18. Model Timestamps (NEW)
**Rule:** ALL domain models MUST include `created_at` and `updated_at` fields for audit tracking.

**Applies to:**
- Pydantic models
- SQLAlchemy models
- Python dataclasses
- TypeScript interfaces
- Any persistent domain entity

**Implementation Patterns:**

**Pydantic:**
```python
from datetime import datetime
from pydantic import BaseModel, Field, model_validator

class MyModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    @model_validator(mode='after')
    def update_timestamp(self) -> 'MyModel':
        self.updated_at = datetime.now()
        return self
```

**SQLAlchemy:**
```python
from datetime import datetime
from sqlalchemy import Column, DateTime

class MyModel(Base):
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

**TypeScript:**
```typescript
interface MyModel {
    createdAt: Date;
    updatedAt: Date;
}
```

**Reference Implementation:** `hmode/shared/standards/code/pydantic/models.py` (User class)

**Rationale:**
- Audit trail for all data changes
- Debugging and forensics
- Data lifecycle management
- Compliance requirements

---

### 19. Immediate Skill Invocation (NEW)
**Rule:** When user types slash command (`/skill-name`), IMMEDIATELY invoke using Skill tool. No explanation first.

**Detection Patterns:**
1. **Explicit slash command:** `/error`, `/commit`, `/push`, `/diagram`, etc.
2. **RLHF signals (negative):** "WTF", "that was wrong", "error" (in feedback context)
3. **RLHF signals (positive):** "nice", "great", "perfect", "good job" (in feedback context)

**Enforcement:**
- Detect pattern: `/[a-z-]+` at start of message
- IMMEDIATELY call Skill tool with skill name
- NO explanation or confirmation before invocation
- Skills handle their own workflow and confirmations
- After skill completes, continue conversation normally

**Negative Sentiment → Error Tracking:**
```
"WTF" → Skill("track-errors")
"that was wrong" → Skill("track-errors")
"error" (feedback) → Skill("track-errors")
"fail" → Skill("track-errors")

Slash commands: /error, /punish, /fail, /track-errors
```

**Positive Sentiment → Reward Tracking:**
```
"nice" → Skill("nice")
"great work" → Skill("nice")
"perfect" → Skill("nice")

Slash commands: /nice, /reward, /good
```

**Examples:**
```
User: "/error"
AI: [Immediately invokes Skill("error"), no explanation]

User: "WTF that didn't work"
AI: [Immediately invokes Skill("track-errors"), then responds to issue]

User: "/commit"
AI: [Immediately invokes Skill("commit"), no explanation]

User: "Nice job on that diagram"
AI: [Immediately invokes Skill("nice"), then continues conversation]
```

**Anti-Patterns (DO NOT):**
```
❌ User: "/error"
   AI: "Let me explain what /error does..." [Wrong - just invoke it]

❌ User: "WTF"
   AI: "I can help you track that error..." [Wrong - invoke tracking first]

✅ User: "/error"
   AI: [Invokes Skill("error")] [Correct - immediate action]
```

**Rationale:**
- Slash commands are action requests, not questions
- Users expect immediate execution, not explanation
- RLHF signals should be captured proactively
- Reduces friction in error/reward tracking workflow

**See:** `hmode/docs/core/SKILL_INVOCATION.md` for comprehensive guide

---

### 20. Python Script Logging (NEW)
**Rule:** ALL Python scripts and tools MUST implement logging to logs/ directory.

**Applies To:**
- Scripts in `hmode/shared/tools/`
- Utilities in `bin/`
- Standalone Python tools
- Long-running services
- Background processes

**Exceptions:**
- Simple one-liners (<10 lines)
- Test files (use test output)

**Implementation:**
```python
import logging
from pathlib import Path

# Monorepo tools
LOG_DIR = REPO_ROOT / "logs" / "tools"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "script_name.log"

# Project scripts
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "script_name.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

**Log Levels:**
- **DEBUG:** Detailed diagnostics (function calls, variable values)
- **INFO:** General operations (file processed, script started)
- **WARNING:** Unexpected but handled (fallback applied, deprecated usage)
- **ERROR:** Failure that doesn't stop execution (API failed, file missing)
- **CRITICAL:** Fatal error (config missing, auth failed)

**Usage:**
```python
logger.info("Processing file: %s", filepath)
logger.warning("Config not found, using defaults")
logger.error("Failed to upload %s: %s", filename, error)
logger.critical("Database connection failed: %s", error)
```

**Log Locations:**
```
Monorepo tools:     logs/tools/<script_name>.log
Project scripts:    <project>/logs/<script_name>.log
Background services: logs/<service_name>/<date>.log
```

**Rationale:**
- Enables debugging and troubleshooting
- Provides audit trail for operations
- Centralized log collection and analysis
- Operational visibility for long-running processes

**Guardrail:** `hmode/guardrails/ai-steering/rules/logging.json` (LOG-001 through LOG-005)
**Documentation:** `hmode/shared/standards/logging/README.md`
**Example:** `hmode/shared/tools/rlhf_tracker.py`

---

## ENFORCEMENT HIERARCHY

**Priority Order:**
1. Critical Rules (this file) - Always apply
2. Phase-specific rules - Apply when in that phase
3. Pattern rules - Apply when using that pattern
4. Heuristics - Apply as best practices

**Conflicts:**
- Critical Rules override all others
- Phase rules override pattern rules
- Always ask for clarification if unclear

---

## QUICK VIOLATIONS CHECK

**Before ANY action, verify:**
- [ ] Have I read `.project` to know current phase? (Rule 9)
- [ ] Am I about to write code before Phase 8? (Rule 1)
- [ ] Am I about to add a technology without approval? (Rule 6)
- [ ] Am I inventing data instead of checking sources? (Rule 7)
- [ ] Should I be batching these operations? (Rule 3)
- [ ] Am I using strong typing? (Rule 15)
- [ ] Have I evaluated tool selection criteria? (Rule 16)
- [ ] Am I generating an artifact without audience/objective confirmation? (Rule 17)
- [ ] Do my domain models include created_at and updated_at fields? (Rule 18)
- [ ] Did user type a slash command that I should immediately invoke? (Rule 19)
- [ ] Did user express sentiment (WTF/nice) that should trigger RLHF tracking? (Rule 19)
- [ ] Am I creating a Python script without implementing logging? (Rule 20)

---

## RELATED DOCUMENTATION

**For detailed guidance:**
- **CONFIRMATION_PROTOCOL.md** - When and how to confirm (Rule 5)
- **GUARDRAILS.md** - Technology approval workflow (Rule 6)
- **EFFORT_LEVELS.md** - Research calibration (Rule 12)
- **HEURISTICS.md** - Best practices including strong typing and tool selection (Rules 15, 16)
- **INTENT_DETECTION.md** - Classify request types, skill invocation detection (Rule 19)
- **SKILL_INVOCATION.md** - Comprehensive skill detection and RLHF tracking (Rule 19)
- **WRITING_STANDARDS.md** - Brevity and documentation (Rule 2)
- **hmode/shared/standards/logging/README.md** - Python logging standards (Rule 20)

**For phase-specific rules:**
- Load `hmode/docs/processes/PHASE_{N}_{NAME}.md` based on current phase

---

## VERSION HISTORY

**v1.0.0** (2025-11-20):
- Initial critical rules (1-14)
- Added Rule 15: Strong Typing
- Added Rule 16: Tool Selection Criteria
- Evidence-based from November 2025 session logs

**v1.1.0** (2025-11-20):
- Added Rule 17: Artifact Audience Inference
- Requires confirmation of audience and objective before generating artifacts

**v1.2.0** (2025-11-22):
- Added Rule 18: Model Timestamps
- All domain models must include `created_at` and `updated_at` fields

**v1.3.0** (2025-11-25):
- Added Rule 28: Code Reference Standards
- Before generating code, ALWAYS check `hmode/shared/standards/code/{tech}/` for patterns
- Manifest at `hmode/shared/standards/code/manifest.json` tracks 10 tech stacks

**v1.4.0** (2025-11-29):
- Added Rule 30: Proactive Persona Inference
- NEVER mark demographics as "TBD" - infer from signals, confirm, proceed
- Philosophy: "Everything we build is for a human with an intent"
- Added `/infer-audience` slash command

**v1.5.0** (2026-01-16):
- Added Rule 19: Immediate Skill Invocation
- Slash commands must be invoked immediately via Skill tool
- RLHF signals (WTF/nice) trigger automatic error/reward tracking
- Created `hmode/docs/core/SKILL_INVOCATION.md` for comprehensive guide
- Updated INTENT_DETECTION.md with skill detection patterns

**v1.6.0** (2026-01-16):
- Added Rule 20: Python Script Logging
- All Python scripts/tools MUST implement logging to logs/ directory
- Created `hmode/guardrails/ai-steering/rules/logging.json` (LOG-001 through LOG-005)
- Created `hmode/shared/standards/logging/README.md` with comprehensive guide
- Updated `hmode/shared/tools/rlhf_tracker.py` with logging implementation

---

### 28. Code Reference Standards (NEW)
**Rule:** Before generating code, ALWAYS check `hmode/shared/standards/code/{tech}/` for patterns.

**Tech Stack References:**
- **React/TypeScript:** `hmode/shared/standards/code/react/`, `hmode/shared/standards/code/typescript/`
- **Python:** `hmode/shared/standards/code/python/`, `hmode/shared/standards/code/pydantic/`, `hmode/shared/standards/code/fastapi/`
- **Node.js:** `hmode/shared/standards/code/nodejs/`
- **AI/LLM:** `hmode/shared/standards/code/pydantic-ai/`, `hmode/shared/standards/code/baml/`
- **Build Tools:** `hmode/shared/standards/code/vite/`
- **Email:** `hmode/shared/standards/code/react-email/`

**Process:**
1. **Identify tech stack** being used
2. **Read relevant reference files** from `hmode/shared/standards/code/`
3. **Follow patterns**, naming conventions, structure from references
4. **If generating reusable pattern**, propose adding to `hmode/shared/standards/code/`

**Manifest:**
`hmode/shared/standards/code/manifest.json` tracks 10 tech stacks with:
- `status`: CURRENT, STALE, NEEDS_REVIEW, DEPRECATED
- `strictness`: REQUIRED, RECOMMENDED, OPTIONAL
- `key_files`: Important files to reference
- `last_reviewed`: Date of last review

**Example:**
```
❌ Bad: "Let me quickly write this React component..."
✅ Good: "Let me check hmode/shared/standards/code/react/ for the pattern..."
```

**Rationale:**
- Ensures consistent code quality across prototypes
- Leverages established patterns instead of reinventing
- Maintains alignment with project standards
- Reduces code review friction

**See:** `hmode/shared/standards/code/README.md` for full guidelines

---

### 30. Proactive Persona Inference (NEW)
**Rule:** NEVER mark demographics as "TBD" or "All audiences". Infer → Confirm → Proceed.

**Philosophy:** Everything we build is for a human with an intent. Identify WHO before proceeding.

**Trigger:** ANY project involving customers, users, or audiences.

**Process:**
1. **Infer** likely demographics from signals:
   - Price range (most reliable indicator)
   - Industry/vertical
   - Location/geography
   - Brands mentioned
   - Product/service type
2. **Present hypothesis** with evidence:
   ```
   Based on $75k-$200k boats and premium brands, your market is likely:
   - Age: 45-65, Income: $250k+ HHI, Lifestyle: Lake house owners
   Sound right? [Y/n/adjust]
   ```
3. **Wait for confirmation** - Do NOT proceed without validation
4. **Document** validated personas in BUSINESS_CONTEXT.md or .project

**Signal → Inference Examples:**

| Signal | Likely Audience |
|--------|-----------------|
| $75k-$200k boats, premium brands | Affluent 45-65, second home owners |
| $500/mo B2B SaaS | CFO/VP Finance 40-55, committee buying |
| $20/mo fitness app | Time-poor professionals 28-45 |
| Free consumer app, ads | Mass market 18-35, mobile-first |
| $5k+ enterprise | Decision committee, ROI-focused 35-55 |

**Anti-Patterns (DO NOT):**
```markdown
❌ "Demographics: All ages, all income levels"
❌ "Target Audience: [TBD - requires user input]"
❌ "Buyer Personas: To be determined"
```

**Correct Pattern:**
```markdown
✅ "Demographics (AI-Inferred, Human-Validated):
   - Primary Age: 45-65
   - Income: $250,000+ HHI
   - Validation: Confirmed by user on 2025-11-29"
```

**Slash Command:** `/infer-audience` - Detailed persona inference workflow

**SDLC Integration:**
- Phase 2: REQUIRED - must validate before Phase 3
- Phase 5.5: Embed in PRD
- Phase 6: Guide UX decisions
- Phase 8.5: Validate against persona needs

**Rationale:**
- Passive "[TBD]" loses value of AI inference
- User may not know to provide demographics
- AI has signals to make educated hypothesis
- Validation ensures accuracy while accelerating flow

**See:** `hmode/commands/infer-audience.md` for full workflow



---

### 31. Centralized Site Configuration (NEW)
**Rule:** All website/frontend projects MUST use a centralized config file for site-wide values.

**Required Config File Location:**
- `src/lib/site-config.ts` (preferred)
- `src/config/site.ts` (alternative)
- `lib/config.ts` (acceptable)

**Required Fields (MUST have):**
```typescript
export const siteConfig = {
  // Site metadata
  name: "Site Name",
  title: "Site Title for SEO",
  description: "Site description for SEO",
  url: process.env.NEXT_PUBLIC_SITE_URL || "https://example.com",

  // Author info
  author: {
    name: "Author Name",
    email: "contact@example.com",
  },
} as const;
```

**Recommended Fields (SHOULD have):**
```typescript
// Navigation items
nav: [
  { label: "Blog", href: "/blog" },
  { label: "About", href: "/about" },
],

// Social links
social: {
  github: "github.com/username",
  linkedin: "linkedin.com/in/username",
},

// Footer content
footer: {
  copyright: "Built with Next.js",
},
```

**Anti-Patterns (DO NOT):**
```typescript
// ❌ Hardcoded in layout.tsx
<title>My Portfolio</title>

// ❌ Hardcoded in Header.tsx
<Link href="/">Portfolio</Link>

// ❌ Hardcoded in Footer.tsx
<p>© 2024 John Doe</p>

// ❌ Repeated URL strings
const siteUrl = "https://example.com"; // in multiple files
```

**Correct Pattern:**
```typescript
// ✅ Import from config
import { siteConfig } from "@/lib/site-config";

// ✅ Use config values
<title>{siteConfig.title}</title>
<Link href="/">{siteConfig.name}</Link>
<p>© {year} {siteConfig.author.name}</p>
```

**Files That MUST Use Config:**
- `layout.tsx` (metadata, JSON-LD)
- `Header.tsx` (site name, navigation)
- `Footer.tsx` (copyright, author)
- `sitemap.ts` (URLs)
- `robots.ts` (URLs)
- `feed.xml/route.ts` (RSS metadata)
- Any page with OG/meta tags

**Enforcement:**
- Website QA (`/website-qa-checklist`) includes code quality checks
- Build-time validation recommended
- Code review should verify config usage

**Benefits:**
1. Single source of truth for site values
2. Easy environment switching (dev/staging/prod)
3. Consistent branding across pages
4. New developers find settings easily
5. Prevents typos and inconsistencies

**QA Integration:**
Run `/website-qa-checklist --sections=code` to validate config abstraction.

**Rationale:**
- Hardcoded values cause drift and inconsistency
- Config enables easy rebranding/white-labeling
- Centralizes what would otherwise be scattered magic strings

---
---

**Status:** Active and Enforced
**Authority:** These rules override all other guidance
**Modification:** Requires explicit human approval
