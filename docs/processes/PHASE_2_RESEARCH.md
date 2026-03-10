### Phase 2: RESEARCH 🔬 (NO CODE)
**Goal:** Evaluate existing solutions AND identify target audience
**Output:** `project-management/ideas/proto-name-xxxxx-NNN-research.md` (2 pages max)
**Title:** `# Stage 2 - Research`
- Existing solutions survey (3-10 tools/libraries/approaches)
- **GitHub SaaS clones** (search for open-source alternatives to commercial products)
- Comparison table (features, pros/cons, licensing, maturity)
- Gaps/opportunities identified
- Build vs. buy vs. adapt recommendation
- **🎯 TARGET AUDIENCE (REQUIRED)** - Inferred personas with validation
**Exit:** Landscape understood, existing solutions documented, **target audience validated**

---

## 🎯 TARGET AUDIENCE INFERENCE (REQUIRED)

**Philosophy:** Everything we build is for a human with an intent. Identify WHO before proceeding.

**🚨 CRITICAL:** Do NOT mark demographics as "TBD" or "All audiences". See Rule 30.

### Process:

1. **Gather signals** from project context:
   - Price range / pricing model
   - Industry / vertical
   - Location / geography
   - Brands / competitors mentioned
   - Product / service type

2. **Infer primary persona** using signal matrix:

   | Signal | Likely Audience |
   |--------|-----------------|
   | $75k-$200k boats, premium brands | Affluent 45-65, second home owners |
   | $500/mo B2B SaaS | CFO/VP Finance 40-55, committee buying |
   | $20/mo fitness app | Time-poor professionals 28-45 |
   | Free consumer app, ads | Mass market 18-35, mobile-first |
   | $5k+ enterprise | Decision committee, ROI-focused 35-55 |

3. **Present hypothesis to user:**
   ```
   Based on [evidence], your primary market is likely:
   - Age: X-Y
   - Income: $XXk+ HHI
   - Lifestyle: [description]
   - Values: [what they care about]

   Sound right? [Y/n/adjust]
   ```

4. **Wait for confirmation** - Do NOT proceed to Phase 3 without validation

5. **Document validated personas** in research output:
   ```markdown
   ## Target Audience (AI-Inferred, Human-Validated)

   ### Primary Persona: "[Name]" (X% of market)
   - Age: X-Y
   - Income: $XXk+ HHI
   - Lifecycle: [stage]
   - Values: [priorities]
   - Pain Points: [problems they have]
   - Decision Style: [how they buy]
   - Validated: [date]

   ### Secondary Persona: "[Name]" (Y% of market)
   [...]
   ```

### Slash Command: `/infer-audience`

Use this command for detailed persona inference workflow with full signal analysis.

---

**Research Strategy:**
1. **Search component libraries** (UI frameworks, chart libs, data grids, etc.)
2. **Search GitHub for SaaS clones** (e.g., "Trello clone", "Notion clone", "Figma clone", "Jira clone")
   - Filter by: stars (>10), recent activity (<6 months), license (MIT/Apache preferred)
   - Evaluate: tech stack match, feature overlap, adaptation effort, code quality
   - Example queries: "[Product] clone GitHub React", "open source [Product] alternative"
3. **Evaluate commercial alternatives** (if applicable, for comparison)
4. **Document build vs. buy vs. adapt** with effort estimates and decision matrix
5. **🎯 Infer and validate target audience** before exiting phase

