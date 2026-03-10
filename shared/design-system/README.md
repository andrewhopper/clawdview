# Design Systems

Multi-design-system architecture supporting different UI needs across prototypes and production sites.

## Available Design Systems

| System | Package | Best For | Storybook |
|--------|---------|----------|-----------|
| **shadcn/ui** (default) | `@protoflow/design-system` | Marketing, consumer apps, custom branding | `:6006` |
| **AWS Cloudscape** | `@protoflow/design-system-cloudscape` | Enterprise dashboards, AWS-style apps | `:6007` |

### Choosing a Design System

```
┌─────────────────────────────────────────────────────────────────┐
│                    Which design system?                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AWS Console-like app? ──────────────────────▶ Cloudscape       │
│  Data-heavy dashboard? ──────────────────────▶ Cloudscape       │
│  Enterprise/internal tool? ──────────────────▶ Cloudscape       │
│                                                                 │
│  Marketing site? ────────────────────────────▶ shadcn/ui        │
│  Consumer app? ──────────────────────────────▶ shadcn/ui        │
│  Need custom branding? ──────────────────────▶ shadcn/ui        │
│  HTML mockup (no build)? ────────────────────▶ shadcn/ui        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Registry:** See `registry.yaml` for full comparison and selection guide.

**Adding new systems:** See `ONBOARDING.md` for documentation on adding additional design systems.

---

# shadcn/ui (Default)

Shared design system based on shadcn/ui for consistent styling across mockups, prototypes, and production sites.

## Quick Start

### For HTML Mockups (No Build Required)

Copy a template and customize:

```bash
cp shared/design-system/templates/mockup.html prototypes/proto-xxx/docs/mockups/my-mockup.html
cp shared/design-system/templates/microsite.html prototypes/proto-xxx/docs/site/index.html
```

Templates include:
- Tailwind CDN with shadcn config
- CSS variables for light/dark themes
- Pre-built component classes (btn, card, input, badge, alert)

### For React/Next.js/Vite Projects

1. Copy globals.css and tailwind.config.ts:
```bash
cp shared/design-system/src/globals.css src/
cp shared/design-system/tailwind.config.ts ./
```

2. Copy components you need:
```bash
cp -r shared/design-system/src/components/ui src/components/
cp -r shared/design-system/src/components/layout src/components/
cp shared/design-system/src/lib/utils.ts src/lib/
```

3. Install dependencies:
```bash
npm install @radix-ui/react-slot @radix-ui/react-label @radix-ui/react-separator class-variance-authority clsx tailwind-merge
```

## File Structure

```
design-system/
├── src/
│   ├── globals.css              # CSS variables + Tailwind base
│   ├── index.ts                 # Main export
│   ├── lib/
│   │   └── utils.ts             # cn() utility
│   └── components/
│       ├── ui/                  # shadcn/ui components
│       │   ├── alert.tsx
│       │   ├── badge.tsx
│       │   ├── button.tsx
│       │   ├── card.tsx
│       │   ├── input.tsx
│       │   ├── label.tsx
│       │   ├── separator.tsx
│       │   ├── textarea.tsx
│       │   └── index.ts
│       └── layout/              # Layout components
│           ├── container.tsx
│           ├── header.tsx
│           ├── sidebar.tsx
│           ├── footer.tsx
│           └── index.ts
├── stories/                     # Storybook stories
│   ├── Button.stories.tsx
│   ├── Card.stories.tsx
│   └── Layout.stories.tsx
├── templates/                   # Standalone HTML templates
│   ├── mockup.html              # General mockup template
│   └── microsite.html           # Landing page template
├── .storybook/                  # Storybook config
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## Design Tokens

### Colors (Dark Theme Default)

| Token | HSL | Usage |
|-------|-----|-------|
| `--background` | 240 10% 3.9% | Page background |
| `--foreground` | 0 0% 98% | Primary text |
| `--card` | 240 10% 3.9% | Card backgrounds |
| `--primary` | 0 0% 98% | Primary buttons, links |
| `--secondary` | 240 3.7% 15.9% | Secondary elements |
| `--muted` | 240 3.7% 15.9% | Muted backgrounds |
| `--muted-foreground` | 240 5% 64.9% | Secondary text |
| `--accent` | 240 3.7% 15.9% | Hover states |
| `--destructive` | 0 62.8% 30.6% | Error states |
| `--border` | 240 3.7% 15.9% | Borders |
| `--ring` | 240 4.9% 83.9% | Focus rings |

### Typography

- **Font**: System font stack (Inter recommended)
- **Base size**: 16px
- **Scale**: text-xs (12px) → text-7xl (72px)

### Spacing

Standard Tailwind spacing: 0.25rem (1) → 24rem (96)

### Border Radius

- `--radius`: 0.5rem (default)
- `radius-lg`: var(--radius)
- `radius-md`: calc(var(--radius) - 2px)
- `radius-sm`: calc(var(--radius) - 4px)

## Components

### UI Components

| Component | Variants | Props |
|-----------|----------|-------|
| Button | default, destructive, outline, secondary, ghost, link | size: default, sm, lg, icon |
| Card | - | CardHeader, CardTitle, CardDescription, CardContent, CardFooter |
| Input | - | All native input props |
| Textarea | - | All native textarea props |
| Badge | default, secondary, destructive, outline | - |
| Alert | default, destructive | AlertTitle, AlertDescription |
| Label | - | All native label props |
| Separator | horizontal, vertical | decorative |

### Layout Components

| Component | Subcomponents | Props |
|-----------|---------------|-------|
| Container | - | size: sm, md, lg, xl, full |
| Header | HeaderTitle, HeaderNav, HeaderActions | sticky: boolean |
| Sidebar | SidebarHeader, SidebarContent, SidebarFooter, SidebarNav, SidebarNavItem | collapsed: boolean |
| Footer | FooterContent, FooterText, FooterLinks, FooterLink | - |

## Storybook

Run Storybook to preview components:

```bash
cd shared/design-system
npm install
npm run dev
# Open http://localhost:6006
```

## Usage Examples

### Button Variants

```tsx
import { Button } from "@/components/ui/button";

<Button variant="default">Default</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
```

### Card with Form

```tsx
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

<Card className="w-[350px]">
  <CardHeader>
    <CardTitle>Login</CardTitle>
  </CardHeader>
  <CardContent className="space-y-4">
    <div className="space-y-2">
      <Label htmlFor="email">Email</Label>
      <Input id="email" type="email" placeholder="name@example.com" />
    </div>
  </CardContent>
  <CardFooter>
    <Button className="w-full">Sign In</Button>
  </CardFooter>
</Card>
```

### Full Page Layout

```tsx
import { Header, HeaderTitle, HeaderActions } from "@/components/layout/header";
import { Sidebar, SidebarNav, SidebarNavItem } from "@/components/layout/sidebar";
import { Container } from "@/components/layout/container";
import { Footer, FooterContent, FooterText } from "@/components/layout/footer";

<div className="flex h-screen flex-col">
  <Header sticky>
    <HeaderTitle>My App</HeaderTitle>
    <HeaderActions>
      <Button variant="ghost">Profile</Button>
    </HeaderActions>
  </Header>
  <div className="flex flex-1">
    <Sidebar>
      <SidebarNav>
        <SidebarNavItem href="/" active>Dashboard</SidebarNavItem>
        <SidebarNavItem href="/settings">Settings</SidebarNavItem>
      </SidebarNav>
    </Sidebar>
    <main className="flex-1 p-6">
      <Container>
        <h1>Content</h1>
      </Container>
    </main>
  </div>
  <Footer>
    <FooterContent>
      <FooterText>&copy; 2024</FooterText>
    </FooterContent>
  </Footer>
</div>
```

## Theme Switching

### In HTML Templates

```html
<!-- Dark theme (default) -->
<html class="dark">

<!-- Light theme -->
<html class="">

<!-- JavaScript toggle -->
<script>
  document.documentElement.classList.toggle('dark');
</script>
```

### In React

```tsx
const [theme, setTheme] = useState<'light' | 'dark'>('dark');

useEffect(() => {
  document.documentElement.classList.toggle('dark', theme === 'dark');
}, [theme]);
```

## Integration with Golden Repos

The design system integrates with these golden repos:
- `typescript-react` - Copy components directly
- `typescript-nextjs` - Copy components + globals.css
- `typescript-vite` - Use HTML templates or adapt for vanilla TS

See `shared/golden-repos/README.md` for integration guides.

---

# AWS Cloudscape

See `cloudscape/README.md` for full Cloudscape documentation.

## Quick Start

```bash
# Install dependencies
npm install @cloudscape-design/components @cloudscape-design/global-styles

# Import in your app
import '@cloudscape-design/global-styles/index.css';
import { AppLayout, Container, Header, Button } from '@cloudscape-design/components';
```

## Example

```tsx
import { AppLayout, Container, Header, Button, SpaceBetween } from '@cloudscape-design/components';

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
