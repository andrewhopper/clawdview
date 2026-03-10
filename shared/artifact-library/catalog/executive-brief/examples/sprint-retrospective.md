# Sprint Retrospective: Checkout Redesign (Sprint 14)

**Domain:** Agile / Team Process
**Artifact Type:** Sprint Retrospective
**Harvested:** 2025-11-25
**Source Pattern:** Agile Retrospectives (Derby & Larsen), Spotify Retro Format

---

## Retrospective Summary

| Field | Value |
|-------|-------|
| **Team** | Checkout Squad |
| **Sprint** | Sprint 14 (Nov 11-22, 2025) |
| **Sprint Goal** | Launch new one-page checkout flow |
| **Facilitator** | Jamie Rodriguez |
| **Participants** | 8 (full team) |
| **Duration** | 90 minutes |
| **Date** | November 22, 2025 |

---

## 1.0 Sprint Metrics

### 1.1 Commitment vs. Delivery

| Metric | Committed | Delivered | % |
|--------|-----------|-----------|---|
| Story points | 34 | 29 | 85% |
| Stories completed | 8 | 6 | 75% |
| Bugs fixed | 5 | 7 | 140% |
| Tech debt items | 2 | 1 | 50% |

### 1.2 Quality Metrics

| Metric | This Sprint | Last Sprint | Trend |
|--------|-------------|-------------|-------|
| Bugs escaped to prod | 2 | 4 | ✅ Improving |
| Test coverage | 78% | 72% | ✅ Improving |
| Code review turnaround | 4.2 hrs | 8.1 hrs | ✅ Improving |
| Deploy frequency | 12 | 8 | ✅ Improving |

### 1.3 Sprint Goal Assessment

**Goal:** Launch new one-page checkout flow

**Status:** ⚠️ Partially Achieved

- ✅ New checkout UI deployed to 25% of traffic
- ✅ Payment integration complete
- ❌ Address autocomplete deferred (API issues)
- ❌ Guest checkout not started (blocked by auth team)

---

## 2.0 What Went Well 🌟

### 2.1 Team Collaboration

> "Pair programming sessions on the payment integration were incredibly productive. We solved in 2 hours what would have taken days solo."
> — *Alex, Senior Engineer*

**Specifics:**
- 3 pair programming sessions held
- Cross-functional pairing (frontend + backend)
- Knowledge shared across team

**Action:** Continue weekly pairing sessions

---

### 2.2 Faster Code Reviews

> "The new review SLA of 4 hours made a huge difference. No more waiting days for feedback."
> — *Priya, Engineer*

**Specifics:**
- Average review time dropped from 8.1 → 4.2 hours
- Team adopted "review before lunch, review before EOD" rhythm
- Smaller PRs (avg 180 lines vs. 340 last sprint)

**Action:** Formalize PR size guidelines (<200 lines)

---

### 2.3 Early Testing Involvement

> "QA joining sprint planning helped us catch edge cases before we wrote code."
> — *Marcus, QA Engineer*

**Specifics:**
- QA wrote test cases during sprint planning
- 4 edge cases identified before development started
- Reduced bug count in review by 60%

**Action:** Make QA sprint planning participation standard

---

## 3.0 What Didn't Go Well 🔴

### 3.1 External Dependency Blocking

> "We lost 3 days waiting for the Auth team to expose the guest checkout API."
> — *Sarah, Tech Lead*

**Specifics:**
- Guest checkout story blocked entire sprint
- No visibility into Auth team's roadmap
- Escalation took 2 days to get response

**Impact:** 8 story points couldn't be completed

**Root Cause:** No cross-team dependency tracking

---

### 3.2 Scope Creep Mid-Sprint

> "The 'small' request from Product to add promo codes turned into 2 days of work."
> — *Alex, Senior Engineer*

**Specifics:**
- Promo code feature added on Day 4
- Estimated at 3 points, actual was 8
- Displaced planned tech debt work

**Impact:** Tech debt item deferred, increased future risk

**Root Cause:** Insufficient pushback on mid-sprint changes

---

### 3.3 Flaky Tests in CI

> "I reran the pipeline 4 times yesterday. Each time different tests failed randomly."
> — *David, Engineer*

**Specifics:**
- 12 flaky tests identified
- Average of 2.3 reruns per PR
- ~45 minutes lost per PR to flakiness

**Impact:** 6+ hours of team time wasted

**Root Cause:** Test isolation issues, shared database state

---

## 4.0 Action Items

### 4.1 High Priority (Start Immediately)

| Action | Owner | Due | Success Metric |
|--------|-------|-----|----------------|
| Create cross-team dependency board | Sarah | Nov 25 | Dependencies visible 2 sprints ahead |
| Fix top 5 flaky tests | David | Nov 27 | CI pass rate >95% |
| Define mid-sprint change policy | Jamie | Nov 26 | Policy documented, PM aligned |

### 4.2 Medium Priority (This Sprint)

| Action | Owner | Due | Success Metric |
|--------|-------|-----|----------------|
| PR size linting (>200 lines = warning) | Alex | Dec 4 | Avg PR size <200 lines |
| QA test case template for planning | Marcus | Dec 4 | Template in Confluence |
| Pairing schedule published weekly | Priya | Ongoing | 2+ sessions per week |

### 4.3 Low Priority (Backlog)

| Action | Owner | Due | Success Metric |
|--------|-------|-----|----------------|
| Investigate test parallelization | David | TBD | CI time <10 min |
| Cross-team retro with Auth team | Sarah | TBD | Joint session scheduled |

---

## 5.0 Kudos & Recognition 🎉

| Person | Recognition |
|--------|-------------|
| **Alex** | Stayed late to help onboard new team member |
| **Priya** | Caught critical security issue in code review |
| **Marcus** | Test automation saved 4 hours of manual testing |
| **David** | Refactored payment module—cleaner and faster |
| **Sarah** | Shielded team from stakeholder chaos mid-sprint |

---

## 6.0 Team Health Check

**Rate 1-5 (1=needs attention, 5=excellent)**

| Dimension | Score | Trend | Notes |
|-----------|-------|-------|-------|
| **Collaboration** | 4.5 | ↑ | Pairing helping |
| **Psychological safety** | 4.0 | → | Stable |
| **Sustainable pace** | 3.0 | ↓ | Scope creep causing stress |
| **Technical practices** | 3.5 | ↑ | Testing improving |
| **Delivery confidence** | 3.5 | → | Dependencies hurt |
| **Fun** | 4.0 | ↑ | Team lunch helped |

**Focus area for next sprint:** Sustainable pace (address scope creep)

---

## 7.0 Experiments

### 7.1 Current Experiments

| Experiment | Started | Status | Result |
|------------|---------|--------|--------|
| 4-hour code review SLA | Sprint 13 | ✅ Keep | Review time halved |
| QA in sprint planning | Sprint 14 | ✅ Keep | Bugs down 60% |
| No meetings Wednesday | Sprint 14 | 🔄 Continue | Need more data |

### 7.2 New Experiment

**Experiment:** "No mid-sprint scope additions without trade-off"

**Hypothesis:** If we require removing equal story points for any addition, scope creep will decrease and sprint predictability will improve.

**Measurement:**
- Sprint commitment vs. delivery %
- Team stress (survey)
- Stakeholder satisfaction

**Duration:** 2 sprints

**Decision criteria:** Keep if delivery % >90% and stakeholder satisfaction maintained

---

## 8.0 Looking Ahead

### 8.1 Next Sprint Focus

1. Complete guest checkout (dependency resolved)
2. Address autocomplete integration
3. Performance optimization (checkout load time <2s)

### 8.2 Risks to Monitor

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Auth API delays again | Medium | Daily standup sync with Auth team |
| Holiday traffic spike | High | Load testing scheduled Nov 28 |
| Team member PTO | Low | Knowledge sharing this sprint |

---

## 9.0 Retro Feedback

**How was this retro?**

| Rating | Count |
|--------|-------|
| 😀 Great | 5 |
| 🙂 Good | 2 |
| 😐 Okay | 1 |
| 😕 Poor | 0 |

**Suggestions for next time:**
- "Try the sailboat format for variety"
- "More time on action items, less on venting"

---

## Appendices

- A: Sprint burndown chart
- B: Velocity trend (last 6 sprints)
- C: Full team health survey results
- D: Dependency board screenshot

---

## Why This Is Best-in-Class

1. **Data-driven:** Metrics before opinions, trends shown
2. **Balanced:** Both celebrations and problems addressed
3. **Actionable:** Specific owners, dates, and success metrics
4. **Experiment mindset:** Treats process changes as hypotheses
5. **Team health focus:** Monitors sustainable pace and morale
6. **Forward-looking:** Risks and next sprint clearly outlined
