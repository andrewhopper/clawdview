# Tech Stack Presets

**Pre-configured technology preferences for common use cases**

---

## Overview

Presets are pre-configured `.tech-preferences.local.json` files that default all technology choices to a specific pattern (AWS-only, preferred defaults, etc.). Copy a preset to your project root to quickly configure your tech stack.

## Available Presets

### 1. AWS-Centric (`aws-centric.json`)

**Use when:** Building AWS-native applications that should use AWS services by default.

**Defaults to:**
- **UI**: AWS Cloudscape
- **ASR**: AWS Transcribe
- **TTS**: AWS Polly
- **OCR**: AWS Textract + Comprehend
- **LLM**: AWS Bedrock (Claude)
- **Embeddings**: AWS Bedrock (Titan)
- **Database**: DynamoDB
- **Storage**: S3
- **Email**: SES
- **Auth**: Cognito
- **Deployment**: Amplify (frontend), Lambda (backend)
- **Monitoring**: CloudWatch
- **CI/CD**: CodePipeline + CodeBuild
- **Caching**: ElastiCache
- **Search**: OpenSearch
- **Queues**: SQS + Lambda
- **Workflows**: Step Functions
- **IaC**: AWS CDK
- **ETL**: AWS Glue
- **Data Warehouse**: Redshift
- **Data Lake**: S3 + Lake Formation

**Example:**
```bash
cp shared/tech-preferences/presets/aws-centric.json .tech-preferences.local.json
```

### 2. Preferred Defaults (`preferred-defaults.json`)

**Use when:** You want to explicitly document using all Rank 1 (default) choices.

**Defaults to:**
- **UI**: shadcn/ui
- **Frontend**: Next.js 15 (React 19)
- **Styling**: Tailwind CSS
- **Collaboration**: Yjs
- **Backend**: Next.js API Routes
- **Database**: PostgreSQL
- **ORM**: Drizzle
- **ASR**: Deepgram
- **TTS**: ElevenLabs
- **OCR**: Claude Vision
- **LLM**: AWS Bedrock (Claude)
- **LLM Framework**: BAML
- **Embeddings**: AWS Bedrock (Titan)
- **Vector DB**: pgvector
- **E2E Tests**: Playwright
- **Unit Tests**: Vitest
- **Deployment**: AWS Amplify (frontend), Lambda (backend)
- **Monitoring**: Sentry
- **CI/CD**: GitHub Actions
- **Auth**: Clerk
- **Email**: Resend
- **Payments**: Stripe
- **Storage**: AWS S3
- **Analytics**: PostHog
- **Caching**: Upstash Redis
- **Search**: Algolia
- **Queues**: Inngest
- **Workflows**: Temporal
- **IaC**: AWS CDK
- **ETL**: dbt
- **Data Warehouse**: Redshift
- **Data Lake**: S3 + Lake Formation
- **Charts**: Recharts
- **Diagrams**: Mermaid
- **API Docs**: OpenAPI/Swagger
- **Docs Platform**: Astro Starlight
- **Internal Wiki**: Notion
- **Static Site**: Astro

**Example:**
```bash
cp shared/tech-preferences/presets/preferred-defaults.json .tech-preferences.local.json
```

**Note:** Generally not needed since Rank 1 is already the default. Useful for:
- Documentation purposes
- Overriding a parent project's overrides
- Explicitly stating "we use the standard stack"

---

## Usage

### Quick Start

1. **Copy preset to project root:**
   ```bash
   cp shared/tech-preferences/presets/aws-centric.json .tech-preferences.local.json
   ```

2. **Verify it works:**
   ```bash
   /fetch-examples "Transcribe"
   # Output should show AWS Transcribe with [PROJECT OVERRIDE] badge
   ```

3. **Customize if needed:**
   Edit `.tech-preferences.local.json` to adjust specific categories.

### Creating Custom Presets

Create a new preset file based on existing ones:

```bash
cp shared/tech-preferences/presets/aws-centric.json shared/tech-preferences/presets/my-preset.json
```

Edit `my-preset.json`:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "My Custom Preset",
  "description": "Description of when to use this preset",
  "presetName": "my-custom-preset",
  "overrides": {
    "frontend_frameworks": {
      "preferences": [{
        "rank": 1,
        "name": "Vite + React",
        "version": "6.x",
        ...
      }]
    }
  }
}
```

### Combining Presets with Custom Overrides

Start with a preset, then add custom overrides:

```bash
# Copy AWS preset
cp shared/tech-preferences/presets/aws-centric.json .tech-preferences.local.json

# Edit to override specific categories
# For example, use shadcn/ui instead of Cloudscape for UI
```

Edit `.tech-preferences.local.json`:
```json
{
  "presetName": "aws-centric-with-shadcn",
  "overrides": {
    "ui_component_libraries": {
      "preferences": [{
        "rank": 1,
        "name": "shadcn/ui",
        ...
      }]
    },
    ... rest of AWS overrides ...
  }
}
```

---

## Preset Patterns

### When to Use AWS-Centric

✅ **Use when:**
- Building AWS-native applications
- Enterprise compliance requirements
- Maximizing AWS ecosystem integration
- Cost optimization through AWS unified billing
- VPC isolation requirements

❌ **Avoid when:**
- Multi-cloud requirements
- Need best-in-class tools regardless of provider
- Cost-sensitive prototypes (some AWS services more expensive)
- Team lacks AWS expertise

### When to Use Preferred Defaults

✅ **Use when:**
- Starting a new prototype with no specific requirements
- Want to follow "golden path" recommendations
- Building a reference implementation
- Training/teaching purposes
- Need to explicitly document "we use defaults"

❌ **Avoid when:**
- Have specific tech requirements
- AWS-only environment
- Cost-sensitive (some rank 1 choices are premium)

---

## Preset Schema

All presets follow this structure:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Preset Name",
  "description": "When to use this preset",
  "version": "1.0.0",
  "lastUpdated": "2025-11-12",
  "presetName": "preset-identifier",
  "note": "Additional notes about this preset",
  "overrides": {
    "category_name": {
      "preferences": [
        {
          "rank": 1,
          "name": "Technology Name",
          "version": "1.x",
          "rationale": "Why this technology",
          "useCases": ["use case 1", "use case 2"],
          "docsUrl": "https://...",
          "examplesUrl": "https://..."
        }
      ]
    }
  }
}
```

---

## Tips

1. **Start with a preset** - Faster than manual configuration
2. **Customize as needed** - Presets are starting points, not constraints
3. **Document your choice** - Add `"note"` field explaining why you used this preset
4. **Version control** - Commit `.tech-preferences.local.json` if team should share config
5. **Gitignore** - Keep `.tech-preferences.local.json` gitignored for personal overrides

---

## Related Documentation

- **[tech-preferences/README.md](../README.md)** - Overview of preferences system
- **[TECH_STACK_PREFERENCES.md](../../TECH_STACK_PREFERENCES.md)** - Human-readable preferences
- **[DEVELOPMENT_STANDARDS.md](../../DEVELOPMENT_STANDARDS.md)** - Implementation standards

---

**Last Updated:** 2025-11-12
**Maintained By:** Andrew Hopper
