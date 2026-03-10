# AWS Cloudscape Design System

AWS Cloudscape is a design system for building intuitive, engaging, and inclusive user experiences at scale. It's the same design system used by AWS Console.

## Quick Start

### Installation

```bash
cd shared/design-system/cloudscape
npm install
```

### For React/Vite Projects

1. Install dependencies in your project:
```bash
npm install @cloudscape-design/components @cloudscape-design/design-tokens @cloudscape-design/global-styles @cloudscape-design/collection-hooks
```

2. Import global styles in your app entry:
```tsx
import '@cloudscape-design/global-styles/index.css';
```

3. Use components:
```tsx
import {
  AppLayout,
  Container,
  Header,
  Button,
  SpaceBetween,
} from '@cloudscape-design/components';

function App() {
  return (
    <AppLayout
      content={
        <Container header={<Header variant="h1">Dashboard</Header>}>
          <SpaceBetween size="l">
            <Button variant="primary">Create Resource</Button>
          </SpaceBetween>
        </Container>
      }
    />
  );
}
```

## When to Use Cloudscape

| Use Case | Cloudscape | shadcn/ui |
|----------|------------|-----------|
| AWS Console-like apps | ✅ | |
| Data-heavy dashboards | ✅ | |
| Enterprise/B2B apps | ✅ | |
| Marketing sites | | ✅ |
| Consumer apps | | ✅ |
| Custom branding needed | | ✅ |

## Key Components

### Layout
- `AppLayout` - Main application shell with navigation, content, and tools
- `ContentLayout` - Content wrapper with header
- `Container` - Grouped content sections
- `Grid` / `ColumnLayout` - Layout utilities
- `SpaceBetween` - Consistent spacing

### Navigation
- `TopNavigation` - Primary navigation bar
- `SideNavigation` - Sidebar navigation
- `BreadcrumbGroup` - Breadcrumb trail
- `Tabs` - Tab navigation

### Forms
- `FormField` - Field wrapper with label, description, error
- `Input`, `Textarea`, `Select`, `Multiselect`
- `Checkbox`, `RadioGroup`, `Toggle`
- `DatePicker`, `FileUpload`

### Data Display
- `Table` - Feature-rich data tables (sorting, filtering, pagination)
- `Cards` - Card-based data display
- `KeyValuePairs` - Key-value display
- `StatusIndicator` - Status badges

### Feedback
- `Alert` - Inline alerts
- `Flashbar` - Stack of dismissible notifications
- `Modal` - Dialog windows
- `Spinner` - Loading indicator

## Design Tokens

Cloudscape uses CSS custom properties. Key tokens:

| Token | Usage |
|-------|-------|
| `--color-background-layout-main` | Main content background |
| `--color-text-body-default` | Default text |
| `--color-text-heading-default` | Heading text |
| `--color-border-divider-default` | Dividers |
| `--space-scaled-*` | Spacing (xxs to xxxl) |

## Dark Mode

```tsx
import { applyMode, Mode } from '@cloudscape-design/global-styles';

// Apply dark mode
applyMode(Mode.Dark);

// Apply light mode
applyMode(Mode.Light);
```

## Table with Collection Hooks

```tsx
import { Table, Header, Pagination, TextFilter } from '@cloudscape-design/components';
import { useCollection } from '@cloudscape-design/collection-hooks';

function DataTable({ items }) {
  const { items: filteredItems, filterProps, paginationProps } = useCollection(items, {
    filtering: {
      empty: 'No items',
      noMatch: 'No matches',
    },
    pagination: { pageSize: 10 },
    sorting: {},
  });

  return (
    <Table
      header={<Header>Resources</Header>}
      items={filteredItems}
      columnDefinitions={[
        { id: 'name', header: 'Name', cell: (item) => item.name },
        { id: 'status', header: 'Status', cell: (item) => item.status },
      ]}
      filter={<TextFilter {...filterProps} />}
      pagination={<Pagination {...paginationProps} />}
    />
  );
}
```

## Resources

- [Cloudscape Documentation](https://cloudscape.design/)
- [Component API Reference](https://cloudscape.design/components/)
- [Design Tokens](https://cloudscape.design/foundation/visual-foundation/design-tokens/)
- [GitHub Repository](https://github.com/cloudscape-design/components)
