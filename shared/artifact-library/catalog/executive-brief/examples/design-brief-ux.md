# Design Brief: Mobile Banking App Redesign

**Domain:** Product Design / UX
**Artifact Type:** Design Brief
**Harvested:** 2025-11-25
**Source Pattern:** [UXPin Design Brief Template](https://www.uxpin.com/studio/blog/design-brief/), [Interaction Design Foundation](https://www.interaction-design.org/literature/topics/design-briefs)

---

## Project Summary

| Field | Value |
|-------|-------|
| **Project** | Horizon Bank Mobile App Redesign |
| **Client** | Horizon Bank (Internal) |
| **Project Lead** | Sarah Chen, Head of Digital Experience |
| **Design Team** | UX Lab (3 designers, 1 researcher) |
| **Duration** | 12 weeks |
| **Budget** | $180,000 |

---

## 1.0 Executive Summary

Redesign Horizon Bank's mobile banking application to improve user engagement, reduce support calls, and increase mobile deposit adoption. Current app suffers from dated UI, confusing navigation, and 2.8-star app store rating threatening customer retention.

**Design Challenge:** Create an intuitive, accessible mobile banking experience that increases daily active users by 40% and reduces "how do I..." support calls by 60%.

---

## 2.0 Background & Context

### 2.1 Current State

| Metric | Current | Industry Avg | Gap |
|--------|---------|--------------|-----|
| App Store rating | 2.8 ★ | 4.2 ★ | -1.4 |
| DAU/MAU ratio | 18% | 35% | -17pts |
| Mobile deposit adoption | 23% | 52% | -29pts |
| Support calls (mobile) | 4,200/mo | — | Target: <1,700 |
| Task completion rate | 67% | 89% | -22pts |

### 2.2 Competitive Landscape

| Competitor | Strengths | Weaknesses |
|------------|-----------|------------|
| Chase | Biometric login, clean UI | Feature bloat |
| Capital One | Conversational UI, Eno assistant | Limited branch integration |
| Chime | Simple, millennial-focused | No branch services |
| Current app | Branch locator, human support | Everything else |

### 2.3 Business Drivers

1. **Customer attrition:** 12% of churned customers cited "app experience" as factor
2. **Cost reduction:** $8.50 avg cost per support call vs. $0.12 per self-service
3. **Competitive pressure:** 3 regional competitors launched updated apps in 2024
4. **Regulatory:** WCAG 2.1 AA compliance required by Q2 2026

---

## 3.0 Target Audience

### 3.1 Primary Personas

**Persona 1: Busy Professional (45% of users)**
| Attribute | Detail |
|-----------|--------|
| Age | 28-45 |
| Income | $75K-150K |
| Behavior | Quick balance checks, transfers, bill pay |
| Pain points | Too many taps, slow load times |
| Success metric | Complete common tasks in <30 seconds |

**Persona 2: Digital-Hesitant Senior (25% of users)**
| Attribute | Detail |
|-----------|--------|
| Age | 55-75 |
| Income | $40K-80K |
| Behavior | Monthly statement review, occasional transfers |
| Pain points | Small text, confusing icons, fear of errors |
| Success metric | Complete tasks without calling support |

**Persona 3: Young Saver (20% of users)**
| Attribute | Detail |
|-----------|--------|
| Age | 18-27 |
| Income | $25K-55K |
| Behavior | Savings goals, P2P payments, spending insights |
| Pain points | Lack of budgeting tools, boring interface |
| Success metric | Weekly engagement with savings features |

### 3.2 Accessibility Requirements

- WCAG 2.1 AA compliance (mandatory)
- Screen reader compatibility (VoiceOver, TalkBack)
- Minimum touch target: 44x44px
- Color contrast ratio: 4.5:1 minimum
- Support for dynamic type scaling

---

## 4.0 Project Goals

### 4.1 Business Objectives

| Goal | Baseline | Target | Deadline |
|------|----------|--------|----------|
| App store rating | 2.8 ★ | 4.3 ★ | Q2 2026 |
| DAU/MAU ratio | 18% | 35% | Q3 2026 |
| Mobile deposit adoption | 23% | 45% | Q4 2026 |
| Support call reduction | 4,200/mo | 1,700/mo | Q2 2026 |

### 4.2 Design Objectives

| Objective | Metric | Target |
|-----------|--------|--------|
| Task completion rate | Usability testing | >90% |
| Time-on-task (transfer) | Usability testing | <25 seconds |
| System Usability Scale | Post-launch survey | >80 |
| Error rate | Analytics | <2% |

### 4.3 Non-Goals (Out of Scope)

1. Backend system changes (API contracts fixed)
2. New banking products or features
3. Web banking redesign (separate project)
4. Branch experience integration
5. Chatbot/AI assistant implementation

---

## 5.0 Design Requirements

### 5.1 Brand Guidelines

| Element | Specification |
|---------|---------------|
| Primary color | Horizon Blue (#1E3A8A) |
| Secondary | Warm Gray (#6B7280) |
| Accent | Success Green (#059669) |
| Typography | SF Pro (iOS), Roboto (Android) |
| Logo | Horizontal lockup, min 24px height |
| Tone | Professional, approachable, trustworthy |

**Brand assets:** `drive.google.com/horizon-brand-2024`

### 5.2 Technical Constraints

| Constraint | Requirement |
|------------|-------------|
| Platforms | iOS 15+, Android 10+ |
| Offline mode | View cached balances, queue transactions |
| Biometrics | Face ID, Touch ID, fingerprint required |
| Session timeout | 5 minutes inactive (regulatory) |
| API latency | Design for <2s response times |

### 5.3 Design System

- Extend existing Horizon Design System (Figma)
- Component library: `figma.com/horizon-ds-v2`
- Follow atomic design methodology
- Document all new components

---

## 6.0 Existing Research & Artifacts

### 6.1 Available Research

| Asset | Location | Date |
|-------|----------|------|
| User personas (5) | `drive/research/personas` | Mar 2024 |
| Journey maps (3 flows) | `drive/research/journeys` | Mar 2024 |
| Competitive analysis | `drive/research/competitive` | Jan 2024 |
| Support call analysis | `drive/research/support-themes` | Apr 2024 |
| App store reviews (coded) | `drive/research/reviews` | May 2024 |

### 6.2 Research Gaps

| Gap | Planned Research |
|-----|------------------|
| Senior user behaviors | 8 contextual inquiries (Week 2) |
| Accessibility audit | WCAG evaluation (Week 1) |
| Feature prioritization | Card sorting with 24 users (Week 3) |

---

## 7.0 Deliverables

### 7.1 Required Outputs

| Deliverable | Format | Deadline |
|-------------|--------|----------|
| Research synthesis | Notion doc | Week 3 |
| Information architecture | FigJam sitemap | Week 4 |
| Low-fidelity wireframes | Figma (grayscale) | Week 5 |
| Usability test results (v1) | Notion report | Week 6 |
| High-fidelity mockups | Figma (all states) | Week 8 |
| Interactive prototype | Figma prototype | Week 9 |
| Usability test results (v2) | Notion report | Week 10 |
| Design specs | Figma dev mode | Week 11 |
| Component documentation | Storybook | Week 12 |

### 7.2 File Specifications

| Asset Type | Format | Naming Convention |
|------------|--------|-------------------|
| Mockups | Figma | `HB-Mobile-[Screen]-[State]-v[#]` |
| Icons | SVG, PNG @1x/2x/3x | `icon-[name]-[size]` |
| Illustrations | SVG | `illust-[name]` |
| Animations | Lottie JSON | `anim-[name]` |
| Handoff | Figma Dev Mode | — |

---

## 8.0 Timeline & Milestones

### 8.1 Project Phases

```
Week 1-3: Discovery & Research
    │
    ▼
Week 4-5: Information Architecture & Wireframes
    │
    ▼
Week 6: Usability Testing Round 1
    │
    ▼
Week 7-9: Visual Design & Prototyping
    │
    ▼
Week 10: Usability Testing Round 2
    │
    ▼
Week 11-12: Refinement & Handoff
```

### 8.2 Key Milestones

| Milestone | Date | Stakeholders |
|-----------|------|--------------|
| Kickoff | Week 1, Mon | All |
| Research readout | Week 3, Fri | Leadership |
| Wireframe review | Week 5, Wed | Product, Eng |
| Usability findings v1 | Week 6, Fri | All |
| Design review | Week 9, Wed | Leadership |
| Usability findings v2 | Week 10, Fri | All |
| Final handoff | Week 12, Fri | Engineering |

### 8.3 Feedback Cadence

- **Daily standups:** 15 min, design team only
- **Weekly syncs:** 30 min with Product Manager
- **Bi-weekly reviews:** 60 min with stakeholders
- **Async feedback:** Figma comments, 24hr response SLA

---

## 9.0 Budget Allocation

| Category | Amount | % |
|----------|--------|---|
| Research (recruiting, incentives) | $25,000 | 14% |
| Design tools & subscriptions | $8,000 | 4% |
| Design team (3 designers × 12 weeks) | $120,000 | 67% |
| UX research (1 researcher × 6 weeks) | $20,000 | 11% |
| Contingency | $7,000 | 4% |
| **Total** | **$180,000** | 100% |

---

## 10.0 Success Criteria

### 10.1 Design Quality Gates

| Gate | Criteria | Owner |
|------|----------|-------|
| Wireframe approval | Stakeholder sign-off | Product |
| Usability v1 | >75% task completion | Research |
| Visual design approval | Brand team sign-off | Brand |
| Usability v2 | >85% task completion, SUS >75 | Research |
| Accessibility | WCAG 2.1 AA pass | QA |
| Engineering handoff | Dev feasibility confirmed | Engineering |

### 10.2 Launch Success Metrics

Measured 90 days post-launch:
- App store rating ≥4.0
- Task completion rate ≥85%
- Support calls ≤2,500/month
- No critical accessibility issues

---

## 11.0 Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep | High | High | Strict change control, documented non-goals |
| Stakeholder alignment | Medium | High | Bi-weekly reviews, early concept sharing |
| Technical constraints | Medium | Medium | Weekly eng sync, feasibility checks |
| Research recruiting | Medium | Low | Partner with existing customer panels |
| Timeline pressure | High | Medium | Prioritized feature list, MVP scope |

---

## 12.0 Team & Contacts

| Role | Name | Responsibility |
|------|------|----------------|
| Project Sponsor | Sarah Chen | Strategic direction, approvals |
| Product Manager | Mike Torres | Requirements, prioritization |
| Lead Designer | Emma Wilson | Design direction, stakeholder mgmt |
| Senior Designer | James Park | Visual design, design system |
| UX Designer | Priya Sharma | Interaction design, prototyping |
| UX Researcher | Alex Rivera | Research planning, synthesis |
| Engineering Lead | David Kim | Technical feasibility, handoff |

---

## 13.0 Appendices

- A: Current app screenshots & audit
- B: Competitor app analysis
- C: Brand guidelines (full)
- D: Technical architecture overview
- E: Previous research reports

---

## Why This Is Best-in-Class

1. **Comprehensive scope:** Covers all aspects from research to handoff
2. **Measurable goals:** Specific metrics with baselines and targets
3. **Clear constraints:** Technical limitations and non-goals explicit
4. **Structured timeline:** Phased approach with defined milestones
5. **Risk awareness:** Proactive identification with mitigations
6. **Stakeholder clarity:** Roles, responsibilities, and feedback cadence defined
