# Push Work Content to Work Remote

**Command:** `/push-work [commit-message]`

## Instructions

You are tasked with committing and pushing work-related content to the work remote repository.

**Workflow:**

1. **Detect work content:**
   - Check for changes in:
     - `prototypes/work/*`
     - `project-management/ideas/work/*`
     - `artifacts/work/*`
     - `docs/work/*`

2. **Verify no personal content:**
   - CRITICAL: Ensure NO files from `personal/` directories are staged
   - If personal content detected, ABORT and warn user

3. **Stage work content:**
   ```bash
   git add prototypes/work/
   git add project-management/ideas/work/
   git add artifacts/work/
   git add docs/work/
   ```

4. **Commit with message:**
   - If user provided commit message, use it
   - Otherwise, generate descriptive commit message based on changes
   - Format: `work: <description>`

5. **Push to work remote:**
   ```bash
   git push work HEAD:main
   ```

6. **Confirm:**
   - Show commit SHA
   - Show files pushed
   - Confirm push to work remote successful

## Safety Checks

**BEFORE pushing:**
- ❌ ABORT if any `*/personal/*` files are staged
- ❌ ABORT if pushing to wrong remote
- ❌ ABORT if current branch contains personal commits
- ✅ ONLY proceed if all work content

## Example

```bash
# User runs: /push-work "Add authentication module"

# AI executes:
git add prototypes/work/auth-module/
git commit -m "work: Add authentication module"
git push work HEAD:main
```

## Error Handling

- If no work changes detected: inform user
- If personal content detected: ABORT with warning
- If push fails: show error and suggest fixes
