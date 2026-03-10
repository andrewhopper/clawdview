---
name: workon
description: Find and launch projects using natural language. Activate when user says "let's work on", "where is", "I want to work on", "continue working on", "keep working on", "resume work on", "find project", or "open project".
version: 1.0.0
---

# Work On - Semantic Project Finder & Launcher

**Automatically activated on work-related phrases: let's work on, where is, I want to work on, continue working on, keep working on, resume work on**

This skill combines project search with the semantic prototype launcher to find and execute projects using natural language.

## Trigger Phrases

This skill activates when the user says:
- "let's work on [project]"
- "where is [project]"
- "I want to work on [project]"
- "continue working on [project]"
- "keep working on [project]"
- "resume work on [project]"
- "find project [name]"
- "open project [name]"
- "work on the [project]"

## Execution Flow

### 1. Extract Search Query

Parse the user's message to extract the project name/description:

```
"let's work on the portfolio manager" → query: "portfolio manager"
"where is the semantic run tool" → query: "semantic run tool"
"I want to work on gocoder" → query: "gocoder"
```

### 2. Search Strategy (Priority Order)

Use the semantic prototype launcher to find matches:

```bash
cd /Users/andyhop/dev/lab/hmode/shared/tools/semantic-run
uv run python semantic_resolver.py "<query>" --dry-run
```

This will:
1. Generate embeddings for the query
2. Search ChromaDB vector store
3. Return confidence scores for matches
4. Show entry points and available agents

**Alternative: Use /workon command**

If semantic_resolver.py fails or returns no results, fall back to the /workon command which searches:
1. Nav hints (`.claude/nav-hints/hints.yaml`)
2. Project files (`projects/**/.project`)
3. Ideas (`project-management/ideas/active/*.md`)

### 3. Present Results

#### High Confidence Match (≥ 0.85)

```
✓ Found: company-researcher (confidence: 0.94)
  📁 projects/shared/active/claude-person-searcher-iyauu
  📝 Automated sales intelligence gathering system
  🛠️ Python, Claude CLI, Firecrawl MCP
  🚀 Entry point: python orchestrator.py

Navigate to project? [Y/n]
```

#### Medium Confidence Match (0.70-0.84)

```
Match: s3-publish-tool (confidence: 0.78)
  📁 projects/unspecified/active/tool-s3-publish-cli-vayfd
  📝 S3 file publishing with presigned URLs
  🛠️ Python, AWS CDK, Click
  🚀 Entry point: python main.py

Is this correct? [Y/n]
```

#### Low Confidence / Multiple Matches (< 0.70)

```
Found 3 potential matches for "portfolio":

[1] tool-project-portfolio-manager-lk5aa  ████████░░
    📁 projects/unspecified/active/
    📝 Portfolio manager with CLI launcher and web UI
    🛠️ React, Ink, Vite, Tailwind
    🔄 Completed | 7.8k lines
    🚀 npm run dev

[2] proto-prototype-dashboard-24tsu  ██░░░░░░░░
    📁 projects/unspecified/
    📝 Web dashboard for prototype lifecycle
    🛠️ Next.js 14, React, Tailwind
    🔄 Phase 2 | idea only
    🚀 npm start

[3] personal-portfolio-site  █░░░░░░░░░
    📁 projects/personal/ideas/
    📝 Personal project portfolio website
    🛠️ (not specified)
    🔄 Phase 1 | idea only

Select [1-3] or 'n' to cancel:
```

### 4. Navigate to Project

Once user confirms selection:

```bash
cd <project_directory>
```

Then provide context:

```
Now working on: <project-name>

Current Status:
- Phase: <phase>
- Status: <active/completed/paused>
- Tech Stack: <technologies>
- Entry Point: <command>

What would you like to do?
[1] Read .project file
[2] Run the project
[3] View recent changes (git log)
[4] Open in editor
[5] Just explore
```

### 5. Quick Actions

After navigating, offer quick actions based on project type:

**For orchestrator-based projects:**
```
Available agents: company, team, tech, social, press
Run with: python orchestrator.py --agents <agent>

Quick runs:
[1] All agents
[2] Specific agent (select)
[3] Quick preset
[4] Full preset
```

**For web projects:**
```
Available commands:
[1] npm run dev
[2] npm run build
[3] npm test
```

**For Python projects:**
```
Available commands:
[1] python main.py
[2] python cli.py --help
[3] pytest
```

## Integration with Semantic Resolver

The semantic resolver (`hmode/shared/tools/semantic-run/semantic_resolver.py`) provides:

### Agent Detection

For queries like "research company tech stack":
- Detects prototype: company-researcher
- Detects agent: tech
- Builds command: `python orchestrator.py --agents tech`

### Preset Detection

For queries like "quick company research":
- Detects prototype: company-researcher
- Detects preset: quick
- Builds command: `python orchestrator.py --preset quick`

### Entry Point Resolution

Automatically finds executable entry points:
1. Python: `orchestrator.py`, `main.py`, `app.py`, `cli.py`, `run.py`
2. Node: `index.js`, `server.js`
3. npm scripts: `start`, `dev`, `run`

Priority: orchestrator > main > app > cli > run > npm_start

## Technical Details

### File Locations

- **Semantic resolver**: `hmode/shared/tools/semantic-run/semantic_resolver.py`
- **Project indexer**: `hmode/shared/tools/semantic-run/index_prototypes.py`
- **Vector database**: `hmode/shared/tools/semantic-run/chroma.sqlite3`
- **Nav hints**: `.claude/nav-hints/hints.yaml`
- **Workon command**: `hmode/commands/workon.md`

### Confidence Thresholds

```python
HIGH_CONFIDENCE = 0.85    # Auto-suggest with confirmation
MEDIUM_CONFIDENCE = 0.70  # Show best match, ask to confirm
LOW_CONFIDENCE = 0.50     # Show multiple alternatives
```

### Search Performance

- Query latency: ~50ms
- Embedding generation: ~20ms
- Vector search: ~30ms
- Model: all-MiniLM-L6-v2 (384-dim vectors)

## Error Handling

### Database Not Found

```
✗ Error: Semantic index not found. Building index...
```

Run indexer:
```bash
cd hmode/shared/tools/semantic-run
python3 index_prototypes.py
```

### No Matches Found

```
No projects found matching "<query>".

Try:
[1] Different search term
[2] Browse all projects
[3] Create new project
```

### Ambiguous Query

```
Query too vague. Please be more specific:
- Include tech stack (e.g., "react project")
- Include purpose (e.g., "portfolio manager")
- Include keywords (e.g., "s3 upload tool")
```

## Examples

### Example 1: Direct Match

```
User: "let's work on the semantic run tool"
AI: Searching for "semantic run tool"...

✓ Found: semantic-run (confidence: 0.96)
  📁 hmode/shared/tools/semantic-run
  📝 Natural language project execution with vector search
  🛠️ Python, ChromaDB, sentence-transformers
  🚀 Entry point: python semantic_resolver.py

Navigate to project? [Y/n]

User: y

AI: Now in hmode/shared/tools/semantic-run

Current Status:
- Phase: Production
- Status: Active
- Tech Stack: Python, ChromaDB, sentence-transformers
- Entry Point: python semantic_resolver.py "<query>"

What would you like to do?
[1] Read documentation
[2] Test the resolver
[3] Re-index projects
[4] View code
[5] Just explore
```

### Example 2: Agent-Specific Run

```
User: "I want to work on company tech stack research"

AI: Searching for "company tech stack research"...

✓ Found: company-researcher (confidence: 0.89)
  Agent detected: tech
  📁 projects/shared/active/claude-person-searcher-iyauu
  📝 Automated sales intelligence with 12 specialized agents
  🛠️ Python, Claude CLI, Firecrawl MCP
  🚀 Command: python orchestrator.py --agents tech

Run now? [Y/n]

User: y

AI: Executing: cd projects/shared/active/claude-person-searcher-iyauu && python orchestrator.py --agents tech

[Output from orchestrator...]
```

### Example 3: Multiple Matches

```
User: "where is the portfolio project"

AI: Found 3 matches for "portfolio project":

[1] tool-project-portfolio-manager-lk5aa  ████████░░
    📁 projects/unspecified/active/
    📝 Portfolio manager with CLI launcher and web UI
    🛠️ React, Ink, Vite, Tailwind
    🔄 Completed | 7.8k lines
    🚀 npm run dev

[2] proto-portfolio-dashboard-24tsu  ██░░░░░░░░
    📁 projects/unspecified/
    📝 Web dashboard for project portfolio
    🛠️ Next.js 14, React
    🔄 Phase 2 | idea only

[3] personal-portfolio-site  █░░░░░░░░░
    📁 projects/personal/ideas/
    📝 Personal portfolio website
    🛠️ (not specified)
    🔄 Phase 1 | idea only

Select [1-3] or 'n' to cancel:

User: 1

AI: Navigating to tool-project-portfolio-manager-lk5aa...

Now working on: Portfolio Manager

Current Status:
- Phase: 9 (Refinement)
- Status: Completed
- Tech Stack: React, Ink, Vite, Tailwind
- Entry Point: npm run dev

What would you like to do?
[1] Start dev server (npm run dev)
[2] View .project file
[3] Check git status
[4] Just explore
```

## Implementation Notes

### When to Use This Skill vs /run Command

**Use this skill (workon):**
- User wants to navigate to a project
- User wants to explore a project structure
- User needs context about a project
- User is uncertain about project name

**Use /run command directly:**
- User wants immediate execution
- User knows exact project name
- User specifies agent/preset
- User wants quick, non-interactive run

### Skill Flow

```
User phrase detected
    ↓
Extract search query
    ↓
Run semantic resolver (--dry-run)
    ↓
Evaluate confidence score
    ↓
Present results (high/medium/low)
    ↓
User confirms selection
    ↓
Navigate to directory (cd)
    ↓
Load project context (.project)
    ↓
Offer quick actions
    ↓
Execute user choice
```

### State Management

After navigation, maintain context:
- Current project name
- Current project directory
- Available commands
- Recent execution history

This allows follow-up commands like:
- "run it"
- "show me the code"
- "what's the current phase"

## Integration Points

### 1. With /run Command

```bash
# User: "let's work on company researcher"
# Skill navigates, then offers:
Run now with: /run company researcher
```

### 2. With /workon Command

```bash
# Fallback if semantic resolver unavailable
hmode/commands/workon.md
```

### 3. With Nav Hints

```yaml
# .claude/nav-hints/hints.yaml
- project_path: hmode/shared/tools/semantic-run
  aliases:
    - semantic run
    - prototype launcher
    - run tool
  description: Natural language project execution
```

### 4. With Project Indexer

Keep index fresh:
```bash
# Run after adding/updating projects
cd hmode/shared/tools/semantic-run
python3 index_prototypes.py --rebuild
```

## Summary

This skill provides a conversational, natural language interface to:
1. Find projects using semantic search
2. Navigate to project directories
3. Load project context
4. Offer quick execution options
5. Integrate with existing tools (/run, /workon)

The combination of semantic search + contextual navigation + quick actions creates a smooth "I want to work on X" → [working on X] experience.
