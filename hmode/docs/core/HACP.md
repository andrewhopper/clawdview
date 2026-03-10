# Human-AI Command Protocol (HACP)

**Status:** Optional — activate via `/comms`
**Inspired by:** Military Mission Command (centralized intent + decentralized execution)

---

## 1.0 CORE PHILOSOPHY

```
CENTRALIZED INTENT  +  DECENTRALIZED EXECUTION
     (what/why)              (how)
```

- Human defines **what** and **why**
- AI determines **how**
- AI acts within intent when facing ambiguity
- BLUF (Bottom Line Up Front) — always lead with the key point

---

## 2.0 TASK ORDER FORMAT (Human → AI)

```
BLUF:      [One sentence: what you need]
INTENT:    [Why / what success looks like]
SCOPE:     [S/M/L/XL]
AUTHORITY: [FULL | STANDARD | LIMITED | CONSULT]
CONTEXT:   [Background, constraints, preferences]
OUTPUT:    [Expected deliverable format]
```

**Minimum viable order:** BLUF + INTENT (others optional for small tasks)

### 2.1 Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| **BLUF** | Yes | Single sentence task statement |
| **INTENT** | Yes | End state / why it matters |
| **SCOPE** | Recommended | S (<1hr), M (1-4hr), L (1-2 days), XL (multi-day) |
| **AUTHORITY** | No | Decision rights (default: STANDARD) |
| **CONTEXT** | No | Background, constraints, preferences |
| **OUTPUT** | No | Expected deliverable format |

---

## 3.0 AUTHORITY LEVELS

| Level | AI Decides | Must Ask Human |
|-------|------------|----------------|
| **FULL** | Everything within intent | Nothing unless blocked |
| **STANDARD** | Implementation details | Architecture, deps, scope changes |
| **LIMITED** | Minor choices | All significant decisions |
| **CONSULT** | Nothing | Everything (advisory mode) |

**Default:** STANDARD for most tasks.
**Rule:** Scale authority inversely with risk.

---

## 4.0 STATUS REPORT FORMAT (AI → Human)

```
BLUF:      [Current state in one sentence]
PROGRESS:  [Done / next]
BLOCKERS:  [Issues needing human decision]
DECISIONS: [Choices made under delegated authority]
REQUEST:   [What needed from human]
```

---

## 5.0 ESCALATION TRIGGERS

AI escalates when:
1. Ambiguity exceeds authority level
2. Scope significantly larger than estimated
3. Multiple valid approaches with major tradeoffs
4. Security/ethical/legal concerns
5. Resources exceed implied constraints

**Escalation format:**
```
ESCALATION: [Category]
SITUATION:  [What triggered this]
OPTIONS:    [1] ... [2] ... [3] ...
RECOMMEND:  [AI's recommendation]
NEED:       [Decision / Guidance / Approval]
```

---

## 6.0 SCOPE-AUTHORITY MATRIX

```
SCOPE:       S ────────────────► XL
AUTHORITY:   FULL ─────────────► LIMITED
CHECKPOINTS: 0 ────────────────► Many
```

| Scope | Example | Authority | Checkpoints |
|-------|---------|-----------|-------------|
| **S** | Bug fix, quick research | FULL | 0 |
| **M** | API integration, ETL pipeline | STANDARD | 1 |
| **L** | New service, major feature | STANDARD/LIMITED | 1-2 |
| **XL** | Migration, platform build | LIMITED | Per-phase |

---

## 7.0 KEY PRINCIPLES

1. **BLUF always** — Lead with bottom line
2. **Intent enables autonomy** — "Why" lets AI handle ambiguity without constant asks
3. **Document decisions made** — Build trust via transparency
4. **Checkpoint at phase gates** — Not constant interruption
5. **Mistakes > hesitation** — Act within intent, course-correct later

---

## 8.0 QUICK EXAMPLES

### 8.1 Small Task
```
BLUF:   Find top 3 Python CV libraries by GitHub stars.
INTENT: Picking one for weekend prototype — need well-maintained.
```

### 8.2 Medium Task
```
BLUF:      Integrate Stripe subscriptions into FastAPI backend.
INTENT:    Enable billing for Pro tier launch next week.
SCOPE:     M
AUTHORITY: STANDARD
CONTEXT:   Existing JWT auth, PostgreSQL, two tiers (Free, Pro $19/mo)
OUTPUT:    Endpoints, webhook handler, DB migrations.
```

### 8.3 Large Task
```
BLUF:      Build notification service for our platform.
INTENT:    Centralized system for email, SMS, push, in-app notifications.
SCOPE:     L
AUTHORITY: LIMITED — check in before major components.
CONTEXT:   Microservices (K8s), Kafka event bus, ~100k notifications/day
OUTPUT:    Service repo, API docs, migration plan.
```

---

## 9.0 CHANGE ORDERS (FRAGORD)

When modifying an active task:
```
REFERENCE: [Original task]
CHANGE:    [What's different]
REASON:    [Why the change]
IMPACT:    [Effect on timeline/scope]
```

---

**Full Research:** `projects/shared/research/human-ai-c2-protocol/`
