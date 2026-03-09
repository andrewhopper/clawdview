import { useMemo } from 'react';
import { sanitizeSvg } from '@/lib/utils';

interface SvgRendererProps {
  content: string;
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
