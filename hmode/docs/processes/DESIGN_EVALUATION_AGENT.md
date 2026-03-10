# Design Evaluation Agent - Process Reference

<!-- File UUID: c7c8e4ce-c8b3-4c4b-b228-cfe8db925e82 -->

## 1.0 Purpose

The design-evaluation-agent assesses software designs and codebases for modularity, decoupling, and decomposition quality. It produces structured evaluation reports with severity-rated findings and actionable recommendations.

## 2.0 When to Invoke

### 2.1 Automatic Triggers (Gate 11)

| Trigger | Context | Action |
|---------|---------|--------|
| Phase 6 → Phase 8 transition | Design complete, entering implementation | Full design review (Workflow 1) |
| Phase 8 mid-implementation | Module growing beyond scope | Targeted decomposition (Workflow 3) |
| Brownfield entry (FEATURE type) | Adding feature to existing code | Code architecture review (Workflow 2) |

### 2.2 Manual Triggers

| User Request | Agent Workflow |
|-------------|---------------|
| "Review my architecture for modularity" | Workflow 1 (Design Review) |
| "Is this codebase well-structured?" | Workflow 2 (Code Architecture Review) |
| "Should I split this service/module?" | Workflow 3 (Decomposition Analysis) |
| "Why are my tests so hard to write?" | Workflow 2 (focus: testability) |
| "Check for coupling issues" | Workflow 2 (focus: coupling) |

### 2.3 Proactive Triggers

Claude Code should suggest this agent when it detects:
- A single file exceeding 500 lines during Phase 8
- Circular import patterns in code being written
- Test files with excessive mock/stub setup
- Phase 6 completion with 3+ interacting modules in design
- User complaints about "spaghetti code" or "everything depends on everything"

## 3.0 Integration with SDLC

### 3.1 Phase 6 (Design) Exit Gate

When Phase 6 design documents are complete and the user wants to advance to Phase 8:

```
Phase 6 Complete
     │
     ▼
┌─────────────────────────────┐
│  Gate 11: Design Evaluation │
│  - Read ARCHITECTURE.md     │
│  - Read API_DESIGN.md       │
│  - Analyze module structure  │
│  - Score 6 dimensions        │
│  - List findings by severity │
└────────┬────────────────────┘
         │
    ┌────┴────┐
    │ Result? │
    └────┬────┘
         │
    ┌────┼────────────┬──────────────┐
    │    │            │              │
  PASS  CONDITIONAL  NEEDS WORK   FAIL
    │    │            │              │
    ▼    ▼            ▼              ▼
  Phase 8  Fix SEV-1   Fix SEV-1+2   Return to
           then go     then re-eval  Phase 6
```

### 3.2 Phase 8 (Implementation) Checkpoints

During implementation, invoke the agent when:
- Module complexity exceeds thresholds
- New cross-module dependencies are introduced
- User requests a design health check
- Before major refactoring work

### 3.3 Brownfield Integration

For brownfield projects (FEATURE or REFACTOR work types):

```
Brownfield Phase 0 (Assessment)
     │
     ▼
┌─────────────────────────────┐
│  Design Evaluation Agent    │
│  - Analyze existing code    │
│  - Map current architecture │
│  - Identify coupling issues │
│  - Score baseline quality   │
└────────┬────────────────────┘
         │
         ▼
  Evaluation report informs
  implementation approach
```

## 4.0 Evaluation Dimensions

### 4.1 Scoring Guide

Each dimension scored 1-5:

**Coupling (independence between modules)**
| Score | Criteria |
|-------|----------|
| 5 | Modules communicate only through interfaces/events; no shared state |
| 4 | Mostly interface-driven; 1-2 direct concrete dependencies |
| 3 | Mix of interface and concrete dependencies; some shared utilities |
| 2 | Heavy direct dependencies; shared mutable state; circular deps present |
| 1 | Monolithic: everything depends on everything; cannot change one without many |

**Cohesion (focus within modules)**
| Score | Criteria |
|-------|----------|
| 5 | Each module has exactly one clear responsibility; name = purpose |
| 4 | Modules mostly focused; 1-2 minor secondary responsibilities |
| 3 | Some modules handle 2-3 unrelated concerns; beginning to diverge |
| 2 | Several god modules; responsibilities scattered across boundaries |
| 1 | No discernible organization; functions grouped by convenience |

**Encapsulation (information hiding)**
| Score | Criteria |
|-------|----------|
| 5 | All implementation details hidden; clean public interfaces only |
| 4 | Mostly encapsulated; 1-2 leaky abstractions |
| 3 | Some internals exposed; DTOs carry implementation details |
| 2 | Significant leakage; consumers depend on internal structure |
| 1 | No encapsulation; all internals accessible and depended upon |

**Composability (reuse in different contexts)**
| Score | Criteria |
|-------|----------|
| 5 | Modules are self-contained; plug-and-play in new contexts |
| 4 | Most modules portable; minor context-specific assumptions |
| 3 | Some modules reusable; others tightly bound to one use case |
| 2 | Few modules can be extracted; heavy environment assumptions |
| 1 | Nothing is reusable outside the current application |

**Testability (isolation for testing)**
| Score | Criteria |
|-------|----------|
| 5 | Every module testable in isolation with simple stubs; < 5 lines setup |
| 4 | Most modules testable; 1-2 require moderate mocking |
| 3 | Testing possible but requires significant mock setup |
| 2 | Many modules need integration test environment to verify |
| 1 | Cannot test without running the full system |

**Deployability (independent deployment)**
| Score | Criteria |
|-------|----------|
| 5 | Each module/service deployable independently; no coordination needed |
| 4 | Mostly independent; 1-2 coordinated deployments required |
| 3 | Some modules independent; core requires full redeploy |
| 2 | Most changes require full system deployment |
| 1 | All-or-nothing deployment; any change requires full release |

## 5.0 Common Patterns and Remediation

### 5.1 Decoupling Strategies

| Strategy | When to Use | Trade-offs |
|----------|------------|------------|
| **Extract Interface** | Concrete dependency between modules | Adds indirection; worth it for stability |
| **Dependency Injection** | Hard-wired dependencies blocking testing | Requires DI container or manual wiring |
| **Event-Driven** | Modules need to react without direct coupling | Adds async complexity; harder to trace |
| **Mediator/Bus** | Multiple modules coordinate without knowing each other | Central point of failure; indirection cost |
| **Facade** | Complex subsystem exposed to consumers | Hides complexity but may limit flexibility |
| **Anti-Corruption Layer** | Integrating with external/legacy system | Extra translation layer; maintenance cost |

### 5.2 Decomposition Strategies

| Strategy | When to Use | Approach |
|----------|------------|----------|
| **By Domain** | Distinct business capabilities identified | One module per bounded context |
| **By Layer** | Clear horizontal separation needed | Presentation / Domain / Infrastructure |
| **By Feature** | Vertical slices more natural | Each feature self-contained across layers |
| **Strangler Fig** | Gradual migration of monolith | New features in new modules; migrate gradually |

## 6.0 Output Artifacts

The agent produces:

| Artifact | Format | Contents |
|----------|--------|----------|
| Evaluation Report | Markdown | Scores, findings, recommendations |
| Dependency Graph | Mermaid diagram | Module relationships and coupling |
| Findings List | Table | Severity-rated issues with locations |
| Recommendation Plan | Numbered list | Prioritized remediation steps |
| Decomposition Proposal | Table + diagram | Split boundaries (Workflow 3 only) |

## 7.0 Agent Metadata

**Version:** 1.0.0
**Created:** 2026-02-19
**Agent Definition:** `hmode/agents/design-evaluation-agent.md`
**Gate:** 11 (Design Evaluation)
**Related Gates:** Gate 6 (Design System), Gate 7 (IA), Gate 9 (Infra/SRE)
