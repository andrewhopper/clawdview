interface SvgRendererProps {
  content: string;
}

export function SvgRenderer({ content }: SvgRendererProps) {
  return (
    <div
      className="p-5 text-center bg-background"
      dangerouslySetInnerHTML={{ __html: content }}
    />
  );
}
