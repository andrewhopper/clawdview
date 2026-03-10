# GitLab MCP Server Setup and Usage Guidelines

<!-- File UUID: 8e3f9a2b-5c7d-4e1a-9b8f-6d4c2a1e0f3b -->

## Important Authentication Note

If you already have this setup but see authentication issues for GitLab operations:

**Refresh Midway token and run:**
```bash
curl -L -b ~/.midway/cookie -c ~/.midway/cookie "https://gitlab.aws.dev/api/v4/projects/" --header "Authorization: Bearer <personal_gitlab_token>"
```

## 1.0 Overview

The GitLab MCP (Model Context Protocol) server enables AI assistants to interact with GitLab repositories, issues, merge requests, and other GitLab resources through a standardized interface. This guide covers enterprise-level setup and usage patterns for teams already using the Amazon Internal MCP Server.

## 2.0 Prerequisites

- Amazon Internal MCP Server already installed and configured (recommended: https://w.amazon.com/bin/view/Amazon-Internal-MCP-Server)
- Node.js 18+ installed
- GitLab instance access (https://gitlab.aws.dev/)
- GitLab Personal Access Token with appropriate permissions

## 3.0 Installation

### 3.1 Install GitLab MCP Server

```bash
npm install -g @zereight/mcp-gitlab
```

### 3.2 GitLab Personal Access Token Setup

**Steps to create token:**

1. Go to GitLab → User Settings → Access Tokens: https://gitlab.aws.dev/-/user_settings/personal_access_tokens
2. Create new token with required scopes
3. Copy the token (you won't see it again)

**Required Token Scopes:**

- `api` - Full API access
- `read_user` - Read user information
- `read_repository` - Read repository content
- `write_repository` - Write repository content (for file operations)

### 3.3 MCP Client Configuration

Update your existing MCP configuration file to include the GitLab server alongside your Amazon Internal MCP Server.

**For Q CLI (~/.aws/amazonq/mcp.json):**

```json
{
  "mcpServers": {
    "amazon-internal-mcp-server": {
      // your existing internal amazon mcp server
    },
    "GitLab communication server": {
      "command": "npx",
      "args": ["-y", "@zereight/mcp-gitlab"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "<your personal gitlab access token>",
        "GITLAB_API_URL": "https://gitlab.aws.dev/api/v4",
        "GITLAB_READ_ONLY_MODE": "false",
        "USE_GITLAB_WIKI": "false",
        "USE_MILESTONE": "false",
        "USE_PIPELINE": "false",
        "GITLAB_AUTH_COOKIE_PATH": "~/.midway/cookie"
      }
    }
  }
}
```

**Note:** Enterprise-level GitLab requires BOTH auth cookie AND personal access token to communicate with GitLab.

**For Claude Code (~/.claude/settings.json):**

```json
{
  "mcpServers": {
    "aws-gitlab": {
      "command": "npx",
      "args": ["-y", "@zereight/mcp-gitlab"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "${GITLAB_TOKEN}",
        "GITLAB_API_URL": "https://gitlab.aws.dev/api/v4",
        "GITLAB_READ_ONLY_MODE": "false",
        "USE_GITLAB_WIKI": "false",
        "USE_MILESTONE": "false",
        "USE_PIPELINE": "false",
        "GITLAB_AUTH_COOKIE_PATH": "~/.midway/cookie"
      }
    }
  }
}
```

## 4.0 Available GitLab MCP Tools

This MCP tool provides operations for:

- Repository Management
- File Operations
- Branch Management
- Issues Management
- Merge Request Operations
- Code Review Operations

**Full list:** https://github.com/zereight/gitlab-mcp?tab=readme-ov-file#tools-%EF%B8%8F

## 5.0 Important Gotchas for Code Review with GitLab MCP

### 5.1 Critical Security & Control Considerations

⚠️ **NEVER auto-approve merge request operations!** Always maintain human oversight for critical actions.

### 5.2 MCP Configuration - Be Selective with Auto-Approve

**Note:** Q CLI doesn't currently support auto-approve section (open request: https://github.com/aws/amazon-q-developer-cli/issues/1938)

**Recommended Alias for Q CLI:**

Create an alias with read tools and draft note actions only (prevents accidental comments on MRs):

```bash
# For Q CLI (uses "GitLab communication server" name)
alias qgitlab='q chat --trust-tools="git_lab_communication_server___get_file_contents,git_lab_communication_server___search_repositories,git_lab_communication_server___get_project,git_lab_communication_server___list_projects,git_lab_communication_server___get_repository_tree,git_lab_communication_server___list_issues,git_lab_communication_server___get_issue,git_lab_communication_server___list_issue_discussions,git_lab_communication_server___list_merge_requests,git_lab_communication_server___get_merge_request,git_lab_communication_server___get_merge_request_diffs,git_lab_communication_server___list_merge_request_diffs,git_lab_communication_server___mr_discussions,git_lab_communication_server___list_draft_notes,git_lab_communication_server___create_draft_note,git_lab_communication_server___update_draft_note,git_lab_communication_server___delete_draft_note,git_lab_communication_server___get_users,git_lab_communication_server___list_namespaces,git_lab_communication_server___get_namespace,git_lab_communication_server___verify_namespace"'
```

**Note for Claude Code:** If using server name "aws-gitlab", tool names will be prefixed with `aws_gitlab___` instead of `git_lab_communication_server___`.

### 5.3 Code Review Workflow - Human-in-the-Loop Approach

#### ❌ DON'T DO THIS:

```
"Review this merge request and approve it if it looks good"
"Auto-merge this MR after running tests"
"Create and immediately merge this hotfix"
```

#### ✅ DO THIS INSTEAD:

```
"Review merge request #123 and provide detailed feedback on potential issues"
"Create draft comments highlighting security concerns in this authentication code"
"Analyze the code changes and suggest improvements, but don't take any actions yet"
```

### 5.4 Effective Code Review Prompts

#### For Initial Review:

```
Analyze merge request #456 in project myorg/backend-service and provide:
1. Security vulnerabilities or concerns
2. Code quality issues (performance, maintainability)
3. Missing test coverage areas
4. Documentation gaps
5. Compliance with team coding standards
Do NOT approve or merge - just provide analysis.
```

#### For Detailed Code Analysis:

```
Review the authentication changes in MR #789 and check for:
- Input validation issues
- SQL injection vulnerabilities
- Proper error handling
- Logging of sensitive data
- Rate limiting implementation
Create draft comments for each issue found, but don't publish them yet.
```

#### For Test Coverage Review:

```
Examine the test files in MR #321 and identify:
- Missing unit test cases
- Integration test gaps
- Edge cases not covered
- Mock/stub usage issues
Suggest specific test cases to add.
```

### 5.5 Multi-Stage Review Process

#### Stage 1: Automated Analysis

```
Perform initial code review of MR #123 focusing on:
- Code structure and organization
- Potential bugs or logic errors
- Performance implications
- Security considerations
Provide summary but take no actions.
```

#### Stage 2: Human Review & Decision

1. Review AI analysis
2. Make manual decisions
3. Add your own comments
4. Decide on approval/rejection

#### Stage 3: Controlled Actions

```
Based on my review, create these specific draft comments:
1. Line 45 in auth.py: 'Consider adding input validation here'
2. Line 78 in database.py: 'This query might be vulnerable to SQL injection'
3. Line 120 in api.py: 'Add error handling for this API call'
Do not publish these comments yet - save as drafts.
```

### 5.6 Branch Protection & Approval Rules

**Configure GitLab Project Settings:**

- Require manual approvals for merge requests
- Enable branch protection for main/master
- Set up required status checks
- Disable auto-merge capabilities

**Verify Protection Settings:**

```
Check the branch protection rules for the main branch in project myorg/critical-service and show me:
- Required approvers count
- Status check requirements
- Auto-merge settings
- Push restrictions
```

### 5.7 Dangerous Operations - Always Manual

**Never auto-approve these operations:**

- `create_merge_request` with auto-merge enabled
- `update_merge_request` with state changes
- `push_files` to protected branches
- `delete_*` operations
- `create_branch` from protected branches
- Any operation with force parameters

### 5.8 Safe Review Patterns

#### Information Gathering (Safe):

```
"Show me all open MRs assigned to my team with their current status"
"List recent commits in the feature/auth-update branch"
"Get the diff for merge request #456 and highlight the database changes"
```

#### Analysis & Feedback (Safe):

```
"Analyze the performance impact of the database changes in MR #789"
"Review the API documentation updates and suggest improvements"
"Check if the new endpoints follow our REST API conventions"
```

#### Controlled Actions (Manual Approval Required):

```
"Create a draft comment on line 67 of auth.py suggesting to use bcrypt instead of MD5"
"Prepare a summary comment for MR #123 with my review findings"
"Draft a response to the developer's question about the caching implementation"
```

### 5.9 Team Collaboration Guidelines

#### For Team Leads:

- Set up clear auto-approve policies
- Train team on safe MCP usage
- Regular audit of MCP actions
- Establish escalation procedures

#### For Developers:

- Always review AI suggestions before acting
- Use draft comments for collaboration
- Verify changes in staging before production
- Document decisions and rationale

### 5.10 Monitoring & Auditing

#### Regular Checks:

```
"Show me all merge requests I've interacted with in the last week"
"List any auto-approved actions from the MCP server"
"Check recent API calls made through the GitLab MCP integration"
```

#### Audit Trail:

- Monitor GitLab audit logs
- Track MCP server actions
- Review approval patterns
- Identify unusual activities

## 6.0 Troubleshooting

### 6.1 Common Issues

#### 1. MCP Server Not Starting:

- Check Node.js version (18+ required)
- Verify environment variables are set
- Check MCP configuration syntax

#### 2. Getting 404 Not Found Every Next Day:

Refresh Midway and run this curl command:

```bash
curl -L -b ~/.midway/cookie -c ~/.midway/cookie "https://gitlab.aws.dev/api/v4/projects/" --header "Authorization: Bearer <replace with your gitlab token>"
```

## 7.0 Advanced Usage

### 7.1 Combining with Amazon Internal Tools

Combine GitLab operations with Amazon internal tools:

**Example Workflow:**

1. Search internal documentation using Amazon MCP
2. Create GitLab issue based on findings
3. Create merge request with fixes
4. Update internal wiki with resolution

**Suggested Prompt:**

```
Search the internal wiki for authentication best practices, then create a GitLab issue to implement these practices in our user service repository
```

### 7.2 CI/CD Integration

Use GitLab MCP with CI/CD workflows:

**Suggested Prompts:**

```
"Review the .gitlab-ci.yml file and suggest improvements for our deployment pipeline"

"Create a merge request to update our CI configuration with the latest security scanning tools"

"Check the status of all recent pipeline runs and identify any failing tests"
```

## 8.0 Related Documentation

- MCP Configuration: `SETUP.md` (Section 10.4)
- CI/CD Testing: `hmode/shared/standards/testing/CICD_TESTING_GUIDE.md`
- Code Standards: `hmode/shared/standards/code/`
