# Domain Model Approval Workflow
<!-- File UUID: 2f9a7c4e-8d3b-4a1f-9e2d-5c6a9b3f8d7e -->

## Overview

Enforced workflow for domain model discovery, research, and approval before implementation.

**Flow:**
```
Feature Request → Check Registry → [Found: Use It] → Implement
                                 ↓
                            [Not Found]
                                 ↓
                        Research Externally
                                 ↓
                        Propose Domain Model
                                 ↓
                        Human Approval Gate
                                 ↓
                    [Approved] → Implement | [Rejected] → Revise
```

**When to Use:**
- ANY feature requiring data models
- New entities, resources, or concepts
- Before Phase 8 (Implementation)
- When spawning domain-modeling-specialist agent

**Critical Rule:** NEVER implement domain models without registry check + human approval.

---

## 1.0 WORKFLOW STAGES

### Stage 1: Domain Discovery (Registry Check)

**Trigger:** User requests feature that requires data models

**Process:**
1. Identify entities/concepts needed:
   - Example: "user authentication" → User, Session, Token
   - Example: "e-commerce checkout" → Cart, Order, Payment, LineItem

2. Check `hmode/hmode/shared/semantic/domains/registry.yaml`:
   ```yaml
   domains:
     - name: auth
       entities: [User, Session, Token, Credential]
       status: active
       version: 2.1.0
   ```

3. **Decision:**
   - **All entities found** → Stage 5 (Use Existing)
   - **Some entities found** → Stage 2 (Research Missing)
   - **No entities found** → Stage 2 (Research New Domain)

**Example Output:**
```
Checking domain registry for: User, Cart, Order, Payment

Results:
✅ User - Found in 'auth' domain (v2.1.0)
✅ Order - Found in 'ecommerce' domain (v1.3.0)
❌ Cart - NOT FOUND
❌ Payment - NOT FOUND

Next: Research missing entities
```

---

### Stage 2: External Research

**Trigger:** Missing entities detected in Stage 1

**Process:**
1. Spawn `domain-modeling-specialist` agent OR research directly
2. Research sources (in order):
   - **schema.org** - Standard vocabulary
   - **GitHub exemplars** - Popular implementations
   - **Provider APIs** - Stripe, AWS, etc.
   - **Industry standards** - ISO, NIST, etc.

3. Document findings:
   ```markdown
   # Research: Cart & Payment Entities

   ## 1.0 Cart (schema.org/Cart)

   Found in: schema.org
   Properties:
   - cartId: string
   - items: LineItem[]
   - subtotal: Money
   - tax: Money
   - total: Money
   - createdAt: datetime
   - updatedAt: datetime

   GitHub examples:
   - shopify/cart-api (15k stars)
   - stripe/shopping-cart (8k stars)

   ## 2.0 Payment (schema.org/PaymentCard + Stripe API)

   Found in: schema.org, Stripe API
   Properties:
   - paymentId: string
   - method: enum [card, bank, wallet]
   - status: enum [pending, completed, failed]
   - amount: Money
   - currency: string
   - processedAt: datetime
   ```

4. Save research to `docs/domain-research/{domain-name}.md`

**Exit Criteria:**
- ✅ All missing entities researched
- ✅ Properties documented with sources
- ✅ Relationships identified
- ✅ Examples found

---

### Stage 3: Domain Model Proposal

**Trigger:** Research complete

**Process:**
1. Generate domain model YAML:
   ```yaml
   # hmode/hmode/shared/semantic/domains/shopping-cart/schema.yaml
   domain:
     name: shopping-cart
     version: 1.0.0
     status: proposed
     description: Shopping cart and checkout domain

   primitives:
     - name: Money
       type: object
       properties:
         amount:
           type: number
           format: decimal
         currency:
           type: string
           pattern: ^[A-Z]{3}$

   entities:
     - name: Cart
       description: Shopping cart containing items for purchase
       properties:
         cartId:
           type: string
           format: uuid
           primary_key: true
         userId:
           type: string
           format: uuid
           nullable: true  # Guest carts
         items:
           type: array
           items:
             $ref: '#/entities/LineItem'
         subtotal:
           $ref: '#/primitives/Money'
         tax:
           $ref: '#/primitives/Money'
         total:
           $ref: '#/primitives/Money'
         createdAt:
           type: string
           format: date-time
         updatedAt:
           type: string
           format: date-time

     - name: LineItem
       description: Individual item in cart
       properties:
         lineItemId:
           type: string
           format: uuid
           primary_key: true
         productId:
           type: string
           format: uuid
         quantity:
           type: integer
           minimum: 1
         unitPrice:
           $ref: '#/primitives/Money'
         totalPrice:
           $ref: '#/primitives/Money'
   ```

2. Generate examples file:
   ```yaml
   # hmode/hmode/shared/semantic/domains/shopping-cart/examples.yaml
   examples:
     - name: Guest cart with two items
       cart:
         cartId: 550e8400-e29b-41d4-a716-446655440000
         userId: null
         items:
           - lineItemId: 660e8400-e29b-41d4-a716-446655440001
             productId: 770e8400-e29b-41d4-a716-446655440002
             quantity: 2
             unitPrice:
               amount: 29.99
               currency: USD
             totalPrice:
               amount: 59.98
               currency: USD
         subtotal:
           amount: 59.98
           currency: USD
         tax:
           amount: 5.40
           currency: USD
         total:
           amount: 65.38
           currency: USD
         createdAt: '2026-02-02T10:30:00Z'
         updatedAt: '2026-02-02T10:35:00Z'
   ```

3. Generate documentation:
   ```markdown
   # Shopping Cart Domain

   ## Overview
   Domain for shopping cart and checkout functionality.

   ## Entities
   - **Cart**: Container for items being purchased
   - **LineItem**: Individual product in cart

   ## Relationships
   - Cart has many LineItems
   - LineItem belongs to one Cart

   ## External Sources
   - schema.org/Cart
   - Stripe Shopping Cart API
   - Shopify Cart API
   ```

4. Save all files to `hmode/hmode/shared/semantic/domains/shopping-cart/`

**Exit Criteria:**
- ✅ YAML schema generated
- ✅ Examples provided
- ✅ Documentation written
- ✅ Ready for human review

---

### Stage 4: Human Approval Gate

**Trigger:** Domain model proposal complete

**Process:**
1. Present proposal to user:
   ```
   ═══════════════════════════════════════════════════════════
     DOMAIN MODEL APPROVAL: shopping-cart
   ═══════════════════════════════════════════════════════════

   Proposed domain: shopping-cart (v1.0.0)

   Entities:
   - Cart (9 properties)
   - LineItem (5 properties)

   Primitives:
   - Money (reusable across domains)

   Research sources:
   - schema.org/Cart
   - Stripe API
   - Shopify Cart API (15k stars)

   Files to review:
   [1] Open: hmode/hmode/shared/semantic/domains/shopping-cart/schema.yaml
   [2] Open: hmode/hmode/shared/semantic/domains/shopping-cart/examples.yaml
   [3] Open: hmode/hmode/shared/semantic/domains/shopping-cart/README.md
   [4] Open: docs/domain-research/shopping-cart.md (research)

   Decision:
   [1] Approve - Add to registry and implement
   [2] Request changes - Provide feedback and revise
   [3] Reject - Don't create this domain
   [4] Use existing - Map to different domain
   ```

2. Wait for decision

3. **If Approved:**
   - Update `hmode/hmode/shared/semantic/domains/registry.yaml`:
     ```yaml
     domains:
       - name: shopping-cart
         version: 1.0.0
         status: active
         path: hmode/hmode/shared/semantic/domains/shopping-cart
         entities: [Cart, LineItem]
         primitives: [Money]
         created_at: '2026-02-02T10:30:00Z'
         approved_by: user@example.com
     ```
   - Proceed to Stage 5 (Implementation)

4. **If Changes Requested:**
   - Collect feedback
   - Return to Stage 3 with revisions
   - Re-submit to approval gate

5. **If Rejected:**
   - Archive proposal to `docs/domain-research/rejected/`
   - Return to Stage 1 or Stage 2

6. **If Use Existing:**
   - Map to existing domain
   - Proceed to Stage 5

**Exit Criteria:**
- ✅ User decision recorded
- ✅ Registry updated (if approved)
- ✅ Approval tracked in `.project-approvals.yaml`

---

### Stage 5: Implementation

**Trigger:** Domain model approved OR existing domain found

**Process:**
1. Import domain models into project:
   ```python
   # src/models/cart.py
   from shared.semantic.domains.shopping_cart.schema import Cart, LineItem
   ```

2. Generate TypeScript types (if applicable):
   ```bash
   python hmode/shared/tools/generate-types.py shopping-cart --lang typescript
   ```

3. Generate database migrations (if applicable):
   ```bash
   alembic revision -m "Add shopping cart tables"
   ```

4. Implement business logic using approved models

**No Further Approvals Required** - models are pre-approved in Stage 4

---

## 2.0 ENFORCEMENT MECHANISMS

### 2.1 Pre-Implementation Check

**Before ANY code that creates data models:**

```python
from shared.libs.sdlc_gates import check_domain_approval

# Check if domain approved
try:
    check_domain_approval('shopping-cart')
except DomainNotApproved as e:
    print(f"Cannot implement: {e}")
    print("Options:")
    print("[1] Check domain registry")
    print("[2] Research and propose domain")
    print("[3] Use existing domain")
```

**Violation Response:**
```
Cannot implement Cart entity:
- Domain 'shopping-cart' not found in registry
- Status: Not approved

Required workflow:
  1. Check hmode/hmode/shared/semantic/domains/registry.yaml
  2. Research external sources (schema.org, GitHub)
  3. Propose domain model (YAML)
  4. Request human approval
  5. Implement after approval

Run workflow? [Y/n]
```

### 2.2 Domain Approval Tracking

**File:** `.project-approvals.yaml`

```yaml
domain_approvals:
  - domain: shopping-cart
    version: 1.0.0
    status: approved
    proposed_at: '2026-02-02T10:30:00Z'
    approved_at: '2026-02-02T11:15:00Z'
    approved_by: user@example.com
    entities: [Cart, LineItem]
    primitives: [Money]
    research_sources:
      - schema.org/Cart
      - Stripe API
      - Shopify Cart API
    files:
      - hmode/hmode/shared/semantic/domains/shopping-cart/schema.yaml
      - hmode/hmode/shared/semantic/domains/shopping-cart/examples.yaml
    feedback: []

  - domain: payment
    version: 1.0.0
    status: changes_requested
    proposed_at: '2026-02-02T12:00:00Z'
    feedback:
      - "Add support for ACH transfers"
      - "Include refund status enum"
```

### 2.3 Registry Check Function

**Add to sdlc_gates.py:**

```python
def check_domain_exists(domain_name: str) -> bool:
    """
    Check if domain exists in registry.

    Args:
        domain_name: Domain to check

    Returns:
        True if domain exists and is active
    """
    registry_path = Path('hmode/hmode/shared/semantic/domains/registry.yaml')

    if not registry_path.exists():
        raise FileNotFoundError("Domain registry not found")

    with open(registry_path) as f:
        registry = yaml.safe_load(f)

    for domain in registry.get('domains', []):
        if domain['name'] == domain_name and domain['status'] == 'active':
            return True

    return False


def check_domain_approval(domain_name: str) -> bool:
    """
    Check if domain has been approved for use in this project.

    Args:
        domain_name: Domain to check

    Returns:
        True if approved or already in registry

    Raises:
        DomainNotApproved: If domain not found or not approved
    """
    # First check global registry
    if check_domain_exists(domain_name):
        return True

    # Check project-specific approvals
    approval_file = Path('.project-approvals.yaml')

    if not approval_file.exists():
        raise DomainNotApproved(
            f"Domain '{domain_name}' not found in registry and no project approvals exist.\n"
            f"Required: Research → Propose → Approve → Implement"
        )

    with open(approval_file) as f:
        approvals = yaml.safe_load(f)

    for approval in approvals.get('domain_approvals', []):
        if approval['domain'] == domain_name and approval['status'] == 'approved':
            return True

    raise DomainNotApproved(
        f"Domain '{domain_name}' not approved.\n"
        f"Check registry: hmode/hmode/shared/semantic/domains/registry.yaml\n"
        f"Or run domain approval workflow"
    )
```

---

## 3.0 AGENT INTEGRATION

### 3.1 Spawning Domain Modeling Specialist

**When to spawn:**
- User requests feature requiring data models
- Existing domain needs evolution
- Shared primitives need extraction

**How to spawn:**
```python
from claude_code import spawn_agent

agent = spawn_agent(
    agent_type='domain-modeling-specialist',
    task=f"""
    Research and propose domain model for: {entities}

    Steps:
    1. Check registry: hmode/hmode/shared/semantic/domains/registry.yaml
    2. Research external sources (schema.org, GitHub, APIs)
    3. Generate YAML schema with examples
    4. Present for human approval

    Entities needed: {', '.join(entities)}
    Context: {feature_description}
    """
)
```

**Agent responsibilities:**
1. Registry discovery
2. External research
3. YAML generation
4. Example generation
5. Documentation
6. Approval request

### 3.2 Agent Output Format

**Agent MUST produce:**
1. `hmode/hmode/shared/semantic/domains/{domain}/schema.yaml`
2. `hmode/hmode/shared/semantic/domains/{domain}/examples.yaml`
3. `hmode/hmode/shared/semantic/domains/{domain}/README.md`
4. `docs/domain-research/{domain}.md` (research notes)

**Agent MUST request approval:**
```
Domain model proposal complete.

Review files:
[1] schema.yaml
[2] examples.yaml
[3] README.md
[4] Research notes

Approve? [Y/n/changes]
```

---

## 4.0 INTEGRATION WITH SDLC

### 4.1 Phase Entry Points

**Phase 3 (Expansion):**
- Identify entities needed for each solution option
- Check registry for existing domains
- Flag missing domains for research in Phase 5

**Phase 5 (Selection):**
- Before selecting solution, verify domains exist or propose new
- If new domains needed, run approval workflow
- Cannot advance to Phase 6 until domains approved

**Phase 8 (Implementation):**
- Verify domain approved before implementing
- Import from registry
- Generate types/migrations

### 4.2 Modified Phase 5 Flow

**Before:**
```
Select Solution → Tech Stack → Advance to Phase 6
```

**After:**
```
Select Solution → Check Domains → [All exist] → Tech Stack → Phase 6
                                 ↓
                            [Missing]
                                 ↓
                    Research → Propose → Approve
                                 ↓
                            Tech Stack → Phase 6
```

### 4.3 Gate Check Integration

**Add to Gate 4 (Domain Models) in gate matrix:**

```
Task Type: New Feature (requires data models)
          ↓
    Gate 1-3 (Artifact, Golden, Tech)
          ↓
    Gate 4: Domain Models
          ├─ Check registry.yaml
          ├─ [Found] → Continue
          └─ [Not Found] ↓
                Research → Propose → Approve → Continue
```

---

## 5.0 EXAMPLE WALKTHROUGH

### Scenario: E-commerce Cart Feature

**User Request:** "Add shopping cart functionality"

**Stage 1: Discovery**
```
Identifying required entities:
- Cart
- LineItem
- Product (reference)
- User (reference)

Checking domain registry...

Results:
✅ User - Found in 'auth' domain (v2.1.0)
✅ Product - Found in 'catalog' domain (v1.5.0)
❌ Cart - NOT FOUND
❌ LineItem - NOT FOUND

Proceeding to research Cart and LineItem...
```

**Stage 2: Research**
```
Spawning domain-modeling-specialist agent...

Agent researching:
- schema.org/Cart
- Stripe Shopping Cart API
- Shopify Cart implementation
- GitHub exemplars (cart-api, shopping-cart)

Research complete. Generating proposal...
```

**Stage 3: Proposal**
```
Domain model generated: shopping-cart

Files created:
- hmode/hmode/shared/semantic/domains/shopping-cart/schema.yaml
- hmode/hmode/shared/semantic/domains/shopping-cart/examples.yaml
- hmode/hmode/shared/semantic/domains/shopping-cart/README.md
- docs/domain-research/shopping-cart.md

Entities: Cart (9 props), LineItem (5 props)
Primitives: Money (reusable)
```

**Stage 4: Approval Request**
```
═══════════════════════════════════════════════════════════
  DOMAIN MODEL APPROVAL: shopping-cart
═══════════════════════════════════════════════════════════

Proposed: shopping-cart v1.0.0

Entities:
- Cart (shopping cart container)
- LineItem (individual cart item)

Primitives:
- Money (amount + currency)

Research sources:
- schema.org/Cart
- Stripe Shopping Cart API
- Shopify implementation (15k GitHub stars)

Review files: [1] schema.yaml [2] examples.yaml [3] README.md

Approve? [Y/n/changes]
```

**User:** "Yes, but add expiresAt field to Cart"

**Revision:**
```
Changes requested: Add expiresAt field

Updating schema.yaml...
[Cart entity updated with expiresAt: datetime]

Re-submitting for approval...

Approve revised model? [Y/n]
```

**User:** "Yes"

**Stage 5: Implementation**
```
Domain approved ✓

Updating registry...
✅ shopping-cart v1.0.0 added to registry

Generating implementation files...
- src/models/cart.py
- src/models/line_item.py
- migrations/add_cart_tables.sql

Ready to implement cart feature.
```

---

## 6.0 SUMMARY

**Key Points:**

1. **Always Check Registry First:** Before any data modeling
2. **Research Required:** Use external sources (schema.org, GitHub, APIs)
3. **Human Approval Gate:** Cannot implement without approval
4. **Agent-Driven:** Use domain-modeling-specialist for discovery
5. **Tracked:** .project-approvals.yaml maintains approval state

**Benefits:**

- Prevents duplicate/inconsistent models
- Leverages industry standards
- Creates reusable domains across projects
- Ensures human oversight on data architecture
- Builds shared vocabulary over time

**Enforcement:**

```python
# Before ANY domain model implementation
check_domain_approval('domain-name')

# Raises DomainNotApproved if not found/approved
```

**Related Files:**
- `hmode/hmode/shared/semantic/domains/registry.yaml` - Global domain registry
- `@processes/DOMAIN_MODEL_SOP` - Domain model standards
- `hmode/shared/libs/sdlc_gates.py` - Gate checking utilities
- `.project-approvals.yaml` - Per-project approval tracking
