# AWS Bootstrap Skill

Install and configure AWS developer tools for Claude Code sessions.

## What This Skill Does

1. **Installs CLI tools:**
   - AWS CLI v2 (includes SSO, `aws s3 cp`)
   - AWS CDK (infrastructure as code)
   - Kiro CLI (AI-assisted AWS development)
   - uv (Python package manager for MCP servers)

2. **Configures AWS credentials:**
   - Creates `~/.aws/config` with profile and region
   - Creates `~/.aws/credentials` from environment variables
   - Supports `ASSET_DIST_AWS_*` (Claude Code web) and standard `AWS_*` vars

3. **Verifies connectivity:**
   - Tests with `aws sts get-caller-identity`
   - Reports account and identity

## Usage

Run the Python tool from `hmode/shared/tools/mcp-cli-wrappers`:

```bash
# Install all tools and configure AWS
python -m mcp_cli_wrappers.aws_bootstrap

# Skip specific tools
python -m mcp_cli_wrappers.aws_bootstrap --no-install-cdk

# JSON output for scripting
python -m mcp_cli_wrappers.aws_bootstrap --format json

# Custom profile name
python -m mcp_cli_wrappers.aws_bootstrap --profile myprofile
```

## Or Use the Slash Command

```
/aws-bootstrap
```

## Tool Location

`hmode/shared/tools/mcp-cli-wrappers/mcp_cli_wrappers/aws_bootstrap.py`

## After Running

Once bootstrap completes, you can:
- Use `aws` CLI commands directly
- Deploy infrastructure with `cdk deploy`
- Use `aws s3 cp` for file uploads
- Run `/aws-mcp` to add AWS MCP servers to Claude Code
