# First Principles Domain Model Framework

## Overview

This document decomposes domain modeling to fundamental primitives drawn from **physics**, **philosophy (metaphysics)**, and **biology**. The goal is to identify the irreducible building blocks from which all domain models can be composed.

---

## 1. The Four Fundamental Primitives

Drawing from first principles across disciplines:

```
                    ┌─────────────────────────────────────────┐
                    │         DOMAIN MODEL UNIVERSE           │
                    └─────────────────────────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
        ▼                              ▼                              ▼
   ┌─────────┐                  ┌─────────────┐                ┌───────────┐
   │ MATTER  │                  │   ENERGY    │                │   FORM    │
   │ (Being) │                  │  (Becoming) │                │ (Pattern) │
   └────┬────┘                  └──────┬──────┘                └─────┬─────┘
        │                              │                              │
        │         ┌────────────────────┴────────────────────┐         │
        │         │                                          │         │
        ▼         ▼                                          ▼         ▼
   ┌─────────────────────┐                           ┌─────────────────────┐
   │      SUBSTANCE      │◄──────── CHANGE ─────────►│      RELATION       │
   │   (what exists)     │       (transformation)     │    (connection)     │
   └─────────────────────┘                           └─────────────────────┘
```

### 1.1 SUBSTANCE (Being/Matter)

**Source:** Aristotelian metaphysics, physics (matter)

What exists - things with identity and persistence.

| Primitive | Description | Examples |
|-----------|-------------|----------|
| **Entity** | Anything with identity | Person, Order, Document |
| **Attribute** | Property of an entity | name, color, size |
| **Boundary** | What defines entity limits | scope, membership |
| **Identity** | What makes it THIS entity | id, fingerprint, hash |

**Physics analog:** Matter - has mass, occupies space
**Biology analog:** Organism - maintains identity over time

---

### 1.2 CHANGE (Becoming/Energy)

**Source:** Heraclitus ("everything flows"), thermodynamics (energy)

What happens - transformations between states.

| Primitive | Description | Examples |
|-----------|-------------|----------|
| **State** | Snapshot of entity at instant | pending, active, archived |
| **Event** | Occurrence marking change | OrderPlaced, UserCreated |
| **Transition** | Movement between states | pending → active |
| **Action** | Agent-initiated change | CreateOrder, ApproveRequest |
| **Force** | What causes/enables change | trigger, motivation, cause |

**Physics analog:** Energy - capacity to do work, causes state change
**Biology analog:** Metabolism - energy flow enabling life processes

---

### 1.3 RELATION (Connection/Form)

**Source:** Category theory, graph theory, ecology (food webs)

How things connect - structure and pattern.

| Primitive | Description | Examples |
|-----------|-------------|----------|
| **Link** | Connection between entities | owns, contains, references |
| **Role** | Function within relationship | buyer, seller, approver |
| **Cardinality** | Quantity of relationship | one-to-one, one-to-many |
| **Constraint** | Rules governing connection | must, may, must-not |
| **Hierarchy** | Nested containment | parent-child, tree |
| **Network** | Many-to-many connections | graph, mesh |

**Physics analog:** Forces/Fields - electromagnetic, gravitational binding
**Biology analog:** Symbiosis, predation, parasitism - ecological relationships

---

### 1.4 VALUE (Worth/Information)

**Source:** Information theory, economics, thermodynamics (entropy)

What matters - measurable quantities and qualitative assessments.

| Primitive | Description | Examples |
|-----------|-------------|----------|
| **Quantity** | Measurable amount | 5 kg, $100, 3 items |
| **Quality** | Qualitative assessment | high, medium, low |
| **Unit** | Standard of measurement | kg, USD, meters |
| **Ratio** | Relationship between quantities | 3:1, 50%, 0.85 |
| **Worth** | Subjective/objective value | utility, price, importance |

**Physics analog:** Measurable properties - mass, charge, temperature
**Biology analog:** Fitness - reproductive success, survival value

---

## 2. The Dimensional Primitives

Every entity exists in context - these are the dimensional primitives:

### 2.1 SPACE (Where)

| Primitive | Description |
|-----------|-------------|
| **Point** | Location with no extent |
| **Extent** | Size/volume in space |
| **Boundary** | Limit in space |
| **Region** | Bounded area/volume |
| **Distance** | Separation between points |

### 2.2 TIME (When)

| Primitive | Description |
|-----------|-------------|
| **Instant** | Point in time |
| **Interval** | Duration between instants |
| **Sequence** | Order of events |
| **Cycle** | Repeating pattern |
| **Epoch** | Reference point for time |

---

## 3. Mapping to Physics, Philosophy, Biology

### 3.1 Physics Mapping

| Domain Primitive | Physics Concept | Conservation Law |
|------------------|-----------------|------------------|
| Entity | Matter/Mass | Conservation of mass |
| State | Configuration | - |
| Change/Event | Energy transfer | Conservation of energy |
| Transition | Work | First law of thermodynamics |
| Value (Quantity) | Observable | Measurement theory |
| Relation | Force/Field | - |
| Space | Position vector | - |
| Time | Time coordinate | - |

### 3.2 Philosophy (Metaphysics) Mapping

| Domain Primitive | Aristotelian | Kantian | Process Philosophy |
|------------------|--------------|---------|-------------------|
| Entity | Substance | Thing-in-itself | Actual entity |
| Attribute | Accident | Property | - |
| State | Form | - | - |
| Change | Potentiality→Actuality | - | Becoming |
| Relation | Category | Category of relation | Prehension |
| Value | Final cause | - | Subjective aim |

### 3.3 Biology Mapping

| Domain Primitive | Biological Concept | Example |
|------------------|-------------------|---------|
| Entity | Organism | Cell, animal, plant |
| Boundary | Membrane, skin | Cell wall |
| State | Phenotype | Awake, dormant |
| Change | Metabolism, growth | Mitosis |
| Transition | Development | Caterpillar→butterfly |
| Relation | Symbiosis, ecology | Predator-prey |
| Value | Fitness | Reproductive success |

---

## 4. Proposed Atomic Domain Decomposition

### 4.1 Foundation Layer (Irreducible)

```
foundation/
├── entity/           # Identity, persistence
├── state/            # State machines, snapshots
├── event/            # Occurrences, signals
├── relation/         # Links, roles, graphs
├── quantity/         # Measurement, units
├── space/            # Location, geometry
└── time/             # Instants, intervals
```

### 4.2 Composition Layer (Combines Foundation)

```
composition/
├── flow/             # entity + event + time (processes)
├── structure/        # entity + relation (hierarchies, graphs)
├── measure/          # quantity + space + time (metrics)
├── lifecycle/        # entity + state + event (state machines)
└── exchange/         # entity + relation + quantity (transactions)
```

### 4.3 Domain Layer (Business Concepts)

```
domain/
├── actor/            # entity + capability + relation
├── resource/         # entity + quantity + state
├── process/          # flow + resource + actor
├── agreement/        # relation + constraint + time
└── transaction/      # exchange + actor + time
```

---

## 5. New Primitive Domains to Create

Based on first-principles analysis, these atomic domains are missing or incomplete:

### 5.1 `primitive-entity` (Foundation)

The absolute base - identity and persistence.

```yaml
entities:
  Thing:
    description: Anything that can be referred to
    properties:
      id: { type: string, required: true }

  IdentifiableThing:
    extends: Thing
    description: Thing with stable identity over time
    properties:
      identity: { type: Identity }

  Identity:
    description: What makes something THIS thing
    properties:
      type: { type: IdentityType }  # natural, surrogate, composite
      value: { type: string }
      namespace: { type: string }
```

### 5.2 `primitive-state` (Foundation)

Explicit state modeling as first-class concept.

```yaml
entities:
  State:
    description: Named condition of an entity
    properties:
      name: { type: string, required: true }
      isInitial: { type: boolean }
      isFinal: { type: boolean }

  StateMachine:
    description: Set of states with transitions
    properties:
      states: { type: array, items: State }
      transitions: { type: array, items: StateTransition }
      currentState: { type: State }

  StateTransition:
    description: Movement from one state to another
    properties:
      from: { type: State, required: true }
      to: { type: State, required: true }
      trigger: { type: string }
      guard: { type: string }  # condition
      effect: { type: string }  # side effect
```

### 5.3 `primitive-relation` (Foundation)

Graph/link primitives for connecting entities.

```yaml
entities:
  Link:
    description: Connection between two things
    properties:
      source: { type: string, required: true }
      target: { type: string, required: true }
      type: { type: string }

  DirectedLink:
    extends: Link
    description: Asymmetric connection (A→B ≠ B→A)

  Role:
    description: Function within a relationship
    properties:
      name: { type: string, required: true }
      cardinality: { type: Cardinality }

  Cardinality:
    description: Quantity constraints on relationship
    properties:
      min: { type: integer, default: 0 }
      max: { type: integer }  # null = unbounded
```

### 5.4 `primitive-event` (Foundation)

Occurrences as first-class entities.

```yaml
entities:
  Event:
    description: Something that happened at a point in time
    properties:
      id: { type: string, required: true }
      type: { type: string, required: true }
      occurredAt: { type: datetime, required: true }
      source: { type: string }

  DomainEvent:
    extends: Event
    description: Business-meaningful occurrence
    properties:
      aggregateId: { type: string }
      aggregateType: { type: string }
      payload: { type: object }

  Signal:
    extends: Event
    description: Notification of something
    properties:
      severity: { type: Severity }
```

### 5.5 `primitive-quantity` (Foundation)

Measurement as atomic concept.

```yaml
entities:
  Quantity:
    description: Amount of something measurable
    properties:
      value: { type: decimal, required: true }
      unit: { type: Unit, required: true }

  Unit:
    description: Standard of measurement
    properties:
      symbol: { type: string, required: true }
      name: { type: string }
      dimension: { type: Dimension }

  Dimension:
    description: Physical dimension (length, mass, time, etc.)
    properties:
      type: { type: DimensionType }  # L, M, T, I, Θ, N, J

  Ratio:
    description: Relationship between two quantities
    properties:
      numerator: { type: Quantity }
      denominator: { type: Quantity }
```

---

## 6. Composition Principles

### 6.1 Single Responsibility

Each primitive domain models ONE concept:
- `entity` = identity
- `state` = condition
- `event` = occurrence
- `relation` = connection
- `quantity` = measurement

### 6.2 Composition Over Inheritance

Build complex concepts by combining primitives:
```
Order = entity + state + relation(to: Customer) + quantity(total)
```

### 6.3 Immutability Where Possible

Prefer events over mutable state:
```
OrderPlaced → OrderPaid → OrderShipped (events)
vs.
Order.status = 'placed' → 'paid' → 'shipped' (mutation)
```

### 6.4 Separation of Concerns

| Concern | Domain |
|---------|--------|
| What exists | entity, resource |
| What happens | event, action |
| How connected | relation, graph |
| How much | quantity, measure |
| Where | space, geo |
| When | time, schedule |

---

## 7. Migration Path

### Phase 1: Create Foundation Primitives

1. `primitive-entity` - base identity
2. `primitive-state` - state machines
3. `primitive-event` - occurrences
4. `primitive-relation` - connections
5. `primitive-quantity` - measurements

### Phase 2: Refactor Core Domain

- Split `core` into primitive domains
- `core` becomes a re-export of primitives
- Backward compatible via type aliases

### Phase 3: Update Existing Domains

- Each domain imports only needed primitives
- Explicit composition documented
- Dependency graph simplified

---

## 8. Theoretical Foundation

### 8.1 Category Theory Perspective

Domains as categories:
- Objects = entity types
- Morphisms = relations/transformations
- Composition = domain composition
- Identity = entity identity

### 8.2 Type Theory Perspective

```typescript
// Sum types for states
type OrderState = 'pending' | 'paid' | 'shipped' | 'delivered';

// Product types for entities
type Order = {
  id: EntityId;
  state: OrderState;
  customer: Relation<Customer>;
  total: Quantity<Money>;
};

// Function types for actions
type PlaceOrder = (cart: Cart) => Event<OrderPlaced>;
```

### 8.3 Process Algebra Perspective

```
Order = pending.pay.paid.ship.shipped.deliver.delivered.STOP
```

---

## 9. Summary: The Irreducible Primitives

| # | Primitive | Question Answered | Physics Analog | Biology Analog |
|---|-----------|-------------------|----------------|----------------|
| 1 | **Entity** | What is it? | Particle | Organism |
| 2 | **State** | What condition? | Configuration | Phenotype |
| 3 | **Event** | What happened? | Interaction | Stimulus |
| 4 | **Relation** | How connected? | Force/Field | Symbiosis |
| 5 | **Quantity** | How much? | Observable | Fitness |
| 6 | **Space** | Where? | Position | Habitat |
| 7 | **Time** | When? | Time | Lifespan |

These seven primitives, combined with composition rules, can generate any domain model.

---

## 10. Next Steps

1. **Create primitive domain schemas** - YAML definitions for each primitive
2. **Refactor core** - Express core as composition of primitives
3. **Document composition patterns** - How to combine primitives
4. **Update registry** - Add primitive domains with dependencies
5. **Migration guide** - How existing domains should evolve

---

---

## 11. Agent-Centric Decomposition: Actor-Intent-Tool-Resource

An alternative (complementary) first-principles decomposition focusing on **agency** and **action**:

### 11.1 The AITR Framework

```
┌──────────────────────────────────────────────────────────────────┐
│                      AGENCY MODEL                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────┐    has     ┌─────────┐    uses     ┌─────────┐    │
│   │  ACTOR  │───────────►│ INTENT  │────────────►│  TOOL   │    │
│   └────┬────┘            └────┬────┘             └────┬────┘    │
│        │                      │                       │          │
│        │ consumes             │ achieves              │ operates │
│        ▼                      ▼                       ▼          │
│   ┌─────────┐            ┌─────────┐            ┌─────────┐     │
│   │RESOURCE │◄───────────│ OUTCOME │◄───────────│ ACTION  │     │
│   └─────────┘  transforms └─────────┘  produces  └─────────┘     │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### 11.2 The Four Agency Primitives

#### ACTOR (Who)

The agent that initiates action - can be human, machine, organization, or AI.

| Primitive | Description | Examples |
|-----------|-------------|----------|
| **Human** | Biological agent | User, employee, customer |
| **Machine** | Automated system | Server, robot, IoT device |
| **AI** | Intelligent system | LLM, agent, model |
| **Organization** | Collective agent | Company, team, department |
| **Role** | Actor function | Admin, approver, viewer |
| **Principal** | Identity for auth | User account, service account |

```yaml
# primitive-actor
Actor:
  properties:
    id: { type: string, required: true }
    type: { type: ActorType }  # human, machine, ai, org
    capabilities: { type: array, items: Capability }
    permissions: { type: array, items: Permission }
    availability: { type: Availability }
```

#### INTENT (Why)

What the actor wants to achieve - the goal or objective.

| Primitive | Description | Examples |
|-----------|-------------|----------|
| **Goal** | Desired end state | "order placed", "report generated" |
| **Objective** | Measurable target | "reduce latency by 20%" |
| **Need** | Requirement to fulfill | "authentication required" |
| **Desire** | Preference | "prefer fast over cheap" |
| **Constraint** | Limitation on achievement | "budget < $1000" |

```yaml
# primitive-intent
Intent:
  properties:
    id: { type: string, required: true }
    description: { type: string, required: true }
    goalState: { type: State }
    priority: { type: Priority }
    constraints: { type: array, items: Constraint }
    deadline: { type: datetime }

Constraint:
  properties:
    type: { type: ConstraintType }  # temporal, resource, quality
    expression: { type: string }
    hardness: { type: Hardness }  # hard, soft, preference
```

#### TOOL (How)

The instrument used to accomplish the intent - capabilities and functions.

| Primitive | Description | Examples |
|-----------|-------------|----------|
| **Capability** | What the tool can do | "send email", "read file" |
| **Function** | Executable operation | API endpoint, method |
| **Service** | Packaged capabilities | Email service, payment gateway |
| **Interface** | Access contract | API, CLI, UI |
| **Protocol** | Interaction pattern | REST, GraphQL, gRPC |

```yaml
# primitive-tool
Tool:
  properties:
    id: { type: string, required: true }
    name: { type: string, required: true }
    description: { type: string }
    capabilities: { type: array, items: Capability }
    inputs: { type: array, items: Parameter }
    outputs: { type: array, items: Result }
    cost: { type: Cost }  # resource cost to use

Capability:
  properties:
    name: { type: string, required: true }
    verb: { type: string }  # create, read, update, delete, transform
    operatesOn: { type: string }  # entity type
```

#### RESOURCE (What)

What is consumed, produced, or transformed - the materials of action.

| Primitive | Description | Examples |
|-----------|-------------|----------|
| **Material** | Physical resource | Inventory, parts, ingredients |
| **Information** | Data resource | Records, documents, messages |
| **Compute** | Processing capacity | CPU, memory, storage |
| **Time** | Temporal resource | Duration, deadline, schedule |
| **Money** | Financial resource | Budget, cost, payment |
| **Attention** | Cognitive resource | Human focus, priority |

```yaml
# primitive-resource
Resource:
  properties:
    id: { type: string, required: true }
    type: { type: ResourceType }  # material, information, compute, time, money
    quantity: { type: Quantity }
    availability: { type: Availability }
    cost: { type: Cost }

ResourcePool:
  properties:
    resources: { type: array, items: Resource }
    capacity: { type: Quantity }
    allocated: { type: Quantity }
    available: { type: Quantity }
```

### 11.3 The Connecting Primitives

#### ACTION (Actor + Tool → Resource)

```yaml
Action:
  properties:
    actor: { type: Actor, required: true }
    tool: { type: Tool, required: true }
    intent: { type: Intent }
    inputResources: { type: array, items: Resource }
    outputResources: { type: array, items: Resource }
    timestamp: { type: datetime, required: true }
```

#### OUTCOME (Intent realized)

```yaml
Outcome:
  properties:
    intent: { type: Intent, required: true }
    status: { type: OutcomeStatus }  # achieved, partial, failed
    result: { type: object }
    resourcesConsumed: { type: array, items: Resource }
    resourcesProduced: { type: array, items: Resource }
```

### 11.4 AITR + Matter-Energy-Change Synthesis

These two frameworks are complementary:

| Physics/Metaphysics | Agency (AITR) | Combined View |
|---------------------|---------------|---------------|
| Entity | Actor + Resource | Things that exist |
| State | Resource state, Intent state | Current condition |
| Change | Action | Transformation |
| Event | Action occurrence | What happened |
| Relation | Actor↔Resource, Actor↔Tool | Connections |
| Value | Resource quantity | Measurement |

### 11.5 Unified Primitive Model

```
┌────────────────────────────────────────────────────────────────────┐
│                   UNIFIED DOMAIN PRIMITIVES                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  STRUCTURAL (Being)        DYNAMIC (Becoming)      AGENTIC (Doing) │
│  ────────────────         ─────────────────       ──────────────── │
│  • Entity                 • Event                  • Actor         │
│  • Attribute              • State                  • Intent        │
│  • Relation               • Transition             • Tool          │
│  • Quantity               • Action                 • Resource      │
│                                                                    │
│  DIMENSIONAL (Context)                                             │
│  ────────────────────                                              │
│  • Space (where)                                                   │
│  • Time (when)                                                     │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 11.6 Composition Examples

**Order Placement:**
```
Actor:     Customer (human)
Intent:    Purchase products
Tool:      Shopping cart, checkout
Resources: Money (consumed), Products (transferred), Order (created)
Action:    PlaceOrder
Outcome:   Order confirmed, inventory decremented
```

**API Request:**
```
Actor:     Client application (machine)
Intent:    Retrieve user data
Tool:      REST API endpoint
Resources: Auth token (consumed), Compute (consumed), User data (produced)
Action:    GET /users/{id}
Outcome:   JSON response returned
```

**LLM Conversation:**
```
Actor:     User (human) + Assistant (AI)
Intent:    Generate code
Tool:      Claude API, code interpreter
Resources: Tokens (consumed), Context window (consumed), Code (produced)
Action:    Chat completion
Outcome:   Working code generated
```

### 11.7 Domain Mapping to AITR

| Existing Domain | Primary AITR Role |
|-----------------|-------------------|
| `auth` | Actor (identity, permissions) |
| `intent` | Intent |
| `action` | Tool (capabilities) |
| `llm-tool-use` | Tool |
| `economic-actor` | Actor |
| `economic-value` | Resource (money) |
| `material` | Resource (physical) |
| `inventory` | Resource pool |
| `capability` | Tool |
| `human-task` | Actor + Intent |
| `workflow` | Intent + Action sequence |

---

## 12. Recommended Primitive Domain Structure

Based on both frameworks, here's the proposed atomic domain structure:

```
shared/semantic/domains/
├── _primitives/                    # Foundation layer
│   ├── entity/                     # Identity, persistence
│   │   └── schema.yaml
│   ├── state/                      # State machines
│   │   └── schema.yaml
│   ├── event/                      # Occurrences
│   │   └── schema.yaml
│   ├── relation/                   # Connections, graphs
│   │   └── schema.yaml
│   ├── quantity/                   # Measurements
│   │   └── schema.yaml
│   ├── actor/                      # Agents
│   │   └── schema.yaml
│   ├── intent/                     # Goals, objectives
│   │   └── schema.yaml
│   ├── tool/                       # Capabilities
│   │   └── schema.yaml
│   └── resource/                   # Consumables
│       └── schema.yaml
│
├── _dimensional/                   # Context layer
│   ├── space/                      # Location, geometry
│   │   └── schema.yaml
│   └── time/                       # Temporal primitives
│       └── schema.yaml
│
└── _composite/                     # Composition layer
    ├── lifecycle/                  # entity + state + event
    ├── flow/                       # actor + action + resource + time
    ├── exchange/                   # actor + resource + relation
    └── structure/                  # entity + relation + hierarchy
```

---

## 13. Atomic Design Parallel (UI/UX Methodology)

Brad Frost's Atomic Design provides a useful parallel for domain model composition:

### 13.1 Atomic Design Levels

```
┌────────────────────────────────────────────────────────────────────┐
│                     ATOMIC DESIGN → DOMAIN MODELING                │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  UI/UX ATOMIC DESIGN           DOMAIN MODEL EQUIVALENT             │
│  ─────────────────────        ─────────────────────────            │
│                                                                    │
│  ATOMS                         PRIMITIVES                          │
│  (button, input, label)        (entity, state, event, quantity)    │
│        │                              │                            │
│        ▼                              ▼                            │
│  MOLECULES                     COMPOSITIONS                        │
│  (search form, card)           (lifecycle, flow, exchange)         │
│        │                              │                            │
│        ▼                              ▼                            │
│  ORGANISMS                     DOMAINS                             │
│  (header, product list)        (email, finance, auth)              │
│        │                              │                            │
│        ▼                              ▼                            │
│  TEMPLATES                     PATTERNS                            │
│  (page layout)                 (ecommerce, CRM, healthcare)        │
│        │                              │                            │
│        ▼                              ▼                            │
│  PAGES                         APPLICATIONS                        │
│  (homepage, checkout)          (online store, patient portal)      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 13.2 Detailed Mapping

| Atomic Design | Domain Models | Description | Examples |
|---------------|---------------|-------------|----------|
| **Atoms** | Primitives | Indivisible building blocks | Entity, State, Event, Quantity, Actor, Resource, Intent, Tool |
| **Molecules** | Compositions | Combinations of primitives | Lifecycle (entity+state+event), Flow (actor+action+time), Exchange (actor+resource+relation) |
| **Organisms** | Domains | Functional groupings | Email, Finance, Auth, Calendar, Workflow |
| **Templates** | Industry Patterns | Domain combinations for verticals | E-commerce (catalog+cart+checkout), Healthcare (patient+provider+encounter) |
| **Pages** | Applications | Specific implementations | Amazon.com, Epic EMR, Salesforce CRM |

### 13.3 Design Principles Transfer

| Atomic Design Principle | Domain Model Equivalent |
|-------------------------|-------------------------|
| **Atoms are abstract** | Primitives have no business logic |
| **Molecules combine atoms** | Compositions combine primitives |
| **Organisms have meaning** | Domains have business context |
| **Templates are structural** | Patterns define architecture |
| **Pages are concrete** | Applications are deployable |

### 13.4 Reusability at Each Level

```
LEVEL          REUSE SCOPE              CHANGE FREQUENCY
────────────────────────────────────────────────────────
Primitives     Universal (all domains)  Very rare
Compositions   Cross-domain             Rare
Domains        Industry-specific        Occasional
Patterns       Vertical-specific        Moderate
Applications   Instance-specific        Frequent
```

### 13.5 Domain Model Atomic Hierarchy

```
shared/semantic/domains/
│
├── _primitives/              ← ATOMS (9 primitives)
│   ├── entity/               # Identity, existence
│   ├── state/                # Conditions, transitions
│   ├── event/                # Occurrences, signals
│   ├── relation/             # Connections, graphs
│   ├── quantity/             # Measurements, units
│   ├── actor/                # Agents who act
│   ├── intent/               # Goals, objectives
│   ├── tool/                 # Capabilities
│   └── resource/             # Consumables
│
├── _dimensional/             ← ATOMS (context)
│   ├── space/                # Location, geometry
│   └── time/                 # Temporal primitives
│
├── _composite/               ← MOLECULES
│   ├── lifecycle/            # entity + state + event
│   ├── flow/                 # actor + action + resource + time
│   ├── exchange/             # actor + resource + relation
│   └── structure/            # entity + relation + hierarchy
│
├── [domain]/                 ← ORGANISMS (55+ domains)
│   ├── email/
│   ├── finance/
│   ├── auth/
│   └── ...
│
└── _patterns/                ← TEMPLATES
    ├── ecommerce/            # catalog + cart + checkout + fulfillment
    ├── healthcare/           # patient + provider + encounter + billing
    ├── saas/                 # auth + subscription + usage + billing
    └── marketplace/          # buyer + seller + listing + transaction
```

### 13.6 Composition Rules (Like CSS Cascade)

Just as CSS has specificity rules, domain composition has precedence:

```
1. Primitive defines base structure
2. Composition adds relationships
3. Domain adds business rules
4. Pattern adds vertical constraints
5. Application adds instance config
```

Example - Order entity cascade:

```yaml
# Level 1: Primitive (entity)
Entity:
  id: string

# Level 2: Composition (lifecycle)
Lifecycle:
  entity: Entity
  states: [State]
  events: [Event]

# Level 3: Domain (ecommerce)
Order:
  extends: Lifecycle
  states: [pending, paid, shipped, delivered]
  lineItems: [LineItem]
  total: Money

# Level 4: Pattern (retail)
RetailOrder:
  extends: Order
  shippingAddress: Address
  returnPolicy: ReturnPolicy

# Level 5: Application (specific store)
AcmeOrder:
  extends: RetailOrder
  loyaltyPoints: integer
  giftWrapping: boolean
```

### 13.7 Benefits of Atomic Approach

| Benefit | UI/UX | Domain Models |
|---------|-------|---------------|
| **Consistency** | Design system | Schema registry |
| **Reusability** | Component library | Domain library |
| **Maintainability** | Change in one place | Update primitive, all domains update |
| **Scalability** | Add new pages easily | Add new domains easily |
| **Communication** | Shared vocabulary | Ubiquitous language |
| **Testing** | Test atoms, molecules | Validate primitives, compositions |

---

## 14. Summary: The Complete Primitive Set

### 14.1 The 11 Primitives

| # | Primitive | Category | Question | First Principle |
|---|-----------|----------|----------|-----------------|
| 1 | **Entity** | Structural | What is it? | Matter (physics) |
| 2 | **State** | Dynamic | What condition? | Configuration (physics) |
| 3 | **Event** | Dynamic | What happened? | Interaction (physics) |
| 4 | **Relation** | Structural | How connected? | Force/Field (physics) |
| 5 | **Quantity** | Structural | How much? | Observable (physics) |
| 6 | **Actor** | Agentic | Who acts? | Agent (philosophy) |
| 7 | **Intent** | Agentic | Why act? | Teleology (philosophy) |
| 8 | **Tool** | Agentic | How act? | Techne (philosophy) |
| 9 | **Resource** | Agentic | With what? | Conservation (physics) |
| 10 | **Space** | Dimensional | Where? | Geometry |
| 11 | **Time** | Dimensional | When? | Duration |

### 14.2 Composition Formula

Any domain model can be expressed as:

```
Domain = Σ(Primitives) + Rules + Context

Where:
- Primitives: selected from the 11 above
- Rules: business logic, constraints, validations
- Context: industry, vertical, application specifics
```

### 14.3 Example Decompositions

**Email Domain:**
```
Email = Entity + State(draft/sent/read) + Event(received) +
        Relation(to/from/cc) + Actor(sender/recipient) + Time(sentAt)
```

**E-commerce Order:**
```
Order = Entity + State(lifecycle) + Event(placed/paid/shipped) +
        Relation(customer/products) + Quantity(total) +
        Actor(buyer) + Intent(purchase) + Resource(payment) + Time(timestamps)
```

**Workflow:**
```
Workflow = Entity + State(steps) + Event(transitions) +
           Relation(sequence) + Actor(assignees) + Intent(completion) +
           Tool(actions) + Time(deadlines)
```

---

## 15. RDF and Graph Theory Foundation

The primitives map directly to RDF and graph structures - they are essentially the same concepts with different vocabulary.

### 15.1 The Triple as Universal Primitive

RDF's fundamental unit is the **triple**: `Subject → Predicate → Object`

```
┌────────────────────────────────────────────────────────────────────┐
│                    RDF TRIPLE STRUCTURE                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│    ┌──────────┐         ┌──────────────┐         ┌──────────┐    │
│    │ SUBJECT  │────────►│  PREDICATE   │────────►│  OBJECT  │    │
│    │ (Entity) │         │  (Relation)  │         │ (Entity/ │    │
│    └──────────┘         └──────────────┘         │  Literal)│    │
│                                                   └──────────┘    │
│                                                                    │
│    Example:                                                        │
│    :Order123  :hasCustomer  :Customer456                          │
│    :Order123  :hasTotal     "99.99"^^xsd:decimal                  │
│    :Order123  :hasStatus    :StatusPending                        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 15.2 Primitive → RDF Mapping

| Primitive | RDF Concept | Graph Concept | Example |
|-----------|-------------|---------------|---------|
| **Entity** | Resource (URI) | Node | `:Order123` |
| **Relation** | Property/Predicate | Edge | `:hasCustomer` |
| **Quantity** | Typed Literal | Node property | `"99.99"^^xsd:decimal` |
| **State** | Resource (enum) | Node | `:StatusPending` |
| **Event** | Reified Statement | Hyperedge | Event as node with edges |
| **Actor** | Agent Resource | Node (typed) | `:Customer456 a :Person` |
| **Intent** | Goal Resource | Node | `:Intent789 :achieves :State` |
| **Tool** | Capability Resource | Node | `:PaymentAPI a :Tool` |
| **Resource** | Resource (URI) | Node | `:Budget a :MonetaryResource` |

### 15.3 Graph Database Equivalence

```
┌─────────────────────────────────────────────────────────────────────┐
│               LABELED PROPERTY GRAPH (Neo4j style)                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────┐                    ┌─────────────────┐       │
│   │     :Order      │                    │    :Customer    │       │
│   │  {id: "123"}    │──[:PLACED_BY]─────►│  {name: "Alice"}│       │
│   │  {total: 99.99} │                    │  {email: "..."}│       │
│   │  {status: "new"}│                    └─────────────────┘       │
│   └────────┬────────┘                                               │
│            │                                                        │
│            │ [:CONTAINS]                                            │
│            ▼                                                        │
│   ┌─────────────────┐                    ┌─────────────────┐       │
│   │   :LineItem     │──[:PRODUCT]───────►│    :Product     │       │
│   │  {qty: 2}       │                    │  {sku: "ABC"}   │       │
│   │  {price: 49.99} │                    │  {name: "..."}  │       │
│   └─────────────────┘                    └─────────────────┘       │
│                                                                     │
│   NODE = Entity + Attributes (Quantity)                             │
│   EDGE = Relation                                                   │
│   LABEL = Entity Type / State                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 15.4 Semantic Web Stack Alignment

```
APPLICATION          │  Applications (Pages)
─────────────────────┼──────────────────────────────────
TRUST / PROOF        │  Validation, Constraints
─────────────────────┼──────────────────────────────────
LOGIC / RULES        │  SHACL shapes = Intent constraints
                     │  OWL axioms = Business rules
─────────────────────┼──────────────────────────────────
ONTOLOGY (OWL)       │  Domains (Organisms)
                     │  Classes, Properties, Restrictions
─────────────────────┼──────────────────────────────────
RDFS                 │  Compositions (Molecules)
                     │  Class hierarchy, domain/range
─────────────────────┼──────────────────────────────────
RDF                  │  Primitives (Atoms)
                     │  Triples: Entity-Relation-Entity
─────────────────────┼──────────────────────────────────
URI / IRI            │  Identity (Entity.id)
─────────────────────┼──────────────────────────────────
UNICODE              │  Encoding
```

### 15.5 Complete RDF Vocabulary Mapping

```turtle
# Namespace declarations
@prefix prim: <http://protoflow.ai/primitives#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

# ===========================================
# ENTITY → owl:Thing / rdfs:Resource
# ===========================================
prim:Entity a owl:Class ;
    rdfs:label "Entity" ;
    rdfs:comment "Anything with identity - maps to rdfs:Resource" ;
    owl:equivalentClass rdfs:Resource .

# ===========================================
# RELATION → rdf:Property
# ===========================================
prim:Relation a owl:Class ;
    rdfs:subClassOf rdf:Property ;
    rdfs:label "Relation" ;
    rdfs:comment "Connection between entities - maps to rdf:Property" .

# ===========================================
# QUANTITY → Typed Literals
# ===========================================
prim:Quantity a owl:Class ;
    rdfs:label "Quantity" ;
    rdfs:comment "Measurable amount - maps to typed literals" .

prim:hasValue a owl:DatatypeProperty ;
    rdfs:domain prim:Quantity ;
    rdfs:range xsd:decimal .

prim:hasUnit a owl:ObjectProperty ;
    rdfs:domain prim:Quantity ;
    rdfs:range prim:Unit .

# ===========================================
# STATE → Named Individual (enum pattern)
# ===========================================
prim:State a owl:Class ;
    rdfs:label "State" ;
    rdfs:comment "Condition - maps to named individuals" .

# States are individuals, not classes
prim:ActiveState a prim:State ;
    rdfs:label "Active" .

prim:PendingState a prim:State ;
    rdfs:label "Pending" .

# ===========================================
# EVENT → Reification Pattern
# ===========================================
prim:Event a owl:Class ;
    rdfs:label "Event" ;
    rdfs:comment "Occurrence - uses RDF reification or named graphs" .

prim:occurredAt a owl:DatatypeProperty ;
    rdfs:domain prim:Event ;
    rdfs:range xsd:dateTime .

prim:causedBy a owl:ObjectProperty ;
    rdfs:domain prim:Event ;
    rdfs:range prim:Actor .

# ===========================================
# ACTOR → foaf:Agent
# ===========================================
prim:Actor a owl:Class ;
    rdfs:subClassOf <http://xmlns.com/foaf/0.1/Agent> ;
    rdfs:label "Actor" ;
    rdfs:comment "Agent that can act - maps to foaf:Agent" .
```

### 15.6 Graph Query Patterns

Each primitive maps to graph traversal patterns:

```cypher
// ENTITY - Find by identity
MATCH (e:Entity {id: $id}) RETURN e

// RELATION - Traverse connection
MATCH (a)-[r:RELATION_TYPE]->(b) RETURN a, r, b

// STATE - Filter by state
MATCH (e:Entity)-[:HAS_STATE]->(:State {name: "active"})

// EVENT - Temporal query
MATCH (e:Event)
WHERE e.occurredAt > datetime('2025-01-01')
RETURN e ORDER BY e.occurredAt

// ACTOR + INTENT + TOOL + RESOURCE (AITR)
MATCH (actor:Actor)-[:HAS_INTENT]->(intent:Intent),
      (actor)-[:USES]->(tool:Tool),
      (actor)-[:CONSUMES]->(resource:Resource)
RETURN actor, intent, tool, resource

// HIERARCHY (Relation pattern)
MATCH path = (root:Entity)-[:PARENT_OF*]->(descendant)
WHERE root.id = $rootId
RETURN path

// STATE MACHINE (State + Event + Transition)
MATCH (from:State)-[t:TRANSITION {trigger: $event}]->(to:State)
WHERE from.name = $currentState
RETURN to.name as nextState, t.effect as sideEffect
```

### 15.7 The Triple Decomposition

Every domain model decomposes to triples:

```
ORDER DOMAIN AS TRIPLES:

:Order123 rdf:type :Order .                    # Entity
:Order123 :hasId "123" .                       # Identity
:Order123 :hasStatus :Pending .                # State
:Order123 :placedBy :Customer456 .             # Relation (Actor)
:Order123 :hasTotal "99.99"^^xsd:decimal .     # Quantity
:Order123 :placedAt "2025-01-15T10:30:00Z" .   # Time
:Order123 :contains :LineItem1 .               # Relation (Composition)

:LineItem1 rdf:type :LineItem .
:LineItem1 :product :ProductABC .              # Relation
:LineItem1 :quantity "2"^^xsd:integer .        # Quantity

:OrderPlacedEvent rdf:type :Event .            # Event
:OrderPlacedEvent :concerns :Order123 .        # Relation
:OrderPlacedEvent :causedBy :Customer456 .     # Actor
:OrderPlacedEvent :occurredAt "..." .          # Time
```

### 15.8 Knowledge Graph as Composition

```
┌─────────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE GRAPH LAYERS                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INSTANCE DATA        :Order123 :hasStatus :Pending                 │
│  (ABox)               :Customer456 :name "Alice"                    │
│                       ────────────────────────────────              │
│                                    │                                │
│  TERMINOLOGICAL       :Order rdfs:subClassOf :Entity                │
│  (TBox)               :hasStatus rdfs:domain :Order                 │
│                       :hasStatus rdfs:range :OrderStatus            │
│                       ────────────────────────────────              │
│                                    │                                │
│  PRIMITIVES           prim:Entity, prim:State, prim:Relation        │
│  (Meta-TBox)          ────────────────────────────────              │
│                                                                     │
│  GRAPH STRUCTURE      Nodes (Entity) + Edges (Relation)             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 15.9 Why This Matters

| Benefit | Description |
|---------|-------------|
| **Interoperability** | Primitives can export to RDF/OWL, Neo4j, JSON-LD |
| **Reasoning** | OWL reasoners can infer new facts from primitives |
| **Validation** | SHACL shapes validate primitive constraints |
| **Querying** | SPARQL/Cypher provide powerful graph traversal |
| **Federation** | Linked data allows cross-system joins |
| **Standardization** | W3C standards ensure longevity |

### 15.10 Implementation Targets

From primitives, generate:

```
Primitive Schemas
       │
       ├──► RDF/OWL Ontology (.ttl, .owl)
       │    └── For semantic web tools, reasoners
       │
       ├──► JSON-LD Context (.jsonld)
       │    └── For web APIs, linked data
       │
       ├──► Neo4j Schema (Cypher)
       │    └── For graph database
       │
       ├──► GraphQL Schema (.graphql)
       │    └── For API layer
       │
       ├──► TypeScript Types (.ts)
       │    └── For application code
       │
       └──► SHACL Shapes (.shacl)
            └── For validation
```

---

## 16. Mathematical Foundation: Category Theory

The primitives form a category-theoretic structure:

### 16.1 Category of Domain Models

```
CATEGORY: DomainModel

Objects:    Entities (Entity, Actor, Resource, Tool, Intent)
Morphisms:  Relations (links between entities)
Identity:   Each entity has identity relation to itself
Composition: Relations compose (A→B, B→C implies A→C)

Example:
  Customer ──[places]──► Order ──[contains]──► LineItem

  Composition:
  Customer ──[purchases_item]──► LineItem
  (derived from places ∘ contains)
```

### 16.2 Functors Between Domains

```
A Functor F: DomainA → DomainB preserves structure:

F(Entity) → Entity
F(Relation) → Relation
F(Composition) = F(R1) ∘ F(R2)

Example: Email → Messaging functor
  F(Email) → Message
  F(sendTo) → recipient
  F(Attachment) → MediaAttachment
```

### 16.3 Natural Transformations

State transitions are natural transformations between functors:

```
η: CurrentState ⟹ NextState

For Order:
  η_pending: pending → paid
  η_paid: paid → shipped
  η_shipped: shipped → delivered
```

---

## 17. W3C Time Ontologies (OWL-Time, PROV-O)

### 17.1 W3C OWL-Time Ontology

The W3C Time Ontology (`time:`) provides standard temporal concepts:

```turtle
@prefix time: <http://www.w3.org/2006/time#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

# ===========================================
# OWL-TIME CORE CONCEPTS
# ===========================================

# Instant - a point in time (our TimePoint)
time:Instant a owl:Class ;
    rdfs:label "Instant" ;
    rdfs:comment "A zero-duration temporal entity" .

# Interval - a period of time (our DateRange)
time:Interval a owl:Class ;
    rdfs:label "Interval" ;
    rdfs:comment "A temporal entity with extent" .

# Duration - length of time (our Duration)
time:Duration a owl:Class ;
    rdfs:label "Duration" ;
    rdfs:comment "Duration of a temporal extent" .

# TemporalEntity - superclass
time:TemporalEntity a owl:Class ;
    owl:unionOf (time:Instant time:Interval) .
```

### 17.2 Primitive → OWL-Time Mapping

| Our Primitive | OWL-Time Equivalent | Description |
|---------------|---------------------|-------------|
| `TimePoint` | `time:Instant` | A moment in time |
| `DateRange` | `time:Interval` | Period with start/end |
| `Duration` | `time:Duration` | Length of time |
| `Recurrence` | `time:TemporalUnit` | Repeating patterns |
| `Season` | `time:GeneralDateTimeDescription` | Cyclical time |

### 17.3 Full OWL-Time Integration

```turtle
@prefix time: <http://www.w3.org/2006/time#> .
@prefix prim: <http://protoflow.ai/primitives#> .

# ===========================================
# TIMEPOINT maps to time:Instant
# ===========================================
prim:TimePoint rdfs:subClassOf time:Instant .

prim:TimePoint a owl:Class ;
    rdfs:label "Time Point" ;
    owl:equivalentClass [
        a owl:Restriction ;
        owl:onProperty time:inXSDDateTimeStamp ;
        owl:cardinality 1
    ] .

# ===========================================
# DATERANGE maps to time:Interval
# ===========================================
prim:DateRange rdfs:subClassOf time:Interval .

prim:DateRange a owl:Class ;
    rdfs:label "Date Range" .

prim:hasBeginning a owl:ObjectProperty ;
    rdfs:subPropertyOf time:hasBeginning ;
    rdfs:domain prim:DateRange ;
    rdfs:range prim:TimePoint .

prim:hasEnd a owl:ObjectProperty ;
    rdfs:subPropertyOf time:hasEnd ;
    rdfs:domain prim:DateRange ;
    rdfs:range prim:TimePoint .

# ===========================================
# DURATION maps to time:Duration
# ===========================================
prim:Duration rdfs:subClassOf time:Duration .

prim:Duration a owl:Class ;
    rdfs:label "Duration" .

prim:inXSDDuration a owl:DatatypeProperty ;
    rdfs:subPropertyOf time:inXSDDuration ;
    rdfs:domain prim:Duration ;
    rdfs:range xsd:duration .

# ===========================================
# ALLEN'S TEMPORAL RELATIONS
# ===========================================
# OWL-Time includes Allen's 13 interval relations

time:before           # A is before B
time:after            # A is after B
time:meets            # A ends when B starts
time:metBy            # A starts when B ends
time:overlaps         # A starts before B, ends during B
time:overlappedBy     # B starts before A, ends during A
time:starts           # A starts with B, ends before B
time:startedBy        # B starts with A
time:during           # A is completely within B
time:contains         # B is completely within A
time:finishes         # A ends with B, starts after B
time:finishedBy       # B ends with A
time:equals           # A and B are the same interval
```

### 17.4 Allen's Interval Algebra Visualization

```
A:    |-------|
B:              |-------|     A before B

A:    |-------|
B:            |-------|       A meets B

A:    |-------|
B:        |-------|           A overlaps B

A:    |-------|
B:    |---------------|       A starts B

A:    |-------|
B:  |---------|               A finishes B

A:    |-------|
B:      |--|                  A contains B

A:    |-------|
B:    |-------|               A equals B
```

### 17.5 PROV-O (Provenance Ontology)

W3C PROV-O captures events and their causes - maps to our Event primitive:

```turtle
@prefix prov: <http://www.w3.org/ns/prov#> .

# ===========================================
# PROV-O CORE CONCEPTS
# ===========================================

# Entity - thing affected by activities
prov:Entity a owl:Class ;
    rdfs:comment "Physical, digital, conceptual thing" .

# Activity - something that occurs (our Event)
prov:Activity a owl:Class ;
    rdfs:comment "Something that occurs over a period" .

# Agent - responsible party (our Actor)
prov:Agent a owl:Class ;
    rdfs:comment "Something that bears responsibility" .

# ===========================================
# PRIMITIVE → PROV-O MAPPING
# ===========================================

prim:Event rdfs:subClassOf prov:Activity .
prim:Actor rdfs:subClassOf prov:Agent .
prim:Entity rdfs:subClassOf prov:Entity .

# Key PROV-O relationships
prov:wasGeneratedBy   # Entity created by Activity
prov:used             # Activity used Entity
prov:wasAttributedTo  # Entity attributed to Agent
prov:wasAssociatedWith # Activity associated with Agent
prov:actedOnBehalfOf  # Agent acting for another Agent
prov:wasDerivedFrom   # Entity derived from Entity
```

### 17.6 Event as PROV-O Activity

```turtle
# Our Event primitive expressed in PROV-O
:OrderPlacedEvent a prim:Event, prov:Activity ;
    prov:startedAtTime "2025-01-15T10:30:00Z"^^xsd:dateTime ;
    prov:endedAtTime "2025-01-15T10:30:01Z"^^xsd:dateTime ;
    prov:wasAssociatedWith :Customer456 ;     # Actor
    prov:generated :Order123 ;                 # Created Entity
    prov:used :ShoppingCart789 .               # Consumed Resource

:Order123 a prim:Entity, prov:Entity ;
    prov:wasGeneratedBy :OrderPlacedEvent ;
    prov:wasAttributedTo :Customer456 .

:Customer456 a prim:Actor, prov:Agent .
```

### 17.7 Complete W3C Standards Map

| W3C Standard | Primitive Coverage | Purpose |
|--------------|-------------------|---------|
| **OWL-Time** | Time, Duration, DateRange | Temporal modeling |
| **PROV-O** | Event, Actor, Entity | Provenance & causation |
| **FOAF** | Actor (Person, Organization) | Social/agent modeling |
| **Schema.org** | Entity, Action, Event | Web semantics |
| **SKOS** | State (as concepts) | Taxonomies & enums |
| **SHACL** | Constraints, Validation | Shape validation |
| **GeoSPARQL** | Space primitives | Spatial queries |
| **QUDT** | Quantity, Unit | Units of measure |

### 17.8 Namespace Declarations

```turtle
# Standard prefixes for primitive ontology
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:    <http://www.w3.org/2002/07/owl#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix time:   <http://www.w3.org/2006/time#> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix foaf:   <http://xmlns.com/foaf/0.1/> .
@prefix schema: <https://schema.org/> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix geo:    <http://www.opengis.net/ont/geosparql#> .
@prefix qudt:   <http://qudt.org/schema/qudt/> .

# Our primitives
@prefix prim:   <http://protoflow.ai/primitives#> .
```

### 17.9 Time-Aware Event Sourcing Pattern

```turtle
# Event with full temporal context
:OrderPaidEvent a prim:Event, prov:Activity ;
    # When it occurred (OWL-Time)
    time:hasTime [
        a time:Instant ;
        time:inXSDDateTimeStamp "2025-01-15T14:30:00Z"^^xsd:dateTimeStamp
    ] ;

    # Provenance (PROV-O)
    prov:wasAssociatedWith :PaymentGateway ;
    prov:used :PaymentMethod123 ;

    # State transition
    prim:fromState :OrderPending ;
    prim:toState :OrderPaid ;

    # Domain context
    prim:concerns :Order123 ;
    prim:payload [
        a prim:PaymentPayload ;
        prim:amount "99.99"^^xsd:decimal ;
        prim:currency "USD"
    ] .

# Temporal relation between events
:OrderPaidEvent time:after :OrderPlacedEvent .
:OrderShippedEvent time:after :OrderPaidEvent .
```

### 17.10 QUDT for Quantity Primitive

```turtle
@prefix qudt: <http://qudt.org/schema/qudt/> .
@prefix unit: <http://qudt.org/vocab/unit/> .

# Map our Quantity to QUDT
prim:Quantity rdfs:subClassOf qudt:QuantityValue .

:orderTotal a prim:Quantity, qudt:QuantityValue ;
    qudt:numericValue "99.99"^^xsd:decimal ;
    qudt:unit unit:USD .

:packageWeight a prim:Quantity, qudt:QuantityValue ;
    qudt:numericValue "2.5"^^xsd:decimal ;
    qudt:unit unit:KiloGM .
```

### 17.11 GeoSPARQL for Space Primitive

```turtle
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix sf: <http://www.opengis.net/ont/sf#> .

# Map our Space primitives to GeoSPARQL
prim:Point rdfs:subClassOf sf:Point .
prim:Polygon rdfs:subClassOf sf:Polygon .
prim:GeoLocation rdfs:subClassOf geo:Geometry .

:deliveryLocation a prim:GeoLocation, sf:Point ;
    geo:asWKT "POINT(-122.4194 37.7749)"^^geo:wktLiteral .

# Spatial query example (GeoSPARQL)
# Find orders within 10km of location
SELECT ?order WHERE {
    ?order prim:deliveryLocation ?loc .
    ?loc geo:sfWithin ?zone .
    FILTER(geo:distance(?loc, ?center) < 10000)
}
```

---

## 18. Implementation Roadmap

### 18.1 Phase 1: Core Primitives (Complete)
- [x] Entity, State, Event schemas
- [x] Relation, Quantity schemas
- [x] Actor, Intent, Tool, Resource schemas
- [x] Framework documentation

### 18.2 Phase 2: W3C Alignment
- [ ] Generate OWL ontology files (.ttl)
- [ ] Map to OWL-Time for temporal primitives
- [ ] Map to PROV-O for events
- [ ] Map to QUDT for quantities
- [ ] Map to GeoSPARQL for spatial

### 18.3 Phase 3: Tooling
- [ ] YAML → RDF/OWL generator
- [ ] SHACL shape generator
- [ ] TypeScript type generator
- [ ] JSON-LD context generator

### 18.4 Phase 4: Validation
- [ ] SHACL validation for all primitives
- [ ] Cross-primitive consistency rules
- [ ] Integration tests with reasoners

---

*Document Version: 1.4.0*
*Created: 2025-11-27*
*Updated: 2025-11-27 - Added RDF/Graph foundation, Category theory*
*Author: Domain Model Decomposition Initiative*
