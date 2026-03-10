# Assemble Project Overview

Collect all project card.html files and assemble into a PDF-ready HTML document.

## Usage

```
/assemble-overview [--category work,oss] [--status active] [--open]
```

## Arguments

- `--category` - Filter by category (comma-separated): work, shared, oss, personal
- `--status` - Filter by status: active (default), archived, completed
- `--open` - Open in browser after generation

## Instructions

Run the assembler script:

```bash
python3 shared/templates/project-overview/assembler.py $ARGS
```

Or if no cards exist yet, report:

```
No card.html files found.
Generate cards first by navigating to each project and running /generate-card
Or use subagents to generate cards in parallel.
```

## Examples

```bash
# All active projects
python3 shared/templates/project-overview/assembler.py --open

# Work projects only
python3 shared/templates/project-overview/assembler.py --category work --open

# Work and OSS projects
python3 shared/templates/project-overview/assembler.py --category work,oss --open

# Archived projects
python3 shared/templates/project-overview/assembler.py --status archived --open
```

## Output

- Generates: `shared/templates/project-overview/overview-{YYYY-MM-DD}.html`
- 4 projects per page
- Grouped by category (Work > Shared > OSS > Personal)
- Footer with date, page number, git hash

## Parallel Card Generation

To generate cards for multiple projects at once, use subagents:

```
Generate card.html files for all active work projects using parallel subagents.
```

This will spawn subagents that each:
1. Navigate to a project directory
2. Read .project file
3. Generate docs/card.html
4. Report completion
