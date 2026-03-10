## 🏷️ XIP TAGGING (AWS/AMAZON IP)

**Purpose:** Mark projects containing AWS/Amazon intellectual property

**XIP includes:**
- AWS internal document templates (PR/FAQs, 6-pagers, etc.)
- AWS brand guidelines, style guides, writing standards
- AWS internal system insights (reporting formats, assessment frameworks)
- AWS-specific methodologies developed internally
- AWS customer engagement templates

**NOT XIP:**
- Generic use of AWS services (Bedrock, SageMaker)
- Public AWS documentation references
- Open-source integrations with AWS

**Tagging Requirements:**
1. **Folder naming:** Add `-xip` suffix → `proto-name-xxxxx-NNN-name-xip`
2. **.project metadata:** Include `"tags": ["XIP"]` field
3. **Manifest:** XIP tag appears in project-manifest.json

**Examples:**
- ✅ `proto-012-genai-adoption-framework-xip` (AWS assessment framework)
- ✅ `proto-008-weekly-progress-report-agent-xip` (AWS reporting standards)
- ✅ `proto-021-aws-presentation-builder-xip` (AWS style templates)
- ❌ `proto-002-bedrock-joke-api` (uses Bedrock, but no internal IP)

**README.md REQUIRED:** ALL ideas and prototypes MUST have README.md with:
- Current phase and status
- Purpose/description
- Tech stack
- Timeline (started, last updated)
- Links to design docs or source code

