// File UUID: b8c9d0e1-2f3a-4b5c-6d7e-8f9a0b1c2d3e
import { useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkFrontmatter from 'remark-frontmatter'
import rehypeHighlight from 'rehype-highlight'
import rehypeSlug from 'rehype-slug'
import rehypeAutolinkHeadings from 'rehype-autolink-headings'
import mermaid from 'mermaid'

interface MarkdownRendererProps {
  content: string
}

// Initialize Mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
})

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Render Mermaid diagrams after markdown is rendered
    const renderMermaid = async () => {
      if (containerRef.current) {
        const mermaidElements = containerRef.current.querySelectorAll('.language-mermaid')

        for (const element of Array.from(mermaidElements)) {
          const code = element.textContent || ''
          const parent = element.parentElement

          if (parent) {
            try {
              const { svg } = await mermaid.render(`mermaid-${Date.now()}`, code)
              const div = document.createElement('div')
              div.innerHTML = svg
              div.className = 'mermaid-diagram'
              parent.replaceWith(div)
            } catch (error) {
              console.error('Mermaid rendering error:', error)
            }
          }
        }
      }
    }

    renderMermaid()
  }, [content])

  return (
    <div ref={containerRef} className="markdown-content">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkFrontmatter]}
        rehypePlugins={[
          rehypeHighlight,
          rehypeSlug,
          [rehypeAutolinkHeadings, { behavior: 'wrap' }]
        ]}
        components={{
          // Custom rendering for code blocks to handle Mermaid
          code: ({ className, children, ...props }: any) => {
            const match = /language-(\w+)/.exec(className || '')
            const lang = match ? match[1] : ''
            const isInline = !className

            if (!isInline && lang === 'mermaid') {
              return (
                <pre className={className}>
                  <code className={className} {...props}>
                    {children}
                  </code>
                </pre>
              )
            }

            return isInline ? (
              <code className={className} {...props}>
                {children}
              </code>
            ) : (
              <pre className={className}>
                <code className={className} {...props}>
                  {children}
                </code>
              </pre>
            )
          }
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}
