---
name: http-tunnel
description: Expose local ports via HTTP long-poll tunnel for previewing web apps
version: 1.0.0
---

# HTTP Tunnel Skill

Expose local ports through an HTTP long-poll tunnel, allowing preview of web apps running in restricted environments like Claude Code Remote.

## Why This Exists

Standard tunnel tools (ngrok, chisel, wstunnel) fail in restricted environments due to:
- TLS interception by proxies
- WebSocket blocking
- HTTP/2 downgrading

This tunnel uses pure HTTP/1.1 long-polling which works through any proxy.

## Prerequisites

1. **Relay Server** - Deploy one of:
   - Lambda: `python deploy_lambda.py deploy --region us-east-1`
   - ECS: `python deploy_ecs.py deploy --region us-east-1`
   - Or use a shared relay URL if available

2. **Environment Variable** (optional):
   ```bash
   export TUNNEL_RELAY_URL=https://your-relay.lambda-url.us-east-1.on.aws
   ```

## Execution Flow

### 1. Start Local Server (if not running)

If no server is running on the target port, start one:

```bash
# For static files
python -m http.server PORT &

# For a specific app
cd /path/to/app && npm run dev &
```

### 2. Start Tunnel Client

```bash
cd /home/user/protoflow/projects/unspecified/active/docker-port-tunnel-dqbax

# Use environment variable or explicit URL
python tunnel_client.py \
  --relay ${TUNNEL_RELAY_URL:-https://your-relay-url} \
  --port PORT
```

### 3. Return Public URL

The tunnel client outputs:
```
Tunnel active!
Public URL:  https://relay-url/t/abc123
Local:       http://127.0.0.1:PORT
```

Return the public URL to the user for browser access.

## Usage Examples

### Preview a React Dev Server

```bash
# User: "Preview my React app on port 3000"

# 1. Ensure dev server is running
cd /path/to/react-app && npm run dev &

# 2. Start tunnel
python /home/user/protoflow/projects/unspecified/active/docker-port-tunnel-dqbax/tunnel_client.py \
  --relay $TUNNEL_RELAY_URL \
  --port 3000

# 3. Return URL to user
```

### Preview Static HTML

```bash
# User: "Let me see the HTML file I just created"

# 1. Start simple server
cd /path/to/html/directory
python -m http.server 8080 &

# 2. Start tunnel
python /home/user/protoflow/projects/unspecified/active/docker-port-tunnel-dqbax/tunnel_client.py \
  --relay $TUNNEL_RELAY_URL \
  --port 8080

# 3. Return URL to user
```

### Quick One-Liner

```bash
# Start server and tunnel in one command
(cd /path/to/app && python -m http.server 8080 &) && \
python /home/user/protoflow/projects/unspecified/active/docker-port-tunnel-dqbax/tunnel_client.py \
  --relay $TUNNEL_RELAY_URL \
  --port 8080
```

## Error Handling

### No Relay URL Configured

```
Error: --relay is required

Resolution: Set TUNNEL_RELAY_URL environment variable or pass --relay explicitly
```

### Local Port Not Responding

```
Local service not available at http://127.0.0.1:PORT

Resolution: Ensure your app is running on the specified port
```

### Relay Server Unreachable

```
Connection error to relay server

Resolution: Check relay URL, ensure Lambda/ECS is deployed and running
```

## Stopping the Tunnel

Press `Ctrl+C` in the tunnel client terminal, or:

```bash
pkill -f tunnel_client.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `TUNNEL_RELAY_URL` | (none) | URL of deployed relay server |
| `--port` | (required) | Local port to expose |
| `--host` | `127.0.0.1` | Local host to forward to |

## Related Files

- Prototype: `/home/user/protoflow/projects/unspecified/active/docker-port-tunnel-dqbax/`
- Client: `tunnel_client.py`
- Lambda deploy: `deploy_lambda.py`
- ECS deploy: `deploy_ecs.py`
