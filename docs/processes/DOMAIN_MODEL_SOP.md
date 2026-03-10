# Domain Model SOP

Standard operating procedure for using, creating, and evolving semantic domain models.

## Overview

Domain models are reusable semantic definitions that ensure consistency across prototypes. When building a prototype:
1. **Identify** which existing domains apply
2. **Generate** models in `shared/domain-models/` directory
3. **Present** models in YAML format for human approval
4. **Create** new domains as needed (with approval gates)
5. **Compose** domains into your prototype

---

## 0. Data Model Approval Workflow (CRITICAL - Rule #19)

**ALL data models MUST follow this workflow before implementation:**

### 0.1 Generate in Shared Location

```bash
# All data models go here first
shared/domain-models/
├── {prototype-name}/
│   ├── models.yaml          # Primary model definitions
│   ├── enums.yaml           # Enum/constant definitions
│   └── relationships.yaml   # Entity relationships
```

### 0.2 YAML Format for Approval

**AI MUST present data models in this YAML format:**

```yaml
# models.yaml - {Prototype Name} Data Models
# Generated: {date}
# Status: PENDING APPROVAL

entities:
  User:
    description: "Application user account"
    properties:
      id:
        type: uuid
        required: true
        description: "Unique identifier"
      email:
        type: string
        required: true
        format: email
        description: "User email address"
      name:
        type: string
        required: true
        max_length: 255
      created_at:
        type: datetime
        required: true
        auto: true
      updated_at:
        type: datetime
        required: true
        auto: true
    indexes:
      - [email]  # Unique index

  Order:
    description: "Customer purchase order"
    properties:
      id:
        type: uuid
        required: true
      user_id:
        type: uuid
        required: true
        references: User.id
      status:
        type: enum
        enum_ref: OrderStatus
        required: true
        default: pending
      total_amount:
        type: decimal
        precision: 10
        scale: 2
      created_at:
        type: datetime
        required: true
        auto: true
      updated_at:
        type: datetime
        required: true
        auto: true

enums:
  OrderStatus:
    values:
      - pending
      - confirmed
      - shipped
      - delivered
      - cancelled
    description: "Order lifecycle states"

relationships:
  - type: one_to_many
    from: User
    to: Order
    foreign_key: user_id
```

### 0.3 Approval Gate (REQUIRED)

**After generating YAML, AI MUST present:**

```markdown
## Data Models: {Prototype Name}

I've generated the data models in `shared/domain-models/{prototype-name}/models.yaml`.

### Entities Summary

| Entity | Properties | Key Relationships |
|--------|------------|-------------------|
| User | id, email, name, created_at, updated_at | has_many Orders |
| Order | id, user_id, status, total_amount, created_at, updated_at | belongs_to User |

### Enums

| Enum | Values |
|------|--------|
| OrderStatus | pending, confirmed, shipped, delivered, cancelled |

---

**Review the full YAML above.**

**Approve these data models?**
- [Y] Yes, proceed to implementation
- [R] Revise (specify changes needed)
- [A] Add entities (tell me what's missing)
- [D] Delete entities (tell me what to remove)
```

**WAIT for human response before implementing ANY code that uses these models.**

### 0.4 Post-Approval Workflow

After human approves:
1. Models remain in `shared/domain-models/` as source of truth
2. Generate implementation code (SQLAlchemy, TypeScript types, etc.)
3. Reference YAML file in prototype's `.project` metadata

### 0.5 Revision Workflow

If human requests changes:
1. Update YAML in `shared/domain-models/`
2. Re-present updated models for approval
3. Repeat until approved

---

## 1. Domain Discovery Workflow

**When starting any prototype, AI MUST:**

```
1. Read registry: cat /hmode/hmode/shared/semantic/domains/registry.yaml
2. Identify applicable domains based on prototype requirements
3. Present domain menu to human for selection
```

### Domain Selection Menu Format

```markdown
## Applicable Domain Models

Based on your [prototype-name] requirements, these domains are relevant:

| # | Domain | Version | Fit | Entities You'd Use |
|---|--------|---------|-----|-------------------|
| 1 | email | 1.0.0 | High | Email, Attachment |
| 2 | auth | 0.1.0 | High | User, Session, Permission |
| 3 | action | 1.0.0 | Medium | CreateAction, UpdateAction |

**Select:** Enter numbers (e.g., "1,2") or "none" to skip existing domains

**New domains needed?** I'll propose these after your selection:
- [ ] ecommerce (Product, Cart, Order, Payment)
- [ ] inventory (Stock, Warehouse, SKU)
```

**WAIT for human response before proceeding.**

---

## 2. Using Existing Domain Models

### 2.1 Import Pattern

After human approves domain selection:

```typescript
// In your prototype
import { Email, EmailStatus } from '@protoflow/semantic/domains/email';
import { User, Session } from '@protoflow/semantic/domains/auth';
```

### 2.2 Composition Pattern

When prototype needs entities from multiple domains:

```typescript
// ecommerce/types.ts - compose from existing domains
import { User } from '@protoflow/semantic/domains/auth';
import { Email } from '@protoflow/semantic/domains/email';

interface Order {
  customer: User;           // Reuse auth domain
  confirmationEmail: Email; // Reuse email domain
  // ... ecommerce-specific fields
}
```

### 2.3 Extension Pattern

When you need to extend an existing entity:

```typescript
// Extend, don't modify the source domain
interface EcommerceUser extends User {
  shippingAddresses: Address[];
  paymentMethods: PaymentMethod[];
  orderHistory: Order[];
}
```

---

## 3. Creating New Domain Models

### 3.1 External Research Phase (REQUIRED)

**Before proposing any new domain, AI MUST research external sources:**

**Step 1: Schema.org**
```
WebSearch: "schema.org [domain] types"
Example: "schema.org ecommerce types" → Product, Offer, Order
```
- Document standard properties and relationships
- Note which schema.org types map to your entities

**Step 2: Top GitHub Projects**
```
WebSearch: "[domain] open source github stars:>10000"
Example: "ecommerce open source github" → Magento, Medusa, Saleor
```

| Domain | Reference Projects (10k+ stars) |
|--------|--------------------------------|
| E-commerce | Magento, Medusa, Saleor, Shopify themes |
| CRM | SuiteCRM, EspoCRM, Monica |
| Healthcare | OpenMRS, HAPI FHIR |
| Finance | Firefly III, Akaunting |
| Project Mgmt | Taiga, Plane, Focalboard |

**Step 3: Industry Provider APIs**
```
WebSearch: "[provider] API reference [domain]"
Example: "Stripe API reference payments" → PaymentIntent, Charge, Refund
```

| Domain | Reference APIs |
|--------|---------------|
| Payments | Stripe, Square, PayPal |
| Communications | Twilio, SendGrid, Mailgun |
| E-commerce | Shopify Admin API, BigCommerce |
| Auth | Auth0, Okta, Firebase Auth |
| CRM | Salesforce, HubSpot |
| Shipping | ShipStation, EasyPost |

**Research Output Format:**
```markdown
## Domain Model Research: [Domain Name]

### Schema.org Findings
- [Entity]: [key properties from schema.org]

### GitHub Project Analysis
- [Project] ([stars]): [key patterns/entities discovered]

### Provider API Analysis
- [Provider]: [entity lifecycle/relationships discovered]

### Synthesized Insights
- [Key design decisions informed by research]
```

**Present research summary to human before proceeding to proposal.**

---

### 3.2 Proposal Gate (REQUIRED)

**After research, AI MUST present proposal with sources:**

```markdown
## Proposed Domain: ecommerce

**Purpose:** E-commerce primitives for online retail prototypes

**Research Sources:**
- Schema.org: Product, Offer, Order types
- GitHub: Magento (product variants), Medusa (region pricing)
- APIs: Stripe (payment lifecycle), Shopify (inventory model)

**Entities:**
| Entity | Description | Key Properties | Informed By |
|--------|-------------|----------------|-------------|
| Product | Sellable item | sku, name, price, inventory | schema.org + Magento |
| Variant | Product option | size, color, sku | Saleor + Shopify |
| Cart | Shopping cart | items[], subtotal, userId | Medusa |
| Order | Completed purchase | orderNumber, status, total | schema.org + Stripe |
| Payment | Payment transaction | method, amount, status | Stripe API |
| Address | Shipping/billing | street, city, country, zip | schema.org |

**Actions:**
- AddToCartAction
- CheckoutAction
- ProcessPaymentAction (informed by Stripe PaymentIntent flow)
- FulfillOrderAction

**Enums:**
- OrderStatus: pending, paid, shipped, delivered, cancelled
- PaymentMethod: card, paypal, applepay, crypto
- PaymentStatus: pending, authorized, captured, failed, refunded (from Stripe)

**Relationships:**
- Order → User (from auth domain)
- Order → Email (confirmation from email domain)

---

**Approve this domain?**
- [Y] Yes, create it
- [R] Revise (tell me what to change)
- [S] Skip (don't need this domain)
```

**WAIT for human response.**

### 3.3 Creation Steps (After Approval)

```bash
# 1. Create from template
cp -r /hmode/hmode/shared/semantic/domains/_template /hmode/hmode/shared/semantic/domains/ecommerce

# 2. Generate ontology.ttl (present to human for review)
# 3. Generate rules.shacl.ttl (present to human for review)
# 4. Update version.json
# 5. Register in registry.yaml
# 6. Generate TypeScript/Python types
```

### 3.4 Ontology Review Gate

**After generating ontology.ttl, present key sections:**

```markdown
## Review: ecommerce/ontology.ttl

### Entities (showing Product as example)

```turtle
ecom:Product a owl:Class ;
    rdfs:label "Product" ;
    rdfs:comment "Sellable item in catalog" .

ecom:sku a owl:DatatypeProperty ;
    rdfs:domain ecom:Product ;
    rdfs:range xsd:string ;
    rdfs:comment "Stock Keeping Unit - unique product identifier" .

ecom:price a owl:DatatypeProperty ;
    rdfs:domain ecom:Product ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Current selling price" .
```

### Actions (showing CheckoutAction)

```turtle
ecom:CheckoutAction a action:CreateAction ;
    rdfs:label "Checkout" ;
    action:operatesOn ecom:Order ;
    action:requiresPermission "ecom:checkout" ;
    action:hasSideEffect "Creates order, reserves inventory, initiates payment" .
```

---

**Approve ontology?**
- [Y] Yes, continue to validation rules
- [R] Revise (specify changes)
```

### 3.5 Validation Rules Review Gate

```markdown
## Review: ecommerce/rules.shacl.ttl

```turtle
ecom:ProductShape a sh:NodeShape ;
    sh:targetClass ecom:Product ;
    sh:property [
        sh:path ecom:sku ;
        sh:minCount 1 ;
        sh:pattern "^[A-Z0-9-]+$" ;
        sh:message "SKU required, uppercase alphanumeric with dashes"
    ] ;
    sh:property [
        sh:path ecom:price ;
        sh:minCount 1 ;
        sh:minInclusive 0 ;
        sh:message "Price required and must be non-negative"
    ] .
```

**Approve validation rules?**
- [Y] Yes, generate types
- [R] Revise
```

---

## 4. Evolving Existing Domains

### 4.1 When to Evolve vs. Extend

| Scenario | Action |
|----------|--------|
| Add optional field to existing entity | Evolve (minor version) |
| Add new entity to domain | Evolve (minor version) |
| Change required field | Evolve (major version) + approval |
| Add prototype-specific field | Extend in prototype (don't modify source) |
| Need completely different structure | Create new domain |

### 4.2 Evolution Proposal Gate

```markdown
## Proposed Evolution: auth domain v0.1.0 → v0.2.0

**Reason:** E-commerce prototype needs customer-specific auth features

**Changes:**
| Change | Type | Impact |
|--------|------|--------|
| Add `CustomerProfile` entity | Addition | None - new entity |
| Add `loyaltyTier` to User | Addition | None - optional field |
| Add `GuestCheckoutSession` | Addition | None - new entity |

**Backward compatible:** Yes

**Approve evolution?**
- [Y] Yes, update auth domain
- [N] No, extend in prototype instead
- [R] Revise changes
```

---

## 5. Complete Prototype Workflow Example

### E-commerce Prototype Flow

```
Human: "Build an e-commerce prototype"

AI: [Reads registry.yaml]

AI: "Here are applicable domains..."
    [Presents Domain Selection Menu]

Human: "Use 1,2 (email, auth)"

AI: "I'll need to create an ecommerce domain. Here's my proposal..."
    [Presents Proposed Domain: ecommerce]

Human: "Y" or "R - add Wishlist entity"

AI: [Creates/revises domain]
    [Presents Ontology Review]

Human: "Y"

AI: [Presents Validation Rules Review]

H: "Y"

AI: [Generates types, registers domain]
    "Domain created. Starting prototype implementation..."
```

---

## 6. Shared Primitives (Core Domain)

### 6.1 Reusable Primitives

Common patterns that should be shared across domains, NOT duplicated:

| Primitive | Description | Used By |
|-----------|-------------|---------|
| **Time** | TimePoint, Duration, DateRange, Timezone | story, sdlc, health, ecommerce |
| **Money** | Amount, Currency, ExchangeRate | ecommerce, billing |
| **Address** | Street, City, Country, PostalCode | ecommerce, auth, shipping |
| **Measurement** | Quantity, Unit, Dimension | health, inventory, shipping |
| **Contact** | Phone, Email, SocialHandle | auth, ecommerce, crm |
| **Media** | Image, Video, Document, URL | email, story, ecommerce |
| **Audit** | CreatedAt, UpdatedAt, CreatedBy, Version | ALL domains |

### 6.2 Core Domain Structure

```
/hmode/hmode/shared/semantic/domains/core/
├── ontology.ttl
│   ├── Time primitives (TimePoint, Duration, DateRange, Recurrence)
│   ├── Money primitives (Amount, Currency)
│   ├── Address primitives (Address, GeoLocation)
│   ├── Measurement primitives (Quantity, Unit)
│   ├── Media primitives (MediaObject, Image, Document)
│   └── Audit primitives (AuditInfo, VersionInfo)
├── rules.shacl.ttl
└── version.json
```

### 6.3 Using Core Primitives

**In domain ontology files:**

```turtle
@prefix core: <http://protoflow.ai/ontology/core#> .
@prefix ecom: <http://protoflow.ai/ontology/ecommerce#> .

ecom:Product a owl:Class ;
    rdfs:label "Product" .

ecom:price a owl:ObjectProperty ;
    rdfs:domain ecom:Product ;
    rdfs:range core:Money ;        # Reuse core Money
    rdfs:comment "Product price" .

ecom:createdAt a owl:ObjectProperty ;
    rdfs:domain ecom:Product ;
    rdfs:range core:TimePoint ;    # Reuse core TimePoint
    rdfs:comment "When product was added" .
```

**In TypeScript:**

```typescript
import { TimePoint, Duration, DateRange } from '@protoflow/semantic/domains/core';
import { Money, Currency } from '@protoflow/semantic/domains/core';

interface Product {
  price: Money;           // { amount: 29.99, currency: 'USD' }
  createdAt: TimePoint;   // { timestamp: Date, timezone: 'UTC' }
  saleWindow?: DateRange; // { start: TimePoint, end: TimePoint }
}
```

### 6.4 Time Model Primitives (from story domain)

These should be extracted to core:

```turtle
# core/ontology.ttl - Time primitives

core:TimePoint a owl:Class ;
    rdfs:label "Time Point" ;
    rdfs:comment "Specific moment in time with optional timezone" .

core:timestamp a owl:DatatypeProperty ;
    rdfs:domain core:TimePoint ;
    rdfs:range xsd:dateTime .

core:timezone a owl:DatatypeProperty ;
    rdfs:domain core:TimePoint ;
    rdfs:range xsd:string .

core:Duration a owl:Class ;
    rdfs:label "Duration" ;
    rdfs:comment "Length of time (ISO 8601 duration)" .

core:DateRange a owl:Class ;
    rdfs:label "Date Range" ;
    rdfs:comment "Time period with start and end" .

core:startTime a owl:ObjectProperty ;
    rdfs:domain core:DateRange ;
    rdfs:range core:TimePoint .

core:endTime a owl:ObjectProperty ;
    rdfs:domain core:DateRange ;
    rdfs:range core:TimePoint .

core:Recurrence a owl:Class ;
    rdfs:label "Recurrence" ;
    rdfs:comment "Repeating time pattern (daily, weekly, etc.)" .

core:TimeOfDay a owl:Class ;
    rdfs:label "Time of Day" ;
    owl:oneOf (core:Morning core:Afternoon core:Evening core:Night) .

core:Season a owl:Class ;
    rdfs:label "Season" ;
    owl:oneOf (core:Spring core:Summer core:Fall core:Winter) .

core:LifeStage a owl:Class ;
    rdfs:label "Life Stage" ;
    rdfs:comment "Stage in lifecycle (infant, child, adult, etc.)" .
```

### 6.5 Primitive Extraction Workflow

When AI identifies duplicated primitives:

```markdown
## Primitive Extraction Proposal

I noticed `TimePoint` is defined in both `story` and your new `ecommerce` domain.

**Recommend:** Extract to `core` domain for reuse.

| Primitive | Currently In | Propose Move To |
|-----------|--------------|-----------------|
| TimePoint | story | core |
| Duration | story | core |
| LifeStage | story | core |
| Address | (new) | core |
| Money | (new) | core |

**Benefits:**
- Single source of truth
- Consistent validation across domains
- Easier maintenance

**Approve extraction?**
- [Y] Yes, extract to core
- [N] No, keep domain-specific
- [P] Partial (specify which)
```

---

## 7. Domain Dependency Graph

### 7.1 Tracking Dependencies

In `registry.yaml`:

```yaml
domains:
  core:
    status: production
    version: "1.0.0"
    description: Shared primitives (time, money, address, etc.)
    dependencies: []  # No dependencies - foundation layer

  auth:
    status: production
    version: "1.0.0"
    dependencies: [core]  # Uses TimePoint, Address

  email:
    status: production
    version: "1.0.0"
    dependencies: [core]  # Uses TimePoint, MediaObject

  ecommerce:
    status: development
    version: "0.1.0"
    dependencies: [core, auth, email]  # Composes multiple domains
```

### 7.2 Dependency Visualization

```
                    ┌──────────┐
                    │   core   │  (primitives)
                    └────┬─────┘
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
      ┌────────┐    ┌────────┐    ┌────────┐
      │  auth  │    │ email  │    │ story  │
      └────┬───┘    └────┬───┘    └────────┘
           │             │
           └──────┬──────┘
                  ▼
            ┌───────────┐
            │ ecommerce │  (composes auth + email + core)
            └───────────┘
```

---

## 8. Quick Reference

### Commands

```bash
# List all domains
cat /hmode/hmode/shared/semantic/domains/registry.yaml

# Create new domain from template
cp -r /hmode/hmode/shared/semantic/domains/_template /hmode/hmode/shared/semantic/domains/NAME

# Generate types
cd /hmode/shared/semantic/tools/generator
npm run generate -- --domain NAME --lang typescript,python

# View domain details
cat /hmode/hmode/shared/semantic/domains/NAME/version.json
```

### Approval Gates Checklist

| Gate | When | Human Action |
|------|------|--------------|
| Domain Selection | Start of prototype | Select which existing domains to use |
| External Research | Before proposing new domain | Review research from schema.org, GitHub, APIs |
| New Domain Proposal | After research complete | Approve/revise entity list (with sources) |
| Ontology Review | After ontology generated | Approve/revise properties |
| Validation Review | After SHACL generated | Approve/revise constraints |
| Primitive Extraction | When duplication detected | Approve moving to core |
| Evolution Proposal | When modifying existing domain | Approve/reject changes |

### Version Bumping

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fix in validation | PATCH | 1.0.0 → 1.0.1 |
| Add optional field | MINOR | 1.0.0 → 1.1.0 |
| Add new entity | MINOR | 1.0.0 → 1.1.0 |
| Change required field | MAJOR | 1.0.0 → 2.0.0 |
| Remove entity | MAJOR | 1.0.0 → 2.0.0 |

---

## 9. Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Duplicate TimePoint in every domain | Import from core |
| Modify production domain without approval | Propose evolution, wait for approval |
| Create domain-specific Money type | Use core:Money |
| Skip validation rules | Always define SHACL constraints |
| Create domain without presenting to human | Always use approval gates |
| Hard-code enums in prototype | Define in domain ontology |
| Invent domain model from scratch | Research schema.org, GitHub projects, provider APIs first |
| Ignore industry conventions | Align with Stripe, Twilio, etc. patterns for familiar DX |
| Skip research phase | Always research before proposing - see 3.1 External Research |