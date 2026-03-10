## 📊 PHASE TRACKING: `.project` FILE

**Location:**
- Phases 1-6: `ideas/proto-name-xxxxx-NNN-name/.project`
- Phases 7-9: `prototypes/proto-name-xxxxx-NNN-name/.project`

**Format (JSON):**
```json
{
  "name": "proto-001-example",
  "version": "0.5.0",
  "current_phase": "TECHNICAL_DESIGN",
  "phase_number": 5,
  "started": "2025-01-15T10:00:00Z",
  "last_updated": "2025-01-17T14:30:00Z",
  "phase_history": [
    { "phase": "SEED", "phase_number": 1, "started": "...", "completed": "...", "deliverables_completed": true }
  ],
  "version_history": [
    { "version": "0.1.0", "date": "2025-01-15T10:00:00Z", "phase": "SEED", "change_type": "major", "description": "Initial project creation" },
    { "version": "0.2.0", "date": "2025-01-15T12:00:00Z", "phase": "RESEARCH", "change_type": "minor", "description": "Phase transition to RESEARCH" },
    { "version": "0.5.0", "date": "2025-01-17T14:30:00Z", "phase": "TECHNICAL_DESIGN", "change_type": "minor", "description": "Phase transition to TECHNICAL_DESIGN" }
  ],
  "status": "ACTIVE",
  "description": "Brief description",
  "success_criteria": ["Criterion 1"],
  "metadata": {
    "tech_stack": [],
    "priority": "high",
    "test_track": "A",
    "prototype_type": "standard",
    "target_output": "CLI tool",
    "target_audience": "SREs",
    "target_company_maturity": ["poc", "mvp", "pmf"],
    "output_validation": {
      "validated_at": "2025-01-15T10:00:00Z",
      "selected_option": "A",
      "user_action": "accept"
    }
  }
}
```

### Semantic Versioning

**Format:** `MAJOR.MINOR.PATCH` (e.g., "1.2.3")

**Version Increment Rules:**

**MAJOR version (X.0.0):**
- Phase milestone transitions:
  - `0.x.x`: Ideas phase (Phases 1-6)
  - `1.x.x`: Implementation phase (Phases 7-8)
  - `2.x.x`: Completed/Refinement phase (Phase 9+)
  - `3.x.x`: Graduated status
- Status changes: ACTIVE → COMPLETED, COMPLETED → GRADUATED
- Breaking architecture changes requiring redesign
- Divergent mode convergence (8.3 → final)

**MINOR version (x.Y.0):**
- Phase transitions within same major milestone
  - Ideas phases: 0.1.0 (SEED) → 0.2.0 (RESEARCH) → 0.3.0 (EXPANSION) → etc.
  - Implementation: 1.0.0 (TEST_DESIGN) → 1.1.0 (IMPLEMENTATION)
- Track upgrade (A → B)
- Adding significant features or metadata
- Divergent mode activation
- Sub-phase transitions (8.1 → 8.2 → 8.3)

**PATCH version (x.x.Z):**
- Documentation updates
- Metadata updates (description, last_updated)
- Success criteria refinements
- Bug fixes in deliverables
- Minor phase_history updates

**Initial Versions:**
| Phase Range | Version Range | Description |
|-------------|---------------|-------------|
| Phase 1 (SEED) | 0.1.x | Initial concept |
| Phases 2-6 (Ideas) | 0.2.x - 0.7.x | Research and design (includes 5.5) |
| Phases 7-8 (Implementation) | 1.0.x - 1.1.x | Development |
| Phase 9 (Refinement) | 2.0.x | Polish and UAT |
| COMPLETED | 2.1.0+ | Production ready |
| GRADUATED | 3.0.0+ | Standalone project |

**Version History:**
- Track all version changes with: version, date, phase, change_type, description
- `change_type`: "major" | "minor" | "patch"
- Required for all version bumps
- Provides audit trail of project evolution

**Examples:**

```json
{
  "version": "0.1.0",
  "version_history": [
    {
      "version": "0.1.0",
      "date": "2025-01-15T10:00:00Z",
      "phase": "SEED",
      "change_type": "major",
      "description": "Initial project creation"
    }
  ]
}
```

```json
{
  "version": "1.0.0",
  "version_history": [
    {
      "version": "1.0.0",
      "date": "2025-01-20T14:00:00Z",
      "phase": "TEST_DESIGN",
      "change_type": "major",
      "description": "Transition to implementation phase"
    }
  ]
}
```

```json
{
  "version": "2.0.0",
  "version_history": [
    {
      "version": "2.0.0",
      "date": "2025-01-25T10:00:00Z",
      "phase": "COMPLETED",
      "change_type": "major",
      "description": "Project completed, all tests passing"
    }
  ]
}
```

**Automation:**
- Use `shared/scripts/bump-version.py` to automatically bump versions
- Script validates phase transitions and suggests appropriate version bump
- Updates both `version` field and appends to `version_history`

**Metadata Fields:**
- `test_track`: "A" (basic smoke tests) or "B" (comprehensive testing)
- `prototype_type`: "standard" (full SDLC) or "spike" (throwaway exploration)
- `target_output`: Expected output format (CLI tool, Web app, Library, API, Dashboard, Mobile app, Browser extension, Shared types, Shared domain model, Shared UI components, Reusable utility library, Single-page product takeaway, Single-page comparison)
- `target_audience`: Primary users (SREs, Developers, Sales, etc.)
- `target_company_maturity`: Company maturity levels this prototype targets (array, multi-select)
  - Available levels: `["poc", "mvp", "pmf", "startup", "scaleup", "enterprise"]`
  - `poc`: Proof of Concept stage (validating idea feasibility)
  - `mvp`: Minimum Viable Product stage (first customer-ready version)
  - `pmf`: Product-Market Fit stage (validated, scaling adoption)
  - `startup`: Early-stage startup (typically seed to Series A)
  - `scaleup`: Growth-stage company (typically Series B-D)
  - `enterprise`: Large established organization (1000+ employees)
  - Examples: `["poc", "mvp"]`, `["startup", "scaleup"]`, `["enterprise"]`
- `output_validation`: Phase 5 validation results (validated_at, selected_option, user_action)
- `uml_diagrams_used`: true/false (Phase 6 optional UML class + sequence diagrams)
- `uml_approval`: Phase 6 UML approval metadata (if uml_diagrams_used: true)
  - `approved_at`: ISO timestamp
  - `diagrams_generated`: ["class", "sequence-auth", "sequence-checkout", etc.]
- `requirements_phase_completed`: true/false (Phase 5.5 completion status)
- `requirements_completed_at`: ISO timestamp (Phase 5.5 completion time)

**Phase Names:** SEED, RESEARCH, IDEA_EXPANSION, IDEA_ANALYSIS, IDEA_CANDIDATE_SELECTION, REQUIREMENTS_AND_PRD, TECHNICAL_DESIGN, TEST_DESIGN, IMPLEMENTATION, QUALITY_VALIDATION, REFINEMENT, DIVERGENT_IMPLEMENTATION, DIVERGENT_EVALUATION, CONVERGENCE, COMPLETED, ARCHIVED, GRADUATED

**Status Values:** ACTIVE, ON_HOLD, BLOCKED, COMPLETED, ARCHIVED, GRADUATED

**Rules:**
- Create `.project` on prototype start
- Update on phase transitions
- Set `deliverables_completed: true` before transition
- Move from ideas/ to prototypes/ at Phase 6→7
- Phase 7: Create tests directory, install Playwright, write tests
- Phase 8: Write implementation code to pass tests, create startup script
- Phase 8.5: Quality validation (web/UI projects only), generate validation report
- Phase 9: UAT automation and polish

