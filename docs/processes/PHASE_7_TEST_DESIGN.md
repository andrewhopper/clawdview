### Phase 7: TEST DESIGN 🧪 (BDD - BEHAVIORS ONLY!)
**Goal:** Write behavior scenarios BEFORE implementation (Behavior-Driven Development)
**Output:** `prototypes/proto-name-xxxxx-NNN-name/features/` with Gherkin scenarios + step definitions
**Title:** `# Stage 7 - Test Design`

**Choose testing track in Phase 6→7 transition. Document in `.project` metadata.**

---

### STEP 1: REFERENCE COLLECTION 📚 (REQUIRED BEFORE TESTS)
**Goal:** Download reference projects and documentation for chosen libraries
**Output:** `prototypes/proto-name-xxxxx-NNN-name/references/` + `REFERENCES.md`

**Activities:**
- **Internal references:** Review `hmode/shared/standards/code/` for relevant tech stack patterns
- **External references:** Download reference projects for each major library in tech stack
- **Documentation:** Use Context7, official docs, or web search for latest API documentation
- **Examples:** GitHub repos, official starter templates, framework examples
- **Storage:** Save in `prototypes/proto-name-xxxxx-NNN-name/references/` (Git-ignored for external code)

**REFERENCES.md Format:**
```markdown
# Stage 7 - Reference Materials

## 1.0 Internal References
- hmode/shared/standards/code/typescript/ - Type safety patterns
- hmode/shared/standards/code/react/ - Component structure

## 2.0 External References
| Library | Version | Reference Source | Location |
|---------|---------|------------------|----------|
| React | 18.x | Official examples | references/react-examples/ |
| FastAPI | 0.109.x | GitHub starter | references/fastapi-starter/ |

## 3.0 Documentation Links
- React 18 Docs: https://react.dev
- FastAPI Tutorial: https://fastapi.tiangolo.com

## 4.0 Key Patterns to Apply
- Error handling: hmode/shared/standards/code/typescript/errors.ts
- Async patterns: references/fastapi-starter/async_routes.py
```

**Exit Criteria:**
- All major libraries have reference materials
- REFERENCES.md created and complete
- References available for test design and implementation

---

### STEP 2: TEST CREATION (BDD SCENARIOS)

### Track A: BASIC SMOKE SCENARIOS (REQUIRED - All Projects)
**Purpose:** Fast LLM feedback during implementation, verify basic functionality

**Setup:**
- Create prototype directory structure (features/, support/, step-definitions/)
- Install Cucumber + Playwright + dependencies
- Configure cucumber.cjs with Gherkin support

**Required Scenarios:**
- Homepage accessibility (Given/When/Then for page load)
- Screenshot capture (visual validation on failure)
- Critical path smoke scenario (1 scenario for primary user flow)
- Basic error handling (404, 500 page scenarios)

**Coverage Target:** 20-30% (critical paths only)

**Format:** Gherkin feature files (`.feature`) with natural language scenarios

**Why:** Gives AI fast feedback during Phase 8 development. Stakeholder-readable scenarios.

---

### Track B: COMPREHENSIVE BDD SCENARIOS (OPTIONAL - Production Quality)
**Purpose:** Code quality, production readiness, full regression coverage

**Setup:**
- All Track A setup requirements
- Additional test frameworks (unit testing for step definitions)
- HTML report generation + S3 upload scripts

**Required Scenarios:**
- All Track A scenarios (baseline)
- E2E scenarios for ALL must-have features (from Phase 5 selection)
- Unit tests for business logic (behind step definitions)
- Integration scenarios for API/database interactions
- Edge cases + error scenarios (Scenario Outlines)
- Input validation scenarios

**Coverage Target:** 50-70% during Phase 8, 80%+ by Phase 9

**Why:** Production-quality code, stakeholder-readable tests, comprehensive regression protection.

---

**Track Selection Guidance:**
- **Track A:** Rapid prototypes, POCs, internal tools, learning projects
- **Track B:** Client deliverables, production systems, graduated prototypes

**🚨 CRITICAL:** Scenarios MUST be written and failing before ANY implementation code (both tracks)

**🔄 Track Upgrade:** Can upgrade A→B anytime. Add to `.project` phase_history.

**BDD Testing Guide:** See `hmode/shared/standards/testing/BDD_TESTING_GUIDE.md` for full setup details

**Exit:** All feature files created with Gherkin scenarios, step definitions stubbed, scenarios run (and fail), coverage plan documented, ready for implementation

