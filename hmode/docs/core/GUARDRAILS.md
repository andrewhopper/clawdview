## 🔒 GUARDRAILS - PROTECTED FILES

**Purpose:** Critical configuration files controlling AI behavior, requiring explicit human approval before modification.

**Location:** `hmode/guardrails/` directory

### Protected Files

**1. Tech Preferences (`tech-preferences/`)**
- **What:** Approved technology stack decisions (libraries, frameworks, services)
- **Why Protected:** Technology choices must be vetted by humans before adoption
- **Update Process:** Use `/update-tech-preferences` or request manual approval
- **Categories:** `ai-ml.json`, `backend.json`, `frontend.json`, `infrastructure.json`, `services.json`
- **Symlinked From:** `shared/tech-preferences/` (backward compatibility)

**2. Architecture Preferences (`architecture-preferences/`)**
- **What:** Approved architectural patterns, design patterns, and development approaches
- **Why Protected:** Architectural decisions must be consistent and vetted across all prototypes
- **Update Process:** Manual approval required, observer detects candidates quarterly
- **Categories:** `process-patterns.json`, `design-patterns.json`, `architecture-patterns.json`, `integration-patterns.json`, `data-patterns.json`
- **Key Patterns:** Claude Code CLI child processes, two-phase execution, service layer pattern, repository pattern

**3. Writing Style Guide (`WRITING_STYLE_GUIDE.md`)**
- **What:** Writing standards for all documentation and communication
- **Why Protected:** Consistent voice and style across all outputs
- **Update Process:** Human approval required for any changes
- **Symlinked From:** `hmode/shared/standards/writing/WRITING_STYLE_GUIDE.md`

**4. CLAUDE.md (Repo Root)**
- **What:** AI development instructions, SDLC rules, workflows
- **Why Protected:** Core behavior and process definitions
- **Update Process:** Human approval required per CRITICAL RULES

### Enforcement Rules

**AI MUST:**
1. **NEVER modify any file in `hmode/guardrails/`** without explicit human approval
2. **Request approval** before making any changes to guardrail files
3. **Explain rationale** for proposed changes when requesting approval
4. **Wait for confirmation** before proceeding with modifications

**AI MUST NOT:**
- Add new technologies to tech-preferences without approval
- Add new architectural patterns to architecture-preferences without approval
- Use unapproved architectural patterns without requesting permission
- Modify writing standards without approval
- Create new guardrail files without approval
- Bypass guardrails via symlinks (protection applies to target files)

### Approval Workflow

When AI needs to modify a guardrail file:

1. **Explain:** What needs to change and why
2. **Present Options:** Multiple approaches if applicable
3. **Recommend:** AI's recommendation with rationale
4. **Wait:** Human approves, rejects, or requests revision
5. **Execute:** Only after explicit approval received

**Example:**
```
AI: "Need to add Terraform to infrastructure.json for proto-023.

     Option A: Add Terraform 1.6.x to infrastructure.json
     - Purpose: IaC for AWS deployments
     - Trade-off: Another tool to maintain

     Option B: Use existing CDK for all infrastructure
     - Purpose: Reuse approved tool
     - Trade-off: Less flexible than Terraform

     Recommend: Option B (reuse CDK)

     Approval required to proceed. y/n?"
```

### Guardrails Workflow Diagrams

**1. Usage During Coding (In-Flow Approval)**

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI/Developer Coding Session                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ Need tech/pattern X?    │
                 └─────────────────────────┘
                              │
                              ▼
            ┌────────────────────────────────┐
            │ Check guardrails/              │
            │ - tech-preferences/            │
            │ - architecture-preferences/    │
            └────────────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
         ┌──────────────┐          ┌──────────────┐
         │  ✅ APPROVED │          │ ❌ NOT FOUND │
         └──────────────┘          └──────────────┘
                 │                         │
                 ▼                         ▼
         ┌──────────────┐          ┌─────────────────────┐
         │ Use tech/    │          │ Request Approval    │
         │ pattern      │          │ - Explain rationale │
         │ Continue     │          │ - Present options   │
         └──────────────┘          │ - Recommend         │
                                   └─────────────────────┘
                                            │
                              ┌─────────────┴─────────────┐
                              ▼                           ▼
                      ┌──────────────┐          ┌──────────────┐
                      │ 👍 APPROVED  │          │ 👎 REJECTED  │
                      └──────────────┘          └──────────────┘
                              │                           │
                              ▼                           ▼
                   ┌────────────────────┐      ┌──────────────────┐
                   │ Update guardrails  │      │ Use alternative  │
                   │ Add to preferences │      │ Continue without │
                   └────────────────────┘      └──────────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │ Use tech/    │
                      │ pattern      │
                      │ Continue     │
                      └──────────────┘
```

**2. Candidate Extraction by Observer (Passive Learning)**

```
┌─────────────────────────────────────────────────────────────────┐
│              Multiple Coding Sessions Running                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Session1 │  │ Session2 │  │ Session3 │  │ Session4 │       │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬────┘       │
└────────┼─────────────┼─────────────┼─────────────┼─────────────┘
         │             │             │             │
         └─────────────┴─────────────┴─────────────┘
                       │
                       ▼
              ┌────────────────────┐
              │  Observer Process  │
              │  (Log Analysis)    │
              └────────────────────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Detect Patterns:   │
              │ - New libraries    │
              │ - Tech decisions   │
              │ - Arch patterns    │
              │ - Design patterns  │
              └────────────────────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Extract Candidates:│
              │ Tech:              │
              │ • Terraform (3x)   │
              │ • Prisma (5x)      │
              │ Patterns:          │
              │ • Event-driven(2x) │
              │ • CQRS (3x)        │
              └────────────────────┘
                       │
                       ▼
              ┌────────────────────┐
              │  Generate Report:  │
              │  - Frequency       │
              │  - Use cases       │
              │  - Prototypes      │
              └────────────────────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Queue for Review   │
              │ (Approval Committee)│
              └────────────────────┘
```

**3. Approval Process (In-Flow vs After-the-Fact)**

```
┌─────────────────────────────────────────────────────────────────┐
│                         APPROVAL PATHS                          │
└─────────────────────────────────────────────────────────────────┘

PATH A: IN-FLOW (Real-Time, Blocking)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ AI needs     │─────▶│ Request      │─────▶│ Human reviews│
│ library X    │      │ approval     │      │ immediately  │
└──────────────┘      │ (BLOCKS)     │      └──────────────┘
                      └──────────────┘             │
                                        ┌──────────┴──────────┐
                                        ▼                     ▼
                                ┌──────────────┐     ┌──────────────┐
                                │ ✅ APPROVE   │     │ ❌ REJECT    │
                                └──────────────┘     └──────────────┘
                                        │                     │
                                        ▼                     ▼
                                ┌──────────────┐     ┌──────────────┐
                                │ Update       │     │ Use          │
                                │ guardrails   │     │ alternative  │
                                │ Continue     │     │ Continue     │
                                └──────────────┘     └──────────────┘

PATH B: AFTER-THE-FACT (Batch, Non-Blocking)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ AI uses      │─────▶│ Log usage    │─────▶│ Continue     │
│ library X    │      │ (Observer)   │      │ coding       │
│ (allowed)    │      └──────────────┘      └──────────────┘
└──────────────┘             │
                             ▼
                      ┌─────────────────┐
                      │ Accumulate logs │
                      │ (daily/weekly)  │
                      └─────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │   Approval Committee       │
                │   (Scheduled Review)       │
                └────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
        ┌──────────────┐          ┌──────────────┐
        │ ✅ APPROVE   │          │ ❌ REJECT    │
        │ Add to       │          │ Mark as      │
        │ guardrails   │          │ deprecated   │
        └──────────────┘          └──────────────┘
                │                         │
                ▼                         ▼
        ┌──────────────┐          ┌──────────────┐
        │ Future use   │          │ Notify teams │
        │ auto-approved│          │ Find alts    │
        └──────────────┘          └──────────────┘

HYBRID: URGENT + BATCH
━━━━━━━━━━━━━━━━━━━━━━

High-value decisions  ──▶  PATH A (In-Flow)
Low-risk experiments  ──▶  PATH B (After-the-Fact)
```

### Directory Structure

```
hmode/guardrails/
├── README.md                          # Guardrails documentation
├── tech-preferences/                  # Technology stack approvals
│   ├── ai-ml.json
│   ├── backend.json
│   ├── frontend.json
│   ├── infrastructure.json
│   ├── services.json
│   └── [other category files]
├── architecture-preferences/          # Architectural pattern approvals
│   ├── README.md                      # Pattern documentation
│   ├── index.json                     # Master index
│   ├── approval-log.json              # Approval audit trail
│   ├── process-patterns.json          # Process/operational patterns
│   ├── design-patterns.json           # Code-level design patterns
│   ├── architecture-patterns.json     # System-level patterns
│   ├── integration-patterns.json      # Integration patterns
│   └── data-patterns.json             # Data management patterns
└── WRITING_STYLE_GUIDE.md            # Writing standards
```

### Symlinks (Backward Compatibility)

The following symlinks preserve existing paths:
- `shared/tech-preferences/` → `hmode/guardrails/tech-preferences/`
- `hmode/shared/standards/writing/WRITING_STYLE_GUIDE.md` → `hmode/guardrails/WRITING_STYLE_GUIDE.md`

**Protection applies to target files**, not just symlinks.

**See:** `hmode/guardrails/README.md` for complete documentation

