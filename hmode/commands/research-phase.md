---
uuid: cmd-research-7u8v9w0x
version: 1.0.0
last_updated: 2025-11-10
description: Phase 2 SDLC - Evaluate existing solutions before building
---

# Research Phase Command

You are helping the user complete **Phase 2: RESEARCH** of the 8-phase SDLC. This phase evaluates existing solutions before brainstorming custom approaches.

## Goal

Survey landscape, compare existing tools/libraries/approaches, identify gaps/opportunities, recommend build vs. buy vs. adapt.

## Research Process

### 1. Define Research Scope

Ask the user:
- **Problem to solve** (from Phase 1: SEED)
- **Solution types** (libraries, SaaS tools, frameworks, platforms)
- **Tech stack constraints** (language, runtime, existing dependencies)
- **Key requirements** (features, performance, licensing, cost)

### 2. Batch Web Research

Execute ALL searches in parallel (one message, multiple WebSearch calls):

**Search patterns:**
- "[problem] existing solutions tools 2025"
- "[problem] open source libraries [language] 2025"
- "[tool name] vs [tool name] comparison 2025"
- "[tool name] pricing licensing features 2025"
- "[tool name] reviews production use cases 2025"
- "[problem] best practices industry standards 2025"

**Sources to prioritize:**
- Official documentation
- GitHub repos (stars, activity, issues)
- Comparison articles (vs. competitors)
- Pricing pages
- Production case studies
- Licensing terms

### 3. Create Research Report

**Output:** `ideas/proto-XXX-name/research.md` (2 pages max)

**Required sections (decimal outline format):**

```
1.0 Research Scope
  1.1 Problem Definition
  1.2 Evaluation Criteria
  1.3 Constraints

2.0 Existing Solutions Survey
  2.1 Solution 1 Name
    2.1.1 Overview
    2.1.2 Key Features
    2.1.3 Maturity & Adoption
  2.2 Solution 2 Name
  [... 3-10 solutions total]

3.0 Comparison Matrix
  [TABLE: Solutions vs. Features/Pros/Cons/License/Maturity/Cost]

4.0 Gap Analysis
  4.1 Capabilities Covered by Existing Solutions
  4.2 Gaps & Missing Features
  4.3 Customization Needs

5.0 Build vs. Buy vs. Adapt
  5.1 Build from Scratch (rationale)
  5.2 Buy/Use Existing (which solution, why)
  5.3 Adapt/Extend Existing (which solution, what modifications)
  5.4 Recommendation

6.0 Key Takeaways
  [3-5 bullets]

7.0 References
  [Numbered citations]
```

### 4. Comparison Matrix Format

Use table with these columns:
- **Solution**: Name + link
- **Features**: Key capabilities (bullets)
- **Pros**: Strengths (bullets)
- **Cons**: Weaknesses (bullets)
- **License**: OSS (MIT/Apache/GPL) or Commercial
- **Maturity**: Active/Stable/Legacy, GitHub stars, last commit
- **Cost**: Free/Freemium/Paid, pricing tier

### 5. Build vs. Buy vs. Adapt Analysis

**Build from Scratch:**
- When: No solutions meet needs, learning opportunity, simple enough
- Risk: Time, maintenance burden, reinventing wheel
- Benefit: Full control, exact fit, no licensing issues

**Buy/Use Existing:**
- When: Mature solution exists, non-differentiating problem
- Risk: Vendor lock-in, cost, limited customization
- Benefit: Fast, proven, maintained by others

**Adapt/Extend Existing:**
- When: 70-80% fit, OSS extensible, active community
- Risk: Upgrade compatibility, contribution overhead
- Benefit: Leverage existing work, community support, faster than building

## Quality Standards

- **Brevity:** Bullets/tables, 50% fewer words
- **Current:** Search "2025" for latest info
- **Concrete:** Real tools, real metrics, real costs
- **Comparative:** Side-by-side, not isolated descriptions
- **Decisive:** Clear recommendation with rationale

## Deliverable Checklist

Before completing Phase 2, verify:
- ✅ 3-10 existing solutions documented
- ✅ Comparison matrix complete (features/pros/cons/license/maturity/cost)
- ✅ Gap analysis identifies missing capabilities
- ✅ Build vs. buy vs. adapt recommendation with clear rationale
- ✅ Document uses decimal outline format (1.0, 1.1, 1.1.1, etc.)
- ✅ All sources cited
- ✅ Output saved to `ideas/proto-XXX-name/research.md`

## Phase Transition

After research complete:
- Update `.project` file: `"current_phase": "RESEARCH"`, `"deliverables_completed": true`
- Ready for **Phase 3: IDEA EXPANSION** (brainstorm custom approaches informed by research)

## Example Usage

```
User: "Research existing SDLC workflow tools for Phase 2"
Assistant: [Searches for: "SDLC workflow tools 2025", "Linear vs Jira vs Asana comparison 2025", etc.]
Assistant: [Creates research.md with comparison matrix, gap analysis, recommendation]
```

---

Now, ask the user: **"What problem should I research existing solutions for? (Provide Phase 1 SEED document or problem description)"**
