## 🤖 DEFAULT LLM MODELS

**Primary: Claude Sonnet 4.5** - Default model for all prototypes
**Fast: Claude Haiku 4.5** - For fast/cheap tasks

**AWS Bedrock Model IDs:**
```
# Primary - Claude Sonnet 4.5 (global cross-region)
global.anthropic.claude-sonnet-4-5-20250929-v1:0

# Fast/Cheap - Claude Haiku 4.5
us.anthropic.claude-haiku-4-5-20251001-v1:0

# Embeddings - Cohere Embed v4
global.cohere.embed-v4:0
```

**Key Details:**
- **Region:** us-east-1 (required for global cross-region inference profiles)
- **Capabilities:** Multimodal (text + vision), structured outputs, function calling
- **Use Cases:** Document analysis, code generation, semantic mapping, AI agents
- **API Version:** bedrock-2023-05-31

**Environment Configuration:**
```bash
AWS_REGION=us-east-1
LLM_PROVIDER=bedrock
LLM_MODEL=global.anthropic.claude-sonnet-4-5-20250929-v1:0
LLM_MODEL_FAST=us.anthropic.claude-haiku-4-5-20251001-v1:0
EMBEDDING_MODEL=global.cohere.embed-v4:0
```

### Writing Rules
**✅ DO:** Numbered lists, tables, `→`, remove filler
**❌ DON'T:** Prose, redundancy, full sentences when bullets work

**List Format:** ALL lists MUST use numbered format (1., 2., 3., etc.)
- Use numbered lists for all items (tasks, ideas, criteria, examples)
- Exception: Checkboxes (✅/❌) for yes/no comparisons only
- Nested lists: 1., 1.1, 1.2 or 1., 2., 2.1, 2.2

Examples:
- ❌ "The system provides capability to generate high-quality content through iterative process..."
- ✅ "System: LLM + human feedback → quality improvement"
- ❌ Bullet list: "- Item 1, - Item 2, - Item 3"
- ✅ Numbered list: "1. Item 1, 2. Item 2, 3. Item 3"

### Document Format
**Decimal Outline Required:** ALL documents MUST use decimal outline format.

**Format:** Hierarchical numbering (1.0, 1.1, 1.1.1, 1.1.2, 1.2, 2.0, etc.)

**Document Title Format:** ALL phase artifacts MUST include stage number in title:
- `# Stage 1 - Concept Seed`
- `# Stage 2 - Research`
- `# Stage 3 - Idea Expansion`
- `# Stage 4 - Idea Analysis`
- `# Stage 5 - Candidate Selection`
- `# Stage 6 - Technical Design`
- `# Stage 7 - Test Design`
- `# Stage 8 - Implementation`
- `# Stage 9 - Refinement`

**Example:**
```
# Stage 3 - Idea Expansion

1.0 Introduction
  1.1 Background
  1.2 Purpose
2.0 Architecture
  2.1 Components
    2.1.1 Frontend
    2.1.2 Backend
  2.2 Data Flow
3.0 Implementation
```

**Rules:**
- Document title MUST start with "# Stage X - [Phase Name]"
- Use decimal numbering for all sections/subsections
- Apply to ALL phase deliverables (seed.md, expansion.md, analysis.md, design docs, etc.)
- Maintain consistent indentation (2 spaces per level)
- Number ALL major sections starting from 1.0

### Markdown Visual Requirements
**REQUIRED:** ASCII art + diagrams in ALL markdown files for rapid comprehension

**Must include:**
- Architecture/flow diagrams (system components, data flow)
- Visual hierarchy (boxes, arrows, relationships)
- Quick-assessment visual at document start
- Tables for comparisons, structured data, matrices

**Example ASCII diagrams:**
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │─────▶│   Server    │─────▶│  Database   │
└─────────────┘      └─────────────┘      └─────────────┘
      │                     │                     │
      ▼                     ▼                     ▼
  [Request]            [Process]              [Store]

Phase Flow:
SEED → RESEARCH → EXPANSION → ANALYSIS → SELECTION → DESIGN → TEST → IMPL → REFINE
  1       2          3           4           5          6       7      8       9
```

**Why:** 10-second visual scan vs. reading entire document

**Applies to:**
- All phase deliverables (seed.md, research.md, design docs, etc.)
- README.md files (MUST have architecture/structure diagram)
- Technical specifications
- Analysis documents
- All .md files

**Enforcement:** Documents rejected without visual elements before phase transitions

