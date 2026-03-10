# 5 Whys Analysis: Production Payment Processing Outage

**Domain:** Operations / Root Cause Analysis
**Artifact Type:** 5 Whys Analysis
**Harvested:** 2025-11-25
**Source Pattern:** Toyota Production System, Lean Six Sigma

---

## Incident Summary

| Field | Value |
|-------|-------|
| **Incident ID** | INC-2025-1847 |
| **Date** | November 18, 2025 |
| **Duration** | 2 hours 14 minutes |
| **Severity** | SEV-1 (Critical) |
| **Impact** | 12,400 failed transactions, $847K revenue affected |
| **Facilitator** | Maria Santos, SRE Lead |
| **Participants** | Platform Team, Payments Team, On-call Engineers |

---

## 1.0 Problem Statement

**What happened?**

On November 18, 2025 at 14:23 UTC, the payment processing service began returning 500 errors for 100% of transaction requests. The outage lasted 2 hours 14 minutes until service was restored at 16:37 UTC.

**Business Impact:**
- 12,400 failed customer transactions
- $847,000 in potentially lost revenue
- 340 customer support tickets
- Social media mentions: 89 (negative sentiment)

---

## 2.0 The 5 Whys Analysis

### Why #1: Why did payments fail?

**Answer:** The payment service couldn't connect to the database.

**Evidence:**
- Error logs: `FATAL: connection to database "payments_prod" failed`
- Connection pool exhausted (0/100 available)
- Database connection timeout errors in APM

---

### Why #2: Why couldn't the service connect to the database?

**Answer:** All database connections were held by long-running queries that never completed.

**Evidence:**
- `pg_stat_activity` showed 100 connections in "active" state
- Oldest query running for 47 minutes
- All queries were the same: `SELECT * FROM transactions WHERE...`

---

### Why #3: Why were queries running so long?

**Answer:** A missing database index caused full table scans on a table with 450 million rows.

**Evidence:**
- `EXPLAIN ANALYZE` showed sequential scan (no index used)
- Table `transactions` has 450M rows, 128GB
- Query plan estimated 45 minutes for full scan
- Index on `customer_id` was missing

---

### Why #4: Why was the index missing?

**Answer:** A database migration removed the index during a schema change, and it was never recreated.

**Evidence:**
- Migration `20251015_refactor_transactions.sql` included `DROP INDEX idx_transactions_customer_id`
- No corresponding `CREATE INDEX` in migration
- Migration author confirmed oversight
- Code review didn't catch the issue

---

### Why #5: Why didn't code review catch the missing index recreation?

**Answer:** There was no checklist or automated validation for database migrations that modify indexes.

**Evidence:**
- Migration review process is manual and informal
- No CI check for index coverage on query patterns
- No pre-deployment query performance validation
- Reviewer focused on schema correctness, not performance

---

## 3.0 Root Cause

**Primary Root Cause:**

Lack of automated validation in the database migration pipeline to ensure query performance is not degraded by schema changes.

**Contributing Factors:**

| Factor | Category | Impact |
|--------|----------|--------|
| Missing index recreation in migration | Human Error | Direct cause |
| No CI check for index coverage | Process Gap | Failed to catch |
| No query performance testing | Process Gap | Failed to catch |
| Manual migration review | Process Gap | Inconsistent quality |
| Large table (450M rows) | Technical Debt | Amplified impact |

---

## 4.0 Corrective Actions

### 4.1 Immediate (This Week)

| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Recreate missing index | @db-team | Nov 19 | ✅ Done |
| Add connection pool monitoring alert | @sre-team | Nov 20 | ✅ Done |
| Document incident in runbook | @maria | Nov 21 | ✅ Done |

### 4.2 Short-Term (This Sprint)

| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Create migration review checklist | @platform | Nov 29 | 🔄 In Progress |
| Add CI check for `DROP INDEX` statements | @platform | Nov 29 | 🔄 In Progress |
| Implement slow query alerting (<1s p99) | @sre-team | Dec 1 | ⏳ Planned |

### 4.3 Long-Term (This Quarter)

| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Automated index coverage analysis in CI | @platform | Dec 15 | ⏳ Planned |
| Query performance regression testing | @qa-team | Jan 15 | ⏳ Planned |
| Database migration staging environment | @infra | Jan 30 | ⏳ Planned |
| Table partitioning for transactions | @db-team | Feb 28 | ⏳ Planned |

---

## 5.0 Prevention Checklist

**For future database migrations, verify:**

- [ ] All dropped indexes are intentional and documented
- [ ] Replacement indexes are created if query patterns require them
- [ ] `EXPLAIN ANALYZE` run on affected queries with production-like data
- [ ] Migration tested in staging with production data volume
- [ ] Rollback plan documented and tested
- [ ] Connection pool impact assessed for long-running migrations

---

## 6.0 Timeline of Events

```
14:23 UTC  First 500 errors in payment service
14:25 UTC  PagerDuty alert triggered (error rate >1%)
14:27 UTC  On-call engineer acknowledges
14:35 UTC  Initial diagnosis: database connection failures
14:48 UTC  Escalation to database team
15:02 UTC  Identified long-running queries
15:21 UTC  Discovered missing index
15:34 UTC  Decision: kill queries and recreate index
15:41 UTC  Queries terminated, connections freed
15:45 UTC  Index creation started (CONCURRENTLY)
16:32 UTC  Index creation completed
16:37 UTC  Service fully restored
16:45 UTC  All-clear announced
```

---

## 7.0 Metrics

### 7.1 Detection

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Time to detect | 2 min | <5 min | ✅ Met |
| Time to acknowledge | 4 min | <10 min | ✅ Met |
| Time to escalate | 25 min | <15 min | ❌ Missed |

### 7.2 Resolution

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Time to identify root cause | 58 min | <30 min | ❌ Missed |
| Time to mitigate | 78 min | <60 min | ❌ Missed |
| Time to resolve | 134 min | <120 min | ❌ Missed |

### 7.3 Impact

| Metric | Value |
|--------|-------|
| Failed transactions | 12,400 |
| Revenue impact | $847,000 |
| Customer tickets | 340 |
| SLA breach | Yes (99.9% → 98.7%) |

---

## 8.0 Lessons Learned

### What Went Well

1. **Alerting worked** — PagerDuty triggered within 2 minutes of first errors
2. **Team collaboration** — Cross-team war room formed quickly
3. **Rollback decision** — Team chose safe path (kill + recreate) over risky fixes

### What Needs Improvement

1. **Escalation speed** — Took 25 min to involve database experts
2. **Runbook gaps** — No runbook for "connection pool exhausted" scenario
3. **Index visibility** — No easy way to see index changes in PRs
4. **Staging parity** — Staging has 1% of production data, didn't surface issue

---

## 9.0 Follow-Up Review

**Scheduled:** December 2, 2025 at 10:00 AM

**Agenda:**
1. Review action item completion
2. Validate new CI checks working
3. Demo staging environment with production data
4. Close or extend any open items

---

## Appendices

- A: Full error logs (link)
- B: Database query plan analysis
- C: Migration file that caused issue
- D: PagerDuty timeline export

---

## Why This Is Best-in-Class

1. **Clear problem statement:** Quantified impact upfront
2. **Evidence-based:** Each "why" supported by specific evidence
3. **True root cause:** Reached systemic issue, not just human error
4. **Actionable outcomes:** Specific actions with owners and deadlines
5. **Prevention focus:** Checklist and process changes to prevent recurrence
6. **Blameless tone:** Focus on process, not individuals
