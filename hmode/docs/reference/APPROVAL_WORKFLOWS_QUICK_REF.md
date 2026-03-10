# Approval Workflows Quick Reference
<!-- File UUID: 9a4f7c2e-5d8b-4e3a-9f1d-6c8a9b4f3d2e -->

## Overview

Two enforced approval workflows with human gates to prevent premature implementation.

| Workflow | When | Stages | File |
|----------|------|--------|------|
| **Design Approval** | Phase 6 (Design) for production projects | Sitemap → Lo-Fi → Hi-Fi | `@processes/DESIGN_APPROVAL_WORKFLOW` |
| **Domain Model Approval** | ANY feature requiring data models | Discovery → Research → Proposal → Approval | `@processes/DOMAIN_MODEL_APPROVAL_WORKFLOW` |

---

## 1.0 DESIGN APPROVAL WORKFLOW

### Flow Diagram

```
Sitemap (IA Agent) → Gate 1 → Lo-Fi Mocks (UX Agent) → Gate 2 → Hi-Fi Mocks (UX Agent) → Final Sign-Off
```

### When to Use

**Automatic:**
- Production projects (`project_type: production` in `.project`)

**Manual:**
- User requests "formal design approval"
- Stakeholder/client involvement mentioned

### Stage Breakdown

| Stage | Agent | Output | Gate | Exit |
|-------|-------|--------|------|------|
| **1. IA** | information-architecture-agent | Navigation, user flows, sitemap | Gate 1 | Approved |
| **2. Lo-Fi** | ux-component-agent (grayscale) | Wireframes, layout structure | Gate 2 | Approved |
| **3. Hi-Fi** | ux-component-agent (full color) | Final mockups, design system | Final | Approved |

### Enforcement

**Before Lo-Fi:**
```python
from shared.libs.sdlc_gates import check_design_gate

check_design_gate('gate_1_ia')  # Raises DesignGateNotApproved if pending
```

**Before Hi-Fi:**
```python
check_design_gate('gate_2_lofi')
```

**Before Phase 7:**
```python
check_design_gate('final_signoff')
```

### Enable Workflow

**Manual:**
```python
from shared.libs.sdlc_gates import initialize_approval_workflow

initialize_approval_workflow()
# Creates .project-approvals.yaml
```

**Automatic:**
- Detects `project_type: production` in `.project`
- Asks user: "Enable formal design approval workflow? [Y/n]"

### Approval Flow

1. Agent generates artifacts (IA/Lo-Fi/Hi-Fi)
2. Claude presents approval request:
   ```
   ═══════════════════════════════════════════════════════════
     APPROVAL GATE N: Stage Name
   ═══════════════════════════════════════════════════════════

   Review artifacts:
   [1] Open: file1.html
   [2] Open: file2.md

   Decision: [approve/changes/reject]
   ```
3. User decides
4. Status updated in `.project-approvals.yaml`
5. Next stage unlocked (or return to previous stage)

---

## 2.0 DOMAIN MODEL APPROVAL WORKFLOW

### Flow Diagram

```
Feature Request → Check Registry → [Found: Use It] → Implement
                                  ↓
                             [Not Found]
                                  ↓
                         Research (schema.org, GitHub)
                                  ↓
                         Propose YAML Schema
                                  ↓
                         Human Approval Gate
                                  ↓
                    [Approved] → Update Registry → Implement
                    [Rejected] → Revise or Abandon
```

### When to Use

**Always:**
- ANY feature requiring data models
- New entities, resources, or domain objects
- Before Phase 8 (Implementation)

### Stage Breakdown

| Stage | Action | Output | Gate | Exit |
|-------|--------|--------|------|------|
| **1. Discovery** | Check `hmode/hmode/shared/semantic/domains/registry.yaml` | List of found/missing entities | - | All checked |
| **2. Research** | External research (schema.org, GitHub, APIs) | Research notes with sources | - | Research complete |
| **3. Proposal** | Generate YAML schema + examples | Domain model files | Approval | Approved |
| **4. Implementation** | Import and use approved models | Code using models | - | Feature complete |

### Enforcement

**Before ANY domain model implementation:**
```python
from shared.libs.sdlc_gates import check_domain_approval

check_domain_approval('domain-name')  # Raises DomainNotApproved if not in registry
```

### Registry Check

**Manual:**
```python
from shared.libs.sdlc_gates import check_domain_exists

if check_domain_exists('shopping-cart'):
    print("Domain exists - use it")
else:
    print("Domain missing - research and propose")
```

**Automatic:**
- Claude checks registry when feature requires data models
- Reports found/missing entities
- Proceeds to research if missing

### Research Sources (Priority Order)

1. **schema.org** - Standard vocabulary (use first)
2. **GitHub exemplars** - Popular implementations (check stars)
3. **Provider APIs** - Stripe, AWS, etc. (if applicable)
4. **Industry standards** - ISO, NIST (if applicable)

### Proposal Format

**Files to generate:**
```
hmode/hmode/shared/semantic/domains/{domain}/
├── schema.yaml          # Entity/primitive definitions
├── examples.yaml        # Example instances
└── README.md            # Documentation

docs/domain-research/
└── {domain}.md          # Research notes with sources
```

**Schema structure:**
```yaml
domain:
  name: shopping-cart
  version: 1.0.0
  status: proposed

primitives:
  - name: Money
    type: object
    properties:
      amount:
        type: number
      currency:
        type: string

entities:
  - name: Cart
    properties:
      cartId:
        type: string
        format: uuid
      items:
        type: array
        items:
          $ref: '#/entities/LineItem'
      createdAt:
        type: string
        format: date-time
      updatedAt:
        type: string
        format: date-time
```

### Approval Flow

1. Agent researches and generates domain model proposal
2. Claude presents approval request:
   ```
   ═══════════════════════════════════════════════════════════
     DOMAIN MODEL APPROVAL: domain-name
   ═══════════════════════════════════════════════════════════

   Proposed: domain-name v1.0.0

   Entities: Entity1, Entity2
   Primitives: Primitive1

   Research sources:
   - schema.org/Entity
   - GitHub repo (15k stars)

   Review files:
   [1] schema.yaml
   [2] examples.yaml
   [3] README.md

   Approve? [Y/n/changes]
   ```
3. User decides
4. If approved:
   - Add to `hmode/hmode/shared/semantic/domains/registry.yaml`
   - Update `.project-approvals.yaml`
   - Allow implementation
5. If changes requested:
   - Revise schema
   - Re-submit for approval

---

## 3.0 COMBINED WORKFLOW EXAMPLE

### Scenario: E-commerce Checkout Feature (Production)

**Phase 5 → Phase 6 Transition:**

1. **Domain Check** (Domain Approval Workflow)
   ```
   Feature: Shopping cart with checkout

   Entities needed: Cart, LineItem, Payment, Order

   Checking registry...
   ✅ Order - Found in 'ecommerce' domain
   ✅ Payment - Found in 'payment' domain
   ❌ Cart - NOT FOUND
   ❌ LineItem - NOT FOUND

   Proceeding to domain approval workflow...
   ```

2. **Domain Research**
   ```
   Researching Cart and LineItem...
   - schema.org/Cart
   - Shopify Cart API
   - Stripe Shopping Cart

   Domain model proposed: shopping-cart v1.0.0
   Approve? [Y/n]
   ```

3. **Domain Approved**
   ```
   ✅ shopping-cart v1.0.0 approved
   ✅ Added to registry

   Advancing to Phase 6 (Design)...
   ```

4. **Design Workflow Enabled** (Design Approval Workflow)
   ```
   Detected: project_type = production
   Enabling formal design approval workflow.

   Stages:
   1. Information Architecture → Gate 1
   2. Lo-Fi Wireframes → Gate 2
   3. Hi-Fi Mockups → Final Sign-Off

   Continue? [Y/n]
   ```

5. **Stage 1: IA**
   ```
   Spawning information-architecture-agent...

   Output: docs/design/01-information-architecture.md
   - Cart page
   - Checkout flow
   - Order confirmation

   Gate 1: Approve? [Y/n]
   ```

6. **Stage 2: Lo-Fi**
   ```
   Gate 1 approved ✓

   Spawning ux-component-agent (lo-fi mode)...

   Output: docs/design/02-lofi-wireframes/*.html
   - Grayscale wireframes
   - Layout structure

   Gate 2: Approve? [Y/n]
   ```

7. **Stage 3: Hi-Fi**
   ```
   Gate 2 approved ✓

   Spawning ux-component-agent (hi-fi mode)...

   Output: docs/design/03-hifi-mockups/*.html
   - Full color mockups
   - Design system applied

   Final sign-off: Approve? [Y/n]
   ```

8. **Phase 7 (Test)**
   ```
   Final sign-off approved ✓

   Phase 6 complete.
   Advancing to Phase 7 (Test)...
   ```

---

## 4.0 TRACKING & STATUS

### Approval File Structure

**.project-approvals.yaml**
```yaml
design_workflow:
  enabled: true
  gates:
    - gate_id: gate_1_ia
      stage: information_architecture
      status: approved
      approved_by: user@example.com
      approved_at: '2026-02-02T10:30:00Z'
      artifacts:
        - docs/design/01-information-architecture.md
      feedback: []

    - gate_id: gate_2_lofi
      stage: lofi_wireframes
      status: pending
      approved_by: null
      approved_at: null
      artifacts: []
      feedback: []

domain_approvals:
  - domain: shopping-cart
    version: 1.0.0
    status: approved
    proposed_at: '2026-02-02T09:00:00Z'
    approved_at: '2026-02-02T09:15:00Z'
    approved_by: user@example.com
    entities: [Cart, LineItem]
    primitives: [Money]
    research_sources:
      - schema.org/Cart
      - Shopify Cart API
    feedback: []
```

### View Status

**Python:**
```python
from shared.libs.sdlc_gates import format_approval_status

print(format_approval_status())
```

**Output:**
```
═══════════════════════════════════════════════════════════
  DESIGN APPROVAL STATUS
═══════════════════════════════════════════════════════════

✅ Information Architecture
   Status: APPROVED
   Approved by: user@example.com
   Approved at: 2026-02-02T10:30:00Z

⏳ Lofi Wireframes
   Status: PENDING

⏳ Hifi Mockups
   Status: PENDING
```

---

## 5.0 GATE FUNCTIONS REFERENCE

### Design Gates

```python
from shared.libs.sdlc_gates import (
    check_design_gate,           # Check if gate passed
    initialize_approval_workflow, # Create .project-approvals.yaml
    update_gate_status,          # Update gate status
    get_approval_status,         # Get all status
    format_approval_status       # Human-readable status
)

# Check before proceeding
check_design_gate('gate_1_ia')      # IA approved?
check_design_gate('gate_2_lofi')    # Lo-Fi approved?
check_design_gate('final_signoff')  # Hi-Fi approved?

# Initialize workflow
initialize_approval_workflow()

# Update status
update_gate_status(
    gate_id='gate_1_ia',
    status='approved',
    approved_by='user@example.com'
)

# View status
status = get_approval_status()
print(format_approval_status())
```

### Domain Gates

```python
from shared.libs.sdlc_gates import (
    check_domain_exists,      # Check registry
    check_domain_approval,    # Check if approved
    update_domain_approval    # Update approval
)

# Check registry
if check_domain_exists('shopping-cart'):
    print("Domain exists")

# Check approval (raises DomainNotApproved if missing)
check_domain_approval('shopping-cart')

# Update approval
update_domain_approval(
    domain_name='shopping-cart',
    status='approved',
    version='1.0.0',
    entities=['Cart', 'LineItem'],
    research_sources=['schema.org/Cart']
)
```

---

## 6.0 EXCEPTION HANDLING

### Design Gate Violations

```python
from shared.libs.sdlc_gates import check_design_gate, DesignGateNotApproved

try:
    check_design_gate('gate_2_lofi')
except DesignGateNotApproved as e:
    print(f"Cannot proceed: {e}")
    # Present options to user:
    # [1] Request approval
    # [2] Revise based on feedback
    # [3] View status
```

### Domain Gate Violations

```python
from shared.libs.sdlc_gates import check_domain_approval, DomainNotApproved

try:
    check_domain_approval('shopping-cart')
except DomainNotApproved as e:
    print(f"Cannot implement: {e}")
    # Run domain approval workflow:
    # 1. Check registry
    # 2. Research
    # 3. Propose
    # 4. Request approval
```

---

## 7.0 INTEGRATION POINTS

### SDLC Phase Integration

| Phase | Design Workflow | Domain Workflow |
|-------|----------------|-----------------|
| **Phase 3** | - | Identify entities needed |
| **Phase 5** | - | Research & approve domains |
| **Phase 6** | Enable & run workflow | - |
| **Phase 7** | Check final sign-off | - |
| **Phase 8** | - | Verify domain approval |

### Agent Integration

**Information Architecture Agent:**
- Spawned in Design Workflow Stage 1
- Generates sitemap, user flows, navigation
- Output to `docs/design/01-information-architecture.md`

**UX Component Agent:**
- Spawned in Design Workflow Stages 3 & 5
- Stage 3: Lo-fi wireframes (grayscale)
- Stage 5: Hi-fi mockups (full color)

**Domain Modeling Specialist Agent:**
- Spawned when missing domain entities detected
- Researches external sources
- Generates YAML schema + examples
- Requests human approval

---

## 8.0 RELATED FILES

| File | Purpose |
|------|---------|
| `@processes/DESIGN_APPROVAL_WORKFLOW` | Full design approval docs |
| `@processes/DOMAIN_MODEL_APPROVAL_WORKFLOW` | Full domain approval docs |
| `hmode/shared/libs/sdlc_gates.py` | Gate checking utilities |
| `.project-approvals.yaml` | Per-project approval state |
| `hmode/hmode/shared/semantic/domains/registry.yaml` | Global domain registry |

---

## 9.0 SUMMARY

**Design Approval Workflow:**
- **Purpose:** Prevent premature visual implementation
- **Stages:** Sitemap → Lo-Fi → Hi-Fi
- **When:** Production projects in Phase 6
- **Enforcement:** Gates block next stage until approved

**Domain Model Approval Workflow:**
- **Purpose:** Prevent duplicate/inconsistent data models
- **Stages:** Discovery → Research → Proposal → Approval
- **When:** ANY feature requiring data models
- **Enforcement:** Cannot implement without registry approval

**Key Benefits:**
- Catches issues early (structure before visuals, research before models)
- Ensures stakeholder buy-in before implementation
- Reduces rework in later phases
- Creates audit trail of decisions
- Builds reusable assets (domain models, design patterns)
