---
description: Generate beautiful Figma/Miro-style architecture diagrams in HTML (mobile responsive)
version: 1.0.0
tags: [architecture, diagram, visualization, html, design]
---

# Architecture Diagram Generator

Generate beautiful, interactive architecture diagrams in Figma/Miro style with mobile-responsive HTML.

## Usage

```bash
/arch-diagram [description]
```

**Parameters:**
- `description` (optional): Brief description of the architecture to diagram

## Examples

```bash
# Generate diagram for current project
/arch-diagram

# Generate specific architecture
/arch-diagram three-tier web application with microservices

# Generate AWS serverless architecture
/arch-diagram serverless api with lambda dynamodb and s3
```

## What It Does

1. Analyzes project context or uses provided description
2. Identifies key components, services, data flows
3. Generates beautiful HTML diagram with:
   - Modern Figma/Miro aesthetic (rounded corners, shadows, gradients)
   - Color-coded components (services, databases, external APIs, users)
   - Animated connection lines showing data flow
   - Interactive hover states
   - Zoom and pan capabilities
   - Mobile-responsive layout
4. Saves to `docs/architecture/` or project-appropriate location
5. Optionally publishes to S3 for sharing

## Design Principles

- **Visual Hierarchy:** Clear grouping with subtle backgrounds
- **Color Palette:** Professional gradients (blues, purples, teals)
- **Typography:** Clean sans-serif fonts (Inter, SF Pro)
- **Spacing:** Generous whitespace, balanced layout
- **Interaction:** Smooth transitions, hover effects
- **Responsive:** Adapts to mobile, tablet, desktop

## Output Format

Creates standalone HTML file with:
- Embedded CSS (no external dependencies)
- SVG-based diagram with CSS animations
- Touch-friendly controls
- Legend explaining component types
- Metadata (project name, date, version)

---

Generate a beautiful, mobile-responsive architecture diagram in HTML with modern Figma/Miro styling.

**Instructions:**

1. **Gather Context**
   - If description provided, use it
   - Otherwise, analyze current project (read .project, README, key files)
   - Identify: components, services, data stores, external integrations, users/actors

2. **Design Layout**
   - Use swim lanes or layered approach (presentation → business logic → data)
   - Group related components with subtle background regions
   - Position elements for clear left-to-right or top-to-bottom flow

3. **Generate HTML**
   - Use semantic HTML5 structure
   - Embedded CSS with CSS Grid/Flexbox for layout
   - SVG for diagram elements with:
     * Rounded rectangles (border-radius: 12px)
     * Subtle shadows (box-shadow with blur)
     * Gradient fills (linear-gradient or subtle radial)
     * Animated arrows/lines (CSS animations or SVG stroke-dasharray)
   - Color scheme:
     * Services/compute: Blue gradients (#4A90E2 → #357ABD)
     * Databases: Purple gradients (#9B59B6 → #8E44AD)
     * External APIs: Teal gradients (#1ABC9C → #16A085)
     * Users/actors: Orange/warm gradients (#E67E22 → #D35400)
   - Typography: system-ui, -apple-system, "Segoe UI", sans-serif
   - Mobile responsive:
     * @media queries for tablet (< 1024px) and mobile (< 768px)
     * Stack layers vertically on mobile
     * Touch-friendly minimum sizes (44px × 44px)

4. **Add Interactivity**
   - Hover effects on components (scale, glow, tooltip)
   - Click to highlight data flow paths
   - Optional zoom/pan controls (simple CSS transform)
   - Legend toggle for component types

5. **Save & Present**
   - Save to `docs/architecture/{project-name}-architecture.html`
   - Test that it renders correctly
   - Ask: "Open diagram? [1] yes [2] publish to S3 [3] skip"

**Example Structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Architecture Diagram</title>
  <style>
    /* Modern reset and base styles */
    /* CSS Grid layout */
    /* Component styles with gradients */
    /* Animation keyframes */
    /* Mobile responsive queries */
  </style>
</head>
<body>
  <div class="diagram-container">
    <header>
      <h1>Project Architecture</h1>
      <div class="legend"><!-- Color key --></div>
    </header>
    <main class="architecture-diagram">
      <!-- SVG or CSS-based diagram elements -->
    </main>
  </div>
</body>
</html>
```

Create a stunning, professional architecture diagram that clearly communicates system design.
