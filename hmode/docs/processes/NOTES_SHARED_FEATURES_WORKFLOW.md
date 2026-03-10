# Notes & Shared Features Workflow

Standard operating procedure for creating notes, shared features, and domain models with mandatory UUID tracking, GitHub research, and test enforcement.

## 1.0 OVERVIEW

**Purpose:** Ensure all shared elements are properly researched, consistently structured, and validated through tests.

**Mandatory Gates:**
1. **UUID Gate** - Every entity must have UUID identifiers
2. **GitHub Research Gate** - Always check existing solutions first
3. **Test Enforcement Gate** - Tests must verify domain model usage

**Applies To:**
- Notes and documentation with structured data
- Shared features across prototypes
- New domain models
- Extensions to existing domains

---

## 2.0 UUID ENFORCEMENT GATE

### 2.1 Required Fields

**ALL entities MUST include these fields:**

```yaml
entities:
  YourEntity:
    properties:
      id:
        type: uuid
        required: true
        description: "Unique identifier (UUIDv4)"
      created_at:
        type: datetime
        required: true
        auto: true
        description: "Creation timestamp (UTC)"
      updated_at:
        type: datetime
        required: true
        auto: true
        description: "Last modification timestamp (UTC)"
```

### 2.2 UUID Generation Pattern

```typescript
// TypeScript pattern
import { v4 as uuidv4 } from 'uuid';

interface BaseEntity {
  id: string;        // UUIDv4
  created_at: Date;  // Auto-set on create
  updated_at: Date;  // Auto-set on create/update
}

// Python pattern
import uuid
from datetime import datetime, timezone

class BaseEntity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

### 2.3 Validation

**AI MUST verify before approval:**
- [ ] All entities have `id: uuid`
- [ ] All entities have `created_at: datetime`
- [ ] All entities have `updated_at: datetime`
- [ ] No entity uses auto-increment integers for primary keys

---

## 3.0 GITHUB RESEARCH GATE (MANDATORY)

### 3.1 Research Sequence

**BEFORE proposing ANY new domain or shared feature, AI MUST:**

```
Step 1: Schema.org Research
─────────────────────────────
WebSearch: "schema.org [domain] types"
→ Document standard properties
→ Note which types map to your entities

Step 2: GitHub Project Analysis
─────────────────────────────
WebSearch: "[domain] open source github stars:>5000"
→ Identify top 3-5 projects
→ Analyze their data models
→ Note patterns and conventions

Step 3: Provider API Analysis
─────────────────────────────
WebSearch: "[provider] API reference [domain]"
→ Study industry-standard APIs
→ Understand entity lifecycles
→ Note common fields and relationships
```

### 3.2 Research Output Format

**AI MUST present research before proposing:**

```markdown
## Domain Research: [Domain Name]

### Schema.org Findings
| Type | Key Properties | Notes |
|------|----------------|-------|
| [Type] | [properties] | [relevance] |

### GitHub Project Analysis
| Project | Stars | Key Patterns |
|---------|-------|--------------|
| [name] | [count] | [patterns discovered] |

### Provider API Analysis
| Provider | Entity Model | Lifecycle |
|----------|--------------|-----------|
| [name] | [entities] | [states/transitions] |

### Synthesized Recommendations
1. [Key design decision from research]
2. [Pattern to adopt]
3. [Anti-pattern to avoid]

---
**Proceed with domain proposal? [Y/n]**
```

### 3.3 Research Reference Table

| Domain Type | Schema.org | GitHub Projects | Provider APIs |
|-------------|------------|-----------------|---------------|
| E-commerce | Product, Offer, Order | Magento, Medusa, Saleor | Stripe, Shopify |
| Auth | Person, Organization | Keycloak, Auth0 OSS | Auth0, Okta |
| Messaging | Message, EmailMessage | Mattermost, Rocket.Chat | Twilio, SendGrid |
| Finance | Invoice, PaymentMethod | Akaunting, Firefly III | Stripe, Plaid |
| CRM | Person, Organization | SuiteCRM, EspoCRM | Salesforce, HubSpot |
| Calendar | Event, Schedule | Cal.com | Google Calendar |

---

## 4.0 TEST ENFORCEMENT GATE

### 4.1 Test Requirements

**Tests MUST be written BEFORE implementation that:**

1. **Import Verification** - Verify entities are imported from shared domains
2. **Type Enforcement** - Ensure proper types are used (not raw objects)
3. **UUID Validation** - Confirm IDs are valid UUIDs
4. **Timestamp Validation** - Confirm created_at/updated_at exist

### 4.2 Test Patterns

#### 4.2.1 TypeScript/Jest Pattern

```typescript
// tests/domain-model-enforcement.test.ts
import { Email } from '@semantic/domains/email';
import { validate as uuidValidate } from 'uuid';

describe('Domain Model Enforcement', () => {
  describe('Email entity', () => {
    it('should import from shared domain (not local definition)', () => {
      // This test fails if someone defines Email locally
      expect(Email).toBeDefined();
      expect(Email.prototype.constructor.name).toBe('Email');
    });

    it('should have UUID id field', () => {
      const email = new Email({ /* ... */ });
      expect(uuidValidate(email.id)).toBe(true);
    });

    it('should have timestamp fields', () => {
      const email = new Email({ /* ... */ });
      expect(email.created_at).toBeInstanceOf(Date);
      expect(email.updated_at).toBeInstanceOf(Date);
    });
  });
});

// Lint rule: no-local-domain-types
// Add to .eslintrc to prevent local type definitions
```

#### 4.2.2 Python/pytest Pattern

```python
# tests/test_domain_model_enforcement.py
import pytest
import uuid
from datetime import datetime
from shared.semantic.domains.email import Email

class TestDomainModelEnforcement:
    """Ensure domain models are used from shared location."""

    def test_email_imports_from_shared(self):
        """Verify Email is imported from shared domains."""
        assert Email.__module__.startswith('shared.semantic.domains')

    def test_email_has_uuid_id(self):
        """Verify id field is valid UUID."""
        email = Email(subject="Test", body="Test body")
        assert uuid.UUID(email.id, version=4)

    def test_email_has_timestamps(self):
        """Verify timestamp fields exist."""
        email = Email(subject="Test", body="Test body")
        assert isinstance(email.created_at, datetime)
        assert isinstance(email.updated_at, datetime)

    def test_no_local_email_definition(self):
        """Fail if Email is defined locally (import check)."""
        import sys
        email_modules = [m for m in sys.modules if 'email' in m.lower()]
        local_definitions = [m for m in email_modules if not m.startswith('shared')]
        assert len(local_definitions) == 0, f"Local Email definitions found: {local_definitions}"
```

### 4.3 CI/CD Integration

```yaml
# .github/workflows/domain-enforcement.yml
name: Domain Model Enforcement

on: [push, pull_request]

jobs:
  test-domain-models:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check domain imports
        run: |
          # Fail if any file imports from local instead of shared
          grep -r "from \.\./.*models" src/ && exit 1 || true
          grep -r "from '\.\.\/.*types'" src/ && exit 1 || true

      - name: Run domain enforcement tests
        run: |
          npm test -- --grep "Domain Model Enforcement"
          # or: pytest tests/test_domain_model_enforcement.py
```

### 4.4 Pre-Implementation Checklist

**AI MUST verify before implementing:**

- [ ] Tests exist for domain model imports
- [ ] Tests verify UUID format for id fields
- [ ] Tests verify timestamp fields exist
- [ ] No local type definitions bypass shared domains
- [ ] CI pipeline includes domain enforcement checks

---

## 5.0 COMPLETE WORKFLOW

### 5.1 Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. TRIGGER: Need for notes/shared feature/domain                │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. DISCOVERY: Check registry.yaml for existing domains         │
│    → If exists: Use existing, skip to step 6                    │
│    → If not: Continue to step 3                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. GITHUB RESEARCH GATE                                         │
│    → Schema.org research                                        │
│    → GitHub project analysis                                    │
│    → Provider API analysis                                      │
│    → Present research summary                                   │
│    → Human approves research [Y/n]                              │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. UUID ENFORCEMENT GATE                                        │
│    → Verify all entities have: id, created_at, updated_at       │
│    → Present YAML model for approval                            │
│    → Human approves model [Y/R/A/D]                             │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. TEST ENFORCEMENT GATE                                        │
│    → Write domain enforcement tests FIRST                       │
│    → Tests must verify:                                         │
│      • Imports from shared domains                              │
│      • UUID validation                                          │
│      • Timestamp validation                                     │
│    → Tests must PASS before implementation                      │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. IMPLEMENTATION                                               │
│    → Import from @semantic/domains/{domain}/                    │
│    → Generate types if needed                                   │
│    → All tests must pass                                        │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. REGISTRATION                                                 │
│    → Add to registry.yaml                                       │
│    → Update documentation                                       │
│    → Commit to main                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Quick Reference Commands

```bash
# Check existing domains
cat hmode/hmode/shared/semantic/domains/registry.yaml

# Create from template
cp -r hmode/hmode/shared/semantic/domains/_template hmode/hmode/shared/semantic/domains/{name}

# Run domain enforcement tests
npm test -- --grep "Domain Model"
pytest tests/test_domain_model_enforcement.py

# Validate UUIDs in YAML
grep -E "type:\s*uuid" hmode/hmode/shared/semantic/domains/{name}/schema.yaml
```

---

## 6.0 ENFORCEMENT RULES

### 6.1 AI Rules

1. **NEVER** skip GitHub research gate
2. **NEVER** propose entities without UUID fields
3. **NEVER** implement before tests exist
4. **ALWAYS** present research summary before proposing
5. **ALWAYS** verify imports come from shared domains

### 6.2 Human Approval Points

| Gate | Approval Format | Options |
|------|-----------------|---------|
| Research | "Proceed with proposal? [Y/n]" | Y, n |
| UUID/Model | "Approve model? [Y/R/A/D]" | Yes, Revise, Add, Delete |
| Tests | "Tests pass. Proceed? [Y/n]" | Y, n |

### 6.3 Failure Handling

| Failure | Action |
|---------|--------|
| Research finds existing solution | Propose using existing instead of creating new |
| Entity missing UUID | Block until fixed |
| Tests fail | Block implementation until tests pass |
| Local type definition found | Refactor to use shared domain |

---

## 7.0 ANTI-PATTERNS

| Don't | Do Instead |
|-------|------------|
| Skip research "to save time" | Research prevents duplicate work |
| Use auto-increment IDs | Always use UUIDv4 |
| Define types locally | Import from shared domains |
| Write tests after implementation | TDD: tests first |
| Assume domain doesn't exist | Always check registry.yaml |

---

**Last Updated:** 2025-12-05
**Version:** 1.0.0
**Status:** Active
