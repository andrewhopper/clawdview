# Stage 3 - Idea Expansion

## 1.0 Problem Reframe

**Core need:** Developers need to discover, understand, and create domain models without friction.

**Deeper questions:**
- Does this need to be a CLI at all?
- What if domain discovery was embedded in the AI workflow?
- What if VS Code knew about domains?
- What if the registry was queryable via natural language?

**Persona's vision:** "Shared semantic layer enables AI - define once, use everywhere"

---

## 2.0 Alternative Delivery Mechanisms

### Alternative A: MCP Server for Domain Discovery
**Description:** Expose domains as an MCP tool that Claude/AI agents can query directly.

| Pros | Cons |
|------|------|
| AI-native: agents discover domains automatically | Requires MCP-capable client |
| No context switching from AI chat | Not usable without AI |
| Natural language queries | New pattern to maintain |
| **Directly enables "semantic layer for AI"** | |

**Example interaction:**
```
User: "I need to model a payment flow"
Claude: [calls domain-search tool] → "Found 3 relevant domains:
  finance, payment-processing, economic-agreement"
```

### Alternative B: VS Code Extension
**Description:** Hover over domain references to see schema, autocomplete domain names.

| Pros | Cons |
|------|------|
| Zero context switch in IDE | VS Code only |
| Inline documentation | Extension maintenance |
| Autocomplete in YAML files | TypeScript skillset needed |
| Go-to-definition for domains | |

### Alternative C: Embedded Domain Index in CLAUDE.md
**Description:** Auto-generated domain summary lives in CLAUDE.md, Claude always has context.

| Pros | Cons |
|------|------|
| Zero tooling needed | Bloats CLAUDE.md |
| Always available to AI | Manual sync required |
| Works in any AI client | No interactive search |

### Alternative D: Web Dashboard
**Description:** Browse domains in a web UI with search, filtering, dependency visualization.

| Pros | Cons |
|------|------|
| Visual dependency graph | Hosting required |
| Accessible to non-terminal users | Context switch from IDE |
| Shareable URLs | Over-engineered for internal use |

### Alternative E: Registry as SQLite + Natural Language
**Description:** Convert registry.yaml to SQLite, enable SQL or NL queries.

| Pros | Cons |
|------|------|
| Powerful analytical queries | Migration effort |
| DuckDB integration | YAML simplicity lost |
| "Which domains have Payment entities?" | |

### Alternative F: CLI Tool Only (Implemented)
**Description:** Traditional CLI with list/show/search/create/validate commands.

| Pros | Cons |
|------|------|
| Familiar pattern | No AI integration |
| Fast, scriptable, pipeable | Manual invocation required |
| Golden repo pattern exists | Doesn't enable AI agents |

### Alternative G: Hybrid CLI + MCP Server
**Description:** CLI for humans, MCP server for AI agents, shared registry module.

| Pros | Cons |
|------|------|
| Best of both worlds | Two interfaces to maintain |
| Human + AI accessible | More code |
| **Directly supports persona vision** | |
| Shared core logic | |

---

## 3.0 CLI Framework Options (If CLI chosen)

### Option 1: Click + Rich (Python)
| Pros | Cons |
|------|------|
| Golden repo pattern | Not interactive |
| Fast startup | Static output |
| Well-documented | |

### Option 2: Typer (Python)
| Pros | Cons |
|------|------|
| Type hints = CLI args | Smaller ecosystem |
| Modern Python | Less flexible |

### Option 3: Textual TUI (Python)
| Pros | Cons |
|------|------|
| Full interactive TUI | Overkill for discovery |
| Same Rich ecosystem | Learning curve |

### Option 4: React Ink (TypeScript)
| Pros | Cons |
|------|------|
| Interactive, fuzzy search | Node runtime, slow startup |
| React patterns | Different language |

---

## 4.0 Alignment Matrix

| Alternative | Enables AI? | Define Once? | Use Everywhere? | Effort |
|-------------|-------------|--------------|-----------------|--------|
| A: MCP Server | ✅ Yes | ✅ Yes | ⚠️ MCP only | 2-3 days |
| B: VS Code Ext | ❌ No | ✅ Yes | ⚠️ VS Code only | 1 week |
| C: CLAUDE.md | ✅ Yes | ❌ Manual | ✅ Yes | 1 day |
| D: Web Dashboard | ❌ No | ✅ Yes | ✅ Yes | 1 week |
| E: SQLite/NL | ⚠️ Indirect | ✅ Yes | ✅ Yes | 3-4 days |
| F: CLI Only | ❌ No | ✅ Yes | ⚠️ Terminal | **Done** |
| **G: CLI + MCP** | ✅ Yes | ✅ Yes | ✅ Yes | +2 days |

---

## 5.0 Key Insight

The CLI is already built. The real question: **Does it serve the persona's vision?**

The persona believes semantic models enable AI. A CLI-only tool does NOT enable AI agents to discover domains.

**Alternative G (CLI + MCP)** directly supports the vision:
- CLI serves human developers (done)
- MCP server enables AI agents to query domains (todo)
- Shared `Registry` module means define-once

---

## 6.0 Candidates for Phase 4

1. **F: CLI Only** - Ship as-is, good enough for now
2. **G: CLI + MCP** - Add MCP server to enable AI agents
3. **A: MCP First** - Pivot to AI-native, deprioritize CLI
