---
title: Mermaid Diagrams
order: 3
description: Examples of Mermaid diagram support
date: 2026-02-05
tags: [diagrams, mermaid, visualization]
---

# Mermaid Diagrams

This documentation site has native support for [Mermaid](https://mermaid.js.org/) diagrams. Simply use `mermaid` as the code fence language.

## Flow Chart Example

```mermaid
flowchart TD
    A[User Opens Docs] --> B{Docs Exist?}
    B -->|Yes| C[Load First Doc]
    B -->|No| D[Show Empty State]
    C --> E[Render Markdown]
    E --> F[Apply Syntax Highlighting]
    F --> G[Render Mermaid Diagrams]
    G --> H[Display Content]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant App
    participant DocLoader
    participant FileSystem

    User->>App: Open Documentation
    App->>DocLoader: getAllDocs()
    DocLoader->>FileSystem: import.meta.glob('docs/**/*.md')
    FileSystem-->>DocLoader: Markdown files
    DocLoader->>DocLoader: Parse frontmatter
    DocLoader-->>App: Sorted DocFile[]
    App->>User: Display first document
```

## Component Diagram

```mermaid
graph LR
    A[App] --> B[Sidebar]
    A --> C[Main Content]
    B --> D[ScrollArea]
    B --> E[Nav Items]
    C --> F[ScrollArea]
    C --> G[MarkdownRenderer]
    G --> H[react-markdown]
    H --> I[rehype-highlight]
    H --> J[Mermaid]
```

## Class Diagram

```mermaid
classDiagram
    class DocFile {
        +String slug
        +String filename
        +DocMetadata metadata
        +String content
        +String path
    }

    class DocMetadata {
        +String title
        +Number order
        +String description
        +String date
        +String[] tags
    }

    class NavItem {
        +String title
        +String slug
        +Number order
    }

    DocFile --> DocMetadata
```

## Entity Relationship Diagram

```mermaid
erDiagram
    DOCUMENT ||--|| METADATA : has
    DOCUMENT {
        string slug
        string filename
        string content
        string path
    }
    METADATA {
        string title
        number order
        string description
        string date
        array tags
    }
```

## Gantt Chart

```mermaid
gantt
    title Documentation Site Development
    dateFormat  YYYY-MM-DD
    section Setup
    Vite + React Setup     :done, setup1, 2026-02-05, 1d
    shadcn/ui Integration  :done, setup2, after setup1, 1d
    section Features
    Markdown Renderer      :done, feat1, 2026-02-05, 1d
    Mermaid Support        :done, feat2, after feat1, 1d
    Sidebar Navigation     :done, feat3, 2026-02-05, 1d
    section Testing
    Manual Testing         :active, test1, after feat3, 1d
```

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Loading
    Loading --> NoDocsFound: docs.length === 0
    Loading --> DocSelected: docs.length > 0
    NoDocsFound --> [*]
    DocSelected --> RenderingMarkdown
    RenderingMarkdown --> HighlightingCode
    HighlightingCode --> RenderingMermaid
    RenderingMermaid --> DisplayingContent
    DisplayingContent --> DocSelected: User clicks nav item
    DisplayingContent --> [*]
```

## Usage

To add a Mermaid diagram to your documentation:

1. Create a code fence with `mermaid` as the language
2. Add your Mermaid diagram syntax inside
3. The diagram will be automatically rendered when the page loads

## Supported Diagram Types

- Flowchart
- Sequence Diagram
- Class Diagram
- State Diagram
- Entity Relationship Diagram
- User Journey
- Gantt Chart
- Pie Chart
- Git Graph
- And more!

For full Mermaid syntax documentation, visit [mermaid.js.org](https://mermaid.js.org/).
