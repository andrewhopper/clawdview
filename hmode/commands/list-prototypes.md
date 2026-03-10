---
uuid: cmd-list-proto-1e2f3g4h
version: 1.0.0
last_updated: 2025-11-10
description: List all prototypes with status and quick info
---

# List All Prototypes

You are a prototype listing assistant. Display all prototypes in the monorepo with their current status and key information.

## Parameters

- `--maturity [level]`: Filter by target company maturity (poc, mvp, pmf, startup, scaleup, enterprise)
- `--audience [type]`: Filter by target audience (SREs, Developers, etc.)
- `--status [status]`: Filter by status (active, completed, archived, etc.)

## Instructions

1. **Scan prototypes directory**:
   ```bash
   ls -la prototypes/
   ```

2. **For each prototype**, read its .project file to extract:
   - Status (🟢 Active / 🟡 On Hold / ✅ Completed / 🔴 Archived / 🚀 Graduated)
   - Purpose/description
   - Tech stack
   - Target company maturity
   - Target audience
   - Last updated date

3. **Count TODO items** in each prototype's TODO.md:
   - Total tasks
   - Completed tasks
   - In-progress tasks
   - Pending tasks
   - Blocked tasks

4. **Display formatted list**:
   ```
   📦 Protoflow Prototypes
   ========================

   Total: X prototypes (X active, X completed, X archived)

   ## 🟢 Active Prototypes

   ### Proto-001: auth-system
   **Status**: 🟢 Active (60% complete)
   **Purpose**: JWT authentication with refresh tokens
   **Tech Stack**: Node.js, Express, PostgreSQL, JWT
   **Target Maturity**: poc, mvp, startup
   **Target Audience**: Developers
   **Progress**: ████████░░ 6/10 tasks complete
   **Location**: prototypes/proto-001-auth-system/
   **Last Updated**: 2025-11-05

   ### Proto-003: data-viz
   **Status**: 🟢 Active (30% complete)
   **Purpose**: Interactive data visualization dashboard
   **Tech Stack**: React, D3.js, Vite
   **Progress**: ███░░░░░░░ 3/10 tasks complete
   **Location**: prototypes/proto-003-data-viz/
   **Last Updated**: 2025-11-04

   ## ✅ Completed Prototypes

   ### Proto-002: chat-interface
   **Status**: ✅ Completed
   **Purpose**: Real-time WebSocket chat
   **Tech Stack**: Node.js, Socket.io, React
   **Completed**: 2025-10-28
   **Key Learnings**: WebSocket scaling, connection management
   **Location**: prototypes/proto-002-chat-interface/

   ## 🟡 On Hold

   ### Proto-004: ml-model
   **Status**: 🟡 On Hold
   **Purpose**: Image classification model
   **Tech Stack**: Python, TensorFlow, FastAPI
   **Reason**: Waiting for dataset
   **Location**: prototypes/proto-004-ml-model/

   ## 🔴 Archived

   ### Proto-000: test-experiment
   **Status**: 🔴 Archived
   **Purpose**: Initial test prototype
   **Archived**: 2025-10-15
   **Reason**: Superseded by proto-001
   **Location**: prototypes/proto-000-test-experiment/

   ---

   💡 Quick Actions:
   - Create new: /new-prototype
   - View dashboard: cat DASHBOARD.md
   - Check todos: /prototype-status
   ```

5. **Calculate statistics**:
   - Total prototypes
   - Active vs completed vs archived
   - Average completion rate
   - Most common tech stacks
   - Total tasks across all prototypes

6. **Optional: Visual timeline** (if multiple prototypes):
   ```
   Timeline:
   2025-10 │ 🟢 001 ──────────────────────────>
   2025-10 │      🟢 002 ─────> ✅
   2025-11 │                    🟢 003 ──────>
   2025-11 │                         🟡 004 ⏸
   ```

## Sorting Options

User can specify sorting:
- `/list-prototypes` - Default (by number)
- `/list-prototypes --by-status` - Group by status
- `/list-prototypes --by-date` - Recent first
- `/list-prototypes --by-progress` - Most/least complete

## Filtering Options

User can filter:
- `/list-prototypes --active` - Only active
- `/list-prototypes --completed` - Only completed
- `/list-prototypes --tech react` - By tech stack
- `/list-prototypes --recent 5` - Last N prototypes

## Output Format Options

- `--short` - Compact one-line per prototype
- `--detailed` - Full details including TODOs
- `--json` - Machine-readable JSON output

## Implementation Notes

1. **Read all READMEs in parallel** - Use multiple Read calls in one message
2. **Parse TODO.md files** - Count checkboxes
3. **Extract git info if needed** - For last updated dates
4. **Handle missing files gracefully** - Some prototypes may be incomplete

## Example Outputs

### Short format:
```
📦 Prototypes (4 total)
🟢 001: auth-system (60%) - Node.js/Express
✅ 002: chat-interface (100%) - Node.js/Socket.io/React
🟢 003: data-viz (30%) - React/D3.js
🟡 004: ml-model (10%) - Python/TensorFlow
```

### Detailed format:
```
[Full details as shown above in main format]
```

### JSON format:
```json
{
  "total": 4,
  "active": 2,
  "completed": 1,
  "on_hold": 1,
  "archived": 0,
  "prototypes": [
    {
      "number": "001",
      "name": "auth-system",
      "status": "active",
      "progress": 0.6,
      "tech_stack": ["Node.js", "Express", "PostgreSQL"],
      "tasks": {"total": 10, "completed": 6, "pending": 4}
    }
  ]
}
```

## Use Cases

- **Quick overview** - See what's being worked on
- **Status check** - Find prototypes that need attention
- **Tech inventory** - See what technologies have been explored
- **Progress tracking** - Monitor completion rates
- **Documentation** - Generate reports or summaries

---

**Remember**: This should be fast and informative. Use parallel file reads for speed.
