# AWS MCP Skill

Configure AWS MCP servers for Claude Code from awslabs/mcp.

## Available Servers

| # | Server | Description |
|---|--------|-------------|
| 1 | aws-knowledge | Real-time AWS docs, API refs (AWS-hosted remote) |
| 2 | aws-docs | Offline documentation search |
| 3 | aws-iac | CDK/CloudFormation validation, cfn-lint, cfn-guard |
| 4 | aws-diagram | Architecture diagram generation (requires GraphViz) |
| 5 | ecs | Container deployment, ECR, load balancers |
| 6 | lambda-tool | Execute Lambda functions as AI tools |
| 7 | sns-sqs | SNS/SQS messaging |
| 8 | cloudwatch | Logs, metrics, alarms analysis |

## Usage

Run the Python tool from `hmode/shared/tools/mcp-cli-wrappers`:

```bash
# List available servers
python -m mcp_cli_wrappers.aws_mcp --list

# Interactive selection
python -m mcp_cli_wrappers.aws_mcp --interactive

# Install specific servers
python -m mcp_cli_wrappers.aws_mcp --install aws-docs --install aws-iac

# Install all servers
python -m mcp_cli_wrappers.aws_mcp --all

# JSON output
python -m mcp_cli_wrappers.aws_mcp --list --format json
```

## Or Use the Slash Command

```
/aws-mcp
```

## Tool Location

`hmode/shared/tools/mcp-cli-wrappers/mcp_cli_wrappers/aws_mcp.py`

## Prerequisites

- **uv**: Required for all servers (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **GraphViz**: Required for aws-diagram (`apt install graphviz`)
- **AWS credentials**: Required for ecs, lambda-tool, sns-sqs, cloudwatch

Run `/aws-bootstrap` first to install prerequisites.

## Installation Methods

1. **claude-cli** (preferred): Uses `claude mcp add` command
2. **settings**: Directly edits `~/.claude/settings.json`

The tool auto-detects which method to use.

## After Installation

Restart Claude Code to activate MCP servers. Then use tools like:
- `mcp__aws-docs__search_documentation("Lambda")`
- `mcp__aws-iac__validate_template(template)`
- `mcp__cloudwatch__get_active_alarms()`

## Sources

- https://github.com/awslabs/mcp
- https://docs.aws.amazon.com/aws-mcp/latest/userguide/what-is-mcp-server.html
