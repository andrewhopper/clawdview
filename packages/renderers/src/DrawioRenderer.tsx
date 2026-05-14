import { useMemo, type CSSProperties } from 'react';

export interface DrawioRendererProps {
  content: string;
  className?: string;
  style?: CSSProperties;
  title?: string;
  /**
   * Override the diagrams.net viewer URL if you want to self-host it.
   */
  viewerUrl?: string;
}

const DEFAULT_STYLE: CSSProperties = {
  width: '100%',
  height: '100%',
  border: 'none',
  background: '#fff',
};

const DEFAULT_VIEWER = 'https://viewer.diagrams.net/js/viewer-static.min.js';

function utf8ToBase64(str: string): string {
  if (typeof window !== 'undefined' && typeof window.btoa === 'function') {
    return window.btoa(unescape(encodeURIComponent(str)));
  }
  return Buffer.from(str, 'utf-8').toString('base64');
}

export function DrawioRenderer({
  content,
  className,
  style,
  title = 'Draw.io Preview',
  viewerUrl = DEFAULT_VIEWER,
}: DrawioRendererProps) {
  const srcDoc = useMemo(() => {
    const xmlBase64 = utf8ToBase64(content);
    return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body { margin: 0; padding: 0; height: 100%; overflow: auto; background: #fff; }
  .mxgraph { max-width: 100%; }
</style>
</head>
<body>
<div id="diagram"></div>
<script>
  var xml = decodeURIComponent(escape(atob("${xmlBase64}")));
  var div = document.getElementById("diagram");
  div.className = "mxgraph";
  div.setAttribute("data-mxgraph", JSON.stringify({
    highlight: "#0000ff",
    nav: true,
    resize: true,
    xml: xml
  }));
</script>
<script src="${viewerUrl}"></script>
</body>
</html>`;
  }, [content, viewerUrl]);

  return (
    <iframe
      className={className}
      style={{ ...DEFAULT_STYLE, ...style }}
      srcDoc={srcDoc}
      title={title}
      sandbox="allow-scripts allow-same-origin"
    />
  );
}
