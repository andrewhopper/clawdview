## 🔒 PHASE TRANSITIONS

**Sequential Only:** 1→2→3→4→5→6→7→8→9
**Spike Exception:** 1→SPIKE IMPLEMENTATION→Findings (throwaway, max 3 days)
**Divergent Path:** 1→2→3→4→5→6→7→8.1→8.2→8.3 (N parallel implementations)
**Phase 6→7:** Select test track (A/B), create feature files and directory structure (NO implementation code)
**Phase 7→8:** ONLY transition allowing implementation code creation (standard path)
**Phase 7→8.1:** Divergent implementation (define criteria, N variants in parallel, Track B required)
**Phase 8→9:** Track A requires smoke scenarios pass, Track B requires all scenarios pass + coverage target
**Phase 8.1→8.2:** All variants complete, all pass shared scenarios
**Phase 8.2→8.3:** Evaluation complete (weighted by criteria), convergence decision made
**Backward:** Major pivot → SEED, architecture change → TECHNICAL DESIGN, scenario strategy change → TEST DESIGN
**Track Upgrade:** A→B anytime, document in `.project` phase_history
**Divergent Entry:** Only from Track B (Phase 7), cannot switch mid-implementation



## 📋 PHASE TRANSITION CHECKPOINTS

**Standard Path:**
**1→2:** Seed doc complete, problem clear, test track recommended, `.project` updated, ZERO code
**2→3:** Existing solutions researched, comparison table complete, spikes identified, `.project` updated, ZERO code
**3→4:** 5-10 approaches, `.project` updated, ZERO code
**4→5:** All analyzed, matrix complete, `.project` updated, ZERO code
**5→6:** Approach selected, MVP defined, test track confirmed, `.project` updated, ZERO code
**6→7:** All docs complete (base docs + component specs if decomposed), COMPONENT_INDEX.md if components exist, all component I/O contracts 100%, no circular dependencies, integration strategy documented, UML diagrams **human-approved** ✅ (if used), implementation strategy **human-approved** ✅, test track selected in `.project`, ZERO code → **REFERENCE COLLECTION + SCENARIO CREATION BEGIN**
**7→8:** References downloaded + REFERENCES.md complete, all Gherkin scenarios written per track, scenarios run and fail (BDD failing scenarios), step definitions stubbed, `.project` updated, ZERO implementation code → **IMPLEMENTATION BEGINS**
**8→8.5 (Web/UI projects):** All scenarios pass per track, features complete, code runs, **startup script created** (starts services + seeds data), `.project` updated → **QUALITY VALIDATION BEGINS**
**8→9 (Non-visual projects):** Skip Phase 8.5, proceed directly to refinement (document skip in `.project`)
**8.5→9:** Validation report complete with screenshots, startup script verified working, seed data functional, accessibility audit complete, critical issues fixed, `.project` updated → **REFINEMENT BEGINS**
**9→COMPLETE:** UAT scenarios complete per track, all scenarios pass, Phase 8.5 issues resolved, docs complete, `.project` set to final status

**Divergent Path (Single Generation - Depth=1):**
**7→8.1:** Divergence declared, evaluation criteria + weights defined (or defaults), width/depth set, WIDTH variant proposals generated and approved across specified dimensions, parent `.project` updated with `divergent_mode`, Track B required → **DIVERGENT IMPLEMENTATION BEGINS**
**8.1→8.2:** All WIDTH variants complete, each passes ALL shared scenarios, VARIANT_NOTES.md written per variant, `.project` updated → **EVALUATION BEGINS**
**8.2→8.3:** BENCHMARKS.md, MAINTAINABILITY.md, TRADE_OFFS.md, RECOMMENDATION.md complete, empirical data collected and weighted by criteria, `.project` updated → **CONVERGENCE BEGINS**
**8.3→COMPLETE:** Convergence decision executed (winner selected/hybrid created/multiple graduated), LEARNINGS.md written with criteria-based rationale, non-selected variants archived, final `.project` status set

**Divergent Path (Multi-Generation - Depth > 1):**
**7→8.1-G1:** Divergence declared with width/depth, WIDTH G1 variants proposed and approved → **G1 IMPLEMENTATION BEGINS**
**8.1-G1→8.1-G1-EVAL:** All WIDTH G1 variants complete and pass scenarios, VARIANT_NOTES.md per variant → **G1 MINI-EVALUATION**
**8.1-G1-EVAL→8.1-G2:** G1 evaluated, breeding plan generated (mutation/crossover strategies), WIDTH × G1_parents G2 proposals created → **G2 IMPLEMENTATION BEGINS**
**8.1-G2→8.1-G2-EVAL (if depth=3):** All G2 variants complete and pass scenarios → **G2 MINI-EVALUATION** → G3 breeding
**8.1-G{N}→8.2:** All final generation variants complete, each passes scenarios, lineage documented → **FINAL EVALUATION BEGINS**
**8.2→8.3:** Final evaluation complete (includes generational analysis), weighted by criteria, GENERATIONAL_ANALYSIS.md written → **CONVERGENCE BEGINS**
**8.3→COMPLETE:** Convergence decision with generational insights, all generations archived, winner graduated

**Spike Path:**
**1→SPIKE:** Problem clear, technical question defined, 3-day time-box set, `prototype_type: "spike"` in `.project`
**SPIKE→FINDINGS:** Code exploration complete (throwaway), findings doc written, go/no-go decision documented
**FINDINGS→1 (if go):** Delete spike code, start new prototype with full SDLC + BDD

