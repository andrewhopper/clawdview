### Phase 8.5: POST-GENERATION QUALITY VALIDATION 📸 (DUAL-TRACK QA)
**Goal:** Automated quality validation for generated artifacts
**Output:** `validation-report.md`, screenshots in `tests/screenshots/`, accessibility audit, CLI validation results
**Title:** `# Stage 8.5 - Quality Validation`

**Applies to:** ALL projects (code quality checks) + Websites, web apps, dashboards, UI-heavy prototypes (visual validation)
**Skip visual validation for:** CLIs, APIs, libraries, backend services (but MUST run code quality checks)

**Validation Approaches:**

**1. Code Quality Validation (ALL projects)**
- **Guardrail enforcement** - Verify tech/architecture compliance
- **Domain model usage verification** - Track shared domain adoption
- **Code standards compliance** - Type safety, naming, structure
- **Dependency audits** - Security vulnerabilities
- No browser required, runs on any project type
- **Execution:** Run all checks in PARALLEL using sub-agents

**2. Browser-Based Validation (Playwright)**
- Visual/UI validation, screenshots, accessibility
- User flow testing, cross-browser checks
- Requires running application + browser automation

**3. CLI-Based Validation (qa-validator.py)**
- Technical validation via curl/grep/filesystem
- Natural language interface: "CSS working", "Fonts loaded"
- Fast, no browser required, ideal for CI/CD
- Complements Playwright with infrastructure checks

**Activities:**

**All Projects (Mandatory - Run in PARALLEL):**

1. **Run guardrail enforcement check**:
   ```bash
   python3 hmode/shared/tools/guardrail-enforce.py --check-all --output validation/guardrail-report.txt
   ```
   - Verifies tech preferences compliance
   - Checks architecture pattern approvals
   - Validates AI steering rules (NEVER/ALWAYS/MUST constraints)
   - **Pass criteria:** No violations OR violations approved
   - **Execution:** Spawn as sub-agent for parallel processing

2. **Run domain usage verification**:
   ```bash
   python3 hmode/shared/tools/verify-domain-usage.py --output validation/domain-usage-report.txt
   ```
   - Scans for shared domain model imports vs. local model definitions
   - Calculates compliance score
   - Identifies opportunities to refactor local models to shared domains
   - **Pass criteria:** Report generated, score documented (no minimum threshold)
   - **Action items:** Document local models that should be promoted to shared
   - **Execution:** Spawn as sub-agent for parallel processing

**Parallel Execution Pattern:**
```python
# In Claude Code: Launch both checks simultaneously
# Sub-agent 1: Guardrail enforcement
# Sub-agent 2: Domain usage verification
# Wait for both to complete before proceeding
```

**Web/UI Projects (Additional):**
2. **Create seed data file** (`seed-data.json`, `fixtures.sql`, or similar)
3. **Run startup script** to launch environment with seeded data
4. **Execute Playwright validation suite**:
   - Screenshot all major pages/views
   - Basic accessibility checks (WCAG Level A minimum)
   - Functional smoke tests (navigation, forms, key interactions)
   - Visual regression baseline capture
5. **Execute CLI validation suite** (optional but recommended):
   - `python qa-validator.py "All checks"`
   - Verifies CSS compilation, JavaScript loading, assets, fonts, colors
   - Fast technical verification using curl/grep
6. **Generate validation report** with screenshots and findings

**Validation Suite Requirements:**

**Track A (Basic Validation):**
- Screenshot homepage and 2-3 key pages
- Basic accessibility audit (automated scan)
- Smoke test: Can load pages without errors
- Validation report with pass/fail summary

**Track B (Comprehensive Validation):**
- Screenshot all major pages/views
- Comprehensive accessibility audit (WCAG A/AA)
- Functional validation of all user flows
- Visual regression testing
- Performance metrics (Core Web Vitals)
- Cross-browser screenshots (Chromium, Firefox, WebKit)

**Validation Report Format:**
```markdown
# Stage 8.5 - Quality Validation Report

## 1.0 Code Quality (ALL Projects)

### 1.1 Guardrail Enforcement
- **Tool:** `guardrail-enforce.py --check-all`
- **Tech Preferences:** ✅ All approved technologies used
- **Architecture Patterns:** ✅ CDK pattern approved, followed
- **AI Steering Rules:** ✅ No violations of NEVER/ALWAYS/MUST rules
- **Protected Files:** ✅ No unauthorized modifications to hmode/guardrails/
- **Status:** ✅ PASS (0 violations)
- **Violations:** None
- **Action Items:** None

### 1.2 Domain Model Usage
- **Tool:** `verify-domain-usage.py`
- **Available Domains:** 130 domains in hmode/hmode/shared/semantic/domains/
- **Shared Domains Used:** 3 (auth, email, product)
- **Local Models Defined:** 5 (2 Python, 3 TypeScript)
- **Compliance Score:** 37.5%
- **Status:** ✅ PASS (report generated)
- **Action Items:**
  - Consider promoting `CustomMetrics` to observability domain
  - Refactor `UserPreferences` to use auth domain models
  - Review `OrderSummary` for alignment with order domain

### 1.3 Code Standards
- ✅ Type hints present (Python)
- ✅ TypeScript strict mode enabled
- ✅ No hardcoded paths or secrets
- ✅ File size under 500 lines

### 1.4 Parallel Execution Summary
- **Guardrail check:** 2.3s (sub-agent)
- **Domain verification:** 4.7s (sub-agent)
- **Total wall time:** 4.7s (parallel execution)
- **Time saved:** 2.3s (vs sequential)

## 2.0 Environment (Web/UI Projects Only)
- Startup script: `npm run start:test`
- Seed data: `scripts/seed-data.json` (50 users, 200 products)
- Test URL: http://localhost:3000

## 3.0 CLI Validation (qa-validator.py)
- ✅ Dev server running
- ✅ CSS working - Found 8 Tailwind color variants
- ✅ JavaScript loading - 3 script tags present
- ✅ Fonts loaded - 4 font families configured
- ✅ Color scheme working - Tailwind + CSS variables
- ✅ Assets load - All critical assets OK
- ✅ Page loads - HTTP 200
- ⚠️  Limited form validation - 2/5 types found
- **Result:** 7/8 checks passed (87%)

## 4.0 Visual Validation (Playwright)
- ✅ Homepage: tests/screenshots/homepage.png
- ✅ Dashboard: tests/screenshots/dashboard.png
- ✅ Product List: tests/screenshots/products.png

## 5.0 Accessibility Audit (Playwright)
- ✅ WCAG Level A: 0 violations
- ⚠️  WCAG Level AA: 2 warnings (color contrast)

## 6.0 Functional Validation (Playwright)
- ✅ Navigation works
- ✅ Forms submit correctly
- ✅ Data displays from seed

## 7.0 Issues Found
1. Low domain compliance score (37.5%) - Consider refactoring local models (Code Quality)
2. Color contrast on secondary buttons (warning - Playwright)
3. Missing alt text on logo (minor - Playwright)
4. Limited form validation attributes (warning - CLI)

## 8.0 Status
**PASS** - Ready for Phase 9 refinement
```

**🚨 ENFORCEMENT:**
- **ALL projects** MUST run code quality checks (guardrail + domain usage) in PARALLEL before Phase 9
- **Web/UI projects** MUST complete visual validation (Playwright) before Phase 9
- Validation report MUST be generated (with screenshots for web/UI)
- Guardrail report MUST be saved to `validation/guardrail-report.txt`
- Domain usage report MUST be saved to `validation/domain-usage-report.txt`
- Startup script MUST work for web/UI projects (seeded environment required)
- Critical issues MUST be fixed before Phase 9
- Guardrail violations MUST be resolved or approved before Phase 9
- Low domain compliance (<25%) should have action plan for refactoring

**Exit Criteria:**
- ✅ Guardrail enforcement report generated (no violations OR approved)
- ✅ Domain usage report generated and saved
- ✅ Both code quality checks run in parallel (efficiency validated)
- ✅ Validation report complete with all sections
- ✅ Screenshots captured (web/UI projects only)
- ✅ Startup script verified (web/UI projects only)
- ✅ Critical issues fixed or documented for Phase 9
- ✅ Action items identified for domain model refactoring (if needed)
- ✅ Ready for Phase 9 refinement

---

