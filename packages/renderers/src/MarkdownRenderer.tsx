import { useMemo, type CSSProperties } from 'react';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export interface MarkdownRendererProps {
  content: string;
  className?: string;
  style?: CSSProperties;
  /**
   * Sanitize the rendered HTML with DOMPurify (default true).
   * Disable only for fully trusted Markdown.
   */
  sanitize?: boolean;
  /**
   * Custom sanitizer. Takes the rendered HTML, returns sanitized HTML.
   * If provided, overrides DOMPurify.
   */
  sanitizer?: (html: string) => string;
  /**
   * Options passed through to marked.
   */
  markedOptions?: Parameters<typeof marked.parse>[1];
}

const DEFAULT_STYLE: CSSProperties = {
  padding: '1.25rem',
  lineHeight: 1.6,
};

export function MarkdownRenderer({
  content,
  className,
  style,
  sanitize = true,
  sanitizer,
  markedOptions,
}: MarkdownRendererProps) {
  const html = useMemo(() => {
    const raw = marked.parse(content, {
      ...markedOptions,
      async: false,
    }) as string;
    if (sanitizer) return sanitizer(raw);
    if (!sanitize) return raw;
    return DOMPurify.sanitize(raw);
  }, [content, sanitize, sanitizer, markedOptions]);

  return (
    <div
      className={className}
      style={{ ...DEFAULT_STYLE, ...style }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
