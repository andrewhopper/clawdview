## 🧬 GENETIC AI: DIVERGENT IMPLEMENTATIONS

**Concept:** Create N maximally diverse implementations to explore solution space, like genetic diversity in evolution.

**Purpose:**
- Explore multiple solution approaches simultaneously
- Compare trade-offs empirically (performance, maintainability, DX)
- Discover unexpected optimal solutions
- Learn which patterns work best for problem class
- Generate reusable patterns for future prototypes

### When to Use Divergent Mode

**✅ USE when:**
- Problem has multiple valid solution approaches
- Unclear which architecture/tech stack is optimal
- High-value decision (client deliverable, production system)
- Learning opportunity (comparing frameworks, patterns)
- Risk mitigation (hedge against single approach failure)

**❌ DON'T USE when:**
- Simple, well-understood problem
- Clear single optimal approach
- Time-constrained (adds 2-3x development time)
- Low-value prototype (internal POC, throwaway spike)
- Track A testing (divergent requires Track B)

### Divergent SDLC Path

**Standard Path:** 1→2→3→4→5→6→7→8→9
**Divergent Path:** 1→2→3→4→5→6→7→**8.1**→**8.2**→**8.3**

**New Phases:**
- **Phase 8.1 (Divergent Implementation):** Implement N variants in parallel
- **Phase 8.2 (Divergent Evaluation):** Compare variants, run benchmarks, assess trade-offs
- **Phase 8.3 (Convergence):** Select winner, create hybrid, or graduate multiple

### Divergence Declaration (Phase 7→8.1)

**At Phase 7 completion, user declares divergence:**

```
divergent --width=3 --depth=1 --diversity=tech_stack,architecture,ui,styles --criteria=performance,developer_experience
```

**Genetic Algorithm Parameters:**

- **Width:** Number of variants per generation (population size)
  - Default: 3
  - Range: 2-5 recommended (exponential growth at depth > 1)

- **Depth:** Number of generations (evolutionary iterations)
  - Default: 1 (single generation)
  - Range: 1-3 recommended
  - **Depth 1:** Single generation (3 variants)
  - **Depth 2:** Two generations (3 → 9 variants total, 9 in final generation)
  - **Depth 3:** Three generations (3 → 9 → 27 variants total, 27 in final generation)

**Example: Multi-Generation Evolution**
```
# Single generation (default)
divergent --width=3 --depth=1

# Two generations: Create 3, each breeds 3 more (9 final candidates)
divergent --width=3 --depth=2

# Three generations: 3 → 9 → 27 final candidates
divergent --width=3 --depth=3
```

**⚠️ Exponential Growth Warning:**
- Width=3, Depth=2: 9 final variants
- Width=3, Depth=3: 27 final variants
- Width=4, Depth=3: 64 final variants
- **Recommendation:** Start with depth=1, only use depth > 1 for critical high-value decisions

**Step 1: Define Evaluation Criteria (Optional)**

User specifies what matters most for this project (used to weight Phase 8.2 evaluation):

```
--criteria=performance,cost,developer_experience,maintainability,time_to_market
--weights=performance:0.3,developer_experience:0.3,maintainability:0.2,cost:0.1,time_to_market:0.1
```

**Common Criteria:**
- **Performance:** Latency, throughput, resource efficiency
- **Cost:** Infrastructure, licensing, development time
- **Developer Experience:** Setup time, debugging, IDE support, learning curve
- **Maintainability:** Code readability, testability, upgrade path
- **Time to Market:** Implementation speed, library maturity
- **Scalability:** Horizontal/vertical scaling, load handling
- **User Experience:** Load times, interactivity, accessibility
- **Security:** Vulnerability surface, auth/authz complexity
- **Operational Excellence:** Monitoring, deployment, incident response

**Default weights** (if not specified): Equal weight across all criteria

**Step 2: AI Generates N Variant Proposals**

| Variant | Tech Stack | Architecture | UI | Styles | Trade-offs |
|---------|-----------|--------------|-----|--------|------------|
| A | Python + FastAPI | Async event-driven | React SPA | CSS-in-JS | High perf, complex, steep learning |
| B | TypeScript + Express | Sync REST | SSR (Next.js) | Tailwind | Simple, slower, great DX |
| C | Rust + Actix | Actor model | Svelte SPA | CSS Modules | Fastest, hardest to maintain |

**User actions:** `accept`, `regenerate`, `customize: <feedback>`

### Diversity Dimensions

**Maximize diversity across:**

1. **Tech Stack:** Language, framework, runtime
   - Example: Python vs TypeScript vs Rust
   - Example: FastAPI vs Express vs Actix

2. **Architecture:** System design, communication patterns
   - Monolith vs microservices
   - Sync vs async
   - Event-driven vs request-response
   - Serverless vs containers vs bare metal
   - Layered vs hexagonal vs clean architecture

3. **Algorithm:** Core problem-solving approach
   - Recursive vs iterative
   - Graph traversal vs dynamic programming
   - Rule-based vs ML-based
   - Batch vs streaming

4. **Data Models:** Schema design, storage strategy
   - SQL vs NoSQL vs in-memory vs graph
   - B-tree vs hash table vs LSM tree
   - Normalized vs denormalized
   - Document-oriented vs relational vs key-value
   - Schema-first vs schema-less

5. **User Interface:** UI paradigm and interaction model
   - SPA vs MPA vs SSR vs SSG
   - React vs Vue vs Svelte vs vanilla
   - Component-driven vs template-driven
   - Client-side routing vs server routing
   - Real-time (WebSocket) vs polling vs server-sent events

6. **Styles:** Styling approach and design system
   - CSS-in-JS vs CSS Modules vs Tailwind vs Sass
   - Utility-first vs semantic CSS vs atomic CSS
   - Design tokens vs hardcoded values
   - Theme switching approach (CSS vars, styled-components, etc.)
   - Responsive strategy (mobile-first vs desktop-first vs container queries)

7. **Sitemap/Navigation:** Information architecture
   - Flat vs hierarchical vs faceted
   - Single-level vs multi-level navigation
   - Sidebar vs top nav vs command palette
   - Tab-based vs wizard vs dashboard layout
   - URL structure (RESTful vs slug-based vs hash-based)

8. **Page Structure:** Layout and composition patterns
   - Grid-based vs flexbox vs absolute positioning
   - Single column vs multi-column vs masonry
   - Header-content-footer vs split-pane vs card-based
   - Infinite scroll vs pagination vs load-more
   - Modal-heavy vs inline editing vs dedicated pages

9. **Patterns:** Code organization, paradigms
   - OOP vs functional vs procedural
   - Imperative vs declarative
   - Repository pattern vs active record
   - MVC vs MVVM vs clean architecture

10. **Performance Strategy:** Optimization approach
    - CPU-optimized vs memory-optimized
    - Latency-optimized vs throughput-optimized
    - Caching strategy (CDN, Redis, in-memory)
    - Bundle splitting strategies
    - Lazy loading vs eager loading vs prefetching

**🚨 CRITICAL:** AI must maximize Hamming distance between variants across all dimensions.

### Multi-Generation Evolution (Depth > 1)

**Concept:** Create generations of variants, where each generation's best performers breed the next generation.

**Generational Flow (Example: Width=3, Depth=2):**

**Generation 1 (G1):** Create 3 maximally diverse variants
- G1-A: Python + FastAPI + React SPA
- G1-B: TypeScript + Express + Next.js SSR
- G1-C: Rust + Actix + Svelte SPA

**Evaluation:** Run Phase 8.2 evaluation on G1 variants

**Selection:** Select top N parents for breeding (default: all pass tests)
- If all variants pass tests → all breed
- If some fail → only passing variants breed

**Generation 2 (G2):** Each G1 parent breeds WIDTH children (crossover + mutation)
- G1-A breeds → G2-A1, G2-A2, G2-A3
  - **G2-A1:** Python + FastAPI + Vue SPA (mutate UI from parent A)
  - **G2-A2:** Python + Actix + React SPA (crossover: A's language + C's framework)
  - **G2-A3:** Go + FastAPI + React SPA (mutate language from parent A)
- G1-B breeds → G2-B1, G2-B2, G2-B3
- G1-C breeds → G2-C1, G2-C2, G2-C3

**Final Evaluation:** Evaluate all 9 G2 variants, select winner

**Breeding Strategies:**

1. **Mutation:** Single dimension change from parent
   - Parent: Python + FastAPI + React
   - Child: **TypeScript** + FastAPI + React (mutate tech_stack)

2. **Crossover:** Combine traits from two parents
   - Parent A: Python + FastAPI + React
   - Parent B: Rust + Actix + Svelte
   - Child: Python + **Actix** + React (A's language + B's framework + A's UI)

3. **Hybrid:** Combination of mutation + crossover
   - Apply crossover, then mutate result

**🚨 CRITICAL:** Each generation must maximize diversity within that generation while maintaining lineage from parent.

**Variant Naming Convention:**
- **G1:** `{name}-{5char}-variant-A`, `{name}-{5char}-variant-B`, `{name}-{5char}-variant-C`
- **G2:** `{name}-{5char}-variant-A1`, `{name}-{5char}-variant-A2`, `{name}-{5char}-variant-B1`, etc.
- **G3:** `{name}-{5char}-variant-A1a`, `{name}-{5char}-variant-A1b`, `{name}-{5char}-variant-A2a`, etc.

**When to Use Depth > 1:**
- ✅ Extremely high-value decision (production system, major investment)
- ✅ Unclear optimal approach after Phase 4 analysis
- ✅ Learning goal: explore solution space comprehensively
- ✅ Research project with publication intent
- ❌ Time-constrained projects
- ❌ Clear leading candidate exists
- ❌ Resource-limited teams

**Evaluation Strategy:**
- **Generational (Default):** Evaluate each generation, breed from top performers
- **Final Only:** Skip intermediate evaluations, only evaluate final generation (faster but less selective)

### Directory Structure (Divergent Mode)

**Single Generation (Depth=1):**
```
projects/{classification}/active/{name}-{5char}/              # Parent (tests only)
├── tests/                              # Shared test suite (all variants must pass)
│   ├── e2e/                            # End-to-end tests
│   ├── integration/                    # Integration tests
│   └── uat/                            # UAT automation
├── README.md                           # Parent overview, variant comparison
├── .project                            # Parent metadata
└── DIVERGENT_SPEC.md                   # Variant proposals, diversity matrix

projects/{classification}/active/{name}-{5char}-variant-A/   # Variant A (Generation 1)
├── src/                                # Implementation A
├── README.md                           # Variant-specific details
├── .project                            # Links to parent
├── playwright.config.ts                # Points to parent tests
└── VARIANT_NOTES.md                    # Design decisions, trade-offs

projects/{classification}/active/{name}-{5char}-variant-B/   # Variant B (Generation 1)
├── src/                                # Implementation B (maximally different)
├── README.md
├── .project
├── playwright.config.ts
└── VARIANT_NOTES.md

projects/{classification}/active/{name}-{5char}-variant-C/   # Variant C (Generation 1)
├── src/                                # Implementation C (maximally different)
├── README.md
├── .project
├── playwright.config.ts
└── VARIANT_NOTES.md

projects/{classification}/active/{name}-{5char}-evaluation/  # Phase 8.2 artifacts
├── BENCHMARKS.md                       # Performance comparisons
├── MAINTAINABILITY.md                  # Code quality, DX analysis
├── TRADE_OFFS.md                       # Comprehensive comparison
└── RECOMMENDATION.md                   # AI recommendation + rationale
```

**Multi-Generation (Depth=2, Width=3):**
```
projects/{classification}/active/{name}-{5char}/              # Parent (tests only)
├── tests/                              # Shared test suite
├── README.md                           # Overview, generational lineage
├── .project                            # Parent metadata (width=3, depth=2)
└── DIVERGENT_SPEC.md                   # Generation proposals

# Generation 1 (G1)
projects/{classification}/active/{name}-{5char}-variant-A/   # G1 Parent A
projects/{classification}/active/{name}-{5char}-variant-B/   # G1 Parent B
projects/{classification}/active/{name}-{5char}-variant-C/   # G1 Parent C

# Generation 1 Evaluation
projects/{classification}/active/{name}-{5char}-evaluation-g1/
├── BENCHMARKS.md                       # G1 performance data
├── TRADE_OFFS.md                       # G1 comparison
└── BREEDING_PLAN.md                    # G2 breeding strategy

# Generation 2 (G2) - Children of A
projects/{classification}/active/{name}-{5char}-variant-A1/  # A's child 1 (mutate UI)
projects/{classification}/active/{name}-{5char}-variant-A2/  # A's child 2 (crossover A+C)
projects/{classification}/active/{name}-{5char}-variant-A3/  # A's child 3 (mutate language)

# Generation 2 - Children of B
projects/{classification}/active/{name}-{5char}-variant-B1/
projects/{classification}/active/{name}-{5char}-variant-B2/
projects/{classification}/active/{name}-{5char}-variant-B3/

# Generation 2 - Children of C
projects/{classification}/active/{name}-{5char}-variant-C1/
projects/{classification}/active/{name}-{5char}-variant-C2/
projects/{classification}/active/{name}-{5char}-variant-C3/

# Final Evaluation (G2)
projects/{classification}/active/{name}-{5char}-evaluation-final/
├── BENCHMARKS.md                       # G2 performance data
├── GENERATIONAL_ANALYSIS.md            # Cross-generation insights
├── TRADE_OFFS.md                       # G2 comparison
└── RECOMMENDATION.md                   # Winner selection
```

**Naming Convention:**
- **Depth=1:** `{name}-{5char}-variant-{A,B,C,...}`
- **Depth=2:** `{name}-{5char}-variant-{A1,A2,A3,B1,B2,B3,...}`
- **Depth=3:** `{name}-{5char}-variant-{A1a,A1b,A1c,A2a,A2b,A2c,...}`

### Phase 8.1: Divergent Implementation

**Goal:** Implement all N variants in parallel, each passing shared test suite

**Single Generation (Depth=1):**

**Activities:**
- Implement variant A using approach A
- Implement variant B using approach B (maximally different)
- Implement variant C using approach C (maximally different)
- Each variant must pass ALL tests in parent `tests/` directory
- Document design decisions in VARIANT_NOTES.md

**Parallel Execution:**
- Use Task tool to launch WIDTH agents in parallel (one per variant)
- Each agent implements one variant independently
- All agents reference same test suite

**TDD Workflow (per variant):**
1. Pick failing test from parent test suite
2. Write minimal code to pass test
3. Run tests → verify green
4. Refactor within variant's architectural constraints
5. Repeat until all tests pass

**Exit Criteria (Depth=1):**
- All WIDTH variants implemented
- Each variant passes ALL shared tests
- VARIANT_NOTES.md documents trade-offs
- Code runs successfully

---

**Multi-Generation (Depth > 1):**

**Generation 1 (G1):**
1. Generate WIDTH maximally diverse variants (same as Depth=1)
2. Implement all G1 variants in parallel
3. **Mini-Evaluation:** Lightweight evaluation of G1 variants
   - Run shared tests (all must pass)
   - Quick performance benchmarks
   - Document trade-offs in `evaluation-g1/TRADE_OFFS.md`
4. **Selection:** Identify which G1 variants breed (default: all that pass tests)
5. **Breeding Plan:** AI generates breeding strategy
   - Mutation targets (which dimensions to mutate)
   - Crossover pairs (which parents to combine)
   - Document in `evaluation-g1/BREEDING_PLAN.md`

**Generation 2 (G2):**
1. Each G1 parent breeds WIDTH children
   - Child 1: Pure mutation (change 1-2 dimensions)
   - Child 2: Crossover (combine traits from 2 parents)
   - Child 3: Hybrid (crossover + mutation)
2. Implement all G2 variants in parallel (WIDTH × G1_survivors variants)
3. Each G2 variant must pass shared tests
4. Document lineage and mutations in VARIANT_NOTES.md

**Generation 3+ (if Depth=3):**
- Repeat G2 process using G2's top performers as parents

**Exit Criteria (Depth > 1):**
- All final generation variants implemented
- Each passes ALL shared tests
- Lineage documented (parent → child relationships)
- Mutation/crossover strategy documented per variant
- Generational evaluation complete

### Phase 8.2: Divergent Evaluation

**Goal:** Compare variants empirically, document trade-offs, recommend path forward

**Uses evaluation criteria and weights from Phase 7→8.1 declaration**

**Evaluation Dimensions:**

1. **Performance Benchmarks**
   - Latency (p50, p95, p99)
   - Throughput (requests/sec)
   - Resource usage (CPU, memory, disk)
   - Cold start time (serverless)
   - Build time, bundle size

2. **Code Quality**
   - Lines of code (LOC)
   - Cyclomatic complexity
   - Test coverage
   - Type safety
   - Error handling robustness

3. **Developer Experience**
   - Setup time (0→running)
   - Debugging ease
   - IDE support
   - Documentation quality
   - Community/library ecosystem

4. **Maintainability**
   - Code readability
   - Testability
   - Modularity
   - Dependency count/freshness
   - Upgrade path

5. **Operational Concerns**
   - Deployment complexity
   - Monitoring/observability
   - Scaling characteristics
   - Cost (compute, storage, egress)
   - Security posture

**Deliverables:**
- BENCHMARKS.md - Performance data (tables, charts)
- MAINTAINABILITY.md - Code quality analysis
- TRADE_OFFS.md - Comprehensive comparison matrix
- RECOMMENDATION.md - AI recommendation with rationale

**Comparison Matrix Example:**

| Dimension | Variant A | Variant B | Variant C | Winner |
|-----------|-----------|-----------|-----------|--------|
| Latency (p95) | 45ms | 120ms | 12ms | C |
| Throughput | 5k req/s | 2k req/s | 15k req/s | C |
| LOC | 850 | 420 | 1200 | B |
| Setup Time | 5min | 2min | 15min | B |
| Memory (peak) | 200MB | 150MB | 80MB | C |
| DX Score | 7/10 | 9/10 | 5/10 | B |
| **Weighted** | **6.8/10** | **6.2/10** | **7.5/10** | **C** |

**Exit Criteria:**
- All evaluation docs complete
- Benchmarks run, data collected
- Trade-offs analyzed according to user-defined criteria
- Weighted scores calculated
- Recommendation documented

### Phase 8.3: Convergence

**Goal:** Select path forward, archive losers, graduate winner(s)

**Convergence Options:**

**Option 1: Single Winner**
- Select best variant based on evaluation
- Graduate winner to `{name}-{5char}/` (move src/ from variant)
- Archive losers to `archived/{name}-{5char}-variant-{B,C}/`
- Document learnings in LEARNINGS.md

**Option 2: Hybrid Approach**
- Combine best features from multiple variants
- Create new implementation in `{name}-{5char}/`
- Use variant A's architecture + variant C's algorithm
- Archive original variants
- Document hybrid design in HYBRID_DESIGN.md

**Option 3: Graduate Multiple**
- Keep 2+ variants as separate projects
- Rename to distinct use cases: `{name}-fast-{5char}/`, `{name}-simple-{5char}/`
- Each serves different audience/requirements
- Document when to use each in parent README.md

**Option 4: Further Evolution**
- Select top 2 variants as "parents"
- Generate new variants by crossover/mutation
- Repeat Phase 8.1→8.2→8.3 (genetic algorithm iteration)
- Rare, only for high-value/complex problems

**Deliverables:**
- Updated parent README.md with convergence decision
- LEARNINGS.md documenting insights
- Archived variants (if applicable)
- Final prototype in standard location

**Exit Criteria:**
- Convergence decision made
- Learnings documented
- Production-ready code in standard location
- All variants accounted for (graduated or archived)

### .project Metadata (Divergent Mode)

**Parent .project** (`projects/{classification}/active/{name}-{5char}/.project`):
```json
{
  "name": "{name}-{5char}",
  "current_phase": "DIVERGENT_IMPLEMENTATION",
  "phase_number": 8.1,
  "divergent_mode": {
    "enabled": true,
    "width": 3,
    "depth": 2,
    "current_generation": 1,
    "total_variants": 9,
    "diversity_targets": ["tech_stack", "architecture", "ui", "styles", "data_models"],
    "evaluation_criteria": {
      "criteria": ["performance", "developer_experience", "maintainability", "cost"],
      "weights": {
        "performance": 0.3,
        "developer_experience": 0.3,
        "maintainability": 0.2,
        "cost": 0.2
      }
    },
    "generations": [
      {
        "generation": 1,
        "variants": [
          { "id": "variant-A", "path": "projects/{classification}/active/{name}-{5char}-variant-A", "status": "COMPLETED", "parent": null },
          { "id": "variant-B", "path": "projects/{classification}/active/{name}-{5char}-variant-B", "status": "COMPLETED", "parent": null },
          { "id": "variant-C", "path": "projects/{classification}/active/{name}-{5char}-variant-C", "status": "COMPLETED", "parent": null }
        ],
        "evaluation": "projects/{classification}/active/{name}-{5char}-evaluation-g1/"
      },
      {
        "generation": 2,
        "variants": [
          { "id": "variant-A1", "path": "projects/{classification}/active/{name}-{5char}-variant-A1", "status": "IMPLEMENTATION", "parent": "variant-A", "strategy": "mutation" },
          { "id": "variant-A2", "path": "projects/{classification}/active/{name}-{5char}-variant-A2", "status": "IMPLEMENTATION", "parent": "variant-A", "strategy": "crossover" },
          { "id": "variant-A3", "path": "projects/{classification}/active/{name}-{5char}-variant-A3", "status": "PENDING", "parent": "variant-A", "strategy": "hybrid" }
        ],
        "evaluation": "projects/{classification}/active/{name}-{5char}-evaluation-final/"
      }
    ],
    "shared_tests": "projects/{classification}/active/{name}-{5char}/tests/",
    "convergence_decision": null
  },
  "metadata": {
    "test_track": "B",
    "prototype_type": "divergent"
  }
}
```

**Variant .project - G1 Parent** (`projects/{classification}/active/{name}-{5char}-variant-A/.project`):
```json
{
  "name": "{name}-{5char}-variant-A",
  "current_phase": "DIVERGENT_IMPLEMENTATION",
  "phase_number": 8.1,
  "divergent_mode": {
    "is_variant": true,
    "parent_project": "{name}-{5char}",
    "variant_id": "variant-A",
    "generation": 1,
    "parent_variant": null,
    "breeding_strategy": null,
    "shared_tests": "../{name}-{5char}/tests/",
    "diversity_profile": {
      "tech_stack": "Python + FastAPI",
      "architecture": "Async event-driven",
      "algorithm": "Graph traversal",
      "data_models": "PostgreSQL normalized",
      "ui": "React SPA",
      "styles": "CSS-in-JS (styled-components)",
      "sitemap": "Hierarchical sidebar nav",
      "page_structure": "Grid-based layout",
      "patterns": "Clean architecture",
      "performance_strategy": "Latency-optimized"
    }
  },
  "metadata": {
    "test_track": "B",
    "prototype_type": "divergent_variant"
  }
}
```

**Variant .project - G2 Child** (`projects/{classification}/active/{name}-{5char}-variant-A1/.project`):
```json
{
  "name": "{name}-{5char}-variant-A1",
  "current_phase": "DIVERGENT_IMPLEMENTATION",
  "phase_number": 8.1,
  "divergent_mode": {
    "is_variant": true,
    "parent_project": "{name}-{5char}",
    "variant_id": "variant-A1",
    "generation": 2,
    "parent_variant": "variant-A",
    "breeding_strategy": "mutation",
    "mutations": ["ui"],
    "mutation_details": {
      "ui": {
        "from": "React SPA",
        "to": "Vue SPA",
        "rationale": "Explore simpler reactive model"
      }
    },
    "shared_tests": "../{name}-{5char}/tests/",
    "diversity_profile": {
      "tech_stack": "Python + FastAPI",
      "architecture": "Async event-driven",
      "algorithm": "Graph traversal",
      "data_models": "PostgreSQL normalized",
      "ui": "Vue SPA",
      "styles": "CSS-in-JS (styled-components)",
      "sitemap": "Hierarchical sidebar nav",
      "page_structure": "Grid-based layout",
      "patterns": "Clean architecture",
      "performance_strategy": "Latency-optimized"
    }
  },
  "metadata": {
    "test_track": "B",
    "prototype_type": "divergent_variant"
  }
}
```

### AI Responsibilities (Divergent Mode)

**Phase 7→8.1 Transition:**
- Capture user-defined evaluation criteria and weights
- Capture width and depth parameters
- Generate WIDTH maximally diverse G1 variant proposals across all specified dimensions
- Create diversity matrix showing Hamming distance
- Present proposals for user approval

**Phase 8.1 (Single Generation):**
- Implement all WIDTH variants in parallel (use Task tool)
- Ensure each variant passes shared test suite
- Document design decisions per variant
- Flag if variant cannot pass tests (fundamental incompatibility)

**Phase 8.1 (Multi-Generation):**
- **Generation 1:**
  - Implement WIDTH maximally diverse G1 variants in parallel
  - Run mini-evaluation (quick benchmarks, test pass/fail)
  - Document G1 trade-offs
  - Generate breeding plan for G2
- **Generation 2+:**
  - For each G1 parent, generate WIDTH breeding proposals
    - Child 1: Mutation strategy (1-2 dimension changes)
    - Child 2: Crossover strategy (combine 2 parents)
    - Child 3: Hybrid strategy (crossover + mutation)
  - Implement all G2 variants in parallel (WIDTH × G1_parents)
  - Document lineage (parent → child) and mutation details
  - Repeat for Generation 3 if depth=3
- Track generational metadata in parent `.project`

**Phase 8.2:**
- Run performance benchmarks for all **final generation** variants
- Analyze code quality metrics
- Assess ALL user-defined evaluation criteria
- Generate comparison matrices weighted by user-defined criteria
- **Multi-Generation:** Include generational analysis (G1 vs G2 improvements)
- Provide weighted recommendation with rationale based on criteria

**Phase 8.3:**
- Recommend convergence strategy (winner, hybrid, multiple) based on weighted evaluation
- **Multi-Generation:** Document generational insights (which breeding strategies worked)
- Archive non-selected variants (preserve all generations)
- Update parent prototype with final implementation

### Enforcement Rules

**🚨 CRITICAL:**
- Divergent mode REQUIRES Track B testing (comprehensive)
- All variants MUST pass same test suite (no variant-specific tests)
- AI MUST maximize diversity (minimize similarity) across ALL specified dimensions
- Phase 8.2 evaluation MUST be data-driven (benchmarks, metrics) weighted by user-defined criteria
- Convergence decision MUST be documented with rationale tied to evaluation criteria

**Phase Restrictions:**
- Cannot enter divergent mode from Track A (must be Track B)
- Cannot skip Phase 8.2 evaluation (required before convergence)
- Cannot mix divergent and standard phases (all-or-nothing)
- Must define evaluation criteria before Phase 8.1 (can use defaults)
- Must define width and depth before Phase 8.1 (defaults: width=3, depth=1)

**Multi-Generation Rules (Depth > 1):**
- Each generation must be fully implemented before next generation starts
- All G1 variants must pass tests before breeding G2
- Mini-evaluation required between generations (document in `evaluation-g{N}/`)
- Breeding plan must document mutation/crossover strategy
- Child variants must maintain lineage metadata (parent_variant, breeding_strategy)
- Cannot skip generations (must go 1→2→3, not 1→3)
- All generations share same test suite and evaluation criteria

**Example Diversity Validation:**

❌ **Insufficient Diversity:**
- Variant A: Python + Flask
- Variant B: Python + FastAPI
- Variant C: Python + Django
- **Problem:** All Python, all sync frameworks (low Hamming distance)

✅ **Maximal Diversity:**
- Variant A: Python + FastAPI (async, high-level)
- Variant B: TypeScript + Express (sync, mid-level)
- Variant C: Rust + Actix (actor model, low-level)
- **Success:** Different languages, runtimes, paradigms (high Hamming distance)

### Success Criteria (Divergent Mode)

**Successful divergent exploration:**
- N variants implemented, all pass tests
- Empirical data collected across evaluation dimensions
- Clear winner or convergence strategy identified
- Learnings documented (when to use each approach)
- Reusable patterns extracted for future prototypes
- Decision rationale clear and defensible

**Bonus:**
- Unexpected optimal solution discovered
- New patterns added to hmode/shared/standards/code/
- Blog post or case study material
- Contribution to open-source ecosystem

---

