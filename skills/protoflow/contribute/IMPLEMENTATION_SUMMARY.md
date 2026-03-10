# Contribution Skill - Implementation Summary

<!-- File UUID: 8d7f9c2e-4b3a-4f5e-9d1c-6a7e8f4b3c2d -->

## What Was Created

### Core Files

```
hmode/skills/contribute/
├── contribute.md                    # Full skill documentation (465 lines)
├── skill.json                       # Skill metadata for Claude Code
├── handler.py                       # Python execution handler
├── contribute-config.yaml           # Configuration file
├── README.md                        # Quick reference guide
├── SETUP.md                         # GitLab MCP setup instructions
├── TESTING.md                       # Testing guide
├── IMPLEMENTATION_SUMMARY.md        # This file
├── test_handler.py                  # Unit test script
└── .gitignore                       # Protect user configs
```

### Features Implemented

#### 1. Sandbox Management
- **Isolated Workspaces:** Each contribution in separate `/tmp/claude-contributions/` directory
- **Automatic Cleanup:** Configurable retention (5 sandboxes, 7 days)
- **Resume Support:** Return to previous contribution sandboxes

#### 2. GitLab Integration
- **Repository Cloning:** Automatic clone from GitLab
- **Fork Creation:** Auto-create fork via GitLab MCP
- **Branch Management:** Automatic branch naming: `contrib-YYYYMMDD-topic`
- **Merge Request Creation:** Full MR creation with templates and metadata

#### 3. Workflow Modes
- **Interactive Mode:** Step-by-step guided workflow
- **Quick Mode:** Pre-configured contributions with arguments
- **Manual Mode:** Pause for external editing
- **Guided Mode:** Claude implements with user approval
- **Suggested Mode:** Claude suggests, user reviews

#### 4. Error Handling
- Authentication failures (401)
- Repository not found (404)
- Permission errors (403)
- Fork conflicts
- Push failures
- MR creation errors

#### 5. Configuration
- Customizable repository settings
- User preferences
- Sandbox settings
- CI/CD integration
- Auto-labels and reviewers

## Quick Start

### Step 1: Setup GitLab MCP

```bash
cd /Users/andyhop/dev/hl-protoflow/hmode/skills/contribute
cat SETUP.md
```

Follow instructions to:
1. Get GitLab personal access token
2. Configure GitLab MCP server: `claude mcp add`
3. Verify: `claude mcp list`

### Step 2: Test the Skill

```bash
# Unit test
python3 test_handler.py

# Integration test
# In Claude Code:
"/contribute --description \"Test\" --type docs"
```

### Step 3: Make Your First Contribution

In Claude Code:
```
User: "I want to contribute a documentation improvement"
```

Claude will guide you through the entire process.

## Usage Examples

### Basic Usage (Interactive)

```
User: "/contribute"
```

Claude asks:
1. What type? (bug-fix, feature, docs, etc.)
2. Title and description?
3. Related issue?

Then creates sandbox, clones repo, and guides through changes.

### Quick Usage (With Arguments)

```
User: "/contribute --description \"Fix timeout\" --type bug-fix --issue 1234"
```

Claude immediately:
1. Creates sandbox
2. Clones repository
3. Creates branch
4. Ready for changes

### Resume Previous Contribution

```
User: "Resume my contribution from yesterday"
```

Claude shows active sandboxes and lets you select.

## Architecture

### Workflow Flow

```
User Request
    ↓
Skill Invocation (/contribute)
    ↓
handler.py Execution
    ↓
Create Sandbox (/tmp/claude-contributions/YYYYMMDD-HHMMSS-uuid)
    ↓
Clone Repository (from GitLab)
    ↓
Create Branch (contrib-YYYYMMDD-topic)
    ↓
Make Changes (guided/manual/suggested)
    ↓
Review Changes (git diff)
    ↓
Commit (with metadata)
    ↓
Check/Create Fork (via GitLab MCP)
    ↓
Push to Fork (git push)
    ↓
Create Merge Request (via GitLab MCP)
    ↓
Display MR URL and Status
```

### Technology Stack

- **Language:** Python 3.13+
- **Git Operations:** subprocess + git commands
- **GitLab API:** GitLab MCP (uvx mcp-server-gitlab)
- **Configuration:** YAML
- **Sandbox:** `/tmp` directory

### GitLab MCP Integration Points

```python
# Fork creation
mcp.gitlab.forkProject({
  project_id: upstream_id,
  namespace: user_namespace
})

# MR creation
mcp.gitlab.createMergeRequest({
  source_project_id: fork_id,
  target_project_id: upstream_id,
  source_branch: branch_name,
  target_branch: "main",
  title: title,
  description: description,
  labels: ["contribution", "needs-review"]
})

# Pipeline status
mcp.gitlab.getPipelineStatus({
  project_id: fork_id,
  ref: branch_name
})
```

## Configuration Options

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
  auto_fork: true
  branch_prefix: contrib
  require_tests: true
  auto_labels:
    - contribution
    - needs-review
  default_reviewers:
    - andyhop
```

### Sandbox Settings

```yaml
sandbox:
  base_path: /tmp/claude-contributions
  keep_count: 5
  auto_clean_after_days: 7
```

## Testing

### Quick Test

```bash
cd /Users/andyhop/dev/hl-protoflow/hmode/skills/contribute
python3 test_handler.py
```

### Full Test Suite

See `TESTING.md` for comprehensive testing instructions:
- Unit tests
- Integration tests
- End-to-end tests
- Error handling tests
- Performance tests
- Cleanup tests

## Security Considerations

### Token Management
- Tokens stored in environment variables only
- Never committed to git
- `.gitignore` protects sensitive files

### Sandbox Isolation
- Each contribution in isolated directory
- Sandboxes in `/tmp` (ephemeral)
- Auto-cleanup prevents accumulation

### Code Review
- All contributions reviewed by maintainers
- CI/CD validation
- Security scanning on MRs

## Troubleshooting

### Common Issues

**Issue 1: GitLab MCP Not Found**
```
Error: gitlab MCP server not found

Solution:
1. Run: claude mcp add
2. Configure GitLab MCP (see SETUP.md)
3. Restart Claude Code
```

**Issue 2: Authentication Failed**
```
Error: 401 Unauthorized

Solution:
1. Check token: echo $GITLAB_PERSONAL_ACCESS_TOKEN
2. Verify scopes: api, read_repository, write_repository
3. Check expiration
```

**Issue 3: Fork Already Exists**
```
Error: Fork already exists

Solution:
1. Use existing fork
2. Or delete via GitLab UI: gitlab.com/[user]/protoflow
```

**Issue 4: Push Failed**
```
Error: Push rejected

Solution:
1. Verify git credentials
2. Check token has write_repository scope
3. Ensure pushing to fork (not upstream)
```

See `SETUP.md` for detailed troubleshooting.

## Next Steps

### For Repository Maintainers

1. **Set Up GitLab MCP**
   ```bash
   cd hmode/skills/contribute
   cat SETUP.md
   ```

2. **Test the Workflow**
   ```bash
   python3 test_handler.py
   ```

3. **Customize Configuration**
   ```bash
   vim contribute-config.yaml
   # Update reviewers, labels, etc.
   ```

4. **Document Repository-Specific Steps**
   - Add to CONTRIBUTING.md
   - Create `.gitlab/merge_request_templates/`
   - Set up CI/CD pipeline

### For Contributors

1. **Request Access**
   - Get GitLab personal access token
   - Contact maintainer for setup help

2. **Run Contribution**
   ```
   In Claude Code: "/contribute"
   ```

3. **Follow Guidance**
   - Claude guides through entire process
   - Make changes as instructed
   - Review before submitting

4. **Respond to Feedback**
   - Watch for MR comments
   - Address review feedback
   - Update as needed

## Benefits

### For Contributors
- ✅ No need to manually fork, clone, or configure git
- ✅ Guided workflow reduces friction
- ✅ Isolated sandboxes prevent conflicts
- ✅ Automatic MR creation with templates
- ✅ CI/CD integration shows status

### For Maintainers
- ✅ Consistent contribution format
- ✅ Proper metadata (labels, reviewers, issue links)
- ✅ Less time answering setup questions
- ✅ Better quality contributions (tests, docs)
- ✅ Automated pipeline validation

### For the Project
- ✅ Lower barrier to entry for contributions
- ✅ More external contributions
- ✅ Better code quality
- ✅ Faster review process
- ✅ Transparent workflow

## Metrics & Success Criteria

Track these metrics to measure success:

- **Contribution Rate:** Number of external MRs per month
- **Time to First Contribution:** Days from signup to first MR
- **MR Quality:** % of MRs passing CI on first try
- **Review Time:** Average time from MR to merge
- **Contributor Retention:** % of contributors making 2+ MRs

## Future Enhancements

Potential improvements:

1. **Multi-Repository Support**
   - Contribute to any GitLab repo
   - Repository templates
   - Cross-project contributions

2. **Advanced Git Operations**
   - Rebase support
   - Cherry-pick commits
   - Squash before MR

3. **Enhanced Testing**
   - Pre-commit hooks
   - Automatic test generation
   - Coverage reports

4. **AI-Powered Assistance**
   - Auto-suggest improvements
   - Code review assistant
   - Documentation generation

5. **GitHub Support**
   - Parallel GitHub MCP integration
   - Unified contribution workflow
   - Cross-platform compatibility

## Version History

- **1.0.0** (2026-02-04)
  - Initial implementation
  - GitLab MCP integration
  - Sandbox management
  - Guided workflow
  - MR automation
  - Error handling
  - Configuration system
  - Testing suite

## Support & Feedback

For questions, issues, or feedback:

1. **Documentation:** Check README.md, SETUP.md, TESTING.md
2. **Issues:** Open issue on GitLab with `/contribute` label
3. **Maintainers:** Contact @andyhop
4. **Improvements:** Use this skill to contribute! 🎉

## Summary

You now have a complete external contribution workflow that:

✅ Creates isolated sandboxes for each contribution
✅ Integrates with GitLab via MCP
✅ Guides users through changes
✅ Automates fork creation and MR submission
✅ Handles errors gracefully
✅ Configurable for different projects
✅ Tested and documented

**Ready to accept contributions!**

To get started:
1. Read `SETUP.md` for GitLab MCP configuration
2. Run `python3 test_handler.py` to test
3. Try `/contribute` in Claude Code
4. Share with potential contributors!
