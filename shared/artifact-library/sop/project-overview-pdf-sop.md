# SOP: Generate Project Overview PDF

## Purpose
Generate a printable PDF overview of monorepo projects with visual stage indicators, file counts, and category badges.

## When to Use
- Weekly/monthly project reviews
- Portfolio planning sessions
- Stakeholder updates
- Personal project tracking

## Architecture

### Distributed Card Storage
Each project stores its own `docs/card.html` file. Cards are assembled on-demand into a paginated PDF.

```
projects/work/active/my-project/
├── .project           ← Project metadata
├── docs/
│   └── card.html      ← Project card (generated)
└── ...

shared/templates/project-overview/
├── card-template.html ← Base template
├── styles.css         ← Shared styles
└── assembler.py       ← PDF assembly script
```

### Benefits
- Small context per card generation
- Incremental updates (regenerate single card)
- Parallel generation via subagents
- Flexible filtering by category/status

---

## Workflow

### Option A: Generate Single Card

Navigate to a project and run:
```
/generate-card
```

This creates `docs/card.html` in the current project.

### Option B: Generate Cards in Parallel

Use subagents to generate multiple cards:
```
Generate card.html files for all active work projects using parallel subagents.
```

### Option C: Assemble PDF

After cards exist, run:
```
/assemble-overview [--category work,oss] [--status active] [--open]
```

Or directly:
```bash
python3 shared/templates/project-overview/assembler.py --open
```

---

## Card Generation Details

### Required Data (from .project)
- `name` - Project name
- `uuid` - Project UUID
- `phase` - Current SDLC phase (1-9)
- `category` - personal/work/oss/shared
- `status` - active/archived/completed
- `description` - Brief summary
- `tech_stack` - Technologies used
- `domain` - Deployed URL (if any)

### File Count
```bash
find {project_path} -type f \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/__pycache__/*" \
  ! -path "*/.venv/*" | wc -l
```

### Summary Format
- 1 sentence max
- Format: "{What it does}. Target: {who it's for}."
- No flowery language

### Phase Classes
- Phases before current: `completed` (green)
- Current phase: `active` (blue)
- Phases after current: empty (gray)

---

## Assembly Details

### Command
```bash
python3 shared/templates/project-overview/assembler.py [OPTIONS]

Options:
  --category CATS    Filter: work,shared,oss,personal (comma-separated)
  --status STATUS    Filter: active, archived, completed
  --output FILE      Output path (default: overview-{date}.html)
  --open             Open in browser
```

### Examples
```bash
# All active projects
python3 assembler.py --open

# Work + OSS only
python3 assembler.py --category work,oss --open

# Archived projects
python3 assembler.py --status archived --open
```

### Output
- Location: `shared/templates/project-overview/overview-{YYYY-MM-DD}.html`
- 4 projects per page
- Grouped by category (Work > Shared > OSS > Personal)
- Footer: date, page number, git hash

---

## Visual Elements

### Category Badges
| Category | Color |
|----------|-------|
| Work | Blue |
| Shared | Orange |
| OSS | Green |
| Personal | Purple |
| Unspecified | Gray dashed |

### Phase Indicators
9 horizontal bars:
- Green = completed phases
- Blue = current phase
- Gray = pending phases

### Phase Names
1. Research
2. Expand
3. Analyze
4. Select
5. PRD
6. Design
7. Test
8. Implementation
9. Refinement

---

## Files

| File | Purpose |
|------|---------|
| `shared/templates/project-overview/card-template.html` | Base card template |
| `shared/templates/project-overview/styles.css` | Shared CSS styles |
| `shared/templates/project-overview/assembler.py` | Assembly script |
| `.claude/commands/generate-card.md` | /generate-card command |
| `.claude/commands/assemble-overview.md` | /assemble-overview command |

---

## Print to PDF
1. Open generated HTML in browser
2. Cmd+P → Save as PDF
3. Ensure "Print backgrounds" is checked
