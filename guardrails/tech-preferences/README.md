# Tech Stack Preferences

**Rank-ordered technology preferences organized by category**

---

## Overview

This directory contains technology preferences split into logical category groups. Each file contains rank-ordered alternatives with canonical documentation URLs and examples.

## File Structure

```
tech-preferences/
├── index.json                 # Index of all category files
├── frontend.json              # Frontend frameworks, UI libs, styling (3 categories)
├── backend.json               # Backend frameworks, databases, ORMs (3 categories)
├── ai-ml.json                 # AI/ML services: ASR, TTS, OCR, LLMs, etc. (7 categories)
├── testing.json               # E2E and unit testing frameworks (2 categories)
├── infrastructure.json        # Deployment, monitoring, CI/CD, caching (8 categories)
├── services.json              # Auth, email, payments, storage, analytics (5 categories)
├── data-viz.json              # Data visualization and diagramming (2 categories)
└── api-docs.json              # API documentation tools (1 category)
```

## JSON Schema

Each preference entry includes:

```json
{
  "rank": 1,
  "name": "Technology Name",
  "version": "1.0.0",
  "rationale": "Why this technology is preferred",
  "useCases": ["use case 1", "use case 2"],
  "docsUrl": "https://example.com/docs",
  "examplesUrl": "https://example.com/examples",
  "approvedOn": "2025-11-16T10:30:00Z",
  "approvedByName": "Your Name",
  "approvedByEmail": "your-email@example.com",
  "approvedInCommit": "abc123def456"
}
```

### Required Fields
- `rank`: Numeric ranking (1 = highest preference)
- `name`: Technology name
- `version`: Version or API designation
- `rationale`: Why this technology is preferred
- `useCases`: Array of use case descriptions

### Optional Fields
- `docsUrl`: Official documentation URL
- `examplesUrl`: Examples/quickstart URL
- `approvedOn`: ISO 8601 timestamp of approval
- `approvedByName`: Full name of person who approved
- `approvedByEmail`: Email of person who approved
- `approvedInCommit`: Git commit SHA where approved

## Usage

### Reading Preferences

**Load index:**
```bash
cat shared/tech-preferences/index.json
```

**Load specific category:**
```bash
cat shared/tech-preferences/frontend.json
cat shared/tech-preferences/ai-ml.json
```

### Using with Slash Commands

Fetch examples for a specific technology:
```bash
/fetch-examples "Next.js"
/fetch-examples "Deepgram"
/fetch-examples "D3.js"
```

## Category Groups

### 1. Frontend (frontend.json)
- Frontend frameworks (Next.js, Vite, Expo)
- UI component libraries (shadcn/ui, Radix, Chakra, Cloudscape, MUI)
- Styling (Tailwind CSS, CSS Modules, vanilla-extract)

### 2. Backend (backend.json)
- Backend frameworks (Next.js API Routes, Fastify, FastAPI)
- Databases (PostgreSQL, SQLite, DynamoDB)
- ORMs & query builders (Drizzle, Prisma, SQLAlchemy)

### 3. AI/ML (ai-ml.json)
- ASR/Speech Recognition (Deepgram, Whisper, AWS Transcribe)
- TTS/Text-to-Speech (ElevenLabs, OpenAI TTS, AWS Polly)
- OCR/Document Intelligence (AWS Textract, Claude vision, Mistral OCR)
- LLM Inference (AWS Bedrock Claude, Anthropic API, OpenAI)
- Image Generation (Bedrock SD, DALL-E 3, self-hosted SD)
- Vector Embeddings (Titan, OpenAI, Cohere, Sentence Transformers)
- Vector Databases (pgvector, Pinecone, Weaviate)

### 4. Testing (testing.json)
- E2E testing (Playwright, Cypress, Selenium)
- Unit testing (Vitest, Jest, pytest)

### 5. Infrastructure (infrastructure.json)
- Frontend deployment (AWS Amplify, Vercel, Cloudflare Pages)
- Backend deployment (Lambda + API Gateway, ECS Fargate, Fly.io)
- Monitoring (Sentry, CloudWatch, Datadog)
- CI/CD (GitHub Actions, AWS CodePipeline, GitLab CI)
- Caching (Upstash Redis, ElastiCache, Cloudflare KV)
- Search (Algolia, Meilisearch, AWS OpenSearch)
- Task queues (Inngest, SQS + Lambda, BullMQ)
- Workflow orchestration (Temporal, Step Functions, n8n)

### 6. Services (services.json)
- Authentication (Clerk, AWS Cognito, Auth.js)
- Email sending (Resend, AWS SES, Postmark)
- Email templating (React Email)
- Payments (Stripe, Lemon Squeezy, Paddle)
- Storage (AWS S3, Cloudflare R2, UploadThing)
- Analytics (PostHog, Plausible, Mixpanel)

### 7. Data Visualization (data-viz.json)
- Data visualization (Recharts, D3.js, Chart.js, Apache ECharts)
- Diagramming (Mermaid, ReactFlow, Excalidraw)

### 8. API Documentation (api-docs.json)
- API documentation (OpenAPI/Swagger, Scalar, Postman Collections)

## Programmatic Access

### Python Example

```python
import json

# Load index
with open('shared/tech-preferences/index.json') as f:
    index = json.load(f)

# Load frontend preferences
with open('shared/tech-preferences/frontend.json') as f:
    frontend = json.load(f)

# Get Next.js documentation URL
for pref in frontend['categories']['frontend_frameworks']['preferences']:
    if pref['name'] == 'Next.js':
        print(f"Docs: {pref['docsUrl']}")
        print(f"Examples: {pref['examplesUrl']}")
```

### JavaScript/TypeScript Example

```typescript
import { readFileSync } from 'fs'
import { join } from 'path'

// Load AI/ML preferences
const aiMlPath = join(__dirname, 'shared/tech-preferences/ai-ml.json')
const aiMl = JSON.parse(readFileSync(aiMlPath, 'utf-8'))

// Get all ASR options with documentation
const asrOptions = aiMl.categories.asr_speech_recognition.preferences
asrOptions.forEach(tech => {
  console.log(`${tech.name}: ${tech.docsUrl}`)
})
```

## Project-Level Overrides

Projects can override global tech preferences with a local `.tech-preferences.local.json` file.

### Use Cases

- Prototypes requiring different tech stacks
- Client-specific requirements
- Experimental technologies
- Developer customizations (gitignored by default)

### Creating Overrides

**Copy example file:**
```bash
cp shared/tech-preferences/.tech-preferences.local.json.example .tech-preferences.local.json
```

**Edit to override technologies:**
```json
{
  "overrides": {
    "frontend_frameworks": {
      "preferences": [{
        "rank": 1,
        "name": "Vite",
        "version": "6.x",
        "rationale": "This project uses Vite for faster builds",
        "useCases": ["SPA", "rapid prototyping"],
        "docsUrl": "https://vitejs.dev/guide/",
        "examplesUrl": "https://github.com/vitejs/vite"
      }]
    }
  }
}
```

### Override Behavior

- **Overrides**: Replace entire category preferences
- **Additions**: Add new categories not in global preferences
- **Automatic**: `/fetch-examples` detects and uses local overrides
- **Gitignored**: `.tech-preferences.local.json` ignored by default

### Example Output

```bash
cd prototypes/proto-042-vite-app/
/fetch-examples "Vite"
# Output: ## Vite (Rank 1) [PROJECT OVERRIDE]
```

---

## Maintenance

### Adding New Technologies

1. **Propose technology:** Present options with rationale, trade-offs
2. **Human approval:** Get explicit approval before adding to preferences
3. **Add preference entry:**
   - Find appropriate category file (e.g., `frontend.json` for UI libraries)
   - Add all required fields (rank, name, version, rationale, useCases)
   - Add approval metadata:
     - `approvedOn`: Current ISO timestamp
     - `approvedByName`: Approver's full name
     - `approvedByEmail`: Approver's email
     - `approvedInCommit`: Git commit SHA (added after commit)
4. **Update index:** If adding new category, update `index.json`
5. **Keep files under 300 lines each**

### Approval Workflow

**CRITICAL:** ALL technology additions MUST be approved by human before adding to preferences.

**Process:**
1. AI proposes technology with comprehensive details (see CLAUDE.md technical paraphrase requirements)
2. Human reviews and approves/rejects
3. AI adds to preferences with approval metadata
4. Commit includes approval reference

**Backfilling Existing Entries:**
- Existing entries without approval metadata remain valid (fields optional)
- Can backfill critical technologies by checking `git log` for first commit adding entry
- Extract: commit SHA, author name/email, commit date

### Updating Documentation URLs

Documentation URLs should be:
- Official documentation (not third-party tutorials)
- Latest stable version documentation
- Direct links to getting started or main docs page
- HTTPS only

Example URLs should be:
- Official examples repository or documentation examples section
- Starter templates or quickstart guides
- Representative of current best practices

## Related Documents

- `../TECH_STACK_PREFERENCES.md` → Human-readable markdown version
- `../DEVELOPMENT_STANDARDS.md` → Implementation standards and patterns
- `../CLAUDE.md` → SDLC process and Phase 2 (RESEARCH) requirements

---

**Last Updated:** 2025-11-16
**Maintained By:** Andrew Hopper
**Version:** 1.1.0 (Added approval tracking)
