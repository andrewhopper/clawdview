# Research Report Standards

**Required metadata and formatting for all research reports**

---

## Overview

All research reports generated in this repository MUST include standardized metadata for traceability, versioning, and citation purposes.

## Required: File Naming Convention

### Format

```
[topic]-[YYYY-MM-DD]-[short-uuid].[ext]
```

### Components

| Component | Description | Example |
|-----------|-------------|---------|
| `topic` | Kebab-case topic name | `communication-density` |
| `YYYY-MM-DD` | ISO date of creation | `2025-11-23` |
| `short-uuid` | First 8 characters of UUID v4 | `a1b2c3d4` |
| `ext` | File extension | `md`, `html`, `pdf` |

### Examples

```
communication-density-2025-11-23-a1b2c3d4.md
communication-density-2025-11-23-a1b2c3d4.html
vector-db-comparison-2025-11-20-f9e8d7c6.md
ai-model-benchmark-2025-11-15-12345678.pdf
```

### Benefits

1. **Sortable:** Files sort chronologically by date
2. **Unique:** UUID suffix prevents collisions
3. **Discoverable:** Topic prefix enables search
4. **Traceable:** Full UUID stored in document metadata

---

## Required: Document Metadata

### 1. Report Identifier (UUID)

Every research report MUST include a unique identifier in UUID v4 format.

**Format:** `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx` (full UUID in document)

**Placement:** In document header/frontmatter AND in filename (first 8 chars)

**Example:**
```markdown
**Report ID:** `a1b2c3d4-e5f6-4789-a012-b3456789cdef`
```

### 2. Generation Date

Every research report MUST include an ISO 8601 formatted date.

**Format:** `YYYY-MM-DD` (minimum) or `YYYY-MM-DDTHH:mm:ssZ` (preferred)

**Placement:** In document header/frontmatter AND in filename

**Example:**
```markdown
**Date:** 2025-11-23
```
or
```markdown
**Generated:** 2025-11-23T14:30:00Z
```

## Recommended Metadata

| Field | Description | Example |
|-------|-------------|---------|
| `Author` | Who/what generated the report | `Research synthesis via Claude` |
| `Version` | Report version if updated | `1.0.0` |
| `Scope` | Brief description of coverage | `Visual, written, spoken communication` |
| `Source Count` | Number of sources cited | `16 primary sources` |

## Template

### Markdown Header

```markdown
# [Report Title]

**Report ID:** `[UUID v4]`
**Date:** [YYYY-MM-DD]
**Author:** [Author/Generator]
**Scope:** [Brief description]
**Sources:** [N] primary references

---
```

### HTML Header

```html
<header>
    <h1>[Report Title]</h1>
    <p class="meta">
        Report ID: <code>[UUID v4]</code> |
        Date: [YYYY-MM-DD] |
        Sources: [N] references
    </p>
</header>
```

## Rationale

1. **Traceability:** UUIDs enable unique identification across systems
2. **Versioning:** Dates enable tracking when research was conducted
3. **Citation:** Both fields enable proper academic/business citation
4. **Audit Trail:** Supports compliance and review processes
5. **Deduplication:** Prevents confusion between similar reports

## Enforcement

- AI assistants MUST include both fields when generating research reports
- Reports missing required metadata should be flagged for update
- Existing reports may be backfilled with UUIDs as needed

## UUID Generation

### Python
```python
import uuid
report_id = str(uuid.uuid4())
```

### JavaScript/TypeScript
```typescript
const reportId = crypto.randomUUID();
```

### Command Line
```bash
uuidgen  # macOS/Linux
```

---

**Created:** 2025-11-23
**Approved By:** User request
**Version:** 1.0.0
