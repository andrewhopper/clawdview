---
title: Getting Started
order: 1
description: Introduction to the project documentation site and SDLC workflow
date: 2026-02-05
tags: [introduction, setup, sdlc]
---

# Getting Started

Welcome to the project documentation site! This is a live documentation viewer built with React, Vite, and TypeScript that automatically displays Markdown files from your `docs/` directory.

## Purpose: Living SDLC Workbench

This documentation site is designed to be set up **immediately after Phase 1 (SEED)** in the protoflow SDLC process. It serves as a living workbench where all phase artifacts are written as markdown and rendered in real-time.

### Why This Exists

1. **Visual Progress**: See your SDLC journey in the sidebar
2. **Living Documentation**: Write once, rendered beautifully
3. **No Context Switching**: Stay in your editor, see results instantly
4. **Stakeholder Friendly**: Share localhost URL for real-time review
5. **Searchable History**: All decisions documented and discoverable

## Features

- **Live Updates**: Documentation automatically refreshes when you edit .md files
- **Syntax Highlighting**: Code blocks with language-specific highlighting
- **Mermaid Diagrams**: Native support for Mermaid diagram rendering
- **Design System**: Uses shadcn/ui components and design tokens
- **Responsive**: Mobile-friendly navigation and content layout
- **Frontmatter Support**: Control page order, titles, and metadata with YAML frontmatter

## How It Works

1. Add Markdown files to the `docs/` directory in your project root
2. Add YAML frontmatter to control metadata (optional)
3. Run `npm run docs` to start the development server
4. Edit files and see changes instantly

## Frontmatter Options

```yaml
---
title: Page Title           # Display title (default: filename)
order: 1                    # Sort order in sidebar (default: 999)
description: Brief summary  # Page description
date: 2026-02-05           # Last updated date
tags: [tag1, tag2]         # Page tags
---
```

## Example Code Block

```typescript
interface DocMetadata {
  title: string
  order?: number
  description?: string
  date?: string
  tags?: string[]
}
```

## Using SDLC Templates

This template includes pre-structured templates for each SDLC phase in the `templates/` directory:

1. **Copy a template** when entering a new phase:
   ```bash
   cp docs-site/docs/templates/RESEARCH.template.md ../docs/RESEARCH.md
   ```

2. **Fill in the template** as you work through the phase

3. **See results live** - the docs site auto-updates as you type

### Available Templates

- `SEED.template.md` - Phase 1: Project vision and idea
- `RESEARCH.template.md` - Phase 2: Research findings
- `EXPANSION.template.md` - Phase 3: Alternative approaches
- `ANALYSIS.template.md` - Phase 4: Trade-off analysis
- `SELECTION.template.md` - Phase 5: Technology decisions
- `ARCHITECTURE.template.md` - Phase 6: System design
- `API_DESIGN.template.md` - Phase 6: API specifications
- `DATABASE_SCHEMA.template.md` - Phase 6: Data models
- `TEST_PLAN.template.md` - Phase 7: Testing strategy
- `.project.template` - Project metadata file

## Next Steps

- Check out the [Architecture](./ARCHITECTURE.md) example
- Learn about [Mermaid Diagrams](./DIAGRAMS.md)
- Browse the `templates/` directory for SDLC phase templates
