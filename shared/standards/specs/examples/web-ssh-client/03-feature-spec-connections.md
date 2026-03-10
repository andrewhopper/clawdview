# Feature Specification: Connection Management

## 1.0 Purpose

Manage SSH connection lifecycle: create, authenticate, maintain, and gracefully terminate sessions. Support multiple concurrent connections with automatic reconnection.

## 2.0 State Machine

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    ▼                                         │
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│   IDLE   │──►│CONNECTING│──►│   AUTH   │──►│CONNECTED │   │
└──────────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   │
                    │              │              │          │
                    │ timeout      │ fail         │ dropped  │
                    ▼              ▼              ▼          │
               ┌──────────┐   ┌──────────┐   ┌──────────┐   │
               │  ERROR   │   │  ERROR   │   │RECONNECT │───┘
               └──────────┘   └──────────┘   └────┬─────┘
                                                  │ max_retries
                                                  ▼
                                             ┌──────────┐
                                             │DISCONNECTED│
                                             └──────────┘
```

## 3.0 Data Structures

### 3.1 Connection Configuration

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SSHConnectionConfig",
  "type": "object",
  "required": ["host", "port", "username"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "description": "Auto-generated connection ID"
    },
    "name": {
      "type": "string",
      "maxLength": 64,
      "description": "User-friendly display name"
    },
    "host": {
      "type": "string",
      "oneOf": [
        { "format": "hostname" },
        { "format": "ipv4" },
        { "format": "ipv6" }
      ]
    },
    "port": {
      "type": "integer",
      "minimum": 1,
      "maximum": 65535,
      "default": 22
    },
    "username": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "auth": {
      "oneOf": [
        {
          "type": "object",
          "title": "PasswordAuth",
          "required": ["method", "password"],
          "properties": {
            "method": { "const": "password" },
            "password": { "type": "string" }
          }
        },
        {
          "type": "object",
          "title": "PublicKeyAuth",
          "required": ["method", "privateKey"],
          "properties": {
            "method": { "const": "publickey" },
            "privateKey": { "type": "string", "description": "PEM-encoded private key" },
            "passphrase": { "type": "string", "description": "Key passphrase if encrypted" }
          }
        },
        {
          "type": "object",
          "title": "AgentAuth",
          "required": ["method"],
          "properties": {
            "method": { "const": "agent" },
            "agentSocket": { "type": "string", "description": "Path to SSH agent socket" }
          }
        }
      ]
    },
    "options": {
      "type": "object",
      "properties": {
        "keepaliveInterval": { "type": "integer", "minimum": 0, "default": 30000 },
        "keepaliveCountMax": { "type": "integer", "minimum": 1, "default": 3 },
        "readyTimeout": { "type": "integer", "minimum": 1000, "default": 20000 },
        "strictHostKeyChecking": { "type": "boolean", "default": true }
      }
    }
  }
}
```

### 3.2 Connection State

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ConnectionState",
  "type": "object",
  "required": ["id", "status", "createdAt"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "status": {
      "enum": ["idle", "connecting", "authenticating", "connected", "reconnecting", "error", "disconnected"]
    },
    "config": { "$ref": "#/$defs/SSHConnectionConfig" },
    "createdAt": { "type": "string", "format": "date-time" },
    "connectedAt": { "type": "string", "format": "date-time" },
    "lastActivity": { "type": "string", "format": "date-time" },
    "reconnectAttempts": { "type": "integer", "minimum": 0 },
    "error": {
      "type": "object",
      "properties": {
        "code": { "type": "string" },
        "message": { "type": "string" },
        "recoverable": { "type": "boolean" }
      }
    },
    "metrics": {
      "type": "object",
      "properties": {
        "bytesReceived": { "type": "integer" },
        "bytesSent": { "type": "integer" },
        "latencyMs": { "type": "number" }
      }
    }
  }
}
```

## 4.0 API Contract

### 4.1 Actions

```typescript
// Connection Manager Interface
interface ConnectionManager {
  // Create and connect
  connect(config: SSHConnectionConfig): Promise<ConnectionState>;

  // Disconnect gracefully
  disconnect(id: string): Promise<void>;

  // Force disconnect
  terminate(id: string): void;

  // Get current state
  getState(id: string): ConnectionState | null;

  // List all connections
  listConnections(): ConnectionState[];

  // Send data to connection
  write(id: string, data: string | Uint8Array): void;

  // Resize terminal
  resize(id: string, cols: number, rows: number): void;
}
```

### 4.2 Events

```json
{
  "events": {
    "connection:state": {
      "description": "Emitted when connection state changes",
      "payload": { "$ref": "#/$defs/ConnectionState" }
    },
    "connection:data": {
      "description": "Emitted when data received from remote",
      "payload": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "data": { "type": "string", "description": "UTF-8 encoded terminal data" }
        }
      }
    },
    "connection:error": {
      "description": "Emitted on connection error",
      "payload": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "error": { "type": "object" }
        }
      }
    }
  }
}
```

## 5.0 Behavior Rules

### 5.1 Reconnection Strategy

```json
{
  "reconnection": {
    "enabled": true,
    "triggers": ["websocket_close", "keepalive_timeout", "network_change"],
    "excludes": ["auth_failure", "host_key_mismatch", "user_disconnect"],
    "strategy": {
      "type": "exponential_backoff",
      "initialDelay": 1000,
      "maxDelay": 30000,
      "multiplier": 2,
      "maxAttempts": 5,
      "jitter": 0.1
    }
  }
}
```

### 5.2 Security Rules

1. **Never log credentials** - Password/keys must not appear in logs
2. **Memory clearing** - Wipe credentials from memory after auth completes
3. **Host key verification** - Prompt user on first connect or key change
4. **Session isolation** - Each connection runs in isolated context

## 6.0 Acceptance Criteria

```json
{
  "tests": [
    {
      "id": "conn-001",
      "name": "Successful password auth",
      "given": "Valid host, username, password",
      "when": "connect() called",
      "then": "State transitions: idle → connecting → authenticating → connected"
    },
    {
      "id": "conn-002",
      "name": "Invalid password rejection",
      "given": "Valid host, username, wrong password",
      "when": "connect() called",
      "then": "State: error, error.code: 'AUTH_FAILED', error.recoverable: false"
    },
    {
      "id": "conn-003",
      "name": "Network interruption recovery",
      "given": "Active connection",
      "when": "Network drops for 5 seconds then recovers",
      "then": "Auto-reconnects within 10 seconds, session resumes"
    },
    {
      "id": "conn-004",
      "name": "Multiple concurrent connections",
      "given": "3 different hosts",
      "when": "connect() called for each",
      "then": "All 3 reach 'connected' state independently"
    },
    {
      "id": "conn-005",
      "name": "Graceful disconnect",
      "given": "Active connection",
      "when": "disconnect() called",
      "then": "SSH channel closed, WebSocket closed, state: disconnected"
    }
  ]
}
```

## 7.0 Error Codes

| Code | Meaning | Recoverable | User Action |
|------|---------|-------------|-------------|
| `CONN_TIMEOUT` | Connection timed out | ✅ | Retry |
| `AUTH_FAILED` | Authentication rejected | ❌ | Check credentials |
| `HOST_UNREACHABLE` | Cannot reach host | ✅ | Check network/host |
| `HOST_KEY_CHANGED` | Server key changed | ❌ | Verify with admin |
| `WEBSOCKET_ERROR` | WebSocket failure | ✅ | Auto-retry |
| `PROTOCOL_ERROR` | SSH protocol error | ❌ | Report bug |
