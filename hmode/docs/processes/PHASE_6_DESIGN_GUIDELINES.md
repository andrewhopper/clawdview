# Phase 6 Design Guidelines

<!-- File UUID: 8f2c4d1a-9e3b-4f7c-a6d8-2b9e5c7f1a3d -->

## 1.0 Overview

Phase 6 (DESIGN) creates comprehensive technical design documents BEFORE implementation. This phase is **planning-heavy** and must enforce strict adherence to tech stack guardrails.

**Key Principle:** All technology decisions must be validated against `hmode/guardrails/tech-preferences/` before being documented.

---

## 2.0 Mandatory Design Checklist

Before creating ANY Phase 6 design document, complete this checklist:

### 2.1 Planning Gate
- [ ] **Use Plan agent** if creating 3+ design documents
- [ ] Plan agent outlines: document structure, dependencies, creation sequence
- [ ] Plan includes tech stack validation step

### 2.2 Tech Stack Verification Gate
- [ ] Read `hmode/guardrails/tech-preferences/infrastructure.json`
- [ ] Read `hmode/guardrails/tech-preferences/ai-ml.json` (if using AI/ML)
- [ ] Read `hmode/guardrails/tech-preferences/frontend.json` (if web UI)
- [ ] Read `hmode/guardrails/tech-preferences/backend.json` (if API/database)
- [ ] Use **exact versions** from guardrails (not approximations)
- [ ] Use **rank 1** preferences unless specific use case requires alternative
- [ ] If technology not in guardrails → **ask human for approval FIRST**

### 2.3 Architecture Alignment Gate
- [ ] Check `hmode/guardrails/architecture-preferences/` for patterns
- [ ] Verify AWS projects include CloudWatch + X-Ray (required per infrastructure.json:94-108)
- [ ] Confirm IaC tool is AWS CDK (not SAM/CloudFormation per infrastructure.json:421)

### 2.4 Violation Response
**If ANY checkbox unchecked:**
1. STOP document creation
2. Fix missing guardrails check
3. Restart checklist from top

---

## 3.0 Common Violations

### 3.1 Model/Framework Versions
❌ **WRONG:**
- "Claude 3.5 Sonnet" (outdated)
- "Next.js 14" (outdated)
- "React 18" (outdated)

✅ **CORRECT (as of 2026-02-05):**
- "Claude Sonnet 4.5" (global.anthropic.claude-sonnet-4-5-20250929-v1:0)
- "Next.js 15.x" (stable with React 19)
- "React 19.x" (stable)

### 3.2 IaC Tools
❌ **WRONG:**
- AWS SAM (not in rank 1)
- AWS CloudFormation (rank 3)
- Terraform (rank 2 - only for multi-cloud)

✅ **CORRECT:**
- AWS CDK 2.x (rank 1 for AWS projects per infrastructure.json:421)

### 3.3 Monitoring (AWS Projects)
❌ **WRONG:**
- Mentioning CloudWatch without X-Ray
- No monitoring section in architecture
- Optional monitoring

✅ **CORRECT (REQUIRED per infrastructure.json:92-108):**
- CloudWatch logs + metrics + alarms (REQUIRED)
- X-Ray active tracing on ALL Lambda functions (REQUIRED)
- Operational dashboards (REQUIRED)
- Error rate, latency P99, availability alarms (REQUIRED)

### 3.4 UI Libraries
❌ **WRONG:**
- Using React Flow without checking guardrails
- Assuming libraries are approved
- Using MUI as first choice

✅ **CORRECT:**
- shadcn/ui (rank 1 per frontend.json:59)
- Radix UI (rank 2 - headless primitives)
- Check guardrails BEFORE adding any UI library

---

## 4.0 Phase 6 Document Sequence

### 4.1 Standard Design Documents (in order)
1. **SPECIFICATION.md** (user-facing requirements) ✓
2. **ARCHITECTURE.md** (system design, components, data flows) ← **GUARDRAILS CRITICAL**
3. **API_DESIGN.md** (endpoints, events, schemas)
4. **DATABASE_SCHEMA.md** (tables, indexes, relationships)
5. **INPUT_OUTPUT_SPEC.md** (data formats, validation)
6. **TECH_STACK.md** (exact versions, justifications) ← **GUARDRAILS CRITICAL**
7. **IMPLEMENTATION_STRATEGY.md** (code structure, modules)
8. **IMPLEMENTATION_PLAN.md** (timeline, milestones)
9. **RISKS.md** (technical risks, mitigations)

### 4.2 Guardrails-Critical Documents
**ARCHITECTURE.md** and **TECH_STACK.md** MUST be validated against guardrails before creation.

---

## 5.0 Tech Stack Decision Process

### 5.1 Decision Tree
```
Need to choose technology for X
    │
    ▼
Does `hmode/guardrails/tech-preferences/{category}.json` exist?
    │
    ├─ YES → Read file
    │         │
    │         ▼
    │     Is X listed in preferences?
    │         │
    │         ├─ YES → Use rank 1 (or justify alternative)
    │         │
    │         └─ NO → Ask human for approval
    │
    └─ NO → Ask human for approval
```

### 5.2 Justifying Non-Rank-1 Choices
If using rank 2+ technology, document WHY in design doc:

```markdown
**Technology Choice: Terraform (Rank 2)**
**Justification:** Multi-cloud deployment required (AWS + GCP).
Infrastructure.json specifies Terraform for multi-cloud use cases.
```

---

## 6.0 Plan Agent Integration

### 6.1 When to Use Plan Agent
**Mandatory for:**
- Creating 3+ design documents
- Multi-technology projects (AI/ML + Infrastructure + Frontend)
- Complex architecture spanning multiple AWS services

### 6.2 Plan Agent Responsibilities
1. **Read guardrails** for all relevant categories
2. **Outline documents** to create and dependencies
3. **Validate tech stack** against guardrails
4. **Define sequence** (which docs first, which depend on others)
5. **Present plan** to human for approval

### 6.3 Plan Agent Output Format
```markdown
# Phase 6 Design Plan for {Project Name}

## 1.0 Tech Stack Validation
- ✅ Infrastructure: AWS CDK 2.x (rank 1)
- ✅ LLM: AWS Bedrock Claude Sonnet 4.5 (rank 1)
- ✅ Frontend: Next.js 15.x (rank 1)
- ✅ UI Library: shadcn/ui (rank 1)
- ⚠️ Monitoring: CloudWatch + X-Ray REQUIRED for AWS projects

## 2.0 Document Creation Sequence
1. SPECIFICATION.md (requirements) - already exists
2. ARCHITECTURE.md (depends on tech stack validation)
3. API_DESIGN.md (depends on ARCHITECTURE.md)
4. DATABASE_SCHEMA.md (depends on ARCHITECTURE.md)
5. TECH_STACK.md (documents validated choices)
...

## 3.0 Dependencies
- ARCHITECTURE.md requires tech stack locked
- API_DESIGN.md requires ARCHITECTURE.md component list
- DATABASE_SCHEMA.md requires data models from domain agent

## 4.0 Approval Request
Proceed with this plan? [Y/n]
```

---

## 7.0 Monitoring Requirements for AWS Projects

Per `infrastructure.json:92-108`, ALL AWS projects MUST configure:

### 7.1 CloudWatch (REQUIRED)
- **Logs:** All Lambda, ECS, API Gateway
- **Metrics:** Custom metrics for business KPIs
- **Alarms:** Error rate >1%, Latency P99 >3s, 5xx >10 in 5min
- **Dashboards:** Per-service operational dashboard
- **Retention:** 30 days minimum, 90 days for production

### 7.2 X-Ray (REQUIRED)
- **Tracing:** Enable active tracing on ALL Lambda functions
- **Sampling:** 1% high-volume, 100% low-volume
- **Annotations:** user_id, request_id, environment
- **Subsegments:** External API calls, database queries

### 7.3 Architecture Document Requirements
Every AWS project ARCHITECTURE.md MUST include:
- Section on CloudWatch configuration
- Section on X-Ray tracing
- Alarm definitions table
- Dashboard mockup or description

---

## 8.0 Example: Correct Architecture Document Header

```markdown
# Meeting Buddy - System Architecture

<!-- File UUID: xxx -->

## 1.0 Overview
Meeting Buddy uses AWS serverless architecture with real-time AI processing.

**Tech Stack (validated against hmode/guardrails/tech-preferences/):**
- **IaC:** AWS CDK 2.x (infrastructure.json rank 1)
- **LLM:** AWS Bedrock Claude Sonnet 4.5 global.anthropic.claude-sonnet-4-5-20250929-v1:0 (ai-ml.json rank 1)
- **ASR:** Deepgram Streaming API (ai-ml.json rank 1) OR AWS Transcribe (rank 4, justified below)
- **Frontend:** Next.js 15.x with React 19 (frontend.json rank 1)
- **UI Library:** shadcn/ui with Radix UI primitives (frontend.json rank 1)
- **Monitoring:** CloudWatch + X-Ray (REQUIRED per infrastructure.json:92-108)

**ASR Justification:** Using AWS Transcribe (rank 4) instead of Deepgram (rank 1) because:
- AWS-native integration simplifies architecture
- Speaker diarization built-in (up to 10 speakers)
- No external API dependencies
- Complies with infrastructure.json use case: "AWS-native apps"
```

---

## 9.0 Enforcement

### 9.1 AI Responsibility
- **MUST** run this checklist before creating Phase 6 documents
- **MUST** read guardrails for every technology decision
- **MUST** use exact versions from guardrails
- **MUST** document justification for non-rank-1 choices

### 9.2 Human Responsibility
- Review tech stack choices in design documents
- Approve technologies not in guardrails
- Update guardrails when new preferences established

### 9.3 Violation Handling
If guardrails violation detected:
1. **STOP** current work
2. **Read** relevant guardrails file
3. **Fix** design document with correct choices
4. **Restart** from corrected state

---

## 10.0 Quick Reference

| Document | Guardrails Check Required? | Plan Agent Required? |
|----------|---------------------------|----------------------|
| SPECIFICATION.md | No (user-facing) | No |
| ARCHITECTURE.md | **YES - infrastructure, ai-ml, frontend** | Yes (if 3+ docs) |
| API_DESIGN.md | Partial (check backend.json if relevant) | Yes (if 3+ docs) |
| DATABASE_SCHEMA.md | Partial (check backend.json databases) | Yes (if 3+ docs) |
| INPUT_OUTPUT_SPEC.md | No (data formats) | Yes (if 3+ docs) |
| TECH_STACK.md | **YES - all categories** | Yes (if 3+ docs) |
| IMPLEMENTATION_STRATEGY.md | Partial (code patterns) | Yes (if 3+ docs) |
| IMPLEMENTATION_PLAN.md | No (timeline) | Yes (if 3+ docs) |
| RISKS.md | No (risk assessment) | Yes (if 3+ docs) |

---

## 11.0 Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-02-05 | Initial guidelines based on Meeting Buddy violations |
