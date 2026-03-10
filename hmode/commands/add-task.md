<!-- File UUID: 7c8d9e0f-1a2b-3c4d-5e6f-7a8b9c0d1e2f -->
---
name: add-task
description: Add a task with intelligent disambiguation. Takes vague input and generates 6 dense interpretations with recommendation.
version: 1.1.0
aliases: [todo, task, add-todo]
---

# Add Task - Intelligent Disambiguation

**Trigger:** `/add-task <vague description>` or `/todo <vague description>`

Takes minimal input → generates 6 semantically dense interpretations → recommends best option.

## Workflow

```
User: /add-task auth

Claude generates 6 interpretations with recommendation:

┌─────────────────────────────────────────────────────────────┐
│  🎯 Interpreting: "auth"                                    │
│                                                             │
│  [1] bcrypt user/pass auth + secure session mgmt            │
│  [2] OAuth2 social login (Google/GitHub) + token refresh    │
│  [3] JWT auth + httpOnly cookies + refresh token rotation ⭐│
│  [4] HTTP Basic auth for internal API endpoints             │
│  [5] Session-based auth + Redis store + CSRF protection     │
│  [6] API key auth for external service integrations         │
│                                                             │
│  💡 Recommend [3]: Most flexible, stateless, industry       │
│     standard for SPAs. Supports mobile + web.               │
│                                                             │
│  [m] More options  [t] Tweak  [c] Cancel                    │
└─────────────────────────────────────────────────────────────┘

User: 3

Claude creates task: "JWT auth + httpOnly cookies + refresh token rotation"
```

## Input Parsing

Extract the vague description from user input:

```
"/add-task auth" → query: "auth"
"/todo fix the bug" → query: "fix the bug"
"/add-task db" → query: "db"
```

## Generation Rules

When generating 6 interpretations:

### 1. Semantic Density (CRITICAL)

Each option MUST be maximally information-dense:
- **Remove filler words:** "Add a feature to" → just describe the feature
- **Use symbols:** `→` for flows, `+` for combinations, `/` for alternatives
- **Abbreviate common terms:** authentication→auth, management→mgmt, configuration→config
- **Chain concepts:** "JWT auth + httpOnly cookies + refresh rotation"
- **Max ~60 chars per option** - pack meaning, not words

**❌ Verbose:** "Add user authentication using passwords with bcrypt hashing"
**✅ Dense:** "bcrypt user/pass auth + secure session mgmt"

**❌ Verbose:** "Implement a caching layer using Redis for API responses"
**✅ Dense:** "Redis cache layer → API response memoization + TTL"

### 2. Variety Spectrum
- Simple vs complex
- Frontend vs backend
- Quick fix vs architectural change

### 3. Specificity Gradient
- 2 specific/narrow interpretations
- 2 moderate scope interpretations
- 2 broader/architectural interpretations

### 4. Technical Diversity
- Different technologies when applicable
- Different patterns/approaches
- Different integration points

### 5. Actionable Language
- Start with action concept (auth, cache, route, test)
- Include key technical details
- Omit "Add/Implement/Create" prefix when obvious

## Recommendation Rules

After generating options, analyze and recommend the best one:

### Selection Criteria (in order)
1. **Most likely intent** - What did user probably mean?
2. **Best practice alignment** - Industry standard approach?
3. **Scope balance** - Not too narrow, not too broad
4. **Feasibility** - Achievable as a single task

### Recommendation Format
```
💡 Recommend [N]: {1-line rationale - why this is best fit}
```

Mark recommended option with ⭐ in the list.

## Response Format

### Initial Options

```
🎯 Interpreting: "{user_input}"

[1] {dense_interpretation_1}
[2] {dense_interpretation_2}
[3] {dense_interpretation_3} ⭐
[4] {dense_interpretation_4}
[5] {dense_interpretation_5}
[6] {dense_interpretation_6}

💡 Recommend [3]: {brief rationale}

[m] More options  [t] Tweak  [c] Cancel
```

### User Actions

| Input | Action |
|-------|--------|
| `1-6` | Select that interpretation |
| `m` or `more` | Generate 6 new interpretations |
| `t <N> <modification>` | Tweak option N with modification |
| `c` or `cancel` | Cancel task creation |

### Tweak Examples

```
User: t 3 with refresh tokens
→ Modifies option 3 to: "Add JWT token-based authentication with refresh tokens"

User: t 1 for admin panel only
→ Modifies option 1 to: "Add user/password authentication with bcrypt for admin panel only"
```

## Task Creation

After user selects or confirms, create the task:

### Method 1: HTTP API (if portfolio manager running)

```bash
curl -X POST http://localhost:5173/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Add JWT token-based authentication",
    "priority": "medium",
    "tags": ["auth", "backend"]
  }'
```

### Method 2: Direct SQLite (if API not available)

```bash
cd /Users/andyhop/dev/hopperlabs
sqlite3 .todo.db "INSERT INTO events (id, timestamp, type, todo_id, branch, payload) VALUES (
  '$(uuidgen | tr -d '-' | tr '[:upper:]' '[:lower:]')$(date +%s%N | cut -c1-10)',
  '$(date -u +%Y-%m-%dT%H:%M:%S.000Z)',
  'TODO_CREATED',
  '$(uuidgen | tr -d '-' | tr '[:upper:]' '[:lower:]')$(date +%s%N | cut -c1-10)',
  '$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)',
  '{\"title\":\"Add JWT token-based authentication\",\"priority\":2,\"tags\":[\"auth\"]}'
);"
```

### Priority Inference

Infer priority from context:
- **high:** Contains "urgent", "critical", "asap", "blocking", "security"
- **low:** Contains "nice to have", "eventually", "minor", "cleanup"
- **medium:** Default for all other tasks

### Tag Inference

Auto-generate tags from the task subject:
- Technical keywords: auth, api, db, ui, test, docs, config
- Action keywords: fix, add, refactor, update, remove
- Domain keywords: user, payment, admin, email

## Confirmation Output

```
✅ Task created!

Subject: Add JWT token-based authentication
Priority: medium
Tags: auth, backend, api

View in portfolio: http://localhost:5173/tasks
```

## Examples

### Example 1: Simple

```
User: /add-task db

🎯 Interpreting: "db"

[1] Connection pooling + health checks
[2] Migration scripts (up/down) + version tracking ⭐
[3] Automated backups → S3 + retention policy
[4] Query logging + slow query alerts
[5] Index optimization + EXPLAIN analysis
[6] Schema docs auto-gen from models

💡 Recommend [2]: Foundation for safe schema changes. Enables team collaboration.

[m] More options  [t] Tweak  [c] Cancel

User: 2

✅ Task created!
Subject: Migration scripts (up/down) + version tracking
Priority: medium
Tags: database, infrastructure
```

### Example 2: With Tweak

```
User: /add-task tests

🎯 Interpreting: "tests"

[1] Unit tests → API endpoints + mocks
[2] Integration tests → auth flow + DB
[3] Playwright E2E → critical user paths ⭐
[4] Coverage reporting + threshold gates
[5] CI test automation + parallel runs
[6] Component snapshots + visual regression

💡 Recommend [3]: Catches real user-facing bugs. High ROI for effort.

[m] More options  [t] Tweak  [c] Cancel

User: t 3 for mobile viewports

Modified [3]: Playwright E2E → critical paths + mobile viewports

Select [1-6], [m]ore, [t]weak, [c]ancel:

User: 3

✅ Task created!
Subject: Playwright E2E → critical paths + mobile viewports
Priority: medium
Tags: testing, e2e, mobile
```

### Example 3: More Options

```
User: /add-task cache

🎯 Interpreting: "cache"

[1] Redis layer → session + API response cache ⭐
[2] localStorage cache + sync strategy
[3] API memoization + SWR pattern
[4] CDN cache headers + invalidation
[5] DB query cache + prepared statements
[6] Service worker → offline-first + cache API

💡 Recommend [1]: Versatile, scales horizontally, industry standard.

[m] More options  [t] Tweak  [c] Cancel

User: m

🎯 Interpreting: "cache" (batch 2)

[1] LRU cache → expensive computations
[2] Elasticache distributed + failover ⭐
[3] Cache invalidation webhooks + pub/sub
[4] Stale-while-revalidate + background refresh
[5] Cache warming on deploy + precompute
[6] Hit/miss metrics + Grafana dashboard

💡 Recommend [2]: Production-ready, managed, auto-scaling.

[m] More options  [t] Tweak  [c] Cancel
```

### Example 4: Project Context

When in a project directory, use project context for better interpretations:

```
User: /add-task auth
(in projects/unspecified/active/tool-project-portfolio-manager-lk5aa)

🎯 Interpreting: "auth" for Portfolio Manager

[1] Cognito auth → portfolio viewer + token refresh
[2] API key auth → task endpoints + rate limiting ⭐
[3] Public read-only mode + share links
[4] Admin-only editing + role-based access
[5] GitHub OAuth → project owner verification
[6] Session auth + secure cookies + CSRF

💡 Recommend [2]: Simple, works for internal tool. Easy to implement.

[m] More options  [t] Tweak  [c] Cancel
```

## Integration

### With Project Detection

If user specifies a project, tag the task:

```
/add-task auth for portfolio-manager
→ Creates task with tags: ["auth", "portfolio-manager"]
→ Sets projectId if detectable
```

### With Terminal Sessions

If a terminal session exists for a task, mention it:

```
✅ Task created!
Subject: Add JWT authentication
🖥️ Launch terminal: /launch-task <task-id>
```

## Error Handling

### API Not Available

```
⚠️ Portfolio API not running. Task saved directly to database.
Start portfolio manager with: cd projects/.../tool-project-portfolio-manager-lk5aa && npm run dev
```

### Invalid Selection

```
Invalid option. Please enter:
- 1-6 to select
- m for more options
- t <N> <change> to tweak
- c to cancel
```

## Configuration

Database location: `$LAB_ROOT/.todo.db` (SQLite with event sourcing)

The task system uses event sourcing, so all changes are appended as immutable events:
- `TODO_CREATED` - New task
- `TODO_UPDATED` - Title change
- `TODO_COMPLETED` - Mark done
- `TODO_PRIORITIZED` - Priority change
- `TODO_TAGGED` - Add tag
