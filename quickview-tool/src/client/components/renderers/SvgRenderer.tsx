import { useMemo } from 'react';

interface SvgRendererProps {
  content: string;
}

function sanitizeSvg(svg: string): string {
  // Remove script tags and event handler attributes
  return svg
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<script[\s\S]*?\/?>/gi, '')
    .replace(/\son\w+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]*)/gi, '');
}

export function SvgRenderer({ content }: SvgRendererProps) {
  const sanitized = useMemo(() => sanitizeSvg(content), [content]);

  return (
    <div
      className="p-5 text-center bg-background"
      dangerouslySetInnerHTML={{ __html: sanitized }}
    />
  );
}
