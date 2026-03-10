---
description: Add error tracking to a project using the shared JS error tracker tool
tags: [integration, error-tracking, monitoring, shared-tools]
trigger: "add error tracker", "integrate error tracking", "add error tracking"
---

# Add Error Tracker Skill

Integrates the lightweight JavaScript error tracker (`tool-error-tracker-js-et001`) into a project.

## Trigger Phrases

- "add error tracker to [project]"
- "integrate error tracking into [project]"
- "add error tracking to [project]"
- "setup error tracker for [project]"

## Prerequisites Check

1. Verify error tracker infrastructure is deployed:
   ```bash
   cd projects/shared/tool-error-tracker-js-et001
   make infra-status
   ```

2. Get API endpoint from CDK outputs:
   ```bash
   cd projects/shared/tool-error-tracker-js-et001
   make get-endpoint
   # Or check: infra/deploys/current/outputs.json
   ```

## Integration Steps

### Step 1: Identify Target Project

Extract project name from user request and resolve using nav hints:

```python
import yaml
target = "gocoder"  # from user request

with open('.claude/nav-hints/hints.yaml') as f:
    hints = yaml.safe_load(f)['hints']

for hint in hints:
    if target.lower() in [a.lower() for a in hint['aliases']]:
        project_path = hint['project_path']
        break
```

### Step 2: Determine Integration Method

**For web projects (React, Next.js, Vite, HTML):**
- Use npm package or script tag
- Check for `package.json` → npm
- Check for static HTML → script tag

**For non-web projects:**
- Skip (error tracker is frontend-only)

### Step 3: Add Package Dependency

**For npm projects:**

```bash
cd {project_path}
npm install @hopper-labs/error-tracker-js
# or
yarn add @hopper-labs/error-tracker-js
```

### Step 4: Initialize Tracker

**React/Vite projects** - Add to main entry point (e.g., `src/main.tsx`):

```typescript
import { ErrorTracker } from '@hopper-labs/error-tracker-js';

// Initialize before React render
ErrorTracker.init({
  endpoint: process.env.VITE_ERROR_TRACKER_ENDPOINT,
  project: '{project-name}',
  release: process.env.VITE_APP_VERSION || '1.0.0',
  environment: process.env.NODE_ENV || 'development',
  // Optional: only track in production
  enabled: process.env.NODE_ENV === 'production',
});

// Your React render code...
```

**Next.js projects** - Add to `pages/_app.tsx`:

```typescript
import { ErrorTracker } from '@hopper-labs/error-tracker-js';
import { useEffect } from 'react';

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    ErrorTracker.init({
      endpoint: process.env.NEXT_PUBLIC_ERROR_TRACKER_ENDPOINT,
      project: '{project-name}',
      release: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
      environment: process.env.NODE_ENV || 'development',
    });
  }, []);

  return <Component {...pageProps} />;
}
```

**Static HTML projects** - Add script tag before `</body>`:

```html
<script
  src="https://cdn.hopper-labs.com/error-tracker.min.js"
  data-endpoint="https://xxx.execute-api.us-east-1.amazonaws.com/v1/errors"
  data-project="{project-name}"
  data-release="1.0.0"
></script>
```

### Step 5: Add Environment Variables

**Vite projects** - Add to `.env`:

```bash
# Error Tracker Configuration
VITE_ERROR_TRACKER_ENDPOINT=https://xxx.execute-api.us-east-1.amazonaws.com/v1/errors
VITE_APP_VERSION=1.0.0
```

**Next.js projects** - Add to `.env.local`:

```bash
# Error Tracker Configuration
NEXT_PUBLIC_ERROR_TRACKER_ENDPOINT=https://xxx.execute-api.us-east-1.amazonaws.com/v1/errors
NEXT_PUBLIC_APP_VERSION=1.0.0
```

**Amplify projects** - Add environment variables in AWS Amplify Console:
1. Go to App Settings → Environment variables
2. Add `VITE_ERROR_TRACKER_ENDPOINT` or `NEXT_PUBLIC_ERROR_TRACKER_ENDPOINT`
3. Redeploy

### Step 6: Test Integration

**Development test:**

```javascript
// Add to a component or console
window.ErrorTracker.trackError(new Error('Test error from skill integration'));
```

**Production test:**
1. Deploy the updated project
2. Open browser DevTools → Network tab
3. Trigger an error or use test code above
4. Verify POST request to error tracker endpoint
5. Check DynamoDB table for error entry

### Step 7: View Errors

**Option A: DynamoDB Console**
```bash
# Get table name from CDK outputs
cd projects/shared/tool-error-tracker-js-et001
make get-table-name

# Open in AWS Console
open "https://console.aws.amazon.com/dynamodbv2/home?region=us-east-1#table?name={table-name}"
```

**Option B: Static HTML Viewer**
```bash
cd projects/shared/tool-error-tracker-js-et001
open viewer/index.html
```

## Output Format

After successful integration, provide:

```
✓ Error tracker integrated into {project-name}

📦 Package: @hopper-labs/error-tracker-js
📍 Initialized in: {file-path}
🔧 Environment: {.env file path}
🎯 Endpoint: {API endpoint}

Next steps:
1. Test with: ErrorTracker.trackError(new Error('Test'))
2. Deploy to see errors in: {viewer URL or DynamoDB link}
3. Check errors: cd projects/shared/tool-error-tracker-js-et001 && make view-errors
```

## Error Handling

**If error tracker not deployed:**
```
⚠️ Error tracker infrastructure not deployed.

To deploy:
  cd projects/shared/tool-error-tracker-js-et001
  make infra-bootstrap  # First time only
  make infra-deploy

Then re-run this skill.
```

**If target project not found:**
```
❌ Could not find project "{project}".

Try:
  /workon {project}    # Search for project
  Add to nav hints     # If project exists but not in hints
```

**If target is not a web project:**
```
ℹ️ Error tracker is for frontend JavaScript projects only.

{project} appears to be a {Python/CLI/backend} project.
Consider using CloudWatch Logs or application-specific logging instead.
```

## Related

- **Tool location:** `projects/shared/tool-error-tracker-js-et001`
- **Generic integration:** Use `/skill add-shared-tool` for other shared tools
- **Documentation:** `projects/shared/tool-error-tracker-js-et001/README.md`

---

**Version:** 1.0.0
**Created:** 2025-12-22
