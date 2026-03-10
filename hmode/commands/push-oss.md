# Push OSS Content to OSS Remote

**Command:** `/push-oss [commit-message]`

## Instructions

You are tasked with committing and pushing open source content to the public OSS remote repository.

**Workflow:**

1. **Detect OSS content:**
   - Check for changes in:
     - `prototypes/oss/*`
     - `project-management/ideas/oss/*`
     - `artifacts/oss/*`
     - `docs/oss/*`

2. **Verify no work/personal content:**
   - CRITICAL: Ensure NO files from `work/` or `personal/` directories are staged
   - If work/personal content detected, ABORT and warn user
   - OSS content is PUBLIC - double-check for secrets/credentials

3. **Stage OSS content:**
   ```bash
   git add prototypes/oss/
   git add project-management/ideas/oss/
   git add artifacts/oss/
   git add docs/oss/
   ```

4. **Commit with message:**
   - If user provided commit message, use it
   - Otherwise, generate descriptive commit message based on changes
   - Format: `oss: <description>`

5. **Double confirmation for PUBLIC push:**
   - Generate random UUID confirmation code
   - Display WARNING and list of files to be pushed PUBLIC
   - Require user to type the exact UUID to proceed
   - If UUID doesn't match, ABORT

6. **Push to OSS remote:**
   ```bash
   git push oss HEAD:main
   ```

7. **Confirm:**
   - Show commit SHA
   - Show files pushed
   - Confirm push to OSS remote successful
   - Remind user this is now PUBLIC

## Safety Checks

**BEFORE pushing:**
- ❌ ABORT if any `*/work/*` files are staged
- ❌ ABORT if any `*/personal/*` files are staged
- ❌ ABORT if secrets/credentials detected (.env, *.pem, etc.)
- ⚠️  Generate UUID and require user to type it to confirm PUBLIC push
- ⚠️  WARN that this is a PUBLIC repository
- ✅ ONLY proceed if UUID matches exactly

## Example

```bash
# User runs: /push-oss "Add CLI framework"

# AI shows:
⚠️  WARNING: You are about to push to a PUBLIC OSS repository!

Files to be pushed:
  - prototypes/oss/cli-framework/src/main.py
  - prototypes/oss/cli-framework/README.md
  - prototypes/oss/cli-framework/package.json

To confirm this PUBLIC push, type the following UUID:
  a3f5c8e1-4b2d-4a9e-8c3f-7d6e5b4a3c2b

# User types: a3f5c8e1-4b2d-4a9e-8c3f-7d6e5b4a3c2b

# AI executes:
git add prototypes/oss/cli-framework/
git commit -m "oss: Add CLI framework"
git push oss HEAD:main

✅ Pushed to PUBLIC OSS remote successfully
Reminder: This code is now publicly accessible
```

## Error Handling

- If no OSS changes detected: inform user
- If work/personal content detected: ABORT with warning
- If secrets detected: ABORT with security warning
- If push fails: show error and suggest fixes

## Security Reminder

**OSS content is PUBLIC.** Before pushing:
- Remove all API keys, tokens, credentials
- Remove company-specific information
- Remove internal URLs/endpoints
- Ensure license headers are present
- Verify README has proper attribution
