---
description: Run prototypes using natural language - semantic intent resolution
tags: [execution, semantic, prototypes]
---

# Semantic Prototype Runner

Execute prototypes using natural language queries with confidence-based auto-approval.

## How It Works

1. **Parse your request** - Natural language → semantic embedding
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

If this is your first time using `/run`, you need to index the prototypes:

```bash
# Dependencies are managed via uv (already configured in pyproject.toml)
cd hmode/shared/tools/semantic-run

# Index all prototypes (takes 30-60 seconds)
uv run python index_prototypes.py

# Test the resolver
uv run python semantic_resolver.py "company researcher" --dry-run
```

## Re-indexing

After adding new prototypes or updating .project files:

```bash
cd hmode/shared/tools/semantic-run
uv run python index_prototypes.py --rebuild
```

## Technical Details

- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2, 384-dim vectors)
- **Vector Store**: ChromaDB with SQLite backend
- **Search**: Cosine similarity
- **Index Size**: ~5KB per prototype, ~150KB total for 30 prototypes
- **Model Size**: 80MB (downloaded once, cached locally)
- **Search Latency**: ~50ms per query

## Confidence Thresholds

```python
HIGH_CONFIDENCE = 0.85    # Auto-execute
MEDIUM_CONFIDENCE = 0.70  # Confirm with best match
LOW_CONFIDENCE = 0.50     # Show alternatives
```

## Command-Line Usage

You can also use the resolver directly:

```bash
# Standard execution (auto-approve high confidence)
cd hmode/shared/tools/semantic-run && uv run python semantic_resolver.py "run company researcher"

# Dry run (show what would execute)
cd hmode/shared/tools/semantic-run && uv run python semantic_resolver.py "quick research" --dry-run

# Disable auto-approval (always confirm)
cd hmode/shared/tools/semantic-run && uv run python semantic_resolver.py "company researcher" --no-auto
```

## Architecture

```
User Query
    ↓
Embedding Generation (sentence-transformers)
    ↓
ChromaDB Semantic Search (cosine similarity)
    ↓
Confidence Scoring (1 - distance)
    ↓
┌─────────────────┬──────────────────┬──────────────────┐
│ High (≥ 0.85)   │ Medium (0.70-.84)│ Low (< 0.70)     │
│ Auto-execute    │ Confirm          │ Show alternatives│
└─────────────────┴──────────────────┴──────────────────┘
    ↓
Command Generation
    ↓
Execution (cd <proto_dir> && <command>)
```

## What Gets Indexed

For each prototype (.project file):
- Name and description
- Key features
- Tech stack
- Entry points (orchestrator.py, main.py, etc.)
- Available agents (for orchestrator-based prototypes)
- Phase and status

## Supported Query Types

1. **Prototype execution**: "run company researcher", "execute sales tool"
2. **Agent-specific**: "run tech agent", "analyze social media"
3. **Preset modes**: "quick research", "full analysis"
4. **Task-based**: "research a company", "analyze tech stack"
5. **Feature-based**: "sales intelligence", "document parsing"

---

**Status**: Ready to use
**Version**: 1.0.0
**Last Updated**: 2025-11-20
