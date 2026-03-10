# Stage 6 - Technical Design

## 1.0 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           domain CLI                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  CLI Layer (Click)                                                      │
│  ┌───────┬───────┬────────┬────────┬──────────┬─────────┬───────────┐  │
│  │ list  │ show  │ search │ create │ validate │ codegen │ analytics │  │
│  └───┬───┴───┬───┴────┬───┴────┬───┴─────┬────┴────┬────┴─────┬─────┘  │
│      │       │        │        │         │         │          │         │
│  ┌───┴───────┴────────┴────────┴─────────┴─────────┴──────────┴───────┐│
│  │                         Core Modules                                ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  ││
│  │  │   Registry   │  │  Knowledge   │  │     Research Agent       │  ││
│  │  │              │  │    Graph     │  │  ┌────────────────────┐  │  ││
│  │  │ - domains    │  │              │  │  │ Schema.org         │  │  ││
│  │  │ - primitives │  │ - rationale  │  │  │ Best-in-class APIs │  │  ││
│  │  │ - search     │  │ - usage      │  │  │ GitHub models      │  │  ││
│  │  └──────────────┘  │ - patterns   │  │  └────────────────────┘  │  ││
│  │                    └──────────────┘  └──────────────────────────┘  ││
│  └────────────────────────────────────────────────────────────────────┘│
│                                    │                                    │
│  ┌─────────────────────────────────┴──────────────────────────────────┐│
│  │                    External Integrations                            ││
│  │  ┌───────────┐ ┌─────────────────┐ ┌───────────┐ ┌───────────────┐ ││
│  │  │ pykwalify │ │ datamodel-code- │ │MCP Server │ │  SQLite Index │ ││
│  │  │(validate) │ │   generator     │ │(AI access)│ │ (knowledge DB)│ ││
│  │  └───────────┘ └─────────────────┘ └───────────┘ └───────────────┘ ││
│  └────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           File System                                    │
│  shared/semantic/domains/                                                │
│  ├── registry.yaml              (domain index)                          │
│  ├── _template/                 (new domain template)                   │
│  ├── _primitives/               (atomic building blocks)                │
│  ├── _references/               (best-in-class API configs)             │
│  ├── _knowledge/                (knowledge graph data)                  │
│  │   ├── graph.db               (SQLite knowledge index)                │
│  │   ├── usage.yaml             (usage analytics)                       │
│  │   └── patterns.yaml          (common patterns library)               │
│  ├── finance/                                                           │
│  │   ├── schema.yaml            (domain schema)                         │
│  │   └── .rationale.yaml        (design rationale)                      │
│  └── ...                                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2.0 Module Structure

```
shared/semantic/domains/cli/
├── pyproject.toml
├── domain_cli/
│   ├── __init__.py
│   ├── cli.py                     # Click entry point
│   ├── registry.py                # Core registry operations (EXISTS)
│   │
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── list_cmd.py            # domain list (EXISTS)
│   │   ├── show.py                # domain show (EXISTS)
│   │   ├── search.py              # domain search (EXISTS)
│   │   ├── create.py              # domain create (REWRITE for gates)
│   │   ├── validate.py            # domain validate (EXISTS)
│   │   ├── codegen.py             # domain codegen (TODO v0.3)
│   │   └── analytics.py           # domain analytics (TODO v0.5)
│   │
│   ├── validation/                # v0.2
│   │   ├── __init__.py
│   │   ├── meta_schema.yaml
│   │   └── validator.py
│   │
│   ├── research/                  # v0.5 - Research Agent
│   │   ├── __init__.py
│   │   ├── api_fetcher.py         # Fetch best-in-class API models
│   │   ├── schema_org.py          # Search schema.org
│   │   ├── github_search.py       # Search GitHub models
│   │   ├── references.yaml        # Best-in-class API config
│   │   └── design_assistant.py    # Suggest compositions
│   │
│   ├── knowledge/                 # v0.5 - Knowledge Graph
│   │   ├── __init__.py
│   │   ├── graph.py               # Knowledge graph operations
│   │   ├── rationale.py           # Rationale capture/query
│   │   ├── usage.py               # Usage analytics
│   │   └── patterns.py            # Pattern library
│   │
│   └── mcp/                       # v0.4
│       ├── __init__.py
│       ├── server.py
│       └── tools.py
│
└── tests/
    ├── __init__.py
    ├── test_registry.py
    ├── test_commands.py
    ├── test_validation.py
    ├── test_research.py
    └── test_knowledge.py
```

---

## 3.0 Component Specifications

### 3.1 Registry Module (v0.1 - EXISTS)

```python
class DomainInfo(BaseModel):
    name: str
    status: str
    version: str
    description: str
    entities: list[str]
    actions: list[str]
    enums: list[str]
    dependencies: list[str]

class Registry:
    def __init__(self, domains_root: Path)
    def list_domains(self, status: str | None) -> list[DomainInfo]
    def get_domain(self, name: str) -> DomainInfo | None
    def search_domains(self, query: str) -> list[DomainInfo]
    def get_domain_schema_path(self, name: str) -> Path | None
    def get_stats(self) -> dict[str, int]
```

### 3.2 Validation Module (v0.2 - TODO)

```python
class DomainValidator:
    def __init__(self, meta_schema_path: Path)
    def validate(self, schema_path: Path) -> ValidationResult
    def validate_all(self) -> list[ValidationResult]

class ValidationResult(BaseModel):
    domain: str
    valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationWarning]
```

### 3.3 Codegen Module (v0.3 - TODO)

```python
@click.command()
@click.argument("name")
@click.option("--output", "-o", type=click.Path())
@click.option("--pydantic-version", type=click.Choice(["v1", "v2"]), default="v2")
def codegen(name: str, output: Path | None, pydantic_version: str):
    """Generate Pydantic models from domain schema."""
```

### 3.4 MCP Server (v0.4 - TODO)

```python
class DomainMCPServer:
    def __init__(self, registry: Registry, knowledge: KnowledgeGraph)

    @tool
    def domain_search(self, query: str) -> list[DomainSummary]

    @tool
    def domain_details(self, name: str) -> DomainDetails

    @tool
    def domain_research(self, concept: str) -> ResearchSummary
        """Research best practices for a domain concept."""
```

### 3.5 Research Agent (v0.5 - TODO)

```python
# domain_cli/research/api_fetcher.py

class APIReference(BaseModel):
    name: str
    docs_url: str
    spec_url: str | None
    models: list[str]

class APIModelFetcher:
    """Fetch and parse data models from best-in-class APIs."""

    SOURCES: dict[str, list[APIReference]] = {
        "payment": [
            APIReference(
                name="Stripe",
                docs_url="https://stripe.com/docs/api",
                spec_url="https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json",
                models=["PaymentIntent", "PaymentMethod", "Charge", "Refund", "Invoice"]
            ),
            APIReference(
                name="Square",
                docs_url="https://developer.squareup.com/reference/square",
                models=["Payment", "Order", "Money"]
            ),
        ],
        "messaging": [
            APIReference(
                name="Twilio",
                docs_url="https://www.twilio.com/docs/api",
                models=["Message", "Call", "Conversation"]
            ),
            APIReference(
                name="SendGrid",
                docs_url="https://docs.sendgrid.com/api-reference",
                models=["Mail", "Contact", "Template"]
            ),
        ],
        "booking": [
            APIReference(
                name="Calendly",
                docs_url="https://developer.calendly.com/api-docs",
                models=["Event", "Invitee", "Availability"]
            ),
        ],
        "auth": [
            APIReference(
                name="Auth0",
                docs_url="https://auth0.com/docs/api",
                models=["User", "Connection", "Token", "Session"]
            ),
            APIReference(
                name="Okta",
                docs_url="https://developer.okta.com/docs/reference",
                models=["User", "Group", "Policy", "Session"]
            ),
        ],
        "crm": [
            APIReference(
                name="Salesforce",
                docs_url="https://developer.salesforce.com/docs/atlas.en-us.api.meta",
                models=["Account", "Contact", "Opportunity", "Lead"]
            ),
            APIReference(
                name="HubSpot",
                docs_url="https://developers.hubspot.com/docs/api",
                models=["Contact", "Company", "Deal", "Ticket"]
            ),
        ],
    }

    def infer_category(self, name: str) -> str | None:
        """Infer domain category from name."""

    def fetch_models(self, category: str) -> list[ModelDefinition]:
        """Fetch relevant models from best-in-class APIs."""

    def identify_patterns(self, models: list[ModelDefinition]) -> list[Pattern]:
        """Identify common patterns across models."""


# domain_cli/research/design_assistant.py

class DomainDesignAssistant:
    """Help design new domains based on research."""

    def suggest_schema(
        self,
        name: str,
        api_models: list[ModelDefinition],
        primitives: list[Primitive],
        existing_domains: list[DomainInfo]
    ) -> SuggestedSchema:
        """Generate a suggested schema based on research."""

    def suggest_primitives(self, name: str) -> list[Primitive]:
        """Suggest primitives to compose from."""
```

### 3.6 Knowledge Graph (v0.5 - TODO)

```python
# domain_cli/knowledge/graph.py

class KnowledgeGraph:
    """SQLite-backed knowledge graph for domain relationships."""

    def __init__(self, db_path: Path)

    # Queries
    def get_domain_rationale(self, name: str) -> Rationale | None
    def get_domain_usage(self, name: str) -> UsageStats
    def get_similar_domains(self, name: str, limit: int = 5) -> list[DomainInfo]
    def get_patterns_for_category(self, category: str) -> list[Pattern]
    def get_most_reused_domains(self, limit: int = 10) -> list[tuple[str, int]]
    def get_inspiration_sources(self, name: str) -> list[InspirationSource]

    # Mutations
    def record_domain_creation(self, name: str, rationale: Rationale)
    def record_domain_import(self, domain: str, project: str, entities: list[str])
    def add_pattern(self, pattern: Pattern)


# domain_cli/knowledge/rationale.py

class InspirationSource(BaseModel):
    source: str  # "stripe", "schema.org", etc.
    url: str
    models_referenced: list[str]
    rationale: str

class RejectedAlternative(BaseModel):
    source: str
    reason: str

class Decision(BaseModel):
    id: str
    question: str
    options: list[str]
    chosen: str
    rationale: str
    date: str

class Rationale(BaseModel):
    """Design rationale for a domain."""
    domain: str
    version: str
    created: str
    author: str

    purpose: str

    inspiration: list[InspirationSource]
    rejected: list[RejectedAlternative]

    primitives_used: dict[str, str]  # primitive -> used_for
    extends_domains: list[str]

    decisions: list[Decision]


# domain_cli/knowledge/usage.py

class UsageStats(BaseModel):
    domain: str
    import_count: int
    projects_using: list[str]
    entities_most_used: dict[str, int]
    last_imported: str | None

class UsageTracker:
    """Track domain usage across projects."""

    def record_import(self, domain: str, project: str, entities: list[str])
    def get_stats(self, domain: str) -> UsageStats
    def get_recommendations(self) -> UsageRecommendations
```

---

## 4.0 Domain Creation Gate Flow

### 4.1 Research → Inspire → Design → Gate

```
domain create payment-processor
  │
  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 1: INTERNAL SEARCH                                                │
│  ─────────────────────────────────────────────────────────────────────  │
│  Searching internal registry...                                         │
│  Similar domains found:                                                 │
│    • finance (82% match) - 47 imports, production                       │
│    • payment-processing (95% match) - 12 imports, development           │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  STEP 2: PRIMITIVE SUGGESTIONS                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  Recommended primitives:                                                │
│    • _primitives/quantity → Money {amount, currency}                    │
│    • _primitives/entity → Base entity with id, timestamps               │
│    • _primitives/state → Status enum with transitions                   │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  STEP 3: BEST-IN-CLASS INSPIRATION                                      │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  📚 STRIPE (Industry Standard)                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ PaymentIntent                                                    │   │
│  │   id: string                                                     │   │
│  │   amount: integer (cents)                                        │   │
│  │   currency: string (iso4217)                                     │   │
│  │   status: enum [requires_payment_method, processing, succeeded]  │   │
│  │   payment_method: PaymentMethod                                  │   │
│  │   metadata: map<string, string>                                  │   │
│  │   created: timestamp                                             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  📚 SCHEMA.ORG                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ schema.org/PayAction                                             │   │
│  │   agent: Person/Organization                                     │   │
│  │   recipient: Person/Organization                                 │   │
│  │   price: Number | priceCurrency: Text                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  STEP 4: PATTERNS IDENTIFIED                                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  Common patterns across Stripe, Square, Adyen:                          │
│    • Money as value object {amount, currency}                           │
│    • Status as state machine with defined transitions                   │
│    • Metadata as map<string, string> for extensibility                  │
│    • Idempotency keys for duplicate prevention                          │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  STEP 5: SUGGESTED SCHEMA                                               │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  entities:                                                              │
│    PaymentProcessor:                                                    │
│      extends: core.Entity                                               │
│      properties:                                                        │
│        amount: quantity.Money         # From primitive                  │
│        status: PaymentStatus          # State machine pattern           │
│        method: PaymentMethod          # Stripe pattern                  │
│        metadata: map<string,string>   # Extensibility pattern           │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  STEP 6: GATE DECISION                                                  │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  [1] Extend existing domain (payment-processing)                        │
│  [2] Compose from primitives + suggested schema                         │
│  [3] Adapt from best-in-class (Stripe model)                            │
│  [4] Create new from scratch → REQUIRES JUSTIFICATION                   │
│                                                                         │
│  Choice: _                                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Rationale Capture (Post-Creation)

```yaml
# Generated: shared/semantic/domains/payment-processor/.rationale.yaml

domain: payment-processor
version: "1.0.0"
created: "2025-12-15"
author: "developer@example.com"

purpose: |
  Unified payment processing model for checkout flows.
  Abstracts provider differences (Stripe, Square) behind common interface.

inspiration:
  - source: stripe
    url: https://stripe.com/docs/api/payment_intents
    models_referenced: [PaymentIntent, PaymentMethod]
    rationale: "Industry standard, battle-tested state machine, excellent docs"

  - source: schema.org
    url: https://schema.org/PayAction
    models_referenced: [PayAction]
    rationale: "W3C semantic web standard for interoperability"

rejected:
  - source: paypal
    reason: "Legacy REST patterns, inconsistent field naming"
  - source: square
    reason: "Less granular status tracking than Stripe"

composition:
  primitives:
    _primitives/quantity: "Money value object {amount, currency}"
    _primitives/entity: "Base entity with id, created_at, updated_at"
    _primitives/state: "PaymentStatus state machine"
  extends:
    - core

decisions:
  - id: PP-001
    question: "How to represent money amounts?"
    options:
      - "Integer cents (Stripe style)"
      - "Decimal with precision"
      - "Value object {amount, currency}"
    chosen: "Value object {amount, currency}"
    rationale: "Prevents currency mismatch bugs, matches primitive"
    date: "2025-12-15"
```

---

## 5.0 Knowledge Graph Schema

### 5.1 Node Types

```yaml
Domain:
  properties: [name, version, status, description, created, author]

Entity:
  properties: [name, domain, properties]

Primitive:
  properties: [name, description, schema_path]

ExternalSource:
  properties: [name, type, url]  # type: api | standard | oss

Pattern:
  properties: [name, description, examples, adoption_rate]

Decision:
  properties: [id, question, chosen, rationale, date]

Project:
  properties: [id, name, path]
```

### 5.2 Edge Types

```yaml
INSPIRED_BY:
  from: Domain → to: ExternalSource
  properties: [models_referenced, rationale]

REJECTED:
  from: Domain → to: ExternalSource
  properties: [reason]

EXTENDS:
  from: Domain → to: Domain
  properties: [entities_inherited]

USES_PRIMITIVE:
  from: Domain → to: Primitive
  properties: [used_for]

IMPLEMENTS_PATTERN:
  from: Domain → to: Pattern

DECIDED:
  from: Domain → to: Decision

IMPORTS:
  from: Project → to: Domain
  properties: [entities_used, import_date]
```

### 5.3 Example Queries

```python
# "What inspires our payment models?"
kg.query_inspiration("finance")
# → [("Stripe", "Industry standard..."), ("schema.org", "W3C compatibility")]

# "Which domains are most reused?"
kg.get_most_reused(limit=5)
# → [("core", 89), ("finance", 47), ("auth", 34), ...]

# "What patterns work for booking domains?"
kg.get_patterns_for_category("booking")
# → [Pattern("Availability slots"), Pattern("Reservation state machine")]

# "Why did we reject PayPal?"
kg.get_rejection_reason("finance", "PayPal")
# → "Legacy patterns, inconsistent naming"

# "Recommend domains for a new checkout feature"
kg.recommend_for_concept("checkout")
# → [finance (47 imports), cart (23 imports), pricing (18 imports)]
```

---

## 6.0 Usage Analytics

### 6.1 Automatic Tracking

When a project imports a domain (detected via code analysis or explicit registration):

```python
# Auto-tracked on import
kg.record_import(
    domain="finance",
    project="projects/work/checkout-service-abc12",
    entities=["Payment", "Invoice", "Transaction"],
    date="2025-12-15"
)
```

### 6.2 Analytics Output

```yaml
# shared/semantic/domains/_knowledge/usage.yaml

summary:
  total_domains: 99
  total_imports: 487
  most_active_month: "2025-12"

domains:
  finance:
    imports: 47
    trend: "+5 this month"
    projects:
      - projects/work/checkout-service-abc12
      - projects/personal/invoice-tracker-def34
    entities_usage:
      Payment: 45
      Invoice: 38
      Transaction: 32
    last_import: "2025-12-14"

  auth:
    imports: 34
    trend: "+2 this month"
    projects: [...]

recommendations:
  highly_reusable:
    - domain: finance
      imports: 47
      reason: "Gold standard for payments - proven patterns"
    - domain: auth
      imports: 34
      reason: "Stable auth patterns - widely adopted"

  underutilized:
    - domain: story
      imports: 3
      reason: "May be too domain-specific - consider generalizing"

  emerging_patterns:
    - pattern: "Money as {amount, currency}"
      found_in: [finance, billing, commerce]
      adoption: "67% of payment-related domains"
```

---

## 7.0 Tech Stack (Updated)

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| CLI Framework | Click | 8.1+ | Command interface |
| Output | Rich | 13.0+ | Terminal formatting |
| Data Models | Pydantic | 2.0+ | Schema validation |
| YAML Parsing | PyYAML | 6.0+ | Config files |
| Validation | pykwalify | 1.8+ | Schema validation |
| Codegen | datamodel-code-generator | 0.25+ | Pydantic generation |
| Knowledge DB | SQLite | 3.x | Knowledge graph storage |
| HTTP Client | httpx | 0.27+ | API fetching |
| MCP | mcp-sdk | 1.0+ | AI agent access |
| Python | Python | 3.11+ | Runtime |

---

## 8.0 Implementation Phases (Updated)

### Phase 1: v0.1 (DONE)
- ✅ Basic CLI: list, show, search, create, validate
- ✅ Registry module
- ✅ Rich output

### Phase 2: v0.2 (Enhanced Validation)
- [ ] Meta-schema for domain YAML
- [ ] pykwalify integration
- [ ] Better error messages

### Phase 3: v0.3 (Code Generation)
- [ ] `codegen` command
- [ ] datamodel-code-generator wrapper
- [ ] Pydantic v1/v2 support

### Phase 4: v0.4 (MCP Server)
- [ ] MCP server implementation
- [ ] domain_search, domain_details tools
- [ ] AI agent integration

### Phase 5: v0.5 (Knowledge System) ⭐ NEW
- [ ] Research Agent
  - [ ] Schema.org search
  - [ ] Best-in-class API fetcher
  - [ ] GitHub model search
  - [ ] Design assistant
- [ ] Knowledge Graph
  - [ ] SQLite schema
  - [ ] Rationale capture
  - [ ] Usage tracking
  - [ ] Pattern library
- [ ] Gated Creation Flow
  - [ ] Multi-step research
  - [ ] Inspiration display
  - [ ] Justification requirement
  - [ ] Rationale file generation

---

## 9.0 Risks & Mitigations (Updated)

| Risk | Impact | Mitigation |
|------|--------|------------|
| API specs unavailable/change | Medium | Cache specs, graceful fallback |
| Knowledge DB corruption | High | SQLite WAL mode, backups |
| Usage tracking privacy | Low | Only track internal projects |
| Pattern detection accuracy | Medium | Start simple, iterate |
| Research slows down creation | Medium | --skip-research flag for experts |

---

## 10.0 Exit Criteria

- ✅ Architecture documented
- ✅ Module structure defined
- ✅ Component interfaces specified
- ✅ Data flows documented
- ✅ Tech stack confirmed
- ✅ Knowledge system designed
- ✅ Rationale capture schema defined
- ✅ Usage analytics designed
- ✅ Gated creation flow specified
- ⏳ **Awaiting human approval of implementation strategy**
