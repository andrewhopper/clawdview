# Project Verification Checklist

A comprehensive checklist for verifying that projects in the Protoflow monorepo meet all quality, consistency, and compliance standards.

**Rules Source:** `shared/semantic/domains/verification/`
- Schema: `schema.yaml` (entity definitions, enums, actions)
- Data: `rules.yaml` (rule instances)

---

## 1.0 QUICK VERIFICATION

Use this section for rapid project audits. Rules defined in `shared/semantic/domains/verification/`.

```
┌──────────────────────────────────────────────────────────────────────┐
│  🔴 CRITICAL (Must Pass)                                             │
├──────────────────────────────────────────────────────────────────────┤
│  [ ] ERR-001/002/003 Error tracker implemented                       │
│  [ ] THM-001 No raw hex colors (use design tokens)                   │
│  [ ] STR-001 .project file exists with valid metadata                │
│  [ ] QUA-001 Type safety enforced (TypeScript strict)                │
│  [ ] QUA-004 No hardcoded secrets or credentials                     │
│  [ ] QUA-005/006 HTTPS and WSS only                                  │
├──────────────────────────────────────────────────────────────────────┤
│  🟡 IMPORTANT (Should Pass)                                          │
├──────────────────────────────────────────────────────────────────────┤
│  [ ] THM-002/003 Night Sky theme applied (if UI project)             │
│  [ ] STR-002 README.md with setup instructions                       │
│  [ ] STR-003 Makefile with standard targets                          │
│  [ ] TST-001/002 Tests exist and pass                                │
│  [ ] QUA-007 Domain models have timestamps                           │
├──────────────────────────────────────────────────────────────────────┤
│  🔵 RECOMMENDED (Nice to Have)                                       │
├──────────────────────────────────────────────────────────────────────┤
│  [ ] PRF-001/002 Performance optimized                               │
│  [ ] DOC-001/002/003 Documentation complete                          │
│  [ ] DEP-001/002 Deployment targets configured                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2.0 RULES DATA MODEL

Rules are defined in `verification-rules.yaml` for use by:
- **frontgate**: Pre-commit/PR validation
- **overwatch**: Real-time file watching
- **manual**: Human checklist verification

### 2.1 Rule Structure

```yaml
- id: "XXX-NNN"           # Unique identifier (category prefix + number)
  name: "Human Name"       # Display name
  category: "category_id"  # Links to categories section
  severity: critical|important|recommended
  description: "What this rule checks"
  applies_to:              # Tech stack filters
    - "react"
    - "python"
    - "all"
  check:                   # Validation logic
    type: file_exists|grep|grep_absent|json_field|yaml_field|...
    pattern: "regex or path"
    paths: ["glob patterns"]
  fix: |                   # Remediation guidance
    How to fix if rule fails
```

### 2.2 Check Types

| Type | Description | Parameters |
|------|-------------|------------|
| `file_exists` | File/pattern exists | `patterns: []` |
| `dir_exists` | Directory exists | `patterns: []` |
| `grep` | Pattern found in files | `pattern`, `paths`, `min_matches` |
| `grep_absent` | Pattern NOT found | `pattern`, `paths`, `exclude` |
| `json_field` | JSON field matches | `file`, `field`, `value` |
| `yaml_field` | YAML field matches | `file`, `field`, `pattern` |
| `yaml_fields` | Multiple fields exist | `file`, `fields: []` |
| `file_contains` | File contains patterns | `file`, `patterns: []` |
| `conditional` | If-then check | `condition`, `then` |

---

## 3.0 ERROR TRACKING

**Rules:** ERR-001, ERR-002, ERR-003, ERR-004

### 3.1 Implementation Patterns

**React Error Boundary (ERR-001):**
```tsx
// src/components/ErrorBoundary.tsx
export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

**Python Global Handler (ERR-002):**
```python
import sys
import logging

def setup_error_tracking():
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception
```

**Node.js Global Handler (ERR-003):**
```typescript
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});
```

---

## 4.0 THEME & DESIGN SYSTEM

**Rules:** THM-001, THM-002, THM-003, THM-004, THM-005

**Theme Reference:** https://asset-distribution-bucket-1762910336.s3.us-east-1.amazonaws.com/previews/night-sky-theme.html

### 4.1 Required CSS Variables

```css
:root {
  --background: 228 25% 7%;        /* Deep navy */
  --foreground: 220 15% 90%;       /* Light text */
  --primary: 220 50% 50%;          /* Blue */
  --accent: 192 45% 52%;           /* Cyan */
  --destructive: 0 50% 50%;        /* Red/Error */
  --success: 160 45% 42%;          /* Teal */
  --warning: 38 55% 52%;           /* Amber */
  --border: 230 18% 20%;
  --ring: 220 50% 50%;
  --radius: 0.5rem;
}
```

### 4.2 Token Validation

```css
/* ✅ CORRECT */
background-color: hsl(var(--background));
color: hsl(var(--foreground));

/* ❌ INCORRECT */
background-color: #1a1a2e;
color: #e0e0e0;
```

---

## 5.0 PROJECT STRUCTURE

**Rules:** STR-001, STR-002, STR-003, STR-004, STR-005, STR-006

### 5.1 Required Files

| File | Rule | Purpose |
|------|------|---------|
| `.project` | STR-001 | Project metadata |
| `README.md` | STR-002 | Documentation |
| `Makefile` | STR-003 | Build targets |
| `.env.example` | STR-004 | Env template |

### 5.2 .project Required Fields

```yaml
uuid: "abc12"              # STR-005
name: "Project Name"
phase: 8
status: active
description: "Brief description"
created_at: "2025-12-16"   # STR-006
updated_at: "2025-12-16"   # STR-006
```

---

## 6.0 CODE QUALITY

**Rules:** QUA-001 through QUA-007

| Rule | Check |
|------|-------|
| QUA-001 | TypeScript strict mode enabled |
| QUA-002 | No `any` types |
| QUA-003 | Python type hints used |
| QUA-004 | No hardcoded secrets |
| QUA-005 | HTTPS only (no http://) |
| QUA-006 | WSS only (no ws://) |
| QUA-007 | Models have created_at/updated_at |

---

## 7.0 TESTING

**Rules:** TST-001, TST-002, TST-003

| Rule | Check |
|------|-------|
| TST-001 | Tests directory exists |
| TST-002 | Test files exist |
| TST-003 | Test script in package.json |

---

## 8.0 DOCUMENTATION

**Rules:** DOC-001, DOC-002, DOC-003

| Rule | Check |
|------|-------|
| DOC-001 | README has description |
| DOC-002 | README has setup instructions |
| DOC-003 | API documentation exists |

---

## 9.0 PERFORMANCE

**Rules:** PRF-001, PRF-002

| Rule | Check |
|------|-------|
| PRF-001 | Async script loading |
| PRF-002 | Image optimization |

---

## 10.0 DEPLOYMENT

**Rules:** DEP-001, DEP-002

| Rule | Check |
|------|-------|
| DEP-001 | `infra-bootstrap` target exists |
| DEP-002 | `infra-deploy` target exists |

---

## 11.0 VALIDATION

### 11.1 Automated Validation

```bash
# Run all rules (future frontgate/overwatch integration)
python3 shared/tools/verify-project.py .

# Check specific category
python3 shared/tools/verify-project.py . --category=theme

# Check specific severity
python3 shared/tools/verify-project.py . --severity=critical
```

### 11.2 Quick Manual Check

```bash
# Structure checks
[ -f ".project" ] && echo "✓ STR-001" || echo "✗ STR-001"
[ -f "README.md" ] && echo "✓ STR-002" || echo "✗ STR-002"
[ -f "Makefile" ] && echo "✓ STR-003" || echo "✗ STR-003"

# Theme check (THM-001)
grep -rE "#[0-9a-fA-F]{6}" src/ --include="*.css" && echo "✗ THM-001" || echo "✓ THM-001"

# Security check (QUA-004)
grep -r "AKIA" . --include="*.ts" && echo "✗ QUA-004" || echo "✓ QUA-004"
```

---

## 12.0 SCORING

Defined in `verification-rules.yaml` under `scoring:`.

| Grade | Score | Description |
|-------|-------|-------------|
| **A** | 90-100% | Production ready |
| **B** | 75-89% | Minor improvements needed |
| **C** | 60-74% | Significant gaps |
| **D** | 40-59% | Major issues |
| **F** | < 40% | Incomplete |

### Category Weights

| Category | Weight |
|----------|--------|
| Error Tracking | 15% |
| Theme/Design System | 20% |
| Project Structure | 15% |
| Code Quality | 20% |
| Testing | 15% |
| Documentation | 10% |
| Performance | 5% |

---

## APPENDIX: Related Files

| File | Purpose |
|------|---------|
| `shared/semantic/domains/verification/` | Domain model (schema + rules) |
| `shared/design-system/MANAGEMENT_GUIDELINES.md` | Design system docs |
| `.claude/commands/website-qa-checklist.md` | Website QA |
| `shared/standards/code/` | Code standards by tech |

---

**Version:** 2.0.0
**Created:** 2025-12-16
**Last Updated:** 2025-12-16
