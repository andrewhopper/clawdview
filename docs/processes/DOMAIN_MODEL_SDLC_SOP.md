# Domain Model SDLC SOP

Standard operating procedure for creating and evolving domain models using the 9-phase SDLC with HTML review documents, human approval gates, and multi-option generation.

---

## 🤖 DOMAIN-MODELING-SPECIALIST AGENT

**For ALL domain modeling work, use the specialized agent:**

```bash
# Invoke the domain-modeling-specialist agent
Task(subagent_type="domain-modeling-specialist",
     prompt="Create domain model for {project} following SDLC")
```

**Agent Capabilities:**
- Executes full 9-phase SDLC for domain modeling
- Researches external standards (schema.org, GitHub, provider APIs)
- Generates HTML review documents for approval
- Creates ontology.ttl and rules.shacl.ttl files
- Manages domain evolution with semantic versioning
- Handles all approval gates and human interaction

**Agent Location:** `hmode/agents/domain-modeling-specialist.md`

---

## Overview

Domain models require rigorous design and validation. This SOP maps the 9-phase SDLC to domain modeling with:
- **HTML review documents** for stakeholder visualization
- **Human approval gates** at every phase transition
- **Multi-option generation** (3-5 options) at design phases
- **Research phase** for existing standards and patterns
- **Specialized agent** to orchestrate the entire workflow

---

## Phase Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DOMAIN MODEL SDLC                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. SEED ──────► 2. RESEARCH ──────► 3. EXPANSION ──────► 4. ANALYSIS       │
│     │                │                    │                    │             │
│     ▼                ▼                    ▼                    ▼             │
│  [Define need]   [Standards]         [3-5 entity        [Evaluate          │
│                  [Existing]           options]           options]           │
│                  [Patterns]                                                  │
│                                                                              │
│  ◄──────────────── HUMAN APPROVAL GATES ────────────────►                   │
│                                                                              │
│  5. SELECTION ──► 6. DESIGN ──────► 7. TEST_DESIGN ──► 8. IMPLEMENTATION   │
│     │                │                    │                    │             │
│     ▼                ▼                    ▼                    ▼             │
│  [Pick winner]   [ontology.ttl]      [SHACL rules]     [Generate types]    │
│  [HTML Review]   [HTML Review]       [Validation]      [Register domain]   │
│                                                                              │
│                              9. REFINEMENT                                   │
│                                    │                                         │
│                                    ▼                                         │
│                              [Evolution]                                     │
│                              [Versioning]                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: SEED - Domain Need Identification

**Goal:** Capture the domain model need
**Output:** `.project` file + `domain-{name}-seed.md`

### 1.1 Domain Need Capture

AI prompts human for:

```markdown
## New Domain Model Request

**Domain Name:** expense-report
**Purpose:** (1-2 sentences describing why this domain is needed)
**Trigger:** (What use case or prototype requires this domain?)
**Project Type:** [ ] exploration [ ] prototype [x] production

**Initial Entities (best guess):**
1. ExpenseReport
2. ExpenseLineItem
3. Receipt
4. ...
```

### 1.2 SEED Approval Gate

```markdown
## ✅ APPROVAL GATE: Phase 1 → 2

**Domain:** expense-report
**Purpose:** Corporate expense reporting and reimbursement workflows

**Proceed to Research?**
- [Y] Yes, research existing standards and patterns
- [N] No, needs more clarification
- [R] Revise scope (provide feedback)

Human response: ___
```

**WAIT for human response before proceeding.**

---

## Phase 2: RESEARCH - Standards & Patterns

**Goal:** Survey existing standards, patterns, and implementations
**Output:** `domain-{name}-research.md` (2 pages max)

### 2.1 Research Checklist

AI MUST research:

| Category | What to Find | Sources |
|----------|--------------|---------|
| **W3C Standards** | Relevant RDF vocabularies, OWL patterns | W3C, Schema.org |
| **Industry Standards** | Domain-specific standards (FHIR, HR-XML, etc.) | Industry bodies |
| **Existing Ontologies** | Published ontologies in this domain | LOV, ontology portals |
| **GitHub Projects** | Open-source domain models, generators | GitHub search |
| **Commercial Products** | How SaaS products model this domain | Product docs, APIs |
| **Internal Domains** | Existing protoflow domains to reuse | registry.yaml |

### 2.2 Research Output Format

```markdown
# Stage 2 - Domain Model Research: {domain-name}

## 2.1 W3C & Industry Standards

| Standard | Relevance | Key Entities | Notes |
|----------|-----------|--------------|-------|
| Schema.org/Invoice | High | Invoice, MonetaryAmount | Foundation for expense items |
| HR-XML | Medium | Expense, ExpenseReport | Enterprise HR standard |

## 2.2 Existing Ontologies

| Ontology | Stars/Maturity | Fit | Adaptation Effort |
|----------|----------------|-----|-------------------|
| expense-ontology.ttl | 45 stars | High | Low (90% reusable) |
| financial-core.owl | 200 stars | Medium | Medium (subset) |

## 2.3 Internal Domain Reuse

| Domain | Entities to Reuse | Why |
|--------|-------------------|-----|
| core | Money, TimePoint, Address | Standard primitives |
| auth | User, Principal | Submitter, Approver identity |

## 2.4 Build vs. Adapt Recommendation

- **Recommendation:** Adapt existing + extend
- **Base:** Schema.org/Invoice + expense-ontology.ttl
- **Extend with:** Approval workflow, Policy, Reimbursement
```

### 2.3 RESEARCH Approval Gate

```markdown
## ✅ APPROVAL GATE: Phase 2 → 3

**Research Summary:**
- Found 3 relevant standards (Schema.org, HR-XML, expense-ontology.ttl)
- Recommend adapting Schema.org/Invoice as base
- Will reuse: core (Money, TimePoint), auth (User)

**Proceed to Expansion?**
- [Y] Yes, generate entity options
- [R] Research deeper (specify area)
- [A] Abandon (existing solution sufficient)

Human response: ___
```

**WAIT for human response before proceeding.**

---

## Phase 3: EXPANSION - Entity Option Generation

**Goal:** Generate 3-5 entity model options
**Output:** `domain-{name}-expansion.md` + **HTML Review Document**

### 3.1 Generate Entity Options

AI generates 3-5 distinct modeling approaches:

```markdown
# Stage 3 - Entity Model Options: {domain-name}

## Option A: Minimal Core
**Philosophy:** Smallest viable model, extend later

| Entity | Properties | Relationships |
|--------|------------|---------------|
| ExpenseReport | id, title, status, totalAmount | → LineItem[] |
| LineItem | id, date, amount, category, vendor | → Receipt? |
| Receipt | id, fileUrl, mimeType | - |

**Pros:** Simple, fast to implement
**Cons:** Limited workflow support

---

## Option B: Full Workflow
**Philosophy:** Complete approval and reimbursement lifecycle

| Entity | Properties | Relationships |
|--------|------------|---------------|
| ExpenseReport | id, title, status, ... | → LineItem[], → ApprovalStep[] |
| LineItem | id, date, amount, ... | → Receipt?, → Policy |
| ApprovalStep | id, order, status, decision | → Approver |
| Policy | id, limits, categories | - |
| Reimbursement | id, amount, method, processedAt | → Report |

**Pros:** Enterprise-ready, audit trail
**Cons:** Complex, longer to implement

---

## Option C: Event-Sourced
**Philosophy:** Immutable event log, derived state

| Entity | Properties | Relationships |
|--------|------------|---------------|
| ExpenseEvent | id, type, timestamp, payload | → Report |
| ExpenseReport | (computed from events) | - |
| ...

**Pros:** Full audit history, temporal queries
**Cons:** Complex queries, eventual consistency
```

### 3.2 Generate HTML Review Document

AI generates interactive HTML for stakeholder review:

**Output:** `artifacts/{project-type}/domain-{name}-options-review.html`

```html
<!-- Template structure - AI fills in domain-specific content -->
<!DOCTYPE html>
<html>
<head>
    <title>{Domain Name} - Entity Model Options</title>
    <!-- Professional styling with cards, comparison table -->
</head>
<body>
    <header>
        <h1>{Domain Name} Domain Model</h1>
        <p>Phase 3: Entity Model Options Review</p>
    </header>

    <!-- Filter bar for option characteristics -->
    <div class="filter-bar">
        <button data-filter="minimal">Minimal</button>
        <button data-filter="full">Full Workflow</button>
        <button data-filter="event">Event-Sourced</button>
    </div>

    <!-- Option cards with pros/cons, entity diagrams -->
    <div class="options-grid">
        <!-- Option A card -->
        <!-- Option B card -->
        <!-- Option C card -->
    </div>

    <!-- Comparison matrix -->
    <table class="comparison-table">
        <tr>
            <th>Criteria</th>
            <th>Option A</th>
            <th>Option B</th>
            <th>Option C</th>
        </tr>
        <tr>
            <td>Entity Count</td>
            <td>3</td>
            <td>6</td>
            <td>4</td>
        </tr>
        <!-- ... more criteria -->
    </table>

    <!-- AI Recommendation section -->
    <div class="recommendation">
        <h2>AI Recommendation: Option B</h2>
        <p>Rationale: ...</p>
    </div>
</body>
</html>
```

### 3.3 EXPANSION Approval Gate

```markdown
## ✅ APPROVAL GATE: Phase 3 → 4

**HTML Review:** [Open Review Document](./domain-expense-report-options-review.html)

**Options Generated:**
| Option | Entities | Complexity | Best For |
|--------|----------|------------|----------|
| A | 3 | Low | Quick prototype |
| B | 6 | Medium | Production use |
| C | 4 | High | Audit-heavy use cases |

**AI Recommendation:** Option B (Full Workflow)

**Select an option or request changes:**
- [A] Select Option A
- [B] Select Option B (recommended)
- [C] Select Option C
- [H] Hybrid (specify which entities from which options)
- [R] Regenerate options (provide feedback)

Human response: ___
```

**WAIT for human response before proceeding.**

---

## Phase 4: ANALYSIS - Deep Evaluation

**Goal:** Deeply evaluate selected option
**Output:** `domain-{name}-analysis.md`

### 4.1 Evaluation Criteria

AI evaluates the selected option against:

| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| **Completeness** | How well does it cover the domain? | |
| **Composability** | Can it integrate with other domains? | |
| **Extensibility** | Can it evolve without breaking changes? | |
| **Standards Alignment** | Does it follow W3C/industry patterns? | |
| **Implementation Effort** | How long to implement? | |
| **Validation Complexity** | How hard to write SHACL rules? | |

### 4.2 Dependency Analysis

```markdown
## Dependency Analysis

### Inbound Dependencies (who will use this domain?)
- proto-expense-tracker: Will use ExpenseReport, LineItem
- Future payroll integration: Will use Reimbursement

### Outbound Dependencies (what domains does this need?)
- core: Money, TimePoint, AuditInfo
- auth: User, Principal, Permission

### Circular Dependency Check: ✅ None detected
```

### 4.3 ANALYSIS Approval Gate

```markdown
## ✅ APPROVAL GATE: Phase 4 → 5

**Selected Option:** B (Full Workflow)

**Evaluation Summary:**
| Criterion | Score | Status |
|-----------|-------|--------|
| Completeness | 5/5 | ✅ |
| Composability | 4/5 | ✅ |
| Extensibility | 5/5 | ✅ |
| Standards Alignment | 4/5 | ✅ |
| Implementation Effort | 3/5 | ⚠️ Medium |
| Validation Complexity | 3/5 | ⚠️ Medium |

**Proceed to Selection?**
- [Y] Yes, finalize this option
- [R] Revisit options (go back to Phase 3)
- [M] Modify selected option (specify changes)

Human response: ___
```

**WAIT for human response before proceeding.**

---

## Phase 5: SELECTION - Final Entity Selection

**Goal:** Lock in final entity model
**Output:** `domain-{name}-selection.md` + **Updated HTML Review**

### 5.1 Final Entity Model

```markdown
# Stage 5 - Final Selection: {domain-name}

## Selected Approach: Option B (Full Workflow)

## Final Entity List

| Entity | Status | Properties (key) | Relationships |
|--------|--------|------------------|---------------|
| ExpenseReport | ✅ Included | id, title, status, totalAmount | → LineItem[], → ApprovalStep[] |
| ExpenseLineItem | ✅ Included | id, date, amount, category, vendor | → Receipt?, → Policy |
| Receipt | ✅ Included | id, fileUrl, mimeType, ocrExtracted | - |
| ExpensePolicy | ✅ Included | id, name, limits, categories | - |
| ApprovalStep | ✅ Included | id, order, approver, status, decision | → User |
| Reimbursement | ✅ Included | id, amount, method, processedAt | → Report |

## MVP Scope

| Must Have | Nice to Have | Out of Scope |
|-----------|--------------|--------------|
| CRUD for all entities | OCR extraction | Currency conversion |
| Submit/Approve flow | Policy violation alerts | Multi-company |
| Basic SHACL validation | Bulk upload | Tax calculation |
```

### 5.2 Constraint Classification

**CRITICAL:** Constraints MUST be classified into two types before implementation. This determines where they are defined and how they can be modified.

```markdown
## Constraint Types

┌─────────────────────────────────────────────────────────────────────────────┐
│                        CONSTRAINT CLASSIFICATION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHYSICAL/UNIVERSAL CONSTRAINTS          BUSINESS/POLICY CONSTRAINTS         │
│  ───────────────────────────────         ──────────────────────────────     │
│  • Laws of nature                        • Organizational policies           │
│  • Mathematical truths                   • Regulatory requirements           │
│  • System limitations                    • Configurable thresholds           │
│                                                                              │
│  IMMUTABLE                               MUTABLE                             │
│  Hard-coded in SHACL                     Externalized to policy files        │
│  rules.shacl.ttl                         policy-rules.yaml + rules.shacl.ttl │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Physical/Universal Constraints

These constraints represent **immutable truths** that will never change regardless of business policy.

| Category | Constraint | Rationale | SHACL Pattern |
|----------|------------|-----------|---------------|
| **Human Biology** | Age: 0-120 years | Physical impossibility | `sh:minInclusive 0; sh:maxInclusive 120` |
| **Time** | Date not in future | Cannot expense future events | `sh:maxInclusive NOW()` |
| **Physics** | File size > 0 bytes | Cannot have negative size | `sh:minInclusive 1` |
| **Mathematics** | Amount >= 0 | Cannot have negative expense | `sh:minInclusive 0` |
| **Data Types** | Email format valid | RFC 5322 specification | `sh:pattern "^[a-zA-Z0-9._%+-]+@..."` |
| **System** | ID not null | Primary key requirement | `sh:minCount 1` |
| **Calendar** | Month: 1-12 | Gregorian calendar | `sh:minInclusive 1; sh:maxInclusive 12` |
| **Geography** | Latitude: -90 to 90 | Earth coordinates | `sh:minInclusive -90; sh:maxInclusive 90` |

**Characteristics:**
- ✅ Never change
- ✅ Hard-coded in `rules.shacl.ttl`
- ✅ Same across all organizations
- ✅ No configuration needed

### 5.4 Business/Policy Constraints

These constraints represent **organizational rules** that may vary by company, region, employee level, or time.

| Category | Constraint | Current Value | Varies By | Config Key |
|----------|------------|---------------|-----------|------------|
| **Submission** | Deadline after expense | 90 days | Company policy | `submission.deadline_days` |
| **Lodging** | Nightly rate limit | $100-$1000 | Region, level | `limits.lodging.{region}.{level}` |
| **Meals** | Per diem limit | $75 domestic | Country, city | `limits.meals.{country}.{city}` |
| **Receipt** | Required above threshold | $25 | Company policy | `receipt.threshold` |
| **Approval** | Auto-approve below | $100 | Department | `approval.auto_threshold.{dept}` |
| **Equipment** | Single item max | $500 | Role | `limits.equipment.{role}` |
| **Travel** | Airfare class | Economy | Flight duration | `travel.class.{duration}` |

**Characteristics:**
- ⚠️ Change with policy updates
- ⚠️ Externalized to `policy-config.yaml`
- ⚠️ May vary by region/role/level
- ⚠️ Requires configuration management

### 5.5 Policy Configuration Schema

Business constraints should be externalized to a configuration file:

```yaml
# policy-config.yaml
# Business constraints that may change - DO NOT hard-code in SHACL

version: "2025.1"
effective_date: "2025-01-01"
expires_date: "2025-12-31"

submission:
  deadline_days: 90
  late_submission_allowed: false
  late_approval_required: true

receipt:
  threshold: 25.00  # Require receipt above this amount
  required_categories: [Equipment, Software, Entertainment]

limits:
  lodging:
    default: { min: 100, max: 500 }
    us_metro: { min: 150, max: 1000 }  # NYC, SF, etc.
    international: { min: 100, max: 800 }
    executive: { min: 200, max: 1500 }

  meals:
    domestic: 75.00
    international: 100.00
    client_entertainment: 150.00

  equipment:
    default: 500
    manager_approval: 1000
    vp_approval: 5000

approval:
  auto_threshold: 100  # Auto-approve below this
  levels:
    - { max: 500, approver: "manager" }
    - { max: 5000, approver: "director" }
    - { max: null, approver: "vp_finance" }
```

### 5.6 Business Rules Capture

After classifying constraints, capture the specific business rules:

```markdown
## Business Rules

### Category-Specific Rules

| Category | Rule | Constraint | Rationale |
|----------|------|------------|-----------|
| Lodging | Hotel charges | $100-$1000/night | Corporate travel policy |
| Meals | Per diem limit | $75/day domestic, $100/day international | IRS guidelines |
| Travel | Airfare class | Economy only (unless >6hr flight) | Cost control |
| Equipment | Single item limit | Max $500 without pre-approval | Procurement policy |

### Temporal Rules

| Rule | Constraint | Implementation |
|------|------------|----------------|
| Expense year | Current or previous year only | SPARQL: YEAR(?date) >= YEAR(NOW()) - 1 |
| Submission deadline | Within 30 days of expense | SPARQL: ?submitDate - ?expenseDate <= 30 |
| Receipt age | Receipts within 90 days | SPARQL: NOW() - ?receiptDate <= 90 |

### Referential Rules

| Rule | Constraint | Error Message |
|------|------------|---------------|
| Approver hierarchy | Approver must be submitter's manager or above | "Approver must be in management chain" |
| Policy assignment | Report must reference active policy | "Policy is inactive or expired" |
| Project code | Must exist in finance system | "Invalid project code" |

### Conditional Rules

| Condition | Rule | Constraint |
|-----------|------|------------|
| If category = Lodging | Require check-in/check-out dates | Both dates required |
| If amount > $500 | Require receipt | Receipt mandatory |
| If international | Require currency code | ISO 4217 currency required |
| If rejected | Require rejection reason | Comments field mandatory |
```

### 5.7 SELECTION Approval Gate

```markdown
## ✅ APPROVAL GATE: Phase 5 → 6

**Final Model:**
- 6 entities: ExpenseReport, ExpenseLineItem, Receipt, ExpensePolicy, ApprovalStep, Reimbursement
- 8 actions: Create, AddLineItem, AttachReceipt, Submit, Approve, Reject, Reimburse, Search
- 3 enums: ExpenseReportStatus, ExpenseCategory, PaymentMethod

**Proceed to Design (ontology creation)?**
- [Y] Yes, create ontology.ttl
- [M] Modify (specify changes)
- [B] Back to Analysis

Human response: ___
```

**WAIT for human response before proceeding.**

---

## Phase 6: DESIGN - Ontology Creation

**Goal:** Create W3C-compliant ontology
**Output:** `ontology.ttl` + **HTML Ontology Review**

### 6.1 Ontology Generation

AI generates full `ontology.ttl` following patterns from existing domains:

```turtle
@prefix expense: <http://protoflow.ai/ontology/expense-report#> .
@prefix core: <http://protoflow.ai/ontology/core#> .
@prefix action: <http://protoflow.ai/ontology/action#> .
# ... full ontology
```

### 6.2 Generate Ontology Review HTML

**Output:** `artifacts/{project-type}/domain-{name}-ontology-review.html`

HTML includes:
- Entity relationship diagram (Mermaid/D3)
- Property tables per entity
- Action definitions with parameters
- Enum visualizations
- Comparison to selected option (Phase 5)

### 6.3 DESIGN Approval Gate

```markdown
## ✅ APPROVAL GATE: Phase 6 → 7

**Generated Files:**
- `ontology.ttl` (425 lines)
- [View Ontology Review HTML](./domain-expense-report-ontology-review.html)

**Ontology Summary:**
| Component | Count |
|-----------|-------|
| Classes (entities) | 6 |
| Object Properties | 12 |
| Datatype Properties | 28 |
| Actions | 8 |
| Enums | 3 |

**Review Checklist:**
- [ ] All entities from Phase 5 included
- [ ] All properties have rdfs:comment
- [ ] All entities have created_at/updated_at (Rule #18)
- [ ] Dependencies (core, auth) properly imported
- [ ] Actions have parameters and error conditions

**Approve ontology?**
- [Y] Yes, proceed to validation rules
- [R] Revise (specify changes)
- [B] Back to Selection

Human response: ___
```

**WAIT for human response before proceeding.**

---

## Phase 7: TEST_DESIGN - SHACL Validation Rules

**Goal:** Define validation constraints (separated by constraint type)
**Output:**
- `rules.shacl.ttl` - Physical/universal constraints (immutable)
- `policy-rules.shacl.ttl` - Business/policy constraints (references config)
- `policy-config.yaml` - Externalized policy values

### 7.1 File Structure for Constraint Separation

```
/hmode/hmode/shared/semantic/domains/expense-report/
├── ontology.ttl              # Entity definitions
├── rules.shacl.ttl           # PHYSICAL constraints (immutable)
├── policy-rules.shacl.ttl    # BUSINESS constraints (configurable)
├── policy-config.yaml        # Externalized policy values
└── version.json              # Domain metadata
```

**Why Separate Files?**
| File | Contains | Changes | Deployment |
|------|----------|---------|------------|
| `rules.shacl.ttl` | Physical constraints | Never | With code releases |
| `policy-rules.shacl.ttl` | Business rule logic | Rarely | With code releases |
| `policy-config.yaml` | Threshold values | Frequently | Hot-reloadable |

### 7.2 Validation Rule Categories by Type

| Category | Type | Examples | File | SHACL Pattern |
|----------|------|----------|------|---------------|
| **Required Fields** | Physical | ID not null, timestamps | `rules.shacl.ttl` | `sh:minCount 1` |
| **Format Constraints** | Physical | Email, URL formats | `rules.shacl.ttl` | `sh:pattern` |
| **Physical Ranges** | Physical | Amount >= 0, age 0-120 | `rules.shacl.ttl` | `sh:minInclusive` |
| **Enum Validation** | Physical | Status values | `rules.shacl.ttl` | `sh:in` |
| **Policy Limits** | Business | Hotel $100-$1000 | `policy-rules.shacl.ttl` | Config reference |
| **Policy Deadlines** | Business | 90-day submission | `policy-rules.shacl.ttl` | Config reference |
| **Policy Thresholds** | Business | Receipt if > $25 | `policy-rules.shacl.ttl` | Config reference |
| **Referential** | Physical | Valid approver | `rules.shacl.ttl` | `sh:class` |

### 7.3 Physical Constraints (rules.shacl.ttl)

These are **immutable truths** - hard-coded, never change:

```turtle
# rules.shacl.ttl - PHYSICAL/UNIVERSAL CONSTRAINTS ONLY

# Amount cannot be negative (mathematical truth)
expense:AmountNonNegativeConstraint a sh:NodeShape ;
    sh:targetClass expense:ExpenseLineItem ;
    sh:property [
        sh:path expense:amount ;
        sh:minInclusive 0 ;
        sh:message "Amount cannot be negative"
    ] .

# Expense date cannot be in future (temporal impossibility)
expense:DateNotFutureConstraint a sh:NodeShape ;
    sh:targetClass expense:ExpenseLineItem ;
    sh:sparql [
        sh:message "Expense date cannot be in the future" ;
        sh:select "SELECT $this WHERE { $this expense:expenseDate ?d . FILTER(?d > NOW()) }"
    ] .

# File size must be positive (physical impossibility)
expense:FileSizePositiveConstraint a sh:NodeShape ;
    sh:targetClass expense:Receipt ;
    sh:property [
        sh:path expense:fileSize ;
        sh:minInclusive 1 ;
        sh:message "File size must be positive"
    ] .
```

### 7.4 Business Constraints (policy-rules.shacl.ttl)

These reference **externalized configuration** - values loaded from `policy-config.yaml`:

```turtle
# policy-rules.shacl.ttl - BUSINESS CONSTRAINTS
# Values come from policy-config.yaml, NOT hard-coded

# Lodging rate limit - references config value
expense:LodgingRateLimitConstraint a sh:NodeShape ;
    sh:targetClass expense:ExpenseLineItem ;
    sh:sparql [
        sh:message "Lodging exceeds policy limit" ;
        sh:select """
            SELECT $this WHERE {
                $this expense:category expense:Lodging .
                $this expense:amount ?amount .
                policy:config policy:lodgingMax ?max .  # From config
                FILTER (?amount > ?max)
            }
        """
    ] .

# Submission deadline - references config value
expense:SubmissionDeadlineConstraint a sh:NodeShape ;
    sh:targetClass expense:ExpenseReport ;
    sh:sparql [
        sh:message "Exceeds submission deadline" ;
        sh:select """
            SELECT $this WHERE {
                $this expense:submittedAt ?submit .
                $this expense:hasLineItem/expense:expenseDate ?expense .
                policy:config policy:deadlineDays ?days .  # From config
                FILTER ((?submit - ?expense) > ?days)
            }
        """
    ] .
```

### 7.5 Legacy SHACL Examples

**Category-Specific Rules (from Phase 5):**

```turtle
# Hotel charges must be $100-$1000 per night
expense:LodgingAmountConstraint a sh:NodeShape ;
    sh:targetClass expense:ExpenseLineItem ;
    sh:sparql [
        sh:message "Hotel charges must be between $100-$1000 per night" ;
        sh:prefixes expense: ;
        sh:select """
            SELECT $this
            WHERE {
                $this expense:category expense:Lodging .
                $this expense:amount ?amount .
                FILTER (?amount < 100 || ?amount > 1000)
            }
        """
    ] .

# Meals per diem limit
expense:MealsPerDiemConstraint a sh:NodeShape ;
    sh:targetClass expense:ExpenseLineItem ;
    sh:sparql [
        sh:message "Meals expense exceeds $75/day per diem limit" ;
        sh:prefixes expense: ;
        sh:select """
            SELECT $this
            WHERE {
                $this expense:category expense:Meals .
                $this expense:amount ?amount .
                FILTER (?amount > 75)
            }
        """
    ] .
```

**Temporal Rules:**

```turtle
# Expense year must be current or previous year
expense:ExpenseYearConstraint a sh:NodeShape ;
    sh:targetClass expense:ExpenseLineItem ;
    sh:sparql [
        sh:message "Expense date must be in current or previous year" ;
        sh:prefixes expense: ;
        sh:select """
            SELECT $this
            WHERE {
                $this expense:expenseDate ?date .
                BIND(YEAR(?date) AS ?expenseYear)
                BIND(YEAR(NOW()) AS ?currentYear)
                FILTER (?expenseYear < ?currentYear - 1 || ?expenseYear > ?currentYear)
            }
        """
    ] .

# Submission within 30 days of expense
expense:SubmissionDeadlineConstraint a sh:NodeShape ;
    sh:targetClass expense:ExpenseReport ;
    sh:sparql [
        sh:message "Report must be submitted within 30 days of latest expense" ;
        sh:prefixes expense: ;
        sh:select """
            SELECT $this
            WHERE {
                $this expense:submittedAt ?submitDate .
                $this expense:hasLineItem ?item .
                ?item expense:expenseDate ?expenseDate .
                FILTER (?submitDate - ?expenseDate > 30)
            }
        """
    ] .
```

**Conditional Rules:**

```turtle
# If amount > $500, receipt required
expense:HighAmountReceiptConstraint a sh:NodeShape ;
    sh:targetClass expense:ExpenseLineItem ;
    sh:sparql [
        sh:message "Expenses over $500 require a receipt" ;
        sh:prefixes expense: ;
        sh:select """
            SELECT $this
            WHERE {
                $this expense:amount ?amount .
                FILTER (?amount > 500)
                FILTER NOT EXISTS { $this expense:hasReceipt ?receipt }
            }
        """
    ] .

# If rejected, require comments
expense:RejectionCommentsConstraint a sh:NodeShape ;
    sh:targetClass expense:ApprovalStep ;
    sh:sparql [
        sh:message "Rejected approvals must include rejection reason" ;
        sh:prefixes expense: ;
        sh:select """
            SELECT $this
            WHERE {
                $this expense:stepStatus "rejected" .
                FILTER NOT EXISTS { $this expense:comments ?comments }
            }
        """
    ] .
```

### 7.3 SHACL Review Summary

```markdown
## Validation Rules Summary

| Entity | Required | Format | Range | Category | Temporal | Conditional |
|--------|----------|--------|-------|----------|----------|-------------|
| ExpenseReport | 5 | 1 | 0 | 0 | 1 | 0 |
| ExpenseLineItem | 6 | 1 | 2 | 4 | 1 | 2 |
| Receipt | 4 | 2 | 1 | 0 | 1 | 0 |
| ApprovalStep | 5 | 1 | 1 | 0 | 0 | 1 |
| ExpensePolicy | 3 | 1 | 0 | 0 | 0 | 0 |
| Reimbursement | 5 | 1 | 0 | 0 | 0 | 0 |

**Total Rules:** 52 (28 basic + 24 business rules from Phase 5)

## Business Rules Traceability

| Phase 5 Rule | SHACL Constraint | Status |
|--------------|------------------|--------|
| Hotel $100-$1000 | LodgingAmountConstraint | ✅ |
| Meals $75/day | MealsPerDiemConstraint | ✅ |
| Current/prev year | ExpenseYearConstraint | ✅ |
| 30-day deadline | SubmissionDeadlineConstraint | ✅ |
| Receipt if >$500 | HighAmountReceiptConstraint | ✅ |
| Rejection reason | RejectionCommentsConstraint | ✅ |
```

### 7.4 TEST_DESIGN Approval Gate

```markdown
## ✅ APPROVAL GATE: Phase 7 → 8

**Generated:** `rules.shacl.ttl` (180 lines, 42 validation rules)

**Sample Rules:**
```turtle
expense:ExpenseReportShape a sh:NodeShape ;
    sh:property [
        sh:path expense:title ;
        sh:minCount 1 ;
        sh:minLength 3 ;
        sh:maxLength 200 ;
        sh:message "Title required, 3-200 chars"
    ] .
```

**Approve validation rules?**
- [Y] Yes, proceed to implementation
- [A] Add more rules (specify)
- [R] Revise existing rules (specify)

Human response: ___
```

**WAIT for human response before proceeding.**

---

## Phase 8: IMPLEMENTATION - Type Generation & Registration

**Goal:** Generate typed code and register domain
**Output:** Generated types + updated `registry.yaml`

### 8.1 Implementation Checklist

| Step | Action | Status |
|------|--------|--------|
| 1 | Create domain directory | ⬜ |
| 2 | Write ontology.ttl | ⬜ |
| 3 | Write rules.shacl.ttl | ⬜ |
| 4 | Write version.json | ⬜ |
| 5 | Update registry.yaml | ⬜ |
| 6 | Generate TypeScript types | ⬜ |
| 7 | Generate Python types | ⬜ |
| 8 | Run SHACL validation tests | ⬜ |

### 8.2 Generated Files

```
/hmode/hmode/shared/semantic/domains/expense-report/
├── ontology.ttl              # W3C OWL ontology
├── rules.shacl.ttl           # Validation constraints
├── version.json              # Domain metadata
├── README.md                 # Usage documentation
└── generated/
    ├── typescript/
    │   └── expense-report.types.ts
    └── python/
        └── expense_report.py
```

### 8.3 IMPLEMENTATION Approval Gate

```markdown
## ✅ APPROVAL GATE: Phase 8 → 9

**Implementation Complete:**
- ✅ Domain directory created
- ✅ ontology.ttl (425 lines)
- ✅ rules.shacl.ttl (180 lines)
- ✅ version.json with dependencies
- ✅ registry.yaml updated
- ✅ TypeScript types generated
- ✅ Python types generated
- ✅ SHACL validation tests passing

**Files ready for commit:**
```
hmode/hmode/shared/semantic/domains/expense-report/ontology.ttl
hmode/hmode/shared/semantic/domains/expense-report/rules.shacl.ttl
hmode/hmode/shared/semantic/domains/expense-report/version.json
hmode/hmode/shared/semantic/domains/registry.yaml
```

**Approve implementation?**
- [Y] Yes, commit and proceed to refinement
- [R] Revise (specify changes)
- [T] Run additional tests

Human response: ___
```

**WAIT for human response before proceeding.**

---

## Phase 9: REFINEMENT - Evolution & Versioning

**Goal:** Document evolution path, version domain
**Output:** Updated version.json, CHANGELOG entry

### 9.1 Version Bumping Rules

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fix in SHACL | PATCH | 0.1.0 → 0.1.1 |
| Add optional property | MINOR | 0.1.0 → 0.2.0 |
| Add new entity | MINOR | 0.1.0 → 0.2.0 |
| Change required field | MAJOR | 0.1.0 → 1.0.0 |
| Remove entity | MAJOR | 0.1.0 → 1.0.0 |

### 9.2 Evolution Proposal Template

When evolving existing domain:

```markdown
## Proposed Evolution: expense-report v0.1.0 → v0.2.0

**Reason:** Need to support multi-currency expenses

**Changes:**
| Change | Type | Impact | Backward Compatible? |
|--------|------|--------|---------------------|
| Add `currency` to LineItem | Addition | None | ✅ Yes |
| Add `exchangeRate` property | Addition | None | ✅ Yes |
| Add CurrencyCode enum | Addition | None | ✅ Yes |

**Migration Notes:**
- Existing data defaults to USD
- No breaking changes

**Approve evolution?**
- [Y] Yes, apply changes
- [R] Revise
- [N] Reject
```

---

## HTML Review Document Template

All HTML review documents follow this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Domain Name} - {Phase} Review</title>
    <style>
        /* Professional styling - gradient header, cards, tables */
        body { font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; }
        .container { max-width: 1400px; margin: 0 auto; padding: 40px; }
        header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { background: white; border-radius: 16px; box-shadow: 0 12px 48px rgba(0,0,0,0.15); }
        .comparison-table { width: 100%; border-collapse: collapse; }
        .approval-section { background: #f8f9fa; padding: 32px; border-radius: 12px; }
        /* ... full styling ... */
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{Domain Name} Domain Model</h1>
            <p class="subtitle">Phase {N}: {Phase Name}</p>
            <p class="meta">Generated: {timestamp} | Version: {version}</p>
        </header>

        <!-- Phase-specific content -->
        <main>
            <!-- Options grid (Phase 3) -->
            <!-- Ontology diagram (Phase 6) -->
            <!-- Validation summary (Phase 7) -->
        </main>

        <!-- Comparison matrix -->
        <section class="comparison">
            <h2>Comparison Matrix</h2>
            <table class="comparison-table">...</table>
        </section>

        <!-- AI Recommendation -->
        <section class="recommendation">
            <h2>AI Recommendation</h2>
            <p>{recommendation}</p>
            <p class="rationale">{rationale}</p>
        </section>

        <!-- Approval section -->
        <section class="approval-section">
            <h2>Approval Required</h2>
            <p>Review the above and respond in Claude Code:</p>
            <code>[Y] Approve | [R] Revise | [B] Back</code>
        </section>

        <footer>
            <p>Domain: {domain-name} | Phase: {phase} | Date: {date}</p>
        </footer>
    </div>
</body>
</html>
```

---

## Quick Reference: Approval Gates

| Phase | Gate Name | Human Action | Outputs |
|-------|-----------|--------------|---------|
| 1 → 2 | Seed Approval | Confirm domain need | .project, seed.md |
| 2 → 3 | Research Approval | Confirm research findings | research.md |
| 3 → 4 | Option Selection | Pick entity model option | expansion.md, HTML review |
| 4 → 5 | Analysis Approval | Confirm evaluation | analysis.md |
| 5 → 6 | Selection Lock | Lock final entities | selection.md |
| 6 → 7 | Ontology Approval | Approve ontology.ttl | ontology.ttl, HTML review |
| 7 → 8 | SHACL Approval | Approve validation rules | rules.shacl.ttl |
| 8 → 9 | Implementation Approval | Approve for commit | All files, registry.yaml |

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Skip research phase | Always check existing standards |
| Generate only 1 option | Generate 3-5 options minimum |
| Skip HTML review | Always generate visual review doc |
| Auto-approve phases | Wait for explicit human approval |
| Modify without versioning | Always bump version, document changes |
| Forget created_at/updated_at | Rule #18: ALL models need timestamps |

---

## File Naming Convention

| Phase | File Pattern |
|-------|--------------|
| Phase 1 | `domain-{name}-seed.md` |
| Phase 2 | `domain-{name}-research.md` |
| Phase 3 | `domain-{name}-expansion.md`, `domain-{name}-options-review.html` |
| Phase 4 | `domain-{name}-analysis.md` |
| Phase 5 | `domain-{name}-selection.md` |
| Phase 6 | `ontology.ttl`, `domain-{name}-ontology-review.html` |
| Phase 7 | `rules.shacl.ttl` |
| Phase 8 | `version.json`, generated types |
| Phase 9 | Updated version.json, CHANGELOG |

---

## Slash Command Integration

```bash
# Start new domain model workflow
/new-domain expense-report

# Generate options HTML review
/domain-options expense-report

# Generate ontology review HTML
/domain-ontology-review expense-report

# Evolve existing domain
/evolve-domain expense-report 0.1.0 0.2.0
```

---

## Related Documentation

- `hmode/docs/processes/DOMAIN_MODEL_SOP.md` - Original domain model SOP
- `hmode/docs/processes/SDLC_OVERVIEW.md` - Full SDLC documentation
- `hmode/docs/patterns/PROGRESSIVE_CONTENT.md` - Stage-gated content pattern
- `hmode/docs/core/CONFIRMATION_PROTOCOL.md` - Approval gate patterns
