# AWS MCP Configuration

Configure AWS MCP servers for Claude Code from awslabs/mcp.

## Instructions

Run the AWS MCP tool to list and install MCP servers:

```bash
cd hmode/shared/tools/mcp-cli-wrappers && python -m mcp_cli_wrappers.aws_mcp --interactive
```

## Available Servers

| Server | Description |
|--------|-------------|
| aws-knowledge | Real-time AWS docs (AWS-hosted) |
| aws-docs | Offline doc search |
| aws-iac | CDK/CFN validation |
| aws-diagram | Architecture diagrams |
| ecs | Container deployment |
| lambda-tool | Lambda as AI tools |
| sns-sqs | Messaging queues |
| cloudwatch | Logs/metrics/alarms |

## Quick Commands

```bash
# List all servers
python -m mcp_cli_wrappers.aws_mcp --list

# Install specific servers
python -m mcp_cli_wrappers.aws_mcp --install aws-docs --install aws-iac

# Install all
python -m mcp_cli_wrappers.aws_mcp --all
```

## Prerequisites

Run `/aws-bootstrap` first to install uv and configure AWS credentials.

## After Installation

Restart Claude Code to activate MCP servers.
