# SDLC Phase Reports Publishing SOP

## Overview

**Rule:** ALL SDLC phases (1-9) MUST publish HTML report sites with findings, progress navigation, and current stage indicators.

**Purpose:**
- Dual-output: Version-controlled markdown + shareable HTML
- Visual progress tracking across SDLC
- Mobile-friendly review on any device
- Persistent URLs for stakeholder sharing

---

## Universal Requirements (All Phases)

### 1. Dual Output Format

**Local markdown:**
- Location: `project-management/ideas/[classification]/{name}-{5char}/[phase].md`
- Version controlled, diffable, grep-friendly
- Examples: `seed.md`, `research.md`, `expansion.md`, `design.md`

**HTML site:**
- Location: `project-management/ideas/[classification]/{name}-{5char}/[phase]-site/`
- Built with Vite, Tailwind CSS
- Interactive, responsive, mobile-friendly

**S3 published:**
- URL pattern: `https://bucket.s3.region.amazonaws.com/[project-id]/[phase]/index.html`
- Environment-aware credentials (personal/work/claude-code)

### 2. Navigation & Progress Indicator (Required)

**Location:** Side navigation (desktop) OR collapsible header (mobile)

**Progress Stages Display:**
```
┌─────────────────────────────────┐
│ Todo Manager Project            │
│                                 │
│ ✅ 1. SEED                      │
│ ✅ 2. RESEARCH      ← Current   │
│ ⏸️ 3. EXPANSION                 │
│ ⏸️ 4. ANALYSIS                  │
│ ⏸️ 5. SELECTION                 │
│ ⏸️ 6. DESIGN                    │
│ ⏸️ 7. TEST DESIGN               │
│ ⏸️ 8. IMPLEMENTATION            │
│ ⏸️ 9. REFINEMENT                │
│                                 │
│ [View All Phases ↗]            │
└─────────────────────────────────┘
```

**Status Icons:**
- ✅ Completed (green)
- 🔄 In Progress (blue, animated)
- ⏸️ Not Started (gray)
- ⚠️ Blocked (yellow)
- ❌ Failed (red)

**Visual Indicator Features:**
- Current phase highlighted with background color
- Completed phases show checkmarks, clickable to view reports
- Click any completed phase to navigate to that report
- Progress bar showing overall completion (N/9 phases)
- Estimated timeline remaining

**Responsive Design:**
- Desktop: Fixed left sidebar (250px width)
- Tablet: Collapsible sidebar
- Mobile: Top header bar with hamburger menu

### 3. Common Template Elements

**Header:**
```html
<header>
  <h1>{name}-{5char}</h1>
  <div class="meta">
    <span class="phase">Phase N: [PHASE_NAME]</span>
    <span class="date">[DATE]</span>
    <span class="status">[Status]</span>
  </div>
  <div class="progress">
    <div class="progress-bar" style="width: 22%">2/9 Phases</div>
  </div>
</header>
```

**Footer:**
```html
<footer>
  <div class="actions">
    <a href="../seed-site/" class="btn">← Previous: SEED</a>
    <a href="../expansion-site/" class="btn">Next: EXPANSION →</a>
  </div>
  <div class="meta">
    <span>Generated: [TIMESTAMP]</span>
    <span>Protoflow SDLC v3.0</span>
  </div>
</footer>
```

---

## Phase-Specific Reports

### Phase 1: SEED (seed.md → seed-site)

**Deliverable:** Concept validation with visual diagrams

**Report Sections:**
- Concept (hero section)
- Problem/Opportunity (grid)
- Assumptions/Constraints
- Success Criteria
- Target metadata (output, audience, maturity)
- Domain Model
- UML Diagrams (class, sequence, component)

**Interactive Features:**
- Expandable UML diagrams
- Zoom/pan on diagrams
- Source classification badges (User/Tech/Guardrails/Inferred)
- Print-friendly view

**Template:** `shared/templates/seed-review-vite/` (exists)

**Script:** `shared/scripts/generate_seed_review.py` (exists)

---

### Phase 2: RESEARCH (research.md → research-site)

**Deliverable:** Existing solutions analysis

**Report Sections:**
- Executive Summary
- Interactive Comparison Table (sortable, filterable)
- Detailed Analysis per tool
- Sync strategies analysis
- Gaps & Opportunities
- Build vs. Buy vs. Adapt matrix
- Recommendation with rationale

**Interactive Features:**
- Sortable comparison table (stars, license, tech stack)
- Filter by: type (CLI/Web/AI), license, activity
- Expandable tool detail cards
- Feature matrix heatmap
- GitHub stats live widgets (optional)

**Template:** `shared/templates/research-review-vite/` (to be created)

**Script:** `shared/scripts/generate_research_review.py` (to be created)

---

### Phase 3: EXPANSION (expansion.md → expansion-site)

**Deliverable:** Expanded tech stack options

**Report Sections:**
- Tech Stack Options (3-5 approaches)
- Comparison matrix per category:
  - CLI frameworks (Cobra, oclif, Commander, etc.)
  - Web frameworks (React, Vue, Svelte)
  - AI integration (Ollama, OpenAI, Anthropic)
  - Sync strategies (WebSocket, CRDT, polling)
  - Storage (SQLite, PostgreSQL, IndexedDB)
- Trade-off analysis
- Prototype recommendations

**Interactive Features:**
- Expandable tech option cards
- Feature comparison sliders
- Effort estimation calculator
- Cost comparison charts (if applicable)

**Template:** `shared/templates/expansion-review-vite/` (to be created)

---

### Phase 4: ANALYSIS (analysis.md → analysis-site)

**Deliverable:** Deep-dive analysis of selected options

**Report Sections:**
- Selected options from Phase 3
- Detailed technical analysis:
  - Performance benchmarks
  - Learning curve assessment
  - Community/ecosystem health
  - Integration complexity
  - Maintenance burden
- Risk analysis
- Recommendation refinement

**Interactive Features:**
- Benchmark comparison charts
- Risk/reward matrix visualization
- Interactive decision tree
- Prototype code samples with syntax highlighting

---

### Phase 5: SELECTION (selection.md → selection-site)

**Deliverable:** Final tech stack selection

**Report Sections:**
- Selected tech stack (final decisions)
- Justification per selection
- Rejected alternatives with rationale
- Integration plan
- Dependency map
- Risk mitigation plan

**Interactive Features:**
- Tech stack architecture diagram (interactive)
- Dependency graph visualization
- Integration timeline Gantt chart
- Risk heat map

---

### Phase 6: DESIGN (design.md → design-site)

**Deliverable:** System architecture and API design

**Report Sections:**
- System architecture diagrams
- API specifications (OpenAPI/Swagger)
- Database schema (ERD)
- Component hierarchy
- Data flow diagrams
- Security design
- Deployment architecture

**Interactive Features:**
- Interactive architecture diagrams (zoom, pan, click nodes)
- API explorer (try endpoints)
- Schema viewer (expandable tables)
- Mermaid diagrams for flows
- Mobile/desktop layout previews

---

### Phase 7: TEST DESIGN (test-design.md → test-design-site)

**Deliverable:** Test strategy and test cases

**Report Sections:**
- Test strategy (unit, integration, e2e)
- Test cases by feature
- Coverage targets
- Test data requirements
- CI/CD pipeline design
- Performance test plan

**Interactive Features:**
- Test case browser (filterable by feature/priority)
- Coverage visualization
- Test execution timeline
- Sample test code with syntax highlighting

---

### Phase 8: IMPLEMENTATION (implementation.md → implementation-site)

**Deliverable:** Implementation progress and code review

**Report Sections:**
- Implementation progress (% complete)
- Completed features
- Code metrics (LOC, complexity, coverage)
- Technical debt log
- Known issues
- Performance benchmarks
- Demo/screenshots

**Interactive Features:**
- Progress dashboard with charts
- Live code metrics
- Issue tracker integration
- Interactive demo embeds
- Screenshot gallery with annotations

---

### Phase 9: REFINEMENT (refinement.md → refinement-site)

**Deliverable:** Post-launch refinements and learnings

**Report Sections:**
- Launch summary
- Performance metrics vs. targets
- User feedback summary
- Bug fixes applied
- Enhancements added
- Lessons learned
- Future roadmap

**Interactive Features:**
- Metrics dashboard (real-time or snapshot)
- Before/after comparisons
- Feedback sentiment analysis
- Issue resolution timeline
- Roadmap Gantt chart

---

## Template Architecture

### Shared Components (All Phases)

**Base Template Structure:**
```
shared/templates/phase-review-base/
├── package.json           # Vite + Tailwind + common deps
├── vite.config.ts         # Shared Vite config
├── tailwind.config.js     # Shared Tailwind theme
├── src/
│   ├── components/
│   │   ├── PhaseNavigation.ts    # Progress sidebar
│   │   ├── Header.ts             # Common header
│   │   ├── Footer.ts             # Common footer
│   │   └── ProgressBar.ts        # Progress indicator
│   ├── utils/
│   │   ├── phaseLoader.ts        # Load .project metadata
│   │   └── navigation.ts         # Inter-phase navigation
│   └── styles/
│       ├── base.css              # Reset + typography
│       ├── components.css        # Shared component styles
│       └── themes.css            # Dark/light themes
```

**Phase-Specific Templates:**
- Inherit from base
- Add phase-specific components
- Override sections as needed

**Example: Research Template**
```
shared/templates/research-review-vite/
├── extends: ../phase-review-base/
├── src/
│   ├── components/
│   │   ├── ComparisonTable.ts   # Sortable table
│   │   ├── ToolCard.ts          # Expandable tool details
│   │   └── FeatureMatrix.ts     # Feature comparison
│   └── data/
│       └── research.json        # Generated from research.md
```

---

## Generation Scripts

### Unified Script: `shared/scripts/generate_phase_review.py`

**Usage:**
```bash
python3 shared/scripts/generate_phase_review.py \
  --phase [1-9] \
  --input project-management/ideas/.../[phase].md \
  --project-file project-management/ideas/.../.project
```

**Functionality:**
1. Detect phase from input file name or `--phase` flag
2. Load appropriate template (phase-specific or base)
3. Parse markdown file (extract sections, tables, diagrams)
4. Load `.project` metadata (for navigation)
5. Generate progress indicator (phases completed vs. remaining)
6. Replace placeholders in template
7. Run `npm install` and `npm run build`
8. Output to `[phase]-site/dist/`

**Options:**
- `--no-build` - Skip npm build (for development)
- `--template` - Custom template override
- `--env` - Environment for S3 publish (personal/work/claude-code)
- `--publish` - Auto-publish to S3 after build

---

## Publishing Workflow

### Automated Publishing (Recommended)

**Trigger:** Phase completion detected in `.project`

**Steps:**
1. User marks phase complete: `phase_history[N].completed = true`
2. Script detects phase completion
3. Prompts: "Generate and publish Phase N report? [y/n]"
4. If yes:
   - Generate HTML site
   - Publish to S3
   - Create bookmark
   - Update `.project` with URL
   - Git commit changes

**Script:** `shared/scripts/auto_publish_phase.py`

### Manual Publishing

**Command:**
```bash
python3 shared/scripts/generate_phase_review.py \
  --phase 2 \
  --input project-management/ideas/personal/todo-manager-fed2/research.md \
  --project-file project-management/ideas/personal/todo-manager-fed2/.project \
  --publish \
  --env personal
```

**S3 Path Pattern:**
```
s3://bucket/[project-id]/phase-[N]/index.html
```

**Examples:**
- SEED: `s3://bucket/todo-manager-fed2/phase-1/index.html`
- RESEARCH: `s3://bucket/todo-manager-fed2/phase-2/index.html`
- DESIGN: `s3://bucket/todo-manager-fed2/phase-6/index.html`

---

## Bookmark Organization

**Structure:**
```
bookmarks/
├── index.html              # Master index
├── projects/
│   ├── todo-manager-fed2/
│   │   ├── phase-1-seed.url
│   │   ├── phase-2-research.url
│   │   ├── phase-3-expansion.url
│   │   └── index.html      # Project-specific index
│   └── other-project-abc12/
│       └── ...
```

**Project Index Template:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>todo-manager-fed2 - All Phases</title>
</head>
<body>
  <h1>Todo Manager - Phase Reports</h1>
  <ul>
    <li><a href="[S3_URL]/phase-1/">✅ Phase 1: SEED</a></li>
    <li><a href="[S3_URL]/phase-2/">✅ Phase 2: RESEARCH</a></li>
    <li><a href="[S3_URL]/phase-3/">🔄 Phase 3: EXPANSION</a> (In Progress)</li>
    <li>⏸️ Phase 4: ANALYSIS</li>
    <li>⏸️ Phase 5: SELECTION</li>
    <li>⏸️ Phase 6: DESIGN</li>
    <li>⏸️ Phase 7: TEST DESIGN</li>
    <li>⏸️ Phase 8: IMPLEMENTATION</li>
    <li>⏸️ Phase 9: REFINEMENT</li>
  </ul>
</body>
</html>
```

---

## .project Schema Updates

**Add phase URLs:**

```json
{
  "phase_urls": {
    "1": {
      "phase": "SEED",
      "url": "https://bucket.s3.region.amazonaws.com/proto-id/phase-1/index.html",
      "published": "2025-11-24T10:00:00Z",
      "version": 2
    },
    "2": {
      "phase": "RESEARCH",
      "url": "https://bucket.s3.region.amazonaws.com/proto-id/phase-2/index.html",
      "published": "2025-11-24T14:00:00Z",
      "version": 1,
      "tools_analyzed": 11,
      "recommendation": "BUILD"
    }
  }
}
```

---

## Benefits

### For Each Phase
- ✅ Visual progress tracking (see where you are in SDLC)
- ✅ Persistent URLs (share with stakeholders)
- ✅ Mobile-friendly (review on phone/tablet)
- ✅ Interactive (sortable tables, expandable sections)
- ✅ Version controlled (markdown source)
- ✅ Professional presentation

### For Navigation
- ✅ See all phases at a glance
- ✅ Jump to any completed phase report
- ✅ Visual completion indicator (progress bar)
- ✅ Understand where you are in process
- ✅ Access previous phase findings quickly

### For Stakeholders
- ✅ Single URL per phase (no file downloads)
- ✅ Always see latest version
- ✅ Track project progress visually
- ✅ Review on any device

---

## Implementation Roadmap

### Phase 1 (MVP): Phases 1-2 Only
- [x] Phase 1 SEED template (exists)
- [x] Phase 1 generation script (exists)
- [ ] Phase 2 RESEARCH template
- [ ] Phase 2 generation script
- [ ] Progress navigation component
- [ ] Unified generation script

### Phase 2: Add Phases 3-5
- [ ] Phase 3 EXPANSION template
- [ ] Phase 4 ANALYSIS template
- [ ] Phase 5 SELECTION template
- [ ] Update navigation to support 5 phases

### Phase 3: Add Phases 6-9
- [ ] Phase 6 DESIGN template
- [ ] Phase 7 TEST DESIGN template
- [ ] Phase 8 IMPLEMENTATION template
- [ ] Phase 9 REFINEMENT template
- [ ] Complete navigation (all 9 phases)

### Phase 4: Automation
- [ ] Auto-detect phase completion
- [ ] Auto-generate reports
- [ ] Auto-publish to S3
- [ ] Auto-update bookmarks
- [ ] Git commit automation

---

## Related Documentation

- **S3 Publishing:** CLAUDE.md "S3 Publishing" section
- **Asset Bookmarks:** CLAUDE.md "Asset Bookmarks SOP"
- **Phase Processes:** `hmode/docs/processes/PHASE_*.md` files
- **.project Schema:** `hmode/docs/reference/PROJECT_METADATA.md`

---

## Status

**Version:** 2.0.0 (Expanded to all phases)
**Last Updated:** 2025-11-24
**Implementation:** Phase 1 (SEED) complete, others pending

**Current Templates:**
- ✅ Phase 1 SEED: `shared/templates/seed-review-vite/` + `shared/scripts/generate_seed_review.py`
- ⏸️ Phase 2-9: Pending creation

**Next Steps:**
1. Create base template with shared navigation component
2. Create Phase 2 research template
3. Test with todo manager research report
4. Iterate on navigation UX
5. Expand to phases 3-9
