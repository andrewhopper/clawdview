# Gift-Giving Domain: Observations & Potential Improvements

**Created:** 2025-11-25
**Domain Version:** 1.1.0

---

## 1. Observations from Domain Model Design

### 1.1 Strengths of Composition Approach

| Observation | Impact |
|-------------|--------|
| **70% reuse** - 7 existing domains (core, calendar, finance, notification, messaging, social-media, auth) provide foundation | Reduces development time, ensures consistency |
| **Clean separation** - Gift-giving logic isolated from payment, calendar, notification concerns | Easier testing, swappable implementations |
| **Cross-domain FK pattern** - Using `type: Money, from: core` makes dependencies explicit | Self-documenting, tooling can validate |
| **Consistent audit fields** - All entities have `createdAt`/`updatedAt` per Rule #18 | Temporal queries work uniformly |

### 1.2 Design Decisions Made

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| Separate `GiftRecipient` from `core:Person` | Gift-specific preferences (sizes, interests, allergies) | Potential data duplication if Person already exists |
| `WishlistClaim` audit entity | Track claim/unclaim history for group coordination | Extra storage, but enables "who claimed what when" |
| `OccasionType` as enum vs. freetext | Type safety, enables occasion-specific logic | Limited extensibility (mitigated by `custom` value) |
| Nested `ClothingSizes` value object | Group related sizes together | Could be separate entity if sizes need history |

### 1.3 Patterns Identified

```
┌─────────────────────────────────────────────────────────────────┐
│ PATTERN: Hidden State Anti-Pattern                             │
├─────────────────────────────────────────────────────────────────┤
│ WishlistItem.claimedById is "hidden from owner"                │
│                                                                 │
│ Problem: Business logic in data model comments                  │
│ Better: Separate "gift-giver view" vs "recipient view" at API  │
│ Action: Consider ViewModels/DTOs for role-based visibility     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PATTERN: Lifecycle State Machine                                │
├─────────────────────────────────────────────────────────────────┤
│ GiftStatus: idea → saved → purchased → shipped → delivered     │
│                                                                 │
│ Observation: This is a state machine, not just an enum         │
│ Consider: workflow domain integration for complex transitions  │
│ Action: Add valid transitions documentation or state machine   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Potential Improvements

### 2.1 Missing Entities (Discovered During Design)

| Entity | Description | Priority |
|--------|-------------|----------|
| `GiftRegistry` | Wedding/baby registry (aggregates wishlists) | Medium |
| `ReturnLabel` | For easy gift returns | Low |
| `GiftReceipt` | Receipt without price for recipient | Medium |
| `ShippingOption` | Carrier, speed, cost options | Medium |
| `GiftTag` | Digital gift tag/card content | Low |
| `RecipientPreferenceHistory` | Track preference changes over time | Low |

### 2.2 Cross-Domain Integration Gaps

| Gap | Current State | Improvement |
|-----|---------------|-------------|
| **Product catalog** | `purchaseUrl` is just a URL | Consider product domain for retailer integration |
| **Inventory checking** | No inventory awareness | API integration for real-time availability |
| **Price tracking** | Single `price` snapshot | Price history, alerts when price drops |
| **Social sharing** | References `social-media:Post` | Dedicated "gift received" post type |
| **Voice/TTS** | No audio integration | Voice thank-you notes via TTS domain |

### 2.3 Schema Improvements

```yaml
# IMPROVEMENT 1: Add state machine transitions
# Current: GiftStatus is just an enum
# Better: Define valid transitions

state_machines:
  GiftStatusMachine:
    initial: idea
    transitions:
      - from: idea, to: [saved, purchased]
      - from: saved, to: [purchased, idea]  # Can go back
      - from: purchased, to: [wrapped, shipped]
      - from: wrapped, to: [shipped, given]
      - from: shipped, to: delivered
      - from: delivered, to: given
      - from: given, to: [received, thanked]
      - from: received, to: thanked

# IMPROVEMENT 2: Add computed fields
# Current: Stats are stored
# Better: Define as computed

computed_fields:
  Wishlist.fulfillmentRate:
    formula: "(claimedCount / itemCount) * 100"
    type: percentage
  GroupGift.fundingProgress:
    formula: "(currentAmount / targetAmount) * 100"
    type: percentage

# IMPROVEMENT 3: Add validation rules
# Current: No validation
# Better: SHACL-like constraints

constraints:
  - entity: GroupGiftContribution
    rule: "amount >= groupGift.minimumContribution"
    message: "Contribution below minimum"

  - entity: WishlistItem
    rule: "claimedById != wishlist.ownerId"
    message: "Cannot claim own wishlist item"

  - entity: ExchangeParticipant
    rule: "assignedToUserId NOT IN exclusions"
    message: "Cannot be matched with excluded person"
```

### 2.4 Performance Considerations

| Concern | Current Design | Optimization |
|---------|----------------|--------------|
| Wishlist item counts | Stored as `itemCount`, `claimedCount` | Keep denormalized, update via triggers |
| Occasion reminders | Scheduled per-user | Batch processing, send in timezone-aware batches |
| Gift search | Tags as array | Consider tag entity for indexing |
| Image storage | Direct URLs | CDN + thumbnails for mobile performance |

### 2.5 Mobile-Specific Observations

```
┌─────────────────────────────────────────────────────────────────┐
│ MOBILE APP CONSIDERATIONS                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. Offline-first wishlist editing                               │
│    - Need: Conflict resolution for claim races                  │
│    - Add: `version` field for optimistic locking                │
│                                                                 │
│ 2. Push notification payloads                                   │
│    - Need: Structured deep links for each notification type     │
│    - Add: Action enum with deep link templates                  │
│                                                                 │
│ 3. Image optimization                                           │
│    - Need: Multiple image sizes for list vs. detail views       │
│    - Add: `thumbnailUrl`, `mediumUrl`, `fullUrl` pattern        │
│                                                                 │
│ 4. Barcode/QR scanning                                          │
│    - Need: Quick add from product barcode                       │
│    - Add: `barcode`, `upc`, `sku` fields to WishlistItem        │
│                                                                 │
│ 5. Sharing URLs                                                 │
│    - Need: Universal links / deep links                         │
│    - Add: `shareToken` pattern already in Wishlist ✓            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Registry Pattern Observations

### 3.1 What Works Well

1. **Centralized registry.yaml** - Single source of truth for all domains
2. **Version tracking** - Each domain has version for breaking changes
3. **Dependency declaration** - Explicit `dependencies: [core, calendar]`
4. **Status field** - `production`, `development`, `deprecated` lifecycle
5. **Source attribution** - Links to external specs (Twilio, RFC, etc.)

### 3.2 Improvement Opportunities

| Current | Improvement |
|---------|-------------|
| No schema validation | Add JSON Schema or SHACL validation for registry |
| Manual entity listing | Auto-generate from schema.yaml files |
| No API versioning | Add `api_version` for breaking changes |
| No deprecation dates | Add `deprecated_at`, `sunset_date` for deprecated domains |
| No example usage | Add `examples/` folder with usage snippets |

---

## 4. Code Generation Opportunities

### 4.1 TypeScript Generation

```typescript
// From schema.yaml → generated TypeScript
// File: shared/semantic/domains/gift-giving/generated/typescript/index.ts

import { Money, Address, Recurrence } from '@shared/semantic/domains/core';
import { Event } from '@shared/semantic/domains/calendar';
import { Payment } from '@shared/semantic/domains/finance';

export interface Gift {
  id: string;
  title: string;
  description?: string;
  gifterId?: string;
  recipientId: string;
  status: GiftStatus;
  estimatedPrice?: Money;
  // ... generated from schema
  createdAt: Date;
  updatedAt: Date;
}

export type GiftStatus =
  | 'idea'
  | 'saved'
  | 'purchased'
  // ... generated from enum
```

### 4.2 Zod Validation Generation

```typescript
// Generated Zod schema for runtime validation
import { z } from 'zod';

export const GiftSchema = z.object({
  id: z.string().uuid(),
  title: z.string().max(200),
  recipientId: z.string(),
  status: GiftStatusSchema,
  // ...
});
```

### 4.3 API Route Generation

```typescript
// Generated tRPC/REST routes from actions
export const giftRouter = router({
  create: protectedProcedure
    .input(CreateGiftSchema)
    .mutation(/* ... */),
  updateStatus: protectedProcedure
    .input(UpdateGiftStatusSchema)
    .mutation(/* ... */),
});
```

---

## 5. Testing Recommendations

### 5.1 Domain Invariant Tests

```yaml
invariants:
  - name: "Wishlist owner cannot claim own items"
    test: |
      Given a wishlist owned by User A
      When User A tries to claim an item
      Then error SELF_CLAIM should be raised

  - name: "Group gift cannot exceed target"
    test: |
      Given a group gift with target $100
      When contributions total $100
      Then status should be 'funded'
      And new contributions should be rejected

  - name: "Exchange matching respects exclusions"
    test: |
      Given User A excludes User B
      When matching algorithm runs
      Then User A should not be assigned to User B
```

### 5.2 Integration Tests Needed

| Test | Domains Involved |
|------|------------------|
| Occasion creates calendar event | gift-giving + calendar |
| Reminder triggers notification | gift-giving + notification |
| Contribution processes payment | gift-giving + finance |
| Thank-you sends message | gift-giving + messaging |

---

## 6. Action Items

### 6.1 Immediate (This Session)

- [x] Create schema.yaml
- [x] Document observations
- [x] Update registry.yaml
- [x] Add barcode/UPC fields for mobile scanning
- [x] Integrate with linking domain (deep links, product links)
- [x] Integrate with data-sync domain (offline support)

### 6.2 Future Improvements

- [ ] Add `GiftRegistry` entity for wedding/baby registries
- [ ] Add state machine validation
- [ ] Create TypeScript generator
- [ ] Add SHACL validation rules
- [ ] Create example API implementations

---

## 7. New Domain Integrations (v1.1.0)

### 7.1 linking Domain Integration

Added deep links and product links to gift-giving:

```yaml
# Wishlist now has deep link and QR code for sharing
Wishlist:
  deepLinkId: { type: uuid, description: "FK to linking:DeepLink" }
  qrCodeId: { type: uuid, description: "FK to linking:QRCode" }

# WishlistItem links to ProductLink for rich product data
WishlistItem:
  productLinkId: { type: uuid, description: "FK to linking:ProductLink" }
  barcode: { type: string }
  barcodeFormat: { type: BarcodeFormat }
  upc: { type: string }
  ean: { type: string }
  asin: { type: string }
```

**Use Cases:**
- Share wishlist via deep link that opens in app
- Generate QR code for physical gift cards/invites
- Import product details from barcode scan
- Track affiliate/referral links for product purchases

### 7.2 data-sync Domain Integration

Added offline sync support:

```yaml
# All major entities now have sync versioning
Wishlist:
  syncVersion: { type: integer, default: 0 }
  lastSyncedAt: { type: datetime }

WishlistItem:
  syncVersion: { type: integer, default: 0 }
  lastSyncedAt: { type: datetime }
```

**Sync Architecture:**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Mobile App     │────▶│  data-sync      │────▶│  Backend        │
│                 │     │                 │     │                 │
│ WishlistItem    │     │ SyncStream      │     │ WishlistItem    │
│ (local SQLite)  │     │ ConflictPolicy  │     │ (PostgreSQL)    │
│                 │◀────│ OfflineQueue    │◀────│                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Conflict Resolution:**
- `latest_wins` - Most recent timestamp wins (default for wishlist edits)
- `source_wins` - Server always wins (for claims - avoid double-buying)
- `manual` - Prompt user for major conflicts

### 7.3 Reusability of data-sync

The data-sync domain is designed to be reused across ANY data movement scenario:

| Use Case | Source | Target | Sync Mode |
|----------|--------|--------|-----------|
| Mobile offline | SQLite | PostgreSQL | bidirectional |
| Email archive | IMAP/Exchange | S3/Analytics | source_to_target |
| Analytics ETL | PostgreSQL | Snowflake | incremental CDC |
| Multi-region | DynamoDB (us-east) | DynamoDB (eu-west) | bidirectional |
| Event sourcing | Kafka | PostgreSQL | streaming CDC |

**Example: Email Replication**
```yaml
SyncStream:
  name: "email-archive"
  sourceId: exchange_endpoint
  targetId: s3_archive_endpoint
  entityType: "email:Email"
  syncPolicy:
    mode: incremental
    direction: source_to_target
    frequency: near_realtime
  conflictPolicy:
    strategy: source_wins  # Exchange is authoritative
```

---

## 8. Summary

**Domain Composition Score: 9/10** (up from 8/10)

| Criteria | Score | Notes |
|----------|-------|-------|
| Reuse of existing domains | 10/10 | Excellent - 9 domains composed |
| Entity completeness | 8/10 | Good - missing registry, returns |
| Enum coverage | 9/10 | Excellent - added BarcodeFormat |
| Action coverage | 8/10 | Good - CRUD + workflows |
| Cross-domain relationships | 10/10 | Excellent - linking + data-sync |
| Mobile readiness | 9/10 | Excellent - barcode + offline sync |

**Key Insight:** The domain model demonstrates how semantic domains compose for real applications. The gift-giving domain adds ~19 entities while reusing ~40+ entities from 9 existing domains. The new `data-sync` and `linking` domains are fully reusable for any application requiring sync or deep linking.
