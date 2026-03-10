# Testing the Contribution Skill

<!-- File UUID: 6f9e8c2d-4b3a-4f5e-9d1c-7a4e8f5b2c3d -->

## Prerequisites

Before testing, ensure you have:

1. **GitLab Personal Access Token**
   - Get from: https://gitlab.com/-/profile/personal_access_tokens
   - Required scopes: `api`, `read_repository`, `write_repository`

2. **GitLab MCP Configured**
   - Run: `claude mcp list`
   - Should show: `gitlab (uvx mcp-server-gitlab)`

3. **Test Repository Access**
   - Verify you can access: https://gitlab.com/protoflow/protoflow
   - Or use a different test repository

## Unit Testing

### Test 1: Handler Script

Test the Python handler in isolation:

```bash
cd /Users/andyhop/dev/hl-protoflow/hmode/skills/contribute
python3 test_handler.py
```

Expected output:
```
Test 1: Interactive mode
------------------------------------------------------------
Exit code: 0
Output:
{
  "status": "ready",
  "sandbox": "/tmp/claude-contributions/20260204-140532-a7f3b2c1",
  "branch": "contrib-20260204-contribution",
  "next_steps": [...]
}

✅ Handler test passed!
```

### Test 2: Configuration Loading

Test that config loads correctly:

```bash
python3 -c "
from handler import ContributionWorkflow
import json

workflow = ContributionWorkflow({})
print(json.dumps(workflow.config, indent=2))
"
```

Expected output:
```json
{
  "repository": {
    "upstream": {
      "url": "https://gitlab.com/protoflow/protoflow",
      "namespace": "protoflow",
      "project": "protoflow",
      "default_branch": "main"
    }
  },
  ...
}
```

### Test 3: Sandbox Creation

Test sandbox creation without cloning:

```bash
python3 -c "
from handler import ContributionWorkflow
from pathlib import Path

workflow = ContributionWorkflow({})
sandbox = workflow._create_sandbox()
print(f'Created sandbox: {sandbox}')
assert sandbox.exists(), 'Sandbox not created'
print('✅ Sandbox creation works')
"
```

## Integration Testing

### Test 4: Skill Invocation

Test the skill through Claude Code:

In Claude Code chat:
```
User: "/contribute --description \"Test contribution\" --type docs"
```

Expected behavior:
1. Claude invokes the skill
2. Sandbox is created
3. Repository is cloned
4. Branch is created
5. Claude provides next steps

### Test 5: Interactive Mode

Test interactive contribution flow:

In Claude Code chat:
```
User: "I want to contribute a documentation fix"
```

Expected behavior:
1. Claude detects contribution intent
2. Asks for contribution type
3. Asks for description
4. Creates sandbox
5. Guides through changes

### Test 6: Manual Changes

Test manual editing workflow:

```
User: "/contribute --type docs"

Claude: [creates sandbox]

User: "I'll make changes manually"

Claude: [provides instructions, pauses]

[User edits files in /tmp/claude-contributions/...]

User: "I'm ready to commit"

Claude: [shows diff, commits, pushes, creates MR]
```

## End-to-End Testing

### Test 7: Complete Contribution

Full workflow test:

1. **Start contribution**
   ```
   User: "/contribute --description \"Add example to README\" --type docs"
   ```

2. **Make changes**
   ```
   User: "Add a quickstart example to the README"
   Claude: [implements change]
   ```

3. **Review**
   ```
   User: "Show me the diff"
   Claude: [shows git diff]
   ```

4. **Commit**
   ```
   User: "Looks good, commit it"
   Claude: [creates commit]
   ```

5. **Push and MR**
   ```
   User: "Create the merge request"
   Claude: [pushes to fork, creates MR via GitLab MCP]
   ```

Expected result:
- MR created on GitLab
- URL provided
- Pipeline status shown

### Test 8: Error Handling

Test error scenarios:

**Scenario A: No GitLab MCP**
```bash
# Temporarily remove MCP config
mv ~/.claude/settings.json ~/.claude/settings.json.bak

# Try contribution
User: "/contribute"

Expected: Error message with setup instructions

# Restore config
mv ~/.claude/settings.json.bak ~/.claude/settings.json
```

**Scenario B: Invalid Repository**
```
User: "/contribute --repo \"https://gitlab.com/invalid/repo\""

Expected: Error message with troubleshooting steps
```

**Scenario C: Authentication Failure**
```bash
# Set invalid token
export GITLAB_PERSONAL_ACCESS_TOKEN="invalid"

User: "/contribute"

Expected: 401 error with token troubleshooting steps
```

## Manual Verification

### Verify Sandbox Creation

```bash
ls -la /tmp/claude-contributions/
```

Should show timestamped directories like:
```
drwxr-xr-x  20260204-140532-a7f3b2c1
drwxr-xr-x  20260204-141022-b3e8f9a2
```

### Verify Git Setup

```bash
cd /tmp/claude-contributions/20260204-140532-a7f3b2c1
git status
git log --oneline -5
git remote -v
```

Expected:
- Clean working directory (or uncommitted changes if in progress)
- Contribution branch checked out
- Commits from workflow
- Origin pointing to GitLab

### Verify Fork Creation

Check GitLab:
1. Go to https://gitlab.com/[your-username]
2. Check for fork of `protoflow`
3. Verify branch exists

### Verify Merge Request

Check GitLab:
1. Go to https://gitlab.com/protoflow/protoflow/-/merge_requests
2. Find your MR
3. Verify:
   - Title and description are correct
   - Labels are applied
   - Source/target branches are correct
   - Pipeline is running/passed

## Performance Testing

### Test 9: Multiple Sandboxes

Create multiple sandboxes to test concurrent usage:

```bash
for i in {1..5}; do
  /contribute --description "Test $i" --type docs &
done
wait
```

Verify:
- All sandboxes created successfully
- No conflicts or race conditions
- Each sandbox is isolated

### Test 10: Large Repository

Test with larger repository:

```
User: "/contribute --repo \"https://gitlab.com/large/repository\""
```

Monitor:
- Clone time
- Disk space usage
- Memory usage

## Cleanup Testing

### Test 11: Sandbox Cleanup

Test cleanup after completion:

```
User: "Clean up my contribution sandboxes"

Claude: Found 3 sandboxes:
[1] 20260204-140532-a7f3b2c1 (contrib-test)
[2] 20260203-091245-d4e8f9a2 (contrib-docs)
[3] 20260202-153412-e7f9c3d4 (contrib-feature)

Select [1-3] or 'all':

User: all

Claude: ✓ Cleaned up 3 sandboxes
```

Verify:
```bash
ls -la /tmp/claude-contributions/
# Should be empty
```

## Test Checklist

Use this checklist to verify all functionality:

- [ ] Handler script executes without errors
- [ ] Configuration loads correctly
- [ ] Sandbox creation works
- [ ] Repository cloning succeeds
- [ ] Branch creation works
- [ ] GitLab MCP is accessible
- [ ] Fork creation works
- [ ] Changes can be committed
- [ ] Push to fork succeeds
- [ ] MR creation succeeds
- [ ] MR has correct metadata
- [ ] Pipeline triggers correctly
- [ ] Error messages are helpful
- [ ] Cleanup works correctly
- [ ] Multiple sandboxes are isolated
- [ ] Interactive mode works
- [ ] Quick mode (with args) works
- [ ] Manual editing mode works
- [ ] Guided mode works

## Troubleshooting Tests

If tests fail, check:

1. **GitLab MCP**
   ```bash
   claude mcp list
   echo $GITLAB_PERSONAL_ACCESS_TOKEN
   ```

2. **Network Connectivity**
   ```bash
   curl -I https://gitlab.com
   ```

3. **Git Configuration**
   ```bash
   git config --list | grep user
   ```

4. **Permissions**
   ```bash
   ls -la /tmp/claude-contributions/
   ```

5. **Python Dependencies**
   ```bash
   python3 -c "import yaml; print('✓ yaml')"
   python3 -c "import subprocess; print('✓ subprocess')"
   ```

## Automated Test Suite

For CI/CD, create automated tests:

```bash
#!/bin/bash
# test-contribute.sh

echo "Running contribution skill tests..."

# Test 1: Handler
python3 test_handler.py || exit 1

# Test 2: Config
python3 -c "from handler import ContributionWorkflow; ContributionWorkflow({})" || exit 1

# Test 3: Sandbox
python3 -c "
from handler import ContributionWorkflow
workflow = ContributionWorkflow({})
sandbox = workflow._create_sandbox()
assert sandbox.exists()
" || exit 1

echo "✅ All tests passed!"
```

Make executable and run:
```bash
chmod +x test-contribute.sh
./test-contribute.sh
```

## Test Results

Document test results:

```markdown
## Test Session: 2026-02-04

**Environment:**
- Claude Code: Web
- GitLab MCP: v1.0.0
- Python: 3.13

**Results:**
- Unit tests: ✅ Passed (3/3)
- Integration tests: ✅ Passed (3/3)
- End-to-end tests: ✅ Passed (2/2)
- Error handling: ✅ Passed (3/3)
- Performance: ✅ Passed (2/2)
- Cleanup: ✅ Passed (1/1)

**Total: 14/14 tests passed**

**Notes:**
- All functionality working as expected
- No issues with sandbox isolation
- GitLab MCP integration smooth
```

## Next Steps

After testing:

1. **Update Documentation**
   - Add any discovered limitations
   - Document workarounds
   - Add FAQs

2. **Create Examples**
   - Real contribution examples
   - Video tutorials
   - Screenshots

3. **User Feedback**
   - Collect feedback from test users
   - Iterate on UX
   - Add requested features
