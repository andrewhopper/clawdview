# Semantic Intent Resolution

**Decision Date**: 2025-11-20
**Status**: Approved
**Category**: Developer Tools / Natural Language Interface

## Approved Technology Stack

### Core Components

1. **Embedding Model**: sentence-transformers (all-MiniLM-L6-v2)
   - 384-dimensional embeddings
   - 80MB model size
   - Apache 2.0 license
   - Fast inference (~50ms)
   - 100% local (no API calls)

2. **Vector Database**: ChromaDB 0.4.x
   - SQLite backend (persistent storage)
   - HNSW indexing algorithm
   - Cosine similarity search
   - Lightweight (~5KB per indexed prototype)
   - No external dependencies

3. **Language**: Python 3.9+
   - Standard library for subprocess execution
   - pathlib for cross-platform path handling
   - json for metadata parsing

## Rationale

### Why Embeddings (vs keyword search)?

**Semantic Understanding**:
- "company researcher" matches "sales intelligence" (related concepts)
- "analyze tech stack" resolves to "tech" agent (understands intent)
- "quick research" maps to `--preset quick` (contextual understanding)

**Keyword Search Limitations**:
- Requires exact term matching
- "company researcher" wouldn't match "sales intelligence tool"
- No understanding of synonyms or related concepts

### Why ChromaDB (vs FAISS, Pinecone, etc.)?

**Local-first**: No API keys, no external services, works offline
**Simple**: SQLite backend, no server required
**Proven**: Used by LangChain, LlamaIndex, major AI frameworks
**Lightweight**: ~150KB total for 30 prototypes
**Persistent**: Survives restarts, no re-indexing needed

**Alternatives Considered**:
- FAISS: Lower-level, requires more manual management
- Pinecone: Cloud-based, costs money, requires API
- Weaviate: Too heavy, requires Docker/server
- Pure SQLite FTS5: No semantic understanding, keyword-only

### Why all-MiniLM-L6-v2 (vs other models)?

**Size**: 80MB (vs 420MB for all-mpnet-base-v2)
**Speed**: ~50ms inference (fast enough for interactive use)
**Quality**: 0.68 average score on semantic similarity benchmarks
**License**: Apache 2.0 (permissive, commercial-friendly)
**Multilingual**: Supports multiple languages (future-proof)

## Use Cases

### Primary: Prototype Execution
```bash
/run company researcher
→ Resolves to proto-company-researcher-uiwid-005
→ Executes python orchestrator.py
```

### Secondary: Agent Resolution
```bash
/run analyze tech stack
→ Prototype: company-researcher
→ Agent: tech
→ Executes python orchestrator.py --agents tech
```

### Tertiary: Preset Detection
```bash
/run quick company research
→ Prototype: company-researcher
→ Preset: quick
→ Executes python orchestrator.py --preset quick
```

## Confidence Thresholds

```python
HIGH_CONFIDENCE = 0.85    # Auto-execute immediately
MEDIUM_CONFIDENCE = 0.70  # Confirm with user
LOW_CONFIDENCE = 0.50     # Show alternatives + select
```

**Rationale**:
- High threshold (0.85): Only auto-execute when very confident
- Medium threshold (0.70): Give user quick confirmation option
- Low threshold (0.50): Prevent false positives, show alternatives

## Performance Characteristics

- **Indexing Time**: ~2 seconds per prototype (one-time cost)
- **Query Latency**: ~50ms (embedding + search)
- **Storage**: ~5KB per prototype (~150KB for 30 prototypes)
- **Model Load**: ~1 second (first query only, cached thereafter)
- **Memory**: ~200MB (model + ChromaDB in-memory)

## Security Considerations

- **Local-only**: No data leaves the machine
- **No credentials**: No API keys or secrets required
- **Sandboxed**: Executes in user's shell context (same as manual execution)
- **No eval()**: No dynamic code execution, subprocess only

## Maintenance

### Re-indexing Frequency
- **On-demand**: After adding new prototypes or updating .project files
- **Manual**: `python index_prototypes.py --rebuild`
- **Future**: Could add file watcher for auto-indexing

### Model Updates
- **Sticky version**: Pin to all-MiniLM-L6-v2 (stable)
- **Upgrade path**: Test new models, compare quality, migrate if significant improvement
- **Backward compat**: Store model version in ChromaDB metadata

## Integration Points

### Slash Command: `/run`
```markdown
.claude/commands/run.md → Semantic resolver → Execution
```

### Global Tool
```bash
shared/tools/semantic-run/semantic_resolver.py
```

### Future: Claude Code Built-in
- Potential to integrate directly into Claude Code as native feature
- Would remove need for manual indexing
- Could auto-detect new prototypes

## Approval Checklist

- ✅ Technology stack documented
- ✅ Rationale provided (why these choices)
- ✅ Alternatives considered
- ✅ Performance characteristics defined
- ✅ Security implications reviewed
- ✅ Maintenance plan established
- ✅ Integration points identified

## Related Documents

- `shared/tools/semantic-run/README.md` - User documentation
- `.claude/commands/run.md` - Slash command docs
- `shared/tools/semantic-run/index_prototypes.py` - Indexer implementation
- `shared/tools/semantic-run/semantic_resolver.py` - Resolver implementation

---

**Approved by**: Human (2025-11-20)
**Implemented by**: Claude Code (2025-11-20)
**Status**: Production-ready
