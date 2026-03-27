interface HtmlRendererProps {
  content: string;
}

export function HtmlRenderer({ content }: HtmlRendererProps) {
  return (
    <iframe
      className="w-full h-full border-none bg-white"
      srcDoc={content}
      title="HTML Preview"
    />
  );
}
