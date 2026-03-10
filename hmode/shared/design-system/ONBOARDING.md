# Design System Onboarding Guide

How to add new design systems to the Protoflow monorepo.

## Overview

The design system architecture supports multiple design systems side-by-side. Each system lives in its own directory with independent dependencies, components, and documentation.

```
shared/design-system/
├── registry.yaml          # Central catalog of all design systems
├── README.md              # Main documentation
├── ONBOARDING.md          # This file
├── design-system/         # shadcn/ui (default)
├── cloudscape/            # AWS Cloudscape
└── <new-system>/          # Your new design system
```

## Step 1: Proposal

Before adding a new design system, document the rationale:

1. **Use Case**: What projects will use this system?
2. **Gap Analysis**: Why doesn't shadcn/ui or Cloudscape fit?
3. **Maintenance**: Who will maintain updates?
4. **Adoption**: Which existing projects might migrate?

Create an entry in `registry.yaml` with `status: proposed`:

```yaml
design_systems:
  my_system:
    name: "My Design System"
    status: proposed  # Mark as proposed initially
    description: "Why we need this"
    use_cases:
      - "Specific use case 1"
```

## Step 2: Directory Structure

Create the standard directory structure:

```bash
mkdir -p shared/design-system/<system-name>/{src/{components,lib},stories,templates}
```

Required files:
```
<system-name>/
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── README.md              # System-specific documentation
├── src/
│   ├── index.ts           # Main export
│   ├── globals.css        # Global styles (if applicable)
│   ├── components/
│   │   └── index.ts       # Component re-exports
│   └── lib/
│       └── utils.ts       # Utility functions
├── stories/               # Storybook stories (optional)
└── templates/             # HTML templates (optional)
```

## Step 3: Package Configuration

Create `package.json` with standard structure:

```json
{
  "name": "@protoflow/design-system-<name>",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./globals.css": "./src/globals.css",
    "./components": "./src/components/index.ts"
  },
  "scripts": {
    "dev": "storybook dev -p <unique-port>",
    "build": "storybook build -o storybook-static",
    "lint": "eslint . --ext ts,tsx",
    "test": "vitest"
  },
  "dependencies": {
    // Design system packages
  },
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    // Storybook, TypeScript, testing
  }
}
```

**Important**: Assign a unique Storybook port (check `registry.yaml` for used ports).

## Step 4: Component Exports

Create `src/components/index.ts` that re-exports from the design system:

```typescript
// Re-export components from the design system library
export {
  Button,
  type ButtonProps,
} from 'design-system-library';

// Add more components...
```

Benefits of re-exporting:
- Centralized import path
- Easy to add wrappers or defaults
- Consistent API across projects

## Step 5: Utility Functions

Create `src/lib/utils.ts` with system-specific helpers:

```typescript
/**
 * Utility functions for <Design System Name>
 */

// Common patterns for event handling, formatting, etc.
```

## Step 6: Global Styles

Create `src/globals.css`:

```css
/* Import the design system's base styles */
@import 'design-system-library/styles.css';

/* Custom overrides for Protoflow (optional) */
:root {
  /* CSS custom properties */
}
```

## Step 7: Documentation

Create `README.md` with:

1. **Quick Start** - Installation and basic usage
2. **When to Use** - Comparison table with other systems
3. **Key Components** - Most commonly used components
4. **Design Tokens** - How to customize
5. **Theme Support** - Dark/light mode
6. **Code Examples** - Common patterns
7. **Resources** - Links to official docs

## Step 8: Registry Update

Update `registry.yaml`:

```yaml
design_systems:
  my_system:
    name: "My Design System"
    path: "./<directory-name>"
    package: "@protoflow/design-system-<name>"
    version: "0.1.0"
    status: active  # Change from proposed to active
    description: "Brief description"
    use_cases:
      - "Use case 1"
      - "Use case 2"
    features:
      - "Feature 1"
      - "Feature 2"
    dependencies:
      # Key npm packages
    storybook_port: <unique-port>
```

## Step 9: Selection Guide Update

Add comparison criteria to `registry.yaml`:

```yaml
selection_guide:
  criteria:
    - name: "Visual Style"
      shadcn: "..."
      cloudscape: "..."
      my_system: "Description of visual style"
```

## Step 10: Testing

1. Run Storybook: `npm run dev`
2. Verify all exports work
3. Test in a sample project
4. Check TypeScript types resolve correctly

## Checklist

```
[ ] Proposal documented in registry.yaml
[ ] Directory structure created
[ ] package.json configured
[ ] tsconfig.json configured
[ ] Component exports created
[ ] Utility functions added
[ ] Global styles configured
[ ] README.md written
[ ] registry.yaml updated (status: active)
[ ] Selection guide updated
[ ] Storybook working
[ ] Tested in sample project
```

## Maintenance

### Version Updates

When the upstream design system releases updates:

1. Update version in `package.json`
2. Run `npm install`
3. Test for breaking changes
4. Update component exports if needed
5. Update README if API changed

### Deprecation

To deprecate a design system:

1. Set `status: deprecated` in `registry.yaml`
2. Add deprecation notice to README
3. Document migration path to alternative
4. Keep available for existing projects

## Examples

### Adding Material UI

```bash
# Create structure
mkdir -p shared/design-system/mui/{src/{components,lib},stories}

# Install dependencies
cd shared/design-system/mui
npm init -y
npm install @mui/material @emotion/react @emotion/styled
```

### Adding Ant Design

```bash
# Create structure
mkdir -p shared/design-system/antd/{src/{components,lib},stories}

# Install dependencies
cd shared/design-system/antd
npm init -y
npm install antd @ant-design/icons
```

## Questions?

Check existing implementations:
- `./design-system/` - shadcn/ui reference
- `./cloudscape/` - Cloudscape reference
