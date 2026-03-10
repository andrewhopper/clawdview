## 🎚️ EFFORT LEVELS (Variable Scope Control)

**Purpose:** Calibrate depth/breadth of research, analysis, and exploration tasks based on user needs.

**Core Principle:** Start small → ask if user wants more → clarify effort level → execute at specified scope.

---

## 🎯 THE FOUR EFFORT LEVELS

**Brief** (Quick answer, minimal depth)
- Time: 2-5 minutes
- Scope: 1-3 items, surface-level analysis
- Output: Summary paragraph + links
- Use case: Quick fact-check, getting started, exploring options

**Standard** (Balanced investigation)
- Time: 5-15 minutes
- Scope: 3-5 items, moderate depth
- Output: Structured comparison table + trade-offs
- Use case: Default for most tasks, tactical decisions

**Comprehensive** (Deep dive, thorough coverage)
- Time: 15-45 minutes
- Scope: 5-10 items, detailed analysis
- Output: Full report with examples, code samples, architectural implications
- Use case: Major technical decisions, architecture selection, vendor evaluation

**Ultra** (Exhaustive research, maximum coverage)
- Time: 45+ minutes
- Scope: 10+ items, exhaustive analysis with multi-dimensional evaluation
- Output: Multi-section report, comparison matrices, POC code, trade-off analysis, recommendation
- Use case: Critical path decisions, high-risk choices, foundational technology selection

---

## 🔄 EFFORT CALIBRATION WORKFLOW

**Step 1: Initial Sample** (Always start here)
```
User: "Research source tools for evals"
AI: [Finds 3 tools: Braintrust, Promptfoo, LangSmith]
```

**Step 2: Continuation Prompt** (Ask before proceeding)
```
AI: "Found 3 eval tools (Braintrust, Promptfoo, LangSmith).

Continue with more? Effort level:
  [1] brief       (1-3 items, quick summary)
  [2] standard    (3-5 items, comparison table) ← recommended
  [3] comprehensive (5-10 items, deep analysis)
  [4] ultra       (10+ items, exhaustive report)

Or done with these 3?"
```

**Step 3: Execute at Specified Level**
```
User: "comprehensive"
AI: [Loads EFFORT_LEVELS.md → executes comprehensive research]
    [Returns 7 tools with detailed analysis, code examples, pricing, integration]
```

---

## 📊 EFFORT LEVEL SPECIFICATIONS

### Brief
**Scope:**
- 1-3 items maximum
- 1-2 sentence description per item
- Links to official docs

**Output Format:**
```markdown
## Quick Summary

1. **Tool A** - Does X. Good for Y. [Link](...)
2. **Tool B** - Does X. Good for Z. [Link](...)
3. **Tool C** - Does X. Good for W. [Link](...)

**Quick take:** Tool A if you need Y, Tool B for Z.
```

**Example Tasks:**
- "What's the latest version of React?"
- "Find 2-3 options for authentication"
- "Quick comparison: REST vs GraphQL"

---

### Standard (Default)
**Scope:**
- 3-5 items
- Paragraph per item (2-4 sentences)
- Comparison table with key dimensions
- Brief trade-off analysis

**Output Format:**
```markdown
## Research: [Topic]

| Tool | Strengths | Weaknesses | Best For |
|------|-----------|------------|----------|
| A    | X, Y      | Z          | Use case |
| B    | X, Y      | Z          | Use case |
| C    | X, Y      | Z          | Use case |

### 1.0 Tool A
Description with key features and limitations.

### 2.0 Tool B
Description with key features and limitations.

**Recommendation:** Tool B if [condition], otherwise Tool A.
```

**Example Tasks:**
- "Research eval frameworks for LLM apps"
- "Find API testing tools"
- "Compare serverless platforms"

---

### Comprehensive
**Scope:**
- 5-10 items
- Detailed analysis per item (5-10 sentences)
- Multi-dimensional comparison (features, pricing, ecosystem, DX)
- Code examples for top 3
- Architecture implications
- Integration considerations

**Output Format:**
```markdown
## Comprehensive Research: [Topic]

### Executive Summary
[2-3 sentence overview of landscape]

### Comparison Matrix
| Tool | Features | Pricing | Ecosystem | DX | Integration |
|------|----------|---------|-----------|----|-----------|
| ...  | ...      | ...     | ...       | ...| ...       |

### 1.0 Tool A (Recommended for X)
[Detailed description]

**Code Example:**
```[language]
[Working example]
```

**Pros:** [3-5 items]
**Cons:** [3-5 items]
**Integration:** [How it fits in stack]

[Repeat for 5-10 tools]

### Recommendations
1. **Use Case A:** Tool X because [rationale]
2. **Use Case B:** Tool Y because [rationale]

### Architecture Impact
[How this choice affects system design]
```

**Example Tasks:**
- "Evaluate databases for real-time analytics workload"
- "Research state management solutions for large React app"
- "Compare CI/CD platforms for monorepo"

---

### Ultra
**Scope:**
- 10+ items
- Exhaustive coverage of landscape
- POC/prototype code for top candidates
- Multi-stage evaluation (quick filter → deep dive → POC)
- Performance benchmarks (if applicable)
- Total cost of ownership analysis
- Migration path considerations
- Risk assessment

**Output Format:**
```markdown
## Exhaustive Research: [Topic]

### 1.0 Executive Summary
[Landscape overview, key trends, market leaders]

### 2.0 Initial Filter (15+ candidates → 10 deep dive)
| Tool | Category | Stage | Keep? |
|------|----------|-------|-------|
| ...  | ...      | ...   | ✅/❌ |

### 3.0 Deep Dive (10 candidates)
[Comprehensive analysis per tool - features, pricing, ecosystem, DX]

### 4.0 Proof of Concept (Top 3)
#### 4.1 Tool A - POC
[Working code example]
[Performance results]
[Integration experience]

#### 4.2 Tool B - POC
[Working code example]
[Performance results]
[Integration experience]

### 5.0 Comparison Matrices
#### 5.1 Feature Matrix
[Detailed feature comparison]

#### 5.2 TCO Analysis
[5-year cost projection]

#### 5.3 Risk Assessment
[Technical risks, vendor risks, migration risks]

### 6.0 Final Recommendations
#### 6.1 By Use Case
[Specific recommendations]

#### 6.2 Migration Path
[If replacing existing tool]

#### 6.3 Decision Criteria
[How to choose between top options]

### 7.0 References
[All sources, docs, benchmarks]
```

**Example Tasks:**
- "Evaluate vector databases for production RAG system (1M+ users)"
- "Research observability platforms for microservices migration"
- "Compare ML feature stores for recommender system"

---

## 🎯 WHEN TO USE EACH LEVEL

**Auto-detect effort level from context:**

| User Signal | Inferred Level | Reasoning |
|-------------|---------------|-----------|
| "quick check", "fast", "just curious" | Brief | Explicit speed signal |
| No qualifier, exploratory | Standard | Default safe choice |
| "evaluate", "compare", "assess" | Standard→Comprehensive | Depends on stakes |
| "critical decision", "production", "replacing" | Comprehensive→Ultra | High impact |
| "exhaustive", "all options", "complete analysis" | Ultra | Explicit breadth signal |

**When stakes are unclear:** Use initial sample (3 items) → ask for effort level.

---

## 🚦 DECISION TREE

```
User Request
    ↓
Can you answer in 3 items or less?
    ↓ YES                          ↓ NO
Return 3 items                 Is effort level clear from context?
    ↓                              ↓ YES              ↓ NO
Ask: "Continue?"              Execute at level    Find 3 items → Ask
    ↓ YES                                               ↓
"What effort level?"                            Execute at specified level
    ↓
Execute at specified level
```

---

## 📝 EFFORT LEVEL TEMPLATES

### Continuation Prompt (After Initial Sample)
```
Found [N] [items] ([name, name, name]).

Continue with more? Effort level:
  [1] brief       ([range], [output type])
  [2] standard    ([range], [output type]) ← recommended
  [3] comprehensive ([range], [output type])
  [4] ultra       ([range], [output type])

Or done with these [N]?
```

### Clarification Prompt (Ambiguous Context)
```
Request: [paraphrase]

This could be:
  [1] Quick check (brief: 2-3 options, summary)
  [2] Tactical decision (standard: 3-5 options, comparison)
  [3] Strategic evaluation (comprehensive: 5-10 options, deep analysis)

Which matches your need?
```

---

## 🔧 INTEGRATION WITH OTHER PROTOCOLS

**Confirmation Protocol:**
- Effort level selection is part of confirmation for research tasks
- AI proposes effort level based on context
- User can adjust up/down

**Phase Detection:**
- Phase 2 (Research): Default to Standard effort
- Phase 4 (Analysis): Default to Comprehensive effort
- Phase 5 (Selection): Default to Comprehensive effort
- Ad-hoc research: Start with initial sample → ask

**Parallel Execution:**
- Brief/Standard: Single AI response
- Comprehensive: May use multiple parallel tool calls (web search, code search, doc reads)
- Ultra: May use Task tool with research subagent for breadth

---

## ⚡ EXAMPLES

### Example 1: Research Task (Auto-detect Standard)
```
User: "Research eval frameworks for LLM apps"
AI: [Detects: evaluation task, no explicit scope]
    [Infers: Standard effort (3-5 items, comparison)]
    [Executes standard research]
    [Returns comparison table with 4 frameworks]
```

### Example 2: Initial Sample → Clarify
```
User: "Find tools for monitoring API performance"
AI: [Finds 3 tools: Datadog, New Relic, Prometheus]

    "Found 3 monitoring tools (Datadog, New Relic, Prometheus).

    Continue with more? Effort level:
      [1] brief       (1-3 items, quick summary)
      [2] standard    (3-5 items, comparison table) ← recommended
      [3] comprehensive (5-10 items, deep analysis)
      [4] ultra       (10+ items, exhaustive report)

    Or done with these 3?"

User: "3"
AI: [Loads EFFORT_LEVELS.md]
    [Executes comprehensive research → 8 tools with detailed analysis]
```

### Example 3: High-Stakes Context (Auto-detect Comprehensive)
```
User: "We're replacing our database for production analytics. Research options."
AI: [Detects: production, replacing = high stakes]
    [Infers: Comprehensive effort minimum]
    [Confirms approach:]

    "Request: Evaluate production analytics databases (replacement decision)

    Given high stakes (production + replacement), recommend comprehensive effort:
      • 7-10 database options
      • Feature comparison, pricing, migration path
      • Code examples for top 3
      • Architecture implications

    Or prefer ultra effort (10+ options, POC code, benchmarks)?

    [1] yes (comprehensive)  [2] no  [3] ultra"
```

### Example 4: Explicit Ultra Request
```
User: "Give me an exhaustive analysis of vector databases"
AI: [Detects: "exhaustive" = ultra effort]
    [Executes ultra research without asking]
    [Returns 12+ databases with POC code, benchmarks, TCO]
```

---

## 🚨 CRITICAL RULES

1. **Always start with initial sample (3 items)** for open-ended research unless effort level is explicit
2. **Ask before expanding** beyond initial sample
3. **Default to Standard** when effort level is ambiguous
4. **Auto-detect Ultra** only when user says "exhaustive", "all options", "complete"
5. **Respect user's time:** Brief is 2-5 min, Standard is 5-15 min, Comprehensive is 15-45 min, Ultra is 45+ min
6. **Quality over quantity:** Better to deeply analyze 5 items than superficially list 20
7. **Load this file** when user specifies effort level (to ensure consistent execution)

---

## 📊 EFFORT LEVEL MATRIX (Quick Reference)

| Level | Items | Time | Output | When |
|-------|-------|------|--------|------|
| **Brief** | 1-3 | 2-5m | Summary + links | Quick check, getting started |
| **Standard** | 3-5 | 5-15m | Comparison table | Default, tactical decisions |
| **Comprehensive** | 5-10 | 15-45m | Full report + examples | Major decisions, architecture |
| **Ultra** | 10+ | 45m+ | Exhaustive analysis + POC | Critical path, foundational tech |

---

[END OF EFFORT LEVELS]
