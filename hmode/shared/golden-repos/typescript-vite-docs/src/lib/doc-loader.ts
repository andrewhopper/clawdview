// File UUID: a7b8c9d0-1e2f-3a4b-5c6d-7e8f9a0b1c2d
import matter from 'gray-matter'
import { DocFile } from './types'

// This will be populated at build time with all markdown files
const docModules = import.meta.glob('../../docs/**/*.md', {
  eager: true,
  query: '?raw',
  import: 'default'
})

export function getAllDocs(): DocFile[] {
  const docs: DocFile[] = []

  for (const [path, content] of Object.entries(docModules)) {
    const rawContent = content as string
    const { data, content: markdownContent } = matter(rawContent)

    // Extract filename and slug from path
    const filename = path.split('/').pop()
    if (!filename) {
      console.error(`Invalid doc path: ${path}`)
      continue
    }
    const slug = filename.replace(/\.md$/, '')

    const doc: DocFile = {
      slug,
      filename,
      metadata: {
        title: data.title || slug,
        order: data.order || 999,
        description: data.description,
        date: data.date,
        tags: data.tags
      },
      content: markdownContent,
      path: path.replace('../../docs/', '')
    }

    docs.push(doc)
  }

  // Sort by order, then by title
  return docs.sort((a, b) => {
    const orderA = a.metadata.order ?? 999
    const orderB = b.metadata.order ?? 999

    if (orderA !== orderB) {
      return orderA - orderB
    }
    return a.metadata.title.localeCompare(b.metadata.title)
  })
}

export function getDocBySlug(slug: string): DocFile | undefined {
  const allDocs = getAllDocs()
  return allDocs.find(doc => doc.slug === slug)
}
