---
uuid: cmd-transform-4b5c6d7e
version: 1.0.0
last_updated: 2025-11-10
description: For outline mode, max depth level (default 3, max 5)
---

# Transform Document

Convert documents between formats: decimal outline structure or cliff notes summary.

## Modes

### Mode 1: Decimal Outline (--outline)

Transform prose/unstructured content → hierarchical decimal outline format.

**Pattern:** 1.0, 1.1, 1.1.1, 1.1.2, 1.2, 2.0, etc.

**Use when:**
- Document lacks clear structure
- Converting narrative to structured format
- Need hierarchical organization
- Preparing for technical documentation

**Example:**
```
Input:
The payment system handles transactions. It uses PostgreSQL for storage
and Redis for caching. The API layer handles requests while background
workers process async tasks.

Output:
1.0 Payment System Architecture
  1.1 Data Layer
    1.1.1 PostgreSQL - Transaction storage
    1.1.2 Redis - Caching layer
  1.2 Application Layer
    1.2.1 API Layer - Request handling
    1.2.2 Background Workers - Async processing
```

### Mode 2: Cliff Notes (--cliffnotes)

Distill document → essential points only (summary format).

**Style:** Brief, bullet-heavy, removes all non-essential content

**Use when:**
- Need quick reference version
- Creating study guide
- Extracting key takeaways
- Pre-meeting prep materials

**Example:**
```
Input:
[5 page design document]

Output:
# Cliff Notes: Payment System Design

**TL;DR:** Microservices architecture, 60% latency reduction, $50K cost, 3mo timeline

## Key Points
- Problem: Monolith causing 400ms p95 latency
- Solution: Microservices with API gateway
- Tech: Node.js, PostgreSQL, Redis, k8s
- Benefits: 400ms→160ms, independent scaling
- Cost: $50K implementation + $2K/mo ops
- Risk: Medium (requires team training)

## Critical Decisions
1. PostgreSQL over DynamoDB (ACID requirements)
2. Kubernetes over ECS (team familiarity)
3. 3-phase rollout (reduce risk)

## Next Steps
- Phase 1: API gateway (Month 1)
- Phase 2: Extract services (Month 2)
- Phase 3: Migration (Month 3)
```

## Instructions

### Step 1: Parse Arguments

1. **Check flags**:
   - Neither `--outline` nor `--cliffnotes`? → Default to `--outline`
   - Both flags present? → Error, choose one
   - `--depth` specified? → Validate (1-5), default to 3

### Step 2: Read Document

2. **Load content**: Use Read tool on `{file_path}`

3. **Analyze structure**:
   - Identify main sections/topics
   - Detect hierarchical relationships
   - Note key points, decisions, metrics
   - Extract critical information

### Step 3A: Decimal Outline Mode

**Execute if `--outline` flag present**

4. **Parse existing structure**:
   - Identify heading hierarchy (if markdown)
   - Detect implicit sections in prose
   - Map topics to hierarchical relationships

5. **Build decimal outline**:

   **Principles:**
   - Top level (1.0, 2.0, 3.0): Major sections
   - Second level (1.1, 1.2, 1.3): Subsections
   - Third level (1.1.1, 1.1.2): Details
   - Fourth level (1.1.1.1): Fine details (if --depth≥4)
   - Fifth level (1.1.1.1.1): Micro details (if --depth=5)

   **Formatting rules:**
   - Use 2 spaces per indentation level
   - Level 1 (1.0): No indentation
   - Level 2 (1.1): 2 spaces
   - Level 3 (1.1.1): 4 spaces
   - Level 4 (1.1.1.1): 6 spaces
   - Level 5 (1.1.1.1.1): 8 spaces

   **Content transformation:**
   - Extract key phrases from paragraphs
   - Preserve technical terms, metrics, decisions
   - Convert verbose explanations → concise labels
   - Maintain logical grouping

6. **Example transformations**:

**Input (prose):**
```
The architecture consists of three main components. First, we have
the API gateway which handles all incoming requests and performs
authentication. Second, the service layer contains the business logic
for payments, user management, and notifications. Third, the data
layer uses PostgreSQL for transactional data and Redis for caching.
```

**Output (decimal outline, depth=3):**
```
1.0 Architecture
  1.1 API Gateway
    1.1.1 Request handling
    1.1.2 Authentication
  1.2 Service Layer
    1.2.1 Payment service
    1.2.2 User management service
    1.2.3 Notification service
  1.3 Data Layer
    1.3.1 PostgreSQL - Transactional data
    1.3.2 Redis - Caching
```

**Output (decimal outline, depth=4):**
```
1.0 Architecture
  1.1 API Gateway
    1.1.1 Request Handling
      1.1.1.1 HTTP routing
      1.1.1.2 Load balancing
    1.1.2 Authentication
      1.1.2.1 JWT validation
      1.1.2.2 Session management
  1.2 Service Layer
    1.2.1 Payment Service
      1.2.1.1 Transaction processing
      1.2.1.2 Refund handling
    1.2.2 User Management Service
      1.2.2.1 User CRUD operations
      1.2.2.2 Profile management
    1.2.3 Notification Service
      1.2.3.1 Email notifications
      1.2.3.2 SMS notifications
  1.3 Data Layer
    1.3.1 PostgreSQL
      1.3.1.1 Transaction storage
      1.3.1.2 User data
    1.3.2 Redis
      1.3.2.1 Session cache
      1.3.2.2 Rate limiting
```

7. **Preserve critical info**:
   - Metrics and numbers
   - Technical decisions and rationale
   - Brand names and technologies
   - Constraints and requirements
   - Action items and timelines

8. **Output format**:

```markdown
# Decimal Outline: {original filename}

**Source:** {file_path}
**Depth:** {depth} levels
**Generated:** {timestamp}

---

1.0 {Section}
  1.1 {Subsection}
    1.1.1 {Detail}
    1.1.2 {Detail}
  1.2 {Subsection}
    1.2.1 {Detail}
2.0 {Section}
  2.1 {Subsection}
    2.1.1 {Detail}
      2.1.1.1 {Fine detail} (if depth≥4)
        2.1.1.1.1 {Micro detail} (if depth=5)

---

**Stats:**
- Original: {chars} chars, {lines} lines
- Outline: {items} items, {levels} levels
- Reduction: {%}%
```

### Step 3B: Cliff Notes Mode

**Execute if `--cliffnotes` flag present**

9. **Extract essential information**:

   a. **TL;DR** (1 sentence):
      - Main topic + key outcome/recommendation
      - Include most critical metric or decision

   b. **Key Points** (5-10 bullets):
      - Problem statement
      - Solution/recommendation
      - Technologies/approach
      - Benefits/outcomes
      - Costs (time/money)
      - Risks/concerns

   c. **Critical Decisions** (if applicable):
      - Choice A vs Choice B → Rationale
      - Keep only decisions that matter

   d. **Metrics/Numbers** (if applicable):
      - Performance improvements
      - Cost figures
      - Timeline estimates
      - Success criteria

   e. **Next Steps** (if applicable):
      - Action items
      - Timeline/phases
      - Milestones

10. **Compression principles**:

   - Remove all background/context (unless critical)
   - Remove verbose explanations
   - Keep only actionable/decision-relevant info
   - Target 10-20% of original length
   - Preserve all numbers, metrics, decisions

11. **Example transformations**:

**Input (3 page design doc):**
```
# Payment System Redesign

## Background
Our current payment system is a monolithic Rails application that was
built in 2018. Over the past two years, we've experienced increasing
latency issues...

[2000 words of detailed analysis]

## Recommendation
After evaluating multiple options, we recommend migrating to a
microservices architecture...

[1000 words of implementation details]
```

**Output (cliff notes):**
```
# Cliff Notes: Payment System Redesign

**TL;DR:** Migrate to microservices to reduce latency 60% (400ms→160ms), cost $50K, 3mo timeline

## Key Points
- **Problem:** Monolith causing 400ms p95 latency, blocking feature velocity
- **Solution:** Microservices architecture with API gateway
- **Tech Stack:** Node.js, PostgreSQL, Redis, Kubernetes
- **Benefits:** 400ms→160ms latency, independent scaling, faster deploys
- **Cost:** $50K implementation, $2K/mo operations
- **Timeline:** 3 months (Q2 2024)
- **Risk:** Medium - requires team upskilling on k8s

## Critical Decisions

**1. PostgreSQL over DynamoDB**
- Rationale: ACID requirements for payment transactions
- Trade-off: Horizontal scaling complexity vs data consistency

**2. Kubernetes over ECS**
- Rationale: Team familiarity, better local dev
- Trade-off: Higher ops complexity vs faster onboarding

**3. 3-phase rollout vs big bang**
- Rationale: Reduce risk, enable rollback
- Trade-off: Longer timeline vs lower risk

## Metrics

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| p95 latency | 400ms | 160ms | 60% |
| Deploy time | 45min | 10min | 78% |
| Service uptime | 99.5% | 99.9% | +0.4% |

## Timeline

- **Month 1:** API gateway + routing (March 2024)
- **Month 2:** Extract payment service (April 2024)
- **Month 3:** Full migration + cutover (May 2024)

## Next Steps
1. Get stakeholder approval (this week)
2. Hire k8s contractor (2 weeks)
3. Start Phase 1 implementation (March 1)
```

12. **Output format**:

```markdown
# Cliff Notes: {original title}

**Source:** {file_path}
**Generated:** {timestamp}

**TL;DR:** {one sentence summary}

## Key Points
- {essential point 1}
- {essential point 2}
- {essential point 3}
[...]

## Critical Decisions (if applicable)
**{Decision}**
- Rationale: {why}
- Trade-off: {what was sacrificed}

## Metrics (if applicable)
| Metric | Value |
|--------|-------|
[...]

## Timeline (if applicable)
- {phase 1}
- {phase 2}
[...]

## Next Steps (if applicable)
1. {action item}
2. {action item}
[...]

---

**Stats:**
- Original: {chars} chars
- Cliff Notes: {chars} chars
- Reduction: {%}%
- Reading time: {X} min → {Y} min
```

### Step 4: Write Output

13. **Create transformed file**:

   a. **For outline mode:**
      - Filename: `{original-name}-outline.md`
      - Example: `design.md` → `design-outline.md`

   b. **For cliff notes mode:**
      - Filename: `{original-name}-cliffnotes.md`
      - Example: `design.md` → `design-cliffnotes.md`

14. **Use Write tool** to create new file (don't modify original)

15. **Report results**:

```markdown
# Document Transformation Complete

**Source:** {file_path}
**Output:** {output_path}
**Mode:** {Decimal Outline / Cliff Notes}

## Transformation Stats

**Original:**
- Length: {chars} chars
- Lines: {lines}
- Reading time: ~{X} min

**Transformed:**
- Length: {chars} chars
- Items/sections: {count}
- Reading time: ~{Y} min
- Reduction: {%}%

## Output Preview

[First 20 lines of transformed content]

---

✅ Transformation complete
📄 Output saved to: {output_path}
```

## Flag Combinations

| Command | Output | File Created |
|---------|--------|--------------|
| `/transform doc.md` | Decimal outline (default) | `doc-outline.md` |
| `/transform doc.md --outline` | Decimal outline | `doc-outline.md` |
| `/transform doc.md --outline --depth=4` | Decimal outline (4 levels) | `doc-outline.md` |
| `/transform doc.md --cliffnotes` | Cliff notes summary | `doc-cliffnotes.md` |
| `/transform doc.md --outline --cliffnotes` | ERROR: Choose one format | N/A |

## Use Cases

### Use Case 1: Structuring Unstructured Notes

**Input:** Meeting notes, brain dump, stream of consciousness
**Command:** `/transform ./notes/brainstorm.md --outline`
**Output:** Clean decimal outline with hierarchical structure

**Before:**
```
We need to build a search feature. It should handle full text search
across documents. Maybe use Elasticsearch? Also need autocomplete.
Ranking is important - most relevant first. Cost is a concern so
maybe start with PostgreSQL full text search...
```

**After:**
```
1.0 Search Feature
  1.1 Requirements
    1.1.1 Full text search across documents
    1.1.2 Autocomplete functionality
    1.1.3 Relevance ranking
  1.2 Technology Options
    1.2.1 Elasticsearch - Full featured
    1.2.2 PostgreSQL full text - Cost effective
  1.3 Constraints
    1.3.1 Cost optimization priority
```

### Use Case 2: Executive Summary

**Input:** 10-page technical design doc
**Command:** `/transform ./docs/design.md --cliffnotes`
**Output:** 1-page cliff notes for executives

**Use:** Share with stakeholders who need key decisions without implementation details

### Use Case 3: Study Guide

**Input:** Long documentation or specification
**Command:** `/transform ./docs/api-spec.md --cliffnotes`
**Output:** Quick reference guide

**Use:** Team onboarding, quick review before meetings

### Use Case 4: Documentation Restructure

**Input:** Legacy doc with poor structure
**Command:** `/transform ./docs/old-design.md --outline --depth=4`
**Output:** Well-structured decimal outline

**Use:** Foundation for rewriting the documentation

### Use Case 5: Multi-Format Documentation

**Commands:**
```bash
# Create all formats
/transform ./docs/architecture.md --outline          # Structured outline
/transform ./docs/architecture.md --cliffnotes       # Quick reference
/polish ./docs/architecture.md --fix                 # Polished original

# Result: 3 versions of same content
# - architecture.md (polished original)
# - architecture-outline.md (structured)
# - architecture-cliffnotes.md (summary)
```

## Depth Level Guidelines

**depth=1:** Top-level only
```
1.0 Section A
2.0 Section B
3.0 Section C
```

**depth=2:** Major sections + subsections
```
1.0 Section A
  1.1 Subsection
  1.2 Subsection
2.0 Section B
  2.1 Subsection
```

**depth=3:** Standard (default)
```
1.0 Section A
  1.1 Subsection
    1.1.1 Detail
    1.1.2 Detail
  1.2 Subsection
```

**depth=4:** Detailed
```
1.0 Section A
  1.1 Subsection
    1.1.1 Detail
      1.1.1.1 Fine detail
```

**depth=5:** Very detailed (use sparingly)
```
1.0 Section A
  1.1 Subsection
    1.1.1 Detail
      1.1.1.1 Fine detail
        1.1.1.1.1 Micro detail
```

**Recommendation:** Use depth=3 for most documents, depth=4 for complex technical specs

## Quality Metrics

### Decimal Outline Quality

**Good outline:**
- Clear hierarchy (parent-child relationships logical)
- Consistent depth (don't jump 1.0 → 1.1.1.1)
- Meaningful labels (not just "Other" or "Misc")
- Balanced tree (avoid 1.1 with 20 children)
- Complete coverage (all original content represented)

**Excellent outline:**
- All of the above
- Parallel structure (similar items at same level)
- Informative labels (include key info, not just topic)
- Optimal depth (3-4 levels, not too deep)
- Scannable (can understand structure at glance)

### Cliff Notes Quality

**Good cliff notes:**
- TL;DR captures essence
- Key points complete (all critical info)
- 80-90% reduction in length
- All metrics/numbers preserved
- Decisions and rationale clear

**Excellent cliff notes:**
- All of the above
- Standalone (can understand without original)
- Actionable (clear next steps)
- Scannable (bullets, tables, headers)
- 5-10 min read (from 30+ min original)

## Integration Examples

### Documentation Pipeline

```bash
# 1. Start with rough draft
vim ./docs/design.md

# 2. Structure it
/transform ./docs/design.md --outline
# Review outline, use as basis for restructure

# 3. Polish the original
/polish ./docs/design.md --fix

# 4. Create quick reference
/transform ./docs/design.md --cliffnotes

# Result:
# - design.md (polished, complete)
# - design-outline.md (structured reference)
# - design-cliffnotes.md (executive summary)
```

### Meeting Prep

```bash
# Before meeting: create cliff notes for quick review
/transform ./docs/proposal.md --cliffnotes

# Share cliffnotes.md with attendees
# Use as basis for discussion
```

### Knowledge Base

```bash
# For each major doc, create multiple formats
for doc in ./docs/*.md; do
  /transform "$doc" --outline
  /transform "$doc" --cliffnotes
done

# Organize:
# /docs/full/        - Complete documents
# /docs/outlines/    - Structured outlines
# /docs/summaries/   - Cliff notes
```

## Error Handling

**Invalid depth:**
```
Error: Invalid depth: {value}
Depth must be 1-5 (default: 3)

Usage: /transform {file_path} --outline --depth=3
```

**Both flags:**
```
Error: Cannot specify both --outline and --cliffnotes
Choose one transformation mode

Examples:
  /transform doc.md --outline
  /transform doc.md --cliffnotes
```

**File not found:**
```
Error: File not found: {file_path}
Check path and try again
```

**Empty file:**
```
Error: File is empty: {file_path}
Cannot transform empty document
```

## Advanced Features

### Smart Depth Detection

If user doesn't specify depth, auto-detect optimal depth:
- Simple doc (1-2 sections): depth=2
- Standard doc (3-5 sections): depth=3
- Complex doc (6+ sections, nested): depth=4

### Content Type Detection

Auto-adjust transformation based on content type:
- **Technical spec:** More detailed outline, preserve all technical terms
- **Meeting notes:** Extract decisions and action items in cliff notes
- **Design doc:** Emphasize architecture and trade-offs
- **Research:** Highlight findings and methodology

### Preservation Rules

**Always preserve:**
- Numbers, metrics, percentages
- Technical decisions and rationale
- Action items and deadlines
- Code examples and commands
- Brand names and product names
- Critical constraints

**Can remove:**
- Background context (unless critical)
- Verbose explanations
- Redundant examples
- Historical tangents
- Filler content

## Success Criteria

**Command succeeds when:**
- Output file created successfully
- Original file unchanged
- Transformation faithful to source
- Format correct (decimal outline or cliff notes)
- All critical information preserved
- Significant size reduction (outline: 30-50%, cliff notes: 80-90%)

**Output quality:**
- Decimal outline: Clear hierarchy, logical grouping, scannable
- Cliff notes: Captures essence, actionable, standalone
- Both: Preserve meaning, maintain technical accuracy

Be precise, faithful to source, and transformation-focused.
