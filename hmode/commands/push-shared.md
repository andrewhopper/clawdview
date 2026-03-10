# Push Shared Content to All Remotes

**Command:** `/push-shared [commit-message]`

## Instructions

You are tasked with committing and pushing shared content (utilities, .claude docs, guardrails) to both work and personal remotes.

**Workflow:**

1. **Detect shared content:**
   - Check for changes in:
     - `prototypes/shared/*`
     - `project-management/ideas/shared/*`
     - `artifacts/shared/*`
     - `docs/shared/*`
     - `.claude/` (documentation, commands)
     - `hmode/guardrails/` (preferences)
     - `shared/` (utilities)
     - `.system/` (scripts)

2. **Verify no work/personal content:**
   - CRITICAL: Ensure NO files from `work/` or `personal/` directories are staged
   - If work/personal content detected, ABORT and warn user

3. **Stage shared content:**
   ```bash
   git add prototypes/shared/
   git add project-management/ideas/shared/
   git add artifacts/shared/
   git add docs/shared/
   git add .claude/
   git add hmode/guardrails/
   git add shared/
   git add .system/
   git add CLAUDE.md
   ```

4. **Commit with message:**
   - If user provided commit message, use it
   - Otherwise, generate descriptive commit message based on changes
   - Format: `shared: <description>`

5. **Push to both remotes:**
   ```bash
   git push work HEAD:main
   git push personal HEAD:main
   ```

6. **Confirm:**
   - Show commit SHA
   - Show files pushed
   - Confirm push to BOTH work and personal remotes successful

## Safety Checks

**BEFORE pushing:**
- ❌ ABORT if any `*/work/*` files are staged
- ❌ ABORT if any `*/personal/*` files are staged
- ✅ ONLY proceed if all shared infrastructure content

## Example

```bash
# User runs: /push-shared "Update SDLC documentation"

# AI executes:
git add hmode/docs/
git commit -m "shared: Update SDLC documentation"
git push work HEAD:main
git push personal HEAD:main
```

## Error Handling

- If no shared changes detected: inform user
- If work/personal content detected: ABORT with warning
- If push to either remote fails: show error and suggest fixes
- Retry push failures with exponential backoff (2s, 4s, 8s, 16s)
