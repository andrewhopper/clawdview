---
uuid: cmd-write-top-0h1i2j3k
version: 1.0.0
last_updated: 2025-11-10
description: Apply improvements automatically instead of just auditing
---

# Write to the Top Audit

Audit `{file_path}` for "write to the top" principles (Bottom Line Up Front, inverted pyramid, executive summaries). Optionally apply improvements with `--fix` flag.

## Write to the Top Principles

### ✅ Core Principles

**1. Executive Summary First:**
- ✅ Documents start with 2-3 sentence summary
- ✅ Summary includes: what, why, outcome
- ❌ No summary → reader must read entire doc to understand

**2. Bottom Line Up Front (BLUF):**
- ✅ Main conclusion/recommendation in first paragraph
- ✅ "We should X because Y" not buried in section 5
- ❌ Building suspense → state conclusion immediately

**3. Inverted Pyramid:**
- ✅ Most critical information first
- ✅ Supporting details progressively deeper
- ❌ Background before conclusion

**4. Section-Level BLUF:**
- ✅ Each major section starts with its conclusion
- ✅ "This section shows X" before diving into details
- ❌ Section purpose unclear until end

**5. Front-Loaded Headings:**
- ✅ "Recommendation: Use PostgreSQL" not "Database Selection"
- ✅ "Result: 40% Performance Gain" not "Performance Analysis"
- ❌ Generic headings that hide the conclusion

**6. Clear Hierarchy:**
- ✅ Logical flow: summary → key findings → details → appendix
- ✅ Critical path clearly marked
- ❌ Important info scattered throughout

### ❌ Anti-Patterns

**Burying the lede:**
```
❌ "After extensive analysis of multiple database options including
   PostgreSQL, MySQL, MongoDB, and DynamoDB, considering factors such
   as scalability, cost, and operational complexity, we determined
   that PostgreSQL is the best choice."

✅ "Recommendation: Use PostgreSQL. Analysis of 4 databases shows
   PostgreSQL offers best balance of performance, cost, and ops simplicity."
```

**Missing executive summary:**
```
❌ Document starts with "1.0 Background" → forces full read

✅ Document starts with summary:
   "This design proposes microservices architecture for the payment
   system, reducing latency by 60% and enabling independent scaling.
   Estimated cost: $50K, timeline: 3 months."
```

**Generic headings:**
```
❌ "## Database Analysis" (what was the conclusion?)

✅ "## Database Selection: PostgreSQL for ACID + Performance"
```

**Background before conclusion:**
```
❌ Flow: Background → History → Analysis → Problem → Solution → Recommendation

✅ Flow: Recommendation → Key Benefits → Implementation → Background (appendix)
```

## Instructions

### Step 1: Read & Parse

1. **Read document**: Use Read tool to load `{file_path}`
2. **Analyze structure**:
   - Does executive summary exist? (first 200 words)
   - Does intro paragraph state main conclusion?
   - Are sections front-loaded with conclusions?
   - Are headings informative vs generic?
   - Is critical info buried deep in doc?

### Step 2: Identify Issues

3. **Score each principle** (0-10):

| Principle | Score | Evidence | Fix |
|-----------|-------|----------|-----|
| Executive summary | 0-10 | Present? Length? Quality? | Add/improve summary |
| BLUF intro | 0-10 | Conclusion in para 1? | Restructure intro |
| Inverted pyramid | 0-10 | Critical info first? | Reorder sections |
| Section BLUF | 0-10 | Sections start with conclusion? | Add section summaries |
| Front-loaded headings | 0-10 | Headings informative? | Rewrite headings |
| Clear hierarchy | 0-10 | Logical flow? | Restructure |

4. **Generate defect list**:

```markdown
# Write to Top Audit: {file_path}

**Overall Score:** {average}/10
**Readability:** {High/Medium/Low}

## Issues Found

### 🔴 CRITICAL: Missing Executive Summary
**Location:** Document start
**Issue:** No executive summary. Reader must read entire doc to understand purpose.
**Fix:** Add 2-3 sentence summary covering: what, why, outcome, timeline/cost

**Example:**
```
# Executive Summary

This design proposes migrating from monolith to microservices architecture.
Benefits: 60% latency reduction, independent scaling, faster deployments.
Cost: $50K, Timeline: 3 months, Risk: Medium (requires team training).
```

---

### ⚠️ WARNING: BLUF Missing in Introduction
**Location:** Lines 1-15
**Current:** Document starts with background history
**Issue:** Main recommendation appears in section 5 (line 243)
**Fix:** Move recommendation to paragraph 1, then provide context

**Current structure:**
```
1. Background
2. Problem statement
3. Analysis
4. Options
5. Recommendation ← BURIED HERE
```

**Proposed structure:**
```
1. Recommendation + key reasons (BLUF)
2. Quick context (2 sentences)
3. Supporting analysis
4. Implementation details
```

---

### 💡 SUGGESTION: Generic Headings
**Location:** Lines 45, 89, 134
**Current headings:**
- "## Database Analysis"
- "## Performance Testing"
- "## Cost Considerations"

**Issue:** Headings don't reveal conclusions
**Proposed headings:**
- "## Database Selection: PostgreSQL for ACID + Scale"
- "## Performance: 60% Latency Reduction Achieved"
- "## Cost Analysis: $50K Implementation, $2K/mo Ops"

---

### 💡 SUGGESTION: Section BLUF Missing
**Location:** Section 3 (lines 67-98)
**Issue:** Section dives into details without stating purpose/conclusion first
**Fix:** Add opening sentence stating section's conclusion

**Current:**
```
## Database Options

PostgreSQL offers ACID compliance...
[30 lines of details]
...therefore PostgreSQL is recommended.
```

**Proposed:**
```
## Database Options

PostgreSQL is recommended for ACID compliance and horizontal scaling.
This section compares 4 options:

PostgreSQL offers ACID compliance...
[details]
```

## Summary

**Issues by severity:**
- 🔴 Critical: {count}
- ⚠️ Warnings: {count}
- 💡 Suggestions: {count}

**Key improvements:**
1. Add executive summary (2-3 sentences)
2. Move recommendation to paragraph 1
3. Front-load section conclusions
4. Make headings informative (include conclusions)
```

### Step 3: Apply Fixes (if `--fix` flag present)

5. **Check for `--fix` flag** in command invocation

6. **If `--fix` NOT present**:
   - Display audit report (Step 2 output)
   - Show example improvements
   - **STOP** - do not modify file

7. **If `--fix` IS present**:
   - Apply all improvements automatically
   - Use Edit tool to restructure content
   - Track changes made

8. **Restructuring logic**:

   a. **Add executive summary** (if missing):
      - Extract: main topic, key recommendation, benefits, cost/timeline
      - Generate 2-3 sentence summary
      - Insert at document top (after title)

   b. **Restructure introduction** (if missing BLUF):
      - Identify main recommendation (scan full doc)
      - Move recommendation + key reasons to paragraph 1
      - Condense background to 2-3 sentences after BLUF
      - Move detailed background to appendix or later section

   c. **Improve headings**:
      - Scan each section for conclusion
      - Rewrite heading to include conclusion
      - Pattern: `## {Topic}: {Conclusion/Key Finding}`

   d. **Add section BLUF**:
      - For each major section lacking opening summary
      - Add 1 sentence stating section's conclusion/purpose
      - Insert before existing content

   e. **Reorder sections** (if needed):
      - Executive summary
      - Introduction (with BLUF)
      - Key findings/recommendations
      - Supporting analysis
      - Implementation details
      - Background/context (move to appendix if lengthy)

### Step 4: Report Results

9. **Show before/after metrics**:

```markdown
# Write to Top Improvements Applied

**File:** {file_path}

## Changes Made

✅ Added executive summary (3 sentences, 287 chars)
✅ Restructured introduction with BLUF (moved recommendation from line 243 → line 8)
✅ Improved 5 headings to front-load conclusions
✅ Added section BLUF to 3 sections
✅ Reordered sections (moved background to appendix)

## Score Improvement

| Principle | Before | After | Δ |
|-----------|--------|-------|---|
| Executive summary | 0/10 | 9/10 | +9 |
| BLUF intro | 2/10 | 8/10 | +6 |
| Inverted pyramid | 4/10 | 8/10 | +4 |
| Section BLUF | 3/10 | 7/10 | +4 |
| Front-loaded headings | 5/10 | 9/10 | +4 |
| Clear hierarchy | 6/10 | 8/10 | +2 |

**Overall:** 3.3/10 → 8.2/10 (+4.9)

## Example Improvements

**Before (buried lede):**
```
## Introduction

The payment processing system has been experiencing latency issues
over the past 6 months. After analyzing multiple architectural
approaches and consulting with 3 vendors, we conducted a 2-week
proof of concept...

[200 more lines]

...therefore we recommend migrating to microservices.
```

**After (BLUF):**
```
## Introduction

**Recommendation:** Migrate to microservices architecture to reduce
payment latency by 60% (400ms → 160ms). Cost: $50K, timeline: 3mo.

The payment system has experienced latency issues (400ms p95). Analysis
of 4 architectural options shows microservices provides best balance of
performance, cost, and operational simplicity. See Section 3 for detailed
comparison.
```

---

**Heading improvements:**
- ❌ "## Performance Analysis" → ✅ "## Performance: 60% Latency Reduction (400ms → 160ms)"
- ❌ "## Cost Review" → ✅ "## Cost Analysis: $50K Implementation + $2K/mo Operations"
- ❌ "## Timeline" → ✅ "## Timeline: 3-Month Rollout (Q2 2024)"
```

## Audit-Only Mode (No `--fix` flag)

10. **If no `--fix` flag**, output audit report with:
    - Overall score (0-10)
    - Breakdown by principle
    - Specific issues with line numbers
    - Example improvements (show what could be changed)
    - Actionable recommendations

```markdown
# Write to Top Audit: {file_path}

**Overall Score:** 4.2/10
**Assessment:** Needs significant restructuring

## Recommendations

1. 🔴 **Add executive summary** (missing)
   - Place 2-3 sentence summary after title
   - Include: what, why, outcome, cost/timeline

2. ⚠️ **Restructure introduction with BLUF** (recommendation buried at line 243)
   - Move main recommendation to paragraph 1
   - Condense background to 2-3 sentences
   - Move detailed background to appendix

3. 💡 **Improve 5 headings** to include conclusions
   - Example: "## Database Analysis" → "## Database Selection: PostgreSQL"

4. 💡 **Add section BLUF** to 3 sections (start each with conclusion)

Run `/write-to-top {file_path} --fix` to apply improvements automatically.
```

## Examples

### Example 1: Audit Only

```bash
/write-to-top ./docs/design.md
```

**Output:** Audit report with scores, issues, recommendations (no changes made)

---

### Example 2: Audit + Fix

```bash
/write-to-top ./docs/design.md --fix
```

**Output:**
1. Apply all improvements
2. Show before/after scores
3. List changes made
4. Display example improvements

---

### Example 3: Well-Written Document

```bash
/write-to-top ./docs/architecture.md
```

**Output:**
```markdown
# Write to Top Audit: architecture.md

**Overall Score:** 9.1/10
**Assessment:** Excellent - follows write to top principles

✅ Executive summary present (3 sentences, clear what/why/outcome)
✅ BLUF in introduction (recommendation in paragraph 1)
✅ Inverted pyramid structure
✅ All sections start with conclusions
✅ Headings front-load key information
✅ Clear hierarchy

**Minor suggestions:**
- Section 4 heading could be more specific: "Implementation Plan" → "Implementation: 3-Phase Rollout (Q2-Q4)"

No fixes needed. Document is well-structured.
```

## Scoring Rubric

**Executive Summary (0-10):**
- 0: No summary
- 3: Summary exists but vague/incomplete
- 6: Summary clear but missing key elements (cost/timeline/outcome)
- 9: Excellent summary (what, why, outcome, cost/timeline in 2-3 sentences)
- 10: Perfect summary + visual aid (table/diagram)

**BLUF Introduction (0-10):**
- 0: Recommendation buried deep in document
- 3: Recommendation in introduction but after lengthy background
- 6: Recommendation in paragraph 1 but unclear
- 9: Clear recommendation in paragraph 1 with key reasons
- 10: Perfect BLUF + 2-sentence context + forward references

**Inverted Pyramid (0-10):**
- 0: Background/history first, conclusion last
- 3: Some important info early but mixed with background
- 6: Mostly good flow but some critical info buried
- 9: Clear progression from critical → supporting → details
- 10: Perfect inverted pyramid + clear navigation aids

**Section BLUF (0-10):**
- 0: No sections start with conclusions
- 3: Few sections start with conclusions
- 6: Half of sections start with conclusions
- 9: All sections start with conclusions
- 10: All sections start with conclusions + forward references

**Front-Loaded Headings (0-10):**
- 0: All generic headings ("Analysis", "Overview", etc.)
- 3: Some headings informative
- 6: Half of headings include conclusions
- 9: All headings informative
- 10: All headings front-load conclusions + consistent pattern

**Clear Hierarchy (0-10):**
- 0: No clear structure, random order
- 3: Some structure but illogical flow
- 6: Decent structure with minor issues
- 9: Clear logical hierarchy
- 10: Perfect hierarchy + visual navigation (TOC, breadcrumbs)

## Key Principles

1. **Respect reader's time**: Most critical info first
2. **Enable skimming**: Headings + section intros reveal content
3. **Bottom line up front**: Never bury the lede
4. **Hierarchical detail**: Critical → supporting → background
5. **Every level summarizes**: Document, section, paragraph all front-load

## Edge Cases

**Technical documentation:**
- Executive summary still required
- BLUF = technical recommendation + key constraints
- Background can be more detailed but comes AFTER recommendation

**Narrative/storytelling:**
- BLUF still applies: state the outcome first
- Can include story elements AFTER establishing conclusion
- Example: "We achieved 60% latency reduction. Here's how..."

**Research papers:**
- Abstract = executive summary
- Introduction should state findings/hypothesis clearly
- Methodology comes AFTER establishing what was found

**Meeting notes:**
- Start with decisions made + action items
- Discussion details come after
- Background/context at end

## Integration with Other Commands

Can be combined with:
- `/densify` - First write to top, then densify
- `/amazon-style-checker` - Check both Amazon style AND write to top
- `/cite` - Add citations after restructuring

**Example workflow:**
```bash
/write-to-top ./docs/design.md --fix    # Restructure
/densify ./docs/design.md                # Compress
/cite ./docs/design.md                   # Add citations
```

## Output Format

### Audit Mode (no --fix)

```markdown
# Write to Top Audit: {filename}

**Overall Score:** {score}/10
**Assessment:** {Excellent/Good/Needs Work/Poor}

## Scores by Principle

| Principle | Score | Status | Issue |
|-----------|-------|--------|-------|
| Executive summary | 0/10 | 🔴 | Missing |
| BLUF intro | 2/10 | ⚠️ | Recommendation at line 243 |
| Inverted pyramid | 6/10 | 💡 | Background before conclusion |
| Section BLUF | 4/10 | ⚠️ | 3/6 sections missing intro |
| Front-loaded headings | 5/10 | 💡 | 5 generic headings |
| Clear hierarchy | 7/10 | ✅ | Good structure |

## Issues ({count} total)

[Detailed issues with examples and fixes]

## Recommendations

1. Priority actions
2. Quick wins
3. Nice-to-haves

Run `/write-to-top {file_path} --fix` to apply automatically.
```

### Fix Mode (with --fix)

```markdown
# Write to Top Improvements Applied: {filename}

## Changes Made

✅ {change 1}
✅ {change 2}
✅ {change 3}

## Score Improvement

| Principle | Before | After | Δ |
|-----------|--------|-------|---|
| ... | ... | ... | ... |

**Overall:** {before}/10 → {after}/10 (+{delta})

## Example Improvements

**Before:**
[snippet]

**After:**
[snippet]

---

File updated: {file_path}
```

## Success Criteria

**Audit provides:**
- Clear scores (0-10) for each principle
- Specific line numbers for issues
- Example improvements showing what to change
- Actionable recommendations prioritized by impact

**Fix mode produces:**
- Document restructured with BLUF at all levels
- Executive summary added (if missing)
- Headings front-load conclusions
- Sections start with summaries
- Clear hierarchy (critical → supporting → background)
- Original meaning preserved (no content loss)

Be precise, actionable, and improvement-focused.
