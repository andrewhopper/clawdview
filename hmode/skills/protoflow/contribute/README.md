# Contribute Skill - External Contribution Workflow

<!-- File UUID: 9e3f7c1d-4b8a-4e2f-9d6c-8a5f7b4e3c2d -->

## Overview

The `/contribute` skill enables external users to contribute improvements to ProtoFlow via GitLab. It automates the entire contribution workflow:

1. **Sandbox Creation** - Isolated workspace for each contribution
2. **Repository Cloning** - Clone from GitLab automatically
3. **Guided Changes** - Step-by-step assistance with changes
4. **GitLab Integration** - Create forks and merge requests via MCP

## Quick Start

### 1. Setup (One-time)

```bash
# Configure GitLab MCP
cd /Users/andyhop/dev/hl-protoflow/hmode/skills/contribute
cat SETUP.md

# Follow the setup instructions to:
# - Get GitLab personal access token
# - Configure GitLab MCP server
# - Verify configuration
```

### 2. Make Your First Contribution

```
User: "I want to contribute a documentation fix"
```

Claude will:
- Create sandbox in `/tmp/claude-contributions/`
- Clone the repository
- Guide you through changes
- Create merge request when ready

## Usage Examples

### Interactive Mode (Recommended)

```
User: "/contribute"
```

Claude will ask:
- What type of contribution? (bug-fix, feature, docs, etc.)
- What's the title and description?
- Related issue number? (optional)

### Quick Mode (With Arguments)

```
User: "/contribute --description \"Fix S3 timeout\" --type bug-fix"
```

Claude will:
- Create sandbox immediately
- Use provided description and type
- Skip interactive questions

### Specific Issue

```
User: "/contribute --type docs --issue 1234"
```

Claude will:
- Link to issue #1234
- Use issue title if available
- Auto-populate description from issue

## File Structure

```
hmode/skills/contribute/
├── README.md                    # This file
├── SETUP.md                     # GitLab MCP setup guide
├── contribute.md                # Full skill documentation
├── skill.json                   # Skill metadata
├── handler.py                   # Python handler script
├── contribute-config.yaml       # Configuration (customizable)
└── .gitignore                   # Protect user configs
```

## Configuration

Edit `contribute-config.yaml` to customize:

### Repository Settings

```yaml
repository:
  upstream:
    url: https://gitlab.com/protoflow/protoflow
    namespace: protoflow
    project: protoflow
    default_branch: main
```

### Contribution Preferences

```yaml
contributions:
  auto_fork: true                # Auto-create fork if needed
  branch_prefix: contrib         # Branch naming: contrib-YYYYMMDD-topic
  require_tests: true            # Require tests before MR
  auto_labels:                   # Auto-apply these labels
    - contribution
    - needs-review
  default_reviewers:             # Request these reviewers
    - andyhop
```

### Sandbox Settings

```yaml
sandbox:
  base_path: /tmp/claude-contributions
  keep_count: 5                  # Keep last 5 sandboxes
  auto_clean_after_days: 7       # Clean up after 7 days
```

## Workflow Details

### Phase 1: Initialization

```
User: "/contribute"
  ↓
Create sandbox: /tmp/claude-contributions/20260204-140532-a7f3b2c1
  ↓
Clone repo: https://gitlab.com/protoflow/protoflow
  ↓
Create branch: contrib-20260204-fix-timeout
```

### Phase 2: Make Changes

Claude offers three modes:

**Mode 1: Guided (Recommended)**
- User describes changes
- Claude implements
- User reviews each change

**Mode 2: Manual**
- Claude pauses
- User edits files externally
- User signals when ready

**Mode 3: Suggested**
- Claude analyzes and suggests
- User approves/modifies
- Claude applies

### Phase 3: Review & Commit

```
Show comprehensive diff
  ↓
User confirms changes
  ↓
Create descriptive commit
  ↓
Include metadata (type, issue, signed-off-by)
```

### Phase 4: Push & MR

```
Check for existing fork
  ↓
Create fork if needed (via GitLab MCP)
  ↓
Push branch to fork
  ↓
Create merge request (via GitLab MCP)
  ↓
Display MR URL and details
```

## GitLab MCP Integration

The skill uses GitLab MCP for:

### 1. Fork Management

```typescript
// Create fork if doesn't exist
await mcp.gitlab.forkProject({
  project_id: upstream_project_id,
  namespace: user_namespace
});
```

### 2. Merge Request Creation

```typescript
// Create MR with template
await mcp.gitlab.createMergeRequest({
  source_project_id: fork_project_id,
  target_project_id: upstream_project_id,
  source_branch: branch_name,
  target_branch: "main",
  title: title,
  description: formatted_description,
  labels: ["contribution", "needs-review"],
  remove_source_branch: false
});
```

### 3. Pipeline Status

```typescript
// Monitor CI/CD pipeline
const pipeline = await mcp.gitlab.getPipelineStatus({
  project_id: fork_project_id,
  ref: branch_name
});
```

## Sandbox Management

### List Active Sandboxes

```bash
ls -la /tmp/claude-contributions/
```

Example output:
```
20260204-140532-a7f3b2c1/  (contrib-fix-timeout)
20260203-091245-d4e8f9a2/  (contrib-docs-update)
```

### Return to Sandbox

```
User: "Resume my contribution from yesterday"

Claude: Found 2 active sandboxes:
[1] 20260204-140532-a7f3b2c1 (contrib-fix-timeout)
[2] 20260203-091245-d4e8f9a2 (contrib-docs-update)

Select [1-2]:
```

### Clean Up Sandboxes

```bash
# Manual cleanup
rm -rf /tmp/claude-contributions/20260204-*

# Or via skill
User: "Clean up my contribution sandboxes"
```

## Contribution Best Practices

### 1. Atomic Changes

Keep contributions focused:
- One logical change per MR
- Clear, specific title
- Detailed description

### 2. Test Locally

Always test before submitting:
```bash
cd /tmp/claude-contributions/20260204-140532-a7f3b2c1
make test  # or npm test, pytest, etc.
```

### 3. Follow Conventions

- Read `CONTRIBUTING.md` (if exists)
- Match existing code style
- Use project's tools and patterns

### 4. Write Good Commit Messages

```
Fix S3 upload timeout issue

Added configurable timeout parameter to S3 upload operations
with exponential backoff retry logic for transient failures.

This fixes the issue where large file uploads would fail after
60 seconds even if the connection was still active.

Contribution-Type: bug-fix
Closes #1234
Signed-off-by: John Doe <john@example.com>
```

### 5. Respond to Feedback

- Address review comments promptly
- Explain design decisions
- Be open to changes
- Iterate based on feedback

## Troubleshooting

### GitLab MCP Not Configured

```
Error: GitLab MCP not found

Solution: Run setup
cd hmode/skills/contribute
cat SETUP.md
```

### Authentication Failed

```
Error: 401 Unauthorized

Solutions:
1. Check token is set: echo $GITLAB_PERSONAL_ACCESS_TOKEN
2. Verify token scopes: api, read_repository, write_repository
3. Check token hasn't expired
```

### Fork Already Exists

```
Error: Fork already exists

Solutions:
1. Use existing fork
2. Delete old fork via GitLab UI
3. Manual fork creation
```

### Push Failed

```
Error: Push rejected

Solutions:
1. Verify git credentials
2. Check token has write_repository scope
3. Ensure pushing to fork (not upstream)
```

## Security Considerations

### 1. Token Management

- Store tokens in environment variables only
- Never commit tokens to git
- Rotate tokens every 6-12 months

### 2. Sandbox Isolation

- Sandboxes in `/tmp` (ephemeral)
- Don't store sensitive data in sandbox
- Clean up regularly

### 3. Code Review

- All contributions reviewed by maintainers
- CI/CD pipeline validates code
- Security scanning on every MR

## Example Session

```
User: "I want to contribute a fix for the S3 upload timeout"

Claude: ✓ Initializing contribution sandbox...
        Sandbox: /tmp/claude-contributions/20260204-140532-a7f3b2c1

        ✓ Cloning from GitLab...
        Repository: gitlab.com/protoflow/protoflow
        Branch: main

        What type of contribution?
        [1] Bug fix ← detected
        [2] New feature
        [3] Documentation
        ...

User: 1

Claude: ✓ Creating branch: contrib-20260204-s3-timeout

        Title: Fix S3 upload timeout issue
        Description: Add timeout parameter to S3 calls
        Related Issue: #1234

        Correct? [Y/n]

User: y

Claude: How to make changes?
        [1] Guide me through changes ← recommended
        [2] I'll edit manually
        [3] Suggest changes for review

User: 1

Claude: ✓ Analyzing codebase...
        Found: hmode/shared/tools/s3publish.py

        Changes needed:
        1. Add timeout parameter (line 45)
        2. Add retry logic (line 67)

        Apply? [Y/n]

User: y

Claude: ✓ Applied changes
        ✓ Running tests... All passed

        Ready to commit? [Y/n]

User: y

Claude: ✓ Changes committed
        ✓ Pushing to fork...
        ✓ Creating merge request...

        ✅ Merge Request Created!
        MR: !42
        URL: https://gitlab.com/protoflow/protoflow/-/merge_requests/42

        Pipeline: ⏳ Running tests...
```

## Support

For issues with the contribution workflow:

1. Check `SETUP.md` for configuration help
2. Review `contribute.md` for full documentation
3. Open issue on GitLab with `/contribute` label
4. Contact maintainers: @andyhop

## Related Skills

- `/workon` - Find and work on existing projects
- `/run` - Execute prototypes with semantic search
- `/domain-search` - Search for reusable domain models

## Version History

- **1.0.0** (2026-02-04)
  - Initial release
  - GitLab MCP integration
  - Sandbox management
  - Guided workflow
  - MR creation automation
