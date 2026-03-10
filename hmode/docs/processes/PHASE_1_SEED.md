### Phase 1: SEED 🌱 (NO CODE)

**Goal:** Capture initial idea with visual review system

**Output:**
- `project-management/ideas/proto-name-xxxxx-NNN-seed.md` (1 page max)
- `README.md` (project summary)
- `.project` (metadata file)
- Mobile-optimized HTML review site (deployed to S3)

**Title:** `# Stage 1 - Concept Seed`

---

## 0.0 BUSINESS MATURITY STAGE GATE (MANDATORY - FIRST STEP)

**BEFORE capturing any idea, AI MUST ask about business maturity stage.**

### Business Stage Question

```markdown
## Business Maturity Stage

What is the business maturity stage for this project?

[1] POC (Proof of Concept) - Validating technical feasibility
[2] MVP (Minimum Viable Product) - First customer-ready version
[3] PMF (Product-Market Fit) - Validated, starting to scale
[4] Startup (Early-stage) - Seed to Series A, iterating fast
[5] Scaleup (Growth-stage) - Series B-D, proven model scaling
[6] Enterprise (Mature) - Large org (1000+ employees), formal processes
```

**WAIT for human response before proceeding.**

### Business Stage Impact

| Stage | Process Rigor | Documentation | Error Tracking | Phase 2.5 |
|-------|---------------|---------------|----------------|-----------|
| POC | Minimal | seed.md only | Optional | Skip |
| MVP | Light | Core docs | Required | Optional |
| PMF | Standard | Full docs | Required | Required |
| Startup | Standard | Full docs | Required | Required |
| Scaleup | Comprehensive | Full + PRD | Required + SLAs | Required |
| Enterprise | Formal | Full + PRD + RFC | Required + SLAs | Required |

### Store in `.project`

```yaml
business_stage: poc  # or mvp, pmf, startup, scaleup, enterprise
business_stage_selected_at: 2025-01-15T10:00:00Z
```

**NEVER skip this question - it determines process rigor throughout the project.**

---

## 1.0 SEED Document Structure

**Required Sections:**
- **Concept** (1-2 sentences): Core idea in plain language
- **Problem** (bullets): What pain points does this solve?
- **Opportunity** (bullets): Why now? What's the market opportunity?
- **Assumptions** (bullets): What are we assuming to be true?
- **Constraints** (bullets): Technical, resource, or timeline limitations
- **Success Criteria** (bullets): How do we know this succeeds?

**Required Metadata:**
- **Target Output:** [CLI tool | Web app | Library | API | Dashboard | Mobile app | Browser extension | Shared types | Shared domain model | Shared UI components | Reusable utility library | Single-page product takeaway | Single-page comparison]
- **Target Audience:** [SREs | Developers | Sales | Marketing | Executives | Data scientists | End users]
- **Target Company Maturity:** [poc | mvp | pmf | startup | scaleup | enterprise] (multi-select, default: ["poc"])
  - poc: Proof of Concept (validating feasibility)
  - mvp: Minimum Viable Product (first customer-ready)
  - pmf: Product-Market Fit (validated, scaling)
  - startup: Early-stage (seed to Series A)
  - scaleup: Growth-stage (Series B-D)
  - enterprise: Large org (1000+ employees)

---

## 2.0 Automatic HTML Review Generation

**After SEED creation, automatically:**

1. **Parse SEED content** - Extract concept, problem, opportunity, etc.
2. **Generate UML diagrams:**
   - Class diagram (domain model)
   - Sequence diagram (interaction flow)
   - Component diagram (system architecture)
3. **Build mobile-optimized Vite site:**
   - Responsive design (Tailwind CSS)
   - Interactive Mermaid diagrams
   - Version tracking with predecessor links
4. **Deploy to S3:**
   - Versioned path: `s3://bucket/{project-id}/v{N}/`
   - Pre-signed URL (7-day expiration)
5. **Present review URL:**
   - Clickable link for mobile/desktop review
   - All diagrams render in browser

**Command:**
```bash
python3 shared/scripts/generate_seed_review.py project-management/ideas/proto-example-123-seed.md
```

**Output:**
```
✅ SEED Review Site Generated Successfully!
📦 Project: Example Project
🔢 Version: 1
📅 Date: 2025-11-20
🔗 Review URL (expires in 7 days):

   https://s3.amazonaws.com/bucket/proto-example-123/v1/index.html?...
```

---

## 3.0 Review Loop with Versioning

**Interactive Review:**
1. AI presents review URL
2. AI asks: "Review complete? [approve/revise]"
3. **If approved:** Proceed to Phase 2 (Research)
4. **If revise:**
   - User provides feedback
   - AI updates seed.md
   - AI increments version (v2, v3, etc.)
   - AI regenerates site with link to previous version
   - Repeat until approved

**Version Retention:**
- All versions retained in S3: `{project-id}/v1/`, `{project-id}/v2/`, etc.
- Each version links to predecessor
- Version history visible in review site
- Original seed.md remains source of truth

**Example Revision:**
```bash
# After user requests changes
python3 shared/scripts/generate_seed_review.py \
  project-management/ideas/proto-example-123-seed.md \
  --version 2 \
  --prev-url "https://s3.amazonaws.com/.../v1/index.html?..."
```

---

## 4.0 Supporting Files

**README.md:**
- Summary with phase status, purpose, tech stack, timeline
- Link to latest review site version

**.project file:**
- Initial metadata with maturity levels
- Version tracking
- Review URL history

---

## 5.0 Exit Criteria

**Phase 1 Complete When:**
- ✅ Idea documented in seed.md (1 page max)
- ✅ Problem clearly articulated
- ✅ Target output/audience/maturity captured
- ✅ README.md created
- ✅ .project file created
- ✅ Persona defined (NOT "TBD" - must be inferred)
- ✅ **Human confirmed persona is correct** ← REQUIRED
- ✅ HTML review site generated and approved
- ✅ UML diagrams generated (class, sequence, component)
- ✅ User has reviewed and approved via review URL

**⚠️ CRITICAL: Cannot proceed to Phase 2 without persona confirmation from human**

**Next Phase:** Phase 2 (Research) - Evaluate existing solutions before building

---

## 6.0 Review Site Features

**Mobile-Optimized:**
- Responsive design (works on phone, tablet, desktop)
- Touch-friendly navigation
- Fast loading (Vite optimized)

**Interactive Diagrams:**
- Mermaid.js rendering
- Zoom/pan support
- Print-friendly

**Version Management:**
- Version number displayed
- Link to previous version (if exists)
- Date stamp
- Project metadata

**Content Source Classification:**
- Every section tagged with source badge
- 4 source types:
  - **User Provided** (blue): Directly from user input
  - **Tech Preferences** (pink): From `hmode/guardrails/tech-preferences/`
  - **Guardrails** (yellow): From `hmode/guardrails/architecture-preferences/`
  - **Inferred** (indigo): AI-generated or heuristic
- Visual legend explaining all source types
- Transparent tracking of content origin

**Content Sections:**
- Concept (hero section)
- Problem/Opportunity (grid layout)
- Assumptions/Constraints (grid layout)
- Success Criteria
- Target metadata (output, audience, maturity)
- Source classification legend
- All 3 UML diagrams (class, sequence, component)

---

## 7.0 File Locations

**Template:**
```
shared/templates/seed-review-vite/
├── package.json           # Vite + dependencies
├── tsconfig.json          # TypeScript config
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind CSS
├── postcss.config.js      # PostCSS config
├── index.html             # Template with placeholders
└── src/
    ├── main.ts            # Mermaid initialization
    └── style.css          # Tailwind + custom styles
```

**Script:**
```
shared/scripts/generate_seed_review.py
```

**S3 Structure:**
```
s3://protoflow-assets/
├── proto-example-123/
│   ├── v1/
│   │   ├── index.html
│   │   ├── assets/
│   │   └── ...
│   ├── v2/
│   │   ├── index.html
│   │   ├── assets/
│   │   └── ...
│   └── v3/
│       ├── index.html
│       ├── assets/
│       └── ...
```

---

## 8.0 Diagram Generation Strategy

**UML Class Diagram (Domain Model):**
- Extract entities from concept and problem
- Show relationships between components
- Include key attributes and methods
- Heuristic-based (can be enhanced with LLM)

**UML Sequence Diagram (Interaction Flow):**
- User → System → Component → Storage flow
- Based on success criteria and target output
- Shows request/response lifecycle

**Component Diagram (System Architecture):**
- User layer → Application layer → Data layer
- Optional external services
- Color-coded by layer type
- Shows dependencies

**Future Enhancement:**
- LLM-powered diagram generation from SEED content
- More sophisticated entity extraction
- Custom diagram templates per target output type

---

## 9.0 Troubleshooting

**Problem:** `npm install` fails in template

**Solution:**
- Ensure Node.js 18+ installed
- Check network connectivity
- Clear npm cache: `npm cache clean --force`

**Problem:** S3 upload fails

**Solution:**
- Check `ASSET_DIST_AWS_ACCESS_KEY_ID` env var
- Verify IAM permissions: `s3:PutObject`, `s3:GetObject`
- Ensure bucket exists: `protoflow-assets`

**Problem:** Diagrams don't render in browser

**Solution:**
- Check browser console for Mermaid errors
- Verify Mermaid syntax in generated diagrams
- Test with simpler diagram first

**Problem:** Pre-signed URL expired

**Solution:**
- Regenerate with longer expiration: modify script default (7 days)
- Or switch to public + obscured ID for long-term access

**Problem:** All content showing as "Inferred"

**Solution:**
- Ensure `hmode/guardrails/tech-preferences/` and `hmode/guardrails/architecture-preferences/` exist
- Check that guardrail files contain relevant keywords
- Verify seed content matches guardrail patterns (case-insensitive)
- User-provided content is default for substantive text without guardrail matches

**Problem:** Source badges not displaying correctly

**Solution:**
- Clear browser cache and reload
- Check that CSS styles are loading in dev tools
- Verify badge HTML is being generated in source

---

**Related Documentation:**
- `hmode/docs/reference/PUBLISHING_STRATEGIES.md` - S3 publishing patterns
- `hmode/docs/reference/ARCHITECTURE_DIAGRAMS.md` - Diagram standards
- `shared/scripts/s3_publish.py` - S3 utilities

