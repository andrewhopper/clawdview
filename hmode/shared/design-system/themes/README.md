# shadcn/ui Themes

Custom theme collections for shadcn/ui components using HSL CSS variables.

## Available Themes

| Theme | Description | Variants |
|-------|-------------|----------|
| [Marine Sunset](./marine-sunset/) | Warm coral/orange tones with deep teal waters | Light, Dark |
| [Night Sky](./night-sky/) | Cosmic blues with violet nebula accents | Dawn, Midnight, Deep Space |

## Usage

### 1. Import CSS Variables

Copy the variables from `{theme}/variables.css` into your `globals.css`:

```css
@layer base {
  :root {
    /* Paste light mode variables here */
  }

  .dark {
    /* Paste dark mode variables here */
  }
}
```

### 2. Install Fonts (Optional)

Each theme includes recommended font pairings:

**Marine Sunset:**
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Source+Sans+Pro:wght@300;400;600;700&display=swap" rel="stylesheet">
```

**Night Sky:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 3. Preview Themes

Open the `demo.html` file in each theme folder to see the full color palette and component examples.

## Theme Structure

```
themes/
├── marine-sunset/
│   ├── variables.css    # HSL CSS variables
│   └── demo.html        # Interactive preview
├── night-sky/
│   ├── variables.css    # HSL CSS variables
│   └── demo.html        # Interactive preview (3 variants)
└── README.md
```

## Creating New Themes

1. Create a new folder: `themes/{theme-name}/`
2. Add `variables.css` with all shadcn/ui CSS variables
3. Create `demo.html` showing colors, typography, and components
4. Document font recommendations and usage

### Required CSS Variables

```css
--background
--foreground
--card / --card-foreground
--popover / --popover-foreground
--primary / --primary-foreground
--secondary / --secondary-foreground
--muted / --muted-foreground
--accent / --accent-foreground
--destructive / --destructive-foreground
--border
--input
--ring
--radius
--chart-1 through --chart-5
```

## Resources

- [shadcn/ui Theming Docs](https://ui.shadcn.com/docs/theming)
- [shadcn/ui Colors Reference](https://ui.shadcn.com/colors)
- [Theme Generator Tool](https://gradient.page/tools/shadcn-ui-theme-generator)
