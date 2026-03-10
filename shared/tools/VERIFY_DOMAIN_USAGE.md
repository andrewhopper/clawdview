# Domain Model Usage Verification Tool

**File UUID:** 9c4e8b2f-1a7d-4f3e-b5c2-6d9e3a1f8b4c

## Overview
Automated tool to verify shared domain model usage across the monorepo. Scans Python and TypeScript projects to identify which use shared domains versus defining their own local models.

## Problem Statement
With 130+ shared domain models available in `shared/semantic/domains/`, many projects still define their own local models. This leads to:
- **Duplication** - Same concepts modeled multiple times
- **Inconsistency** - Different field names/types for same concepts
- **Maintenance burden** - Changes must be made in multiple places
- **Lost discoverability** - New developers don't know what's available

## Solution
Automated scanner that:
1. Identifies all available shared domains
2. Scans project codebases for domain imports and local model definitions
3. Calculates compliance scores
4. Generates actionable reports

## How It Works

### Detection Strategy

#### Python Projects
**Shared Domain Import Detection:**
```python
from shared.semantic.domains.auth import User
from shared.semantic.domains.product import Product
```

**Local Model Detection:**
```python
from pydantic import BaseModel

class LocalUser(BaseModel):  # ← Detected as local model
    name: str
```

#### TypeScript Projects
**Shared Domain Import Detection:**
```typescript
import { User } from 'shared/semantic/domains/auth'
import type { Product } from 'shared/semantic/domains/product'
```

**Local Model Detection:**
```typescript
interface LocalUser {  // ← Detected as local model
  name: string
}

type Product = {  // ← Detected as local model
  id: string
}
```

### Compliance Scoring
```
Compliance Score = shared_imports / (shared_imports + local_models)
```

**Examples:**
- **10 shared, 0 local** → 100% (ideal)
- **5 shared, 5 local** → 50% (mixed)
- **0 shared, 10 local** → 0% (needs attention)

## Usage

### Command Line

#### Scan All Projects
```bash
python3 shared/tools/verify-domain-usage.py
```

#### Scan Specific Category
```bash
python3 shared/tools/verify-domain-usage.py --category personal
python3 shared/tools/verify-domain-usage.py --category work
```

#### Generate JSON Output
```bash
python3 shared/tools/verify-domain-usage.py --format json
```

#### Save to File
```bash
python3 shared/tools/verify-domain-usage.py --output reports/domain-usage-$(date +%Y%m%d).txt
```

### Claude Code Skill
```bash
/verify-domain-usage
/verify-domain-usage --category personal
/verify-domain-usage --format json --output report.json
```

## Output Format

### Text Report
```
================================================================================
SHARED DOMAIN MODEL USAGE REPORT
================================================================================

Available Shared Domains: 130
  auth, email, product, order, inventory, ...

Projects Scanned: 42
  Using Shared Domains: 15
  Local Models Only: 27

Total Shared Domain Imports: 87
Total Local Models Defined: 312

================================================================================
PROJECTS BY COMPLIANCE SCORE
================================================================================

Project: projects/personal/proto-001-starbucks-online-ordering
  Compliance Score: 0.0%
  Shared Domains Used: 0 []
  Local Python Models: 0
  Local TypeScript Models: 24
    - MenuItem in src/types/index.ts
    - Modifier in src/types/index.ts
    - ModifierGroup in src/types/index.ts
    - ModifierOption in src/types/index.ts
    - Size in src/types/index.ts
    ... and 19 more

Project: projects/work/customer-portal-xyr8a
  Compliance Score: 75.0%
  Shared Domains Used: 3 ['auth', 'email', 'notification']
  Local Python Models: 1
    - CustomMetrics in src/analytics/metrics.py
  Local TypeScript Models: 0
```

### JSON Report
```json
{
  "total_projects": 42,
  "projects_using_shared": 15,
  "projects_with_local_only": 27,
  "total_shared_imports": 87,
  "total_local_models": 312,
  "shared_domains_available": ["auth", "email", "product", ...],
  "domain_usage": [
    {
      "project_path": "projects/personal/proto-001-starbucks-online-ordering",
      "project_name": "proto-001-starbucks-online-ordering",
      "shared_domains_used": [],
      "local_pydantic_models": [],
      "local_typescript_models": [
        ["src/types/index.ts", "MenuItem"],
        ["src/types/index.ts", "Modifier"]
      ],
      "shared_import_count": 0,
      "local_model_count": 24,
      "compliance_score": 0.0
    }
  ]
}
```

## Interpreting Results

### High Priority (0-25% Compliance)
Projects that should use shared domains but don't. Common causes:
- **Built before domain system existed**
- **Developer unaware of available domains**
- **Models should be promoted to shared**

**Action:** Review local models. Can they be replaced with shared domains? Should they be promoted?

### Medium Priority (25-75% Compliance)
Projects with mixed usage. Often indicates:
- **Partial migration in progress**
- **Some domain-specific extensions**
- **Legacy code not yet refactored**

**Action:** Identify which local models should be shared. Create refactoring plan.

### Low Priority (75-100% Compliance)
Projects following best practices. Minimal local models are acceptable for:
- **Prototype-specific data**
- **UI state models**
- **Request/response DTOs**

**Action:** None, or promote remaining local models if reusable.

## Integration Points

### SDLC Gates
**Phase 4 (Domain Models Gate):**
- Run verification after domain model creation
- Verify new domain is imported by intended projects
- Track adoption over time

**Phase 8 (Implementation):**
- Check compliance before code review
- Ensure new code uses shared domains
- Flag local model creation for review

### Automated Checks
**Pre-commit Hook:**
```bash
# Warn if new Pydantic models created outside shared/
python3 shared/tools/verify-domain-usage.py --category personal --format json | \
  jq '.domain_usage[] | select(.local_model_count > 0)'
```

**CI/CD Pipeline:**
```yaml
- name: Domain Usage Audit
  run: |
    python3 shared/tools/verify-domain-usage.py --output reports/domain-usage.txt
    # Fail if compliance drops below threshold
```

## Maintenance Schedule

### Weekly
- Review new projects with 0% compliance
- Notify project owners of available shared domains

### Monthly
- Generate full compliance report
- Identify trends (improving vs. degrading)
- Plan domain promotion/refactoring sprints

### Quarterly
- Audit shared domains for usage
- Archive unused domains
- Promote commonly duplicated local models to shared

## Related Tools

### Domain Discovery
- `/domain-search` - Search registry for existing domains
- `domain-modeling-specialist` agent - Discover and create domains

### Domain Creation
- `/domain-create` - Create new shared domain with approval
- `shared/semantic/domains/registry.yaml` - Domain registry

### Code Quality
- `/software-quality-check` - Overall code quality audit
- `/guardrail-enforce` - Verify tech preferences compliance

## Limitations

### False Positives
- **Type aliases** detected as models (TypeScript)
- **Props interfaces** for React components
- **DTO/Request models** that shouldn't be shared

### False Negatives
- **Dynamic imports** not detected
- **Models in .d.ts files** may be missed
- **Re-exported models** not traced back to source

### Performance
- **Large monorepos** may take 1-2 minutes to scan
- **Binary files** safely ignored
- **node_modules/** and **venv/** skipped

## Future Enhancements

### Planned Features
- [ ] Suggest shared domains based on local model names
- [ ] Detect semantic similarity between local and shared models
- [ ] Auto-generate refactoring PRs
- [ ] Track compliance trends over time
- [ ] Integration with domain-modeling-specialist agent
- [ ] Web dashboard for visualization

### Integration Ideas
- **GitHub Actions** - Comment on PRs with compliance impact
- **Slack Notifications** - Alert on compliance drops
- **VS Code Extension** - Suggest shared domains while coding
- **LLM Integration** - Ask "What shared domains are similar to this model?"

## Examples

### Example 1: Starbucks Ordering Prototype
**Finding:** 24 local TypeScript models, 0% compliance

**Analysis:**
- Models: MenuItem, Modifier, ModifierGroup, Size, CartItem, Order
- Opportunity: `food-beverage` and `order` domains exist in shared
- Action: Refactor to use shared domains or promote if prototype-specific

**Refactoring:**
```typescript
// Before
interface MenuItem {
  id: string
  name: string
  price: number
}

// After
import { Product } from 'shared/semantic/domains/product'
import { Money } from 'shared/semantic/domains/core'

type MenuItem = Product & {
  price: Money
}
```

### Example 2: Customer Portal
**Finding:** 3 shared domains used, 1 local model, 75% compliance

**Analysis:**
- Shared: auth, email, notification (good!)
- Local: CustomMetrics (analytics-specific)
- Action: Consider if metrics should be promoted to observability domain

### Example 3: Internal Tool
**Finding:** 0 shared domains, 5 local models, 0% compliance

**Analysis:**
- All models are API response DTOs
- Not reusable across projects
- Action: No change needed - DTOs are acceptable

## Support
- **Documentation:** `.claude/skills/verify-domain-usage/instructions.md`
- **Issues:** Report bugs via GitHub issues
- **Questions:** Ask in #domain-modeling Slack channel
