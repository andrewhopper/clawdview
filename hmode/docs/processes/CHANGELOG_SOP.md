# Changelog SOP

Standard operating procedure for maintaining the repository changelog spreadsheet.

## Overview

The changelog tracks all commits with structured metadata for auditing, reporting, and project tracking.

**Location:** `docs/changelog.xlsx`
**Template:** `artifacts/templates/changelog-template.xlsx`

---

## 1. Spreadsheet Schema

### Sheets
| Sheet | Purpose |
|-------|---------|
| **Changelog** | Main data (date, time, hash, project, change_type, summary, author) |
| **Metadata** | Generation info (date, time, git hash, schema version) |
| **Change Types** | Reference for valid change_type values |

| Column | Description | Example |
|--------|-------------|---------|
| **date** | Commit date (YYYY-MM-DD) | 2025-11-22 |
| **time** | Commit time (HH:MM:SS) | 14:32:15 |
| **hash** | Short commit hash (7 chars) | 1615dd34 |
| **project** | Project/prototype/idea name | proto-s3-publish |
| **change_type** | Category of change | new project |
| **summary** | Brief description of change | Add S3 upload functionality |
| **artifacts** | Comma-separated list of items added | domain:ecommerce, cmd:/deploy |
| **author** | Commit author name | Andrew Hopper |

---

## 2. Change Type Classification

| Change Type | Description | Example |
|-------------|-------------|---------|
| **new project** | New prototype created | Adding proto-s3-publish |
| **new feature** | Feature added to existing project | Add export functionality |
| **bug fix** | Fix for existing functionality | Fix timeout issue |
| **new utility** | Shared utility/tool added | Add semantic resolver |
| **new domain model** | Domain model created/updated | Add ecommerce domain |
| **new idea** | Idea captured in Phase 1 | Add idea-llm-router |
| **research added** | Research/analysis documented | Add competitor analysis |

---

## 2.5 Artifact Prefixes

| Prefix | Type | Example |
|--------|------|---------|
| `domain:` | Domain model | domain:ecommerce, domain:auth |
| `cmd:` | Slash command | cmd:/deploy, cmd:/publish |
| `skill:` | Skill | skill:pdf, skill:xlsx |
| `module:` | Shared module | module:semantic-resolver |
| `hook:` | Hook | hook:pre-commit, hook:stop |
| `sop:` | SOP document | sop:changelog, sop:domain-model |
| `template:` | Template file | template:changelog |
| `mcp:` | MCP server | mcp:outlook, mcp:sentral |
| `api:` | API endpoint | api:/validate, api:/upload |

---

## 3. Project Classification

| Prefix | Location | Example |
|--------|----------|---------|
| `proto-*` | `/prototypes/` | proto-s3-publish-vayfd-023 |
| `idea-*` | `/project-management/ideas/` | idea-llm-router |
| `shared-*` | `/shared/` | shared-semantic-domains |
| `docs-*` | `/docs/` | docs-architecture |
| `core-*` | Root config/orchestration | core-claude-md |
| `merge` | Branch merges | merge |

---

## 4. Maintenance Workflow

### On Each Commit

**AI MUST:**
1. Identify affected project from changed files
2. Classify change type (minor/major)
3. Add row to `docs/changelog.xlsx`
4. Commit changelog update with main changes

### Batch Backfill

For historical commits:
```bash
git log --oneline --format="%h|%ad|%s|%an" --date=short | head -100
```

Parse and populate spreadsheet.

---

## 5. Automation Integration

### Pre-commit Hook (Optional)
```bash
# .git/hooks/pre-commit
# Validate changelog has entry for today if commits exist
```

### Report Generation
```bash
# Generate weekly summary
python3 scripts/changelog_report.py --week
```

---

## 6. Quick Reference

### Adding Entry (Python)
```python
from openpyxl import load_workbook

wb = load_workbook('docs/changelog.xlsx')
ws = wb.active
ws.append(['2025-11-22', '14:32:15', 'abc1234', 'proto-example', 'bug fix', 'Fix timeout issue', 'domain:auth, api:/login', 'Author'])
wb.save('docs/changelog.xlsx')
```

### Filtering by Project
```python
# In Excel: Data > Filter > Select project column
# In Python: df[df['project'].str.contains('proto-')]
```

---

## 7. Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Skip changelog for "small" changes | Log ALL commits |
| Use vague summaries ("updates") | Be specific ("Fix S3 upload timeout") |
| Default to "new feature" for everything | Use specific change types |
| Backfill without verification | Verify each entry against actual diff |
