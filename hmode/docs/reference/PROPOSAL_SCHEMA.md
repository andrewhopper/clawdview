# Proposal Schema Extension

> **Purpose:** Define proposal review and prioritization fields for `.project` files
> **Integrates with:** PROJECT_METADATA.md, SDLC phases, gate criteria

---

## 1.0 Schema Overview

The `proposal` field extends `.project` with prioritization and review tracking:

```json
{
  "name": "proto-example",
  "version": "0.3.0",
  "current_phase": "IDEA_EXPANSION",
  "phase_number": 3,
  "...existing fields...",

  "proposal": {
    "one_pager": "docs/ONE_PAGER.md",
    "strategic_alignment": {...},
    "rice_score": {...},
    "wsjf_score": {...},
    "moscow": "should_have",
    "review_history": [...]
  }
}
```

---

## 2.0 Field Definitions

### 2.1 `one_pager` (string, optional)

Path to the proposal one-pager document (mini PR/FAQ).

```json
"one_pager": "docs/ONE_PAGER.md"
```

**Template:** `/shared/templates/ONE_PAGER.md`

---

### 2.2 `strategic_alignment` (object)

Links proposal to organizational goals.

```json
"strategic_alignment": {
  "okr_link": "Q4-2025-OKR-3",
  "alignment_score": 8,
  "committed_or_aspirational": "aspirational",
  "notes": "Directly supports revenue expansion goal"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `okr_link` | string | Reference to related OKR |
| `alignment_score` | int (1-10) | How well aligned to strategy |
| `committed_or_aspirational` | enum | "committed" or "aspirational" |
| `notes` | string | Justification for score |

---

### 2.3 `rice_score` (object)

RICE prioritization score (Intercom model).

```json
"rice_score": {
  "reach": 5000,
  "impact": 2,
  "confidence": 0.8,
  "effort": 3,
  "total": 2667
}
```

| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `reach` | int | Users affected per quarter | 0-∞ |
| `impact` | float | Effect magnitude | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal |
| `confidence` | float | Certainty level | 1.0=high, 0.8=medium, 0.5=low |
| `effort` | float | Person-months | 0.1-∞ |
| `total` | float | Calculated score | Auto-computed |

**Formula:** `total = (reach × impact × confidence) / effort`

---

### 2.4 `wsjf_score` (object)

WSJF prioritization score (SAFe model).

```json
"wsjf_score": {
  "business_value": 8,
  "time_criticality": 3,
  "risk_reduction": 5,
  "job_size": 5,
  "cost_of_delay": 16,
  "total": 3.2
}
```

| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `business_value` | int | Revenue/satisfaction impact | Fibonacci (1,2,3,5,8,13,21) |
| `time_criticality` | int | Cost of waiting | Fibonacci |
| `risk_reduction` | int | Enables other work / reduces risk | Fibonacci |
| `job_size` | int | Relative effort | Fibonacci |
| `cost_of_delay` | int | BV + TC + RR | Auto-computed |
| `total` | float | CoD / Job Size | Auto-computed |

**Formula:** `total = (business_value + time_criticality + risk_reduction) / job_size`

---

### 2.5 `moscow` (enum)

MoSCoW prioritization category.

```json
"moscow": "should_have"
```

| Value | Description |
|-------|-------------|
| `must_have` | Non-negotiable for release |
| `should_have` | Important but not critical |
| `could_have` | Nice to have if time permits |
| `wont_have` | Explicitly out of scope |

---

### 2.6 `review_history` (array)

Audit trail of review decisions.

```json
"review_history": [
  {
    "date": "2025-11-22T14:30:00Z",
    "decision": "go",
    "reviewer": "portfolio_committee",
    "gate": 3,
    "notes": "Approved for Phase 3 expansion"
  },
  {
    "date": "2025-11-20T10:00:00Z",
    "decision": "recycle",
    "reviewer": "tech_lead",
    "gate": 2,
    "notes": "Need to clarify technical approach"
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `date` | ISO 8601 | When review occurred |
| `decision` | enum | "go", "kill", "hold", "recycle" |
| `reviewer` | string | Who made decision |
| `gate` | int | Phase transition reviewed |
| `notes` | string | Rationale/feedback |

---

## 3.0 Gate Criteria

Phase transitions require minimum scores:

| Phase → Phase | RICE Min | Alignment Min | Auto-Approve |
|---------------|----------|---------------|--------------|
| 1 → 2 | 500 | - | Always |
| 2 → 3 | 1000 | - | RICE ≥ 2000 |
| 3 → 4 | - | 6 | Alignment ≥ 8 |
| 5 → 6 | 1500 | 6 | - |
| 6 → 7 | 2000 | 7 | RICE ≥ 5000 |
| 7 → 8 | - | - | Tests exist |
| 8 → 9 | - | - | Tests passing |

**Auto-approve:** If threshold met, no committee review required.

---

## 4.0 Composite Score

For portfolio ranking, use composite score:

```
Composite = (RICE × 0.6) + (Alignment × 100 × 0.4)
```

**Example:**
- RICE = 2667
- Alignment = 8

```
Composite = (2667 × 0.6) + (8 × 100 × 0.4) = 1600.2 + 320 = 1920.2
```

---

## 5.0 Tooling

### CLI Tool

```bash
# Calculate score
python hmode/shared/tools/proposal-scorer/proposal_scorer.py score path/to/project

# Rank all projects
python hmode/shared/tools/proposal-scorer/proposal_scorer.py rank --base .

# Check gate criteria
python hmode/shared/tools/proposal-scorer/proposal_scorer.py gate-check path/to/project --target-phase 7

# Update scores interactively
python hmode/shared/tools/proposal-scorer/proposal_scorer.py update path/to/project -i
```

### Slash Commands

| Command | Purpose |
|---------|---------|
| `/score-proposal [path]` | Calculate and display scores |
| `/rank-projects` | Show ranked project list |
| `/gate-check [path] [phase]` | Validate phase transition |

---

## 6.0 Example: Complete Proposal Block

```json
{
  "name": "proto-semantic-search-api",
  "version": "0.4.0",
  "current_phase": "IDEA_ANALYSIS",
  "phase_number": 4,
  "status": "ACTIVE",
  "description": "API for semantic search across enterprise documents",

  "proposal": {
    "one_pager": "docs/ONE_PAGER.md",
    "strategic_alignment": {
      "okr_link": "Q4-2025-OKR-2",
      "alignment_score": 9,
      "committed_or_aspirational": "committed",
      "notes": "Critical for enterprise search initiative"
    },
    "rice_score": {
      "reach": 10000,
      "impact": 2,
      "confidence": 0.8,
      "effort": 4,
      "total": 4000
    },
    "wsjf_score": {
      "business_value": 13,
      "time_criticality": 8,
      "risk_reduction": 5,
      "job_size": 8,
      "cost_of_delay": 26,
      "total": 3.25
    },
    "moscow": "must_have",
    "review_history": [
      {
        "date": "2025-11-22T14:30:00Z",
        "decision": "go",
        "reviewer": "portfolio_committee",
        "gate": 4,
        "notes": "High strategic value, proceed to analysis"
      },
      {
        "date": "2025-11-18T10:00:00Z",
        "decision": "go",
        "reviewer": "self",
        "gate": 2,
        "notes": "Auto-approved: RICE 4000 > 2000"
      }
    ]
  }
}
```

---

## 7.0 Sources

- [RICE Framework](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)
- [WSJF in SAFe](https://framework.scaledagile.com/wsjf)
- [Amazon PR/FAQ](https://productstrategy.co/working-backwards-the-amazon-prfaq-for-product-innovation/)
- [Google OKRs](https://rework.withgoogle.com/intl/en/guides/set-goals-with-okrs)
- [Stage-Gate Process](https://www.toolshero.com/innovation/stage-gate-process/)

---

[END OF PROPOSAL SCHEMA]
