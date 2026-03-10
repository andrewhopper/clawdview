---
uuid: cmd-upd-man-6d7e8f9g
version: 1.0.0
last_updated: 2025-11-10
description: Update project manifest and README with latest prototype data
---

# Update Project Manifest

Scan all `.project` files in the monorepo and:
1. Generate unified `project-manifest.json`
2. Update README.md tables (prototypes, ideas, counts)
3. Ensure proto-014 (project portfolio) has latest data

## Instructions

Run the manifest generator script:

```bash
node tools/generate-manifest.js
```

This will:
- Scan `prototypes/` and `ideas/` for `.project` files
- Generate `/project-manifest.json` with all metadata
- Update README.md prototypes table (lines ~21-38)
- Update README.md ideas table (lines ~40-49)
- Update counts and last update date

## Output Format

The manifest includes:
- Total counts (prototypes, ideas, projects)
- Full `.project` data for each prototype/idea
- Enriched metadata (_location, _path, _last_commit)
- ISO timestamp of generation

## Usage

This command is automatically triggered by pre-commit hooks when `.project` files are modified. You can also run it manually anytime.
