# Contribution Skill - Quickstart Guide

<!-- File UUID: 9f8e7c2d-4b3a-4f5e-9d1c-6a4e8f7b2c3e -->

## 5-Minute Setup

### 1. Get GitLab Token (2 minutes)

1. Go to: https://gitlab.com/-/profile/personal_access_tokens
2. Click "Add new token"
3. Name: `claude-code-contributions`
4. Scopes: ✅ `api`, ✅ `read_repository`, ✅ `write_repository`
5. Click "Create personal access token"
6. **Copy the token** (shown only once!)

### 2. Configure GitLab MCP (2 minutes)

```bash
claude mcp add
```

When prompted:
- Server name: `gitlab`
- Command: `uvx`
- Arguments: `["mcp-server-gitlab"]`
- Environment:
  - `GITLAB_PERSONAL_ACCESS_TOKEN`: `<paste-your-token>`
  - `GITLAB_URL`: `https://gitlab.com`

### 3. Verify Setup (1 minute)

```bash
# Check MCP is configured
claude mcp list

# Expected output:
# Configured MCP servers:
# - gitlab (uvx mcp-server-gitlab)
```

### 4. Test It!

In Claude Code:
```
User: "/protoflow:contribute --description \"Add quickstart to README\" --type docs"
```

Expected:
```
✓ Created sandbox: /tmp/claude-contributions/20260204-140532-a7f3b2c1
✓ Cloned repository
✓ Created branch: contrib-20260204-quickstart

Ready to make changes!
```

## Usage

### Interactive Mode (Recommended for First Time)

```
User: "I want to contribute a bug fix"
```

Claude will ask:
1. What's the bug?
2. Related issue number?
3. How to make changes? (guided/manual/suggested)

Then guide you through the entire process.

### Quick Mode (When You Know What You Want)

```
User: "/contribute --description \"Fix S3 timeout\" --type bug-fix --issue 1234"
```

Claude immediately:
1. Creates sandbox
2. Clones repo
3. Creates branch
4. Ready for changes

### Common Commands

```bash
# Start contribution
/protoflow:contribute

# With description
/protoflow:contribute --description "Fix typo in README"

# Specific type
/protoflow:contribute --type docs
/protoflow:contribute --type bug-fix
/protoflow:contribute --type feature

# Link to issue
/protoflow:contribute --issue 1234

# All together
/protoflow:contribute --description "Add tests" --type tests --issue 42
```

## Workflow Steps

### Step 1: Start
```
User: "/contribute --description \"Your contribution\" --type docs"
```

### Step 2: Make Changes
Claude offers three ways:
- **Guided:** You describe, Claude implements, you review
- **Manual:** You edit files directly, Claude assists
- **Suggested:** Claude suggests, you approve, Claude applies

### Step 3: Review
```
User: "Show me the changes"
Claude: [shows git diff with all changes]
```

### Step 4: Commit
```
User: "Looks good, commit it"
Claude: [creates descriptive commit with metadata]
```

### Step 5: Submit
```
User: "Create the merge request"
Claude: [pushes to fork, creates MR on GitLab]
```

### Step 6: Done!
```
✅ Merge Request Created!
MR: !42
URL: https://gitlab.com/protoflow/protoflow/-/merge_requests/42
Status: Open
Pipeline: ✓ Passed

Maintainers notified. You'll get email updates.
```

## Tips

### For Best Results

1. **Be Specific**
   - Good: "Add timeout parameter to S3 upload"
   - Bad: "Fix S3"

2. **Link to Issues**
   - Always include `--issue NUMBER` if one exists
   - Helps maintainers understand context

3. **Test Locally**
   - Before committing, test your changes
   - Run: `make test` or `npm test`

4. **Follow Conventions**
   - Match existing code style
   - Use project's naming conventions
   - Check CONTRIBUTING.md (if exists)

5. **Small Changes**
   - One logical change per MR
   - Easier to review and merge
   - Better than large, multi-purpose MRs

### Contribution Types

Choose the right type:

- `bug-fix` - Fixing broken functionality
- `feature` - New capability or enhancement
- `docs` - Documentation improvements
- `performance` - Speed or efficiency improvements
- `refactor` - Code cleanup without behavior change
- `tests` - Adding or improving tests
- `other` - Anything else (describe in detail)

## Troubleshooting

### "GitLab MCP not found"

```bash
# Verify configuration
claude mcp list

# If not listed, run setup again
claude mcp add
```

### "401 Unauthorized"

```bash
# Check token is set
env | grep GITLAB

# If not set, reconfigure MCP
claude mcp add
```

### "Fork already exists"

Just use it! Claude will detect and use your existing fork.

### "Push failed"

```bash
# Check git credentials
git config --list | grep user

# If not set:
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## Full Documentation

For detailed information:

- **README.md** - Overview and quick reference
- **SETUP.md** - Detailed GitLab MCP setup
- **contribute.md** - Complete skill documentation
- **TESTING.md** - Testing guide
- **IMPLEMENTATION_SUMMARY.md** - Architecture and design

## Getting Help

1. **Check Documentation:** Read files above
2. **Test Handler:** Run `python3 test_handler.py`
3. **Open Issue:** Create issue with `/contribute` label
4. **Contact Maintainer:** @andyhop on GitLab

## Examples

### Example 1: Documentation Fix

```
User: "I want to contribute a typo fix in the README"

Claude: ✓ Creating sandbox...
        ✓ Cloned repository
        ✓ Branch: contrib-20260204-typo-fix

        What's the typo?

User: "Change 'recieve' to 'receive' on line 42"

Claude: ✓ Fixed typo in README.md
        ✓ Running tests... Passed

        Ready to commit? [Y/n]

User: y

Claude: ✓ Committed changes
        ✓ Pushed to fork
        ✓ Created MR: !43

        URL: https://gitlab.com/protoflow/protoflow/-/merge_requests/43
```

### Example 2: Bug Fix with Tests

```
User: "/contribute --description \"Fix S3 timeout\" --type bug-fix --issue 1234"

Claude: ✓ Sandbox created
        ✓ Repository cloned
        ✓ Branch: contrib-20260204-s3-timeout

        How would you like to make changes?
        [1] Guide me through ← recommended
        [2] I'll edit manually
        [3] Suggest changes

User: 1

Claude: Found: hmode/shared/tools/s3publish.py

        Suggested changes:
        1. Add timeout parameter (line 45)
        2. Add exponential backoff (line 67)
        3. Update tests (test_s3publish.py)

        Apply all? [Y/n]

User: y

Claude: ✓ Applied 3 changes
        ✓ Running tests... 45/45 passed

        Review changes? [Y/n]

User: y

Claude: [shows comprehensive diff]

        Commit? [Y/n]

User: y

Claude: ✓ Committed: "Fix S3 upload timeout issue"
        ✓ Pushed to fork
        ✓ Created MR: !44

        Links issue #1234
        Pipeline: ⏳ Running...
```

### Example 3: Feature Addition

```
User: "I want to add a --verbose flag to the CLI tool"

Claude: Great! Let me set up a contribution for that.

        ✓ Sandbox: /tmp/claude-contributions/20260204-140815-c4f9a2b3
        ✓ Repository cloned
        ✓ Branch: contrib-20260204-verbose-flag

        This is a new feature. Should I:
        [1] Add to existing tool (where?)
        [2] Create new functionality
        [3] Show me the current CLI structure first

User: 3

Claude: Current CLI structure:
        - main.py: Entry point
        - cli.py: Click commands
        - utils.py: Helper functions

        Add --verbose to cli.py? [Y/n]

User: y

Claude: ✓ Added --verbose flag to cli.py
        ✓ Added logging configuration
        ✓ Updated help text
        ✓ Added tests
        ✓ Updated documentation

        Test it? [Y/n]

User: y

Claude: Running: python cli.py --verbose
        [shows verbose output]

        Works! Commit? [Y/n]

User: y

Claude: ✓ Committed
        ✓ Pushed
        ✓ MR created: !45

        Feature complete! 🎉
```

## Success Checklist

Before submitting, verify:

- [ ] Changes are tested locally
- [ ] All tests pass
- [ ] Documentation updated (if needed)
- [ ] Commit message is descriptive
- [ ] Related issue linked (if exists)
- [ ] Code follows project style
- [ ] No secrets or sensitive data
- [ ] Changes are focused and atomic

## What Happens Next?

After submitting your MR:

1. **Automated Checks**
   - CI/CD pipeline runs
   - Tests execute
   - Linting validates style
   - Security scans

2. **Review**
   - Maintainers review code
   - May request changes
   - Discussion on approach

3. **Iteration** (if needed)
   - Address feedback
   - Push updates to same branch
   - MR updates automatically

4. **Merge**
   - When approved, maintainer merges
   - Your contribution is live!
   - Sandbox can be cleaned up

## Start Contributing!

You're ready! Try it now:

```
User: "/contribute"
```

Or check out open issues:
https://gitlab.com/protoflow/protoflow/-/issues?label_name=good-first-issue

Happy contributing! 🚀
