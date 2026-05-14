import { useMemo, type CSSProperties } from 'react';
import { escapeHtml } from './utils';

export interface ReactRendererProps {
  content: string;
  className?: string;
  style?: CSSProperties;
  title?: string;
  /**
   * CDN URLs for the React runtime loaded inside the iframe. Override to pin
   * versions or self-host.
   */
  runtime?: {
    react?: string;
    reactDom?: string;
    babel?: string;
  };
  /**
   * Background color for the iframe document. Defaults to white.
   */
  background?: string;
}

const DEFAULT_RUNTIME = {
  react: 'https://unpkg.com/react@18/umd/react.development.js',
  reactDom: 'https://unpkg.com/react-dom@18/umd/react-dom.development.js',
  babel: 'https://unpkg.com/@babel/standalone/babel.min.js',
};

const DEFAULT_STYLE: CSSProperties = {
  width: '100%',
  height: '100%',
  border: 'none',
  background: '#fff',
};

function utf8ToBase64(str: string): string {
  if (typeof window !== 'undefined' && typeof window.btoa === 'function') {
    return window.btoa(unescape(encodeURIComponent(str)));
  }
  return Buffer.from(str, 'utf-8').toString('base64');
}

/**
 * Renders user-supplied JSX in a sandboxed iframe with React + ReactDOM +
 * Babel loaded from CDN. This keeps the JSX isolated from the host React app
 * (no global pollution, no version conflicts) and matches the authoring
 * conventions used by ClawdView: a top-level capitalized function, optionally
 * assigned to `window.<Name>`.
 */
export function ReactRenderer({
  content,
  className,
  style,
  title = 'React Preview',
  runtime,
  background = '#fff',
}: ReactRendererProps) {
  const srcDoc = useMemo(() => {
    const r = { ...DEFAULT_RUNTIME, ...runtime };
    const sourceBase64 = utf8ToBase64(content);
    return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body { margin: 0; padding: 0; height: 100%; background: ${escapeHtml(background)}; font-family: system-ui, -apple-system, sans-serif; }
  #react-preview { min-height: 100%; }
  .clawdview-react-error { color: #b91c1c; padding: 1rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; white-space: pre-wrap; }
</style>
<script src="${r.react}" crossorigin></script>
<script src="${r.reactDom}" crossorigin></script>
<script src="${r.babel}"></script>
</head>
<body>
<div id="react-preview"></div>
<script>
(function () {
  var mount = document.getElementById('react-preview');
  function showError(msg) {
    mount.innerHTML = '<div class="clawdview-react-error">' + msg + '</div>';
  }
  try {
    var source = decodeURIComponent(escape(atob("${sourceBase64}")));
    var transformed = Babel.transform(source, { presets: ['react'] }).code;
    // Evaluate in a function so top-level "var Foo = ..." still lands on window
    // (matches existing ClawdView authoring convention).
    (new Function(transformed + '\\n//# sourceURL=react-preview.jsx'))();
    var componentName = Object.keys(window).find(function (key) {
      return (
        typeof window[key] === 'function' &&
        key[0] && key[0] === key[0].toUpperCase() &&
        key !== 'React' && key !== 'ReactDOM' && key !== 'Babel'
      );
    });
    if (componentName) {
      var Component = window[componentName];
      ReactDOM.render(React.createElement(Component), mount);
    } else {
      showError('No top-level component found. Define a capitalized function or assign one to window.');
    }
  } catch (error) {
    showError('React Error: ' + (error && error.message ? error.message : String(error)));
  }
})();
</script>
</body>
</html>`;
  }, [content, runtime, background]);

  return (
    <iframe
      className={className}
      style={{ ...DEFAULT_STYLE, ...style }}
      srcDoc={srcDoc}
      title={title}
      sandbox="allow-scripts"
    />
  );
}
