# Artifact Library Menu

**Version:** 2.0.0
**Updated:** 2025-12-10

Quick reference for all standard artifacts. Say "give me a [artifact name]" to generate.

---

## SDLC Gate Artifacts

Every gate in the SDLC has an associated approval artifact:

| Phase | Gate | Approval Artifact | Purpose |
|-------|------|-------------------|---------|
| 2.5 | Feasibility Gate | `feasibility-study` | Go/no-go decision |
| 5 | Selection Gate | `tech-selection` | Technology stack approval |
| 5.5 | PRD Gate | `prd` | Requirements approval |
| 6 | Design Gate | `architecture-review` | Architecture approval |
| 6 | Design Gate | `data-model-review` | Data model approval |
| 6 | Design Gate | `api-design` | API design approval |
| 7 | Test Gate | `test-plan` | Test strategy approval |
| 8 | Implementation Gate | `execution-plan` | Implementation plan |
| 8 | Standards Gate | `naming-conventions` | Naming standards |
| 8 | Standards Gate | `coding-standards` | Code style standards |
| 9 | Review Gate | `security-review` | Security approval |
| 9 | Review Gate | `performance-review` | Performance approval |

**Usage:** Before passing a gate, generate the corresponding approval artifact.

---

## Quick Reference by Phase

```
SDLC Phase          Artifacts Available
─────────────────────────────────────────────────────────────────
1. SEED/IDEA        idea-capture, concept-brief
2. RESEARCH         research-brief, competitive-analysis, market-research
3. REQUIREMENTS     prd, functional-reqs, nonfunctional-reqs, user-stories
4. DESIGN           architecture-doc, data-model-doc, api-design, system-design
5. SELECTION        tech-selection, vendor-evaluation
6. PLANNING         execution-plan, project-charter, risk-assessment
7. STANDARDS        naming-conventions, setup-guide, coding-standards
8. IMPLEMENTATION   implementation-plan, sprint-plan
9. REVIEW           code-review, security-review, architecture-review
```

---

## 1.0 BRIEFS (Quick Summaries)

| ID | Name | When to Use | Word Range |
|----|------|-------------|------------|
| `executive-brief` | Executive Brief | C-suite decision summary | 300-500 |
| `one-pager` | One Pager (PR/FAQ) | New initiative pitch | 800-1500 |
| `research-brief` | Research Brief | Summarize research findings | 800-3000 |
| `concept-brief` | Concept Brief | Early-stage idea summary | 200-400 |

**Triggers:** "executive summary", "one-pager", "PR/FAQ", "brief for leadership"

---

## 2.0 REQUIREMENTS DOCUMENTS

| ID | Name | When to Use | Sections |
|----|------|-------------|----------|
| `prd` | Product Requirements Document | Full product spec | 8-12 |
| `functional-reqs` | Functional Requirements | What the system does | 5-10 |
| `nonfunctional-reqs` | Non-Functional Requirements | Quality attributes | 6-8 |
| `user-stories` | User Stories Collection | Agile requirements | N/A |
| `use-cases` | Use Cases Document | Detailed interactions | 4-8 |
| `acceptance-criteria` | Acceptance Criteria | Test conditions | N/A |

**Triggers:** "PRD", "requirements doc", "functional requirements", "user stories"

---

## 3.0 ARCHITECTURE & DESIGN

| ID | Name | When to Use | Sections |
|----|------|-------------|----------|
| `architecture-doc` | Architecture Document | System architecture | 10-15 |
| `architecture-review` | Architecture Review | Evaluate existing arch | 8-10 |
| `data-model-doc` | Data Model Document | Database/entity design | 6-10 |
| `api-design` | API Design Document | REST/GraphQL spec | 8-12 |
| `system-design` | System Design Document | High-level design | 10-14 |
| `component-design` | Component Design | Individual component | 5-8 |
| `integration-design` | Integration Design | System integrations | 6-10 |

**Triggers:** "architecture document", "data model", "API design", "system design"

---

## 4.0 TECHNOLOGY & SELECTION

| ID | Name | When to Use | Sections |
|----|------|-------------|----------|
| `tech-selection` | Technology Selection Approval | Choose tech stack | 8-12 |
| `vendor-evaluation` | Vendor Evaluation Matrix | Compare vendors | 5-8 |
| `tool-assessment` | Tool Assessment | Evaluate tools | 6-8 |
| `migration-assessment` | Migration Assessment | Tech migration plan | 8-12 |
| `feasibility-study` | Feasibility Study | Go/no-go decision | 6-10 |

**Triggers:** "tech selection", "technology approval", "vendor comparison", "feasibility"

---

## 5.0 PLANNING & EXECUTION

| ID | Name | When to Use | Sections |
|----|------|-------------|----------|
| `execution-plan` | Execution Plan | Implementation roadmap | 8-12 |
| `project-charter` | Project Charter | Project kickoff | 6-10 |
| `sprint-plan` | Sprint Plan | Sprint scope/goals | 4-6 |
| `release-plan` | Release Plan | Release strategy | 6-8 |
| `risk-assessment` | Risk Assessment | Risk identification | 5-8 |
| `resource-plan` | Resource Plan | Team/resource needs | 4-6 |

**Triggers:** "execution plan", "project plan", "sprint plan", "risk assessment"

---

## 6.0 STANDARDS & GUIDES

| ID | Name | When to Use | Sections |
|----|------|-------------|----------|
| `naming-conventions` | Naming Conventions | Code/file naming rules | 5-8 |
| `setup-guide` | Setup Guide | Dev environment setup | 6-10 |
| `coding-standards` | Coding Standards | Code style rules | 8-12 |
| `contribution-guide` | Contribution Guide | How to contribute | 5-8 |
| `onboarding-doc` | Onboarding Document | New team member guide | 8-12 |
| `runbook` | Runbook | Operations procedures | 6-10 |

**Triggers:** "naming conventions", "setup guide", "coding standards", "onboarding"

---

## 7.0 REVIEW & APPROVAL

| ID | Name | When to Use | Sections |
|----|------|-------------|----------|
| `architecture-review` | Architecture Review | Evaluate architecture | 8-10 |
| `data-model-review` | Data Model Review | Evaluate data model | 6-8 |
| `security-review` | Security Review | Security assessment | 8-12 |
| `performance-review` | Performance Review | Performance analysis | 6-10 |
| `accessibility-review` | Accessibility Review | A11y compliance | 6-8 |
| `code-review-checklist` | Code Review Checklist | PR review guide | 4-6 |

**Triggers:** "architecture review", "security review", "code review checklist"

---

## 8.0 REPORTS & FINDINGS

| ID | Name | When to Use | Sections |
|----|------|-------------|----------|
| `findings-report` | Findings Report | Analysis results | 6-8 |
| `audit-report` | Audit Report | Compliance audit | 8-12 |
| `incident-report` | Incident Report | Incident postmortem | 6-10 |
| `status-report` | Status Report | Progress update | 4-6 |
| `retrospective` | Retrospective | Sprint/project retro | 4-6 |

**Triggers:** "findings report", "audit report", "incident report", "retro"

---

## 9.0 DIAGRAMS (Visual Artifacts)

| ID | Name | When to Use | Format |
|----|------|-------------|--------|
| `architecture-diagram` | Architecture Diagram | System overview | HTML/SVG |
| `data-flow-diagram` | Data Flow Diagram | Data movement | HTML/SVG |
| `sequence-diagram` | Sequence Diagram | Interaction flow | Mermaid |
| `entity-relationship` | ER Diagram | Database schema | Mermaid |
| `deployment-diagram` | Deployment Diagram | Infrastructure | HTML/SVG |
| `component-diagram` | Component Diagram | Component view | HTML/SVG |
| `user-journey` | User Journey Map | UX flow | HTML/SVG |

**Triggers:** "architecture diagram", "ER diagram", "sequence diagram", "data flow"

---

## Usage Examples

```
User: "Give me a PRD for the new search feature"
→ Generates: Product Requirements Document

User: "I need a tech selection document for choosing a database"
→ Generates: Technology Selection Approval Document

User: "Create an architecture review for the payment system"
→ Generates: Architecture Review Document

User: "Give me naming conventions for this Python project"
→ Generates: Naming Conventions Document
```

---

## Artifact Structure

All artifacts follow this pattern:

```yaml
# Metadata
id: artifact-id
name: Human Readable Name
category: requirements | architecture | planning | standards | review
complexity: simple | moderate | complex

# Schema (sections)
schema:
  sections:
    - id: section-id
      name: Section Name
      required: true
      format: prose | bullets | table | code

# Generation prompt
prompt:
  system: Role and style
  task: What to generate
  tone: professional | technical | conversational

# Validators
validators:
  - word count
  - required sections
  - quality checks
```

---

## Adding New Artifacts

1. Check if exists: `shared/artifact-library/catalog/`
2. Create folder: `catalog/{artifact-id}/`
3. Create definition: `artifact.yaml`
4. Add examples: `examples/`
5. Update registry: `catalog/registry.yaml`

Template: See `shared/artifact-library/schema.yaml`

---

## Quick Commands

| Say... | Get... |
|--------|--------|
| "PRD" | Product Requirements Document |
| "architecture doc" | Architecture Document |
| "tech selection" | Technology Selection Approval |
| "data model doc" | Data Model Document |
| "execution plan" | Execution Plan |
| "naming conventions" | Naming Conventions |
| "setup guide" | Setup Guide |
| "security review" | Security Review |
| "arch review" | Architecture Review |

---

[END OF MENU]
