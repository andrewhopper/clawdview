# TypeScript Ink CLI Template

Gold standard TypeScript CLI template using React and Ink for beautiful terminal UIs.

## Features

- Ink for React-based terminal UI
- Meow for argument parsing
- Built-in components (spinner, select menu, text input)
- Vitest for testing

## Getting Started

```bash
# Install dependencies
npm install

# Development mode
npm run dev -- greet World

# Build
npm run build

# Run built CLI
npm start -- greet World

# Run tests
npm test
```

## Commands

```bash
# Greet command
mycli greet <name> [--loud]

# Process command
mycli process <files...> [--dry-run]
```

## Project Structure

```
src/
├── cli.tsx          # CLI entry point
├── App.tsx          # Default component
├── commands/        # Command components
│   ├── Greet.tsx
│   └── Process.tsx
└── components/      # Reusable UI components
    ├── SelectMenu.tsx
    └── TextPrompt.tsx
```

## Creating New Commands

1. Create a new component in `src/commands/`
2. Add the command case in `cli.tsx`
3. Update the help text in meow config

## Available Components

### SelectMenu

Interactive selection menu:
```tsx
<SelectMenu
  title="Choose an option"
  items={[
    { label: 'Option 1', value: 1 },
    { label: 'Option 2', value: 2 },
  ]}
  onSelect={(item) => console.log(item.value)}
/>
```

### TextPrompt

Text input prompt:
```tsx
<TextPrompt
  prompt="Enter your name"
  placeholder="John Doe"
  onSubmit={(value) => console.log(value)}
/>
```
