# HTML Templates

Standalone HTML templates using the shadcn/ui design system. No build step required — copy, customize, and use.

## Quick Start

```bash
# Copy template to your project
cp shared/design-system/templates/pitch.html my-project/docs/pitch.html

# Replace placeholders and customize
```

## Available Templates

| Template | Purpose | Theme | Placeholders |
|----------|---------|-------|--------------|
| `pitch.html` | One-page product/idea pitch | Dark | `{{TITLE}}`, `{{TAGLINE}}`, etc. |
| `landing-dark.html` | Marketing landing page | Dark | Hero, features, pricing, CTA |
| `landing-light.html` | Marketing landing page | Light | Hero, features, pricing, CTA |
| `landing-aws-dark.html` | AWS-styled landing page | Dark | Cloudscape-inspired |
| `landing-aws-light.html` | AWS-styled landing page | Light | Cloudscape-inspired |
| `microsite.html` | Multi-section microsite | Dark | Flexible sections |
| `mockup.html` | General UI mockup | Dark | Minimal, component-focused |
| `lofi-wireframe.html` | Low-fidelity wireframe | Light | Sketch-style, grayscale |

## Template Details

### pitch.html
**Best for:** Product pitches, idea presentations, stakeholder decks

**Sections:**
- Sticky header with title + badge
- Hero with gradient headline
- Comparison table (before/after)
- Stats grid (4-up metrics)
- Tagline CTA box
- Footer with date + commit hash

**Placeholders:**
```
{{TITLE}}              - Project name
{{AUTHOR}}             - Author/company name
{{HEADLINE_PREFIX}}    - First part of headline
{{HEADLINE_HIGHLIGHT}} - Gradient-highlighted text
{{SUBHEADLINE}}        - Supporting description
{{COMPARISON_TITLE}}   - Table section title
{{COL1_HEADER}}        - Left column header
{{COL2_HEADER}}        - Right column header
{{ROW1_COL1}} ... {{ROW4_COL2}} - Table cells
{{STATS_TITLE}}        - Stats section title
{{STAT1_VALUE}} ... {{STAT4_LABEL}} - Stat cards
{{TAGLINE}}            - Closing tagline quote
{{STATUS_BADGE}}       - Badge text (e.g., "Ready to Build")
{{DATE}}               - Generation date
{{COMMIT_HASH}}        - Git commit hash
```

### landing-dark.html / landing-light.html
**Best for:** Marketing sites, product launches, SaaS landing pages

**Sections:**
- Navigation bar
- Hero with CTA buttons
- Logo strip
- Features grid (6 cards)
- Pricing tiers (3 cards)
- Final CTA
- Footer with links

### microsite.html
**Best for:** Documentation, project sites, portfolio pages

### mockup.html
**Best for:** UI component mockups, design explorations

### lofi-wireframe.html
**Best for:** Early-stage wireframes, quick sketches, stakeholder reviews

## Design System

All templates use the same design tokens:

**Colors (Dark Theme):**
- `--background`: Near-black
- `--foreground`: Near-white
- `--primary`: White (buttons, accents)
- `--secondary`: Dark gray (cards, backgrounds)
- `--muted-foreground`: Medium gray (secondary text)

**Components:**
- `.btn` / `.btn-primary` / `.btn-outline` - Buttons
- `.card` - Bordered container
- `.badge` - Pill-shaped label
- `code` - Inline code styling

**Typography:**
- System font stack
- Tailwind utilities for sizing

## Adding New Templates

1. Copy closest existing template
2. Use `{{PLACEHOLDER}}` syntax for customizable content
3. Keep shadcn/ui CSS variables and Tailwind config
4. Add footer with date + commit hash
5. Document in this README
6. Commit to `shared/design-system/templates/`

## Footer Standard

All templates should include a footer with:
```html
<footer class="border-t py-8">
  <div class="container mx-auto px-4">
    <div class="flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-muted-foreground">
      <div>
        <span class="font-semibold text-foreground">{{AUTHOR}}</span> · {{TITLE}}
      </div>
      <div class="flex gap-4">
        <span>Generated: {{DATE}}</span>
        <span>·</span>
        <span>Commit: <code>{{COMMIT_HASH}}</code></span>
      </div>
    </div>
  </div>
</footer>
```

## Related

- `shared/design-system/README.md` - Full design system docs
- `shared/design-system/src/` - React components
- `shared/design-system/examples/` - Example implementations
