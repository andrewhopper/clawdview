# Brownfield Project Standards

Templates and standards for maintaining legacy/brownfield codebases.

## Contents

| File | Purpose |
|------|---------|
| `Makefile.template` | Standard Makefile with required targets |
| `example.env.template` | Environment configuration template |
| `gitignore.template` | Comprehensive .gitignore for secrets |
| `README.template.md` | README structure for brownfield projects |

## Quick Start

```bash
# Copy templates to your project
cp Makefile.template /path/to/project/Makefile
cp example.env.template /path/to/project/example.env
cp gitignore.template /path/to/project/.gitignore

# Run brownfield audit
/brownfield-audit /path/to/project
```

## Required Setup Targets

Every brownfield project MUST have these Makefile targets:

| Target | Command | Purpose |
|--------|---------|---------|
| `setup` | `make setup` | One-command project setup |
| `run` | `make run` | Start the application |
| `test` | `make test` | Run test suite |
| `lint` | `make lint` | Run linters |
| `clean` | `make clean` | Remove artifacts |
| `build` | `make build` | Production build |

## Checklist

See `.claude/docs/reference/BROWNFIELD_CHECKLIST.md` for the full audit checklist.

## Related

- `/brownfield-audit` - Slash command to audit projects
- `shared/standards/code/` - Language-specific standards
