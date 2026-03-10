---
uuid: cmd-impact-7a8b9c0d
version: 1.0.0
last_updated: 2025-11-10
description: Generate business impact assessment scorecard for a project
---

# Impact Assessment

Generate quantitative business impact assessment for projects based on effort, usage, audience, and financial impact.

## Instructions

**Usage:**
```bash
# Assess specific project
/impact-assessment proto-002-bedrock-joke-api
/impact-assessment prototypes/proto-007-flowey-sdlc

# Assess current directory (infer from pwd)
/impact-assessment

# Generate summary report for all projects
/impact-assessment --all
```

## Assessment Process

1. **Identify target project**:
   - If path provided → use that
   - If proto name provided → find in prototypes/ or ideas/
   - If no args → use current directory (must contain .project file)
   - If `--all` → assess all prototypes with .project files

2. **Read project files** (parallel):
   - `.project` → metadata, tech stack, status
   - `README.md` → purpose, description
   - `package.json` or requirements files → dependencies count
   - Source code → analyze file count, LOC estimate

3. **Calculate impact scores** (0-10 scale):

   **Level of Effort (LOE)** [0-10, inverse scoring]:
   - File count, LOC, dependencies
   - Complexity indicators (microservices, databases, APIs)
   - Tech stack complexity
   - **0 = months**, 5 = weeks, **10 = hours**

   **Frequency of Usage** [0-10]:
   - One-time tool = 0-2
   - Occasional (monthly) = 3-4
   - Regular (weekly) = 5-7
   - Daily/continuous = 8-10
   - Infer from: automation keywords, "daily", "continuous", "pipeline"

   **Audience Size** [0-10]:
   - Individual (1 person) = 1-2
   - Team (2-10) = 3-5
   - Department (10-50) = 6-7
   - Company (50-500) = 8-9
   - Public/External (500+) = 10
   - Infer from: "customer service", "public API", "internal tool"

   **Business Impact** [0-10]:
   - Cost savings (time, resources, manual labor)
   - Revenue generation potential
   - Risk reduction
   - Competitive advantage
   - Infer from: automation %, "customer service", "sales", keywords

   **Financial Impact** [0-10]:
   - Meme generator, toy projects = 0-2
   - Internal efficiency tools = 3-5
   - Customer-facing features = 6-7
   - Revenue-generating = 8-9
   - Business-critical automation (90% case reduction) = 10
   - Infer from: ROI indicators, cost savings, revenue mentions

4. **Generate scorecard** (concise, 1 page max):

```
# Impact Assessment: Proto-XXX - [Project Name]

**Generated**: 2025-11-09
**Project**: prototypes/proto-XXX-name/
**Status**: [ACTIVE/COMPLETED/etc]
**Phase**: [Phase name from .project]

---

## 📊 Impact Scorecard

| Dimension | Score | Assessment |
|-----------|-------|------------|
| 💪 **Level of Effort** | 3/10 | Moderate complexity - 2-3 week build |
| 🔄 **Usage Frequency** | 8/10 | Daily automated usage expected |
| 👥 **Audience Size** | 4/10 | Team tool (5-10 users) |
| 🎯 **Business Impact** | 7/10 | Saves 10hrs/week team time |
| 💰 **Financial Impact** | 6/10 | $50K/year cost savings |

**Overall Impact Score**: **6.2/10** ⭐⭐⭐

---

## 📈 Impact Analysis

**Effort vs. Value**:
- **ROI Ratio**: 2.1x (Value: 6.3 / Effort: 3.0)
- **Category**: 🟢 High-value, low-effort (Quick Win!)

**Usage Profile**:
- Frequency: Daily automation
- Users: 5-10 team members
- Total usage: ~40 hrs/month saved

**Business Value**:
- Primary: Time savings (10 hrs/week)
- Secondary: Reduced manual errors
- Annual value: ~$50,000 (labor cost savings)

**Key Insights**:
- Automation eliminates repetitive task
- ROI positive within first month
- Low maintenance burden (set and forget)

---

## 🎯 Recommendation

**Priority**: 🟢 **HIGH** - Implement immediately

**Rationale**:
- High ROI (2.1x)
- Quick implementation (2-3 weeks)
- Immediate team productivity gain
- Low ongoing maintenance

**Suggested Timeline**:
- Week 1-2: Core implementation
- Week 3: Testing + deployment
- Week 4: Monitor + iterate

---

## 📋 Impact Metrics Summary

```
Effort:    [███░░░░░░░] 3/10  (Lower is better)
Frequency: [████████░░] 8/10
Audience:  [████░░░░░░] 4/10
Business:  [███████░░░] 7/10
Financial: [██████░░░░] 6/10
═══════════════════════════════
Overall:   [██████░░░░] 6.2/10 ⭐⭐⭐
```

**Investment**: 2-3 weeks → **Return**: $50K/year

---

## 📎 Metadata

- **Assessment Date**: 2025-11-09
- **Project Phase**: IMPLEMENTATION
- **Tech Stack**: [List from .project]
- **Dependencies**: X packages
- **Source Files**: X files, ~X LOC
- **Assessment Version**: 1.0
```

5. **Save assessment**:
   - Create `meta/impact-assessment/` if not exists
   - Save as: `meta/impact-assessment/proto-XXX-name.md`
   - Update `meta/impact-assessment/INDEX.md` with entry
   - Link back to project README

6. **Update index** (`meta/impact-assessment/INDEX.md`):
   - Sorted by overall score (highest first)
   - Include date, score, phase, recommendation
   - Generate summary stats (avg score, distribution)

## Scoring Rubrics

### Level of Effort (LOE) [Inverse: 0 = high effort, 10 = low effort]

| Score | Time | Complexity | Indicators |
|-------|------|------------|------------|
| 10 | Hours | Trivial | Single script, <100 LOC, no deps |
| 8-9 | 1-3 days | Simple | 1-2 files, <500 LOC, few deps |
| 6-7 | 1 week | Moderate | 5-10 files, ~1K LOC, standard stack |
| 4-5 | 2-3 weeks | Medium | 10-20 files, 2-5K LOC, API + DB |
| 2-3 | 1-2 months | Complex | 20+ files, 5-10K LOC, microservices |
| 0-1 | 3+ months | Very complex | Multiple services, >10K LOC, distributed |

### Frequency of Usage

| Score | Frequency | Example |
|-------|-----------|---------|
| 10 | Continuous/Real-time | Production API, monitoring system |
| 8-9 | Multiple times daily | Dev tools, CI/CD pipeline |
| 6-7 | Daily | Daily reports, automation scripts |
| 4-5 | Weekly | Weekly analytics, batch jobs |
| 2-3 | Monthly | Monthly reports, occasional tools |
| 0-1 | One-time/Rare | Migration script, POC |

### Audience Size

| Score | Users | Scope |
|-------|-------|-------|
| 10 | 1000+ | Public API, customer-facing product |
| 8-9 | 100-1000 | Company-wide tool |
| 6-7 | 50-100 | Multi-department |
| 4-5 | 10-50 | Team/department tool |
| 2-3 | 2-10 | Small team |
| 0-1 | 1 | Personal tool |

### Business Impact

| Score | Impact Level | Indicators |
|-------|--------------|------------|
| 10 | Transformational | Core business model, competitive advantage |
| 8-9 | High | Revenue generation, major cost savings |
| 6-7 | Moderate | Process improvement, efficiency gains |
| 4-5 | Low-Moderate | Quality of life, minor improvements |
| 2-3 | Minimal | Experimental, learning value only |
| 0-1 | None | Toy project, no business application |

### Financial Impact (Annual Value)

| Score | Annual Value | Examples |
|-------|--------------|----------|
| 10 | $500K+ | 90% customer service automation |
| 8-9 | $100K-$500K | Sales enablement, major efficiency |
| 6-7 | $50K-$100K | Team productivity tool |
| 4-5 | $10K-$50K | Small process improvement |
| 2-3 | $1K-$10K | Minor utility |
| 0-1 | <$1K | No financial impact, toy/learning |

## Inference Strategy

**Automated scoring (AI infers from project files):**

1. **Read project description** → identify keywords:
   - "customer service", "automation", "sales" → high business/financial
   - "internal tool", "team", "developers" → moderate audience
   - "daily", "continuous", "production" → high frequency
   - "POC", "experiment", "learning" → low scores

2. **Analyze code complexity**:
   - File count, LOC, dependencies → effort score
   - Tech stack (microservices, databases) → complexity indicators

3. **Extract explicit metrics** (if documented):
   - "saves X hours/week" → calculate financial impact
   - "reduces cases by 90%" → high impact score
   - "5-10 users" → audience size

4. **Ask clarifying questions** if ambiguous:
   ```
   📊 Impact Assessment: Proto-XXX

   I've analyzed the project and estimated scores.
   To improve accuracy, clarify:

   1. Expected usage frequency? (daily/weekly/monthly)
   2. Target audience size? (1/10/100/1000+ users)
   3. Time/cost savings estimate? ($X/year or X hrs/week)

   Or proceed with auto-assessed scores?
   ```

5. **Use defaults for missing data**:
   - If no usage info → assume weekly (5/10)
   - If no audience info → assume team (4/10)
   - If no ROI data → estimate from time savings

## All Projects Report

When `--all` flag used:

```
# Impact Assessment: All Projects

**Generated**: 2025-11-09
**Projects Assessed**: 15
**Total Portfolio Value**: ~$850K/year

---

## 🏆 Top Impact Projects

| Rank | Project | Score | ROI | Phase | Recommendation |
|------|---------|-------|-----|-------|----------------|
| 1 | proto-007-flowey-sdlc | 8.5 | 3.2x | IMPL | 🟢 Critical - fast-track |
| 2 | proto-012-genai-adoption | 7.8 | 2.8x | COMP | 🟢 Deploy + promote |
| 3 | proto-014-project-portfolio | 6.9 | 2.1x | IMPL | 🟢 Complete this sprint |

## 📊 Portfolio Distribution

**By Impact Score:**
- High (8-10): 3 projects (20%)
- Moderate (5-7): 8 projects (53%)
- Low (0-4): 4 projects (27%)

**By ROI:**
- Excellent (>3x): 2 projects
- Good (2-3x): 5 projects
- Fair (1-2x): 6 projects
- Poor (<1x): 2 projects

**By Phase:**
- Completed: 4 projects
- Implementation: 7 projects
- Design: 3 projects
- Research: 1 project

## 💰 Financial Summary

**Total Annual Value**: ~$850,000
**Total Investment**: ~45 weeks
**Average ROI**: 2.3x
**Quick Wins (>2.5x ROI)**: 5 projects

## 🎯 Recommendations

**Immediate action:**
1. Fast-track proto-007 (highest impact, nearly complete)
2. Promote proto-012 (completed, high ROI)
3. Deprioritize proto-003 (low ROI, complex)

**Portfolio health:**
- 73% projects have positive ROI
- 53% in high-value category
- Recommend focusing on top 5 for maximum impact
```

## Pre-Commit Hook Integration

If `--setup-hook` flag provided, create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Auto-generate impact assessment if >20% files changed

CHANGED_FILES=$(git diff --cached --name-only | wc -l)
TOTAL_FILES=$(find . -type f -not -path "./.git/*" | wc -l)
CHANGE_PERCENT=$((CHANGED_FILES * 100 / TOTAL_FILES))

if [ $CHANGE_PERCENT -gt 20 ]; then
  echo "📊 Significant changes detected (${CHANGE_PERCENT}% of files)"
  echo "Generating impact assessment..."

  # Run impact assessment
  claude-code "/impact-assessment"

  # Add generated assessment to commit
  git add meta/impact-assessment/
fi
```

## Implementation Notes

1. **Parallel file operations** - Read all project files together
2. **Cache assessments** - Don't regenerate if project unchanged
3. **Version assessments** - Track changes over time (v1, v2, etc.)
4. **Link bidirectionally** - Project README ↔ Assessment
5. **Machine-readable format** - Include JSON metadata block

## Assessment Metadata (YAML frontmatter)

```yaml
---
project: proto-002-bedrock-joke-api
assessment_date: 2025-11-09
assessment_version: 1.0
scores:
  effort: 3
  frequency: 8
  audience: 4
  business_impact: 7
  financial_impact: 6
  overall: 6.2
metrics:
  roi_ratio: 2.1
  annual_value_usd: 50000
  implementation_weeks: 2-3
  user_count: 5-10
recommendation: HIGH
phase: IMPLEMENTATION
---
```

---

**Goal**: Provide objective, data-driven impact assessment to prioritize projects and maximize ROI.
