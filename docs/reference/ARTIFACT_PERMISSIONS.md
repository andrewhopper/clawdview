# Artifact Permissions Matrix

<!-- File UUID: 8f3c2a7b-9e4d-4c8f-a1b6-3d5e7f9c2b4a -->

**Purpose:** Define which artifacts ARE and ARE NOT permitted in each SDLC phase

---

## Quick Reference Matrix

| Phase | Permitted Artifacts | Forbidden Artifacts |
|-------|-------------------|-------------------|
| **1. SEED** | Idea description, problem statement, target persona | Code, tests, user stories, technical specs |
| **2. RESEARCH** | Research notes, solution comparisons, citations, feasibility analysis | Code, tests, user stories, architecture docs |
| **2.5 FEASIBILITY** | Go/no-go analysis, risk assessment, effort estimates | Code, tests, implementation details |
| **3. EXPANSION** | High-level approaches (5-10), pros/cons, feature lists, tech options | User stories, detailed requirements, code, tests |
| **4. ANALYSIS** | Approach comparison tables, scoring matrices, tradeoff analysis | User stories, code, tests, implementation plans |
| **5. SELECTION** | Selected approach rationale, decision log, constraints | Code, tests, detailed specs |
| **5.5 PRD** | PRD, requirements, user stories, acceptance criteria | Code, tests, architecture diagrams |
| **6. DESIGN** | Architecture docs, UML diagrams, API specs, domain models | Code, tests (design only, no implementation) |
| **7. TEST_DESIGN** | Test plans, test cases, BDD scenarios | Implementation code (tests only) |
| **8. IMPL** | All code, configs, scripts, deployment files | None (everything permitted) |
| **8.5 VALIDATION** | Screenshots, test reports, accessibility audits | N/A (validation phase) |
| **9. REFINEMENT** | Bug fixes, polish, optimizations, UAT tests | New features (refinement only) |

---

## Phase-by-Phase Breakdown

### Phase 1: SEED 🌱

**Goal:** Capture the idea essence

**PERMITTED:**
- Idea description (1-2 paragraphs)
- Problem statement (who has what problem?)
- Target persona (inferred, not TBD)
- Vision statement (what success looks like)
- Context/motivation (why now?)

**FORBIDDEN:**
- ❌ Code (any language)
- ❌ Tests
- ❌ User stories
- ❌ Technical specifications
- ❌ Architecture diagrams
- ❌ Implementation details

**OUTPUT FORMAT:** `seed.md` in decimal outline format

---

### Phase 2: RESEARCH 🔍

**Goal:** Understand existing solutions

**PERMITTED:**
- Research notes with citations
- Existing solution comparisons (3-5 alternatives)
- Pros/cons tables
- Gap analysis (what's missing?)
- Feasibility notes
- Technology landscape review

**FORBIDDEN:**
- ❌ Code (any language)
- ❌ Tests
- ❌ User stories
- ❌ Detailed requirements
- ❌ Architecture diagrams (too early)
- ❌ API specifications

**OUTPUT FORMAT:** `research.md` with citations in decimal outline

---

### Phase 2.5: FEASIBILITY ⚖️ (Production Only)

**Goal:** Go/no-go decision

**PERMITTED:**
- Feasibility analysis (6 criteria)
- Risk assessment
- Effort estimates (rough)
- Build vs buy comparison
- Decision recommendation (PROCEED | CONDITIONAL | SPIKE | ABANDON)

**FORBIDDEN:**
- ❌ Code
- ❌ Tests
- ❌ Implementation details
- ❌ Detailed technical specs

**OUTPUT FORMAT:** `feasibility.md` with decision matrix

---

### Phase 3: EXPANSION 🧠

**Goal:** Brainstorm high-level approaches

**PERMITTED:**
- 5-10 high-level approaches (architectural patterns, solution strategies)
- Pros/cons for each approach
- Feature lists (what capabilities each approach enables)
- Scenarios/use cases
- Edge cases to consider
- Technology options (frameworks, languages, platforms)
- Tables and bullet points

**FORBIDDEN:**
- ❌ User stories (too detailed, premature)
- ❌ Detailed requirements (not yet selected)
- ❌ Acceptance criteria (Phase 5.5)
- ❌ Code
- ❌ Tests
- ❌ API specifications (Phase 6)
- ❌ Database schemas (Phase 6)

**WHY NO USER STORIES?** Phase 3 is divergent thinking - exploring multiple possible solutions. User stories are convergent (specific requirements for a chosen solution). Save them for Phase 5.5 after approach is selected.

**OUTPUT FORMAT:** `expansion.md` (2 pages max) in decimal outline

**Example Permitted Content:**
```markdown
## Approach 1: Microservices Architecture
**Description:** Separate services for auth, data, and API
**Pros:** Independent scaling, technology flexibility
**Cons:** Deployment complexity, network overhead
**Technologies:** Node.js (API), Python (data processing), PostgreSQL

## Approach 2: Monolithic Architecture
**Description:** Single codebase with modular structure
**Pros:** Simpler deployment, easier debugging
**Cons:** Scaling challenges, tight coupling
**Technologies:** Next.js full-stack, Prisma ORM, PostgreSQL
```

**Example Forbidden Content:**
```markdown
❌ User Story: As a user, I want to log in so that I can access my dashboard
❌ Acceptance Criteria: Given valid credentials, when I submit...
```

---

### Phase 4: ANALYSIS 📊

**Goal:** Compare approaches systematically

**PERMITTED:**
- Approach comparison tables
- Scoring matrices (weighted criteria)
- Tradeoff analysis
- Risk comparisons
- Cost/effort estimates
- Technical complexity rankings

**FORBIDDEN:**
- ❌ User stories (Phase 5.5)
- ❌ Code
- ❌ Tests
- ❌ Implementation plans (Phase 6)
- ❌ Detailed specs (Phase 5.5)

**OUTPUT FORMAT:** `analysis.md` with comparison tables

---

### Phase 5: SELECTION 🎯

**Goal:** Choose winning approach

**PERMITTED:**
- Selected approach announcement
- Rationale (why this one?)
- Decision log
- Constraints identified
- Risks accepted
- Approach summary

**FORBIDDEN:**
- ❌ Code
- ❌ Tests
- ❌ Detailed requirements (Phase 5.5)
- ❌ Architecture diagrams (Phase 6)

**OUTPUT FORMAT:** `selection.md` with decision rationale

---

### Phase 5.5: PRD & REQUIREMENTS 📋 (Production Only)

**Goal:** Document formal requirements

**PERMITTED:**
- PRD (Product Requirements Document)
- User stories with acceptance criteria
- Requirements specification
- Functional requirements
- Non-functional requirements (performance, security, etc.)
- Success metrics
- Out of scope declarations

**FORBIDDEN:**
- ❌ Code
- ❌ Tests
- ❌ Architecture diagrams (Phase 6)
- ❌ API specifications (Phase 6)
- ❌ Database schemas (Phase 6)

**OUTPUT FORMAT:** `PRD.md`, `REQUIREMENTS.md`, `ACCEPTANCE_CRITERIA.md`

---

### Phase 6: DESIGN 🏗️

**Goal:** Design system architecture

**PERMITTED:**
- Architecture diagrams (C4, UML, Mermaid)
- Component design docs
- API specifications (OpenAPI, GraphQL schemas)
- Database schemas (ERD, DDL)
- Domain models (YAML)
- Interface definitions
- Data flow diagrams
- Security design
- Deployment architecture

**FORBIDDEN:**
- ❌ Implementation code (design only)
- ❌ Tests (Phase 7)
- ❌ Config files with secrets (design references only)

**OUTPUT FORMAT:** `ARCHITECTURE.md`, `docs/diagrams/*.mmd`, `shared/domain-models/{project}/*.yaml`

**CRITICAL:** Domain models MUST be checked/created via `domain-modeling-specialist` agent

---

### Phase 7: TEST DESIGN 🧪

**Goal:** Write tests BEFORE implementation (TDD)

**PERMITTED:**
- Test files (unit, integration, E2E)
- BDD scenarios (Cucumber .feature files)
- Test plans
- Test data fixtures
- Mock/stub implementations
- Test configuration

**FORBIDDEN:**
- ❌ Implementation code (only test code)
- ❌ Production config files

**OUTPUT FORMAT:** `tests/`, `*.test.ts`, `*.spec.ts`, `*.feature`

**WHY TESTS FIRST?** Test-Driven Development - tests define contract before implementation

---

### Phase 8: IMPLEMENTATION 💻

**Goal:** Implement to pass tests

**PERMITTED:**
- **EVERYTHING** - all code, configs, scripts, deployment files, documentation

**FORBIDDEN:**
- Nothing (implementation phase is unrestricted)

**OUTPUT FORMAT:** Full project structure

**REQUIRED DELIVERABLES:**
- Working code that passes tests
- Startup script (`bin/start-{project}` or `package.json` scripts)
- Environment config (`.env.example`)
- README with setup instructions
- Error tracking integration (web/UI projects at MVP+ stage)
- Buildinfo.json generation (frontend projects)

---

### Phase 8.5: VALIDATION ✅ (Web/UI Only)

**Goal:** Verify quality before user testing

**PERMITTED:**
- Screenshots (automated via Playwright)
- Test execution reports
- Accessibility audit results
- Performance metrics
- Bug reports (to be fixed in Phase 9)

**FORBIDDEN:**
- N/A (validation phase, not creation phase)

**OUTPUT FORMAT:** `validation-report.md`, screenshots in `docs/screenshots/`

---

### Phase 9: REFINEMENT ✨

**Goal:** Fix issues, polish, UAT

**PERMITTED:**
- Bug fixes from Phase 8.5
- Polish and optimizations
- UAT automation
- Performance improvements
- Documentation updates
- Deployment refinements

**FORBIDDEN:**
- ❌ New features (that's a new SDLC cycle)
- ❌ Scope creep

**OUTPUT FORMAT:** Polished, production-ready codebase

---

## Special Cases

### SPIKE Mode

**Goal:** Answer specific technical question (throwaway code)

**PERMITTED:**
- Spike plan document (`spikes/{name}/SPIKE_PLAN.md`)
- Throwaway code (will be deleted)
- Findings document (`spikes/{name}/FINDINGS.md`)

**FORBIDDEN:**
- Production-ready code (spikes are throwaway)
- Comprehensive tests (POC only)
- Production deployments

**DURATION:** Max 3 days

---

### BROWNFIELD Mode (Existing Projects)

**Goal:** Work on existing codebase

**Phase 0: ASSESSMENT**
**PERMITTED:**
- Code analysis notes
- Impact assessment
- Test coverage report
- Risk analysis
- Work type classification (HOTFIX, BUG_FIX, FEATURE, REFACTOR)

**FORBIDDEN:**
- Code changes (assessment only)

**THEN:** Route to abbreviated phase flow based on work type

---

## Enforcement Rules

### 1. Pre-Code Gate (MANDATORY)

BEFORE writing ANY code, verify:
- [ ] Current phase is 8, 9, or declared SPIKE
- [ ] `.project` file confirms phase number
- [ ] If phase < 8: REFUSE code, explain violation, offer options

**Violation Response:**
```
Cannot write code - currently in Phase {N} ({phase_name}).
Code is only permitted in Phase 8 (Implementation) or 9 (Refinement).

Options:
[1] Continue Phase {N} activities
[2] Advance to Phase 8
[3] Declare SPIKE mode (throwaway prototype)
```

### 2. User Story Prevention (MANDATORY)

BEFORE writing user stories, verify:
- [ ] Current phase is 5.5 (PRD) OR 6+ (post-selection)
- [ ] If phase = 3 (Expansion): REFUSE user stories

**Violation Response:**
```
Cannot write user stories in Phase 3 (Expansion).
Phase 3 is for high-level approach brainstorming, not detailed requirements.

User stories belong in Phase 5.5 (PRD) after approach is selected.

Continue with high-level approach exploration?
```

### 3. Architecture Prevention (MANDATORY)

BEFORE creating architecture diagrams, verify:
- [ ] Current phase is 6+ (Design)
- [ ] If phase < 6: REFUSE architecture work

**Violation Response:**
```
Cannot design architecture in Phase {N}.
Architecture design requires Phase 6 (Design).

Current phase activities: {phase_description}
```

---

## Artifact Format Standards

### All Phases

**Required in every artifact:**
- Decimal outline numbering (1.0, 1.1, 1.2, 2.0)
- File UUID comment header
- Stage title: `# Stage {N} - {Phase Name}`
- Date created
- Clear section headings

**Markdown preferences:**
- Numbered lists over bullets (except checkmarks)
- Tables for comparisons
- ASCII diagrams (when helpful)
- Densified language (50% fewer words)

### Design System Assets

**Required for visual artifacts (HTML, SVG, mockups):**
- Asset UUID (8-char)
- Design tokens (NO raw hex colors)
- Atomic classification (atom/molecule/organism/template/page)
- Metadata comment header
- Template from `hmode/shared/design-system/templates/`

**See:** `@design-system/MANAGEMENT_GUIDELINES`

---

## Quick Violation Checks

**"Can I write code?"**
→ Check phase: 8/9/SPIKE = YES, else NO

**"Can I write user stories?"**
→ Check phase: 5.5+ = YES, 3 = NO (high-level approach only)

**"Can I design architecture?"**
→ Check phase: 6+ = YES, else NO

**"Can I write tests?"**
→ Check phase: 7+ = YES, else NO

**"Can I add new features?"**
→ Check phase: 8 = YES, 9 = NO (refinement only)

---

## See Also

- `@processes/SDLC_OVERVIEW` - Full phase flow
- `@core/CRITICAL_RULES` - Top 25 rules
- `@processes/PHASE_{N}_{NAME}` - Individual phase docs
- `@design-system/MANAGEMENT_GUIDELINES` - Visual asset rules
