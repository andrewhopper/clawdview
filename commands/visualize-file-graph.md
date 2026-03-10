---
description: Visualize markdown file connection graph with Mermaid diagram
version: 1.0.0
tags: [documentation, visualization, graph, project]
---

# Visualize File Connection Graph

Generate a Mermaid diagram showing connections between markdown files in the repository.

## Usage

```bash
/visualize-file-graph [max-nodes] [output-path]
```

**Parameters:**
- `max-nodes` (optional): Maximum nodes to include in graph (default: 30)
- `output-path` (optional): Output file path (default: docs/diagrams/file-connections.md)

## Examples

```bash
# Generate with defaults (30 nodes)
/visualize-file-graph

# Generate larger graph (50 nodes)
/visualize-file-graph 50

# Custom output location
/visualize-file-graph 30 docs/custom-graph.md
```

## What It Does

1. Scans all markdown files in repository
2. Parses `[text](file.md)` link patterns
3. Builds connection graph
4. Generates Mermaid diagram with:
   - File nodes (colored by type: CLAUDE.md, README.md, prototypes)
   - Directed edges showing references
   - Link text as edge labels
5. Includes summary statistics:
   - Total files and links
   - Top files by outgoing/incoming connections

## Output

Creates markdown file with:
- Summary statistics table
- Mermaid graph visualization
- Color-coded nodes for different file types

---

Execute the visualization script now.

```bash
# Parse arguments
MAX_NODES=${1:-30}
OUTPUT_PATH=${2:-docs/diagrams/file-connections.md}

# Run visualization
python3 shared/scripts/visualize_markdown_links.py \
  --summary \
  --max-nodes "$MAX_NODES" \
  --output "$OUTPUT_PATH"

echo ""
echo "✅ Graph visualization complete!"
echo "📊 View at: $OUTPUT_PATH"
echo ""
echo "💡 Tip: Increase max-nodes for larger graph (warning: may be cluttered)"
echo "   Example: /visualize-file-graph 50"
```
