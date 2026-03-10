# GitLab MCP Setup for Contributions

<!-- File UUID: 3c7e9f1d-4b8a-4e2f-9d6c-8a5f7b3e4c1d -->

## Quick Setup

### 1. Install GitLab MCP Server

```bash
# The MCP server will be installed via uvx automatically
# No manual installation needed
```

### 2. Configure GitLab MCP

```bash
cd /Users/andyhop/dev/hl-protoflow
claude mcp add
```

When prompted, enter:

```
Server name: gitlab
Command: uvx
Arguments (JSON array): ["mcp-server-gitlab"]

Environment variables:
GITLAB_PERSONAL_ACCESS_TOKEN: <your-token>
GITLAB_URL: https://gitlab.com
```

### 3. Get GitLab Personal Access Token

1. Go to GitLab: https://gitlab.com/-/profile/personal_access_tokens
2. Click "Add new token"
3. Token name: `claude-code-contributions`
4. Expiration: Set as needed (recommend 1 year)
5. Scopes:
   - [x] `api` - Full API access
   - [x] `read_repository` - Read repository contents
   - [x] `write_repository` - Push to repositories

6. Click "Create personal access token"
7. **IMPORTANT:** Copy the token immediately (shown only once)

### 4. Verify Configuration

```bash
claude mcp list
```

Expected output:
```
Configured MCP servers:
- gitlab (uvx mcp-server-gitlab)
```

### 5. Test GitLab MCP

Create a test script to verify:

```bash
cat > /tmp/test-gitlab-mcp.py << 'EOF'
#!/usr/bin/env python3
import os
import sys

# This would be called via Claude Code's MCP integration
# For now, verify environment variable is set
token = os.getenv('GITLAB_PERSONAL_ACCESS_TOKEN')
if not token:
    print("❌ GITLAB_PERSONAL_ACCESS_TOKEN not set")
    sys.exit(1)

print(f"✅ GitLab token configured (length: {len(token)})")
print("✅ Ready to use /contribute skill")
EOF

chmod +x /tmp/test-gitlab-mcp.py
python3 /tmp/test-gitlab-mcp.py
```

## Alternative: Configure via settings.json

If you prefer manual configuration:

Edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "uvx",
      "args": ["mcp-server-gitlab"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "glpat-xxxxxxxxxxxxxxxxxxxx",
        "GITLAB_URL": "https://gitlab.com"
      }
    }
  }
}
```

## Repository Configuration

For the protoflow repository, configure in `.claude/contribute-config.yaml`:

```yaml
# File UUID: 5d9f2c4e-7b3a-4f8e-9c1d-6a4e8f7b2c3e

# GitLab Repository Configuration
repository:
  upstream:
    url: https://gitlab.com/protoflow/protoflow
    namespace: protoflow
    project: protoflow
    default_branch: main
    project_id: 12345678  # Get from GitLab project page

# Contribution Settings
contributions:
  # Auto-detect user's fork or create one
  auto_fork: true

  # Branch naming pattern
  branch_prefix: contrib

  # Require tests before MR
  require_tests: true

  # Auto-assign labels
  auto_labels:
    - contribution
    - needs-review

  # Default reviewers (GitLab usernames)
  default_reviewers:
    - andyhop

  # Merge request template
  mr_template: .gitlab/merge_request_templates/contribution.md

# Sandbox Settings
sandbox:
  base_path: /tmp/claude-contributions
  keep_count: 5
  auto_clean_after_days: 7

# CI/CD Integration
ci:
  wait_for_pipeline: true
  require_passing: false
  show_pipeline_status: true
```

## Troubleshooting

### Issue: MCP server not found

```
Error: gitlab MCP server not found
```

**Solution:**
```bash
# Restart Claude Code after adding MCP server
# Or verify configuration:
cat ~/.claude/settings.json
```

### Issue: Authentication failed

```
Error: 401 Unauthorized
```

**Solution:**
- Verify token has correct scopes
- Check token hasn't expired
- Ensure token is correctly set in environment

```bash
# Test token manually
curl --header "PRIVATE-TOKEN: glpat-xxxxxxxxxxxxxxxxxxxx" \
     "https://gitlab.com/api/v4/user"
```

### Issue: Fork creation failed

```
Error: Cannot create fork - already exists
```

**Solution:**
- Use existing fork
- Or delete old fork via GitLab UI and retry

### Issue: Push rejected

```
Error: remote: GitLab: You are not allowed to push code to this project
```

**Solution:**
- Verify pushing to fork (not upstream)
- Check SSH keys or HTTPS credentials
- Ensure token has `write_repository` scope

## Security Best Practices

### 1. Token Storage

- **NEVER** commit tokens to git
- Store in environment variables only
- Use `.gitignore` to exclude config with tokens

### 2. Token Rotation

- Rotate tokens every 6-12 months
- Revoke tokens after use if temporary
- Use minimal scopes needed

### 3. Sandbox Isolation

- Sandboxes are in `/tmp` (ephemeral)
- Clean up sandboxes regularly
- Don't store sensitive data in sandbox

## Next Steps

After setup, test the contribution workflow:

```
User: "I want to contribute a documentation fix"
```

Claude will:
1. Create sandbox
2. Clone from GitLab
3. Guide through changes
4. Create merge request via MCP

## Additional Resources

- GitLab MCP Server: https://github.com/modelcontextprotocol/servers/tree/main/src/gitlab
- GitLab API Docs: https://docs.gitlab.com/ee/api/
- Personal Access Tokens: https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
