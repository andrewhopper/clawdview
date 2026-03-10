### Phase 5.5: REQUIREMENTS & PRD 📋 (NO CODE)

**Goal:** Document formal product requirements, PRD, and acceptance criteria

**Output:** `project-management/ideas/proto-name-xxxxx-NNN-requirements/` (3-5 pages total)

**Title:** `# Stage 5.5 - Requirements & PRD` (in each requirements doc)

---

## When to Use This Phase

**Skip Conditions:**

| Project Type | Phase 5.5 Required? | Rationale |
|--------------|---------------------|-----------|
| **exploration** | ❌ Skip | Learning-focused, no formal product |
| **spike** | ❌ Skip | Throwaway code, technical validation only |
| **prototype** | ⚠️ Optional | Quick validation, informal is acceptable |
| **production** | ✅ Required | Serious projects need formal documentation |

**Document in `.project` metadata:**
```json
{
  "metadata": {
    "prototype_type": "production",
    "requirements_phase_completed": true,
    "requirements_completed_at": "2025-01-20T14:00:00Z"
  }
}
```

---

## Required Deliverables

### 1. PRD.md (Product Requirements Document)

**Purpose:** Business context, goals, user stories, success metrics

**Structure:**

```markdown
# Stage 5.5 - Product Requirements Document

## 1.0 Executive Summary
- What: 1-2 sentence description
- Why: Problem being solved
- Who: Target users/audience
- Success: Primary metric

## 2.0 Background
- Problem statement
- Current state/pain points
- Opportunity
- Constraints

## 3.0 Goals & Non-Goals

### 3.1 Goals
- [Goal 1]: Measurable outcome
- [Goal 2]: Measurable outcome

### 3.2 Non-Goals
- [Explicitly out of scope]

## 4.0 User Stories

### 4.1 Primary Flows
- **As a [user type]**, I want to [action], so that [benefit]
- **As a [user type]**, I want to [action], so that [benefit]

### 4.2 Secondary Flows
- Edge cases
- Admin/configuration flows

## 5.0 Success Metrics
- Metric 1: [How measured, target]
- Metric 2: [How measured, target]

## 6.0 Assumptions & Dependencies
- Assumptions: [What we're assuming is true]
- Dependencies: [External systems, data, services]

## 7.0 Risks & Mitigations
- Risk 1: [Description] → Mitigation: [Strategy]
- Risk 2: [Description] → Mitigation: [Strategy]
```

**Page Limit:** 2-3 pages max

---

### 2. REQUIREMENTS.md (Functional & Non-Functional Requirements)

**Purpose:** Detailed requirements that the solution MUST satisfy

**Structure:**

```markdown
# Stage 5.5 - Requirements Specification

## 1.0 Functional Requirements

### 1.1 Core Features (Must Have)
- **FR-001**: [Requirement description]
  - Priority: P0 (must have)
  - Rationale: [Why critical]
  - Dependencies: [Other requirements]

- **FR-002**: [Requirement description]
  - Priority: P0 (must have)
  - Rationale: [Why critical]

### 1.2 Secondary Features (Should Have)
- **FR-101**: [Requirement description]
  - Priority: P1 (should have)
  - Rationale: [Value add]

### 1.3 Nice to Have (Could Have)
- **FR-201**: [Requirement description]
  - Priority: P2 (nice to have)
  - Future phase candidate

## 2.0 Non-Functional Requirements

### 2.1 Performance
- **NFR-001**: Response time < 500ms for 95th percentile
- **NFR-002**: Support 1000 concurrent users

### 2.2 Security
- **NFR-101**: Authentication via OAuth 2.0
- **NFR-102**: Encrypt data at rest (AES-256)
- **NFR-103**: HTTPS only (TLS 1.3)

### 2.3 Reliability
- **NFR-201**: 99.9% uptime SLA
- **NFR-202**: Automated failover < 30 seconds

### 2.4 Scalability
- **NFR-301**: Horizontal scaling to 10x load
- **NFR-302**: Handle 1M requests/day

### 2.5 Usability
- **NFR-401**: WCAG 2.1 AA accessibility compliance
- **NFR-402**: Mobile responsive (320px min width)

### 2.6 Maintainability
- **NFR-501**: 80%+ test coverage
- **NFR-502**: Type safety (TypeScript/mypy)
- **NFR-503**: Automated CI/CD pipeline

### 2.7 Observability
- **NFR-601**: Structured logging (JSON)
- **NFR-602**: Distributed tracing
- **NFR-603**: Metrics dashboards

## 3.0 Data Requirements
- **DR-001**: Support PostgreSQL 14+
- **DR-002**: Max record size 10MB
- **DR-003**: Retention policy: 90 days

## 4.0 Integration Requirements
- **IR-001**: REST API with OpenAPI 3.0 spec
- **IR-002**: Webhook support for events
- **IR-003**: SDK support (Python, TypeScript)

## 5.0 Compliance Requirements
- **CR-001**: GDPR compliant (data export, deletion)
- **CR-002**: SOC 2 Type II controls
- **CR-003**: Audit logging for all changes

## 6.0 Constraints
- Budget: $X per month infrastructure
- Timeline: Delivery by [date]
- Team: [size] engineers
- Tech stack: [Approved technologies from Phase 5]
```

**Page Limit:** 2-3 pages max

---

### 3. ACCEPTANCE_CRITERIA.md (Definition of Done)

**Purpose:** Testable criteria for success - what does "done" mean?

**Structure:**

```markdown
# Stage 5.5 - Acceptance Criteria

## 1.0 Feature Acceptance Criteria

### 1.1 User Registration (FR-001)
**Given** a new user visits the registration page
**When** they submit valid email and password
**Then**
- ✅ Account is created in database
- ✅ Confirmation email is sent
- ✅ User is redirected to welcome page
- ✅ Audit log entry created

**Edge Cases:**
- ❌ Duplicate email → Show error "Email already exists"
- ❌ Weak password → Show error "Password must be 12+ chars"
- ❌ Invalid email → Show error "Invalid email format"

### 1.2 User Login (FR-002)
**Given** a registered user visits the login page
**When** they submit valid credentials
**Then**
- ✅ JWT token issued (expires in 1 hour)
- ✅ User session created
- ✅ Last login timestamp updated
- ✅ User redirected to dashboard

**Edge Cases:**
- ❌ Invalid password → Show error, increment failed attempts
- ❌ Account locked → Show error "Account locked, contact support"
- ❌ Expired password → Redirect to password reset

## 2.0 Performance Acceptance Criteria

### 2.1 Response Times
- ✅ API endpoints: p50 < 100ms, p95 < 500ms, p99 < 1000ms
- ✅ Database queries: 95% < 50ms
- ✅ Page load time: First contentful paint < 1.5s

### 2.2 Load Testing
- ✅ 1000 concurrent users without degradation
- ✅ 10,000 requests/minute sustained for 1 hour
- ✅ CPU < 70% under peak load
- ✅ Memory < 80% under peak load

## 3.0 Security Acceptance Criteria

### 3.1 Authentication
- ✅ Passwords hashed with bcrypt (12 rounds)
- ✅ JWT tokens signed with RS256
- ✅ Refresh tokens rotated every 24 hours
- ✅ Failed login attempts rate limited (5 per 15 min)

### 3.2 Authorization
- ✅ Role-based access control (RBAC) enforced
- ✅ API endpoints check permissions
- ✅ Database queries filter by user permissions
- ✅ Admin actions require 2FA

### 3.3 Data Protection
- ✅ TLS 1.3 enforced (no fallback)
- ✅ PII encrypted at rest (AES-256)
- ✅ Secrets stored in secrets manager
- ✅ SQL injection prevention (parameterized queries)

## 4.0 Reliability Acceptance Criteria

### 4.1 Error Handling
- ✅ All errors logged with context
- ✅ User-facing error messages (no stack traces)
- ✅ Retry logic for transient failures (3 attempts, exponential backoff)
- ✅ Circuit breakers for external services

### 4.2 Data Integrity
- ✅ Database transactions for multi-step operations
- ✅ Foreign key constraints enforced
- ✅ Validation on write (schema validation)
- ✅ Backup/restore tested monthly

### 4.3 Monitoring
- ✅ Health check endpoint (200 OK if healthy)
- ✅ Metrics exported (Prometheus format)
- ✅ Alerts configured (error rate > 1%, latency > 1s)
- ✅ Dashboards created (Grafana)

## 5.0 Usability Acceptance Criteria

### 5.1 Accessibility
- ✅ WCAG 2.1 AA compliance (automated scan)
- ✅ Keyboard navigation (all interactive elements)
- ✅ Screen reader compatible (ARIA labels)
- ✅ Color contrast ratios ≥ 4.5:1

### 5.2 Responsive Design
- ✅ Mobile (320px - 767px): Single column layout
- ✅ Tablet (768px - 1023px): Two column layout
- ✅ Desktop (1024px+): Multi-column layout
- ✅ Touch targets ≥ 44x44px

### 5.3 Browser Support
- ✅ Chrome (last 2 versions)
- ✅ Firefox (last 2 versions)
- ✅ Safari (last 2 versions)
- ✅ Edge (last 2 versions)

## 6.0 Testing Acceptance Criteria

### 6.1 Test Coverage
- ✅ Unit tests: 80%+ coverage
- ✅ Integration tests: Critical paths covered
- ✅ E2E tests: Happy paths + 3 edge cases per feature
- ✅ Load tests: Peak load + 2x peak load

### 6.2 Test Quality
- ✅ Tests pass consistently (no flaky tests)
- ✅ Tests run in < 5 minutes
- ✅ Tests isolated (no shared state)
- ✅ Tests documented (describe intent)

## 7.0 Documentation Acceptance Criteria

### 7.1 Code Documentation
- ✅ README with setup instructions
- ✅ API documentation (OpenAPI spec)
- ✅ Architecture diagrams (current)
- ✅ Inline comments for complex logic

### 7.2 User Documentation
- ✅ User guide (getting started)
- ✅ FAQ (common questions)
- ✅ Troubleshooting guide
- ✅ Video walkthrough (optional)

## 8.0 Deployment Acceptance Criteria

### 8.1 CI/CD
- ✅ Automated build on commit
- ✅ Automated tests in CI
- ✅ Automated deployment to staging
- ✅ Manual approval for production
- ✅ Rollback procedure documented

### 8.2 Infrastructure
- ✅ Infrastructure as code (CDK/Terraform)
- ✅ Blue-green or canary deployment
- ✅ Database migrations automated (up + down)
- ✅ Secrets managed securely (not in code)

## 9.0 Definition of Done Checklist

**Before marking Phase 8 complete:**

- [ ] All P0 functional requirements implemented
- [ ] All non-functional requirements met
- [ ] All acceptance criteria pass
- [ ] Test coverage ≥ 80%
- [ ] Security scan passes (no high/critical issues)
- [ ] Load testing passes
- [ ] Documentation complete
- [ ] Code review approved
- [ ] Deployment successful (staging + production)
- [ ] Monitoring/alerts configured
- [ ] Runbook/troubleshooting guide written
- [ ] Post-launch support plan documented

**Optional (Phase 9 refinement):**
- [ ] Performance optimization (if < targets)
- [ ] UX improvements (if user feedback indicates)
- [ ] Additional edge cases handled
- [ ] Expanded browser/device support
```

**Page Limit:** 2-3 pages max

---

## Phase 5.5 Workflow

### 1. Entry Criteria (Phase 5 → 5.5 transition)
- ✅ Approach selected in Phase 5
- ✅ Output/audience alignment validated
- ✅ Technical feasibility confirmed (Phase 2.5 if production)
- ✅ Human approval to proceed

### 2. Phase 5.5 Execution

**Step 1: Draft PRD (AI generates, human reviews)**
- AI reads Phase 1 (SEED), Phase 5 (SELECTION)
- AI generates PRD.md using template above
- Human reviews: goals, user stories, success metrics
- Iterate until approved

**Step 2: Draft Requirements (AI generates, human reviews)**
- AI generates REQUIREMENTS.md from PRD
- Include functional + non-functional requirements
- Human reviews: completeness, priority, feasibility
- Iterate until approved

**Step 3: Draft Acceptance Criteria (AI generates, human reviews)**
- AI generates ACCEPTANCE_CRITERIA.md from requirements
- Use Given/When/Then format for functional criteria
- Include edge cases, performance targets, security requirements
- Human reviews: testability, coverage, realism
- Iterate until approved

**Step 4: Create requirements directory**
```bash
mkdir -p project-management/ideas/proto-name-xxxxx-NNN-requirements
mv PRD.md project-management/ideas/proto-name-xxxxx-NNN-requirements/
mv REQUIREMENTS.md project-management/ideas/proto-name-xxxxx-NNN-requirements/
mv ACCEPTANCE_CRITERIA.md project-management/ideas/proto-name-xxxxx-NNN-requirements/
```

**Step 5: Update `.project` file**
```json
{
  "current_phase": "REQUIREMENTS_AND_PRD",
  "phase_number": 5.5,
  "phase_history": [
    {
      "phase": "REQUIREMENTS_AND_PRD",
      "phase_number": 5.5,
      "started": "2025-01-20T10:00:00Z",
      "completed": "2025-01-20T14:00:00Z",
      "deliverables_completed": true
    }
  ],
  "metadata": {
    "prototype_type": "production",
    "requirements_phase_completed": true,
    "requirements_completed_at": "2025-01-20T14:00:00Z"
  }
}
```

### 3. Exit Criteria (Phase 5.5 → 6 transition)
- ✅ PRD.md complete and approved
- ✅ REQUIREMENTS.md complete and approved
- ✅ ACCEPTANCE_CRITERIA.md complete and approved
- ✅ Requirements are testable and measurable
- ✅ No conflicts between requirements
- ✅ Scope is clear (in/out of scope defined)
- ✅ Human approval to proceed to Phase 6

---

## Phase 5.5 Validation Gate

**AI presents summary to human:**

```markdown
# Phase 5.5 - Requirements Summary

## Overview
- **Project:** [name]
- **Type:** [production/prototype/exploration]
- **Phase:** 5.5 - Requirements & PRD

## Deliverables
- ✅ PRD.md (2 pages)
- ✅ REQUIREMENTS.md (3 pages)
- ✅ ACCEPTANCE_CRITERIA.md (3 pages)

## Key Stats
- Functional requirements: [count] (P0: X, P1: Y, P2: Z)
- Non-functional requirements: [count]
- Acceptance criteria: [count]
- User stories: [count]

## Scope Summary
**Must have:**
- [Requirement 1]
- [Requirement 2]

**Should have:**
- [Requirement 3]

**Out of scope:**
- [Item 1]
- [Item 2]

## Risks & Dependencies
- Risk: [Top risk] → Mitigation: [Strategy]
- Dependency: [Critical dependency]

## Review Checklist
- [ ] All requirements are testable
- [ ] No conflicts between requirements
- [ ] Priorities are clear (P0/P1/P2)
- [ ] Acceptance criteria cover happy + edge cases
- [ ] Non-functional requirements are measurable
- [ ] Scope is realistic for timeline/team

## Decision Required
Approve Phase 5.5 completion and proceed to Phase 6 (Design)?

**Options:**
- ✅ Approve (proceed to Phase 6)
- 🔄 Revise (iterate on requirements)
- ❌ Reject (re-evaluate approach in Phase 5)
```

**Human actions:** `approve`, `revise`, `reject`

---

## Best Practices

### 1. Requirements Writing

**Good Requirements:**
- ✅ Testable: Can be verified with clear pass/fail
- ✅ Measurable: Quantifiable targets (%, seconds, count)
- ✅ Unambiguous: One interpretation only
- ✅ Traceable: Linked to user story/business goal
- ✅ Feasible: Achievable with available resources

**Bad Requirements:**
- ❌ "System should be fast" (not measurable)
- ❌ "Users should love the UI" (not testable)
- ❌ "Support scale" (not specific)
- ❌ "Be secure" (too vague)

**Example - Before/After:**

**Before (bad):**
> "System should handle lots of users"

**After (good):**
> "NFR-301: System shall support 1000 concurrent users with p95 response time < 500ms under load test for 1 hour sustained"

### 2. Acceptance Criteria Format

**Use Given/When/Then (Gherkin) format:**

```gherkin
Given [precondition/context]
When [action/trigger]
Then [expected outcome]
```

**Example:**
```gherkin
Given a user with 2FA enabled
When they attempt login with valid credentials
Then
  - Username/password validated
  - 2FA prompt displayed
  - SMS code sent
  - Login pending until 2FA verified
```

### 3. Prioritization (MoSCoW)

| Priority | Label | Meaning | Phase |
|----------|-------|---------|-------|
| **P0** | Must Have | Blocking for MVP | Phase 8 |
| **P1** | Should Have | Important but not blocking | Phase 9 or later |
| **P2** | Could Have | Nice to have, future phase | Future |
| **P3** | Won't Have | Out of scope, never | N/A |

### 4. Non-Functional Requirements Categories

Use this checklist to ensure comprehensive NFRs:

- [ ] **Performance:** Response time, throughput, latency
- [ ] **Security:** Authentication, authorization, encryption, compliance
- [ ] **Reliability:** Uptime, failover, disaster recovery, data integrity
- [ ] **Scalability:** Horizontal/vertical scaling, load capacity
- [ ] **Usability:** Accessibility, responsiveness, browser support
- [ ] **Maintainability:** Test coverage, type safety, code quality, CI/CD
- [ ] **Observability:** Logging, metrics, tracing, alerting
- [ ] **Operability:** Deployment, rollback, health checks, runbooks
- [ ] **Compliance:** GDPR, SOC 2, HIPAA, industry-specific regulations
- [ ] **Compatibility:** Browser versions, API versions, backward compatibility

### 5. Scope Management

**Explicitly document out-of-scope items:**

```markdown
## Out of Scope (Phase 5.5)
- Mobile native apps (iOS/Android) - Web only
- Real-time collaboration (future phase)
- Multi-language support (English only for MVP)
- Advanced analytics (basic metrics only)
```

**Why:** Prevents scope creep, sets expectations, focuses effort

---

## Common Pitfalls

### ❌ Pitfall 1: Requirements too vague
**Problem:** "System should be secure"
**Solution:** "System shall encrypt data at rest (AES-256), enforce TLS 1.3, hash passwords (bcrypt 12 rounds), implement RBAC with least privilege"

### ❌ Pitfall 2: Acceptance criteria not testable
**Problem:** "Users should be happy with the UI"
**Solution:** "95% of test users complete checkout in < 3 minutes on first attempt (measured via user testing)"

### ❌ Pitfall 3: Missing non-functional requirements
**Problem:** Only functional requirements listed
**Solution:** Include performance, security, reliability, scalability, usability, maintainability, observability

### ❌ Pitfall 4: Conflicts between requirements
**Problem:** "FR-001: Support 10,000 users" + "NFR-001: Infrastructure cost < $100/month"
**Solution:** Validate requirements don't conflict, adjust priorities, or negotiate trade-offs

### ❌ Pitfall 5: Premature design decisions
**Problem:** Requirements specify technology choices
**Solution:** Requirements describe WHAT, not HOW. Save technology decisions for Phase 6 (Design)

**Example - Before/After:**

**Before (too specific):**
> "FR-001: Use PostgreSQL database to store user data"

**After (requirement, not design):**
> "FR-001: Persist user data with ACID guarantees, support transactions, handle 1M records with sub-50ms query time"

---

## Phase 5.5 Summary

**Inputs:**
- Phase 5 selection output
- Phase 1 SEED document
- Target output/audience from Phase 1

**Outputs:**
- PRD.md (2-3 pages)
- REQUIREMENTS.md (2-3 pages)
- ACCEPTANCE_CRITERIA.md (2-3 pages)

**Duration:** 2-4 hours (production), 0 hours (skip for exploration/spike)

**Gate:** Human approval required before Phase 6

**Next Phase:** Phase 6 - Technical Design (architecture, API design, data models)
