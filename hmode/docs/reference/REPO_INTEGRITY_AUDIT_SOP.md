# Repo Integrity Audit SOP

## Run
```bash
python3 shared/scripts/repo-integrity-audit.py --manifest
```

## Checks

| Category | Validates |
|----------|-----------|
| Prototypes | `.project` file, `README.md`, `upstream/` pattern for submodules |
| Ideas | `active/`, `archived/`, `rejected/` subdirs exist |
| Submodules | Paths exist, prototype submodules use `upstream/` |
| Cruft | No unexpected files in repo root |

## Fixes

**Missing .project:**
```yaml
# prototypes/proto-NAME/.project
id: proto-NAME-xxxxx-NNN
name: Name
type: prototype
status: active
phase: 8
description: Brief
created: YYYY-MM-DD
```

**Submodule migration:**
```bash
git submodule deinit -f prototypes/proto-NAME
git rm -f prototypes/proto-NAME
mkdir -p prototypes/proto-NAME
git submodule add URL prototypes/proto-NAME/upstream
```

**Missing ideas dirs:**
```bash
mkdir -p project-management/ideas/{archived,rejected}
```

## Output
- Console: Stats, issues, warnings
- `PROJECT_MANIFEST.json`: Full inventory

## Exit Codes
- `0` = clean
- `1` = issues found
