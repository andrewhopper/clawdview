---
version: 1.0.0
last_updated: 2025-11-16
description: Validate completeness of technical proposal against category checklists
args:
  proposal: Technical proposal text to audit (paste the paraphrase)
---

# Audit Technical Proposal

Validate a technical paraphrase/proposal against comprehensive checklists to ensure all critical details are included.

## Usage

```
/audit-proposal "Adding postgres database:
- Stack: PostgreSQL 16.1 + Prisma ORM v5.x
- Location: Local Docker (dev)
..."
```

## Audit Categories

Auto-detect category based on proposal content, then validate against category-specific checklist.

### Database Proposals

**Required fields:**
- [ ] Stack (DB engine + version, ORM + version)
- [ ] Extensions (pg_vector, PostGIS, etc. if applicable)
- [ ] Location (local/Docker/RDS/managed, environment-specific)
- [ ] Instance name (for cloud deployments)
- [ ] AWS Account/Project ID (for managed services)
- [ ] Credentials (where stored: .env, Secrets Manager, rotation policy)
- [ ] Schema (tables, key fields, relationships)
- [ ] Pooling (max connections, timeout)
- [ ] Migrations (tool, versioning)
- [ ] Backups (method, retention, frequency)
- [ ] Port + connection string location

**Scoring:**
- 11/11 required fields: ✅ Complete
- 9-10/11: ⚠️ Nearly complete (list missing)
- 7-8/11: ⚠️ Incomplete (list missing)
- <7/11: ❌ Insufficient detail

### AI/ML Integration Proposals

**Required fields:**
- [ ] Model (specific model name/ID)
- [ ] Provider + client library (Bedrock, OpenAI, Anthropic direct)
- [ ] AWS Account/Project ID
- [ ] Region (for cloud services)
- [ ] Auth method (IAM role, API key, service account)
- [ ] Credential storage (Secrets Manager, .env, etc.)
- [ ] Features (streaming, caching, function calling, vision)
- [ ] Cost estimate (per token/request)
- [ ] Integration point (API endpoint, service module)
- [ ] Error handling (retries, fallback, timeouts)
- [ ] Rate limiting strategy

**Scoring:**
- 11/11 required fields: ✅ Complete
- 9-10/11: ⚠️ Nearly complete
- <9/11: ❌ Insufficient detail

### Authentication Proposals

**Required fields:**
- [ ] Provider (Supabase, Auth0, Cognito, custom)
- [ ] Project/Account ID
- [ ] Project URL (for managed services)
- [ ] Methods (email/password, OAuth providers, magic link, etc.)
- [ ] Session management (JWT, cookie, expiry, refresh)
- [ ] Storage (auth tables, user profiles schema)
- [ ] Middleware/guards (where applied, protection scope)
- [ ] Password policy (hashing, complexity, length)
- [ ] MFA support (method, optional/required)
- [ ] Rate limiting (attempts, window, tracking method)
- [ ] Email sender (address, display name, SMTP provider) ← CRITICAL if email-based auth
- [ ] Integration (library init, env var location)

**Scoring:**
- 12/12 required fields: ✅ Complete
- 10-11/12: ⚠️ Nearly complete
- <10/12: ❌ Insufficient detail

### DNS Setup Proposals

**Required fields:**
- [ ] Provider (Cloudflare, Route53, etc.)
- [ ] Account ID
- [ ] Zone/domain
- [ ] Apex domain record (A/AAAA, IP/target)
- [ ] WWW subdomain record (CNAME, target)
- [ ] Additional subdomains (api, cdn, etc.)
- [ ] SSL/TLS (provider, mode, auto-renew)
- [ ] TTL values (per record type)
- [ ] Redirects (www ↔ apex, HTTP → HTTPS)
- [ ] Integration/IaC (Terraform, CloudFormation, manual)

**Scoring:**
- 10/10 required fields: ✅ Complete
- 8-9/10: ⚠️ Nearly complete
- <8/10: ❌ Insufficient detail

### Payment Integration Proposals

**Required fields:**
- [ ] SDK (library + version)
- [ ] Account ID
- [ ] API keys (test/live, where stored)
- [ ] Webhook (endpoint, signature verification)
- [ ] Events (which events subscribed)
- [ ] Products/Prices (IDs, pricing)
- [ ] Features (customer portal, invoices, tax)
- [ ] Error handling (idempotency, retries)
- [ ] PCI compliance (no card storage, tokenization method)
- [ ] Integration (framework, customer mapping)

**Scoring:**
- 10/10 required fields: ✅ Complete
- 8-9/10: ⚠️ Nearly complete
- <8/10: ❌ Insufficient detail

### API Integration Proposals

**Required fields:**
- [ ] Service name + provider
- [ ] Account/Project ID
- [ ] SDK/library + version
- [ ] API keys (where stored, rotation)
- [ ] Endpoints (which APIs used)
- [ ] Rate limiting (provider limits, our handling)
- [ ] Error handling (retries, fallback)
- [ ] Webhooks (if applicable)
- [ ] Data mapping (how integrated with app)
- [ ] Integration point (module, service layer)

**Scoring:**
- 10/10 required fields: ✅ Complete
- 8-9/10: ⚠️ Nearly complete
- <8/10: ❌ Insufficient detail

### Infrastructure/Deployment Proposals

**Required fields:**
- [ ] Platform (AWS, GCP, Azure, Vercel, etc.)
- [ ] Account/Organization ID
- [ ] Region(s)
- [ ] Services (specific service names: ECS, AppRunner, Lambda, etc.)
- [ ] Instance/Resource names
- [ ] Compute specs (CPU, memory, scaling)
- [ ] Networking (VPC, subnets, security groups)
- [ ] Storage (volumes, S3, backups)
- [ ] Monitoring (CloudWatch, DataDog, etc.)
- [ ] IaC tool (Terraform, CDK, CloudFormation)
- [ ] Cost estimate

**Scoring:**
- 11/11 required fields: ✅ Complete
- 9-10/11: ⚠️ Nearly complete
- <9/11: ❌ Insufficient detail

## Output Format

```
## Audit Report: [Category] Proposal

**Completeness Score:** X/Y (Z%)

### ✅ Present
- Field 1: [value]
- Field 2: [value]
...

### ❌ Missing
- [ ] Field A (CRITICAL: reason why needed)
- [ ] Field B (reason)
...

### ⚠️ Recommendations
- Consider adding: [specific suggestion]
- Clarify: [ambiguous detail]

### Verdict
[✅ Complete / ⚠️ Nearly Complete / ❌ Insufficient] - [explanation]

**Suggested additions:**
```
[Show what a complete version would look like with missing fields added]
```
```

## Instructions

1. **Read proposal** from user argument
2. **Detect category** (database, AI/ML, auth, DNS, payment, API, infrastructure)
3. **Load checklist** for detected category
4. **Parse proposal** and check for each required field
5. **Score completeness** (present fields / total required)
6. **List missing fields** with criticality explanations
7. **Generate verdict** (Complete, Nearly Complete, Insufficient)
8. **Show improved version** with missing fields added (using reasonable defaults/examples)

## Edge Cases

**Multiple categories:**
If proposal spans multiple categories (e.g., "Add auth with email"), audit against ALL relevant checklists.

**Unrecognized category:**
If category unclear, ask user to specify or list fields found vs. general best practices.

**Partial proposals:**
If proposal is intentionally high-level (early planning), note this and suggest when to expand.

## Examples

### Example 1: Incomplete Database Proposal

**Input:**
```
Adding PostgreSQL with Prisma
```

**Output:**
```
## Audit Report: Database Proposal

**Completeness Score:** 2/11 (18%)

### ✅ Present
- Stack: PostgreSQL + Prisma ORM

### ❌ Missing (CRITICAL)
- [ ] Versions (PostgreSQL version? Prisma version?)
- [ ] Extensions (pg_vector needed? PostGIS?)
- [ ] Location (local, Docker, RDS? Env-specific?)
- [ ] Instance name (for cloud deployments)
- [ ] AWS Account/Project ID (for managed DB)
- [ ] Credentials (where stored? Rotation?)
- [ ] Schema (which tables? Key fields?)
- [ ] Pooling (max connections? timeout?)
- [ ] Migrations (versioning strategy?)
- [ ] Backups (method? retention?)
- [ ] Port + connection string

### Verdict
❌ INSUFFICIENT - Missing 82% of critical details. Cannot approve without:
1. Env-specific locations (local vs prod)
2. Schema design
3. Credential management
4. Operational details (pooling, migrations, backups)

**Complete version:**
```
Adding postgres database:
- Stack: PostgreSQL 16.1 + Prisma ORM v5.x + pg_vector extension
- Instance: Local Docker (dev), RDS postgres-prod-01 (prod, us-east-1)
- AWS Account: protoflow-prod (123456789012)
- Credentials: .env (dev), AWS Secrets Manager db-creds (prod), rotated 90d
- Schema: users, documents, embeddings tables
  - users: id (uuid), email (unique), created_at
  - documents: id, user_id (fk), content (text), vector (vector(1536))
- Pooling: max 20 connections, timeout 30s
- Migrations: Prisma migrate, versioned in git
- Backups: RDS auto-backup daily, retention 7d
- Port: 5432, connection string in DATABASE_URL
```
```

### Example 2: Complete Auth Proposal

**Input:**
```
Adding authentication:
- Provider: Supabase Auth + JWT
- Project: protoflow-prod (xyzabcdefghijklmnop)
- URL: https://xyzabcdefghijklmnop.supabase.co
- Methods: Email/password, OAuth (Google, GitHub)
- Session: JWT in httpOnly cookie, 7d expiry, refresh rotation
- Storage: auth.users, public.user_profiles
- Middleware: NextJS validates JWT on /api/*, /dashboard/*
- Password: bcrypt, min 12 chars, complexity enforced
- MFA: TOTP optional, qrcode npm
- Rate limiting: 5 attempts/15min, Redis
- Email: noreply@protoflow.com (Protoflow), AWS SES us-east-1
- Integration: lib/supabase.ts, .env.local
```

**Output:**
```
## Audit Report: Authentication Proposal

**Completeness Score:** 12/12 (100%)

### ✅ Present
- Provider: Supabase Auth + JWT
- Project ID: protoflow-prod (xyzabcdefghijklmnop)
- Project URL: https://xyzabcdefghijklmnop.supabase.co
- Methods: Email/password, OAuth (Google, GitHub)
- Session: JWT, httpOnly cookie, 7d expiry, refresh rotation
- Storage: auth.users, public.user_profiles
- Middleware: NextJS, /api/*, /dashboard/*
- Password: bcrypt, min 12 chars, complexity
- MFA: TOTP optional, qrcode
- Rate limiting: 5/15min, Redis
- Email: noreply@protoflow.com (Protoflow), AWS SES us-east-1
- Integration: lib/supabase.ts, .env.local

### ❌ Missing
(none)

### Verdict
✅ COMPLETE - All critical fields present. Proposal ready for approval.

Tech lead can verify:
- Supabase project exists and accessible
- AWS SES configured in us-east-1
- Redis available for rate limiting
- OAuth apps configured for Google/GitHub
```
```

## Category Detection Heuristics

**Database:** postgres, mysql, mongo, dynamo, prisma, typeorm, schema, migration
**AI/ML:** bedrock, openai, anthropic, claude, gpt, llm, model, embedding
**Auth:** authentication, auth, login, oauth, jwt, session, password, supabase auth
**DNS:** dns, domain, cloudflare, route53, apex, www, cname, a record
**Payment:** stripe, payment, subscription, webhook, price, checkout
**API:** api, integration, webhook, sdk, endpoint, rest, graphql
**Infrastructure:** aws, deploy, ecs, lambda, apprunner, docker, terraform

## Enforcement

AI MUST:
- Check ALL required fields for detected category
- Flag missing CRITICAL fields explicitly
- Provide completeness score
- Show improved version with missing fields

AI MUST NOT:
- Approve incomplete proposals
- Guess at missing details
- Skip category-specific requirements
