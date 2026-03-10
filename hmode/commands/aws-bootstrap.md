# AWS Bootstrap

Install and configure AWS developer tools for this Claude Code session.

## Instructions

Run the AWS bootstrap tool to install AWS CLI, CDK, Kiro CLI, and configure credentials:

```bash
cd hmode/shared/tools/mcp-cli-wrappers && python -m mcp_cli_wrappers.aws_bootstrap
```

This will:
1. Check/install AWS CLI v2, CDK, Kiro CLI, uv
2. Configure ~/.aws/config and ~/.aws/credentials from environment variables
3. Test AWS connectivity with `aws sts get-caller-identity`
4. Report status

## Environment Variables

The tool detects credentials from:
- `ASSET_DIST_AWS_ACCESS_KEY_ID` / `ASSET_DIST_AWS_ACCESS_KEY_SECRET` (Claude Code web)
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (standard)

## After Bootstrap

Run `/aws-mcp` to configure AWS MCP servers for enhanced Claude Code capabilities.
