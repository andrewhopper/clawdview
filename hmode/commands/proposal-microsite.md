# Generate Proposal Microsite

Generate a responsive HTML microsite for a technical proposal or RFC.

## Arguments
- `$ARGUMENTS` - Path to the proposal markdown file or project directory

## Instructions

Create a mobile-responsive HTML microsite based on the provided proposal/project with the following structure:

### Required Sections

1. **Hero Section**
   - Gradient background (purple/cyan gradient)
   - Project title (large, bold)
   - One-line value proposition
   - Key metric highlight (e.g., "50-80% cost reduction")
   - CTA buttons (How It Works, See Examples)

2. **Problem Section**
   - 3 problem cards with icons
   - Each card: icon, title, description
   - Use red/orange/yellow color scheme for urgency

3. **Solution Section**
   - Key dimensions/features as a grid (2x4 or similar)
   - Each dimension: emoji icon, title, subtitle
   - Brief explanation of the approach

4. **Architecture Diagram**
   - SVG diagram (not ASCII art)
   - Dark background section
   - Show data flow with arrows
   - Color-coded components
   - Include escalation/feedback loops if applicable

5. **Examples Section**
   - 3-5 concrete examples with real numbers
   - Color-coded cards by category/savings tier
   - Each example shows: task, model selected, cost, key metric
   - Include savings percentage badges

6. **Advanced Features** (if applicable)
   - 3 feature cards
   - Code snippets or diagrams
   - Concrete savings/benefits

7. **Code Example**
   - Dark theme code block
   - Syntax highlighting colors
   - Show simple and advanced usage

8. **Comparison Table** (if applicable)
   - Sortable/scannable table
   - Use checkmarks/X marks for features
   - Include cost column
   - Highlight best options

9. **CTA Section**
   - Gradient background matching hero
   - GitHub link
   - Secondary action

10. **Footer**
    - Project name
    - License
    - Key links

### Design System

**Colors:**
```css
primary: #6366f1 (indigo)
secondary: #8b5cf6 (purple)
accent: #06b6d4 (cyan)
dark: #0f172a (slate-900)
light: #f1f5f9 (slate-100)
```

**Gradients:**
- Hero/CTA: `linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%)`

**Typography:**
- Headings: Inter, bold
- Code: JetBrains Mono
- Body: Inter, regular

**Components:**
- Cards: rounded-2xl, shadow-sm, white background
- Buttons: rounded-lg, font-semibold
- Badges: rounded-full, colored backgrounds
- Tables: hover states, alternating backgrounds

### Technical Requirements

1. **Single HTML file** - All CSS inline or in `<style>` tags
2. **Tailwind CSS via CDN** - Use `<script src="https://cdn.tailwindcss.com"></script>`
3. **No external dependencies** except Google Fonts (Inter, JetBrains Mono)
4. **Mobile responsive** - Test at 375px, 768px, 1024px widths
5. **SVG diagrams** - Not ASCII art, use proper SVG with:
   - `<defs>` for gradients and markers
   - Proper arrow markers
   - Color-coded boxes
6. **Smooth animations** - Scroll reveal, hover effects
7. **Accessible** - Proper heading hierarchy, link text

### Process

1. Read the proposal/project files to understand:
   - What problem does it solve?
   - What are the key features/dimensions?
   - What are concrete examples with numbers?
   - What's the architecture/flow?

2. Generate the HTML following the template structure

3. Save to the project directory as `index.html`

4. Optionally publish to S3 with `--publish` flag

### Example Reference

See `hmode/examples/proposal-microsite-template.html` for a complete working example (Dynamic Model Router proposal).

### Output

After generating, provide:
- Path to generated `index.html`
- Offer to publish to S3 with temporary URL
