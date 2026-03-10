# Documentation Strategy for Golden Repos

## Overview

This guide defines documentation standards across all golden repo templates.

## Documentation Layers

```
┌─────────────────────────────────────────────────┐
│  Layer 1: README.md (Entry Point)               │
│  - Quick start, installation, basic usage       │
├─────────────────────────────────────────────────┤
│  Layer 2: /docs/ (Detailed Guides)              │
│  - Architecture, tutorials, deployment          │
├─────────────────────────────────────────────────┤
│  Layer 3: API Reference (Generated)             │
│  - TypeDoc, Sphinx, Swagger/OpenAPI             │
├─────────────────────────────────────────────────┤
│  Layer 4: Inline Comments (Code)                │
│  - JSDoc/TSDoc, docstrings, complex logic       │
└─────────────────────────────────────────────────┘
```

## Documentation Platforms

### Mintlify (Recommended for Public Docs)
Modern, beautiful documentation with MDX support.

- **Config**: `docs/mint.json`
- **Format**: MDX with custom components
- **Features**: API playground, search, versioning
- **Templates**: `templates/docs/*.mdx`

```bash
# Install Mintlify CLI
npm i -g mintlify

# Start local preview
cd docs && mintlify dev

# Deploy
mintlify deploy
```

### When to Use Mintlify
- Public-facing API documentation
- Developer portals
- Product documentation
- When you need interactive API playground

## By Template Type

### TypeScript Templates
- **Code Docs**: TypeDoc
- **User Docs**: Mintlify or Docusaurus
- **Config**: `typedoc.json`
- **Output**: `docs/api/`
- **Comments**: TSDoc format

### Python Templates
- **Code Docs**: MkDocs + mkdocstrings
- **User Docs**: Mintlify or Sphinx
- **Config**: `mkdocs.yml`
- **Output**: `site/`
- **Comments**: Google-style docstrings

### API Templates (FastAPI, Express)
- **Interactive**: OpenAPI/Swagger (built-in at `/api/docs`)
- **User Docs**: Mintlify with OpenAPI import
- **Export**: `/api/docs.json` → `mint.json` openapi field

## File Structure

```
project/
├── README.md              # Quick start (required)
├── CONTRIBUTING.md        # How to contribute
├── CHANGELOG.md           # Version history
├── docs/
│   ├── index.md           # Docs home
│   ├── getting-started.md # Installation & setup
│   ├── architecture.md    # System design
│   ├── deployment.md      # Deploy guides
│   └── api/               # Generated API docs
├── typedoc.json           # TypeDoc config (TS)
└── mkdocs.yml             # MkDocs config (Python)
```

## README Template Structure

1. **Title & Badges** - Name, build status, version
2. **Description** - One paragraph, what it does
3. **Quick Start** - 3-5 commands to get running
4. **Features** - Bullet list of capabilities
5. **Installation** - Detailed setup steps
6. **Usage** - Code examples
7. **Configuration** - Environment variables, options
8. **API Reference** - Link to generated docs
9. **Contributing** - Link to CONTRIBUTING.md
10. **License** - License type

## Comment Standards

### TypeScript (TSDoc)
```typescript
/**
 * Creates a new user in the system.
 *
 * @param email - User's email address
 * @param options - Optional configuration
 * @returns The created user object
 * @throws {ValidationError} If email is invalid
 *
 * @example
 * ```ts
 * const user = await createUser('user@example.com');
 * ```
 */
```

### Python (Google-style)
```python
def create_user(email: str, options: dict | None = None) -> User:
    """Creates a new user in the system.

    Args:
        email: User's email address.
        options: Optional configuration dictionary.

    Returns:
        The created user object.

    Raises:
        ValidationError: If email is invalid.

    Example:
        >>> user = create_user('user@example.com')
    """
```

## When to Document

### Always Document
- Public APIs and exported functions
- Complex business logic
- Non-obvious algorithms
- Configuration options
- Error handling strategies

### Skip Documentation
- Self-explanatory code (`getUserById`)
- Internal implementation details
- Trivial getters/setters
- Test files (unless complex setup)

## Generated Docs Commands

```bash
# TypeScript - TypeDoc
npm run docs        # Generate docs
npm run docs:serve  # Serve locally

# Python - MkDocs
mkdocs build        # Generate docs
mkdocs serve        # Serve locally

# API - Export OpenAPI
curl http://localhost:3000/api/docs.json > openapi.json
```

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Generate docs
  run: npm run docs

- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    publish_dir: ./docs/api
```
