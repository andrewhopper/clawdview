# React Component Library Template

Gold standard template for React component libraries with TypeScript.

## Features

- **TypeScript**: Strict type safety
- **Vite**: Fast builds with library mode
- **Testing**: Vitest + React Testing Library
- **Components**: Button, Card, Input with docs
- **Hooks**: useToggle, useDebounce, useLocalStorage

## Quick Start

```bash
# Install dependencies
npm install

# Run Storybook/dev
npm run dev

# Build library
npm run build

# Run tests
npm test

# Type check
npm run typecheck
```

## Usage

```tsx
import { Button, Card, useToggle } from 'react-component-library';

function App() {
  const [isOpen, toggle] = useToggle(false);

  return (
    <Card header="My Card">
      <Button onClick={toggle}>
        {isOpen ? 'Close' : 'Open'}
      </Button>
    </Card>
  );
}
```

## Project Structure

```
typescript-react/
├── src/
│   ├── components/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   ├── hooks/
│   │   ├── useToggle.ts
│   │   ├── useDebounce.ts
│   │   └── useLocalStorage.ts
│   ├── utils/
│   │   ├── cn.ts
│   │   └── format.ts
│   └── index.ts
├── tests/
├── package.json
├── tsconfig.json
└── vite.config.ts
```
