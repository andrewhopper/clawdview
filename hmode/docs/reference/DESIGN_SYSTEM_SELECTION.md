# Design System Selection
<!-- File UUID: 4e8a9f3d-6c7b-4a2e-9f1d-7c9a8b5f4d3e -->

## Overview

When starting a new project with a UI component, prompt the user to select a design system.

**Available Design Systems:**
1. **Cloudscape** - AWS design system for web applications
2. **ShadCN/UI** - Modern component library built on Radix UI + Tailwind

---

## 1.0 WHEN TO ASK

### Trigger Conditions

**Ask during Phase 1 (SEED) when:**
- Project type includes UI (web app, mobile app, landing page)
- User mentions "frontend", "UI", "interface", or "website"
- Tech stack includes React, Next.js, Vite, or other UI frameworks

**Do NOT ask when:**
- Backend-only projects (API, CLI, worker, lambda)
- Infrastructure projects (CDK, Terraform)
- Data processing projects
- Projects with no user interface

---

## 2.0 SELECTION PROMPT

### Prompt Format

```
Select design system for this project:

[1] Cloudscape (Recommended for AWS-focused apps)
    • AWS design language
    • Enterprise UI patterns
    • Built-in accessibility
    • Best for: Admin panels, dashboards, AWS tools

[2] ShadCN/UI (Recommended for modern web apps)
    • Modern, minimal aesthetic
    • Highly customizable
    • Built on Radix UI + Tailwind
    • Best for: Marketing sites, SaaS apps, consumer apps

[3] None - Build custom components

Which design system? [1/2/3]
```

### Smart Recommendations

**Recommend Cloudscape ([1]) when:**
- Project involves AWS services heavily
- Building admin panel or internal tool
- User mentions "dashboard", "console", or "management UI"
- Target audience is technical/enterprise

**Recommend ShadCN/UI ([2]) when:**
- Consumer-facing application
- Marketing website or landing page
- Modern aesthetic mentioned
- User mentions "sleek", "modern", or "minimalist"

**Recommend None ([3]) when:**
- Highly custom design requirements
- Design system already exists in project
- User explicitly wants custom components

---

## 3.0 RECORDING SELECTION

### File Location

Record selection in `.project` file:

```yaml
design_system:
  type: cloudscape | shadcn | custom
  version: "1.0.0"  # For cloudscape/shadcn
  configured_at: "2026-02-02T10:30:00Z"
```

### Tech Preferences Integration

Also record in `hmode/guardrails/tech-preferences/frontend.json`:

```json
{
  "framework": "nextjs",
  "design_system": "cloudscape",
  "styling": "css-modules",
  "reasoning": "Selected Cloudscape for AWS-focused admin panel"
}
```

---

## 4.0 IMPLEMENTATION IMPACT

### 4.1 Cloudscape Selection

**Immediate actions:**
1. Add to package.json:
   ```json
   {
     "dependencies": {
       "@cloudscape-design/components": "^3.0.0",
       "@cloudscape-design/global-styles": "^1.0.0"
     }
   }
   ```

2. Configure layout:
   ```tsx
   // src/app/layout.tsx
   import '@cloudscape-design/global-styles/index.css';
   ```

3. Update design system docs:
   ```
   Design System: AWS Cloudscape v3
   Component Library: @cloudscape-design/components
   Documentation: https://cloudscape.design/
   ```

**Golden repo:**
- Use `hmode/shared/golden-repos/typescript-nextjs-cloudscape` (if exists)
- Or adapt from `typescript-nextjs` with Cloudscape setup

### 4.2 ShadCN/UI Selection

**Immediate actions:**
1. Run shadcn-ui init:
   ```bash
   npx shadcn-ui@latest init
   ```

2. Configure components.json:
   ```json
   {
     "style": "default",
     "tailwind": {
       "config": "tailwind.config.js",
       "css": "app/globals.css"
     },
     "aliases": {
       "components": "@/components",
       "utils": "@/lib/utils"
     }
   }
   ```

3. Install base components:
   ```bash
   npx shadcn-ui@latest add button card input
   ```

4. Update design system docs:
   ```
   Design System: ShadCN/UI
   Component Library: shadcn-ui (Radix UI + Tailwind)
   Documentation: https://ui.shadcn.com/
   ```

**Golden repo:**
- Use `hmode/shared/golden-repos/typescript-nextjs` (already has shadcn setup)
- Or `typescript-vite` for Vite projects

### 4.3 Custom Selection

**Immediate actions:**
1. Create design tokens file:
   ```css
   /* src/styles/tokens.css */
   :root {
     --color-primary: #3b82f6;
     --color-background: #ffffff;
     --spacing-unit: 8px;
   }
   ```

2. Document design system:
   ```
   Design System: Custom
   Component Library: None (custom components)
   Design Tokens: src/styles/tokens.css
   ```

---

## 5.0 PHASE INTEGRATION

### 5.1 Phase 1 (SEED)

**After persona inference, before advancing to Phase 2:**

```
Project: E-commerce checkout redesign
Persona: Online shoppers (ages 25-45)
Type: Production web app

[Design System Selection]

This project requires a UI. Select design system:

[1] Cloudscape (AWS design system)
[2] ShadCN/UI (Modern, customizable) - Recommended
[3] None (Custom components)

Selection? [1/2/3]
```

**Record in .project:**
```yaml
project:
  name: ecommerce-checkout
  phase: 1
  design_system:
    type: shadcn
    version: latest
    configured_at: "2026-02-02T10:30:00Z"
```

### 5.2 Phase 5 (Selection)

**If design system not selected in Phase 1, ask again:**

```
Tech Stack Selected:
- Framework: Next.js 14
- Language: TypeScript
- Styling: Tailwind CSS

Design system selection required.

[1] Cloudscape
[2] ShadCN/UI - Recommended for consumer apps
[3] Custom

Selection? [1/2/3]
```

### 5.3 Phase 6 (Design)

**Use selected design system for mockups:**

**If Cloudscape:**
- Use Cloudscape components in mockups
- Follow AWS design guidelines
- Use Cloudscape color palette

**If ShadCN/UI:**
- Use shadcn components in mockups
- Follow Radix UI patterns
- Use Tailwind design tokens

**If Custom:**
- Create components from scratch
- Define custom design tokens
- Document component API

---

## 6.0 CHANGING DESIGN SYSTEM

### Mid-Project Changes

**When allowed:**
- Before Phase 6 (Design) starts
- Phase 1-5 (no visual assets created yet)

**When NOT allowed:**
- After Phase 6 (mockups created with current system)
- After Phase 8 (components already implemented)

**Change process:**
1. User requests: "Switch to [system]"
2. Check current phase
3. If < Phase 6:
   - Update `.project` file
   - Update tech preferences
   - Proceed with new system
4. If >= Phase 6:
   - Warn about rework required
   - List impacted files
   - Require explicit confirmation

---

## 7.0 COMPARISON TABLE

| Feature | Cloudscape | ShadCN/UI | Custom |
|---------|-----------|-----------|--------|
| **Setup Time** | Fast (npm install) | Medium (init + add components) | Slow (build from scratch) |
| **Customization** | Limited | High | Complete |
| **AWS Integration** | Excellent | Manual | Manual |
| **Accessibility** | Built-in | Built-in (Radix) | Manual |
| **Component Count** | 50+ | 40+ | As needed |
| **Styling** | CSS-in-JS | Tailwind | Your choice |
| **Bundle Size** | Large | Small | Smallest |
| **Best For** | AWS tools, dashboards | Modern web apps | Unique designs |
| **Learning Curve** | Steep | Medium | N/A |

---

## 8.0 DETECTION LOGIC

### Automatic Detection

**Detect design system from existing project:**

```python
def detect_design_system(project_root: Path) -> str:
    """Detect which design system is used in project."""

    package_json = project_root / 'package.json'
    if package_json.exists():
        with open(package_json) as f:
            pkg = json.load(f)
            deps = pkg.get('dependencies', {})

            if '@cloudscape-design/components' in deps:
                return 'cloudscape'
            elif 'shadcn-ui' in deps or (project_root / 'components.json').exists():
                return 'shadcn'

    # Check for custom design tokens
    if (project_root / 'src/styles/tokens.css').exists():
        return 'custom'

    return 'none'
```

### Prompt User If Not Detected

```python
if detect_design_system(project_root) == 'none':
    print("No design system detected. Would you like to configure one?")
    print("[1] Cloudscape")
    print("[2] ShadCN/UI")
    print("[3] Keep as-is (custom)")
```

---

## 9.0 ENFORCEMENT

### Pre-Mockup Check

**Before generating ANY UI mockup or component:**

```python
def check_design_system_configured() -> str:
    """Ensure design system is selected before creating UI assets."""

    with open('.project') as f:
        project = yaml.safe_load(f)

    if 'design_system' not in project:
        raise DesignSystemNotConfigured(
            "Design system not selected. Run design system selection prompt."
        )

    return project['design_system']['type']
```

**Use in workflows:**
```python
# Before Phase 6 (Design)
design_system = check_design_system_configured()

if design_system == 'cloudscape':
    # Use Cloudscape components in mockups
    pass
elif design_system == 'shadcn':
    # Use ShadCN components in mockups
    pass
```

---

## 10.0 SUMMARY

**When:** Phase 1 (SEED) or Phase 5 (Selection) for UI projects

**Options:**
1. Cloudscape - AWS design system
2. ShadCN/UI - Modern component library
3. Custom - Build your own

**Recording:**
- `.project` file (design_system field)
- `hmode/guardrails/tech-preferences/frontend.json`

**Impact:**
- Phase 5: Dependencies and configuration
- Phase 6: Mockup component selection
- Phase 8: Implementation patterns

**Enforcement:**
- Check before creating mockups
- Check before implementing components
- Prevent changes after Phase 6 without confirmation
