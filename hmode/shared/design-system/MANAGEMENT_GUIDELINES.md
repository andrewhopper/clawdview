# Design System Management Guidelines

Instructions for managing, extending, and maintaining design systems based on best practices from Airbnb DLS, Spotify Encore, and AWS Cloudscape.

---

## 1.0 ARCHITECTURE MODELS

### 1.1 Component Philosophy

**Airbnb Approach: Living Organism**
Components are elements of a living organism, not atomic particles:
- Each component has a function and personality
- Defined by a set of properties
- Can co-exist with others and evolve independently
- Can be deprecated ("die") without breaking the system

**Spotify Approach: System of Systems**
A federated family of design systems:
- Foundation layer (shared by all)
- Platform-specific systems (Web, iOS, Android)
- Local systems (product-specific extensions)

**Cloudscape Approach: Atomic Design**
Build complex from simple:
- Primitives → Components → Patterns → Pages
- Everything theme-able via design tokens

### 1.2 Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 4: PATTERNS                        │
│  Loading states, error handling, navigation, forms          │
├─────────────────────────────────────────────────────────────┤
│                    LAYER 3: COMPONENTS                      │
│  Buttons, cards, inputs, modals, tables                     │
├─────────────────────────────────────────────────────────────┤
│                    LAYER 2: PRIMITIVES/ELEMENTS             │
│  Labels, icons, dividers (cannot be broken down further)    │
├─────────────────────────────────────────────────────────────┤
│                    LAYER 1: FOUNDATION                      │
│  Colors, typography, spacing, motion, design tokens         │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Multi-System Strategy

When managing multiple design systems (like shadcn + Cloudscape):

```yaml
decision_tree:
  aws_console_like: cloudscape
  data_heavy_dashboard: cloudscape
  enterprise_internal: cloudscape
  marketing_site: shadcn
  consumer_app: shadcn
  custom_branding: shadcn
  rapid_prototype: shadcn
```

---

## 2.0 DESIGN TOKENS

### 2.1 Token Categories

| Category | Purpose | Example |
|----------|---------|---------|
| **Constant** | Raw values | `#1a1a2e`, `16px`, `400ms` |
| **Semantic** | Purpose-based | `color-background-primary`, `spacing-md` |
| **Contextual** | Component-specific | `button-background-hover`, `card-border-radius` |

### 2.2 Token Hierarchy

```
Foundation Tokens (constant)
    └── Semantic Tokens (purpose)
            └── Component Tokens (contextual)
                    └── State Tokens (interaction)
```

### 2.3 Token Naming Convention

```
{category}-{property}-{variant}-{state}

Examples:
  color-background-primary
  color-background-primary-hover
  spacing-component-padding-lg
  border-radius-button-sm
```

### 2.4 Token Management Rules

1. **Single source of truth**: Tokens defined in one place (JSON/YAML)
2. **Platform distribution**: Use Style Dictionary or similar for cross-platform export
3. **No magic numbers**: Every value traces back to a token
4. **Semantic first**: Prefer `--color-error` over `--color-red-500`

### 2.5 Token File Structure

```
tokens/
├── foundation/
│   ├── colors.json
│   ├── typography.json
│   ├── spacing.json
│   ├── motion.json
│   └── breakpoints.json
├── semantic/
│   ├── colors.json      # purpose-based color mapping
│   ├── typography.json  # text roles (heading, body, caption)
│   └── spacing.json     # layout spacing (page, section, component)
├── components/
│   ├── button.json
│   ├── card.json
│   └── input.json
└── themes/
    ├── light.json
    └── dark.json
```

---

## 3.0 COMPONENT GUIDELINES

### 3.1 Component Requirements

Every component MUST have:

| Requirement | Description |
|-------------|-------------|
| **Props interface** | TypeScript types for all props |
| **Default values** | Sensible defaults for optional props |
| **Variants** | Enum of visual/behavioral variations |
| **States** | Default, hover, active, focus, disabled, loading |
| **Accessibility** | ARIA labels, keyboard nav, screen reader support |
| **Responsive** | Works at all breakpoints |
| **Themeable** | Uses design tokens, not hardcoded values |
| **Documentation** | Usage examples, do/don't guidelines |
| **Tests** | Unit tests, visual regression tests |

### 3.2 Component API Design Principles

1. **Consistent prop names** across all components
   ```tsx
   // GOOD: consistent naming
   <Button variant="primary" size="lg" disabled />
   <Input variant="outlined" size="lg" disabled />

   // BAD: inconsistent naming
   <Button type="primary" btnSize="large" isDisabled />
   <Input style="outlined" inputSize="lg" disabled />
   ```

2. **Composition over configuration**
   ```tsx
   // GOOD: composable
   <Card>
     <CardHeader><CardTitle>Title</CardTitle></CardHeader>
     <CardContent>Content</CardContent>
   </Card>

   // BAD: prop explosion
   <Card title="Title" content="Content" hasHeader headerVariant="large" />
   ```

3. **Escape hatches** for edge cases
   ```tsx
   <Button className="custom-override" style={{ width: 'fit-content' }} />
   ```

### 3.3 Component State Matrix

Document all state combinations:

```
┌──────────────┬─────────┬─────────┬─────────┬──────────┬─────────┐
│ State        │ Default │ Hover   │ Focus   │ Active   │ Disabled│
├──────────────┼─────────┼─────────┼─────────┼──────────┼─────────┤
│ Primary      │ ✓       │ ✓       │ ✓       │ ✓        │ ✓       │
│ Secondary    │ ✓       │ ✓       │ ✓       │ ✓        │ ✓       │
│ Destructive  │ ✓       │ ✓       │ ✓       │ ✓        │ ✓       │
│ Ghost        │ ✓       │ ✓       │ ✓       │ ✓        │ ✓       │
└──────────────┴─────────┴─────────┴─────────┴──────────┴─────────┘
```

### 3.4 Platform Considerations

**Cross-Platform (Airbnb approach):**
- Design solutions that feel at home across platforms
- Platform-agnostic components where possible
- Follow conventions for: navigation, system icons, contextual actions

**Platform-Specific:**
- Use native patterns for critical interactions
- Respect platform guidelines (iOS HIG, Material Design)

---

## 4.0 GOVERNANCE MODEL

### 4.1 Governance Options

| Model | Best For | Description |
|-------|----------|-------------|
| **Centralized** | Small orgs, early stage | Core team owns everything |
| **Federated** | Medium orgs | Product teams contribute, core team reviews |
| **Community** | Large orgs, mature systems | Open contribution, collective decision-making |
| **Mixed** | Complex organizations | Combines elements based on component criticality |

### 4.2 Recommended Structure (Federated)

```
┌─────────────────────────────────────────────────────────────┐
│                    DESIGN SYSTEM COUNCIL                    │
│  - Sets standards and principles                            │
│  - Approves breaking changes                                │
│  - Resolves cross-team conflicts                            │
├─────────────────────────────────────────────────────────────┤
│                    CORE TEAM                                │
│  - Maintains foundation and shared components               │
│  - Reviews all contributions                                │
│  - Publishes releases                                       │
├─────────────────────────────────────────────────────────────┤
│  PRODUCT TEAMS    │  PRODUCT TEAMS    │  PRODUCT TEAMS     │
│  - Build features │  - Build features │  - Build features  │
│  - Propose comps  │  - Propose comps  │  - Propose comps   │
│  - Own local sys  │  - Own local sys  │  - Own local sys   │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Decision Framework

| Change Type | Who Decides | Process |
|-------------|-------------|---------|
| Foundation tokens | Council | RFC + vote |
| New shared component | Core team | RFC + review |
| Component bug fix | Core team | PR review |
| Local system addition | Product team | Core team notification |
| Breaking change | Council | RFC + migration plan |

### 4.4 Communication Cadence

| Meeting | Frequency | Purpose |
|---------|-----------|---------|
| Core team standup | Weekly | Progress, blockers |
| Design system review | Bi-weekly | Contribution reviews |
| Council meeting | Monthly | Strategic decisions |
| Open house | Monthly | Q&A, feedback collection |

---

## 5.0 CONTRIBUTION PROCESS

### 5.1 Contribution Types

| Type | Definition | Review Level |
|------|------------|--------------|
| **Bug fix** | Fixes broken behavior | Light (1 reviewer) |
| **Enhancement** | Improves existing component | Standard (2 reviewers) |
| **New variant** | Adds variant to existing component | Standard |
| **New component** | Entirely new component | Full (design + code review) |
| **Foundation change** | Token/primitive changes | Council review |

### 5.2 Contribution Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. PROPOSE │────▶│  2. REVIEW  │────▶│  3. BUILD   │
│  - Open RFC │     │  - Design   │     │  - Code     │
│  - Use case │     │  - Feasibil │     │  - Tests    │
│  - Mockups  │     │  - Priority │     │  - Docs     │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
┌─────────────┐     ┌─────────────┐            │
│  5. RELEASE │◀────│  4. APPROVE │◀───────────┘
│  - Merge    │     │  - QA       │
│  - Version  │     │  - A11y     │
│  - Announce │     │  - Final    │
└─────────────┘     └─────────────┘
```

### 5.3 RFC Template

```markdown
# RFC: [Component/Change Name]

## Summary
One paragraph explaining the proposal.

## Motivation
Why is this needed? What use cases does it address?

## Detailed Design
- Props/API
- Visual specs
- Interaction specs
- Accessibility requirements

## Alternatives Considered
What other approaches were considered?

## Adoption Strategy
How will teams migrate/adopt?

## Open Questions
What decisions need input?
```

### 5.4 Acceptance Criteria (Spotify Requirements)

Before merging, components MUST satisfy:

1. **Accessibility**: WCAG 2.1 AA compliance
2. **Tokens**: All colors, spacing use design tokens
3. **TypeScript**: Full type coverage for props
4. **Tests**: Unit tests, visual regression tests
5. **Documentation**: Usage examples, prop docs
6. **Support plan**: Stay within 1 major version of latest

---

## 6.0 VERSIONING

### 6.1 Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (prop removal, behavior change)
MINOR: New features, backwards compatible
PATCH: Bug fixes, backwards compatible
```

### 6.2 What Constitutes a Breaking Change

| Breaking | Non-Breaking |
|----------|--------------|
| Removing a prop | Adding optional prop |
| Changing prop type | Adding new variant |
| Changing default behavior | Bug fix |
| Removing component | Deprecation warning |
| Changing token name | Adding new token |

### 6.3 Deprecation Process

```
v1.0.0: Component works normally
v1.1.0: Deprecation warning added (console.warn)
v1.2.0: Warning links to migration guide
v2.0.0: Component removed
```

### 6.4 Changelog Format

```markdown
## [2.0.0] - 2025-01-15

### Breaking Changes
- Removed `Button` `type` prop (use `variant` instead)
- Changed `Card` default padding from `md` to `lg`

### Added
- New `Tooltip` component
- `Button` now supports `loading` state

### Fixed
- Fixed focus ring not showing in Safari
- Fixed `Input` placeholder color in dark mode

### Deprecated
- `Badge` `color` prop (use `variant` in next major)
```

### 6.5 Release Automation

Recommended tools:
- **Conventional Commits**: Standardized commit messages
- **semantic-release**: Automated versioning from commits
- **Changesets**: Multi-package version management

---

## 7.0 DOCUMENTATION

### 7.1 Documentation Requirements

| Doc Type | Required For | Format |
|----------|--------------|--------|
| **API Reference** | All components | Auto-generated from types |
| **Usage Examples** | All components | Code snippets + preview |
| **Do/Don't** | Complex components | Visual examples |
| **Accessibility** | All components | ARIA patterns, keyboard nav |
| **Migration Guide** | Breaking changes | Step-by-step instructions |

### 7.2 Component Documentation Template

```markdown
# ComponentName

Brief description of what the component does.

## Usage

\`\`\`tsx
import { ComponentName } from '@design-system/components';

<ComponentName variant="primary">Label</ComponentName>
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' | 'primary' | Visual variant |

## Variants

[Visual showcase of all variants]

## States

[Visual showcase of all states]

## Accessibility

- Uses `role="button"`
- Supports keyboard activation (Enter, Space)
- Announces loading state to screen readers

## Do's and Don'ts

✅ Do: Use primary for main actions
❌ Don't: Use multiple primary buttons in one view
```

### 7.3 Living Documentation

- **Storybook**: Interactive component playground
- **Auto-sync**: Documentation generated from code (JSDoc/TSDoc)
- **Screenshots**: Rendered from production code (Airbnb approach)
- **Links to source**: Each component links to Git repository

---

## 8.0 TOOLING

### 8.1 Required Tools

| Category | Tool | Purpose |
|----------|------|---------|
| **Component dev** | Storybook | Development, documentation |
| **Token management** | Style Dictionary | Cross-platform token export |
| **Visual testing** | Chromatic/Percy | Visual regression testing |
| **Accessibility** | axe-core | Automated a11y testing |
| **Linting** | ESLint + stylelint | Code consistency |
| **Type checking** | TypeScript | Type safety |
| **Bundling** | tsup/Rollup | Package building |

### 8.2 Automation (Spotify Model)

- **Figma sync**: Figgy bot syncs code changes to Figma
- **Token generation**: Color themes auto-generated with accessible contrast
- **Release automation**: Conventional commits → semantic versioning
- **PR checks**: a11y, visual regression, type checks on every PR

### 8.3 Quality Gates

Every PR must pass:

```yaml
checks:
  - lint: "npm run lint"
  - types: "npm run type-check"
  - unit_tests: "npm run test"
  - visual_tests: "npm run test:visual"
  - a11y: "npm run test:a11y"
  - build: "npm run build"
```

---

## 9.0 MAINTENANCE

### 9.1 Maintenance Checklist (Weekly)

- [ ] Review open issues/PRs
- [ ] Check for security vulnerabilities in dependencies
- [ ] Monitor adoption metrics
- [ ] Address deprecation warnings from dependencies

### 9.2 Maintenance Checklist (Monthly)

- [ ] Update dependencies (minor/patch)
- [ ] Review component usage analytics
- [ ] Audit for unused components
- [ ] Review contribution backlog
- [ ] Update documentation for recent changes

### 9.3 Maintenance Checklist (Quarterly)

- [ ] Major dependency updates
- [ ] Accessibility audit
- [ ] Performance audit
- [ ] Token consistency audit
- [ ] Review governance process effectiveness
- [ ] Plan deprecations for next major version

### 9.4 Audit Process (Airbnb Tip)

> "Strive for the smallest amount of robust components possible that can be applied to a large amount of use cases."

Regularly audit for:
- Duplicate components (merge or deprecate)
- Underused components (consider deprecation)
- Components that grew too complex (decompose)
- Missing components (from product team feedback)

### 9.5 Master File Management (Airbnb Tip)

- Keep master files in version-controlled location
- Prevent unauthorized alterations
- Enable quick rollback when issues arise
- Archive previous versions for reference

---

## 10.0 ADOPTION & EVANGELISM

### 10.1 Adoption Metrics

| Metric | How to Measure |
|--------|----------------|
| **Coverage** | % of products using design system |
| **Compliance** | % of components from design system vs custom |
| **Satisfaction** | Developer survey scores |
| **Velocity** | Time to build new features |
| **Bug rate** | Bugs in design system vs custom components |

### 10.2 Evangelism Strategies

1. **Champions program**: Representatives from each product team
2. **Office hours**: Regular Q&A sessions
3. **Showcase wins**: Highlight successful implementations
4. **Easy onboarding**: Getting started in < 30 minutes
5. **Migration support**: Help teams adopt incrementally

### 10.3 Common Language (Airbnb Tip)

> "Develop a common language so everyone refers to components in the same way."

- Maintain glossary of terms
- Consistent naming across design and code
- Use same names in Figma, Storybook, code

---

## 11.0 IMPLEMENTATION CHECKLIST

When implementing these guidelines, follow this order:

### Phase 1: Foundation
- [ ] Define design token structure
- [ ] Create color, typography, spacing tokens
- [ ] Set up token distribution pipeline
- [ ] Establish naming conventions

### Phase 2: Core Components
- [ ] Identify MVP component set (button, input, card, etc.)
- [ ] Build components with full state coverage
- [ ] Write comprehensive tests
- [ ] Create Storybook documentation

### Phase 3: Governance
- [ ] Define governance model
- [ ] Create contribution process
- [ ] Set up quality gates in CI
- [ ] Document RFC process

### Phase 4: Documentation
- [ ] Create documentation site
- [ ] Write getting started guide
- [ ] Document all components
- [ ] Create migration guides

### Phase 5: Adoption
- [ ] Onboard pilot team
- [ ] Gather feedback
- [ ] Iterate on pain points
- [ ] Roll out to additional teams

---

## 12.0 ATOMIC DESIGN METHODOLOGY

### 12.1 Overview

Atomic Design is a methodology by Brad Frost for creating design systems by breaking interfaces into five hierarchical stages. It's a mental model for thinking of UIs as both a cohesive whole and a collection of parts.

### 12.2 The Five Stages

```
┌─────────────────────────────────────────────────────────────┐
│  PAGES          Specific instances with real content        │
│  "What users see and interact with"                         │
├─────────────────────────────────────────────────────────────┤
│  TEMPLATES      Page-level layouts with content structure   │
│  "Skeleton that holds components"                           │
├─────────────────────────────────────────────────────────────┤
│  ORGANISMS      Complex UI sections (header, footer, forms) │
│  "Distinct interface sections"                              │
├─────────────────────────────────────────────────────────────┤
│  MOLECULES      Simple groups of atoms (search form, card)  │
│  "Do one thing and do it well"                              │
├─────────────────────────────────────────────────────────────┤
│  ATOMS          Basic HTML elements (button, input, label)  │
│  "Cannot be broken down further"                            │
└─────────────────────────────────────────────────────────────┘
```

### 12.3 Stage Definitions

| Stage | Definition | Examples |
|-------|------------|----------|
| **Atoms** | Basic HTML elements that can't be broken down further | `<button>`, `<input>`, `<label>`, icons |
| **Molecules** | Simple groups of atoms functioning as a unit | Search form, card, navigation item |
| **Organisms** | Complex components composed of molecules/atoms | Header, footer, sidebar, product grid |
| **Templates** | Page layouts showing content structure | Dashboard layout, article layout |
| **Pages** | Specific instances with real representative content | Homepage, user profile, checkout |

### 12.4 Implementation Rules

1. **Atoms are indivisible**: If it can be broken down further, it's not an atom
2. **Molecules do one thing**: Follow single responsibility principle
3. **Organisms are sections**: They form distinct, reusable interface areas
4. **Templates are content-agnostic**: Focus on structure, not content
5. **Pages test the system**: Use real content to validate design decisions

### 12.5 Mapping to Repository

```yaml
atomic_mapping:
  atoms:
    - shared/design-system/design-system/src/components/ui/button.tsx
    - shared/design-system/design-system/src/components/ui/input.tsx
    - shared/design-system/design-system/src/components/ui/label.tsx
    - shared/design-system/design-system/src/components/ui/badge.tsx
  molecules:
    - shared/design-system/design-system/src/components/ui/card.tsx
    - shared/design-system/design-system/src/components/ui/alert.tsx
  organisms:
    - shared/design-system/design-system/src/components/layout/header.tsx
    - shared/design-system/design-system/src/components/layout/sidebar.tsx
    - shared/design-system/design-system/src/components/layout/footer.tsx
  templates:
    - shared/design-system/templates/*.html
  pages:
    - Project-specific implementations
```

---

## 13.0 VISUAL & INFORMATION HIERARCHY

### 13.1 Core Principle

Visual hierarchy guides users to process information in the intended order of importance. The eye should naturally flow from most important to least important.

### 13.2 Hierarchy Tools

| Tool | How It Works | Usage |
|------|--------------|-------|
| **Size** | Larger = more important | Headlines > body text |
| **Weight** | Bolder = more emphasis | Key labels, CTAs |
| **Color** | Contrast draws attention | Primary actions, errors |
| **Position** | Top-left = first seen (LTR) | Primary navigation, logos |
| **Whitespace** | Space isolates importance | Section separation |
| **Proximity** | Close items are related | Form groups, card content |

### 13.3 Typography Hierarchy

```
Level 1: Page Title       (32-48px, bold, primary color)
Level 2: Section Header   (24-32px, bold or semibold)
Level 3: Subsection       (18-24px, semibold)
Level 4: Body Text        (14-16px, regular)
Level 5: Caption/Meta     (12-14px, muted color)
Level 6: Labels           (10-12px, uppercase, letter-spacing)
```

### 13.4 Spacing Hierarchy

```
Page padding:      24-64px   (largest)
Section spacing:   32-48px
Component spacing: 16-24px
Element spacing:   8-16px
Inline spacing:    4-8px     (smallest)
```

### 13.5 Hierarchy Rules

1. **3-Level Maximum**: More than 3 levels confuses users
2. **Consistent Contrast**: Same importance = same treatment
3. **Proximity Principle**: Related items grouped, unrelated separated
4. **Reading Flow**: Support natural left-to-right, top-to-bottom (LTR)
5. **Single Focal Point**: One primary CTA per view

### 13.6 Hierarchy Checklist

Before finalizing any layout:

- [ ] Can users identify the most important element in < 3 seconds?
- [ ] Is there a clear reading order?
- [ ] Are related items visually grouped?
- [ ] Is there adequate whitespace between sections?
- [ ] Is typography scaled consistently?
- [ ] Is the primary action obvious?

---

## 14.0 INFORMATION ARCHITECTURE

### 14.1 Definition

Information Architecture (IA) is how content is organized, structured, and labeled to support findability and usability. IA informs the UI but is not the UI itself.

### 14.2 Core Components

| Component | Purpose | Examples |
|-----------|---------|----------|
| **Organization** | How content is structured | Categories, hierarchies, taxonomies |
| **Labeling** | How content is named | Menu items, button text, headings |
| **Navigation** | How users move through content | Menus, breadcrumbs, links |
| **Search** | How users find specific content | Search bars, filters, facets |

### 14.3 IA vs Navigation vs User Flow

```
┌─────────────────────────────────────────────────────────────┐
│ INFORMATION ARCHITECTURE                                    │
│ "The blueprint - how content is organized"                  │
│ → Sitemaps, content hierarchies, taxonomies                 │
├─────────────────────────────────────────────────────────────┤
│ NAVIGATION DESIGN                                           │
│ "The wayfinding - how users get around"                     │
│ → Menus, breadcrumbs, links, tabs                           │
├─────────────────────────────────────────────────────────────┤
│ USER FLOWS                                                  │
│ "The journey - steps to complete a task"                    │
│ → Checkout flow, onboarding flow, signup flow               │
└─────────────────────────────────────────────────────────────┘
```

### 14.4 Navigation Patterns

| Pattern | Best For | Example |
|---------|----------|---------|
| **Global nav** | Site-wide access | Top header menu |
| **Local nav** | Section-specific | Sidebar within dashboard |
| **Contextual nav** | Related content | "See also" links |
| **Breadcrumbs** | Deep hierarchies | Home > Category > Item |
| **Tabs** | Parallel content | Settings tabs |
| **Wizards** | Sequential tasks | Checkout steps |

### 14.5 IA Principles

1. **Users' mental models first**: Match how users think, not how systems work
2. **Shallow hierarchies**: Max 3 clicks to any content
3. **Clear labeling**: Use user language, not internal jargon
4. **Consistent patterns**: Same type of content = same navigation
5. **Progressive disclosure**: Show only what's needed at each step

### 14.6 IA Validation Methods

| Method | When to Use | What It Tests |
|--------|-------------|---------------|
| **Card sorting** | Early design | Category organization |
| **Tree testing** | Mid design | Navigation findability |
| **First-click testing** | Pre-launch | Initial navigation choices |
| **Analytics review** | Post-launch | Actual navigation patterns |

---

## 15.0 ASSET CONSISTENCY ENFORCEMENT (PROTOFLOW)

### 15.1 Purpose

This section defines how to enforce design system consistency for ALL generated assets in the Protoflow monorepo, including HTML mockups, diagrams, documents, and React components.

### 15.2 Asset Types & Rules

| Asset Type | Design System | Enforcement |
|------------|---------------|-------------|
| React components | shadcn/ui or Cloudscape | 4-layer enforcement (see ENFORCEMENT_GUIDE.md) |
| HTML mockups | shadcn/ui via templates | Template-based |
| Diagrams (HTML/SVG) | Design tokens | Token validation |
| Landing pages | Templates | Template-based |
| PDF/XLSX | Brand colors | Style guide reference |

### 15.3 Mandatory Standards

**ALL generated assets MUST include:**

```yaml
required_metadata:
  - design_system: "shadcn/ui" | "cloudscape" | "tokens-only"
  - project_uuid: string  # From .project file
  - asset_uuid: string    # 8-char unique ID
  - date: ISO-8601        # Creation date
  - version: "v1" | "v2"  # Increment for revisions

required_styling:
  - colors: "Use design tokens, not hex values"
  - typography: "Use scale from design system"
  - spacing: "Use spacing tokens (4, 8, 16, 24, 32, 48, 64)"
  - border_radius: "Use radius tokens"
```

### 15.4 Color Token Requirements

**ALWAYS use CSS variables, never raw hex:**

```css
/* ✅ CORRECT */
background-color: hsl(var(--background));
color: hsl(var(--foreground));
border-color: hsl(var(--border));

/* ❌ WRONG */
background-color: #1a1a2e;
color: #ffffff;
border-color: #333;
```

### 15.5 Typography Token Requirements

**Use consistent type scale:**

```css
/* Heading levels */
--text-h1: 2.25rem;    /* 36px */
--text-h2: 1.875rem;   /* 30px */
--text-h3: 1.5rem;     /* 24px */
--text-h4: 1.25rem;    /* 20px */

/* Body text */
--text-lg: 1.125rem;   /* 18px */
--text-base: 1rem;     /* 16px */
--text-sm: 0.875rem;   /* 14px */
--text-xs: 0.75rem;    /* 12px */
```

### 15.6 Spacing Token Requirements

**Use 4px base unit:**

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

### 15.7 Asset Generation Checklist

Before generating ANY visual asset:

**Foundation Check:**
- [ ] Using design tokens for colors?
- [ ] Using typography scale?
- [ ] Using spacing scale?
- [ ] Using border radius tokens?

**Hierarchy Check:**
- [ ] Clear visual hierarchy (3 levels max)?
- [ ] Single primary focal point?
- [ ] Adequate whitespace?
- [ ] Consistent element sizing?

**Architecture Check:**
- [ ] Logical content grouping?
- [ ] Clear navigation (if applicable)?
- [ ] Consistent labeling?

**Metadata Check:**
- [ ] Asset UUID assigned?
- [ ] Project UUID referenced?
- [ ] Version number included?
- [ ] Date recorded?

### 15.8 Template Usage

**HTML Mockups:**
```bash
# Always start from template
cp shared/design-system/templates/mockup.html my-mockup.html
```

**Landing Pages:**
```bash
# Choose appropriate template
cp shared/design-system/templates/landing-dark.html landing.html
# OR
cp shared/design-system/templates/landing-light.html landing.html
```

**Architecture Diagrams:**
- Use `/arch-diagram` command
- Diagrams inherit design tokens automatically

### 15.9 Validation Commands

```bash
# Validate HTML assets
python3 .guardrails/ai-steering/design_system_validator.py validate path/to/file.html

# Check React components
npm run lint

# Visual regression (if configured)
npm run test:visual
```

### 15.10 Common Violations & Fixes

| Violation | Fix |
|-----------|-----|
| Raw hex colors | Replace with `hsl(var(--token))` |
| Inline styles in React | Use Tailwind classes |
| Inconsistent spacing | Use spacing tokens |
| Missing hierarchy | Add clear H1 > H2 > body |
| No metadata comment | Add asset header block |
| Magic numbers | Replace with tokens |

---

## 16.0 AI GENERATION RULES

### 16.1 Preamble

When AI generates ANY design asset, it MUST follow these rules automatically.

### 16.2 Before Generation

1. Check if template exists in `shared/design-system/templates/`
2. Load design tokens from `shared/design-system/design-system/src/globals.css`
3. Determine appropriate design system (shadcn vs Cloudscape)
4. Generate asset UUID

### 16.3 During Generation

1. Use ONLY design tokens for colors, spacing, typography
2. Apply visual hierarchy principles (size, weight, color, space)
3. Structure content with clear information architecture
4. Follow atomic design principles for component composition

### 16.4 After Generation

1. Add metadata comment block
2. Validate against design system rules
3. Check visual hierarchy (3 levels max)
4. Verify token usage (no raw values)

### 16.5 Asset Header Template

```html
<!--
  Asset: {descriptive-name}
  Project: {project-uuid}
  Asset ID: {asset-uuid}.v{N}
  Date: {YYYY-MM-DD}
  Design System: shared/design-system

  Atomic Level: {atom|molecule|organism|template|page}

  Tokens Used:
  - Colors: --background, --foreground, --primary, --muted
  - Spacing: space-4, space-6, space-8
  - Typography: text-base, text-lg, text-h2
-->
```

---

## Sources

This document synthesizes practices from:

**Design Systems:**
- [Airbnb Design Language System](https://karrisaarinen.com/dls/)
- [Building a Visual Language - Airbnb](https://medium.com/airbnb-design/building-a-visual-language-behind-the-scenes-of-our-airbnb-design-system-224748775e4e)
- [5 Tips from an Airbnb Designer](https://www.designsystems.com/5-tips-from-an-airbnb-designer-on-maintaining-a-design-system/)
- [Spotify Encore - Three Years On](https://spotify.design/article/can-i-get-an-encore-spotifys-design-system-three-years-on)
- [Reimagining Design Systems at Spotify](https://spotify.design/article/reimagining-design-systems-at-spotify)
- [Cloudscape Design System](https://cloudscape.design/)
- [Cloudscape Foundation](https://cloudscape.design/foundation/)

**Governance & Contribution:**
- [Design System Governance - zeroheight](https://zeroheight.com/help/guides/design-system-governance-models-and-which-is-right-for-your-organization/)
- [Design System Governance Process - Brad Frost](https://bradfrost.com/blog/post/a-design-system-governance-process/)
- [Design System Contribution Model - UXPin](https://www.uxpin.com/studio/blog/design-system-contribution-model/)

**Tokens & Versioning:**
- [Design Token Architecture - Martin Fowler](https://martinfowler.com/articles/design-token-based-ui-architecture.html)
- [Versioning Design Systems - Nathan Curtis](https://medium.com/eightshapes-llc/versioning-design-systems-48cceb5ace4d)
- [Versioning Design Tokens - Francesco Improta](https://designtokens.substack.com/p/versioning-design-tokens)

**Atomic Design:**
- [Atomic Design Methodology - Brad Frost](https://atomicdesign.bradfrost.com/chapter-2/)
- [Atomic Web Design - Brad Frost](https://bradfrost.com/blog/post/atomic-web-design/)
- [Build Systems Not Pages - Design Systems](https://www.designsystems.com/brad-frosts-atomic-design-build-systems-not-pages/)

**Visual & Information Hierarchy:**
- [Visual Hierarchy - Interaction Design Foundation](https://www.interaction-design.org/literature/topics/visual-hierarchy)
- [Visual Hierarchy in UX - Nielsen Norman Group](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)
- [Typographic Hierarchy - Smashing Magazine](https://www.smashingmagazine.com/2022/10/typographic-hierarchies/)
- [Typography Hierarchy Guide - Toptal](https://www.toptal.com/designers/typography/typographic-hierarchy)

**Information Architecture:**
- [Guide to Information Architecture - Toptal](https://www.toptal.com/designers/ia/guide-to-information-architecture)
- [What is Information Architecture - Figma](https://www.figma.com/resource-library/what-is-information-architecture/)
- [IA vs Navigation - Nielsen Norman Group](https://www.nngroup.com/articles/ia-vs-navigation/)
- [Information Architecture - Interaction Design Foundation](https://www.interaction-design.org/literature/topics/information-architecture)

---

**Version:** 2.0.0
**Last Updated:** 2025-12-05
