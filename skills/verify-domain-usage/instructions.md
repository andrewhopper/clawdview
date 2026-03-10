# Verify Domain Usage Skill

**Agent Name:** Domain Usage Verifier
**File UUID:** 2a8f4d1c-6e3b-4f2a-9c5d-7b1e8f3a6c4d

## Overview
Scans projects for usage of shared domain models from `hmode/hmode/shared/semantic/domains/`. Identifies projects that properly reuse shared domains versus those defining their own local models.

## Purpose
- **Track compliance** with domain model reuse standards
- **Identify opportunities** to refactor local models into shared domains
- **Report statistics** on domain adoption across the monorepo

## How It Works

### Scanning Logic
1. **Python Projects:** Detects `from shared.semantic.domains.{domain} import` statements and local `class X(BaseModel)` definitions
2. **TypeScript Projects:** Detects `import ... from 'hmode/hmode/shared/semantic/domains/{domain}'` and local `interface`/`type` definitions
3. **Compliance Score:** `shared_imports / (shared_imports + local_models)`

### Output
- **Available domains:** List of all domains in `hmode/hmode/shared/semantic/domains/`
- **Project statistics:** Total projects, projects using shared, projects with local-only models
- **Per-project details:** Compliance score, shared domains used, local models defined

## Usage

### Scan All Projects
```bash
/verify-domain-usage
```

### Scan Specific Category
```bash
/verify-domain-usage --category personal
/verify-domain-usage --category work
```

### Generate JSON Report
```bash
/verify-domain-usage --format json --output domain-report.json
```

## Interpreting Results

### Compliance Score
- **100%** = Only uses shared domains (ideal)
- **50%** = Mixed usage (opportunity to refactor)
- **0%** = All local models (needs attention)

### Red Flags
- Projects with many local models that overlap with existing shared domains
- Low compliance scores in Phase 8+ projects
- TypeScript projects that should import from shared but don't

## Example Output
```
Available Shared Domains: 130
  auth, email, product, order, user-research, ...

Projects Scanned: 42
  Using Shared Domains: 15
  Local Models Only: 27

Project: projects/personal/proto-001-starbucks-online-ordering
  Compliance Score: 0.0%
  Shared Domains Used: 0 []
  Local TypeScript Models: 24
    - MenuItem in src/types/index.ts
    - Modifier in src/types/index.ts
    ...
```

## When to Use
- **Monthly audits** to track domain adoption
- **Before Phase 8** to identify reusable models
- **After creating domains** to verify usage
- **Refactoring planning** to find opportunities

## Related Tools
- `/domain-search` - Search for existing domains before creating new ones
- `/domain-create` - Create new shared domain models
- Domain Modeling Specialist Agent - For domain discovery and creation
