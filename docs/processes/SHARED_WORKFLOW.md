# SHARED WORKFLOW

Comprehensive workflow for managing shared elements: domain models, utilities, helper functions, and process tools.

## 1.0 OVERVIEW

**Purpose:** Standardize creation, management, and evolution of shared resources across the monorepo.

**Scope:**
- Domain models (semantic layer)
- Utilities and helper functions
- Process tools and automation
- Code standards and patterns
- Templates and boilerplate

**Principles:**
1. **Reuse First:** Check existing before creating new
2. **Approval Gates:** Human approval for schema changes
3. **Semantic Consistency:** Use canonical domain models
4. **Progressive Enhancement:** Start simple, evolve as needed
5. **Documentation Driven:** Document before implementing

---

## 2.0 DOMAIN MODEL WORKFLOW

### 2.1 Discovery Phase

**ALWAYS check existing domains first:**

```bash
# Step 1: Check registry
cat hmode/hmode/shared/semantic/domains/registry.yaml

# Step 2: Search for similar domains
grep -r "YourEntity" hmode/hmode/shared/semantic/domains/

# Step 3: Check archived domains
ls hmode/hmode/shared/semantic/domains/_archive/
```

### 2.2 Reuse Workflow

**When domain exists:**

```typescript
// Import from canonical location
import { Email, Thread } from '@semantic/domains/email/generated/typescript';
import { Meeting } from '@semantic/domains/meeting/generated/typescript';

// Extend for prototype-specific needs
interface ExtendedEmail extends Email {
  customField?: string;
  prototypeSpecific: boolean;
}
```

### 2.3 Creation Workflow

**When new domain needed:**

#### 2.3.1 Generate Proposal

```yaml
# Location: shared/domain-models/{domain-name}/models.yaml
# Status: PENDING APPROVAL

entities:
  YourEntity:
    description: "Clear business description"
    properties:
      id:
        type: uuid
        required: true
      name:
        type: string
        required: true
        max_length: 255
      created_at:
        type: datetime
        required: true
        auto: true
      updated_at:
        type: datetime
        required: true
        auto: true
```

#### 2.3.2 Present for Approval

```markdown
## 📊 Domain Model Proposal: {Domain Name}

**Status:** PENDING APPROVAL
**Location:** shared/domain-models/{domain-name}/

### Entities (3)
1. **User** - Application user account
2. **Order** - Customer purchase order
3. **Product** - Catalog product

### Enums (2)
1. **OrderStatus** - pending, confirmed, shipped, delivered
2. **ProductCategory** - electronics, clothing, food

### Relationships
- User → Order (1:many)
- Order → Product (many:many via OrderItem)

**Approve? [Y/n/m]**
```

#### 2.3.3 After Approval

```bash
# Step 1: Add to registry
vi hmode/hmode/shared/semantic/domains/registry.yaml

# Step 2: Create domain directory
mkdir -p hmode/hmode/shared/semantic/domains/{domain-name}/

# Step 3: Copy approved models
cp shared/domain-models/{domain-name}/*.yaml \
   hmode/hmode/shared/semantic/domains/{domain-name}/

# Step 4: Generate types
cd hmode/shared/tools/domain-generator/
./generate.sh {domain-name}
```

### 2.4 Evolution Workflow

**When modifying existing domain:**

```yaml
# Location: hmode/hmode/shared/semantic/domains/{domain}/changes/v2.0.0.yaml
version: "2.0.0"
changes:
  - type: add_field
    entity: User
    field: preferences
    schema:
      type: jsonb
      required: false
  - type: add_enum_value
    enum: OrderStatus
    value: cancelled
```

**Approval Required:** Present changes → Get approval → Apply migration

---

## 3.0 UTILITIES WORKFLOW

### 3.1 Discovery

```bash
# Search existing utilities
find shared/ -name "*.ts" -o -name "*.py" | xargs grep -l "export function"

# Check tools directory
ls -la hmode/shared/tools/

# Check scripts directory
ls -la shared/scripts/
```

### 3.2 Classification

| Type | Location | Criteria | Example |
|------|----------|----------|---------|
| **Tool** | `hmode/shared/tools/` | Standalone, CLI, reusable | semantic-run |
| **Utility** | `shared/utils/` | Library function, imported | formatDate() |
| **Script** | `shared/scripts/` | Ad-hoc, one-off | migrate-v1-v2.sh |
| **Service** | `shared/services/` | API wrapper, client | S3Service |
| **Helper** | Prototype-specific | Not reusable yet | local helper |

### 3.3 Creation Workflow

#### 3.3.1 Utility Function

```typescript
// Location: shared/utils/{category}/{name}.ts
// Example: shared/utils/formatting/currency.ts

/**
 * Format number as currency
 * @example formatCurrency(1234.56) // "$1,234.56"
 */
export function formatCurrency(
  amount: number,
  currency: string = 'USD'
): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency
  }).format(amount);
}

// Always export from index
// shared/utils/formatting/index.ts
export * from './currency';
```

#### 3.3.2 CLI Tool

```python
# Location: hmode/shared/tools/{tool-name}/
# Structure:
hmode/shared/tools/my-tool/
├── README.md           # Usage documentation
├── pyproject.toml      # Python dependencies
├── src/
│   └── my_tool.py      # Main implementation
├── bin/
│   └── run            # Executable wrapper
└── tests/
    └── test_my_tool.py
```

#### 3.3.3 Service Module

```typescript
// Location: shared/services/{service}/
// Example: shared/services/aws/s3.ts

export class S3Service {
  private client: S3Client;

  constructor(config: S3Config) {
    this.client = new S3Client(config);
  }

  async upload(file: File): Promise<string> {
    // Implementation
  }
}
```

### 3.4 Promotion Workflow

**From prototype to shared:**

```bash
# Step 1: Identify reusable code
grep -r "TODO: make shared" prototypes/

# Step 2: Extract and generalize
cp prototypes/proto-xyz/src/utils/helper.ts \
   shared/utils/category/helper.ts

# Step 3: Add tests
vi shared/utils/category/helper.test.ts

# Step 4: Update imports in prototype
# Change: import { helper } from './utils/helper';
# To:     import { helper } from '@shared/utils/category';
```

---

## 4.0 PROCESS TOOLS WORKFLOW

### 4.1 Tool Categories

| Category | Purpose | Location | Examples |
|----------|---------|----------|----------|
| **Generators** | Code generation | `hmode/shared/tools/` | domain-generator |
| **Analyzers** | Code analysis | `hmode/shared/tools/` | proposal-scorer |
| **Exporters** | Data export | `hmode/shared/tools/` | claude-exporter |
| **Runners** | Execution | `hmode/shared/tools/` | semantic-run |
| **Validators** | Quality checks | `hmode/shared/tools/` | uat-validator |

### 4.2 Tool Creation Workflow

#### 4.2.1 Tool Scaffold

```bash
# Create tool structure
mkdir -p hmode/shared/tools/{tool-name}/{src,bin,tests,docs}

# Create executable
cat > hmode/shared/tools/{tool-name}/bin/run << 'EOF'
#!/usr/bin/env bash
cd "$(dirname "$0")/.."
python3 src/main.py "$@"
EOF
chmod +x hmode/shared/tools/{tool-name}/bin/run
```

#### 4.2.2 Tool Interface

```python
# hmode/shared/tools/{tool-name}/src/main.py
import argparse
from typing import Any, Dict

def main() -> int:
    """Tool entry point."""
    parser = argparse.ArgumentParser(
        description="Tool description"
    )
    parser.add_argument(
        'input',
        help='Input file or directory'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'yaml', 'text'],
        default='json'
    )

    args = parser.parse_args()
    result = process(args)
    output(result, args.format)
    return 0

if __name__ == "__main__":
    exit(main())
```

#### 4.2.3 Tool Documentation

```markdown
# Tool Name

## Purpose
Brief description of what the tool does

## Installation
\`\`\`bash
cd hmode/shared/tools/{tool-name}
pip install -r requirements.txt
\`\`\`

## Usage
\`\`\`bash
./bin/run input.yaml --format json
\`\`\`

## Options
- `--format`: Output format (json|yaml|text)
- `--verbose`: Verbose output

## Examples
\`\`\`bash
# Example 1: Basic usage
./bin/run data.yaml

# Example 2: With options
./bin/run data.yaml --format text --verbose
\`\`\`
```

---

## 5.0 CODE STANDARDS WORKFLOW

### 5.1 Discovery

```bash
# Check existing standards
ls hmode/shared/standards/code/

# Read manifest
cat hmode/shared/standards/code/manifest.json

# Find patterns for your tech stack
ls hmode/shared/standards/code/{technology}/
```

### 5.2 Usage Workflow

**Before generating code:**

```typescript
// Step 1: Load relevant standard
const reactStandard = await read('hmode/shared/standards/code/react/component.tsx');

// Step 2: Follow patterns
// Use naming conventions, structure, patterns from standard

// Step 3: Cite standard in comments
/**
 * Component follows hmode/shared/standards/code/react/component.tsx
 * Pattern: Functional component with hooks
 */
```

### 5.3 Contribution Workflow

**Adding new standard:**

```bash
# Step 1: Create directory
mkdir -p hmode/shared/standards/code/{technology}/

# Step 2: Add pattern files
vi hmode/shared/standards/code/{technology}/pattern.{ext}

# Step 3: Add examples
vi hmode/shared/standards/code/{technology}/examples.md

# Step 4: Update manifest
vi hmode/shared/standards/code/manifest.json
```

---

## 6.0 TEMPLATE WORKFLOW

### 6.1 Template Types

| Type | Purpose | Location |
|------|---------|----------|
| **Project** | Full prototype scaffold | `shared/templates/project/` |
| **Component** | UI component boilerplate | `shared/templates/component/` |
| **Service** | Backend service scaffold | `shared/templates/service/` |
| **Test** | Test suite boilerplate | `shared/templates/test/` |

### 6.2 Using Templates

```bash
# Copy template
cp -r shared/templates/project/vite-react \
      prototypes/proto-new-xyz/

# Customize
cd prototypes/proto-new-xyz/
./customize.sh --name "New Prototype" --port 3001
```

### 6.3 Creating Templates

```bash
# Step 1: Create from successful prototype
cp -r prototypes/proto-successful/ \
      shared/templates/project/new-template/

# Step 2: Generalize (remove specific logic)
# - Replace hardcoded values with placeholders
# - Remove prototype-specific code
# - Add customization script

# Step 3: Document
vi shared/templates/project/new-template/README.md
```

---

## 7.0 APPROVAL GATES

### 7.1 Required Approvals

| Change Type | Approval Required | Format |
|-------------|------------------|---------|
| New domain model | Yes | YAML presentation |
| Modify domain model | Yes | Change proposal |
| New shared utility | No* | Code review |
| New tool | No* | Documentation |
| New standard | Yes | RFC format |
| New template | No* | Example usage |

*Recommended but not required

### 7.2 Approval Format

```yaml
# APPROVAL REQUEST: {Type}
# Date: {Date}
# Requester: {Name}

type: domain_model | standard | architecture
action: create | modify | deprecate
severity: minor | major | breaking

proposal:
  summary: "One line description"
  rationale: "Why this change is needed"
  impact: "What will be affected"

changes:
  - description: "Specific change 1"
  - description: "Specific change 2"

alternatives:
  - option: "Alternative approach"
    tradeoff: "Pros/cons"

# APPROVE? [Y/n/m]
```

---

## 8.0 MIGRATION WORKFLOW

### 8.1 Promoting to Shared

```bash
# Step 1: Identify candidate
# Look for: Used in 3+ prototypes, stable API, documented

# Step 2: Extract
cp -r prototypes/proto-x/src/utils/candidate \
      shared/utils/

# Step 3: Generalize
# Remove prototype-specific code
# Add configuration options
# Improve error handling

# Step 4: Test
cd shared/utils/candidate/
npm test

# Step 5: Update imports in prototypes
# Update all prototypes to use shared version
```

### 8.2 Deprecation Workflow

```typescript
// Step 1: Mark as deprecated
/**
 * @deprecated Use @shared/utils/new-thing instead
 * Will be removed in v2.0.0
 */
export function oldThing() {}

// Step 2: Log usage
export function oldThing() {
  console.warn('Deprecated: Use newThing instead');
  return newThing();
}

// Step 3: Archive after migration
mv shared/utils/old-thing \
   shared/utils/_archive/
```

---

## 9.0 TESTING REQUIREMENTS

### 9.1 Shared Code Testing

**Required for shared code:**
- Unit tests for all public functions
- Integration tests for tools
- Type tests for TypeScript
- Documentation tests (examples must work)

```typescript
// shared/utils/category/thing.test.ts
describe('thing', () => {
  it('should handle basic case', () => {
    expect(thing('input')).toBe('output');
  });

  it('should handle edge cases', () => {
    expect(thing(null)).toBe(defaultValue);
  });
});
```

### 9.2 Tool Testing

```python
# hmode/shared/tools/{tool}/tests/test_main.py
def test_basic_usage():
    """Test basic tool functionality."""
    result = run_tool(['input.yaml'])
    assert result.exit_code == 0
    assert 'expected' in result.output
```

---

## 10.0 DOCUMENTATION STANDARDS

### 10.1 Required Documentation

| Element | Documentation Required |
|---------|----------------------|
| Domain Model | Business description, relationships |
| Utility Function | JSDoc/docstring, examples |
| Tool | README, usage, examples |
| Service | API docs, configuration |
| Template | Customization guide |

### 10.2 Documentation Format

```typescript
/**
 * Brief description (one line)
 *
 * Detailed description (if needed)
 *
 * @example
 * // Example usage
 * const result = myFunction('input');
 * console.log(result); // 'output'
 *
 * @param input - Parameter description
 * @returns Return value description
 * @throws {ErrorType} When this error occurs
 *
 * @see {@link RelatedFunction}
 * @since 1.0.0
 */
```

---

## 11.0 VERSIONING

### 11.1 Version Strategy

```yaml
# hmode/hmode/shared/semantic/domains/{domain}/version.yaml
current: "1.2.0"
history:
  - version: "1.2.0"
    date: "2024-11-25"
    changes: ["Added preferences field"]
  - version: "1.1.0"
    date: "2024-11-20"
    changes: ["Added status enum"]
  - version: "1.0.0"
    date: "2024-11-15"
    changes: ["Initial release"]
```

### 11.2 Breaking Changes

**Process for breaking changes:**
1. Deprecation notice (min 2 weeks)
2. Migration guide
3. Automated migration script (if possible)
4. Version bump (major)
5. Archive old version

---

## 12.0 QUICK REFERENCE

### 12.1 Directory Map

```
shared/
├── semantic/domains/        # Domain models (canonical)
├── domain-models/          # Domain proposals (pending)
├── utils/                  # Utility functions
├── tools/                  # CLI tools
├── scripts/                # Ad-hoc scripts
├── services/               # Service wrappers
├── standards/              # Code standards
├── templates/              # Project templates
└── _archive/               # Deprecated items
```

### 12.2 Import Paths

```typescript
// Domain models
import { Email } from '@semantic/domains/email/generated/typescript';

// Utilities
import { formatCurrency } from '@shared/utils/formatting';

// Services
import { S3Service } from '@shared/services/aws';

// Standards (for reference, not import)
// See: hmode/shared/standards/code/react/
```

### 12.3 Common Commands

```bash
# Find reusable code
grep -r "TODO: make shared" prototypes/

# Check domain registry
cat hmode/hmode/shared/semantic/domains/registry.yaml

# Run domain generator
cd hmode/shared/tools/domain-generator && ./generate.sh

# Test shared utility
cd shared/utils/{category} && npm test

# Check code standards
ls hmode/shared/standards/code/
```

---

## 13.0 CHECKLIST

### 13.1 Before Creating Shared Element

- [ ] Checked if already exists
- [ ] Used in 2+ prototypes (or will be)
- [ ] Stable API/interface
- [ ] Clear purpose and scope
- [ ] Documentation ready

### 13.2 After Creating Shared Element

- [ ] Added tests
- [ ] Added documentation
- [ ] Updated relevant imports
- [ ] Added to appropriate index
- [ ] Committed to repository

---

## 14.0 ENFORCEMENT

**AI Assistant Rules:**
1. ALWAYS check existing before creating new
2. ALWAYS present domain models in YAML for approval
3. ALWAYS use canonical import paths
4. NEVER modify domain models without approval
5. ALWAYS add tests for shared code

**Human Rules:**
1. Review and approve domain model changes
2. Decide on architectural patterns
3. Approve breaking changes
4. Set versioning strategy

---

**Last Updated:** 2024-11-25
**Version:** 1.0.0
**Status:** Active
**Owner:** Platform Team