# CLI Tools with React Ink

**Status**: Approved
**Last Updated**: 2025-11-19

## Overview

For interactive terminal applications, use React Ink for component-based UI rendering with familiar React patterns.

## Core Stack

**UI Framework**: React Ink v5
- Component-based terminal UI
- Hooks support (useState, useEffect, useInput)
- Terminal dimension awareness (useStdout)

**Required Dependencies**:
```json
{
  "dependencies": {
    "ink": "^5.0.1",
    "react": "^18.3.1"
  }
}
```

## Common Patterns

### 1. CLI Entry Point

```typescript
#!/usr/bin/env node
import { render } from 'ink'
import React from 'react'
import App from './App.js'

render(<App />)
```

### 2. Input Handling

Use `useInput` hook for keyboard navigation:

```typescript
import { useInput } from 'ink'

useInput((input, key) => {
  if (key.upArrow) handleUp()
  if (key.downArrow) handleDown()
  if (key.return) handleSelect()
  if (key.escape) process.exit(0)
})
```

### 3. Terminal Size Awareness

```typescript
import { useStdout } from 'ink'

const { stdout } = useStdout()
const terminalHeight = stdout?.rows || 24
const MAX_VISIBLE = Math.max(5, terminalHeight - 6)
```

### 4. Layout Patterns

**List View with Selection**:
```typescript
<Box flexDirection="column">
  {items.map((item, index) => (
    <Box key={item.id}>
      <Text inverse={index === selectedIndex}>
        {item.name}
      </Text>
    </Box>
  ))}
</Box>
```

**Scrollable List**:
```typescript
{items.slice(scrollOffset, scrollOffset + MAX_VISIBLE).map((item, index) => {
  const actualIndex = scrollOffset + index
  const isSelected = actualIndex === selectedIndex
  // render item
})}
```

### 5. Search/Filter with Fuse.js

```typescript
import Fuse from 'fuse.js'

const fuse = new Fuse(items, {
  keys: ['name', 'description'],
  threshold: 0.4
})

const results = fuse.search(query).map(r => r.item)
```

### 6. Text Input

```typescript
import TextInput from 'ink-text-input'

<TextInput
  value={query}
  onChange={setQuery}
  placeholder="Type to filter..."
/>
```

## UI Components

### Standard Components

**Box**: Container with flexbox layout
```typescript
<Box flexDirection="column" padding={1}>
  <Box marginBottom={1}>
    <Text bold>Label: </Text>
    <Text>Value</Text>
  </Box>
</Box>
```

**Text**: Styled text output
```typescript
<Text bold color="blue">Bold blue text</Text>
<Text dimColor>Dimmed text</Text>
<Text inverse>Inverted (selected)</Text>
```

### Custom UI Patterns

**Table Header**:
```typescript
<Box width="100%">
  <Box width={4}><Text bold>COL1</Text></Box>
  <Box width={35}><Text bold>COL2</Text></Box>
  <Box flexGrow={1}><Text bold>COL3</Text></Box>
</Box>
```

**Bordered Section**:
```typescript
<Box borderStyle="round" padding={1}>
  <Text>Content</Text>
</Box>
```

**Status Indicators**:
```typescript
<Text>{isRunning ? '🟢' : '⚪'} Status</Text>
```

## Build & Distribution

### TypeScript Configuration

Use separate config for CLI builds:

**tsconfig.cli.json**:
```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist/cli",
    "module": "ESNext",
    "target": "ES2022"
  },
  "include": ["src/cli/**/*"]
}
```

### Build Script

```javascript
#!/usr/bin/env node
import { execSync } from 'child_process'
import { writeFileSync, readFileSync } from 'fs'

// Compile TypeScript
execSync('npx tsc --project tsconfig.cli.json', { stdio: 'inherit' })

// Make executable
execSync('chmod +x dist/cli/launcher.js')

// Add shebang
const content = readFileSync('dist/cli/launcher.js', 'utf8')
if (!content.startsWith('#!/usr/bin/env node')) {
  writeFileSync('dist/cli/launcher.js', '#!/usr/bin/env node\n' + content)
}
```

### Package.json

```json
{
  "bin": {
    "app-name": "./dist/cli/launcher.js"
  },
  "scripts": {
    "build:cli": "node build-cli.js",
    "start:cli": "./dist/cli/launcher.js"
  }
}
```

## Common Add-ons

**Fuzzy Search**: `fuse.js`
**Text Input**: `ink-text-input`
**Spinner**: `ink-spinner`
**Select Input**: `ink-select-input`

## Best Practices

1. **Clear on Mount**: `console.clear()` in useEffect
2. **Full Terminal Height**: Calculate visible items from `stdout.rows`
3. **Keyboard Navigation**: Arrow keys + Enter/Escape standard
4. **Inverse Text for Selection**: Use `<Text inverse>` for selected items
5. **Exit on Escape**: `if (key.escape) process.exit(0)`
6. **Detached Processes**: Use `spawn(..., { detached: true })` for launched apps
7. **PID Management**: Track spawned processes for status display

## Anti-patterns

❌ **Don't** use console.log in render (use Text components)
❌ **Don't** assume fixed terminal size (use `useStdout`)
❌ **Don't** forget shebang (`#!/usr/bin/env node`)
❌ **Don't** use `stdin` mode (breaks with piped input)
❌ **Don't** hard-code terminal dimensions

## Related Preferences

- See `nodejs-cli-tools.md` for Commander.js integration
- See `typescript-config.md` for TypeScript setup
