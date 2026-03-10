## 🎭 COMPOSABLE AI FEATURES

**Purpose:** React-style composition for AI workflows - providers inject context, observers react to events

### Provider Wrappers (Context Injection)

**Syntax:**
```
<provider-type provider="value">
  commands here
</provider-type>
```

**Available Providers:**
| Provider | Purpose | Values | Example |
|----------|---------|--------|---------|
| `audience` | Target audience | startup-techies, executives, sres, developers, sales, data-scientists | `<audience provider="startup-techies">` |
| `style` | Writing style | aws, amazon, academic, casual, technical, densified | `<style provider="aws">` |
| `tech` | Tech context | python, typescript, react, serverless, containers | `<tech provider="serverless">` |
| `tone` | Communication | formal, casual, authoritative, collaborative | `<tone provider="formal">` |
| `format` | Output format | presentation, document, diagram, code, table | `<format provider="presentation">` |
| `quality` | Quality level | prototype, production, client-ready | `<quality provider="production">` |

**Nesting:** Inner providers override outer (like React Context)

**Example:**
```
<audience provider="startup-techies">
  <style provider="aws">
    <format provider="presentation">
      create GenAI adoption whitepaper, website, demo video
    </format>
  </style>
</audience>
```

**Shorthand:** `@audience(startup-techies) @style(aws) @format(presentation) make whitepaper`

---

### Observers (Passive Monitoring)

**Purpose:** Monitor execution, collect data, learn patterns (non-blocking)

**Syntax:**
```
<observer type="observer-type" [scope="global|local"] [report="realtime|summary|none"]>
  commands here
</observer>
```

**Observer Types:**

| Type | Monitors | Output | Use Case |
|------|----------|--------|----------|
| `quality` | Code quality, test coverage, errors | Quality score + suggestions | Track code health during Phase 8 |
| `pattern` | Architectural patterns, library usage | Pattern frequency report | Learn what works (feed to guardrails) |
| `performance` | API latency, build time, test duration | Performance metrics | Identify bottlenecks |
| `cost` | LLM token usage, API calls, resource usage | Cost breakdown | Budget tracking |
| `learning` | User feedback, correction frequency | Learning report | Improve CLAUDE.md |
| `divergence` | Variant differences, trade-offs | Diversity matrix | Genetic AI analysis |

**Example:**
```
<observer type="quality" report="realtime">
  <observer type="cost" report="summary">
    /new-prototype "API Gateway"
  </observer>
</observer>
```

**Output:**
- `realtime`: Stream metrics during execution
- `summary`: Report at end
- `none`: Silent collection (logs only)

**Scope:**
- `global`: Persists across commands in session
- `local`: Only for nested commands (default)

---

### Listeners (Event-Driven Reactions)

**Purpose:** React to events, trigger actions (active, can block)

**Syntax:**
```
<listener event="event-type" action="action-spec" [block="true|false"]>
  commands here
</listener>
```

**Event Types:**

| Event | Triggers When | Common Actions |
|-------|---------------|----------------|
| `test-failure` | Test fails | Retry, analyze error, suggest fix |
| `phase-transition` | SDLC phase changes | Update docs, notify, archive |
| `error` | Any error occurs | Log, rollback, fallback approach |
| `pattern-detected` | New pattern found | Add to guardrails (approval required) |
| `quality-drop` | Quality below threshold | Block merge, suggest refactor |
| `cost-exceeded` | Cost > budget | Pause, switch to haiku, alert |
| `divergence-complete` | All variants done | Run evaluation automatically |

**Example:**
```
<listener event="test-failure" action="analyze-and-suggest-fix" block="true">
  <listener event="quality-drop" action="pause-and-review">
    /implementation
  </listener>
</listener>
```

**Actions:**
- `analyze-and-suggest-fix`: Debug test failures
- `pause-and-review`: Stop execution, request human review
- `fallback:haiku`: Switch to cheaper model
- `auto-commit`: Commit on phase transition
- `update-manifest`: Sync project-manifest.json
- `custom:<slash-command>`: Run custom slash command

**Block:**
- `true`: Wait for action to complete before proceeding
- `false`: Fire-and-forget (default)

---

### Composition Patterns

**Pattern 1: Quality-Gated Development**
```
<observer type="quality" report="realtime">
  <listener event="quality-drop" action="pause-and-review" block="true">
    <listener event="test-failure" action="analyze-and-suggest-fix">
      @quality(production) /implementation
    </listener>
  </listener>
</observer>
```

**Pattern 2: Multi-Format Delivery**
```
<audience provider="executives">
  <style provider="aws">
    <observer type="pattern">
      <format provider="presentation">
        create executive briefing
      </format>
      <format provider="document">
        create 6-pager
      </format>
      <format provider="diagram">
        create architecture overview
      </format>
    </observer>
  </style>
</audience>
```

**Pattern 3: Cost-Aware Divergent Mode**
```
<observer type="cost" report="realtime">
  <listener event="cost-exceeded" action="fallback:haiku">
    <listener event="divergence-complete" action="auto-evaluate">
      divergent --width=3 --depth=2
    </listener>
  </listener>
</observer>
```

**Pattern 4: Learning Observer (Guardrails Update)**
```
<observer type="pattern" scope="global" report="summary">
  <observer type="learning" scope="global">
    [Multiple prototype sessions over time]
  </observer>
</observer>

# At end of quarter: Observer generates candidates for guardrails
# Output: "Detected patterns: Terraform (15x), Prisma (22x), Event-driven (8x)"
# Human reviews → Approval → Update hmode/guardrails/
```

---

### Implementation Rules

**AI MUST:**
- Apply ALL provider context to nested commands
- Honor provider overrides (inner > outer)
- Run observers passively (no blocking unless event triggers listener)
- Execute listener actions when events fire
- Maintain observer state for `scope="global"`
- Generate observer reports per `report` setting

**AI MUST NOT:**
- Add patterns to guardrails without human approval (even if observer suggests)
- Block execution for `block="false"` listeners
- Ignore provider context (all nested commands inherit)
- Leak observer state across sessions (global scope = session only)

**Enforcement:**
- Providers: Context applied to ALL nested commands
- Observers: Passive, non-blocking (unless listener triggered)
- Listeners: Active, can block if `block="true"`
- Composability: Unlimited nesting, inner overrides outer

---

### Metadata (.project)

**Provider Context:**
```json
{
  "composable_features": {
    "providers": {
      "audience": "startup-techies",
      "style": "aws",
      "quality": "production"
    },
    "observers_active": ["quality", "pattern", "cost"],
    "listeners_active": [
      {"event": "test-failure", "action": "analyze-and-suggest-fix"}
    ]
  }
}
```

**Observer Reports:**
```json
{
  "observer_reports": {
    "quality": {
      "score": 8.5,
      "coverage": "72%",
      "issues": ["Missing error handling in auth.ts:45"]
    },
    "pattern": {
      "detected": ["Repository pattern (5x)", "Factory pattern (3x)"],
      "candidates_for_guardrails": ["Zod validation pattern"]
    },
    "cost": {
      "total_usd": 2.35,
      "breakdown": {"input": 1.20, "output": 1.15}
    }
  }
}
```

