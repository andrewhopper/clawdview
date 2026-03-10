# Component Specification: Terminal Emulator

## 1.0 Purpose

Render an interactive terminal in the browser that behaves identically to a native terminal emulator. Built on xterm.js with custom addons.

## 2.0 Interface Contract

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TerminalComponentProps",
  "type": "object",
  "required": ["connectionId"],
  "properties": {
    "connectionId": {
      "type": "string",
      "format": "uuid",
      "description": "Active WebSocket session ID"
    },
    "options": {
      "type": "object",
      "properties": {
        "fontSize": { "type": "integer", "minimum": 8, "maximum": 32, "default": 14 },
        "fontFamily": { "type": "string", "default": "JetBrains Mono, monospace" },
        "theme": { "$ref": "#/$defs/TerminalTheme" },
        "cursorStyle": { "enum": ["block", "underline", "bar"], "default": "block" },
        "cursorBlink": { "type": "boolean", "default": true },
        "scrollback": { "type": "integer", "minimum": 0, "maximum": 100000, "default": 10000 },
        "bellStyle": { "enum": ["none", "sound", "visual"], "default": "visual" }
      }
    },
    "onData": {
      "description": "Callback when user types - receives string of characters",
      "type": "string",
      "const": "(data: string) => void"
    },
    "onResize": {
      "description": "Callback when terminal dimensions change",
      "type": "string",
      "const": "(cols: number, rows: number) => void"
    },
    "onTitleChange": {
      "description": "Callback when terminal title changes (escape sequence)",
      "type": "string",
      "const": "(title: string) => void"
    }
  },
  "$defs": {
    "TerminalTheme": {
      "type": "object",
      "properties": {
        "background": { "type": "string", "pattern": "^#[0-9a-fA-F]{6}$" },
        "foreground": { "type": "string", "pattern": "^#[0-9a-fA-F]{6}$" },
        "cursor": { "type": "string", "pattern": "^#[0-9a-fA-F]{6}$" },
        "selection": { "type": "string", "pattern": "^#[0-9a-fA-F]{8}$" },
        "black": { "type": "string" },
        "red": { "type": "string" },
        "green": { "type": "string" },
        "yellow": { "type": "string" },
        "blue": { "type": "string" },
        "magenta": { "type": "string" },
        "cyan": { "type": "string" },
        "white": { "type": "string" }
      }
    }
  }
}
```

## 3.0 Behavior Specifications

### 3.1 Keyboard Handling

| Key Combo | Action | Passthrough to SSH |
|-----------|--------|-------------------|
| `Ctrl+C` | Interrupt signal | ✅ Yes |
| `Ctrl+V` | Paste from clipboard | ❌ No (handled locally) |
| `Ctrl+Shift+C` | Copy selection | ❌ No (handled locally) |
| `Ctrl+Shift+V` | Paste from clipboard | ❌ No (handled locally) |
| `Ctrl+Plus` | Increase font size | ❌ No (local) |
| `Ctrl+Minus` | Decrease font size | ❌ No (local) |
| All other | Pass to remote | ✅ Yes |

### 3.2 Selection & Clipboard

```json
{
  "selection_behavior": {
    "trigger": "mousedown + drag OR shift+arrow keys",
    "copy_on_select": false,
    "copy_action": "Ctrl+Shift+C OR right-click menu",
    "paste_action": "Ctrl+Shift+V OR right-click menu OR middle-click",
    "format": "text/plain"
  }
}
```

### 3.3 Resize Handling

```
Browser resize event
       │
       ▼
┌─────────────────┐
│ Debounce 100ms  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FitAddon.fit()  │  ← Calculate new cols/rows
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ onResize(c, r)  │  ← Notify parent
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Send to backend │  ← WebSocket: {"type":"resize","cols":c,"rows":r}
└─────────────────┘
```

## 4.0 Acceptance Criteria

```json
{
  "tests": [
    {
      "id": "term-001",
      "name": "Renders 256 colors correctly",
      "input": "Run: for i in {0..255}; do printf '\\e[48;5;${i}m  '; done",
      "expected": "256 distinct colored blocks visible"
    },
    {
      "id": "term-002",
      "name": "Handles rapid output",
      "input": "Run: yes | head -10000",
      "expected": "Completes in <500ms, no dropped frames"
    },
    {
      "id": "term-003",
      "name": "Unicode rendering",
      "input": "echo '日本語 emoji: 🚀🎉 box: ┌──┐'",
      "expected": "All characters render with correct width"
    },
    {
      "id": "term-004",
      "name": "vim compatibility",
      "input": "Open vim, navigate, edit, save",
      "expected": "All cursor movements, modes, and redraws work"
    },
    {
      "id": "term-005",
      "name": "tmux compatibility",
      "input": "Attach to tmux session, split panes, resize",
      "expected": "Pane borders render correctly, mouse mode works"
    }
  ]
}
```

## 5.0 Implementation Notes

### Required xterm.js Addons
- `@xterm/addon-fit` - Auto-resize to container
- `@xterm/addon-web-links` - Clickable URLs
- `@xterm/addon-search` - Find in scrollback
- `@xterm/addon-unicode11` - Full unicode support
- `@xterm/addon-webgl` - GPU-accelerated rendering (optional)

### Performance Targets
- First render: <100ms after connection
- Keystroke latency: <16ms local processing
- Scrollback search: <50ms for 10K lines
