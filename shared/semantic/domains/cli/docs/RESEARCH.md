# Stage 2 - Research

## 1.0 Existing Solutions Survey (GitHub Research)

### 1.1 Schema/Code Generation Tools

| Tool | Stars | Description | Fit | Source |
|------|-------|-------------|-----|--------|
| [**datamodel-code-generator**](https://github.com/koxudaxi/datamodel-code-generator) | 2.5k+ | Generate Pydantic/dataclass from JSON Schema, YAML, OpenAPI | ⭐ HIGH - Could generate Python types from our YAML schemas | MIT |
| [**OpenAPI Generator**](https://github.com/OpenAPITools/openapi-generator) | 20k+ | Generate client/server code from OpenAPI specs | MEDIUM - Focused on API, not domain models | Apache 2.0 |
| [**sysgears/domain-schema**](https://github.com/sysgears/domain-schema) | 100+ | DDD schema as single source of truth for DB, forms, GraphQL | ⭐ HIGH - Same philosophy as our domain models | MIT |

### 1.2 Schema Registry / GitOps Tools

| Tool | Stars | Description | Fit | Source |
|------|-------|-------------|-----|--------|
| [**schema-registry-gitops**](https://github.com/domnikl/schema-registry-gitops) | 200+ | Manage Confluent Schema Registry via YAML + IaC | MEDIUM - Kafka-specific, but YAML-first approach | Apache 2.0 |
| [**Jikkou CLI**](https://github.com/streamthoughts/jikkou) | 100+ | GitOps schema management for Kafka | LOW - Kafka-specific | Apache 2.0 |
| [**Confluent Schema Registry**](https://github.com/confluentinc/schema-registry) | 2k+ | Kafka schema registry | LOW - Kafka-specific | Confluent License |

### 1.3 Data/Table Schema Tools

| Tool | Stars | Description | Fit | Source |
|------|-------|-------------|-----|--------|
| [**tableschema-py**](https://github.com/frictionlessdata/tableschema-py) | 200+ | Frictionless Data table schema library | LOW - Tabular data focused | MIT |
| [**appnexus/schema-tool**](https://github.com/appnexus/schema-tool) | 50+ | Database schema migration CLI | LOW - DB migrations only | Apache 2.0 |

### 1.4 DDD Resources (Not Direct Tools)

| Resource | Description | Source |
|----------|-------------|--------|
| [**awesome-ddd**](https://github.com/heynickc/awesome-ddd) | Curated DDD resources list | GitHub |
| [**ddd-by-examples/library**](https://github.com/ddd-by-examples/library) | Comprehensive DDD example | GitHub |
| [**DDD Crew**](https://github.com/ddd-crew) | Aggregate design canvas, message flow templates | GitHub |

---

## 2.0 Key Findings

### 2.1 datamodel-code-generator (Most Relevant)

**What it does:**
- Input: JSON Schema, YAML, OpenAPI → Output: Pydantic models, dataclasses, TypedDict
- CLI: `datamodel-codegen --input schema.yaml --output model.py`
- Used by: Airbyte, Apache Iceberg, AWS Lambda Powertools, DataDog

**Relevance to our problem:**
- Could **generate Python types** from our domain YAML schemas
- Doesn't solve discovery/search - only code generation
- Potential integration: `domain codegen <domain>` command

### 2.2 sysgears/domain-schema (Philosophy Match)

**What it does:**
- Define schema once → generate DB schemas, forms, GraphQL types
- JavaScript/TypeScript focused
- Single source of truth philosophy

**Relevance:**
- Same DDD philosophy as our domain models
- Different language ecosystem (JS vs Python)
- Validates our approach is sound

### 2.3 Gap Analysis

| Need | Existing Tools | Gap |
|------|----------------|-----|
| **List/search domains** | None | ❌ No tool does this |
| **View domain details** | None | ❌ No tool does this |
| **Create from template** | None | ❌ No tool does this |
| **Validate schema** | JSON Schema validators | ⚠️ Generic, not domain-specific |
| **Generate code** | datamodel-code-generator | ✅ Could integrate |

---

## 3.0 Build vs Buy vs Adapt

| Option | Tool | Effort | Fit | Recommendation |
|--------|------|--------|-----|----------------|
| **Adapt** | datamodel-code-generator | Low | Partial - code gen only | ✅ Integrate for `codegen` command |
| **Adapt** | sysgears/domain-schema | High | Philosophy match, wrong language | ❌ Skip |
| **Build** | Custom CLI | Low | Perfect fit for discovery/CRUD | ✅ Build core CLI |
| **Build** | MCP Server | Medium | Enables AI discovery | ✅ Consider for v2 |

**Decision:**
- **BUILD** custom CLI for discovery/CRUD/validation
- **INTEGRATE** datamodel-code-generator for optional code generation

---

## 4.0 Target Audience (AI-Inferred, Human-Validated)

### 4.1 Primary Persona: "Monorepo Developer"

| Attribute | Value |
|-----------|-------|
| **Role** | Software Engineer / AI Engineer |
| **Experience** | 2-10 years |
| **Environment** | Terminal + VSCode/Cursor |
| **Working style** | Fast iteration, minimal context switching |
| **Pain points** | Finding right domain, creating consistent schemas |
| **Decision style** | Self-serve, values good DX |
| **Tech comfort** | High - uses pip, npm, docker daily |
| **Core belief** | Shared semantic layer enables AI - define once, use everywhere |
| **Motivation** | DRY principle - refuses to redefine same concepts across projects |
| **Vision** | Domain models as contracts that AI agents can understand and use |

### 4.2 Secondary Persona: "New Team Member"

| Attribute | Value |
|-----------|-------|
| **Role** | New hire or contractor |
| **Experience** | Variable, new to this codebase |
| **Need** | Understand what domains exist |
| **Pain point** | Onboarding friction, "where do I find X?" |

---

## 5.0 Exit Criteria

- ✅ GitHub tools surveyed (10+ tools evaluated)
- ✅ Relevant tools identified (datamodel-code-generator, domain-schema)
- ✅ Gaps identified (no discovery/search tool exists)
- ✅ Build vs adapt decision made
- ✅ Primary persona validated
- ✅ Secondary persona validated
