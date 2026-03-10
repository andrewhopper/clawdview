# Lo-Fi Wireframe Protocol

Black & white wireframe mockups for rapid ideation and stakeholder review.

## Purpose

Lo-fi wireframes communicate **layout and structure** without visual distraction. Use for:
- Early-stage concept validation
- Stakeholder alignment on information architecture
- Quick iteration on layouts before committing to design

## Design Constraints

### Color Palette (Grayscale Only)

| Token | Value | Usage |
|-------|-------|-------|
| `--lofi-white` | `#FFFFFF` | Background, content areas |
| `--lofi-gray-100` | `#F5F5F5` | Secondary backgrounds |
| `--lofi-gray-200` | `#E5E5E5` | Borders, dividers |
| `--lofi-gray-300` | `#D4D4D4` | Disabled states |
| `--lofi-gray-400` | `#A3A3A3` | Placeholder text |
| `--lofi-gray-500` | `#737373` | Secondary text |
| `--lofi-gray-700` | `#404040` | Primary text |
| `--lofi-gray-900` | `#171717` | Headings, emphasis |
| `--lofi-black` | `#000000` | Borders, strong accents |

### Visual Effects

**Shadows** - Subtle depth indication:
```css
/* Card shadow */
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

/* Elevated element */
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

/* Modal/overlay */
box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
```

**Gradients** - Subtle backgrounds only:
```css
/* Section differentiation */
background: linear-gradient(180deg, #FFFFFF 0%, #F5F5F5 100%);

/* Button hover state */
background: linear-gradient(180deg, #404040 0%, #171717 100%);
```

### Typography

- **Font**: System sans-serif (no custom fonts)
- **Weights**: 400 (normal), 500 (medium), 700 (bold)
- **Scale**: Standard Tailwind (text-sm, text-base, text-lg, etc.)

### Component Styles

| Element | Style |
|---------|-------|
| **Buttons** | Solid black/white, 1px borders, subtle hover gradient |
| **Cards** | White background, 1px gray border, soft shadow |
| **Inputs** | White background, 1px gray border |
| **Images** | Gray placeholder boxes with diagonal cross |
| **Icons** | Simple black strokes, no fills |
| **Dividers** | 1px gray lines |

## Template Usage

```bash
cp shared/design-system/templates/lofi-wireframe.html \
   prototypes/proto-xxx/docs/mockups/wireframe.html
```

## Component Classes

### Buttons
```html
<button class="lofi-btn">Primary Action</button>
<button class="lofi-btn lofi-btn-outline">Secondary</button>
<button class="lofi-btn lofi-btn-ghost">Ghost</button>
```

### Cards
```html
<div class="lofi-card">
  <div class="lofi-card-header">Title</div>
  <div class="lofi-card-content">Content here</div>
</div>
```

### Image Placeholders
```html
<div class="lofi-img lofi-img-16x9">Image</div>
<div class="lofi-img lofi-img-square">Avatar</div>
<div class="lofi-img lofi-img-hero">Hero Banner</div>
```

### Inputs
```html
<input class="lofi-input" placeholder="Text input">
<textarea class="lofi-textarea" placeholder="Message"></textarea>
```

### Layout
```html
<div class="lofi-container">
  <nav class="lofi-nav">...</nav>
  <main class="lofi-main">...</main>
  <footer class="lofi-footer">...</footer>
</div>
```

## Annotation System

Use these markers for stakeholder communication:

```html
<!-- Annotation box -->
<div class="lofi-annotation">
  <span class="lofi-annotation-number">1</span>
  <span class="lofi-annotation-text">Hero CTA leads to signup</span>
</div>

<!-- Inline note -->
<span class="lofi-note">[Dynamic content from API]</span>
```

## When to Use Lo-Fi vs Hi-Fi

| Stage | Mockup Type | Purpose |
|-------|-------------|---------|
| Phase 3-4 | **Lo-Fi** | Explore layout options |
| Phase 5-6 | **Lo-Fi** | Lock information architecture |
| Phase 7+ | **Hi-Fi** | Final visual design |

## Anti-Patterns

**DO NOT:**
- Add brand colors (defeats purpose)
- Use real images (use placeholders)
- Perfect spacing (sketch-like is intentional)
- Add animations/transitions
- Include detailed iconography

**DO:**
- Use placeholder boxes for images
- Keep text generic ("Button", "Heading")
- Show content hierarchy through size/weight
- Include annotations for stakeholders
- Create multiple layout variations quickly

## Example Workflow

1. **Sketch** - Paper/whiteboard first (optional)
2. **Wireframe** - Create lo-fi HTML mockup
3. **Review** - Stakeholder feedback on structure
4. **Iterate** - Quick revisions to layout
5. **Approve** - Lock information architecture
6. **Design** - Move to hi-fi with approved layout

## Integration

Lo-fi wireframes live alongside other mockups:

```
prototypes/proto-xxx/
└── docs/
    └── mockups/
        ├── wireframes/           # Lo-fi wireframes
        │   ├── home-v1.html
        │   ├── home-v2.html
        │   └── dashboard.html
        └── designs/              # Hi-fi mockups
            └── home-final.html
```
