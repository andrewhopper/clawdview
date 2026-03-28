import { useMemo } from 'react';

interface DrawioRendererProps {
  content: string;
}

export function DrawioRenderer({ content }: DrawioRendererProps) {
  const srcDoc = useMemo(() => {
    // Base64-encode the XML to avoid any escaping issues with quotes,
    // angle brackets, etc. in the HTML attribute.
    const xmlBase64 = btoa(unescape(encodeURIComponent(content)));
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
<script src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
</body>
</html>`;
  }, [content]);

  return (
    <iframe
      className="w-full h-full border-none bg-white"
      srcDoc={srcDoc}
      title="Draw.io Preview"
      sandbox="allow-scripts allow-same-origin"
    />
  );
}
