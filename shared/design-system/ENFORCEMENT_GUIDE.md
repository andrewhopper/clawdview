# Design System Enforcement Guide

**Complete guide to enforcing shadcn/ui design system across React+Vite projects.**

## Overview

This guide documents the **4-layer enforcement strategy** that ensures consistent UI component usage across all React projects in the Protoflow monorepo.

### The Problem

**Before enforcement:**
- 5-10 different implementations of buttons, modals, forms across projects
- 50-200 hours wasted per project rebuilding components
- Inconsistent UX confusing users
- Bug fixes don't propagate between projects

**After enforcement:**
- ✅ Consistent shadcn/ui components everywhere
- ✅ Build fails if raw HTML elements used
- ✅ AI automatically reminded to fix violations
- ✅ Violations caught at development, build, and AI-assistance time

### Pain Point

**Source:** `problems/pain-inconsistent-ui-components-t8c2d6.md`

**Impact:**
- 5,720-15,250 wasted lines of code
- $75k-200k in duplicated engineering effort
- Inconsistent user experiences

## 4-Layer Enforcement Strategy

```
┌─────────────────────────────────────────────────────┐
│ Layer 1: Guardrails (Rules Definition)             │
│   File: .guardrails/design-system-rules.md          │
│   Protected - requires human approval to modify     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Layer 2: ESLint (Development Time)                 │
│   Files: shared/eslint-config/                      │
│   Errors in IDE, on save, in editor                 │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Layer 3: Vite Plugin (Build Time)                  │
│   Files: shared/vite-plugins/                       │
│   Blocks build if violations detected               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Layer 4: Hook Validation (AI Assistance)           │
│   Files: .claude/hooks/tool-result.sh               │
│           .guardrails/ai-steering/                   │
│   Reminds AI to fix violations in real-time         │
└─────────────────────────────────────────────────────┘
```

### Why 4 Layers?

**Defense in depth:**
- **Layer 1** defines the rules (source of truth)
- **Layer 2** catches violations during development (fast feedback)
- **Layer 3** blocks production builds (safety net)
- **Layer 4** guides AI to follow rules (proactive)

## Layer 1: Guardrails

**File:** `.guardrails/design-system-rules.md`

**Purpose:** Defines the rules and rationale for design system enforcement.

**Protected:** Requires human approval to modify.

### Core Rules

❌ **PROHIBITED:**
- Raw HTML elements: `<button>`, `<input>`, `<select>`, `<textarea>`, `<dialog>`
- Inline styles: `style={{...}}`
- CSS module imports (except globals)
- Custom button/input/modal base components

✅ **REQUIRED:**
- shadcn/ui components for all interactive elements
- Tailwind utilities for styling
- TypeScript with strict types

### Required Stack

**ALL React projects MUST use:**
1. React
2. Vite
3. TypeScript
4. Tailwind CSS
5. shadcn/ui

### Reading the Guardrails

```bash
cat .guardrails/design-system-rules.md
```

## Layer 2: ESLint Configuration

**Location:** `shared/eslint-config/`

**Files:**
- `design-system.js` - Design system rules only
- `react-vite.js` - Full React+Vite config with design system
- `package.json` - Package metadata
- `README.md` - Usage docs

### Installation

#### Option 1: Monorepo Projects

```bash
# In your Vite project
npm install --save-dev file:../../shared/eslint-config
```

**.eslintrc.cjs:**
```js
module.exports = {
  extends: ['@protoflow/eslint-config-design-system/react-vite']
}
```

#### Option 2: External Projects

Copy files:
```bash
cp shared/eslint-config/design-system.js .eslint/
```

Then extend in `.eslintrc.cjs`:
```js
module.exports = {
  extends: [
    'eslint:recommended',
    './.eslint/design-system.js',
  ]
}
```

### Rules Enforced

**Errors (build-blocking):**
- `no-restricted-syntax` - Prohibits raw HTML interactive elements
- `react/forbid-dom-props` - Prohibits inline `style` prop

**Exceptions:**
- Test files: `*.test.tsx`, `*.spec.tsx`
- Story files: `*.stories.tsx`
- shadcn components: `components/ui/**/*.tsx`

### IDE Integration

**VS Code** (`.vscode/settings.json`):
```json
{
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

### Testing

```bash
# Lint all files
npm run lint

# Test specific file
npx eslint src/components/MyComponent.tsx

# Auto-fix violations
npx eslint src/ --fix
```

## Layer 3: Vite Plugin

**Location:** `shared/vite-plugins/`

**Files:**
- `design-system-validator.ts` - Vite plugin
- `package.json` - Package metadata
- `README.md` - Usage docs

### Installation

```bash
npm install --save-dev file:../../shared/vite-plugins
```

**vite.config.ts:**
```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { designSystemValidator } from '@protoflow/vite-plugins/design-system-validator'

export default defineConfig({
  plugins: [
    react(),
    designSystemValidator({
      strict: true,      // Fail build on errors
      verbose: true,     // Print all violations
    }),
  ],
})
```

### Build-Time Validation

```bash
# Production build (automatic validation)
npm run build
```

**Output if violations found:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 DESIGN SYSTEM VIOLATIONS DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ 1 ERROR(S):

  src/components/MyComponent.tsx:15:8
  Raw <button> prohibited. Use <Button> from shadcn/ui
  Fix: import { Button } from "@/components/ui/button"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Build fails**, preventing deployment of non-compliant code.

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `strict` | `boolean` | `true` | Fail build on violations |
| `verbose` | `boolean` | `false` | Print all violations |
| `include` | `string[]` | `['src/**/*.tsx', 'src/**/*.jsx']` | Files to validate |
| `exclude` | `string[]` | See docs | Files to skip |

## Layer 4: Hook Validation

**Location:**
- `.claude/hooks/tool-result.sh` - Hook that runs after file operations
- `.guardrails/ai-steering/design_system_validator.py` - Python validator

### How It Works

```
User: "Create a contact form component"
   ↓
AI: Uses Write tool to create component
   ↓
tool-result.sh hook runs
   ↓
design_system_validator.py checks file
   ↓
If violations found → Append reminder to tool output
   ↓
AI sees reminder and fixes violations
```

### Example Flow

**AI creates file with violation:**
```tsx
// ContactForm.tsx
export function ContactForm() {
  return (
    <form>
      <input type="text" placeholder="Name" />
      <button type="submit">Submit</button>
    </form>
  )
}
```

**Hook detects violations:**
```
File created successfully at: src/components/ContactForm.tsx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 DESIGN SYSTEM GUARDRAIL REMINDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ 2 DESIGN SYSTEM ERROR(S) in src/components/ContactForm.tsx:

  Line 4: Raw <input> prohibited
  Fix: Use <Input> from shadcn/ui: import { Input } from '@/components/ui/input'

  Line 5: Raw <button> prohibited
  Fix: Use <Button> from shadcn/ui: import { Button } from '@/components/ui/button'

📋 REQUIRED ACTION:
  Fix violations above by using shadcn/ui components instead of raw HTML.
  See: .guardrails/design-system-rules.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**AI automatically fixes:**
```tsx
// ContactForm.tsx (fixed)
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export function ContactForm() {
  return (
    <form>
      <Input type="text" placeholder="Name" />
      <Button type="submit">Submit</Button>
    </form>
  )
}
```

### Manual Testing

Test validator directly:
```bash
# Validate a file
python3 .guardrails/ai-steering/design_system_validator.py validate src/App.tsx

# Check format (for hook)
python3 .guardrails/ai-steering/design_system_validator.py check src/App.tsx
```

## Quick Start: New Project

### 1. Initialize Vite + React + TypeScript

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```

### 2. Install shadcn/ui

```bash
npx shadcn-ui@latest init
```

Answer prompts:
- Style: **Default**
- Color: **Slate**
- CSS variables: **Yes**

### 3. Install ESLint Config

```bash
npm install --save-dev file:../../shared/eslint-config
```

**.eslintrc.cjs:**
```js
module.exports = {
  extends: ['@protoflow/eslint-config-design-system/react-vite']
}
```

### 4. Install Vite Plugin

```bash
npm install --save-dev file:../../shared/vite-plugins
```

**vite.config.ts:**
```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { designSystemValidator } from '@protoflow/vite-plugins/design-system-validator'

export default defineConfig({
  plugins: [
    react(),
    designSystemValidator(),
  ],
})
```

### 5. Add shadcn Components

```bash
npx shadcn-ui@latest add button input dialog card
```

### 6. Test Enforcement

Create a test file with violations:

**src/Test.tsx:**
```tsx
export function Test() {
  return <button>Test</button>  // ❌ Should error
}
```

Run lint:
```bash
npm run lint
# ❌ Should show error: Raw <button> prohibited
```

Run build:
```bash
npm run build
# ❌ Should fail with design system violation
```

Fix the violation:
```tsx
import { Button } from "@/components/ui/button"

export function Test() {
  return <Button>Test</Button>  // ✅ Correct
}
```

Run again:
```bash
npm run lint  # ✅ Passes
npm run build # ✅ Passes
```

## Quick Start: Existing Project

### 1. Audit Current State

Check for violations:
```bash
# Install UAT validator
cd prototypes/proto-uat-a4idz-001

# Run web validation
./bin/run -c web ../../my-app/src/
```

Review violations:
- Count of raw HTML elements
- Inline styles
- Missing shadcn/ui imports

### 2. Install shadcn/ui

```bash
cd my-app
npx shadcn-ui@latest init
```

### 3. Add Components

Install commonly-used components:
```bash
npx shadcn-ui@latest add button input dialog card form select textarea
```

### 4. Replace Violations

**Before:**
```tsx
<button onClick={handleClick}>Submit</button>
<input type="text" value={name} onChange={handleChange} />
```

**After:**
```tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

<Button onClick={handleClick}>Submit</Button>
<Input type="text" value={name} onChange={handleChange} />
```

### 5. Enable Enforcement

Install ESLint config and Vite plugin (see Quick Start above).

### 6. Test

```bash
npm run lint   # Check for violations
npm run build  # Should pass if all fixed
```

## Violation Examples & Fixes

### Raw Button

```tsx
// ❌ VIOLATION
<button onClick={handleClick}>Click me</button>

// ✅ FIX
import { Button } from "@/components/ui/button"
<Button onClick={handleClick}>Click me</Button>
```

### Raw Input

```tsx
// ❌ VIOLATION
<input type="text" value={name} onChange={handleChange} />

// ✅ FIX
import { Input } from "@/components/ui/input"
<Input type="text" value={name} onChange={handleChange} />
```

### Inline Styles

```tsx
// ❌ VIOLATION
<div style={{ color: 'blue', padding: '10px' }}>Hello</div>

// ✅ FIX
<div className="text-blue-500 p-2.5">Hello</div>
```

### Raw Select

```tsx
// ❌ VIOLATION
<select>
  <option value="1">Option 1</option>
</select>

// ✅ FIX
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"

<Select>
  <SelectTrigger>
    <SelectValue placeholder="Select option" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="1">Option 1</SelectItem>
  </SelectContent>
</Select>
```

### Raw Textarea

```tsx
// ❌ VIOLATION
<textarea value={bio} onChange={handleChange} />

// ✅ FIX
import { Textarea } from "@/components/ui/textarea"
<Textarea value={bio} onChange={handleChange} />
```

## Exceptions

**When raw HTML IS allowed:**

✅ **Test files:** `*.test.tsx`, `*.spec.tsx`
✅ **Storybook:** `*.stories.tsx`
✅ **shadcn components:** `components/ui/**/*.tsx`
✅ **Non-interactive elements:** `<div>`, `<p>`, `<span>`, etc.

**Still enforced:**
- ❌ Inline styles (`style={{}}`)
- ❌ CSS imports (except `index.css`, `globals.css`)

## Disabling Enforcement (NOT RECOMMENDED)

### Disable ESLint Rule

```tsx
/* eslint-disable no-restricted-syntax */
<button>Temporary button</button>
/* eslint-enable no-restricted-syntax */
```

### Disable Vite Plugin

```ts
// vite.config.ts
export default defineConfig({
  plugins: [
    react(),
    // designSystemValidator(), // ← Commented out
  ],
})
```

**⚠️ WARNING:** Disabling defeats the purpose of enforcement!

## CI/CD Integration

### GitHub Actions

**.github/workflows/ci.yml:**
```yaml
name: CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run lint  # ← Catches violations

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm run build  # ← Blocks if violations
```

### Pre-commit Hook

**Using Husky:**
```bash
npm install --save-dev husky
npx husky install
npx husky add .husky/pre-commit "npm run lint"
```

**.husky/pre-commit:**
```bash
#!/bin/sh
npm run lint
```

Commit blocked if violations detected.

## Troubleshooting

### ESLint Not Detecting Violations

**Check:**
1. `.eslintrc.cjs` extends design system config
2. ESLint plugin installed: `npm install --save-dev eslint-plugin-react`
3. Run: `npx eslint src/ --ext .tsx,.jsx`

### Vite Plugin Not Running

**Check:**
1. Plugin imported in `vite.config.ts`
2. Plugin added to `plugins` array
3. Build command: `npm run build` (not `npm run dev`)

### False Positives

**Check:**
1. File excluded in `exclude` patterns
2. File is test/story file
3. Component in `components/ui/` directory

### Hook Not Triggering

**Check:**
1. Hook executable: `chmod +x .claude/hooks/tool-result.sh`
2. Python validator executable: `chmod +x .guardrails/ai-steering/design_system_validator.py`
3. Test manually: `python3 .guardrails/ai-steering/design_system_validator.py check src/App.tsx`

## File Locations

```
protoflow/
├── .guardrails/
│   ├── design-system-rules.md                    # Layer 1: Rules definition
│   └── ai-steering/
│       └── design_system_validator.py            # Layer 4: Python validator
├── .claude/
│   └── hooks/
│       └── tool-result.sh                        # Layer 4: Hook integration
├── shared/
│   ├── eslint-config/                            # Layer 2: ESLint rules
│   │   ├── design-system.js
│   │   ├── react-vite.js
│   │   ├── package.json
│   │   └── README.md
│   ├── vite-plugins/                             # Layer 3: Vite plugin
│   │   ├── design-system-validator.ts
│   │   ├── package.json
│   │   └── README.md
│   └── design-system/
│       └── ENFORCEMENT_GUIDE.md                  # This file
└── prototypes/proto-uat-a4idz-001/               # Validation testing
    └── validation_tests/web/rules.yaml
```

## Related Documents

**Problem Statement:**
- `problems/pain-inconsistent-ui-components-t8c2d6.md` - The pain this solves

**Guardrails:**
- `.guardrails/design-system-rules.md` - Protected rules definition

**Layer Documentation:**
- `shared/eslint-config/README.md` - ESLint usage
- `shared/vite-plugins/README.md` - Vite plugin usage

**Standards:**
- `shared/standards/code/react/README.md` - React patterns
- `shared/standards/code/vite/README.md` - Vite configuration

## Version History

**1.0.0** (2025-11-24)
- Initial 4-layer enforcement strategy
- Layer 1: Guardrails
- Layer 2: ESLint configuration
- Layer 3: Vite plugin
- Layer 4: Hook validation
- Complete documentation

## Summary

**4-layer enforcement ensures:**
✅ Consistent shadcn/ui components across all projects
✅ No raw HTML interactive elements
✅ No inline styles
✅ Build fails if violations detected
✅ AI automatically reminded to fix violations

**Result:**
- **Zero component duplication**
- **Consistent UX across all projects**
- **$75k-200k engineering savings**
- **Automatic enforcement** at development, build, and AI time

**Next Steps:**
1. Apply to new projects immediately
2. Migrate existing projects incrementally
3. Monitor compliance via CI/CD
