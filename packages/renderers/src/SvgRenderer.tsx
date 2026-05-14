import { useMemo, type CSSProperties } from 'react';
import { sanitizeSvgString } from './utils';

export interface SvgRendererProps {
  content: string;
  className?: string;
  style?: CSSProperties;
  /**
   * If false, the SVG is injected without removing scripts or on* handlers.
   * Only do this for fully trusted content. Default true.
   */
  sanitize?: boolean;
}

const DEFAULT_STYLE: CSSProperties = {
  padding: '1.25rem',
  textAlign: 'center',
};

export function SvgRenderer({
  content,
  className,
  style,
  sanitize = true,
}: SvgRendererProps) {
  const html = useMemo(
    () => (sanitize ? sanitizeSvgString(content) : content),
    [content, sanitize],
  );

  return (
    <div
      className={className}
      style={{ ...DEFAULT_STYLE, ...style }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
