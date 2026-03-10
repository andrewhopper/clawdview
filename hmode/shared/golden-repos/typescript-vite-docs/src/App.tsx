// File UUID: d0e1f2a3-4b5c-6d7e-8f9a-0b1c2d3e4f5a
import { useState, useEffect } from 'react'
import { Sidebar } from './components/Sidebar'
import { MarkdownRenderer } from './components/MarkdownRenderer'
import { ScrollArea } from './components/ui/scroll-area'
import { getAllDocs, getDocBySlug } from './lib/doc-loader'
import { DocFile, NavItem } from './lib/types'
import { FileText } from 'lucide-react'

function App() {
  const [docs, setDocs] = useState<DocFile[]>([])
  const [currentSlug, setCurrentSlug] = useState<string | null>(null)
  const [currentDoc, setCurrentDoc] = useState<DocFile | null>(null)

  useEffect(() => {
    // Load all documentation files
    const allDocs = getAllDocs()
    setDocs(allDocs)

    // Set initial document (first one in the list)
    if (allDocs.length > 0 && !currentSlug) {
      setCurrentSlug(allDocs[0].slug)
    }
  }, [])

  useEffect(() => {
    // Load current document when slug changes
    if (currentSlug) {
      const doc = getDocBySlug(currentSlug)
      setCurrentDoc(doc || null)
    }
  }, [currentSlug])

  const navItems: NavItem[] = docs.map(doc => ({
    title: doc.metadata.title,
    slug: doc.slug,
    order: doc.metadata.order || 999
  }))

  return (
    <div className="flex h-screen">
      <Sidebar
        navItems={navItems}
        currentSlug={currentSlug}
        onNavigate={setCurrentSlug}
      />

      <main className="flex-1 overflow-hidden">
        <ScrollArea className="h-full">
          <div className="max-w-4xl mx-auto px-8 py-12">
            {currentDoc ? (
              <>
                <div className="mb-8">
                  <h1 className="text-4xl font-bold tracking-tight">
                    {currentDoc.metadata.title}
                  </h1>
                  {currentDoc.metadata.description && (
                    <p className="mt-2 text-lg text-muted-foreground">
                      {currentDoc.metadata.description}
                    </p>
                  )}
                  {currentDoc.metadata.date && (
                    <p className="mt-2 text-sm text-muted-foreground">
                      Last updated: {currentDoc.metadata.date}
                    </p>
                  )}
                </div>

                <MarkdownRenderer content={currentDoc.content} />
              </>
            ) : docs.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-[60vh] text-center">
                <FileText className="h-16 w-16 text-muted-foreground mb-4" />
                <h2 className="text-2xl font-semibold mb-2">No Documentation Found</h2>
                <p className="text-muted-foreground max-w-md">
                  Add Markdown files to the <code className="bg-muted px-2 py-1 rounded">docs/</code> directory
                  in your project root. Files will automatically appear here.
                </p>
                <div className="mt-6 text-left bg-muted p-4 rounded-lg max-w-md">
                  <p className="text-sm font-mono">
                    docs/<br />
                    ├── README.md<br />
                    ├── ARCHITECTURE.md<br />
                    └── API_DESIGN.md
                  </p>
                </div>
              </div>
            ) : null}
          </div>
        </ScrollArea>
      </main>
    </div>
  )
}

export default App
