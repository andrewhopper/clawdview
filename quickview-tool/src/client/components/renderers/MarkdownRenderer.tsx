import { useMemo } from 'react';

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const html = useMemo(
    () =>
      content
        .replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold mb-4 mt-6">$1</h1>')
        .replace(/^## (.*$)/gim, '<h2 class="text-2xl font-semibold mb-3 mt-5">$1</h2>')
        .replace(/^### (.*$)/gim, '<h3 class="text-xl font-medium mb-2 mt-4">$1</h3>')
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/gim, '<em>$1</em>')
        .replace(/\n/gim, '<br>'),
    [content],
  );

  return (
    <div
      className="p-5 text-foreground prose prose-sm max-w-none"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
