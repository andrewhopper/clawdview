---
title: Architecture
order: 2
description: System architecture and component design
date: 2026-02-05
tags: [architecture, design]
---

# Architecture

This documentation site follows a component-based architecture using React and shadcn/ui.

## System Overview

The documentation site consists of three main layers:

1. **Presentation Layer**: React components with shadcn/ui
2. **Data Layer**: Markdown file loading and parsing
3. **Rendering Layer**: Markdown-to-HTML conversion with plugins

## Component Hierarchy

```
App
├── Sidebar
│   ├── ScrollArea
│   └── Navigation Items
└── Main Content Area
    ├── ScrollArea
    └── MarkdownRenderer
```

## Data Flow

1. **Load Phase**: `getAllDocs()` scans `docs/` directory using Vite's `import.meta.glob`
2. **Parse Phase**: `gray-matter` extracts YAML frontmatter and content
3. **Sort Phase**: Documents sorted by `order` field, then alphabetically
4. **Render Phase**: `react-markdown` converts content to React components
5. **Enhancement Phase**: Plugins add syntax highlighting, Mermaid diagrams, and heading links

## Design System Integration

All components use design tokens from `shared/design-system/`:

- **Colors**: `hsl(var(--primary))`, `hsl(var(--background))`, etc.
- **Spacing**: Tailwind spacing scale aligned with `--space-*` tokens
- **Typography**: System font stack with consistent sizing
- **Components**: shadcn/ui components (ScrollArea, Separator, etc.)

## Key Technologies

| Technology | Purpose |
|------------|---------|
| React 18 | UI framework |
| Vite | Build tool and dev server |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| shadcn/ui | Component library |
| react-markdown | Markdown rendering |
| Mermaid | Diagram generation |
| gray-matter | YAML frontmatter parsing |

## File Structure

```
docs-site/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   ├── Sidebar.tsx      # Navigation sidebar
│   │   └── MarkdownRenderer.tsx  # Content renderer
│   ├── lib/
│   │   ├── doc-loader.ts    # File loading logic
│   │   ├── types.ts         # TypeScript interfaces
│   │   └── utils.ts         # Utility functions
│   ├── styles/
│   │   └── globals.css      # Design system tokens
│   ├── App.tsx              # Main application
│   └── main.tsx             # Entry point
└── docs/                    # Documentation files (parent dir)
```

## Hot Module Replacement

The Vite config includes a custom plugin that watches the `docs/` directory and triggers a full page reload when Markdown files change. This ensures documentation updates are immediately visible during development.
