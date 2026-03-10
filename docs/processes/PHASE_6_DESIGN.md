### Phase 6: TECHNICAL DESIGN 🏗️ (NO CODE)
**Goal:** Complete technical specification for the SELECTED approach from Phase 5
**Output:** `project-management/ideas/proto-name-xxxxx-NNN-design/` (7 pages total max base + component specs)
**Title:** `# Stage 6 - Technical Design` (in each design doc)

---

## 🎯 PURPOSE: DETAILED DESIGN FOR ONE APPROACH

**Phase 6 is where we design the architecture for the approach chosen in Phase 5.**

**THIS IS NOT EXPLORATION - THIS IS DETAILED SPECIFICATION.**

**Input:** Single selected approach from Phase 5
**Output:** Complete technical design documents
**Scope:** Design ONLY for the chosen approach, not alternatives

---

## 🔀 TWO DISTINCT DESIGN DOMAINS (MANDATORY SEPARATION)

**Phase 6 has TWO distinct design activities that MUST be explicitly separated:**

### 6A: APPLICATION DESIGN (What the app does)
**Focus:** User-facing functionality, business logic, features, UI/UX
**Questions:**
- What features does the application have?
- How do users interact with it?
- What does the UI look like?
- What is the business logic?
- What are the user flows?
- What data does the app work with?
- What APIs does the app expose to clients?

**Output:** Application design documents (see 6A section below)

### 6B: INFRASTRUCTURE DESIGN (How to deploy and run it)
**Focus:** AWS resources, networking, deployment, monitoring
**Questions:**
- How is the application deployed? (CDK stacks, CloudFormation)
- What AWS services are used? (Lambda, API Gateway, S3, CloudFront, etc.)
- How does networking work? (VPC, security groups, load balancers)
- How is monitoring configured? (CloudWatch, X-Ray, alarms)
- How is CI/CD configured? (GitHub Actions, CodePipeline)
- How do secrets and environment configs work?

**Output:** Infrastructure design documents (see 6B section below)

**🚨 CRITICAL: Both 6A and 6B MUST be completed. Completing only infrastructure without application design is a FAILURE.**

---

## 📋 PHASE 6A: APPLICATION DESIGN DOCUMENTS

**Required documents (application layer):**
- **SPECIFICATION.md** - Detailed functional requirements and features
- **USER_FLOWS.md** - User interaction flows and journeys
- **API_DESIGN.md** - Application API contracts (what endpoints the app exposes)
- **DATABASE_SCHEMA.md** - Data models and schemas (application entities)
- **UI_DESIGN.md** - UI/UX wireframes, component hierarchy, interaction patterns
- **BUSINESS_LOGIC.md** - Core business rules, validation logic, workflows
- **INPUT_OUTPUT_SPEC.md** - Input/output contracts for application features

**Application Design Checklist:**
- [ ] Features and functionality clearly defined
- [ ] User flows documented with diagrams
- [ ] API contracts specified (endpoints, request/response formats)
- [ ] Data models defined (entities, relationships, validation)
- [ ] UI/UX wireframes created (if applicable)
- [ ] Business logic rules documented
- [ ] Application I/O contracts 100% defined

---

## 📋 PHASE 6B: INFRASTRUCTURE DESIGN DOCUMENTS

**Required documents (infrastructure layer):**
- **ARCHITECTURE.md** - System architecture (AWS services, components, data flow)
- **DEPLOYMENT_DESIGN.md** - Deployment strategy (CDK stacks, environments, rollout)
- **NETWORKING_DESIGN.md** - VPC, security groups, load balancers, DNS
- **MONITORING_DESIGN.md** - CloudWatch, X-Ray, alarms, dashboards
- **CI_CD_DESIGN.md** - GitHub Actions, CodePipeline, testing automation
- **SECURITY_DESIGN.md** - IAM policies, encryption, secrets management
- **TECH_STACK.md** - Technology selections (frameworks, libraries, AWS services)
- **RISKS.md** - Technical risks and mitigations

**Infrastructure Design Checklist:**
- [ ] AWS architecture diagram created
- [ ] CDK stacks defined (or Terraform modules)
- [ ] Networking topology documented
- [ ] Monitoring and alarms specified
- [ ] CI/CD pipeline designed
- [ ] Security controls documented
- [ ] Tech stack approved against hmode/guardrails/tech-preferences/

---

## 🔄 PHASE 6 WORKFLOW (Sequential: 6A → 6B)

**Phase 6 MUST execute in order:**

```
1. Domain Model Gate (mandatory first step)
   ↓
2. Phase 6A: Application Design
   - Define what the app does
   - Design features, UI, business logic, APIs
   - Human approval required
   ↓
3. Phase 6B: Infrastructure Design
   - Define how to deploy and run it
   - Design AWS architecture, monitoring, CI/CD
   - Human approval required
   ↓
4. Phase 7: Test Design
```

**Why this order matters:**
- You can't design infrastructure without knowing what the application does
- Application design is independent of deployment details
- Infrastructure design depends on application requirements

**🚨 AI MUST ASK: "Phase 6A (Application) or 6B (Infrastructure)?"**

When entering Phase 6, AI must explicitly ask:
```
Phase 6 has two distinct phases:

6A: Application Design - Define features, UI, business logic, APIs
6B: Infrastructure Design - Define AWS architecture, deployment, monitoring

Which phase should we start with?
[A] Phase 6A - Application Design (recommended first)
[B] Phase 6B - Infrastructure Design (do after 6A)
[C] Both - Guide me through 6A then 6B sequentially
```

**Never assume user wants infrastructure when they might want application design.**

---

---

## 📊 DOMAIN MODEL GATE (MANDATORY - FIRST STEP)

**BEFORE any design work, AI MUST check semantic domain models.**

**🤖 DELEGATE TO DOMAIN-MODELING-SPECIALIST AGENT:**

Use the specialized agent for all domain modeling work:
```bash
# Invoke domain-modeling-specialist agent
Task(subagent_type="domain-modeling-specialist",
     prompt="Discover and create domain models for this project")
```

The agent will handle:
- Reading the domain registry
- Presenting applicable domains with fitness scores
- Researching new domains (schema.org, GitHub, provider APIs)
- Generating YAML data models for approval
- Creating ontology and validation rules
- Auto-generating UML diagrams

### Agent Workflow Summary

**Step 1:** Agent reads domain registry

```bash
cat hmode/hmode/shared/semantic/domains/registry.yaml
```

**Step 2:** Agent presents domain menu

```markdown
## Domain Model Gate - Phase 6

Before designing architecture, let's identify reusable domain models.

### Applicable Existing Domains:

| # | Domain | Version | Relevance | Key Entities |
|---|--------|---------|-----------|--------------|
| 1 | auth | 1.0.0 | High | User, Session, Permission |
| 2 | email | 1.0.0 | Medium | Email, Attachment |
| 3 | core | 1.0.0 | High | TimePoint, Money, Address |
| 4 | ecommerce | 0.1.0 | Low | Product, Order, Cart |

**Relevance scoring:**
- High: Direct match to project domain
- Medium: Some entities applicable
- Low: Peripheral/optional

---

**Select domains to use:** (e.g., "1,3" or "none")
**New domains needed?** [Y/n] - I'll research and propose
```

**Step 3:** Agent generates domain models

If domains selected or new domain needed, the agent will:

1. **Import selected domains** from `@protoflow/semantic/domains/{domain}/`
2. **Generate project YAML models** in `shared/domain-models/{project-name}/`
   - `models.yaml` - Entity definitions
   - `enums.yaml` - Enum definitions
   - `relationships.yaml` - Entity relationships
3. **Present for human approval** (WAIT for confirmation)

**Step 4:** Agent auto-generates UML class diagram (MANDATORY)

After domain model approval:

```bash
# Auto-generate Mermaid class diagram from YAML
python3 hmode/shared/tools/yaml-to-mermaid.py \
  shared/domain-models/{project-name}/models.yaml \
  --output docs/diagrams/domain-model.mmd
```

**Output files:**
- `docs/diagrams/domain-model.mmd` - Mermaid source
- `docs/diagrams/domain-model.png` - Rendered image (optional)

**Auto-Documentation Confirmation:**

```
✓ Domain model created: shared/domain-models/{project}/models.yaml
✓ UML class diagram generated: docs/diagrams/domain-model.mmd
✓ Domain registry updated with dependencies
```

### Domain Model Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Skip domain check | ALWAYS delegate to domain-modeling-specialist agent |
| Duplicate existing domains | Agent imports and extends existing domains |
| Create domain without approval | Agent presents for human review with research |
| Skip UML generation | Agent auto-generates after approval |
| Modify production domains without approval | Agent proposes evolution with versioning |
| Handle domain modeling directly | Use domain-modeling-specialist agent |

**See:**
- `@processes/DOMAIN_MODEL_SOP` for detailed workflow documentation
- `hmode/agents/domain-modeling-specialist.md` for agent specification
- Use Task tool with `subagent_type="domain-modeling-specialist"` to invoke

---

### OPTIONAL: UML DIAGRAMS 📐 (Visual Design Documentation)

**When to use:**
- ✅ Complex systems with multiple interacting components
- ✅ Intricate class hierarchies or data models
- ✅ Critical user flows requiring precise sequencing
- ✅ Team collaboration (visual aids for shared understanding)
- ✅ Client deliverables requiring formal documentation
- ❌ Simple prototypes with few classes
- ❌ Straightforward CRUD applications
- ❌ Rapid POCs where speed trumps documentation

**Required Diagrams (if UML is used):**

**1. UML Class Diagram** - `design/UML_CLASS_DIAGRAM.md` or `.png/.svg`
- All major classes, interfaces, abstract classes
- Relationships: inheritance, composition, aggregation, association
- Key attributes and methods (public APIs)
- Cardinality and multiplicity
- **Tools:** PlantUML, Mermaid, draw.io, Lucidchart, or hand-drawn

**2. UML Sequence Diagrams (Plural)** - `design/UML_SEQUENCE_DIAGRAMS.md` or separate files
- One diagram per key flow (3-7 flows typical)
- **Key flows examples:**
  - User authentication flow
  - Primary business transaction (e.g., checkout, data processing)
  - Error handling and recovery
  - Critical async operations
  - External API integrations
- Actor interactions, object lifelines, messages
- Alternative paths and error scenarios
- **Tools:** PlantUML, Mermaid, draw.io, Lucidchart

**Format Options:**
- **Markdown + Mermaid/PlantUML:** Code-based diagrams in `.md` files (version control friendly)
- **Image exports:** `.png`, `.svg` files with source in `design/diagrams/source/`
- **Hybrid:** Both formats (source + rendered images)

**Example Structure:**
```
design/
├── SPECIFICATION.md
├── ARCHITECTURE.md
├── UML_CLASS_DIAGRAM.md          # Mermaid/PlantUML source
├── UML_CLASS_DIAGRAM.png          # Rendered image
├── UML_SEQUENCE_DIAGRAMS.md       # All flows in one doc
│   └── (or separate files)
├── diagrams/
│   ├── sequence-auth-flow.md
│   ├── sequence-checkout-flow.md
│   └── sequence-error-handling.md
└── IMPLEMENTATION_STRATEGY.md
```

**🚨 HUMAN APPROVAL REQUIRED (if UML used)**
- AI generates UML diagrams based on ARCHITECTURE.md and SPECIFICATION.md
- Human reviews class diagram for accuracy and completeness
- Human reviews sequence diagrams for all key flows
- Human approves or requests changes
- **Proceed to implementation strategy approval only after UML approved**

**Document in `.project` metadata:** `"uml_diagrams_used": true/false`

---

**🚨 HUMAN APPROVAL REQUIRED**
AI presents implementation strategy → Human approves → Proceed to Phase 7

**Exit:** All docs complete, I/O contracts 100%, UML diagrams approved (if used), strategy approved

