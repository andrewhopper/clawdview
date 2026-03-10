---
description: Find and resume work on projects/ideas by fuzzy search
tags: [workflow, projects, search, resume]
args:
  - name: query
    description: "Search term (e.g., 'portfolio', 'ai agent', 'scheduler')"
    required: false
---

# Work On - Project Finder

Find and resume work on projects or ideas using fuzzy search.

## Trigger Phrases

This command auto-triggers when user says:
- "let's work on..."
- "continue working on..."
- "I want to work on..."
- "keep working on..."
- "resume work on..."

## Execution Steps

### 1. Parse Query

Extract search term from `$ARGUMENTS` or natural language.

### 2. Search Strategy

**MANDATORY: Always use Overwatch semantic search API**

Query the Overwatch search API at `http://localhost:5557/search` with the search term. This provides:
- Semantic understanding of project descriptions (e.g., "auth system" matches "authentication gateway")
- Fuzzy matching beyond simple keyword search
- Conceptually related projects, not just keyword matches
- Combined results from nav hints, projects, and ideas

**API Request:**
```bash
curl -X POST http://localhost:5557/search \
  -H "Content-Type: application/json" \
  -d '{"query": "<search_term>", "limit": 10}'
```

**Fallback (if Overwatch unavailable):**

If semantic search API is not running, fall back to file-based search:

1. **Nav Hints (Priority)** - Search `.claude/nav-hints/hints.yaml` first
   - Match against: `aliases` list for each project
   - Direct alias mapping to `project_path`
   - Case-insensitive matching

2. **Projects** - Search all `.project` files in `projects/`
   - Match against: `name`, `description`, `id`, folder name
   - Include: `projects/{oss,personal,shared,work,unspecified}/{active,ideas}/**/.project`

3. **Ideas** - Search markdown files in `project-management/ideas/`
   - Match against: filename, frontmatter title, content
   - Include: `project-management/ideas/active/*.md`

### 3. Scoring

For each match, calculate relevance (base + maturity bonus):

**Base Score (text match):**
| Match Type | Score |
|------------|-------|
| Exact alias match (nav hints) | 100 |
| Alias contains query (nav hints) | 90 |
| Exact name match (.project) | 85 |
| Name contains query (.project) | 75 |
| ID contains query | 70 |
| Description contains query | 60 |
| Folder path contains query | 50 |

**Maturity Bonus (added to base):**
| Maturity Signal | Bonus |
|-----------------|-------|
| Has code (>100 lines) | +30 |
| Has package.json/requirements.txt | +20 |
| Phase 5+ (past selection) | +15 |
| Phase 8+ (implementation) | +25 |
| Status: completed | +10 |
| Has node_modules/.venv | +10 |
| Updated in last 7 days | +15 |

**Maturity Penalties:**
| Signal | Penalty |
|--------|---------|
| Idea only (no code) | -20 |
| Status: archived | -10 |
| No updates in 30+ days | -10 |

**Final Score** = Base + Maturity Bonus - Penalties

This ensures built projects rank above ideas, and actively developed projects rank above stale ones.

### 4. Present Results

Show top 3 matches with format (include tech stack summary):

```
Found matches for "<query>":

[1] tool-project-portfolio-manager-lk5aa-014  ████████░░
    📁 projects/unspecified/active/
    📝 Portfolio manager with CLI launcher and web UI
    🛠️ React, Ink, Vite, Tailwind
    🔄 Completed | 7.8k lines

[2] proto-prototype-dashboard-24tsu-137  ██░░░░░░░░
    📁 projects/unspecified/
    📝 Web dashboard for prototype lifecycle
    🛠️ Next.js 14, React, Tailwind
    🔄 Phase 2 | idea only

[3] tool-project-portfolio-lk5aa-014  █░░░░░░░░░
    📁 projects/personal/ideas/
    📝 Personal project portfolio site
    🛠️ Node.js, JavaScript
    🔄 Phase 2 | idea only

Continue with? [1/2/3/n]
```

**Maturity bar:** `████████░░` = 80% mature (has code, deps, tests)
- Full bar (10 blocks) = production-ready
- Empty bar = idea/spec only

**Tech stack line format:**
- Extract from `.project` `tech_stack` field
- Prioritize frameworks/tools over languages: React, Next.js, FastAPI, Django, Express, etc.
- Only show language if no framework (e.g., "Python CLI" or "Bash script")
- Flatten frontend/backend/infra into single line, max 3-4 items
- If no tech_stack: show `(idea - no tech yet)` or `(not specified)`

**Priority order:** Framework > Library > Runtime > Language
Examples:
- `Next.js, Tailwind, Prisma` ✓ (not "TypeScript, CSS, SQL")
- `FastAPI, PostgreSQL, Redis` ✓ (not "Python")
- `React, Express, MongoDB` ✓ (not "JavaScript, Node.js")
- `Python CLI` ✓ (when no framework, specify type)

**Status line format:**
- Show phase OR completion status
- Show lines of code if >100, otherwise "idea only"
- Examples:
  - `🔄 Completed | 7.8k lines`
  - `🔄 Phase 8 | 2.1k lines`
  - `🔄 Phase 2 | idea only`

### 5. Handle Selection

**If user selects 1-3:**
1. Navigate to project directory
2. Read `.project` file
3. Load context: "Working on: {name} - {description}"
4. Show current phase and next steps
5. If has `.project`, display: "Resume where you left off? [Y/n]"

**If user enters 'n':**
- "No problem. What would you like to work on instead?"

**If no matches:**
- "No matches found for '{query}'. Try a different search term or create a new project?"

## Quick Examples

```bash
# Direct command
/workon portfolio
/workon ai agent
/workon scheduler

# Natural language (auto-detected)
"let's work on the portfolio project"
"continue working on my ai agent"
"I want to keep working on the scheduler"
```

## Implementation Details

### Nav Hints Search (Python)

```python
import yaml
from pathlib import Path

def search_nav_hints(query: str) -> list:
    """Search nav hints for alias matches."""
    hints_file = Path('.claude/nav-hints/hints.yaml')
    if not hints_file.exists():
        return []

    with open(hints_file) as f:
        hints = yaml.safe_load(f)['hints']

    matches = []
    query_lower = query.lower()

    for hint in hints:
        project_path = hint['project_path']
        description = hint.get('description', '')

        for alias in hint['aliases']:
            alias_lower = alias.lower()

            # Exact match
            if alias_lower == query_lower:
                matches.append({
                    'path': project_path,
                    'score': 100,
                    'match_type': 'exact_alias',
                    'match_text': alias,
                    'description': description
                })
                break  # Don't check other aliases for this project

            # Contains match
            elif query_lower in alias_lower or alias_lower in query_lower:
                matches.append({
                    'path': project_path,
                    'score': 90,
                    'match_type': 'alias_contains',
                    'match_text': alias,
                    'description': description
                })
                break  # Don't check other aliases for this project

    return matches
```

### Search Command (Bash)

```bash
# 1. Search nav hints first (Python)
python3 -c "
import yaml
query = '$QUERY'
with open('.claude/nav-hints/hints.yaml') as f:
    hints = yaml.safe_load(f)['hints']
for hint in hints:
    for alias in hint['aliases']:
        if query.lower() in alias.lower():
            print(hint['project_path'])
            break
"

# 2. Find all .project files and grep for query
find projects -name ".project" -exec grep -l -i "<query>" {} \;

# 3. Search ideas
grep -r -l -i "<query>" project-management/ideas/active/
```

### Parse .project YAML

Extract these fields for display:
- `name` - Project name
- `description` - Brief description
- `phase` - Current phase (1-9)
- `status` - active/paused/completed
- `ownership` - personal/work/shared/oss
- `updated_at` - Last activity date

### Fuzzy Matching

If exact match fails, try:
1. Lowercase comparison
2. Partial word matching
3. Levenshtein distance < 3

## Nav Hints Integration

### How It Works

1. **Query "auth":**
   - Searches aliases in `.claude/nav-hints/hints.yaml`
   - Finds exact match: "auth" → `projects/shared/shared-auth-gateway`
   - Returns with score 100 (highest priority)

2. **Query "gocoder":**
   - Finds exact match: "gocoder" → `projects/personal/active/gocoder-t9x2k`
   - Also matches URL alias: "gocoder.b.lfg.new"
   - Returns with score 100

3. **Query "meeting":**
   - Finds partial match: "meeting" in "meeting buddy"
   - Returns `projects/unspecified/active/meeting-buddy-ll07j` with score 90

### Advantages

- **Instant recognition** of URLs, nicknames, abbreviations
- **No ambiguity** for commonly referenced projects
- **Faster search** with curated aliases
- **Multiple names** for same project (e.g., "auth", "auth.x.lfg.new", "shared auth")

### Maintenance

To add new hints, edit `.claude/nav-hints/hints.yaml`:

```yaml
- project_path: projects/your/project/path
  aliases:
    - shortname
    - url.domain.com
    - nickname
  description: Brief description
```

Then validate: `.claude/nav-hints/validate-hints.py`

---

**Version**: 2.1.0 (Semantic Search Mandatory)
**Updated**: 2026-01-27
**Created**: 2025-12-01
