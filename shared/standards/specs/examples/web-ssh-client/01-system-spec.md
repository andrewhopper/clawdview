# System Specification: Web SSH Client

## 1.0 Overview

A browser-based SSH terminal client enabling secure remote server access without native SSH clients. Users connect via WebSocket to a backend proxy that establishes SSH connections on their behalf.

## 2.0 System Context

```
┌─────────────┐     HTTPS/WSS      ┌─────────────┐      SSH       ┌─────────────┐
│   Browser   │ ◄───────────────► │   Backend   │ ◄────────────► │   Remote    │
│  (xterm.js) │                    │   Proxy     │                │   Server    │
└─────────────┘                    └─────────────┘                └─────────────┘
      │                                  │
      │ Renders terminal                 │ node-pty / ssh2
      │ Captures keystrokes              │ Session management
      │ Handles resize                   │ Auth forwarding
```

## 3.0 Constraints

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "WebSSHSystemConstraints",
  "required": ["performance", "security", "compatibility"],
  "properties": {
    "performance": {
      "type": "object",
      "properties": {
        "latency_ms": { "type": "number", "maximum": 100, "description": "Keystroke to render round-trip" },
        "reconnect_ms": { "type": "number", "maximum": 5000, "description": "Auto-reconnect timeout" },
        "max_scrollback": { "type": "integer", "minimum": 1000, "maximum": 100000 }
      }
    },
    "security": {
      "type": "object",
      "properties": {
        "transport": { "const": "wss", "description": "WebSocket Secure only" },
        "auth_methods": { "type": "array", "items": { "enum": ["password", "publickey", "keyboard-interactive"] } },
        "credential_storage": { "const": "none", "description": "Never persist credentials server-side" }
      }
    },
    "compatibility": {
      "type": "object",
      "properties": {
        "browsers": { "type": "array", "items": { "enum": ["chrome", "firefox", "safari", "edge"] }, "minItems": 4 },
        "terminal_emulation": { "const": "xterm-256color" },
        "unicode_support": { "const": true }
      }
    }
  }
}
```

## 4.0 Core Capabilities

### 4.1 Terminal Emulation
- Full xterm compatibility (escape sequences, colors, cursor modes)
- Unicode/emoji rendering
- Copy/paste with system clipboard
- Configurable fonts, colors, cursor styles

### 4.2 Connection Management
- Multiple concurrent sessions (tabbed interface)
- Session persistence across page refresh (optional)
- Graceful disconnect handling with auto-reconnect

### 4.3 Authentication
- Password authentication
- SSH key authentication (paste or upload)
- Keyboard-interactive (2FA prompts)

### 4.4 File Transfer
- SFTP integration for upload/download
- Drag-and-drop file upload to current directory

## 5.0 Output Schema

When describing system capabilities to an LLM, use:

```json
{
  "type": "object",
  "required": ["capability", "status", "implementation"],
  "properties": {
    "capability": { "type": "string" },
    "status": { "enum": ["required", "optional", "future"] },
    "implementation": {
      "type": "object",
      "properties": {
        "frontend": { "type": "string" },
        "backend": { "type": "string" },
        "protocol": { "type": "string" }
      }
    },
    "acceptance_criteria": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

## 6.0 Examples

### Example: Terminal Resize

**Input:** User resizes browser window
**Expected:**
```json
{
  "capability": "terminal_resize",
  "status": "required",
  "implementation": {
    "frontend": "xterm.js FitAddon",
    "backend": "PTY resize via SIGWINCH",
    "protocol": "WebSocket binary frame: {cols: u16, rows: u16}"
  },
  "acceptance_criteria": [
    "Terminal reflows within 16ms of resize event",
    "No content loss during resize",
    "Works with vim, tmux, screen"
  ]
}
```
