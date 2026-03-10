## 🚨 ENFORCEMENT

**Before ANY action:**
1. **Apply confirmation protocol** (complex/ambiguous tasks → paraphrase + options + confirm)
2. **Check if modifying guardrail files** (hmode/guardrails/*, CLAUDE.md) → REQUIRE human approval first
3. Read `.project` file → determine current phase
4. Validate action allowed in phase
5. Update `.project` on transitions
6. **REFUSE code writing in phases 1-6**
7. **REFUSE implementation code in phase 7** (tests only!)
8. **REQUIRE startup script creation during Phase 8** (ALL projects: starts services + seeds data)
9. **REQUIRE tests to pass before phase 8→8.5 or 8→9 transition**
10. **REQUIRE Phase 8.5 for web/UI projects** (validation report + screenshots + startup script verification)
11. **ALLOW Phase 8→9 skip for non-visual projects** (CLIs, APIs, libraries - document in `.project`)
12. **REFUSE new features in phase 9** (polish only, fix Phase 8.5 issues)
13. **REQUIRE Track B for divergent mode** (no Track A divergent)
14. **REQUIRE all variants pass shared tests** (no variant-specific tests)
15. **REQUIRE Phase 8.2 evaluation before convergence** (no skipping Phase 8.2→8.3)
16. **REQUIRE evaluation criteria defined** (can use defaults if not specified)
17. **REQUIRE human approval for ALL technology decisions** (libraries, frameworks, infrastructure, services) before adding to tech preferences or implementing

**AI Partnership by Phase:**
- **SEED:** Clarify problem, ask questions, capture target output/audience, recommend test track + prototype type
- **RESEARCH:** Find existing solutions, compare tools, identify gaps, flag spikes needed
- **EXPANSION:** Generate approaches, explore "what ifs"
- **ANALYSIS:** Evaluate objectively, assess complexity/risk
- **SELECTION:** Recommend approach, define MVP, confirm test track selection, **generate 3 output/audience validation options** → user accepts/rejects
- **DESIGN:** Suggest architecture, validate tech choices, ensure I/O complete, **optionally generate UML class + sequence diagrams** (if requested or complex system), **automatically decompose into components if complex** (5+ modules, multi-domain, >2 page ARCHITECTURE.md), create COMPONENT_INDEX.md if applicable, ensure all component I/O contracts 100% specified, present UML for human approval before implementation strategy
- **TEST_DESIGN:**
  - **Step 1:** Download reference materials (Context7, GitHub, official docs), review internal hmode/shared/standards/code/, create REFERENCES.md
  - **Step 2:** Write Playwright tests per track (A=smoke, B=comprehensive) using reference patterns - TDD red phase
- **IMPLEMENTATION:** Write code to pass tests, run tests per track continuously (TDD green/refactor), **create startup script** (start services + seed data)
- **QUALITY_VALIDATION (8.5):** Run startup script, execute Playwright validation suite, capture screenshots, accessibility audit, generate validation report (web/UI projects only)
- **REFINEMENT:** UAT automation, polish, fix Phase 8.5 issues, document learnings
- **DIVERGENT_IMPLEMENTATION (8.1):** Capture evaluation criteria, generate N maximally diverse variants, implement in parallel, all pass shared tests
- **DIVERGENT_EVALUATION (8.2):** Benchmark variants, compare metrics weighted by criteria, analyze trade-offs, recommend convergence
- **CONVERGENCE (8.3):** Select winner/hybrid/multiple based on weighted evaluation, document learnings, archive non-selected variants

