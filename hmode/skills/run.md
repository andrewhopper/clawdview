---
name: run
description: Run prototypes using natural language - semantic intent resolution
version: 1.1.0
---

# Semantic Prototype Runner

Execute prototypes using natural language queries with confidence-based auto-approval.

## Execution

When the user invokes `/run <query>`, execute the semantic resolver:

```bash
cd /Users/andyhop/dev/lab/hmode/shared/tools/semantic-run
uv run python semantic_resolver.py "<query>"
```

## How It Works

1. **Parse request** - Natural language → semantic embedding
2. **Find best match** - Search indexed prototypes using cosine similarity
3. **Confidence-based execution:**
   - **High confidence (≥ 0.85)**: Auto-execute immediately
   - **Medium confidence (0.70-0.84)**: Show match + confirm
   - **Low confidence (< 0.70)**: Show top 3 alternatives + select

## Examples

```bash
# High confidence - auto-executes
/run company researcher
→ ✓ Running proto-company-researcher (confidence: 0.94)

# With agent specification
/run company tech stack research
→ ✓ Running proto-company-researcher/agent:tech (confidence: 0.87)

# With preset mode
/run quick company research
→ ✓ Running proto-company-researcher --preset quick (confidence: 0.91)

# Medium confidence - confirms
/run analyze companies
→ Match: proto-company-researcher (confidence: 0.78)
→ Command: python orchestrator.py
→ Execute? (y/n):

# Low confidence - shows alternatives
/run research thing
→ Ambiguous query. Did you mean:
→   1. company-researcher (confidence: 0.65)
→   2. document-parser (confidence: 0.62)
→   3. web-scraper (confidence: 0.58)
→ Select 1-3 or 'n' to cancel:
```

## Agent Resolution

For orchestrator-based prototypes (like company-researcher), the system can resolve specific agents:

```bash
/run company basic info        → Resolves to 'company' agent
/run research team members     → Resolves to 'team' agent
/run analyze tech stack        → Resolves to 'tech' agent
/run check social media        → Resolves to 'social' agent
/run find press coverage       → Resolves to 'press' agent
```

## Preset Detection

Automatically detects execution modes:

```bash
/run quick company research    → --preset quick
/run full company analysis     → --preset full
/run comprehensive research    → --preset comprehensive
```

## First-Time Setup

If the index doesn't exist:

```bash
cd /Users/andyhop/dev/lab/hmode/shared/tools/semantic-run
uv run python index_prototypes.py
```

## Re-indexing

After adding new prototypes:

```bash
cd /Users/andyhop/dev/lab/hmode/shared/tools/semantic-run
uv run python index_prototypes.py --rebuild
```

## Technical Details

- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2, 384-dim vectors)
- **Vector Store**: ChromaDB with SQLite backend
- **Search**: Cosine similarity
- **Dependencies**: Managed via uv (pyproject.toml)
- **Search Latency**: ~50ms per query

## Confidence Thresholds

```python
HIGH_CONFIDENCE = 0.85    # Auto-execute
MEDIUM_CONFIDENCE = 0.70  # Confirm with best match
LOW_CONFIDENCE = 0.50     # Show alternatives
```
