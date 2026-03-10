# Architecture Preferences - Protected Patterns

**Purpose:** Capture and govern approved architectural patterns, design decisions, and development approaches used across all prototypes.

## 🚨 PROTECTED CONTENT

All files in this directory require **explicit human approval** before modifications. This ensures:
- Consistent architectural approaches across projects
- Vetted patterns that align with team expertise
- Clear rationale for architectural decisions
- Traceable approval history

## 📂 STRUCTURE

```
.guardrails/architecture-preferences/
├── README.md                          # This file
├── index.json                         # Master index of all patterns
├── approval-log.json                  # Approval history and audit trail
├── process-patterns.json              # Development/operational patterns
├── design-patterns.json               # Code-level design patterns
├── architecture-patterns.json         # System-level architecture patterns
├── integration-patterns.json          # System integration patterns
└── data-patterns.json                 # Data management patterns
```

## 📋 CATEGORIES

### 1. Process Patterns (`process-patterns.json`)
**Development and operational process patterns**

Categories:
- **parallel_execution**: Patterns for concurrent processes/tasks
- **agent_orchestration**: Multi-AI agent coordination patterns

**Example:** Claude Code CLI Child Processes pattern for parallel autonomous agents

---

### 2. Design Patterns (`design-patterns.json`)
**Code-level design patterns and best practices**

Categories:
- **creational_patterns**: Object creation patterns (Factory, Builder, Singleton, etc.)
- **structural_patterns**: Object composition patterns (Adapter, Decorator, Proxy, etc.)
- **behavioral_patterns**: Object interaction patterns (Observer, Strategy, Command, etc.)
- **code_organization**: Code structure patterns (Service Layer, Repository, etc.)

---

### 3. Architecture Patterns (`architecture-patterns.json`)
**System-level architecture patterns**

Categories:
- **application_architecture**: Overall app structure (Monolith, Microservices, Serverless, etc.)
- **service_architecture**: Service organization patterns (Event-driven, CQRS, Saga, etc.)
- **deployment_architecture**: Deployment patterns (Blue/green, Canary, Feature flags, etc.)
- **scaling_patterns**: Scaling strategies (Horizontal, Vertical, Auto-scaling, etc.)

---

### 4. Integration Patterns (`integration-patterns.json`)
**System integration and communication patterns**

Categories:
- **api_patterns**: API design patterns (REST, GraphQL, gRPC, etc.)
- **messaging_patterns**: Async messaging (Pub/Sub, Message Queue, Event Bus, etc.)
- **data_sync_patterns**: Data synchronization (CDC, ETL, Replication, etc.)
- **authentication_patterns**: Auth integration (OAuth, SAML, JWT, API Keys, etc.)

---

### 5. Data Patterns (`data-patterns.json`)
**Data management and persistence patterns**

Categories:
- **data_access_patterns**: Database access (Repository, DAO, Active Record, etc.)
- **data_modeling_patterns**: Schema design (Normalized, Denormalized, Star Schema, etc.)
- **caching_patterns**: Caching strategies (Write-through, Write-behind, Cache-aside, etc.)
- **event_sourcing_patterns**: Event-based data (Event Store, CQRS, Snapshots, etc.)

## 🔍 PATTERN SCHEMA

Each approved pattern includes:

```json
{
  "rank": 1,
  "name": "Pattern Name",
  "version": "1.0.0",
  "rationale": "Why this pattern is preferred",
  "useCases": [
    "When to use this pattern",
    "Specific scenarios"
  ],
  "keyPrinciples": [
    "Core principle 1",
    "Core principle 2"
  ],
  "exampleLocation": "path/to/reference/implementation",
  "docsLocation": "path/to/documentation",
  "approvedBy": "Approver Name",
  "approvedDate": "2025-11-16",
  "status": "approved"
}
```

## 🔄 PATTERN LIFECYCLE

### 1. Detection (Passive Observer)
AI observes patterns emerging across prototypes:
- Repeated architectural approaches
- Common design patterns
- Successful integration strategies
- Effective data management techniques

**Observer Process:**
- Monitors coding sessions (logs, git commits, design docs)
- Detects pattern frequency and usage contexts
- Generates candidate patterns quarterly
- Queues for approval committee review

---

### 2. Approval (In-Flow or Committee)

**Path A: In-Flow Approval** (Real-time, blocking)
```
AI needs pattern X → Request approval → Human reviews → Approve/Reject
                                                      ↓
                                                  Use pattern
```

**Path B: After-the-Fact** (Batch, non-blocking)
```
AI uses pattern X → Log usage → Accumulate → Committee Review → Approve/Archive
                                                              ↓
                                                    Future use auto-approved
```

**Approval Criteria:**
- ✅ Pattern solves real recurring problem
- ✅ Team has expertise to maintain
- ✅ Clear advantages over alternatives
- ✅ Well-documented with examples
- ✅ Aligns with existing tech stack

---

### 3. Usage (Post-Approval)
Once approved:
- AI can use pattern without re-requesting approval
- Pattern appears in design recommendations
- Referenced in Phase 6 technical design
- Documented in implementation strategy

---

### 4. Evolution (Versioning)
Patterns evolve over time:
- **Minor version** (1.0.0 → 1.1.0): Add use cases, refine principles
- **Major version** (1.0.0 → 2.0.0): Breaking changes, new approach
- **Deprecation**: Mark obsolete, suggest replacement

## 📊 APPROVAL LOG

`approval-log.json` tracks all pattern approvals:

```json
{
  "approvals": [
    {
      "pattern": "Claude Code CLI Child Processes",
      "category": "process-patterns",
      "subcategory": "parallel_execution",
      "approvedBy": "Andy Hopper",
      "approvedDate": "2025-11-16T10:00:00Z",
      "version": "1.0.0",
      "rationale": "Proven in proto-005, enables scalable multi-agent workflows",
      "status": "approved"
    }
  ],
  "rejections": [],
  "pending": []
}
```

## 🤖 AI RESPONSIBILITIES

### When Coding (In-Flow)

**✅ AI MUST:**
1. Check architecture-preferences before choosing patterns
2. Use approved patterns when available
3. Request approval for new patterns (blocking)
4. Document pattern usage in design docs
5. Reference pattern location in code comments

**❌ AI MUST NOT:**
- Use unapproved patterns without requesting permission
- Modify architecture-preferences files directly
- Skip pattern approval for "small" projects
- Assume patterns from previous projects are approved

---

### When Observing (Passive Learning)

**Observer AI SHOULD:**
1. Detect repeated patterns across prototypes (3+ uses)
2. Extract pattern details (name, principles, use cases)
3. Generate candidate pattern proposals
4. Queue for quarterly approval committee review
5. Document pattern frequency and success metrics

**Example Detection:**
```
Pattern Detected: "Two-Phase Agent Execution"
Frequency: 5 prototypes
Success Rate: 100% (all completed Phase 9)
Time Savings: ~3x vs sequential (avg 9min → 3min)
Candidate for: process-patterns.json → agent_orchestration
```

## 🔐 ENFORCEMENT

### Phase-Specific Rules

**Phase 6 (Technical Design):**
- MUST reference approved architecture patterns
- MUST justify if NOT using approved pattern
- MUST request approval for new patterns
- Cannot proceed to Phase 7 without pattern approval

**Phase 8 (Implementation):**
- MUST follow approved design patterns
- Code review checks pattern adherence
- Cannot transition to Phase 9 with pattern violations

### Approval Requirements

**MUST request approval when:**
- Introducing new architectural approach
- Choosing system integration strategy
- Designing data access layer
- Selecting deployment pattern
- Using design pattern not in preferences

**CAN use without approval:**
- Approved patterns from architecture-preferences
- Standard language idioms (not architectural decisions)
- Tactical code patterns (loops, conditionals, etc.)

## 📚 REFERENCE EXAMPLES

Approved patterns link to reference implementations:

**Process Patterns:**
- `prototypes/proto-company-researcher-uiwid-005/orchestrator.py` - Claude Code CLI child processes

**Design Patterns:**
- `shared/standards/code/nodejs/` - Service layer pattern
- `shared/standards/code/typescript/` - Repository pattern

**Data Patterns:**
- `shared/standards/code/python/` - Repository pattern with Pydantic

## 🔄 QUARTERLY REVIEW PROCESS

**Observer Summary Generation:**
1. Collect pattern usage data (last 90 days)
2. Identify candidates (3+ uses, >80% success rate)
3. Generate proposal document with:
   - Pattern name and description
   - Frequency and contexts
   - Success metrics
   - Reference implementations
   - Recommended category

**Approval Committee Review:**
1. Review observer-generated candidates
2. Evaluate against approval criteria
3. Approve, reject, or request revision
4. Update architecture-preferences files
5. Notify teams of new approved patterns

## 🎯 SUCCESS METRICS

**Pattern Adoption:**
- % prototypes using approved patterns
- Pattern reuse rate across projects
- Time saved vs. ad-hoc approaches

**Pattern Quality:**
- Success rate (% projects reaching Phase 9)
- Developer satisfaction scores
- Maintenance burden

**Governance Effectiveness:**
- Approval turnaround time
- Rejection rate (high = too restrictive)
- Pattern evolution frequency

## ⚡ QUICK REFERENCE

**Check approved patterns:**
```bash
cat .guardrails/architecture-preferences/index.json
```

**Request new pattern approval:**
1. Explain pattern and rationale
2. Provide use cases and examples
3. Wait for human approval
4. Use only after approved

**Observer candidates:**
- Generated quarterly
- Based on 90-day usage data
- Require 3+ uses, >80% success rate
- Committee reviews and approves
