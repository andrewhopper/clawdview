# Classify Unspecified Projects

Analyze and organize projects in `projects/unspecified/` using heuristic-based classification.

## Usage

Run the classification tool to analyze unspecified projects:

```bash
python3 hmode/shared/tools/project-classifier/classify_projects.py --root .
```

## Options

| Flag | Description |
|------|-------------|
| `--all` | Show all projects (not just top 20 per category) |
| `--json` | Output as JSON for batch processing |
| `--category CATEGORY` | Filter by suggested category (work/oss/shared/personal) |
| `--batch-move TARGET` | Move all high-confidence projects to TARGET category |
| `--execute` | Actually execute moves (use with --batch-move) |
| `--duplicates-only` | Only show duplicate project groups |

## Examples

### Preview work classifications
```bash
python3 hmode/shared/tools/project-classifier/classify_projects.py --root . --category work
```

### Batch move all work projects (dry run)
```bash
python3 hmode/shared/tools/project-classifier/classify_projects.py --root . --category work --batch-move work
```

### Execute batch move
```bash
python3 hmode/shared/tools/project-classifier/classify_projects.py --root . --category work --batch-move work --execute
```

### Find duplicates
```bash
python3 hmode/shared/tools/project-classifier/classify_projects.py --root . --duplicates-only
```

## Classification Heuristics

| Category | Patterns |
|----------|----------|
| **work** | aws-*, bedrock, workshop-*, kiro-*, medical-doc, slack-automation, sa-* |
| **oss** | diagram-craft, overwatch, frontgate, remarkable-*, repo-sync, baml-*, kiro-rules |
| **shared** | lib-*, service-*, protocol-*, domain-model-*, tool-browser, tool-claude-person |
| **personal** | kids-story, avatar-*, dementia-*, *-clone, tinder-*, news-digest, todo-manager |

## Workflow

1. Run report to see suggestions
2. Review high-confidence (✓) projects
3. Batch move categories you agree with
4. Manually classify unknown (!) projects

## After Classification

Run `/flow` to update project tracking.
