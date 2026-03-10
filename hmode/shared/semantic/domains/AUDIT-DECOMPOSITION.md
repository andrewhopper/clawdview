# Domain Model Decomposition Audit

**Date:** 2025-11-27
**Auditor:** Claude (via audit request)
**Scope:** All 60+ domains in `shared/semantic/domains/`

---

## Executive Summary

The current domain model contains **~60 domains** with **500+ entities**. Analysis reveals significant opportunity for decomposition into two fundamental primitives:

1. **Events** - Immutable facts that happened (subject + happened_at + payload)
2. **Properties** - Attributes of things (subject + property + value + validity)

**Key Insight:** Current "entities" often conflate state snapshots with history. By decomposing into Events + Properties, we gain:
- Temporal queries ("what was X at time T?")
- Audit trails (automatic)
- Event sourcing compatibility
- Cleaner CQRS separation

---

## The Two Primitives Model

### 1. Event (Something That Happened)

```yaml
Event:
  id: string           # unique event ID
  subject_id: string   # what this happened to
  subject_type: string # type of subject
  happened_at: datetime
  event_type: string   # e.g., "BookingCreated", "PositionRecorded"
  payload: object      # event-specific data
  metadata:
    correlation_id: string
    causation_id: string
    actor_id: string   # who/what caused this
    source: string
```

**Characteristics:**
- Immutable (never change, only append)
- Past tense naming: "Created", "Updated", "Deleted", "Occurred"
- Contains minimal payload (just the facts)

### 2. Property (Attribute of Something)

```yaml
Property:
  subject_id: string
  subject_type: string
  property_name: string
  value: any
  value_type: string
  valid_from: datetime
  valid_until: datetime?  # null = current
  source_event_id: string?
```

**Characteristics:**
- Bitemporal (when valid + when recorded)
- Can be derived from events
- Enables "as-of" queries

---

## Current State Analysis

### Well-Decomposed Domains ✅

These already follow the Event + Property pattern well:

| Domain | Why It Works |
|--------|--------------|
| `tracking-position` | Position = "thing at place at time" (event) |
| `economic-exchange` | Exchange = "value transferred at time" (event) |
| `events` | Pure event infrastructure |
| `core` | Value objects (Money, Duration, Quantity) |

### Needs Decomposition ⚠️

These conflate state with history:

#### 1. **booking** domain

**Current:** `Booking` entity with 50+ fields including status flags

```yaml
# Current - problematic
Booking:
  status: BookingStatus
  confirmed_at: datetime
  checked_in: boolean
  checked_in_at: datetime
  checked_out: boolean
  checked_out_at: datetime
  canceled_at: datetime
  # ... 40+ more fields mixing state and history
```

**Proposed Decomposition:**

```yaml
# Events (things that happened)
BookingRequested:
  booking_id: string
  customer_id: string
  resource_id: string
  requested_start: datetime
  requested_end: datetime

BookingConfirmed:
  booking_id: string
  confirmed_by: string
  confirmation_code: string

BookingCheckedIn:
  booking_id: string
  checked_in_by: string

BookingCheckedOut:
  booking_id: string

BookingCanceled:
  booking_id: string
  reason: string
  canceled_by: string

BookingRescheduled:
  booking_id: string
  new_start: datetime
  new_end: datetime
  reason: string

# Properties (current state derived from events)
BookingProperties:
  booking_id: string
  customer_name: string   # denormalized
  resource_name: string   # denormalized
  notes: string
  special_requests: string
```

**State derived from events:**
```
status = last(BookingRequested → Confirmed → CheckedIn → CheckedOut | Canceled)
checked_in = exists(BookingCheckedIn where booking_id = X)
```

#### 2. **workflow** domain

**Current:** `WorkflowInstance` with status fields

**Proposed Events:**
- WorkflowStarted
- StepEntered
- StepCompleted
- StepDelegated
- ApprovalRequested
- ApprovalDecided
- WorkflowCompleted
- WorkflowCanceled
- StepEscalated

#### 3. **community** domain

**Current:** `CommunityMember` with role/status

**Proposed Events:**
- MemberJoined
- MemberLeft
- RoleAssigned
- RoleRevoked
- MemberBanned
- BanLifted
- MemberMuted
- MemberUnmuted

#### 4. **subscription/membership** domain

**Current:** `Subscription` with status

**Proposed Events:**
- SubscriptionCreated
- SubscriptionActivated
- SubscriptionPaused
- SubscriptionResumed
- SubscriptionCanceled
- SubscriptionRenewed
- PlanChanged
- PaymentReceived
- PaymentFailed

#### 5. **tracking-asset** domain

**Current:** `TrackedAsset` with status

**Proposed Events:**
- AssetRegistered
- AssetActivated
- AssetDeactivated
- TrackerAttached
- TrackerDetached
- AssetTransferred (custody)
- MaintenanceStarted
- MaintenanceCompleted

#### 6. **vehicle** domain

**Current:** `VehicleHistory` is good, but base `Vehicle` conflates

**Proposed Events:**
- VehicleRegistered
- OwnershipTransferred
- AccidentRecorded
- ServicePerformed
- RecallIssuedForVehicle
- RecallCompleted
- TitleIssued
- StatusChanged

---

## Pattern: State as Event Projection

Current entities become **projections** (materialized views):

```
┌─────────────┐
│   Events    │ ──────> │ Projector │ ──────> │  Read Model  │
│  (append)   │         │           │         │  (derived)   │
└─────────────┘         └───────────┘         └──────────────┘

BookingCreated ─┐
BookingConfirmed─┼──> BookingProjector ──> Booking (current state)
BookingCheckedIn─┘
```

---

## Implementation Strategy

### Phase 1: Core Event Infrastructure ✅
Already done: `events/` domain has DomainEvent, EventMetadata, etc.

### Phase 2: Define Domain Events
For each domain, identify events (past-tense verbs):
- What can be **created**?
- What can be **changed**?
- What can **happen** to it?

### Phase 3: Extract Properties
Identify stable attributes that aren't events:
- Names, descriptions
- Configuration settings
- Denormalized lookup data

### Phase 4: Create Projections
Define how current state is derived from event stream.

---

## Benefits of Decomposition

| Benefit | Description |
|---------|-------------|
| **Audit Trail** | Every change recorded as event |
| **Time Travel** | "What was status on Jan 1?" |
| **Debugging** | Replay events to understand state |
| **CQRS** | Separate write (events) from read (projections) |
| **Simpler Schema** | Small, focused event types |
| **Integration** | Events easy to publish/subscribe |
| **Undo/Compensate** | Issue compensating events |

---

## Anti-Patterns to Avoid

### 1. Event as State Change
❌ `StatusChanged { old: X, new: Y }`
✅ `BookingCanceled`, `BookingConfirmed` (semantic events)

### 2. CRUD Events
❌ `BookingUpdated { fields: [...] }`
✅ `BookingRescheduled`, `NotesAdded` (intent-revealing)

### 3. Derived Data in Events
❌ Event contains computed fields
✅ Event contains only facts; derivation happens in projector

### 4. Missing Context
❌ `StatusChanged` (what caused it?)
✅ `BookingCanceledByCustomer`, `BookingCanceledByAdmin`

---

## Recommended New Domains

### `event-types` domain
Central catalog of all domain events with schemas.

### `projections` domain
Defines how read models are derived from events.

### `property-history` domain
If needed: bitemporal property tracking separate from events.

---

## Next Steps

1. **Prioritize domains** - Start with most actively used
2. **Define event schemas** - Formal YAML definitions per domain
3. **Build event store** - Choose implementation (EventStoreDB, Kafka, etc.)
4. **Create projectors** - Code that builds read models from events
5. **Migrate gradually** - New features use events; backfill historical

---

## Appendix: Domain Classification

| Domain | Type | Decomposition Priority |
|--------|------|----------------------|
| booking | Entity-heavy | HIGH |
| workflow | Event candidate | HIGH |
| membership | State-heavy | HIGH |
| community | Role/status heavy | MEDIUM |
| tracking-asset | Already good | LOW |
| tracking-position | Event-native ✅ | NONE |
| economic-exchange | Event-native ✅ | NONE |
| core | Value objects ✅ | NONE |
| events | Infrastructure ✅ | NONE |
| finance | Transaction = event | MEDIUM |
| auth | Session events | MEDIUM |
| notification | Already events | LOW |

---

## Summary

**Core Principle:** Everything is either:
- An **Event**: Something that happened (immutable, timestamped)
- A **Property**: Current attribute of something (derived or stable)

**State = f(events)** - Current state is always derivable from event history.

This decomposition aligns with:
- Event Sourcing (Greg Young)
- Temporal databases (bitemporal modeling)
- Domain-Driven Design (domain events)
- Fact-based modeling (SBVR, ORM2)

The current model is functional but conflates "what is" with "what happened." Decomposing into Events + Properties provides better auditability, temporal queries, and system integration.
