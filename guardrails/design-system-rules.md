# Design System Guardrails

**Status:** Protected - requires human approval to modify
**Version:** 1.0.0
**Last Updated:** 2025-11-24

## 1.0 Purpose

Enforce consistent UI component patterns across all Vite+React projects to prevent:
- Component duplication (5-10+ implementations of buttons, modals, forms)
- Wasted engineering effort (50-200hrs per project rebuilding components)
- Inconsistent UX (different styles/patterns confuse users)
- Maintenance nightmare (bug fixes don't propagate)

## 2.0 Protected Design System

### 2.1 Required Stack

**ALL React web applications MUST use:**

1. **React** - UI framework
2. **Vite** - Build tool
3. **TypeScript** - Type safety
4. **Tailwind CSS** - Utility-first styling
5. **shadcn/ui** - Component library
   - Built on Radix UI primitives
   - Accessible by default
   - Customizable with Tailwind

### 2.2 Why shadcn/ui?

**Rationale:**
- **Copy-paste architecture** - Components live in your codebase (not node_modules)
- **Tailwind-native** - Uses utility classes, matches our styling approach
- **Accessible** - Built on Radix UI (ARIA-compliant)
- **Customizable** - Full control over component code
- **Type-safe** - TypeScript-first design
- **No framework lock-in** - Own the code, modify as needed

**Alternative Considered:** Material-UI, Chakra UI, Ant Design
**Rejected Because:** Heavy bundles, opinionated styles, harder to customize, doesn't match brand

## 3.0 Enforcement Rules

### 3.1 MUST Rules (Errors)

❌ **MUST NOT use raw HTML elements for interactive components**
```tsx
// ❌ PROHIBITED
<button className="...">Click me</button>
<input type="text" />
<select>...</select>

// ✅ REQUIRED
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select } from "@/components/ui/select"
```

❌ **MUST NOT create custom button/input/modal components**
```tsx
// ❌ PROHIBITED - creating custom basic components
export const CustomButton = ({ children }) => (
  <button className="custom-btn">{children}</button>
)

// ✅ REQUIRED - extend shadcn components
import { Button } from "@/components/ui/button"
export const PrimaryButton = (props) => (
  <Button variant="default" {...props} />
)
```

❌ **MUST NOT use inline styles**
```tsx
// ❌ PROHIBITED
<div style={{ color: 'blue', padding: '10px' }}>...</div>

// ✅ REQUIRED - use Tailwind utilities
<div className="text-blue-500 p-2.5">...</div>
```

❌ **MUST NOT import CSS files (except globals)**
```tsx
// ❌ PROHIBITED
import './Button.css'
import styles from './Button.module.css'

// ✅ REQUIRED - use Tailwind or shadcn components
import { Button } from "@/components/ui/button"
```

### 3.2 SHOULD Rules (Warnings)

⚠️ **SHOULD use shadcn/ui components for common patterns**

| Pattern | shadcn/ui Component | Prohibited Alternative |
|---------|---------------------|------------------------|
| Buttons | `<Button>` | `<button>`, custom components |
| Forms | `<Form>`, `<Input>`, `<Label>` | Raw HTML form elements |
| Modals | `<Dialog>` | Custom modal, `<div>` overlays |
| Dropdowns | `<DropdownMenu>`, `<Select>` | Custom dropdowns, `<select>` |
| Cards | `<Card>` | Custom card divs |
| Toasts | `<Toast>` | Custom notification systems |
| Popovers | `<Popover>` | Custom tooltips/popovers |
| Tabs | `<Tabs>` | Custom tab implementations |
| Alerts | `<Alert>` | Custom alert boxes |

⚠️ **SHOULD use Tailwind utilities over custom CSS**
- Prefer: `className="flex items-center gap-4"`
- Avoid: Custom flexbox CSS classes

⚠️ **SHOULD use shadcn theme variables**
```tsx
// ✅ REQUIRED - use CSS variables
className="bg-primary text-primary-foreground"

// ❌ AVOID - hardcoded colors
className="bg-blue-500 text-white"
```

### 3.3 Component Exceptions

**When you CAN create custom components:**

✅ **Business-specific components**
```tsx
// ✅ OK - domain-specific component using shadcn primitives
export const ProductCard = ({ product }) => (
  <Card>
    <CardHeader><CardTitle>{product.name}</CardTitle></CardHeader>
    <CardContent>...</CardContent>
  </Card>
)
```

✅ **Composite patterns**
```tsx
// ✅ OK - combining multiple shadcn components
export const SearchBar = () => (
  <div className="flex gap-2">
    <Input placeholder="Search..." />
    <Button>Search</Button>
  </div>
)
```

✅ **Layout components**
```tsx
// ✅ OK - layout-specific components
export const PageLayout = ({ children }) => (
  <div className="min-h-screen flex flex-col">{children}</div>
)
```

## 4.0 Required Setup

### 4.1 File Structure
```
src/
├── components/
│   ├── ui/              # shadcn components (auto-generated)
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   └── business/        # Custom business components
│       ├── ProductCard.tsx
│       ├── UserProfile.tsx
│       └── ...
├── lib/
│   └── utils.ts         # cn() utility for className merging
└── ...
```

### 4.2 Required Config Files

**components.json** - shadcn/ui configuration
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

**tailwind.config.js** - Must include shadcn setup
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // ... other theme colors
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

**src/lib/utils.ts** - className merging utility
```ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## 5.0 Migration Path

### 5.1 For New Projects

1. ✅ Initialize with Vite + React + TypeScript
2. ✅ Install shadcn/ui: `npx shadcn-ui@latest init`
3. ✅ Add components as needed: `npx shadcn-ui@latest add button`
4. ✅ Use components in your code

### 5.2 For Existing Projects

**Phase 1: Audit**
- Run UAT validation: `./bin/run -c web src/`
- Identify violations: raw buttons, custom components, inline styles

**Phase 2: Install shadcn/ui**
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input dialog card
```

**Phase 3: Replace Components**
- Replace `<button>` → `<Button>` from shadcn
- Replace custom modals → `<Dialog>` from shadcn
- Replace custom inputs → `<Input>` from shadcn

**Phase 4: Enable Enforcement**
- Add ESLint rules (see Layer 2)
- Add Vite plugin (see Layer 3)
- Test build: `npm run build`

## 6.0 Enforcement Layers

### Layer 1: Guardrails (this document)
- Defines rules and rationale
- Protected file - requires approval to modify

### Layer 2: ESLint (development time)
- Errors: raw HTML interactive elements
- Warnings: missing shadcn imports
- Runs in IDE, on save, in CI

### Layer 3: Vite Plugin (build time)
- Blocks build if violations detected
- Prints violations with file paths
- Fails CI pipeline if rules broken

### Layer 4: Hook Validation (AI assistance)
- Validates files after Write/Edit operations
- Appends reminders to AI context
- Prompts AI to fix violations

## 7.0 Approval Required

**Human approval required for:**
- ❌ Adding component libraries OTHER than shadcn/ui
- ❌ Using CSS-in-JS (styled-components, emotion)
- ❌ Creating custom button/input/modal base components
- ❌ Disabling enforcement rules
- ❌ Modifying this guardrail file

**Auto-approved:**
- ✅ Adding more shadcn/ui components
- ✅ Creating business-specific composite components
- ✅ Extending shadcn components with variants
- ✅ Customizing Tailwind theme

## 8.0 Related Documents

**Pain Points:**
- `problems/pain-inconsistent-ui-components-t8c2d6.md` - The problem this solves

**Validation:**
- `prototypes/proto-uat-a4idz-001/validation_tests/web/rules.yaml` - Post-build checks

**Standards:**
- `shared/standards/code/react/README.md` - React patterns
- `shared/standards/code/vite/README.md` - Vite configuration

**Enforcement:**
- `shared/eslint-config/design-system.js` - ESLint rules (Layer 2)
- `shared/vite-plugins/design-system-validator.ts` - Vite plugin (Layer 3)
- `.claude/hooks/tool-result.sh` - AI validation hook (Layer 4)

## 9.0 Version History

**1.0.0** (2025-11-24)
- Initial design system guardrails
- Required stack: React + Vite + TypeScript + Tailwind + shadcn/ui
- 4-layer enforcement strategy
