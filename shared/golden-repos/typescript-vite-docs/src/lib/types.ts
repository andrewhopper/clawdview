// File UUID: c3d4e5f6-7a8b-9c0d-1e2f-3a4b5c6d7e8f

export interface DocMetadata {
  title: string
  order?: number
  description?: string
  date?: string
  tags?: string[]
}

export interface DocFile {
  slug: string
  filename: string
  metadata: DocMetadata
  content: string
  path: string
}

export interface NavItem {
  title: string
  slug: string
  order: number
}
