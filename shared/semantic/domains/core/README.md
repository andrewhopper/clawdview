# Core Primitives Domain

Foundation layer providing reusable primitives for all domain models.

## Purpose

**Don't duplicate - import from core.**

This domain provides common building blocks that every other domain needs:
- Base entity with audit trail
- Person and organization
- Time modeling (points, durations, ranges, recurrence)
- Money and currency
- Addresses and geolocation
- Contact information
- Measurements and quantities
- Media objects
- Status indicators
- External identifiers

## Primitives

### 1. Base Entities

| Entity | Description |
|--------|-------------|
| `Entity` | Base class with id, name, description |
| `AuditInfo` | createdAt, updatedAt, createdBy, version |
| `Individual` | Any identifiable agent |
| `Person` | Human with firstName, lastName, dateOfBirth |
| `Organization` | Company with legalName, taxId |

### 2. Time

| Entity | Description |
|--------|-------------|
| `TimePoint` | Specific moment (timestamp + timezone) |
| `Duration` | Length of time (ISO 8601 or milliseconds) |
| `DateRange` | Period with start and end |
| `Recurrence` | Repeating pattern (RRULE format) |

| Enum | Values |
|------|--------|
| `TimeOfDay` | Morning, Afternoon, Evening, Night |
| `Season` | Spring, Summer, Fall, Winter |
| `LifeStage` | Infant, Child, Adolescent, YoungAdult, Adult, MiddleAge, Senior |
| `RecurrenceFrequency` | Hourly, Daily, Weekly, Monthly, Yearly |

### 3. Money

| Entity | Description |
|--------|-------------|
| `Money` | Amount + currency code |
| `Currency` | ISO 4217 definition (code, symbol, minorUnits) |

### 4. Location

| Entity | Description |
|--------|-------------|
| `Address` | Postal address (line1, city, country, postalCode) |
| `GeoLocation` | Coordinates (latitude, longitude, altitude) |

| Enum | Values |
|------|--------|
| `AddressType` | Home, Work, Billing, Shipping, Mailing |

### 5. Contact

| Entity | Description |
|--------|-------------|
| `ContactInfo` | email, phone, website |

| Enum | Values |
|------|--------|
| `PhoneType` | Mobile, Landline, Fax, Toll-Free |

### 6. Measurement

| Entity | Description |
|--------|-------------|
| `Quantity` | value + unit |
| `Weight` | Quantity subclass |
| `Length` | Quantity subclass |
| `Volume` | Quantity subclass |
| `Temperature` | Quantity subclass |
| `Percentage` | 0-100 value |

| Enum | Values |
|------|--------|
| `UnitSystem` | Metric, Imperial, USCustomary |

### 7. Media

| Entity | Description |
|--------|-------------|
| `MediaObject` | Base (url, mimeType, fileSize) |
| `Image` | width, height |
| `Document` | pageCount |
| `Video` | duration |
| `Audio` | duration |

### 8. Status & Identity

| Entity | Description |
|--------|-------------|
| `Status` | Generic status indicator |
| `Identifier` | External ID (value, type, source) |

| Enum | Values |
|------|--------|
| `GenericStatus` | Active, Inactive, Pending, Archived, Deleted |

## Usage

### In Ontology Files

```turtle
@prefix core: <http://protoflow.ai/ontology/core#> .
@prefix mydom: <http://protoflow.ai/ontology/mydomain#> .

mydom:Order a owl:Class .

mydom:customer a owl:ObjectProperty ;
    rdfs:domain mydom:Order ;
    rdfs:range core:Person .

mydom:total a owl:ObjectProperty ;
    rdfs:domain mydom:Order ;
    rdfs:range core:Money .

mydom:placedAt a owl:ObjectProperty ;
    rdfs:domain mydom:Order ;
    rdfs:range core:TimePoint .

mydom:shippingAddress a owl:ObjectProperty ;
    rdfs:domain mydom:Order ;
    rdfs:range core:Address .
```

### In TypeScript

```typescript
import {
  Person,
  Money,
  TimePoint,
  Address,
  DateRange
} from '@protoflow/semantic/domains/core';

interface Order {
  customer: Person;
  total: Money;
  placedAt: TimePoint;
  shippingAddress: Address;
  deliveryWindow?: DateRange;
}
```

### In Python

```python
from protoflow.semantic.domains.core import (
    Person,
    Money,
    TimePoint,
    Address
)

@dataclass
class Order:
    customer: Person
    total: Money
    placed_at: TimePoint
    shipping_address: Address
```

## Design Principles

1. **Single source of truth** - Define once, use everywhere
2. **Schema.org alignment** - Where applicable, extend schema.org types
3. **ISO standards** - Use ISO 4217 (currency), ISO 8601 (time), ISO 3166 (country)
4. **Validation built-in** - SHACL rules for all constraints
5. **No dependencies** - Core depends on nothing else

## Files

| File | Purpose |
|------|---------|
| `ontology.ttl` | RDF/OWL definitions for all primitives |
| `rules.shacl.ttl` | Validation constraints |
| `version.json` | Metadata and entity list |
| `generated/` | Auto-generated TypeScript/Python/Rust |
