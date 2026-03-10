# Violation Tracking System

<!-- File UUID: 6d9e8f3a-7c5b-4e2f-9a6d-7c8b4e5f2a3c -->

## 1.0 Overview

Track violations over time to show compliance trends and inform policy decisions.

## 2.0 Tracking Database

### 2.1 Schema

```sql
CREATE TABLE violations (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    file_path TEXT,
    message TEXT NOT NULL,
    mode TEXT NOT NULL,  -- LOG, WARN, APPROVAL_REQUIRED, BLOCK
    severity TEXT,  -- rank_1, rank_2_3, rank_4_plus, not_listed
    allowed BOOLEAN NOT NULL,
    approved_by_user BOOLEAN,
    context_phase TEXT,
    context_project_type TEXT,
    context_environment TEXT
);

CREATE INDEX idx_timestamp ON violations(timestamp);
CREATE INDEX idx_rule_id ON violations(rule_id);
CREATE INDEX idx_mode ON violations(mode);
```

### 2.2 Storage Location

```
.guardrails/.violations.db  (SQLite)
```

## 3.0 Tracking API

```python
from overwatch_guardrails import ViolationTracker

tracker = ViolationTracker(".guardrails/.violations.db")

# Log a violation
tracker.log_violation(
    rule_id="unapproved-dependency",
    file_path="package.json",
    message="Package 'angular' not approved",
    mode=EnforcementMode.APPROVAL_REQUIRED,
    severity="not_listed",
    allowed=False,
    approved_by_user=True,  # User approved it
    context={"phase": "phase_8"}
)

# Query violations
violations = tracker.get_violations(
    rule_id="unapproved-dependency",
    since="2026-01-01",
    mode=EnforcementMode.BLOCK
)

# Get trends
trends = tracker.get_trends(days=30)
# Returns: {
#   "total": 145,
#   "by_mode": {"LOG": 100, "WARN": 40, "APPROVAL_REQUIRED": 5, "BLOCK": 0},
#   "by_severity": {"rank_2_3": 40, "not_listed": 5}
# }
```

## 4.0 Compliance Reporting

### 4.1 Project Compliance Over Time

```python
# Show compliance improvement across phases
report = tracker.get_compliance_by_phase()

# Output:
# Phase 1: 45 violations (LOG: 40, WARN: 5)
# Phase 2: 38 violations (LOG: 35, WARN: 3)
# Phase 8: 5 violations (LOG: 5, WARN: 0)
# Phase 9: 0 violations
```

### 4.2 Rule Effectiveness

```python
# Which rules trigger most?
stats = tracker.get_rule_stats(days=30)

# Output:
# unapproved-dependency: 25 violations (20 approved, 5 blocked)
# raw-hex-colors: 15 violations (15 warnings)
# file-size-limit: 50 violations (50 logged)
```

## 5.0 Historical Queries

```python
# Violations by time range
violations = tracker.query(
    start_date="2026-01-01",
    end_date="2026-01-15",
    rule_id="unapproved-dependency"
)

# Violations requiring approval
pending = tracker.query(
    mode=EnforcementMode.APPROVAL_REQUIRED,
    allowed=False
)

# Violations by file
file_violations = tracker.query(
    file_path="package.json",
    since="2026-01-01"
)
```

## 6.0 Audit Trail

All user decisions are logged:

```python
{
    "timestamp": "2026-01-15T15:30:00Z",
    "rule_id": "unapproved-dependency",
    "file_path": "package.json",
    "message": "Package 'angular' not approved",
    "mode": "APPROVAL_REQUIRED",
    "user_decision": "approved",
    "justification": "Spike only, will remove in phase 8",
    "user": "andyhop"
}
```

## 7.0 Compliance Dashboard

Generate HTML compliance reports:

```python
from overwatch_guardrails import ComplianceReporter

reporter = ComplianceReporter(tracker)
reporter.generate_html_report(
    output_path="compliance-report.html",
    period_days=30
)
```

Report includes:
- Violation trends over time
- Top violated rules
- Compliance by phase
- Approval rate
- Policy recommendations
