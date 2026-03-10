# Push Personal Content to Personal Remote

**Command:** `/push-personal [commit-message]`

## Instructions

You are tasked with committing and pushing personal content to the personal remote repository.

**Workflow:**

1. **Detect personal content:**
   - Check for changes in:
     - `prototypes/personal/*`
     - `project-management/ideas/personal/*`
     - `artifacts/personal/*`
     - `docs/personal/*`

2. **Verify no work content:**
   - CRITICAL: Ensure NO files from `work/` directories are staged
   - If work content detected, ABORT and warn user

3. **Stage personal content:**
   ```bash
   git add prototypes/personal/
   git add project-management/ideas/personal/
   git add artifacts/personal/
   git add docs/personal/
   ```

4. **Commit with message:**
   - If user provided commit message, use it
   - Otherwise, generate descriptive commit message based on changes
   - Format: `personal: <description>`

5. **Push to personal remote:**
   ```bash
   git push personal HEAD:main
   ```

6. **Confirm:**
   - Show commit SHA
   - Show files pushed
   - Confirm push to personal remote successful

## Safety Checks

**BEFORE pushing:**
- ❌ ABORT if any `*/work/*` files are staged
- ❌ ABORT if pushing to wrong remote
- ❌ ABORT if current branch contains work commits
- ✅ ONLY proceed if all personal content

## Example

```bash
# User runs: /push-personal "Add blog post generator"

# AI executes:
git add prototypes/personal/blog-generator/
git commit -m "personal: Add blog post generator"
git push personal HEAD:main
```

## Error Handling

- If no personal changes detected: inform user
- If work content detected: ABORT with warning
- If push fails: show error and suggest fixes
