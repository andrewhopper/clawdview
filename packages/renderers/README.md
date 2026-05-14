# clawdview-renderers

Standalone, in-line content renderers extracted from [ClawdView](../../README.md).
Drop them into a chat interface, a notebook, or any React app where you want
to render assistant-produced content next to the message.

Each renderer accepts a `content: string` prop and one or two optional knobs.
Nothing assumes the surrounding ClawdView UI.

## Install

```bash
npm install clawdview-renderers
# or, for local development inside this monorepo, import from
# `../../packages/renderers/src` directly.
```

Peer dependency: `react >= 18`.

## Quick start

```tsx
import { Renderer } from 'clawdview-renderers';

function ChatMessage({ message }) {
  return (
    <div className="chat-bubble">
      <Renderer
        content={message.body}
        kind="markdown"
      />
    </div>
  );
}
```

Or let the dispatcher infer from a filename:

```tsx
<Renderer content={toolOutput.content} filename={toolOutput.filename} />
```

## Renderers

| Kind | Component | Notes |
|------|-----------|-------|
| `html` | `HtmlRenderer` | Sandboxed iframe via `srcDoc`. |
| `markdown` | `MarkdownRenderer` | Uses `marked` + `DOMPurify` (sanitized by default). |
| `svg` | `SvgRenderer` | Strips `<script>` and inline event handlers. |
| `json` | `JsonRenderer` | Pretty-prints; shows parse errors inline. |
| `jsx` | `ReactRenderer` | Sandboxed iframe; loads React + Babel from CDN. |
| `drawio` | `DrawioRenderer` | Sandboxed iframe; loads `viewer.diagrams.net`. |

Each can also be imported directly:

```tsx
import { MarkdownRenderer } from 'clawdview-renderers/MarkdownRenderer';
```

## Security notes for chat usage

- **HTML / JSX / Drawio** run in sandboxed iframes. `ReactRenderer` uses
  `sandbox="allow-scripts"` (no `allow-same-origin`), so the rendered JSX
  cannot read or modify the host page.
- **Markdown** is sanitized with DOMPurify by default. Pass `sanitize={false}`
  or your own `sanitizer` for trusted content.
- **SVG** has `<script>` tags and `on*` handlers stripped. For paranoid
  contexts, wrap it in your own iframe.
- **HtmlRenderer** does not set a sandbox by default — pass one explicitly when
  rendering untrusted markup in chat (e.g. `sandbox=""` for fully inert, or
  `sandbox="allow-scripts"` to allow interactivity without same-origin).

## Why no Python renderer?

The original Python renderer was just a "click Run" placeholder that called
the ClawdView server's `/api/execute/python` endpoint. That requires a backend
and is out of scope for in-line chat rendering. Run Python server-side and
feed the output through `Renderer` as text or markdown.
