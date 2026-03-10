---
name: contribute
description: Contribute improvements to the project via GitLab. Creates sandbox, clones repo, makes changes, and opens merge request.
version: 1.0.0
---
<!-- File UUID: 8f2a4c1d-7e9b-4a2f-8c3d-9b5e6f4a7c2e -->

# Contribute - External Contribution Workflow

**Automatically sets up a clean sandbox for external contributions via GitLab**

This skill creates an isolated environment for users to contribute improvements, bug fixes, or features to the project.

## Trigger Phrases

This skill activates when the user says:
- "contribute [description]"
- "make a contribution"
- "open a merge request"
- "submit a change"
- "I want to contribute"

## Execution Flow

### 1. Initialize Sandbox

Create a clean, isolated workspace for the contribution:

```bash
SANDBOX_DIR="/tmp/claude-contributions/$(date +%Y%m%d-%H%M%S)-$(uuidgen | cut -d- -f1)"
mkdir -p "$SANDBOX_DIR"
cd "$SANDBOX_DIR"
```

### 2. Clone from GitLab

Prompt user for repository details if not provided:

```
Repository: [gitlab.com/protoflow/protoflow]
Branch to start from: [main]
```

Clone the repository:

```bash
git clone https://gitlab.com/$NAMESPACE/$REPO.git .
git checkout -b "contrib-$(date +%Y%m%d)-$TOPIC"
```

### 3. Describe the Contribution

Ask user what they want to contribute:

```
What would you like to contribute?
[1] Bug fix
[2] New feature
[3] Documentation improvement
[4] Performance optimization
[5] Refactoring
[6] Test coverage
[7] Other (describe)
```

Gather details:
- **Title:** Brief one-line summary
- **Description:** Detailed explanation
- **Related Issue:** (optional) GitLab issue number

### 4. Make Changes

Options for making changes:

```
How would you like to make changes?

[1] Let me guide Claude to make changes
[2] I'll make changes manually (pause and resume)
[3] Claude suggests changes, I review and apply
```

**Option 1: Guided Changes**
- User describes changes
- Claude implements changes
- User reviews each change

**Option 2: Manual Changes**
- Claude pauses and provides instructions
- User makes changes in external editor
- User signals when ready to continue

**Option 3: Suggested Changes**
- Claude analyzes codebase
- Claude suggests specific changes with diffs
- User approves/modifies each suggestion

### 5. Review Changes

Before committing, show comprehensive diff:

```bash
git status
git diff
```

Display summary:
```
Files changed: 3
  - hmode/shared/tools/s3publish.py (+45, -12)
  - hmode/shared/tools/test_s3publish.py (+120, -0)
  - hmode/shared/tools/README.md (+8, -2)

Changes:
- Added retry logic for S3 uploads
- Added comprehensive test coverage
- Updated documentation with new options

Ready to commit? [Y/n/e] (e = edit more)
```

### 6. Commit Changes

Create descriptive commit with metadata:

```bash
git add .
git commit -m "$(cat <<'EOF'
$TITLE

$DESCRIPTION

Contribution-Type: $TYPE
Relates-To: #$ISSUE_NUMBER
Signed-off-by: $USER_NAME <$USER_EMAIL>
EOF
)"
```

Example commit message:
```
Add retry logic to S3 publish tool

Added exponential backoff retry mechanism for S3 uploads to handle
transient network failures. Includes comprehensive test coverage and
updated documentation.

Contribution-Type: enhancement
Relates-To: #1234
Signed-off-by: John Doe <john@example.com>
```

### 7. Push to Fork

Check if user has a fork:

```
Do you have a fork of this repository? [y/N]
```

**If no fork:**
- Use GitLab MCP to create fork
- Add fork as remote

**If has fork:**
- Prompt for fork URL
- Add as remote

```bash
git remote add fork $FORK_URL
git push fork $BRANCH_NAME
```

### 8. Create Merge Request via GitLab MCP

Use GitLab MCP to create merge request:

```typescript
// Using GitLab MCP
await mcp.gitlab.createMergeRequest({
  source_project_id: $FORK_PROJECT_ID,
  target_project_id: $UPSTREAM_PROJECT_ID,
  source_branch: $BRANCH_NAME,
  target_branch: "main",
  title: $TITLE,
  description: `
## Summary
${DESCRIPTION}

## Type of Change
- [x] ${TYPE}

## Testing
${TESTING_NOTES}

## Checklist
- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Comments added for complex code
- [x] Documentation updated
- [x] No new warnings generated
- [x] Tests added/updated
- [x] All tests pass

## Related Issues
${ISSUE_LINKS}
  `,
  labels: [$LABELS],
  remove_source_branch: false
});
```

### 9. Report Success

Display merge request details:

```
✅ Merge Request Created!

Title: Add retry logic to S3 publish tool
MR: !42
URL: https://gitlab.com/protoflow/protoflow/-/merge_requests/42
Status: Open
Branch: contrib-20260204-retry-logic → main

Sandbox Location: $SANDBOX_DIR

Next Steps:
[1] Wait for review
[2] Address review comments (return to sandbox)
[3] Clean up sandbox (when MR is merged)

Maintainers will be notified. You'll receive email updates on the MR.
```

## Advanced Features

### A. Multi-Commit Contributions

For larger contributions spanning multiple logical changes:

```
This contribution involves multiple changes. Create separate commits? [Y/n]

Commit 1/3: Add retry mechanism
[make changes, commit]

Commit 2/3: Add tests
[make changes, commit]

Commit 3/3: Update documentation
[make changes, commit]
```

### B. Draft Merge Requests

For work-in-progress contributions:

```
Mark as draft? [y/N]

This creates a draft MR for early feedback. You can:
- Get maintainer input on approach
- Show progress on complex features
- Mark ready when complete
```

### C. CI/CD Preview

If project has CI/CD:

```
✓ Pushed to fork
⏳ Waiting for CI/CD pipeline...

Pipeline Status:
- lint: ✓ passed
- test: ✓ passed (42 tests)
- build: ⏳ running...

View pipeline: https://gitlab.com/.../pipelines/12345
```

### D. Contribution Templates

Auto-fill from `.gitlab/merge_request_templates/`:

```
Select contribution template:
[1] bug_fix.md
[2] feature.md
[3] documentation.md
[4] skip (manual description)
```

## Error Handling

### No GitLab MCP Configured

```
✗ Error: GitLab MCP not configured

To set up GitLab MCP:
1. Run: claude mcp add

2. When prompted, configure:
   Server name: gitlab
   Command: uvx
   Args: ["mcp-server-gitlab"]
   Environment:
     GITLAB_PERSONAL_ACCESS_TOKEN: <your-token>
     GITLAB_URL: https://gitlab.com

3. Restart Claude Code

Or contribute manually:
[1] Create fork manually
[2] Push changes manually
[3] Open MR via web UI
```

### Fork Creation Failed

```
✗ Error: Could not create fork

This may happen if:
- Fork already exists
- Insufficient permissions
- GitLab API rate limit

Workaround:
[1] Use existing fork
[2] Create fork via web UI
[3] Try again later
```

### Push Failed

```
✗ Error: Push rejected

Common causes:
- Authentication failure
- Protected branch
- Large file in commit

Solutions:
[1] Check git credentials
[2] Push to different branch
[3] Remove large files (.gitignore)
```

### Merge Request Creation Failed

```
✗ Error: Could not create merge request

Common causes:
- MR already exists for branch
- Invalid target branch
- API token lacks permissions

Fallback:
View MR URL: https://gitlab.com/$NAMESPACE/$REPO/-/merge_requests/new?merge_request[source_branch]=$BRANCH

You can create the MR manually using this URL.
```

## Sandbox Management

### List Active Sandboxes

```bash
ls -la /tmp/claude-contributions/
```

### Return to Sandbox

```
Return to previous contribution? [y/N]

Active sandboxes:
[1] 20260204-140532-a7f3b2c1 (contrib-retry-logic)
[2] 20260203-091245-d4e8f9a2 (contrib-docs-update)

Select [1-2] or 'n':
```

### Clean Up Sandbox

```
Clean up sandbox? [y/N]

This will:
- Remove local sandbox directory
- Keep your fork and MR intact

Choose:
[1] Clean up after MR merged
[2] Clean up now (I'm done)
[3] Keep sandbox (I'll return)
```

## Best Practices

### 1. Small, Focused Changes

Encourage atomic contributions:
- One logical change per MR
- Clear, specific title
- Detailed description with context

### 2. Follow Project Conventions

Before making changes:
- Read CONTRIBUTING.md (if exists)
- Match existing code style
- Follow naming conventions
- Use project's preferred tools

### 3. Test Locally

Always test before pushing:
```bash
# Run project tests
make test  # or npm test, pytest, etc.

# Verify changes work
make build
make run
```

### 4. Clear Communication

MR description should include:
- **Why:** Problem or motivation
- **What:** Changes made
- **How:** Implementation approach
- **Testing:** How to verify

### 5. Respond to Feedback

Be prepared to:
- Address review comments
- Make requested changes
- Explain design decisions
- Iterate on implementation

## Integration with Existing Workflows

### A. Link to Issues

```
Related to existing issue? [y/N]

Issue number: #1234

Closes #1234
```

### B. Request Review

```
Request specific reviewers? [y/N]

GitLab usernames (comma-separated): @maintainer1, @maintainer2
```

### C. Assign Labels

```
Add labels? [y/N]

Available labels:
- enhancement
- bug
- documentation
- good-first-issue

Select (comma-separated): enhancement, needs-review
```

## Example Session

```
User: "I want to contribute a fix for the S3 upload timeout issue"

AI: ✓ Initializing contribution sandbox...
    Sandbox: /tmp/claude-contributions/20260204-140532-a7f3b2c1

    Cloning from GitLab...
    Repository: gitlab.com/protoflow/protoflow
    Branch: main

    What would you like to contribute?
    [1] Bug fix ← detected from your message
    [2] New feature
    [3] Documentation improvement
    ...

User: 1

AI: ✓ Creating branch: contrib-20260204-s3-timeout-fix

    Describe the bug fix:
    Title: [Fix S3 upload timeout issue]
    Description: [Add timeout parameter to S3 upload calls]
    Related Issue: [#1234]

User: (confirms details)

AI: How would you like to make changes?
    [1] Let me guide Claude to make changes ← recommended
    [2] I'll make changes manually
    [3] Claude suggests changes, I review

User: 1

AI: ✓ Analyzing codebase...
    Found: hmode/shared/tools/s3publish.py

    Suggested changes:
    1. Add timeout parameter to boto3 calls (line 45)
    2. Add exponential backoff retry logic (line 67)
    3. Update function signature (line 12)

    Apply changes? [Y/n]

User: y

AI: ✓ Changes applied
    ✓ Running tests: All passed

    Ready to commit:
    - hmode/shared/tools/s3publish.py (+15, -3)

    Commit message:
    Fix S3 upload timeout issue

    Added configurable timeout parameter to S3 upload operations
    with exponential backoff retry logic for transient failures.

    Closes #1234

    Commit? [Y/n]

User: y

AI: ✓ Changes committed
    ✓ Pushing to fork: gitlab.com/user/protoflow
    ✓ Creating merge request...

    ✅ Merge Request Created!
    MR: !42
    URL: https://gitlab.com/protoflow/protoflow/-/merge_requests/42

    Pipeline Status: ⏳ Running tests...
```

## Configuration

Store user preferences in `.claude/contribute-config.yaml`:

```yaml
# GitLab Configuration
gitlab:
  default_instance: gitlab.com
  username: johndoe
  fork_namespace: johndoe

# Contribution Preferences
preferences:
  default_branch: main
  auto_cleanup: false
  request_reviewers: true
  add_labels: true

# Sandbox Settings
sandbox:
  base_path: /tmp/claude-contributions
  keep_count: 5
  auto_clean_after_days: 7
```

## Summary

This skill provides a complete external contribution workflow:

1. **Isolated Environment:** Clean sandbox for each contribution
2. **GitLab Integration:** Seamless fork, push, and MR creation
3. **Guided Process:** Step-by-step assistance
4. **Best Practices:** Enforces good contribution habits
5. **Error Handling:** Graceful fallbacks for common issues

The combination of sandbox isolation + GitLab MCP + guided workflow creates a smooth contribution experience for external users.
