# Component Decomposition Pattern

**When to decompose Phase 6 design:**
- 5+ major modules/services
- Multi-domain system (auth + data + UI + API)
- ARCHITECTURE.md exceeds 2 pages
- Multiple teams/developers

**Component-Based Structure:**
```
design/
├── SPECIFICATION.md           # System-level spec
├── ARCHITECTURE.md            # High-level architecture
├── COMPONENT_INDEX.md         # Component catalog + dependencies
├── IMPLEMENTATION_PLAN.md     # Cross-component integration
├── TECH_STACK.md
├── RISKS.md
└── specs/                     # Component specifications
    ├── authentication/
    │   ├── SPECIFICATION.md
    │   ├── ARCHITECTURE.md
    │   └── IMPLEMENTATION_STRATEGY.md
    ├── data-processing/
    │   └── ...
    └── api-gateway/
        └── ...
```

**COMPONENT_INDEX.md Format:**
```markdown
# Component Index

## 1.0 Components

| Component | Purpose | Dependencies | Status |
|-----------|---------|--------------|--------|
| authentication | User auth + JWT | - | DESIGN |
| data-processing | ETL pipeline | authentication | DESIGN |
| api-gateway | REST API | authentication, data-processing | DESIGN |

## 2.0 Dependency Graph
```
authentication
    ↓
data-processing
    ↓
api-gateway
```

## 3.0 Integration Points
- authentication → api-gateway: JWT validation middleware
- data-processing → api-gateway: Async job queue
```

**Rules:**
- Each component has full design docs (SPEC + ARCH + IMPL_STRATEGY)
- COMPONENT_INDEX.md tracks dependencies (no circular deps)
- All component I/O contracts 100% specified
- Integration strategy documented in parent IMPLEMENTATION_PLAN.md

**See:** `hmode/docs/processes/PHASE_6_DESIGN.md` for full workflow
