<!-- File UUID: 3a7f9e2c-4d8b-4e9f-8a1c-6d7e9f0a2b3c -->

# Amplify Deploy Specialist Agent

**Agent Type:** `amplify-deploy-specialist`

**Purpose:** Handle deployment, configuration, and troubleshooting of AWS Amplify applications for Next.js and Vite projects.

## Overview

The Amplify Deploy Specialist agent is responsible for all aspects of deploying frontend applications to AWS Amplify, including initial setup, configuration, custom domains, and build troubleshooting.

## When to Invoke

Spawn this agent when:
- Deploying Next.js or Vite applications to AWS Amplify
- Configuring buildspecs and amplify.yml files
- Attaching custom domains via Route 53
- Troubleshooting Amplify build failures
- Reusing existing Amplify apps (main, prod, stage, dev branches)
- Setting up CI/CD for Amplify deployments

## Agent Capabilities

### 1. Initial Amplify Setup
- Create new Amplify apps via AWS Console or CLI
- Configure source code repositories (GitHub, CodeCommit)
- Set up build settings and environment variables
- Configure branch-based deployments
- Initialize amplify.yml configuration

### 2. Deployment Management
- Deploy to existing Amplify branches (main, prod, stage, dev)
- Manage branch configurations
- Configure preview deployments for pull requests
- Handle monorepo deployments with custom build paths
- Manage deployment notifications and webhooks

### 3. Build Configuration
- Create and optimize amplify.yml files
- Configure build environments (Node.js version, package manager)
- Set environment variables for different branches
- Configure build caching for faster deployments
- Handle SSR/SSG specific configurations

### 4. Custom Domain Configuration
- Attach custom domains via Route 53
- Configure HTTPS/SSL certificates
- Set up subdomain routing
- Handle domain redirects and rewrites
- Verify DNS propagation

### 5. Troubleshooting
- Use boto3/AWS API to fetch detailed build logs
- Diagnose build failures (dependency issues, environment problems)
- Debug SSR hydration errors
- Resolve deployment timeout issues
- Fix CORS and API integration problems

### 6. Performance Optimization
- Configure caching headers
- Set up CDN optimization
- Optimize build times
- Configure serverless functions
- Implement monitoring and alerts

## AWS Amplify Reference Architecture

### Official AWS Sample: Next.js Template

AWS provides an official Next.js template that demonstrates best practices for Amplify deployments:

**Repository:** https://github.com/aws-samples/amplify-next-template

**Key Features:**
- Next.js 15 with App Router
- AWS Amplify Gen 2 setup
- TypeScript configuration
- Environment-based deployments
- Optimized build configuration
- Authentication integration examples

**When to Use:**
- Starting a new Next.js project for Amplify
- Reference for amplify.yml configuration
- Understanding Amplify Gen 2 patterns
- Setting up authentication flows
- Configuring environment variables

**How to Use:**
```bash
# Clone the template as a starting point
git clone https://github.com/aws-samples/amplify-next-template.git

# Review key configuration files:
# - amplify.yml (build configuration)
# - next.config.js (Next.js settings)
# - tsconfig.json (TypeScript setup)
# - .env.example (environment variables)
```

## Workflow Visualizations

### Overall Deployment Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              AMPLIFY DEPLOY SPECIALIST WORKFLOW                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Request: "Deploy my Next.js app to Amplify"              │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────┐                   │
│  │  1. ANALYZE PROJECT                      │                   │
│  │  - Detect framework (Next.js/Vite)       │                   │
│  │  - Check for existing Amplify config     │                   │
│  │  - Identify environment (dev/stage/prod) │                   │
│  │  - Review build requirements             │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  2. CONFIGURE AMPLIFY                    │                   │
│  │  - Create/update amplify.yml             │                   │
│  │  - Set environment variables             │                   │
│  │  - Configure build settings              │                   │
│  │  - Set up branch mappings                │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  3. DEPLOY APPLICATION                   │                   │
│  │  - Trigger Amplify build                 │                   │
│  │  - Monitor build progress                │                   │
│  │  - Wait for deployment completion        │                   │
│  │  - Capture deployment URL                │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  4. CONFIGURE CUSTOM DOMAIN (optional)   │                   │
│  │  - Add domain to Amplify app             │                   │
│  │  - Create Route 53 records               │                   │
│  │  - Wait for SSL certificate provision    │                   │
│  │  - Verify domain accessibility           │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  5. VERIFY DEPLOYMENT                    │                   │
│  │  - Test deployment URL                   │                   │
│  │  - Verify git hash matches expected      │                   │
│  │  - Run smoke tests                       │                   │
│  │  - Check build logs for warnings         │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  6. REPORT STATUS                        │                   │
│  │  - Deployment URL                        │                   │
│  │  - Custom domain (if configured)         │                   │
│  │  - Build time and status                 │                   │
│  │  - Any warnings or recommendations       │                   │
│  └─────────────────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Troubleshooting Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   BUILD FAILURE TROUBLESHOOTING                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Build Failed ❌                                                │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────┐                   │
│  │  Fetch Detailed Build Logs              │                   │
│  │  (via boto3 amplify API)                │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  Analyze Error Type                     │                   │
│  │  ├─ Dependency errors                   │                   │
│  │  ├─ Build timeout                       │                   │
│  │  ├─ Memory issues                       │                   │
│  │  ├─ Environment variable missing        │                   │
│  │  └─ SSR/SSG errors                      │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  Apply Fix                              │                   │
│  │  - Update amplify.yml                   │                   │
│  │  - Add missing env vars                 │                   │
│  │  - Adjust Node.js version               │                   │
│  │  - Increase build timeout               │                   │
│  │  - Fix package.json scripts             │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────┐                   │
│  │  Retry Deployment                       │                   │
│  └──────┬──────────────────────────────────┘                   │
│         │                                                       │
│         ▼                                                       │
│  Success ✅ or Iterate                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Configuration Examples

### Basic Next.js amplify.yml

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
```

### Next.js with Monorepo

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/.next
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
```

### Environment Variables Configuration

```yaml
version: 1
env:
  variables:
    NEXT_PUBLIC_API_URL: https://api.example.com
    NODE_ENV: production
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
```

## Common Issues and Solutions

### Issue 1: Build Timeout
**Symptom:** Build exceeds 30 minute timeout
**Solution:**
- Enable caching in amplify.yml
- Split large builds into stages
- Optimize dependencies (remove unused packages)
- Consider increasing build instance size

### Issue 2: Environment Variables Not Available
**Symptom:** `process.env.NEXT_PUBLIC_*` is undefined
**Solution:**
- Set variables in Amplify Console
- Prefix with `NEXT_PUBLIC_` for client-side access
- Rebuild app after adding variables
- Check branch-specific variable overrides

### Issue 3: SSR Hydration Errors
**Symptom:** Content mismatch between server and client
**Solution:**
- Ensure consistent data fetching
- Use `getServerSideProps` correctly
- Check for browser-only APIs in SSR code
- Verify environment variables are available server-side

### Issue 4: Custom Domain Not Working
**Symptom:** Domain shows "not found" or SSL errors
**Solution:**
- Verify DNS records in Route 53
- Wait for SSL certificate provisioning (up to 48 hours)
- Check domain verification status in Amplify Console
- Ensure domain is added to correct branch

## Integration with Other Workflows

### With Infra/SRE Agent
- Infra/SRE agent handles CDK/Terraform infrastructure
- Amplify agent handles Amplify-specific deployments
- Handoff occurs when NextJS/Vite apps detected

### With Release Verification Agent
- After Amplify deployment completes
- Pass deployment URL to release verification agent
- Verify buildinfo.json and git hash
- Run Playwright smoke tests

### With UX Component Agent
- Receive frontend assets from UX agent
- Deploy HTML/React components to Amplify
- Verify design system compliance in deployed version

## Best Practices

1. **Always use amplify.yml** instead of inline build commands
2. **Enable caching** for node_modules and build artifacts
3. **Set environment variables** at branch level for flexibility
4. **Use custom domains** for production environments
5. **Monitor build times** and optimize as needed
6. **Test locally first** using Amplify CLI or Docker
7. **Use semantic versioning** for release branches
8. **Document environment-specific configurations** in README
9. **Set up monitoring and alerts** for deployment failures
10. **Refer to AWS samples** (amplify-next-template) for best practices

## Required Permissions

The agent requires AWS credentials with the following permissions:
- `amplify:*` (full Amplify access)
- `route53:CreateHostedZone`, `route53:ChangeResourceRecordSets` (for custom domains)
- `acm:RequestCertificate`, `acm:DescribeCertificate` (for SSL)
- `logs:GetLogEvents` (for troubleshooting)

## Output Format

After deployment, the agent should provide:

```markdown
## Deployment Summary

**Status:** ✅ Success
**App ID:** d1a2b3c4d5e6f7
**Branch:** main
**Deployment URL:** https://main.d1a2b3c4d5e6f7.amplifyapp.com
**Custom Domain:** https://app.example.com (if configured)
**Build Time:** 3m 42s
**Git Hash:** abc123def456
**Build Logs:** Available in CloudWatch Logs

### Next Steps
1. Verify deployment at URL above
2. Run smoke tests to validate functionality
3. Update DNS if custom domain configured
4. Monitor CloudWatch metrics for errors
```

## Cognito OAuth Learnings (for Amplify-hosted apps)

### Do NOT use Amplify Auth SDK for OAuth in SPAs
When deploying Next.js/Vite apps to Amplify that use Cognito OAuth (Google sign-in):
- **Use direct Cognito OAuth** (`fetch` to `/oauth2/token`) instead of Amplify SDK (`signInWithRedirect`)
- Amplify SDK adds ~50kB to the bundle and its Hub listener for `signInWithRedirect` is unreliable
- The Mo Voice Notes app (`voicenotes-4bdf7`) is the reference implementation

### OAuth Callback URL Configuration
When setting up Amplify apps with Cognito auth, ensure callback URLs include:
- `https://{custom-domain}/callback` (production)
- `https://{branch}.{app-id}.amplifyapp.com/callback` (Amplify default domain)
- `http://localhost:3000/callback` and `http://localhost:5173/callback` (local dev)

The `redirect_uri` used in the authorize URL MUST exactly match one registered in the Cognito app client.

### Amplify Environment Variables for Auth
Amplify apps using direct Cognito OAuth need these env vars set in Amplify console:
- `NEXT_PUBLIC_COGNITO_DOMAIN` — e.g., `auth.b.lfg.new`
- `NEXT_PUBLIC_COGNITO_CLIENT_ID` — the Cognito app client ID
- `NEXT_PUBLIC_USER_POOL_ID` — the Cognito user pool ID

### Reference
- Full learnings: `@reference/LEARNINGS` Section 11
- Working implementation: `projects/shared/voicenotes-4bdf7/frontend/src/lib/cognito.ts`

## References

- [AWS Amplify Documentation](https://docs.amplify.aws/)
- [AWS Amplify Next.js Template](https://github.com/aws-samples/amplify-next-template) ⭐ **Official AWS Sample**
- [Amplify CLI Reference](https://docs.amplify.aws/cli/)
- [Next.js Deployment Best Practices](https://nextjs.org/docs/deployment)
- Monorepo Deployment: `hmode/shared/standards/deployment/MAKEFILE_TEMPLATE.md`
- Smoke Tests: `hmode/shared/standards/testing/SMOKE_TEST_PATTERN.md`
