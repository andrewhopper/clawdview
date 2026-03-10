# /generate-domain - Generate Domain Model Types

Generate language-specific types from W3C RDF/OWL domain models.

## Usage

```bash
/generate-domain <domain> [options]
```

## Arguments

- `<domain>` - Domain name (email, crm, calendar, task, etc.)

## Options

- `--lang <languages>` - Comma-separated languages (typescript, rust, python, go)
  - Default: typescript
  - Example: `--lang typescript,rust,python`

- `--entities <names>` - Create new domain with entities (comma-separated)
  - Example: `--entities Contact,Account,Opportunity`

- `--actions <names>` - Actions for new domain (comma-separated)
  - Example: `--actions CreateContact,UpdateAccount,DeleteOpportunity`

- `--validate` - Validate ontology without generating types

- `--bump-version <level>` - Bump semantic version (major, minor, patch)
  - Example: `--bump-version minor`

- `--changelog <message>` - Changelog message for version bump
  - Example: `--changelog "Add BCC field to Email entity"`

- `--list` - List all available domains

## Examples

### Generate TypeScript types for email domain

```bash
/generate-domain email --lang typescript
```

**Output:**
```
✓ Parsed ontology: @semantic/domains/email/ontology.ttl
✓ Extracted 5 entities, 1 enum
✓ Generated TypeScript types: @semantic/domains/email/generated/typescript/email.types.ts
```

### Generate types for multiple languages

```bash
/generate-domain email --lang typescript,rust,python
```

**Output:**
```
✓ Parsed ontology: @semantic/domains/email/ontology.ttl
✓ Extracted 5 entities, 1 enum
✓ Generated TypeScript: email.types.ts
✓ Generated Rust: email.rs
✓ Generated Python: email.py
```

### Create new CRM domain

```bash
/generate-domain crm --entities Contact,Account,Opportunity --actions CreateContact,UpdateAccount
```

**Output:**
```
✓ Created domain: @semantic/domains/crm/
✓ Generated ontology: crm/ontology.ttl (3 entities, 2 actions)
✓ Generated SHACL rules: crm/rules.shacl.ttl
✓ Generated version.json: crm/version.json (v1.0.0)
✓ Generated README: crm/README.md
✓ Generated TypeScript types: crm/generated/typescript/crm.types.ts
```

### Validate email domain ontology

```bash
/generate-domain email --validate
```

**Output:**
```
✓ Valid Turtle syntax
✓ Found 5 owl:Class definitions
✓ Found 1 owl:oneOf enumeration
✓ SHACL constraints valid
✓ version.json present (v1.0.0)
```

### Bump version after adding field

```bash
/generate-domain email --bump-version minor --changelog "Add BCC field to Email entity"
```

**Output:**
```
✓ Version bumped: 1.0.0 → 1.1.0
✓ Changelog updated
✓ Updated version.json
⚠ Remember to regenerate types: /generate-domain email --lang typescript,rust,python
```

### List all domains

```bash
/generate-domain --list
```

**Output:**
```
Available domains:

email (v1.0.0)
  Entities: Email, Folder, Attachment, Thread, Inbox
  Languages: typescript, rust, python
  Actions: SendEmail, DeleteEmail, ForwardEmail, MarkAsRead, Archive, Search

crm (v1.2.3)
  Entities: Contact, Account, Opportunity
  Languages: typescript, python
  Actions: CreateContact, UpdateContact, DeleteContact
```

## Workflow

### Step 1: Define Domain (Manual or AI-Generated)

**Option A: Manual (for full control)**

```turtle
# shared/domain-models/calendar/ontology.ttl
@prefix calendar: <http://protoflow.ai/domain/calendar#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

calendar:Event a owl:Class ;
    rdfs:label "Calendar Event" ;
    rdfs:comment "Scheduled event with date, time, location" .

calendar:title a owl:DatatypeProperty ;
    rdfs:domain calendar:Event ;
    rdfs:range xsd:string .
```

**Option B: AI-Generated (for speed)**

```bash
/generate-domain calendar --entities Event,Reminder --actions CreateEvent,UpdateEvent,DeleteEvent
```

AI generates complete ontology, SHACL rules, version.json, README.

### Step 2: Generate Types

```bash
/generate-domain calendar --lang typescript,rust,python
```

### Step 3: Use in Applications

**TypeScript app:**

```typescript
import { Event, EventStatus } from '@shared/domain-models/calendar/generated/typescript';

const event: Event = {
  id: '123',
  title: 'Team Meeting',
  startTime: new Date('2025-11-22T10:00:00Z'),
  endTime: new Date('2025-11-22T11:00:00Z'),
  status: EventStatus.Confirmed,
};
```

**Rust app:**

```rust
use shared::domain_models::calendar::*;

let event = Event {
    id: "123".to_string(),
    title: "Team Meeting".to_string(),
    start_time: Utc.ymd(2025, 11, 22).and_hms(10, 0, 0),
    end_time: Utc.ymd(2025, 11, 22).and_hms(11, 0, 0),
    status: EventStatus::Confirmed,
};
```

## AI Instructions

When user runs `/generate-domain <domain>`:

**If domain exists:**

1. Read ontology: `shared/domain-models/{domain}/ontology.ttl`
2. Parse RDF/OWL with N3.js
3. Extract entities, properties, enums, actions
4. Generate types using templates
5. Write to `generated/{lang}/` directories
6. Report success

**If domain does not exist and --entities provided:**

1. Generate ontology from entities + actions
2. Generate SHACL constraints
3. Generate version.json (v1.0.0)
4. Generate README.md
5. Generate types
6. Report success

**If --validate flag:**

1. Parse ontology, check syntax
2. Validate SHACL constraints
3. Check version.json present
4. Report validation results

**If --bump-version flag:**

1. Read current version from version.json
2. Bump version (major.minor.patch)
3. Add changelog entry
4. Write updated version.json
5. Remind user to regenerate types

**If --list flag:**

1. Scan `shared/domain-models/` for domains
2. Read version.json for each
3. Display table with entities, versions, languages

## Implementation Details

**Parser:** `hmode/shared/tools/domain-generator/src/parser.ts`
- Uses N3.js to parse Turtle files
- Extracts owl:Class → entities
- Extracts owl:DatatypeProperty → properties
- Extracts owl:oneOf → enums
- Extracts SHACL constraints

**Generators:** `hmode/shared/tools/domain-generator/src/generators/`
- TypeScript: Interfaces + enums + validation helpers
- Rust: Structs + enums + serde derives
- Python: Pydantic models + enums

**Templates:** `hmode/shared/tools/domain-generator/templates/`
- Handlebars templates for each language
- Variables: entities, properties, enums, constraints

## Technical Details

**W3C Standards Used:**
- RDF (Resource Description Framework)
- OWL (Web Ontology Language)
- SHACL (Shapes Constraint Language)
- Turtle (Terse RDF Triple Language)

**Type Mappings:**

| XSD Type | TypeScript | Rust | Python |
|----------|------------|------|--------|
| xsd:string | string | String | str |
| xsd:integer | number | i64 | int |
| xsd:boolean | boolean | bool | bool |
| xsd:dateTime | Date | DateTime<Utc> | datetime |
| xsd:decimal | number | f64 | float |

**SHACL Constraint Mappings:**

| SHACL | TypeScript | Rust | Python |
|-------|------------|------|--------|
| sh:minLength | // min | // min | min_length |
| sh:maxLength | // max | // max | max_length |
| sh:pattern | // regex | // regex | regex |
| sh:minCount | required | required | required |
| sh:maxCount | array | Vec<T> | list |

## Benefits

**Single Source of Truth:**
- Define domain once in RDF/OWL
- Generate types for any language
- Business rules in SHACL (enforced)

**Language Agnostic:**
- TypeScript email client
- Rust CRM backend
- Python workflow automation
- All use same Email domain model

**Semantic Versioning:**
- Breaking changes → major bump
- New entities/fields → minor bump
- Bug fixes → patch bump
- Applications see type errors on breaking changes

**Standards-Based:**
- W3C RDF/OWL (interoperable)
- SHACL validation (machine-readable)
- Semantic web compatible
- Can query with SPARQL

## Troubleshooting

**Error: "Domain not found"**
- Domain directory doesn't exist
- Create with: `/generate-domain <domain> --entities Entity1,Entity2`

**Error: "Invalid Turtle syntax"**
- Check ontology.ttl syntax
- Validate at: https://www.w3.org/RDF/Validator/
- Check prefix declarations

**Error: "SHACL validation failed"**
- Check SHACL shapes reference correct classes
- Validate shapes syntax

**Generated code doesn't compile**
- Check type mappings (XSD → target language)
- Manually inspect generated file
- Report issue for template fix

## Related Documentation

- Domain Models README: `shared/domain-models/README.md`
- Email Domain Example: `shared/domain-models/email/README.md`
- Generator README: `hmode/shared/tools/domain-generator/README.md`
- Semantic Layer Vision: `shared/semantic-layer/VISION.md`

## Future Enhancements

- GraphQL schema generation
- JSON Schema generation
- Database migration generation (Prisma, SQLx)
- REST API generation (OpenAPI)
- gRPC service definition generation
- Automated testing generation
