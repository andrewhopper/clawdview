# Enforceable Rules Catalog
<!-- File UUID: 6e9a8f4d-7c5b-4a3e-9f2d-8b6a9c5f4d8e -->

## Overview

Comprehensive catalog of deterministic rules that can be enforced through hooks and gates.

**Rule Types:**
1. **Pre-commit hooks** - Run before git commit
2. **Phase gates** - Run before advancing to next SDLC phase
3. **Pre-deploy gates** - Run before deployment
4. **Runtime gates** - Run during execution
5. **Periodic audits** - Run on schedule

---

## 1.0 CODE QUALITY GATES

### 1.1 Linting & Formatting

**Rule:** Code must pass linting and formatting checks before commit

**Implementation:**
```bash
# .claude/hooks/pre-commit/lint-check.sh
#!/bin/bash

# Check Python files
if git diff --cached --name-only | grep -q '\.py$'; then
    ruff check . || exit 1
    black --check . || exit 1
fi

# Check TypeScript files
if git diff --cached --name-only | grep -q '\.(ts|tsx)$'; then
    npm run lint || exit 1
    npm run format:check || exit 1
fi
```

**Violation Response:**
```
❌ Linting failed

Files with issues:
- src/models/cart.py: Line 45 - Unused import
- src/components/Button.tsx: Line 12 - Missing semicolon

Run fixes:
[1] ruff check --fix .
[2] npm run lint:fix
[3] Skip (not recommended)
```

**Phase Gate:** Phase 7 (Test) - All code must be linted before tests

---

### 1.2 Complexity Limits

**Rule:** Functions/methods cannot exceed cyclomatic complexity threshold

**Implementation:**
```python
# hmode/shared/tools/complexity_checker.py
import radon.complexity as radon_complexity

MAX_COMPLEXITY = 10

def check_complexity(file_path: str) -> list[str]:
    """Check if file exceeds complexity threshold."""
    violations = []

    with open(file_path) as f:
        code = f.read()

    results = radon_complexity.cc_visit(code)

    for result in results:
        if result.complexity > MAX_COMPLEXITY:
            violations.append(
                f"{file_path}:{result.lineno} - "
                f"Function '{result.name}' complexity {result.complexity} "
                f"(max {MAX_COMPLEXITY})"
            )

    return violations
```

**Violation Response:**
```
❌ Complexity threshold exceeded

src/services/checkout.py:145 - Function 'process_payment' complexity 15 (max 10)

Refactoring required:
[1] Extract helper functions
[2] Use early returns
[3] Simplify conditional logic

Cannot proceed to Phase 8 until resolved.
```

**Phase Gate:** Phase 7 → Phase 8 transition

---

### 1.3 Dead Code Detection

**Rule:** No unused imports, variables, or functions

**Implementation:**
```bash
# Pre-commit hook
vulture . --min-confidence 80 || exit 1
```

**Violation Response:**
```
❌ Dead code detected

Unused imports:
- src/models/cart.py:5 - 'datetime' imported but unused

Unused functions:
- src/utils/helpers.py:34 - 'format_price' defined but never used

Action:
[1] Remove unused code
[2] Mark as intentional with # noqa comment
```

---

## 2.0 SECURITY GATES

### 2.1 Secrets Detection

**Rule:** No secrets, API keys, passwords, or credentials in code

**Implementation:**
```bash
# .claude/hooks/pre-commit/secrets-check.sh
#!/bin/bash

# Use gitleaks or trufflehog
gitleaks protect --staged || exit 1
```

**Violation Response:**
```
❌ Secrets detected in code

src/config.py:12 - AWS Access Key detected
  AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"

CRITICAL: Secrets must NEVER be committed.

Required actions:
1. Remove secret from code
2. Add to .env.example as placeholder
3. Use environment variables
4. If already committed: Rotate credentials immediately

Cannot commit until resolved.
```

**Phase Gate:** Every commit (pre-commit hook)

---

### 2.2 Dependency Vulnerabilities

**Rule:** No dependencies with known high/critical vulnerabilities

**Implementation:**
```bash
# Pre-deploy gate
npm audit --audit-level=high || exit 1
pip-audit --strict || exit 1
```

**Violation Response:**
```
❌ Vulnerable dependencies detected

High severity:
- lodash@4.17.15 - Prototype Pollution (CVE-2020-8203)
- pillow@8.0.0 - Arbitrary Code Execution (CVE-2021-23437)

Actions:
[1] Update: npm update lodash@latest
[2] Update: pip install --upgrade pillow
[3] Review: Check for breaking changes

Cannot deploy until vulnerabilities patched.
```

**Phase Gate:** Phase 8 → Phase 9 (before deployment)

---

### 2.3 License Compliance

**Rule:** No dependencies with incompatible licenses

**Implementation:**
```python
# hmode/shared/tools/license_checker.py
PROHIBITED_LICENSES = ['AGPL', 'GPL-3.0', 'SSPL']
ALLOWED_LICENSES = ['MIT', 'Apache-2.0', 'BSD-3-Clause', 'ISC']

def check_licenses(project_root: Path) -> list[str]:
    """Check for prohibited licenses in dependencies."""
    violations = []

    # Check npm packages
    result = subprocess.run(['npm', 'list', '--json'], capture_output=True)
    packages = json.loads(result.stdout)

    for pkg, info in packages.get('dependencies', {}).items():
        license = info.get('license')
        if license in PROHIBITED_LICENSES:
            violations.append(f"{pkg} - {license} license not allowed")

    return violations
```

**Violation Response:**
```
❌ License violations detected

mysql-connector@8.0.0 - GPL-3.0 license not allowed

Company policy: Only permissive licenses allowed
Prohibited: AGPL, GPL-3.0, SSPL

Options:
[1] Find alternative package with MIT/Apache license
[2] Request legal exception
[3] Implement feature without this dependency

Cannot deploy until resolved.
```

---

## 3.0 TESTING GATES

### 3.1 Test Coverage Threshold

**Rule:** Minimum test coverage percentage required

**Implementation:**
```bash
# Phase 7 gate
pytest --cov=src --cov-fail-under=80 || exit 1
```

**Violation Response:**
```
❌ Test coverage below threshold

Current: 65%
Required: 80%

Files below threshold:
- src/models/cart.py: 45% (35% short)
- src/services/payment.py: 60% (20% short)

Add tests for:
[1] Cart.add_item() - No tests
[2] Cart.calculate_total() - Edge cases missing
[3] Payment.process() - Error handling untested

Cannot advance to Phase 8 until coverage >= 80%.
```

**Phase Gate:** Phase 7 → Phase 8 transition

---

### 3.2 Required Test Types

**Rule:** Must have unit, integration, and E2E tests for production projects

**Implementation:**
```python
# hmode/shared/tools/test_type_checker.py
def check_test_types(project_root: Path, project_type: str) -> list[str]:
    """Verify required test types exist."""
    violations = []

    if project_type == 'production':
        required_tests = ['unit', 'integration', 'e2e']

        for test_type in required_tests:
            test_dir = project_root / 'tests' / test_type
            if not test_dir.exists() or not list(test_dir.glob('test_*.py')):
                violations.append(f"Missing {test_type} tests")

    return violations
```

**Violation Response:**
```
❌ Missing required test types

Production project requires:
✅ Unit tests - Found (45 tests)
✅ Integration tests - Found (12 tests)
❌ E2E tests - NOT FOUND

E2E tests required for:
- User authentication flow
- Checkout process
- Payment processing

Add E2E tests before Phase 9.
```

**Phase Gate:** Phase 8 → Phase 9 (production only)

---

### 3.3 Test Performance

**Rule:** Tests must complete within time limit

**Implementation:**
```bash
# Phase 7 gate
timeout 5m pytest || exit 1
```

**Violation Response:**
```
❌ Test suite timeout

Test suite exceeded 5 minute limit.

Slow tests:
- test_large_data_import: 3m 45s
- test_full_checkout_flow: 2m 30s

Optimization required:
[1] Mock slow external calls
[2] Use test fixtures instead of full setup
[3] Parallelize tests with pytest-xdist

Cannot advance until tests complete < 5m.
```

---

## 4.0 DOCUMENTATION GATES

### 4.1 README Exists

**Rule:** Every project must have README.md with required sections

**Implementation:**
```python
# hmode/shared/tools/readme_checker.py
REQUIRED_SECTIONS = [
    '## Overview',
    '## Installation',
    '## Usage',
    '## Development',
]

def check_readme(project_root: Path) -> list[str]:
    """Check README completeness."""
    readme = project_root / 'README.md'

    if not readme.exists():
        return ['README.md does not exist']

    content = readme.read_text()
    missing = [s for s in REQUIRED_SECTIONS if s not in content]

    return [f"Missing section: {s}" for s in missing]
```

**Violation Response:**
```
❌ README incomplete

Missing required sections:
- ## Installation
- ## Development

Add these sections before Phase 9.

Template: shared/templates/README.md
```

**Phase Gate:** Phase 8 → Phase 9

---

### 4.2 API Documentation

**Rule:** All public APIs must have docstrings/JSDoc

**Implementation:**
```python
# hmode/shared/tools/docstring_checker.py
import ast

def check_docstrings(file_path: Path) -> list[str]:
    """Check all public functions have docstrings."""
    violations = []

    with open(file_path) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith('_'):  # Public function
                if not ast.get_docstring(node):
                    violations.append(
                        f"{file_path}:{node.lineno} - "
                        f"Function '{node.name}' missing docstring"
                    )

    return violations
```

**Violation Response:**
```
❌ Missing API documentation

src/models/cart.py:45 - Function 'add_item' missing docstring
src/models/cart.py:67 - Function 'remove_item' missing docstring

Required docstring format:
"""
Brief description.

Args:
    param: Description

Returns:
    Description
"""

Cannot advance to Phase 9 until documented.
```

---

### 4.3 Changelog Updates

**Rule:** CHANGELOG.md must be updated for version changes

**Implementation:**
```bash
# Pre-deploy hook
if git diff HEAD~1 package.json | grep -q '"version"'; then
    if ! git diff HEAD~1 CHANGELOG.md | grep -q "^+##"; then
        echo "❌ Version changed but CHANGELOG.md not updated"
        exit 1
    fi
fi
```

**Violation Response:**
```
❌ CHANGELOG not updated

Version changed: 1.2.0 → 1.3.0
But CHANGELOG.md has no new entry.

Add entry:
## [1.3.0] - 2026-02-02

### Added
- Feature description

### Fixed
- Bug description

Cannot deploy without changelog entry.
```

---

## 5.0 PERFORMANCE GATES

### 5.1 Bundle Size Limits

**Rule:** Frontend bundle size cannot exceed limit

**Implementation:**
```bash
# Pre-deploy gate
npm run build
BUNDLE_SIZE=$(du -sm dist | cut -f1)

if [ $BUNDLE_SIZE -gt 5 ]; then
    echo "❌ Bundle size ${BUNDLE_SIZE}MB exceeds 5MB limit"
    exit 1
fi
```

**Violation Response:**
```
❌ Bundle size exceeds limit

Current: 7.2 MB
Limit: 5.0 MB
Overage: 2.2 MB

Largest chunks:
- vendor.js: 3.5 MB
- main.js: 2.1 MB
- icons.js: 1.6 MB

Optimization steps:
[1] Enable code splitting
[2] Lazy load icons
[3] Tree-shake unused dependencies
[4] Use dynamic imports

Cannot deploy until bundle < 5MB.
```

**Phase Gate:** Pre-deployment

---

### 5.2 Database Query Performance

**Rule:** No N+1 queries, queries must use indexes

**Implementation:**
```python
# hmode/shared/tools/query_analyzer.py
def analyze_queries(test_run_queries: list[str]) -> list[str]:
    """Detect performance issues in queries."""
    violations = []

    # Check for N+1 queries
    query_counts = {}
    for query in test_run_queries:
        normalized = re.sub(r'\d+', 'N', query)
        query_counts[normalized] = query_counts.get(normalized, 0) + 1

    for query, count in query_counts.items():
        if count > 10:
            violations.append(f"Potential N+1: {query} executed {count} times")

    # Check for missing indexes
    for query in test_run_queries:
        if 'WHERE' in query and 'USING INDEX' not in query:
            violations.append(f"Missing index: {query}")

    return violations
```

**Violation Response:**
```
❌ Query performance issues

N+1 query detected:
SELECT * FROM line_items WHERE cart_id = N
Executed 47 times in test_checkout_flow

Missing indexes:
SELECT * FROM users WHERE email = 'user@example.com'

Fixes required:
[1] Add prefetch: Cart.objects.prefetch_related('line_items')
[2] Add index: CREATE INDEX idx_users_email ON users(email)

Cannot deploy until fixed.
```

---

## 6.0 ARCHITECTURE GATES

### 6.1 Circular Dependency Detection

**Rule:** No circular dependencies between modules

**Implementation:**
```python
# hmode/shared/tools/circular_dependency_checker.py
import networkx as nx

def check_circular_dependencies(project_root: Path) -> list[str]:
    """Detect circular import chains."""
    graph = nx.DiGraph()

    # Build dependency graph from imports
    for py_file in project_root.rglob('*.py'):
        imports = extract_imports(py_file)
        for imp in imports:
            graph.add_edge(py_file.stem, imp)

    # Find cycles
    cycles = list(nx.simple_cycles(graph))

    return [f"Circular dependency: {' → '.join(cycle)}" for cycle in cycles]
```

**Violation Response:**
```
❌ Circular dependencies detected

models.cart → services.payment → models.cart

This creates import order issues and tight coupling.

Refactoring options:
[1] Extract shared interface/protocol
[2] Use dependency injection
[3] Move shared code to separate module

Cannot advance to Phase 8 until resolved.
```

**Phase Gate:** Phase 7 → Phase 8

---

### 6.2 Layer Violation Detection

**Rule:** Strict layered architecture (presentation → application → domain → infrastructure)

**Implementation:**
```python
# hmode/shared/tools/layer_checker.py
LAYER_ORDER = ['presentation', 'application', 'domain', 'infrastructure']

def check_layer_violations(project_root: Path) -> list[str]:
    """Ensure layers only depend on lower layers."""
    violations = []

    for py_file in project_root.rglob('*.py'):
        layer = get_layer_from_path(py_file)
        imports = extract_imports(py_file)

        for imp in imports:
            import_layer = get_layer_from_module(imp)

            if LAYER_ORDER.index(layer) > LAYER_ORDER.index(import_layer):
                violations.append(
                    f"{py_file}: {layer} layer importing from {import_layer} layer"
                )

    return violations
```

**Violation Response:**
```
❌ Architecture layer violations

src/domain/models/cart.py: domain layer importing from application layer
  from application.services.payment import PaymentService

Layers must follow strict order:
  presentation → application → domain → infrastructure

Domain layer CANNOT depend on application layer.

Refactor:
[1] Move PaymentService interface to domain
[2] Implement in application layer
[3] Use dependency injection

Cannot advance to Phase 8.
```

---

### 6.3 Dependency Direction Enforcement

**Rule:** Core domain has zero external dependencies

**Implementation:**
```python
# hmode/shared/tools/domain_dependency_checker.py
PROHIBITED_IN_DOMAIN = [
    'requests', 'boto3', 'sqlalchemy', 'fastapi', 'flask'
]

def check_domain_dependencies(project_root: Path) -> list[str]:
    """Ensure domain layer is pure (no external deps)."""
    violations = []

    domain_dir = project_root / 'src' / 'domain'

    for py_file in domain_dir.rglob('*.py'):
        imports = extract_imports(py_file)

        for imp in imports:
            if imp in PROHIBITED_IN_DOMAIN:
                violations.append(
                    f"{py_file}: Domain importing external library '{imp}'"
                )

    return violations
```

**Violation Response:**
```
❌ Domain layer has external dependencies

src/domain/models/user.py: Importing 'sqlalchemy'

Domain layer must be pure business logic.
No external libraries (databases, HTTP, etc.)

Use ports/adapters pattern:
[1] Define interface in domain
[2] Implement adapter in infrastructure
[3] Inject at runtime

Cannot advance to Phase 8.
```

---

## 7.0 DATA QUALITY GATES

### 7.1 Schema Validation

**Rule:** All data must match domain model schema

**Implementation:**
```python
# hmode/shared/tools/schema_validator.py
from pydantic import ValidationError

def validate_against_domain(data: dict, domain: str) -> list[str]:
    """Validate data against domain model schema."""
    violations = []

    schema_path = Path(f'hmode/hmode/shared/semantic/domains/{domain}/schema.yaml')
    schema = yaml.safe_load(schema_path.read_text())

    # Generate Pydantic model from schema
    model = generate_pydantic_model(schema)

    try:
        model(**data)
    except ValidationError as e:
        for error in e.errors():
            violations.append(f"{error['loc']}: {error['msg']}")

    return violations
```

**Violation Response:**
```
❌ Data validation failed

Cart data does not match shopping-cart domain schema:

Field 'cartId': Expected UUID, got string
Field 'createdAt': Missing required field
Field 'items[0].quantity': Expected positive integer, got 0

Fix data or update domain schema.
Cannot save invalid data.
```

**Runtime Gate:** Before persisting data

---

### 7.2 Migration Reversibility

**Rule:** All database migrations must be reversible

**Implementation:**
```python
# hmode/shared/tools/migration_checker.py
def check_migration_reversibility(migration_file: Path) -> list[str]:
    """Ensure migration has both upgrade and downgrade."""
    violations = []

    content = migration_file.read_text()

    if 'def upgrade(' not in content:
        violations.append("Missing upgrade() function")

    if 'def downgrade(' not in content:
        violations.append("Missing downgrade() function")

    # Check if downgrade is just 'pass'
    if 'def downgrade():\n    pass' in content:
        violations.append("downgrade() is empty - not reversible")

    return violations
```

**Violation Response:**
```
❌ Migration not reversible

migrations/002_add_cart_table.py: Missing downgrade() function

All migrations must be reversible.

Add downgrade:
def downgrade():
    op.drop_table('carts')

Cannot commit migration without downgrade path.
```

**Phase Gate:** Pre-commit (for migration files)

---

## 8.0 DEPLOYMENT GATES

### 8.1 Smoke Test Pass

**Rule:** Deployed app must pass smoke tests

**Implementation:**
```python
# hmode/shared/tools/smoke_test.py
async def run_smoke_tests(app_url: str) -> list[str]:
    """Run post-deployment smoke tests."""
    violations = []

    # Health check
    resp = await httpx.get(f"{app_url}/health")
    if resp.status_code != 200:
        violations.append(f"Health check failed: {resp.status_code}")

    # Git hash verification
    deployed_hash = resp.json().get('git_hash')
    expected_hash = subprocess.run(['git', 'rev-parse', 'HEAD'],
                                   capture_output=True, text=True).stdout.strip()

    if deployed_hash != expected_hash:
        violations.append(
            f"Wrong version deployed: {deployed_hash} != {expected_hash}"
        )

    return violations
```

**Violation Response:**
```
❌ Smoke tests failed

1. Health check: 503 Service Unavailable
2. Wrong version deployed: abc123 (expected: def456)

Deployment issues detected.
Rolling back...

Investigate:
[1] Check application logs
[2] Verify build artifacts
[3] Check DNS propagation

Cannot mark deployment as successful.
```

**Phase Gate:** Post-deployment (Phase 9)

---

### 8.2 Zero-Downtime Validation

**Rule:** Deployment must maintain service availability

**Implementation:**
```bash
# hmode/shared/tools/zero_downtime_checker.sh
#!/bin/bash

# Monitor app during deployment
FAILURES=0
CHECKS=60

for i in $(seq 1 $CHECKS); do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" $APP_URL/health)

    if [ "$STATUS" != "200" ]; then
        FAILURES=$((FAILURES + 1))
    fi

    sleep 1
done

UPTIME=$(echo "scale=2; ($CHECKS - $FAILURES) / $CHECKS * 100" | bc)

if (( $(echo "$UPTIME < 99.9" | bc -l) )); then
    echo "❌ Uptime ${UPTIME}% below 99.9% requirement"
    exit 1
fi
```

**Violation Response:**
```
❌ Deployment caused downtime

Uptime during deployment: 94.3%
Required: 99.9%

Downtime events:
- 00:45:12 - 00:45:47 (35 seconds)
- 00:46:03 - 00:46:15 (12 seconds)

Use blue-green or rolling deployment.
Cannot proceed with this deployment strategy.
```

---

## 9.0 COST GATES

### 9.1 AWS Spend Limit

**Rule:** Deployed resources cannot exceed budget

**Implementation:**
```python
# hmode/shared/tools/cost_estimator.py
import boto3

def estimate_stack_cost(stack_name: str) -> float:
    """Estimate monthly cost of CloudFormation stack."""
    cf = boto3.client('cloudformation')

    resources = cf.list_stack_resources(StackName=stack_name)

    monthly_cost = 0.0

    for resource in resources['StackResourceSummaries']:
        resource_type = resource['ResourceType']
        monthly_cost += COST_TABLE.get(resource_type, 0)

    return monthly_cost

def check_budget(stack_name: str, budget_limit: float) -> list[str]:
    """Check if stack cost is within budget."""
    estimated_cost = estimate_stack_cost(stack_name)

    if estimated_cost > budget_limit:
        return [f"Estimated cost ${estimated_cost:.2f} exceeds budget ${budget_limit:.2f}"]

    return []
```

**Violation Response:**
```
❌ Deployment exceeds budget

Estimated monthly cost: $450.00
Budget limit: $200.00
Overage: $250.00

Cost breakdown:
- RDS db.t3.large: $180.00
- EC2 t3.xlarge: $150.00
- ALB: $45.00
- S3: $25.00

Optimization options:
[1] Use db.t3.medium ($90/mo savings)
[2] Use t3.large ($75/mo savings)
[3] Use CloudFront instead of ALB ($30/mo savings)

Cannot deploy until cost < $200/mo.
```

**Phase Gate:** Pre-deployment (Phase 9)

---

## 10.0 ACCESSIBILITY GATES

### 10.1 A11y Compliance

**Rule:** UI must pass WCAG 2.1 AA accessibility checks

**Implementation:**
```bash
# Pre-deploy gate
npm run build
npx @axe-core/cli dist --exit || exit 1
```

**Violation Response:**
```
❌ Accessibility violations detected

Critical:
- Button missing accessible name (3 instances)
- Form input missing label (5 instances)
- Color contrast ratio 3.2:1 (minimum 4.5:1)

Moderate:
- Missing skip navigation link
- Images missing alt text (2 instances)

Cannot deploy until WCAG 2.1 AA compliance achieved.

Fixes:
[1] Add aria-label to buttons
[2] Associate labels with inputs
[3] Increase contrast: #666 → #595959
```

**Phase Gate:** Phase 8 → Phase 9 (production projects)

---

## 11.0 GIT WORKFLOW GATES

### 11.1 Commit Message Format

**Rule:** Commit messages must follow conventional commits

**Implementation:**
```bash
# .claude/hooks/commit-msg
#!/bin/bash

COMMIT_MSG=$(cat "$1")

if ! echo "$COMMIT_MSG" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"; then
    echo "❌ Invalid commit message format"
    echo ""
    echo "Required format:"
    echo "  <type>(<scope>): <subject>"
    echo ""
    echo "Examples:"
    echo "  feat(cart): add item quantity validation"
    echo "  fix(auth): resolve token expiration bug"
    echo "  docs(readme): update installation instructions"
    exit 1
fi
```

**Violation Response:**
```
❌ Invalid commit message format

Current: "added cart feature"

Required format:
  <type>(<scope>): <subject>

Type: feat, fix, docs, style, refactor, test, chore
Scope: module/component name
Subject: Brief description

Examples:
  feat(cart): add item quantity validation
  fix(auth): resolve token expiration bug

Update commit message and try again.
```

---

### 11.2 Branch Naming Convention

**Rule:** Branch names must follow pattern

**Implementation:**
```bash
# .claude/hooks/pre-push
#!/bin/bash

BRANCH=$(git rev-parse --abbrev-ref HEAD)

if ! echo "$BRANCH" | grep -qE "^(feature|bugfix|hotfix|refactor)/[a-z0-9-]+$"; then
    echo "❌ Invalid branch name: $BRANCH"
    echo ""
    echo "Required format:"
    echo "  <type>/<description>"
    echo ""
    echo "Type: feature, bugfix, hotfix, refactor"
    echo "Description: lowercase-with-hyphens"
    echo ""
    echo "Examples:"
    echo "  feature/shopping-cart"
    echo "  bugfix/payment-validation"
    exit 1
fi
```

**Violation Response:**
```
❌ Invalid branch name: "cart_feature"

Required format:
  <type>/<description>

Type: feature, bugfix, hotfix, refactor
Description: lowercase-with-hyphens

Valid examples:
  feature/shopping-cart
  bugfix/payment-validation
  hotfix/security-patch

Rename branch:
  git branch -m feature/shopping-cart
```

---

## 12.0 ASSET OPTIMIZATION GATES

### 12.1 Image Optimization

**Rule:** All images must be optimized/compressed

**Implementation:**
```python
# hmode/shared/tools/image_optimizer.py
from PIL import Image

MAX_IMAGE_SIZE_KB = 500

def check_image_optimization(image_path: Path) -> list[str]:
    """Check if image is optimized."""
    violations = []

    size_kb = image_path.stat().st_size / 1024

    if size_kb > MAX_IMAGE_SIZE_KB:
        violations.append(
            f"{image_path}: {size_kb:.0f}KB exceeds {MAX_IMAGE_SIZE_KB}KB limit"
        )

    # Check if image has EXIF data (should be stripped)
    img = Image.open(image_path)
    if img.info.get('exif'):
        violations.append(f"{image_path}: Contains EXIF data (should be stripped)")

    return violations
```

**Violation Response:**
```
❌ Unoptimized images detected

public/images/hero.jpg: 2.3MB exceeds 500KB limit
public/images/product-1.png: Contains EXIF data

Optimize:
[1] Run: npx @squoosh/cli --optimize public/images/*.jpg
[2] Strip EXIF: exiftool -all= public/images/*.jpg
[3] Convert to WebP: cwebp -q 80 input.jpg -o output.webp

Cannot deploy with unoptimized images.
```

---

## 13.0 TECHNICAL DEBT GATES

### 13.1 TODO/FIXME Limit

**Rule:** Limited number of TODOs/FIXMEs allowed per phase

**Implementation:**
```python
# hmode/shared/tools/todo_counter.py
def count_todos(project_root: Path, phase: int) -> dict:
    """Count TODOs and FIXMEs in codebase."""
    todos = []
    fixmes = []

    for file in project_root.rglob('*.py'):
        content = file.read_text()

        for i, line in enumerate(content.split('\n'), 1):
            if 'TODO' in line:
                todos.append(f"{file}:{i}")
            if 'FIXME' in line:
                fixmes.append(f"{file}:{i}")

    max_todos = {7: 0, 8: 5, 9: 0}  # Phase: max allowed

    violations = []
    if len(fixmes) > 0:
        violations.append(f"{len(fixmes)} FIXMEs found (0 allowed)")

    if len(todos) > max_todos[phase]:
        violations.append(
            f"{len(todos)} TODOs found ({max_todos[phase]} allowed in Phase {phase})"
        )

    return violations
```

**Violation Response:**
```
❌ Technical debt threshold exceeded

Phase 9 (Production): 0 TODOs/FIXMEs allowed

Found:
- 3 FIXMEs
- 7 TODOs

FIXME locations:
- src/models/cart.py:45 - FIXME: Handle edge case
- src/services/payment.py:89 - FIXME: Add retry logic
- src/utils/helpers.py:23 - FIXME: Optimize performance

Resolve all FIXMEs before production deployment.
Convert TODOs to issues or remove.

Cannot advance to Phase 9.
```

**Phase Gate:** Phase 8 → Phase 9

---

## 14.0 DEPENDENCY GATES

### 14.1 Deprecated Package Detection

**Rule:** No deprecated packages in dependencies

**Implementation:**
```python
# hmode/shared/tools/deprecation_checker.py
import requests

def check_deprecated_packages(requirements_file: Path) -> list[str]:
    """Check if any dependencies are deprecated."""
    violations = []

    with open(requirements_file) as f:
        packages = [line.split('==')[0] for line in f if '==' in line]

    for package in packages:
        # Check PyPI API for deprecation
        resp = requests.get(f"https://pypi.org/pypi/{package}/json")
        if resp.status_code == 410:  # Gone
            violations.append(f"{package} is deprecated")
        elif resp.status_code == 200:
            data = resp.json()
            if data.get('info', {}).get('yanked'):
                violations.append(f"{package} has been yanked")

    return violations
```

**Violation Response:**
```
❌ Deprecated packages detected

requests-oauthlib is deprecated
Maintainer message: "Use authlib instead"

python-dateutil==2.8.0 has been yanked
Security vulnerability: CVE-2021-XXXXX

Actions:
[1] Replace: requests-oauthlib → authlib
[2] Update: python-dateutil==2.8.2

Cannot use deprecated packages in production.
```

---

## 15.0 SUMMARY TABLE

| Category | Rule | Gate Type | Phase | Severity |
|----------|------|-----------|-------|----------|
| **Code Quality** | Linting/Formatting | Pre-commit | 7 | High |
| | Complexity Limits | Phase Gate | 7→8 | High |
| | Dead Code Detection | Pre-commit | All | Medium |
| **Security** | Secrets Detection | Pre-commit | All | Critical |
| | Dependency Vulnerabilities | Pre-deploy | 8→9 | Critical |
| | License Compliance | Pre-deploy | 8→9 | High |
| **Testing** | Coverage Threshold | Phase Gate | 7→8 | High |
| | Required Test Types | Phase Gate | 8→9 | High |
| | Test Performance | Phase Gate | 7 | Medium |
| **Documentation** | README Exists | Phase Gate | 8→9 | Medium |
| | API Documentation | Phase Gate | 8→9 | High |
| | Changelog Updates | Pre-deploy | 9 | Medium |
| **Performance** | Bundle Size Limits | Pre-deploy | 9 | High |
| | Database Query Performance | Runtime | 8 | High |
| **Architecture** | Circular Dependencies | Phase Gate | 7→8 | High |
| | Layer Violations | Phase Gate | 7→8 | High |
| | Domain Dependencies | Phase Gate | 7→8 | High |
| **Data Quality** | Schema Validation | Runtime | 8 | High |
| | Migration Reversibility | Pre-commit | All | High |
| **Deployment** | Smoke Tests | Post-deploy | 9 | Critical |
| | Zero-Downtime | Post-deploy | 9 | High |
| **Cost** | AWS Spend Limit | Pre-deploy | 9 | High |
| **Accessibility** | WCAG 2.1 AA | Pre-deploy | 8→9 | High (production) |
| **Git Workflow** | Commit Message Format | Pre-commit | All | Low |
| | Branch Naming | Pre-push | All | Low |
| **Assets** | Image Optimization | Pre-deploy | 9 | Medium |
| **Tech Debt** | TODO/FIXME Limit | Phase Gate | 8→9 | Medium |
| **Dependencies** | Deprecated Packages | Pre-deploy | 8→9 | High |

---

## 16.0 IMPLEMENTATION PRIORITY

### Phase 1: Critical Gates (Security & Stability)
1. Secrets detection
2. Dependency vulnerabilities
3. Smoke tests
4. Test coverage threshold

### Phase 2: Quality Gates (Code & Architecture)
5. Linting/formatting
6. Circular dependencies
7. Layer violations
8. Complexity limits

### Phase 3: Production Readiness
9. README completeness
10. API documentation
11. License compliance
12. A11y compliance

### Phase 4: Optimization Gates
13. Bundle size limits
14. Image optimization
15. Database query performance

### Phase 5: Process Gates
16. Commit message format
17. TODO/FIXME limits
18. Changelog updates
19. Deprecated packages

---

## 17.0 NEXT STEPS

1. **Prioritize gates** - Start with Phase 1 (Critical)
2. **Implement in hmode/shared/tools/** - Create checking utilities
3. **Add to .claude/hooks/** - Install pre-commit/pre-push hooks
4. **Update sdlc_gates.py** - Add gate checking functions
5. **Test thoroughly** - Verify gates work and provide clear feedback
6. **Document exceptions** - When gates can be bypassed (with approval)
7. **Monitor effectiveness** - Track violations caught vs. missed
