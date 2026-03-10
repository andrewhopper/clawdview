<!-- File UUID: 3e8f7a1c-2d4b-5e9f-8a6c-1f3d9e5b7c2a -->

# Local Development Environment Skill

**Skill Name:** `local-dev`
**Alias:** `ld`

## Purpose

Manage local development environments using Docker, Docker Compose, and AWS SAM CLI for running Lambda functions and services locally.

## Usage

```
/local-dev [action] [options]
```

## Actions

### SAM CLI Operations

| Action | Description | Example |
|--------|-------------|---------|
| `sam-build` | Build SAM application | `/local-dev sam-build` |
| `sam-invoke` | Invoke Lambda function | `/local-dev sam-invoke FunctionName event.json` |
| `sam-api` | Start local API Gateway | `/local-dev sam-api` |
| `sam-event` | Generate sample event | `/local-dev sam-event s3 put` |
| `sam-logs` | View Lambda logs | `/local-dev sam-logs FunctionName` |

### Docker Operations

| Action | Description | Example |
|--------|-------------|---------|
| `up` | Start Docker Compose services | `/local-dev up` |
| `down` | Stop Docker Compose services | `/local-dev down` |
| `logs` | View service logs | `/local-dev logs api` |
| `status` | Show running containers | `/local-dev status` |
| `exec` | Execute command in container | `/local-dev exec api bash` |

### Environment Management

| Action | Description | Example |
|--------|-------------|---------|
| `env-setup` | Create local env files | `/local-dev env-setup` |
| `clean` | Clean up containers/volumes | `/local-dev clean` |

## Quick Start Examples

### Test Lambda Locally
```
/local-dev sam-build
/local-dev sam-event apigateway aws-proxy > event.json
/local-dev sam-invoke MyFunction event.json
```

### Start Local API
```
/local-dev sam-build
/local-dev sam-api
# API available at http://localhost:3000
```

### Start Full Stack
```
/local-dev up
/local-dev logs -f
/local-dev down
```

## Workflow

When invoked, the skill will:

1. **Detect Project Type**
   - Check for `template.yaml` (SAM project)
   - Check for `docker-compose.yml` (Docker project)
   - Check for both (hybrid project)

2. **Verify Prerequisites**
   - Docker running
   - SAM CLI installed (if SAM project)
   - Required files exist

3. **Execute Action**
   - Run appropriate command based on action
   - Display output and logs
   - Handle errors gracefully

4. **Provide Guidance**
   - Suggest next steps
   - Show available endpoints
   - Offer troubleshooting if errors occur

## Agent Invocation

For complex scenarios, this skill spawns the `local-dev` agent:
- Multi-service debugging
- Complex Docker Compose setups
- Step-through debugging configuration
- LocalStack integration

See full agent documentation: `@processes/LOCAL_DEV_AGENT`

## Default Behavior (No Action)

When run without arguments (`/local-dev`), the skill will:

1. Scan current directory for project type
2. Show current status (running containers, available services)
3. Suggest common next actions

## Interactive Mode

```
/local-dev interactive
```

Enters interactive mode with menu:
```
Local Development Environment
─────────────────────────────
[1] Start local API (sam local start-api)
[2] Invoke function (sam local invoke)
[3] Generate event (sam local generate-event)
[4] Start Docker services (docker-compose up)
[5] View logs (docker-compose logs)
[6] Stop all services
[7] Clean up (remove containers/volumes)
[q] Quit
```

## Configuration

The skill respects `.local-dev.yml` if present:

```yaml
# .local-dev.yml
sam:
  port: 3000
  warm_containers: true
  env_file: env.local.json

docker:
  compose_file: docker-compose.dev.yml
  env_file: .env.local

defaults:
  action: sam-api  # Default when running /local-dev
```
