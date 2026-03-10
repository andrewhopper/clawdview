# Coding Session Domain Model

**Version:** 1.0.0
**Status:** Production
**Created:** 2025-12-19
**Dependencies:** core@^1.0.0, auth@^1.0.0, infrastructure@^1.0.0

## Overview

The **coding-session** domain model defines the structure for interactive coding sessions with ephemeral compute, terminals, and AI assistants. This domain powers the GoCoder CLI application and similar cloud-based development environments.

## Purpose

Enable users to:
1. Create and manage isolated coding environments with configurable compute resources
2. Interact with multiple terminal sessions within a coding environment
3. Collaborate via shareable session links
4. Authenticate git operations with SSH keys
5. Automate session management via API keys
6. Track resource usage and costs

## Core Entities

### CodingSession
The main entity representing a complete coding environment with:
- **Compute resources** (ECS, EC2, Firecracker, Lambda)
- **Development environment** (Docker image, env vars, git repo)
- **AI assistant** (Claude Code, Aider, Copilot, etc.)
- **Terminals** (multiple interactive shells)
- **Lifecycle management** (creation, idle timeout, termination)

### Terminal
Individual terminal sessions within a coding session:
- **PTY/shell access** via WebSocket, MQTT, or SSH
- **Resize support** for responsive terminals
- **Reconnection** handling for network interruptions

### ComputeConfig
Resource allocation configuration:
- **Type**: ECS Fargate, EC2, Firecracker micro-VMs
- **Size**: small (1 vCPU), medium (2 vCPU), large (4 vCPU), GPU
- **Region**: Compute region for latency optimization

### EnvironmentConfig
Development environment setup:
- **Base image**: Docker image or VM template
- **Git repository**: Auto-clone on startup
- **Environment variables**: Runtime configuration
- **Secrets**: AWS Secrets Manager references
- **Startup scripts**: Custom initialization

### AIAssistantConfig
AI coding assistant configuration:
- **Providers**: Claude Code, Aider, GitHub Copilot, Cursor
- **Model selection**: claude-3-5-sonnet, gpt-4, etc.
- **API key management**: Secure credential storage

### SSHKey
User SSH keys for git authentication:
- **Public key storage** for git servers
- **Private key** stored in AWS Secrets Manager
- **Fingerprint** for key identification

### APIKey
Programmatic access credentials:
- **Scoped permissions** (session:create, session:read, etc.)
- **Key rotation** support
- **Usage tracking** for audit trails

### ShareLink
Collaboration links for session sharing:
- **Permissions**: view, interact, edit, admin
- **Expiration**: Time-based or usage-based limits
- **Revocation**: Instant link invalidation

## Lifecycle

### Session Creation
```
CreateCodingSession → Provision Compute → Clone Git Repo → Create Default Terminal → Active
```

### Session Usage
```
Active → User Interaction → Update lastActivityAt → (timeout check) → Idle or Active
```

### Session Termination
```
TerminateSession → Cleanup Terminals → Release Compute → Stopped
```

## Key Actions

1. **CreateCodingSession** - Provision a new coding environment
2. **AttachToSession** - Connect to an existing session
3. **TerminateSession** - Release resources and stop session
4. **CreateTerminal** - Add a new terminal to a session
5. **CreateShareLink** - Generate collaboration link
6. **CreateAPIKey** - Issue programmatic access credentials

## Relationships

```
User (auth) ──1:N──> CodingSession
CodingSession ──1:N──> Terminal
CodingSession ──1:N──> ShareLink
CodingSession ──1:1──> ComputeConfig
CodingSession ──1:1──> EnvironmentConfig
CodingSession ──0:1──> AIAssistantConfig
CodingSession ──1:1──> SessionUsageMetrics
User (auth) ──1:N──> SSHKey
User (auth) ──1:N──> APIKey
```

## Integration with Existing Domains

### auth Domain
- **User** entity provides user identity and authentication
- **Session** differs from auth.Session (which is for web/API auth)
- **APIKey** in coding-session is for GoCoder API access, not general auth

### infrastructure Domain
- **ComputeProvider** entities (Container, Server, ServerlessFunction) are referenced by `computeResourceId`
- **ComputeConfig** maps to infrastructure compute types

### llm-conversation Domain
- **AIAssistantConfig** integrates with LLM conversation for AI-powered coding
- Future integration: Track AI assistant conversations within coding sessions

## Use Cases

### Personal Development
```bash
gocoder sessions create --quick
gocoder sessions attach $(gocoder sessions last --id)
```

### Team Collaboration
```bash
gocoder sessions create --name "pair-programming"
gocoder sessions share session-123 --permissions edit --expires 24h
# Share code: ABC123XYZ
# Teammate: gocoder sessions join ABC123XYZ
```

### CI/CD Automation
```bash
export GOCODER_API_KEY="gck_..."
curl -X POST https://api.gocoder.dev/v1/sessions \
  -H "Authorization: Bearer $GOCODER_API_KEY" \
  -d '{"computeConfig": {"size": "small"}, ...}'
```

### Multi-Terminal Workflows
```bash
gocoder sessions create
gocoder terminals create session-123 --name "server"
gocoder terminals create session-123 --name "logs"
gocoder terminals create session-123 --name "git"
```

## Future Extensions

1. **Session Templates** - Pre-configured environments for common stacks
2. **Workspace Persistence** - EFS-backed persistent storage
3. **Session Replay** - Time-travel debugging with full session history
4. **Multi-User Real-Time Collaboration** - Live cursor/edit sharing
5. **Voice Interface** - Speech-to-text command input
6. **Mobile Support** - Touch-optimized terminal interface

## See Also

- [auth domain](/home/user/protoflow/shared/semantic/domains/auth/README.md)
- [infrastructure domain](/home/user/protoflow/shared/semantic/domains/infrastructure/schema.yaml)
- [GoCoder CLI Idea](/home/user/protoflow/project-management/ideas/active/gocoder-cli-session-management-3d15bc2c.md)
- [GoCoder Project](/home/user/protoflow/projects/personal/active/tool-gocoder-web-agentic-coding-ui-like-claude-code-web-t9x2k/)
