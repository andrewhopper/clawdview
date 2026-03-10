/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  // Add other env variables here
}

interface ImportMeta {
  readonly env: ImportMetaEnv
  glob: (pattern: string, options?: {
    eager?: boolean
    query?: string
    import?: string
  }) => Record<string, any>
}
