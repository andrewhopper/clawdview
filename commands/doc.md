---
description: Quick artifact selection menu - generate documents, diagrams, reviews
tags: [artifact, document, generate, sdlc]
args:
  - name: selection
    description: "Optional: direct selection (e.g., 'prd', 'a3', '2b')"
    required: false
---

# Document Generator - Quick Artifact Selection

Present a numbered/lettered menu for fast artifact selection.

## Trigger Phrases

This command triggers on:
- "give me a doc"
- "give me a document"
- "I need a document"
- "generate a doc"
- "/doc"

## Execution

### If No Selection Provided

Display this menu:

```
📄 Document Generator

Select artifact type by code (e.g., "a3" or "prd"):

─────────────────────────────────────────────────
A. REQUIREMENTS
─────────────────────────────────────────────────
  [a1] PRD                Product Requirements Document
  [a2] functional-reqs    Functional Requirements
  [a3] nonfunctional-reqs Non-Functional Requirements
  [a4] user-stories       User Stories Collection

─────────────────────────────────────────────────
B. ARCHITECTURE & DESIGN
─────────────────────────────────────────────────
  [b1] architecture-doc   System Architecture Document
  [b2] data-model-doc     Data Model Document
  [b3] api-design         API Design Document
  [b4] system-design      System Design Document

─────────────────────────────────────────────────
C. TECHNOLOGY & DECISIONS
─────────────────────────────────────────────────
  [c1] tech-selection     Technology Selection Approval
  [c2] vendor-evaluation  Vendor Evaluation Matrix
  [c3] feasibility-study  Feasibility Study

─────────────────────────────────────────────────
D. PLANNING
─────────────────────────────────────────────────
  [d1] execution-plan     Execution Plan
  [d2] project-charter    Project Charter
  [d3] sprint-plan        Sprint Plan
  [d4] risk-assessment    Risk Assessment

─────────────────────────────────────────────────
E. STANDARDS & GUIDES
─────────────────────────────────────────────────
  [e1] naming-conventions Naming Conventions
  [e2] setup-guide        Setup Guide
  [e3] coding-standards   Coding Standards
  [e4] onboarding-doc     Onboarding Document
  [e5] runbook            Operations Runbook

─────────────────────────────────────────────────
F. REVIEWS & APPROVALS (SDLC Gates)
─────────────────────────────────────────────────
  [f1] architecture-review  Architecture Review
  [f2] data-model-review    Data Model Review
  [f3] security-review      Security Review
  [f4] performance-review   Performance Review
  [f5] code-review-checklist Code Review Checklist

─────────────────────────────────────────────────
G. BRIEFS & REPORTS
─────────────────────────────────────────────────
  [g1] executive-brief    Executive Brief (300-500 words)
  [g2] one-pager          One Pager / PR-FAQ
  [g3] research-brief     Research Brief
  [g4] findings-report    Findings Report

─────────────────────────────────────────────────
H. DIAGRAMS
─────────────────────────────────────────────────
  [h1] architecture-diagram  Architecture Diagram (HTML)
  [h2] data-flow-diagram     Data Flow Diagram (HTML)
  [h3] sequence-diagram      Sequence Diagram (Mermaid)
  [h4] entity-relationship   ER Diagram (Mermaid)

Select: [code/name] or [n] to cancel
```

### If Selection Provided

Parse the selection:
- **By code**: `a1`, `b3`, `f2`, etc.
- **By name**: `prd`, `tech-selection`, `architecture-review`, etc.
- **By alias**: `PRD`, `arch doc`, `tech approval`, etc.

### Selection Mapping

```yaml
# Requirements (A)
a1: prd
a2: functional-reqs
a3: nonfunctional-reqs
a4: user-stories

# Architecture (B)
b1: architecture-doc
b2: data-model-doc
b3: api-design
b4: system-design

# Technology (C)
c1: tech-selection
c2: vendor-evaluation
c3: feasibility-study

# Planning (D)
d1: execution-plan
d2: project-charter
d3: sprint-plan
d4: risk-assessment

# Standards (E)
e1: naming-conventions
e2: setup-guide
e3: coding-standards
e4: onboarding-doc
e5: runbook

# Reviews (F)
f1: architecture-review
f2: data-model-review
f3: security-review
f4: performance-review
f5: code-review-checklist

# Briefs (G)
g1: executive-brief
g2: one-pager
g3: research-brief
g4: findings-report

# Diagrams (H)
h1: architecture-diagram
h2: data-flow-diagram
h3: sequence-diagram
h4: entity-relationship
```

### After Selection

1. **Load artifact definition** from `hmode/shared/artifact-library/catalog/{artifact-id}/artifact.yaml`
2. **Check for required inputs** in the schema
3. **Ask for context**:
   ```
   Generating: {Artifact Name}

   I need some context:
   1. What is this for? (project/feature name)
   2. [Any artifact-specific required inputs]

   Or paste existing context/documentation.
   ```
4. **Generate the artifact** following the artifact.yaml prompt and schema
5. **Validate** against validators if defined
6. **Present result** with menu:
   ```
   Generated: {Artifact Name}

   Open: [1] Save as .md  [2] Copy to clipboard  [3] Show full
   ```

## Quick Examples

```bash
# Show menu
/doc

# Direct selection by code
/doc a1          # → PRD
/doc f1          # → Architecture Review
/doc h3          # → Sequence Diagram

# Direct selection by name
/doc prd
/doc tech-selection
/doc architecture-review

# Natural language (trigger detection)
"give me a doc"           # → shows menu
"give me a prd"           # → generates PRD
"I need a tech selection" # → generates tech selection
```

## SDLC Gate Quick Reference

When at an SDLC gate, suggest the appropriate artifact:

| At Gate | Suggest |
|---------|---------|
| Phase 2.5 (Feasibility) | `c3` feasibility-study |
| Phase 5 (Selection) | `c1` tech-selection |
| Phase 5.5 (PRD) | `a1` prd |
| Phase 6 (Design) | `f1` architecture-review, `f2` data-model-review |
| Phase 8 (Implementation) | `d1` execution-plan, `e1` naming-conventions |
| Phase 9 (Review) | `f3` security-review, `f4` performance-review |

---

**Version**: 1.0.0
**Created**: 2025-12-10
**Registry**: hmode/shared/artifact-library/catalog/registry.yaml
