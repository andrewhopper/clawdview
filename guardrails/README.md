# Guardrails - Protected Configuration Files

**Purpose:** This directory contains critical configuration and guidance files that control AI behavior and project standards. ALL files in this directory require **explicit human approval** before any modifications.

## 🚨 PROTECTED FILES

### tech-preferences/
- **What:** Approved technology stack decisions (libraries, frameworks, services)
- **Why Protected:** Technology choices must be vetted by humans before adoption
- **Update Process:** Use `/update-tech-preferences` or manual approval required
- **Symlinked From:** `shared/tech-preferences/` (backward compatibility)

### architecture-preferences/
- **What:** Approved architectural patterns, design patterns, and development approaches
- **Why Protected:** Architectural decisions must be consistent and vetted across all prototypes
- **Update Process:** Manual approval required, observer detects candidates quarterly
- **Categories:** Process patterns, design patterns, architecture patterns, integration patterns, data patterns

### WRITING_STYLE_GUIDE.md
- **What:** Writing standards for all documentation and communication
- **Why Protected:** Consistent voice and style across all outputs
- **Update Process:** Human approval required for any changes
- **Symlinked From:** `shared/standards/writing/WRITING_STYLE_GUIDE.md`

## 🔒 ENFORCEMENT RULES

**AI MUST:**
1. **NEVER modify any file in `.guardrails/`** without explicit human approval
2. **Request approval** before making any changes to guardrail files
3. **Explain rationale** for proposed changes when requesting approval
4. **Wait for confirmation** before proceeding with modifications

**AI MUST NOT:**
- Add new technologies to tech-preferences without approval
- Add new architectural patterns to architecture-preferences without approval
- Modify writing standards without approval
- Create new guardrail files without approval
- Bypass guardrails via symlinks (protection applies to target files)
- Use unapproved architectural patterns without requesting permission

## 📂 DIRECTORY STRUCTURE

```
.guardrails/
├── README.md                          # This file
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

**Note:** CLAUDE.md remains in repo root for visibility, also requires human approval per CRITICAL RULES.

## 🔗 SYMLINKS (Backward Compatibility)

The following symlinks preserve existing paths:
- `shared/tech-preferences/` → `.guardrails/tech-preferences/`
- `shared/standards/writing/WRITING_STYLE_GUIDE.md` → `.guardrails/WRITING_STYLE_GUIDE.md`

**Protection applies to target files**, not just symlinks.

## ✅ APPROVAL WORKFLOW

When AI needs to modify a guardrail file:

1. **Explain:** What needs to change and why
2. **Present Options:** Multiple approaches if applicable
3. **Recommend:** AI's recommendation with rationale
4. **Wait:** Human approves, rejects, or requests revision
5. **Execute:** Only after explicit approval received

**Examples:**

**Technology Approval:**
```
AI: "Need to add Terraform to infrastructure.json for proto-023.

     Option A: Add Terraform 1.6.x to infrastructure.json
     - Purpose: IaC for AWS deployments
     - Trade-off: Another tool to maintain

     Approval required to proceed. y/n?"
```

**Architecture Pattern Approval:**
```
AI: "Detected new pattern: Event-Driven Microservices

     Used in: proto-027, proto-031 (2 prototypes)
     Success Rate: 100% (both reached Phase 9)

     Pattern Details:
     - Category: architecture-patterns → service_architecture
     - Principles: Async communication, loose coupling, event bus
     - Use Cases: Decoupled services, scalable systems

     Add to architecture-preferences/architecture-patterns.json? y/n?"