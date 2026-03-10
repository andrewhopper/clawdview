---
name: diagram
description: Generate architecture diagrams (system, class/ERD, sequence) for any project
version: 1.0.0
triggers:
  - "make a diagram"
  - "make diagrams"
  - "generate diagram"
  - "create diagram"
  - "architecture diagram"
  - "diagram for"
---

# Diagram Generator Skill

**Generate beautiful, interlinked architecture diagrams for any project.**

## Execution Flow

1. **Detect project** → resolve path from context or argument
2. **Analyze codebase** → parse TypeScript types, API routes, components
3. **Generate diagrams** → system, class/ERD, sequence as standalone HTML
4. **Update README** → add diagram section with links
5. **Publish (optional)** → upload to S3 with presigned URLs

## Usage

```bash
# Via slash command
/diagram
/diagram projects/personal/active/goodhue-hawkins-boats-001

# Natural language (auto-detected)
"Make a diagram for this project"
"Generate diagrams for the boat website"
"Create architecture diagrams"
```

## Implementation

### Step 1: Resolve Project Path

```python
from pathlib import Path

# If argument provided, use it
# Otherwise check current directory for .project file
# Extract metadata: id, name, folder, git_hash

project_path = Path(argument or ".").resolve()
```

### Step 2: Run Diagram Generator

```bash
python /home/user/protoflow/hmode/shared/tools/diagram-generator/run_generator.py "$PROJECT_PATH"
```

Or via Python:

```python
import sys
sys.path.insert(0, '/home/user/protoflow/hmode/shared/tools/diagram-generator')
from run_generator import generate_diagrams, update_readme

result = generate_diagrams(project_path)
update_readme(project_path, result)
```

### Step 3: Display Results

```
Diagrams generated successfully!

Files created:
  artifacts/diagrams/index.html
  artifacts/diagrams/system-{hash}-{date}.html
  artifacts/diagrams/class-{hash}-{date}.html
  artifacts/diagrams/sequence-{hash}-{date}.html

Stats:
  Types found: {N}
  Endpoints found: {N}
  Components found: {N}

README.md updated with diagram section.
```

### Step 4: Prompt for S3 Publishing

```
Publish to S3? [1] Yes (get presigned URLs) [2] No
```

If user selects [1], publish to S3 using the s3_publish.py script:

```bash
# Upload each diagram file
S3_SCRIPT="/home/user/protoflow/projects/unspecified/active/tool-s3-publish-cli-vayfd-023/s3_publish.py"
OUTPUT_DIR="$PROJECT_PATH/artifacts/diagrams"
PREFIX="diagrams/${PROJECT_ID}/$(date +%Y%m%d)"

for file in "$OUTPUT_DIR"/*.html; do
    python3 "$S3_SCRIPT" "$file" --prefix "$PREFIX" --temp 7d --yes
done
```

Or via Python (integrations module):

```python
from integrations import publish_to_s3

urls = publish_to_s3(result, expiry_days=7)

# Display URLs
print("Presigned URLs (valid 7 days):")
for name, url in urls.items():
    print(f"  {name}: {url}")
```

## Output Files

| File | Description |
|------|-------------|
| `artifacts/diagrams/index.html` | Navigation hub with links to all diagrams |
| `artifacts/diagrams/system-{hash}-{date}.html` | System architecture with layers |
| `artifacts/diagrams/class-{hash}-{date}.html` | Class/ERD diagram from TypeScript types |
| `artifacts/diagrams/sequence-{hash}-{date}.html` | API endpoints and flows |

## Metadata Embedded

Each diagram includes:
- **Project ID** - extracted from folder name
- **Project Name** - from `.project` file
- **Git Hash** - 8-char commit hash at generation time
- **Generation Date** - YYYY-MM-DD format

## Diagram Features

| Feature | Description |
|---------|-------------|
| Standalone HTML | No external dependencies |
| Mobile Responsive | Touch-friendly, pan/zoom |
| Interlinked | Navigation between diagrams |
| Modern Aesthetic | Light, airy, Figma/Miro style |

## Dependencies

- `hmode/shared/tools/diagram-generator/` - Core generation tool
- `shared/storage/s3_provider.py` - S3 publishing (optional)

## What Gets Parsed

### TypeScript Types (→ Class/ERD)
- `src/types/**/*.ts`
- `src/db/schema.ts`
- `src/models/**/*.ts`

### API Routes (→ Sequence)
- `src/app/api/**/route.ts` (Next.js App Router)
- `src/pages/api/**/*.ts` (Next.js Pages Router)

### Components (→ System)
- `src/app/**/page.tsx` → Presentation layer
- `src/components/**/*.tsx` → Presentation layer
- `src/app/api/**/route.ts` → Application layer
- `src/lib/**/*.ts` → Application layer
- `src/db/**/*.ts` → Data layer

## Error Handling

| Error | Action |
|-------|--------|
| No .project file | Use folder name as project ID |
| No TypeScript types | Show empty class diagram |
| No API routes | Show empty sequence diagram |
| S3 credentials missing | Skip publishing, show local paths |

## Example Output

```
Generating diagrams for: /path/to/project

Stats:
  Types found: 5
  Endpoints found: 5
  Components found: 25

Files created:
  artifacts/diagrams/index.html
  artifacts/diagrams/system-2804d7b8-20251203.html
  artifacts/diagrams/class-2804d7b8-20251203.html
  artifacts/diagrams/sequence-2804d7b8-20251203.html

README.md updated!

Publish to S3? [1] Yes [2] No
> 1

Publishing to protoflow-public...
Presigned URLs (7 days):
  index.html: https://...
  system-2804d7b8-20251203.html: https://...
  class-2804d7b8-20251203.html: https://...
  sequence-2804d7b8-20251203.html: https://...
```
