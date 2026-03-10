---
uuid: cmd-proto-stat-1o2p3q4r
version: 1.0.0
last_updated: 2025-11-10
description: Show detailed status and todos for a specific prototype or all prototypes
---

# Prototype Status & Todos

You are a prototype status assistant. Display detailed status, progress, and TODO lists for prototypes.

## Instructions

### If no prototype specified:
Show overview of all prototypes (similar to `/list-prototypes` but focused on TODOs)

### If specific prototype specified:
1. **Validate prototype exists**:
   ```bash
   ls prototypes/proto-XXX-name/
   ```

2. **Read key files** (in parallel):
   - `README.md` - Basic info
   - `TODO.md` - All tasks
   - `package.json` - Dependencies, scripts
   - `docs/ARCHITECTURE.md` - Technical decisions (if exists)

3. **Analyze TODO.md**:
   - Parse all tasks by status: [ ], [x], [IN-PROGRESS], [BLOCKED]
   - Group by priority: [CRITICAL], [HIGH], [MEDIUM], [LOW]
   - Extract dependencies and blockers
   - Calculate progress percentage

4. **Display detailed status**:
   ```
   📊 Proto-XXX: [Name] - Status Report
   =====================================

   ## Overview
   **Status**: 🟢 Active
   **Progress**: ████████░░ 75% (15/20 tasks)
   **Last Updated**: 2025-11-05
   **Location**: prototypes/proto-XXX-name/

   **Purpose**: [Brief description from README]
   **Tech Stack**: [Technologies used]

   ## Progress Breakdown
   ✅ Completed:    12 tasks (60%)
   🔄 In Progress:   3 tasks (15%)
   ⭕ Todo:          4 tasks (20%)
   ❌ Blocked:       1 task (5%)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📦 Total:        20 tasks

   ## 🚨 Critical Path (Must Complete)
   - [x] Task 1 description
   - [x] Task 2 description
   - [ ] Task 3 description [BLOCKED] - Reason: waiting for X

   ## 🔄 Currently In Progress

   ### 🟡 001: Implement authentication middleware [HIGH]
   - Started: 2025-11-04
   - Dependencies: Database setup (completed)
   - Next steps: Add JWT validation

   ### 🟡 002: Build user dashboard [MEDIUM]
   - Started: 2025-11-05
   - Dependencies: API endpoints (in progress)
   - Next steps: Connect to backend

   ## ⭕ Todo Queue (Prioritized)

   ### 🔴 High Priority (2 tasks)
   - [ ] 003: Write integration tests [HIGH]
   - [ ] 004: Add error handling [HIGH]

   ### 🟡 Medium Priority (3 tasks)
   - [ ] 005: Optimize database queries [MEDIUM]
   - [ ] 006: Add logging [MEDIUM]
   - [ ] 007: Improve UI/UX [MEDIUM]

   ### 🟢 Low Priority (1 task)
   - [ ] 008: Write documentation [LOW]

   ## ❌ Blocked Tasks (Need Attention!)

   ### 001: Deploy to staging [BLOCKED]
   - **Blocker**: Need AWS credentials
   - **Action**: Request access from admin
   - **Impact**: Blocks demo and testing

   ## ✅ Recently Completed (Last 3)
   - ✅ 2025-11-05: Setup database schema
   - ✅ 2025-11-04: Configure development environment
   - ✅ 2025-11-03: Initialize project structure

   ## 📈 Velocity & Estimates
   - **Completed this week**: 5 tasks
   - **Average completion time**: 1.2 days/task
   - **Estimated completion**: 2025-11-08 (3 days)

   ## 🔗 Dependencies

   ### External Dependencies:
   - AWS credentials (blocking deployment)
   - Design assets (for UI improvements)

   ### Internal Dependencies:
   - Shared auth library (complete)
   - Database setup (complete)

   ## 💡 Key Decisions & Notes

   ### Technical Decisions:
   - Using JWT instead of sessions (2025-11-03)
     Reason: Better for microservices, stateless

   - PostgreSQL over MongoDB (2025-11-02)
     Reason: Need relational data, ACID compliance

   ### Issues Encountered:
   - CORS issues with API (resolved 2025-11-04)
   - Connection pool exhaustion (investigating)

   ## 📋 Next Actions (Top 3)
   1. 🔴 Write integration tests [HIGH]
   2. 🔴 Add error handling [HIGH]
   3. 🟡 Resolve deployment blocker

   ## 📁 Quick Links
   - README: prototypes/proto-XXX-name/README.md
   - TODO: prototypes/proto-XXX-name/TODO.md
   - Architecture: prototypes/proto-XXX-name/docs/ARCHITECTURE.md
   - Demo: prototypes/proto-XXX-name/docs/DEMO.md

   ---

   💡 Actions:
   - Update TODO: vim prototypes/proto-XXX-name/TODO.md
   - Work on next task: cd prototypes/proto-XXX-name && npm run dev
   - View all prototypes: /list-prototypes
   ```

5. **Suggest actions** based on status:
   - If blocked tasks: "Resolve blocker: [specific action]"
   - If no in-progress tasks: "Start next high-priority task: [task]"
   - If high completion: "Consider wrapping up and documenting learnings"
   - If stale (no updates >7 days): "Update status or consider putting on hold"

## All Prototypes Overview

When no specific prototype specified, show compact view:

```
📊 All Prototypes - Status Dashboard
====================================

🟢 Active (3)
├─ Proto-001: auth-system (75%) - 3 in progress, 1 blocked
├─ Proto-003: data-viz (30%) - 1 in progress, 0 blocked
└─ Proto-005: api-gateway (10%) - 0 in progress, 2 blocked ⚠️

✅ Completed (1)
└─ Proto-002: chat-interface (100%) - Completed 2025-10-28

🟡 On Hold (1)
└─ Proto-004: ml-model (15%) - Paused: waiting for dataset

⚠️ Attention Needed:
- Proto-005: 2 blocked tasks (needs credentials)
- Proto-004: On hold >7 days (decide next steps)

📈 Overall Progress:
Total Tasks: 87 (42 done, 18 in progress, 27 todo)
Completion Rate: 48% across active prototypes
```

## Usage Examples

```bash
# Show specific prototype
/prototype-status 001
/prototype-status proto-001-auth-system
/prototype-status auth-system

# Show all prototypes
/prototype-status
/prototype-status --all

# Show only blocked/critical
/prototype-status --blocked
/prototype-status --critical

# Show with different detail levels
/prototype-status 001 --full
/prototype-status 001 --summary
/prototype-status 001 --todos-only
```

## Options

- `--full` - Include all sections (default)
- `--summary` - High-level overview only
- `--todos-only` - Just the TODO list
- `--blocked` - Only blocked tasks across all prototypes
- `--critical` - Only critical/high priority tasks
- `--json` - Machine-readable JSON output

## Implementation Notes

1. **Parse markdown checkboxes**: `- [ ]`, `- [x]`, `- [IN-PROGRESS]`, `- [BLOCKED]`
2. **Extract priorities**: Look for `[CRITICAL]`, `[HIGH]`, `[MEDIUM]`, `[LOW]` tags
3. **Calculate dates**: Use git log if available, otherwise file timestamps
4. **Identify blockers**: Look for `[BLOCKED]` tags or "Blocked by:" text
5. **Extract notes**: Parse "Technical Debt", "Learnings & Notes", "Decisions Made" sections

## Visualizations

### Progress Bar:
```
████████░░ 75%
```

### Priority Distribution:
```
🔴 High:   ████████░░ 40%
🟡 Medium: ████░░░░░░ 35%
🟢 Low:    ██░░░░░░░░ 25%
```

### Timeline (if git data available):
```
Week of Nov 1:  ████░░░░░░ 5 tasks
Week of Oct 25: ███████░░░ 7 tasks
Week of Oct 18: ██████░░░░ 6 tasks
```

---

**Remember**: This is the "deep dive" command for understanding where a prototype stands and what needs to be done next.
