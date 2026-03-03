# Patterns from VSCode Web and Similar Projects

> Research for [Issue #22](https://github.com/andrewhopper/clawdview/issues/22) — investigating patterns borrowable from vscode.dev and similar browser-based IDEs.

## Current State of QuickView

Before diving into patterns, here is a precise audit of what QuickView currently has and what the gaps are.

**Current stack:**
- Express + Socket.IO + chokidar for server and live reload
- `highlight.js` for read-only syntax highlighting in a `<pre><code>` block
- Babel standalone for in-browser JSX transpilation
- Tab-based UI (Preview / Code / Output) with no split-pane capability
- File tree as a flat list with CSS emoji icons
- Python execution via `child_process.spawn` on the server
- A basic hand-rolled markdown renderer and JS/HTML/CSS formatter

**Gaps relative to professional tools:**
- Code panel is view-only (no in-browser editing)
- No command palette / keyboard-first navigation
- No split-pane resizing (code + preview side by side)
- No inline diagnostics or error overlay tied to line numbers
- No terminal panel
- No Language Server Protocol (LSP) integration
- No theme switching

---

## 1. VSCode Web (vscode.dev) Key Architectural Patterns

### Monaco Editor Integration

Monaco is the editor engine that powers VSCode. It is published as a standalone npm package (`monaco-editor`) separate from the full VSCode shell.

**CDN setup (recommended for QuickView's current architecture):**

```html
<script src="https://cdn.jsdelivr.net/npm/monaco-editor@0.50.0/min/vs/loader.js"></script>
<script>
  require.config({
    paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.50.0/min/vs' }
  });
  require(['vs/editor/editor.main'], function () {
    const editor = monaco.editor.create(document.getElementById('editor-container'), {
      value: '// Hello World\n',
      language: 'javascript',
      theme: 'vs-dark',
      automaticLayout: true,   // handles container resizes
      minimap: { enabled: false },
      fontSize: 14,
      lineNumbers: 'on',
      scrollBeyondLastLine: false,
      wordWrap: 'on'
    });
  });
</script>
```

**Key APIs:**

```javascript
// Update content without destroying editor state
editor.setValue(newContent);

// Get edited content to send back to server
const currentCode = editor.getValue();

// Listen for content changes (for auto-save)
editor.onDidChangeModelContent(() => {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    socket.emit('file:save', { path: currentFile.path, content: editor.getValue() });
  }, 500);
});

// Set language when a different file is selected
monaco.editor.setModelLanguage(editor.getModel(), 'python');

// Supported languages out of the box:
// 'javascript', 'typescript', 'python', 'html', 'css',
// 'json', 'markdown', 'xml', 'shell', 'sql', 'yaml'

// Jump to a specific line (for error click-through)
editor.revealLineInCenter(lineNumber);
editor.setPosition({ lineNumber, column: 1 });

// Inline error squiggles from external validation
monaco.editor.setModelMarkers(model, 'owner', [
  {
    severity: monaco.MarkerSeverity.Error,
    message: 'Unexpected token',
    startLineNumber: 3,
    startColumn: 1,
    endLineNumber: 3,
    endColumn: 10
  }
]);

// Custom theme matching QuickView's CSS variables
monaco.editor.defineTheme('quickview-dark', {
  base: 'vs-dark',
  inherit: true,
  rules: [],
  colors: { 'editor.background': '#0d0d0f' }
});
```

**Why this matters:** This single change transforms QuickView from a read-only previewer into an in-browser editor with live preview — the core value proposition of CodeSandbox and Glitch.

---

### Command Palette Pattern

VSCode's command palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) is a fuzzy-searchable list of all available actions.

**Architecture:**
1. A global registry maps command IDs to handlers
2. A floating `<div>` with a text input and a filtered list appears on the keyboard shortcut
3. The input uses fuzzy matching (score each label against the query)
4. Arrow keys navigate; Enter executes; Escape dismisses

**Monaco's built-in action system** makes this simpler — register actions on the editor and they appear in Monaco's own command palette automatically:

```javascript
editor.addAction({
  id: 'quickview.run',
  label: 'QuickView: Run Code',
  keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyR],
  run: () => runCurrentFile()
});

editor.addAction({
  id: 'quickview.format',
  label: 'QuickView: Format Document',
  keybindings: [monaco.KeyMod.Alt | monaco.KeyMod.Shift | monaco.KeyCode.KeyF],
  run: () => editor.getAction('editor.action.formatDocument').run()
});
```

For a standalone command palette (outside the editor):

```javascript
const commands = [
  { id: 'quickview.openFile',    label: 'Open File',          fn: openFilePicker },
  { id: 'quickview.runCode',     label: 'Run Code',           fn: runCurrentFile },
  { id: 'quickview.toggleTheme', label: 'Toggle Theme',       fn: toggleTheme },
  { id: 'quickview.splitView',   label: 'Toggle Split View',  fn: toggleSplit },
];

function fuzzyMatch(pattern, str) {
  let pi = 0;
  const lowerStr = str.toLowerCase();
  const lowerPat = pattern.toLowerCase();
  for (let i = 0; i < lowerStr.length && pi < lowerPat.length; i++) {
    if (lowerStr[i] === lowerPat[pi]) pi++;
  }
  return pi === lowerPat.length;
}
```

---

### Split Pane Layout

The most impactful UX change. Pattern using CSS Grid + drag handle:

```css
.editor-layout {
  display: grid;
  grid-template-columns: var(--split-left, 1fr) 4px var(--split-right, 1fr);
  height: 100%;
}

.split-handle {
  background: var(--border-color);
  cursor: col-resize;
}

.split-handle:hover { background: var(--primary-color); }
```

```javascript
handle.addEventListener('mousedown', () => {
  const onDrag = (e) => {
    const pct = (e.clientX / window.innerWidth) * 100;
    const clamped = Math.min(Math.max(pct, 20), 80);
    document.documentElement.style.setProperty('--split-left', `${clamped}%`);
    document.documentElement.style.setProperty('--split-right', `${100 - clamped}%`);
    monacoEditor?.layout(); // CRITICAL: Monaco caches its dimensions
  };
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', () => {
    document.removeEventListener('mousemove', onDrag);
    localStorage.setItem('quickview-split', pct); // persist preference
  }, { once: true });
});
```

**Three layout modes** (replace current tab system):
- **Code only** — full-width Monaco editor
- **Split** — editor left, preview right (resizable)
- **Preview only** — full-width preview iframe

---

### Status Bar Pattern

A thin bar at the bottom showing file info, connection status, and diagnostics count.

```html
<div class="status-bar">
  <span class="status-left">
    <span id="sb-connection" class="sb-item">● Connected</span>
    <span id="sb-file" class="sb-item">index.html</span>
  </span>
  <span class="status-right">
    <span id="sb-problems" class="sb-item clickable">⚠ 2</span>
    <span id="sb-language" class="sb-item">HTML</span>
    <span id="sb-position" class="sb-item">Ln 1, Col 1</span>
  </span>
</div>
```

Monaco exposes cursor position: `editor.onDidChangeCursorPosition(e => updateStatusBar(e.position))`

---

### Theme System (CSS Variables Approach)

QuickView already uses CSS custom properties — extending to support theme switching requires only:

```javascript
const themes = {
  dark:  { '--background': '240 10% 3.9%', '--foreground': '0 0% 98%', /* ... */ },
  light: { '--background': '0 0% 100%',    '--foreground': '240 10% 3.9%', /* ... */ },
};

function applyTheme(name) {
  Object.entries(themes[name]).forEach(([prop, val]) =>
    document.documentElement.style.setProperty(prop, val)
  );
  monaco.editor.setTheme(name === 'dark' ? 'vs-dark' : 'vs');
  localStorage.setItem('quickview-theme', name);
}
```

---

### File Tree Improvements (VSCode Explorer Pattern)

**Collapsible directories with keyboard navigation:**

```javascript
class FileTreeNode {
  constructor(item, level = 0) {
    this.item = item;
    this.level = level;
    this.expanded = level === 0;
  }

  render() {
    const el = document.createElement('div');
    el.className = `tree-item ${this.item.type}`;
    el.style.setProperty('--indent', this.level);
    el.setAttribute('role', 'treeitem');
    el.setAttribute('aria-expanded', this.expanded);
    el.setAttribute('tabindex', '-1');
    // ... chevron, icon, label
    return el;
  }
}
```

**Keyboard navigation:**
```javascript
treeContainer.addEventListener('keydown', (e) => {
  const items = [...treeContainer.querySelectorAll('[role="treeitem"]')];
  const idx = items.indexOf(document.activeElement);
  if (e.key === 'ArrowDown') items[idx + 1]?.focus();
  if (e.key === 'ArrowUp')   items[idx - 1]?.focus();
  if (e.key === 'Enter')     selectNode(items[idx]);
});
```

**Context menu on right-click:**
```javascript
treeItem.addEventListener('contextmenu', (e) => {
  e.preventDefault();
  showContextMenu(e.clientX, e.clientY, [
    { label: 'Open',      action: () => openFile(item) },
    { label: 'Copy Path', action: () => navigator.clipboard.writeText(item.path) },
  ]);
});
```

---

## 2. Similar Projects: Key Patterns

### CodeSandbox — In-Browser Module Bundling (Sandpack)

Sandpack is CodeSandbox's open-source, embeddable in-browser bundler. It replaces QuickView's current Babel-standalone + `<script>` injection approach with a proper module-aware bundler:

```javascript
import { SandpackClient } from '@codesandbox/sandpack-client';

const client = new SandpackClient('#preview-iframe', {
  files: {
    '/App.jsx': { code: jsxContent },
    '/index.js': { code: `import React from 'react'; import ReactDOM from 'react-dom/client';
      import App from './App';
      ReactDOM.createRoot(document.getElementById('root')).render(<App />);` }
  },
  dependencies: { react: '^18.0.0', 'react-dom': '^18.0.0' }
});

// Incremental file update without full reload
client.updateSandbox({ files: { '/App.jsx': { code: newContent } } });
```

**Key insight from CodeSandbox's architecture:** The bundler runs in a Service Worker. The preview iframe communicates with the bundler via `postMessage`. This means user code is completely isolated from the editor UI.

**For QuickView's iframe sandboxing:**
```javascript
// In main UI
previewIframe.contentWindow.postMessage({ type: 'update', code, language }, '*');

// In preview-sandbox.html
window.addEventListener('message', (e) => {
  if (e.data.type === 'update') executeCode(e.data.code, e.data.language);
});
```

---

### StackBlitz — WebContainers API

WebContainers runs a full Node.js environment in the browser using WebAssembly:

```javascript
import { WebContainer } from '@webcontainer/api';

const webcontainerInstance = await WebContainer.boot();
await webcontainerInstance.mount({
  'package.json': { file: { contents: JSON.stringify({ name: 'app', type: 'module' }) } },
  'index.js':     { file: { contents: 'console.log("Hello!")' } }
});

// Run npm install and dev server
const installProcess = await webcontainerInstance.spawn('npm', ['install']);
await installProcess.exit;
const devProcess = await webcontainerInstance.spawn('npm', ['run', 'dev']);
webcontainerInstance.on('server-ready', (port, url) => {
  previewIframe.src = url; // special *.webcontainer.io URL
});

// Write a file — triggers hot reload automatically
await webcontainerInstance.fs.writeFile('/src/App.jsx', newContent);
```

**Requirements:**
- HTTP response headers: `Cross-Origin-Opener-Policy: same-origin` + `Cross-Origin-Embedder-Policy: require-corp`
- Modern browser (Chrome 89+, Safari 16.4+, Firefox 111+)

**For QuickView's server.js:**
```javascript
app.use((req, res, next) => {
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
  next();
});
```

---

### Pyodide — Python in the Browser

**Replaces** the current `child_process.spawn('python3', ...)` approach. Pyodide runs CPython in WebAssembly:

```html
<script src="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"></script>
```

```javascript
const pyodide = await loadPyodide();

// Capture print() output
pyodide.globals.set('print', (s) => appendOutput(s));

try {
  await pyodide.runPythonAsync(pythonCode);
} catch (err) {
  showError(err.message);
}
```

**Benefits over server-side execution:**
- No Python installation required on the server
- No rate limiting needed (runs in browser sandbox)
- Supports NumPy, pandas, matplotlib (renders to canvas)
- Eliminates the `/api/execute/python` endpoint entirely

---

### Glitch — Inline Console Log Capture

Glitch shows `console.log` from the preview iframe in the output panel:

```javascript
// In preview sandbox iframe
const originalLog = console.log;
console.log = (...args) => {
  originalLog(...args);
  window.parent.postMessage({ type: 'console', level: 'log', args: args.map(String) }, '*');
};

['warn', 'error', 'info'].forEach(level => {
  const orig = console[level];
  console[level] = (...args) => {
    orig(...args);
    window.parent.postMessage({ type: 'console', level, args: args.map(String) }, '*');
  };
});

// In main UI
window.addEventListener('message', (e) => {
  if (e.data.type === 'console') {
    appendToOutput(`[${e.data.level}] ${e.data.args.join(' ')}`, e.data.level);
  }
});
```

---

### Replit — Streaming Output Pattern

Replace QuickView's current "wait for full output" approach with streaming:

```javascript
// Server side — emit output line by line
python.stdout.on('data', (data) => socket.emit('output:line', { content: data.toString(), type: 'stdout' }));
python.stderr.on('data', (data) => socket.emit('output:line', { content: data.toString(), type: 'stderr' }));
python.on('close', (code) => socket.emit('output:end', { exitCode: code }));

// Client side
socket.on('output:line', ({ content, type }) => {
  const line = document.createElement('div');
  line.className = `output-line ${type}`;
  line.textContent = content;
  outputContainer.appendChild(line);
  outputContainer.scrollTop = outputContainer.scrollHeight; // auto-scroll
});
```

---

## 3. Terminal Integration (xterm.js)

All mature browser IDEs include a terminal panel. The standard is `xterm.js`:

```javascript
import { Terminal } from 'xterm';
import { FitAddon } from '@xterm/addon-fit';

const term = new Terminal({
  theme: { background: '#0d0d0f', foreground: '#c9d1d9' },
  fontFamily: 'JetBrains Mono, Menlo, monospace',
  fontSize: 13,
  cursorBlink: true
});
const fitAddon = new FitAddon();
term.loadAddon(fitAddon);
term.open(document.getElementById('terminal'));
fitAddon.fit();

// Connect to server-side PTY via Socket.IO
const socket = io('/terminal');
term.onData(data => socket.emit('input', data));
socket.on('output', data => term.write(data));
```

```javascript
// Server side with node-pty
const pty = require('node-pty');
const shell = pty.spawn(process.env.SHELL || 'bash', [], {
  name: 'xterm-color',
  cols: 80, rows: 24,
  cwd: watchDir
});
socket.on('input', data => shell.write(data));
shell.on('data', data => socket.emit('output', data));
```

The terminal panel replaces the current read-only Output tab and enables users to run arbitrary commands (`python3 script.py`, `node index.js`, `npm run dev`).

---

## 4. Language Server Protocol (LSP) Integration

For Python autocompletion, hover docs, and go-to-definition — bridge the LSP server over WebSocket:

```
Browser (monaco-languageclient) <--WebSocket--> Express server (ws-proxy) <--stdio--> pylsp/pyright
```

```javascript
// Server: lsp-bridge.js
const { createConnection } = require('vscode-ws-jsonrpc/server');
const { spawn } = require('child_process');

wsServer.on('connection', (ws) => {
  const lspServer = spawn('pylsp', [], { cwd: watchDir });
  const conn = createConnection(new WebSocketMessageReader(ws), new WebSocketMessageWriter(ws));
  const serverConn = createConnection(
    new StreamMessageReader(lspServer.stdout),
    new StreamMessageWriter(lspServer.stdin)
  );
  conn.forward(serverConn);
  serverConn.forward(conn);
});
```

```javascript
// Client: lsp-client.js
import { MonacoLanguageClient } from 'monaco-languageclient';
const client = new MonacoLanguageClient({
  name: 'Python Language Client',
  clientOptions: { documentSelector: [{ language: 'python' }] },
  connectionProvider: { get: async () => ({ reader, writer }) }
});
client.start();
```

**Simpler alternative:** Register Monaco completion providers directly for basic snippets without a full LSP server:
```javascript
monaco.languages.registerCompletionItemProvider('python', {
  provideCompletionItems: () => ({
    suggestions: [
      { label: 'print', kind: monaco.languages.CompletionItemKind.Function,
        insertText: 'print(${1:})',
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet },
      { label: 'def',   kind: monaco.languages.CompletionItemKind.Keyword,
        insertText: 'def ${1:name}(${2:}):\n    ${3:pass}',
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet }
    ]
  })
});
```

---

## 5. Keyboard Shortcuts Registry

A centralized keybinding registry prevents conflicts and enables the command palette to show keybindings:

```javascript
const keybindings = new Map([
  ['meta+shift+p', 'quickview.showCommandPalette'],
  ['ctrl+shift+p', 'quickview.showCommandPalette'],
  ['meta+r',       'quickview.runCode'],
  ['ctrl+r',       'quickview.runCode'],
  ['ctrl+`',       'quickview.toggleTerminal'],
  ['meta+b',       'quickview.toggleSidebar'],
  ['meta+\\',      'quickview.toggleSplit'],
  ['meta+s',       'quickview.saveFile'],
  ['ctrl+s',       'quickview.saveFile'],
]);

document.addEventListener('keydown', (e) => {
  const key = [
    e.metaKey  ? 'meta'  : '',
    e.ctrlKey  ? 'ctrl'  : '',
    e.shiftKey ? 'shift' : '',
    e.altKey   ? 'alt'   : '',
    e.key.toLowerCase()
  ].filter(Boolean).join('+');

  const commandId = keybindings.get(key);
  if (commandId) {
    e.preventDefault();
    executeCommand(commandId);
  }
});
```

---

## Priority Roadmap

### Priority 1 — High Impact, Low Complexity

1. **Replace `highlight.js` with Monaco Editor** (CDN AMD loader). Adds syntax highlighting, line numbers, and in-browser editing.
2. **Add split-pane layout** (Monaco left, preview iframe right) with a CSS Grid drag handle. Replace tabs with a three-mode toggle.
3. **Debounced auto-save via Socket.IO** when Monaco content changes — removes the need for a separate "Format" step and makes the tool feel "always live" like Glitch.

### Priority 2 — Medium Impact, Moderate Complexity

4. **Command Palette** (`Ctrl+Shift+P`) using Monaco's built-in `editor.addAction()` API.
5. **Status bar** at the bottom with file name, language, cursor position, and connection state.
6. **Stream Python output line-by-line** via Socket.IO events instead of waiting for full completion.
7. **Capture `console.log` from preview iframes** via `postMessage` and display in the output panel.

### Priority 3 — High Impact, Higher Complexity

8. **Pyodide** for in-browser Python execution — eliminates the server-side Python dependency entirely.
9. **xterm.js terminal panel** at the bottom, replacing the read-only Output tab with a real shell.
10. **Inline error markers** in Monaco tied to Python stderr output and JSX Babel errors.
11. **COOP/COEP headers** on the Express server to enable SharedArrayBuffer (required for WebContainers and Pyodide's multi-threading).

### Priority 4 — Future / Optional

12. **Sandpack client** (`@codesandbox/sandpack-client`) for proper React preview with npm module support.
13. **WebContainers API** for full Node.js project execution in the browser.
14. **LSP proxy** on the server for Python (`pylsp` or `pyright` via WebSocket bridge) enabling autocomplete and hover docs.
15. **Collaborative editing** via `yjs` + `y-monaco` + `y-websocket`.
16. **Responsive preview modes** (desktop / tablet / mobile viewport simulation).

---

## Libraries Summary

| Library | Purpose | Size | Priority |
|---|---|---|---|
| `monaco-editor` | Editor (replaces highlight.js) | ~5MB CDN | P1 |
| `pyodide` | Python in browser | ~8MB | P3 |
| `xterm` + `@xterm/addon-fit` | Terminal panel | ~300KB | P3 |
| `@codesandbox/sandpack-client` | React module bundling | ~2MB | P4 |
| `@webcontainer/api` | Node.js in browser | n/a (CDN) | P4 |
| `monaco-languageclient` | LSP client for Monaco | ~500KB | P4 |
| `yjs` + `y-monaco` | Collaborative editing | ~200KB | P4 |

---

*Research completed: 2026-03-03*
