# UX & IA Audit Criteria

<!-- File UUID: 7e9f8d2c-1a3b-4c5d-6e7f-8a9b0c1d2e3f -->

Comprehensive audit checklist for Information Architecture and UX Component validation.

---

## 1.0 INFORMATION ARCHITECTURE (IA) AUDIT

### 1.1 Quality Checklist

After completing IA work, validate ALL of the following:

```
✓ All primary user goals have clear paths (< 3 clicks)
✓ Navigation hierarchy is 3 levels or fewer
✓ No more than 7 items at any single navigation level (Miller's Law)
✓ Labels are consistent and user-centered
✓ No orphan pages (everything reachable)
✓ Error/empty states considered
✓ Mobile navigation approach documented
✓ Primary tasks more accessible than secondary tasks
✓ Role-based validation completed (default: technical software engineer)
```

### 1.2 Core IA Principles

| Principle | Requirement | Validation |
|-----------|-------------|------------|
| **User Mental Models** | Structure by user thinking, not org structure | User goals documented, paths tested |
| **Progressive Disclosure** | Show only what's needed at each step | Information layered appropriately |
| **Clear Wayfinding** | Users know: where they are, where they can go, how to get back | Breadcrumbs, consistent landmarks |
| **Flat > Deep** | Max 3 levels deep | Hierarchy diagram shows depth |
| **Miller's Law** | 7 items max per level | Count items at each navigation level |
| **Clear Labels** | Plain language, specific, consistent | No jargon, labels reviewed |
| **Task Prioritization** | Primary tasks more prominent than secondary | Visual prominence matches task priority |

### 1.3 Required Deliverables

| Deliverable | Format | Must Include |
|-------------|--------|--------------|
| **Navigation Hierarchy** | ASCII tree | Primary, secondary, utility nav |
| **User Flows** | Flowchart/ASCII | Decision points, error paths |
| **Content Hierarchy** | Priority list | P1 (above fold), P2, P3 |
| **Sitemap** | Tree format | All pages, relationships, templates |
| **Task Accessibility Map** | Task-to-UI mapping | Primary vs secondary task prominence |

---

## 2.0 UX COMPONENT AUDIT

### 2.1 Design System Compliance Checklist

Before completing any visual asset:

**Foundation Check:**
```
✓ All colors use hsl(var(--token)) format (NEVER raw hex)
✓ Typography uses scale (text-xs through text-7xl)
✓ Spacing uses token scale (space-1 through space-16)
✓ Border radius uses tokens (rounded-sm/md/lg)
```

**Hierarchy Check:**
```
✓ Clear visual hierarchy (3 levels max: H1 > H2 > Body)
✓ Single primary focal point per section
✓ Adequate whitespace between elements
✓ Consistent element sizing
✓ Primary tasks visually dominant over secondary tasks
```

**Architecture Check:**
```
✓ Logical content grouping
✓ Clear navigation (if applicable)
✓ Consistent labeling
✓ Semantic HTML (<header>, <main>, <footer>, <nav>)
```

**Metadata Check:**
```
✓ Asset UUID assigned (8-char)
✓ Project UUID referenced
✓ Version number included (v1, v2, etc.)
✓ Date recorded (YYYY-MM-DD)
✓ Atomic level classified (atom/molecule/organism/template/page)
✓ Design tokens documented
✓ Target persona documented (default: technical software engineer, 35yo)
```

**Miller's Law (Cognitive Load):**
```
✓ No more than 7 navigation items at any single level
✓ No more than 7 action buttons visible per section
✓ Tab bars limited to 7 tabs max
✓ Dropdown/select menus with >7 options use grouping or search
```

**Accessibility:**
```
✓ Accessible contrast ratios (4.5:1 for text)
✓ Interactive states defined (hover, focus, active)
✓ ARIA labels where needed
✓ Keyboard navigation supported
✓ Primary tasks keyboard-accessible without mouse
```

**Performance:**
```
✓ File size within atomic level limit:
  - Atom: 5KB max
  - Molecule: 15KB max
  - Organism: 50KB max
  - Template: 100KB max
  - Page: 150KB max
✓ Minimal external resources (prefer inline CSS)
✓ Minimal inline styles (prefer Tailwind classes)
✓ DOM nesting depth under 15 levels
```

### 2.2 Asset Header Template (REQUIRED)

Every asset MUST include this metadata block:

```html
<!--
  Asset: {descriptive-name}
  Project: {project-uuid}
  Asset ID: {8-char-uuid}.v{N}
  Date: {YYYY-MM-DD}
  Design System: shared/design-system

  Atomic Level: {atom|molecule|organism|template|page}

  Target Persona: {persona-name or default}

  Task Accessibility:
  - Primary: {list primary tasks and their accessibility paths}
  - Secondary: {list secondary tasks and their accessibility paths}

  Tokens Used:
  - Colors: --background, --foreground, --primary
  - Spacing: space-4, space-6
  - Typography: text-base, text-lg
-->
```

### 2.3 Common Violations & Fixes

| Violation | Fix |
|-----------|-----|
| Raw hex colors (#1a1a2e) | Replace with `hsl(var(--token))` |
| Inline styles in React | Use Tailwind classes |
| Inconsistent spacing (17px, 23px) | Use spacing tokens (space-4 = 16px) |
| Missing hierarchy | Add clear H1 > H2 > body structure |
| No metadata comment | Add asset header block |
| Magic numbers | Replace with design tokens |
| >7 nav items at one level | Group into categories |
| Multiple primary CTAs | Single focal point per section |
| >3 heading levels | Flatten to H1 > H2 > Body only |
| Primary/secondary tasks same prominence | Increase size, contrast, position of primary |
| No persona specified | Add target persona to metadata |

---

## 3.0 PRIMARY/SECONDARY TASK ACCESSIBILITY

### 3.1 Overview

Primary tasks must be more accessible (visually prominent, fewer steps, easier to find) than secondary tasks. This follows the Pareto principle: 80% of users will use 20% of features.

### 3.2 Task Classification

Before designing any interface, classify all tasks:

```yaml
task_classification:
  primary_tasks:
    definition: "Tasks users perform frequently or that are critical to core workflow"
    examples:
      - "Create new project"
      - "Search items"
      - "View dashboard"
      - "Submit form"
    accessibility_requirements:
      - "≤ 2 clicks from home"
      - "Above the fold on relevant pages"
      - "Largest/most prominent CTAs"
      - "Keyboard shortcuts available"

  secondary_tasks:
    definition: "Tasks performed occasionally or by power users"
    examples:
      - "Export data"
      - "Advanced settings"
      - "Bulk operations"
      - "Generate report"
    accessibility_requirements:
      - "≤ 3 clicks from home"
      - "Available but not prominent"
      - "Secondary/ghost button styling"
      - "May require hover/dropdown to reveal"
```

### 3.3 Visual Prominence Hierarchy

| Task Priority | Button Style | Placement | Size | Keyboard Shortcut |
|---------------|-------------|-----------|------|-------------------|
| **Primary** | Solid, primary color | Above fold, center/right | Large (px-6 py-3) | Required (e.g., Cmd+N) |
| **Secondary** | Outline or ghost | Below fold or sidebar | Medium (px-4 py-2) | Optional |
| **Tertiary** | Text link or icon | Utility nav or overflow menu | Small (px-3 py-1) | Rare |

### 3.4 Task Accessibility Audit Checklist

For every interface design:

```
Step 1: List all tasks
├── Primary tasks (3-5 max)
├── Secondary tasks (5-10 max)
└── Tertiary tasks (remaining)

Step 2: Map tasks to UI elements
├── Where does each task appear?
├── How many clicks to reach?
└── What visual weight does it have?

Step 3: Validate prominence
├── Primary tasks are largest/most prominent? ✓
├── Primary tasks ≤ 2 clicks from home? ✓
├── Secondary tasks less prominent but findable? ✓
├── Tertiary tasks hidden in overflow/settings? ✓
└── No competing primary CTAs on same screen? ✓

Step 4: Validate accessibility paths
├── Primary tasks keyboard-accessible (Tab + Enter)? ✓
├── Primary tasks have keyboard shortcuts? ✓
├── Secondary tasks reachable via keyboard? ✓
└── Error recovery paths clear? ✓
```

### 3.5 Example: Dashboard Task Accessibility

```
PRIMARY TASKS:
├── Create New Project
│   ├── Placement: Top-right, always visible
│   ├── Style: Solid primary button, large
│   ├── Shortcut: Cmd+N / Ctrl+N
│   └── Clicks: 0 (always visible)
│
└── Search Projects
    ├── Placement: Top-center, search bar
    ├── Style: Prominent input with icon
    ├── Shortcut: Cmd+K / Ctrl+K
    └── Clicks: 0 (always visible)

SECONDARY TASKS:
├── Export All Projects
│   ├── Placement: Dropdown in header
│   ├── Style: Outline button or menu item
│   ├── Shortcut: None
│   └── Clicks: 1 (open dropdown)
│
└── Filter by Status
    ├── Placement: Sidebar or toolbar
    ├── Style: Toggle or dropdown
    ├── Shortcut: None
    └── Clicks: 1 (click filter)

TERTIARY TASKS:
├── Change Theme
│   ├── Placement: Settings page
│   ├── Style: Radio buttons or toggle
│   ├── Shortcut: None
│   └── Clicks: 2 (Settings → Theme)
│
└── View Audit Log
    ├── Placement: Settings page, admin section
    ├── Style: Text link
    ├── Shortcut: None
    └── Clicks: 3 (Settings → Admin → Audit)
```

### 3.6 Common Task Accessibility Issues

| Issue | Example | Fix |
|-------|---------|-----|
| **Primary task buried** | "Create" button in overflow menu | Move to always-visible position |
| **Competing primaries** | Multiple solid blue CTAs on one screen | Keep ONE primary, make others outline |
| **No keyboard access** | Critical action requires mouse hover | Add keyboard shortcut or focus state |
| **Secondary too prominent** | "Export" button same size as "Create" | Reduce size, change to outline style |
| **Unclear priority** | All buttons same style | Apply visual hierarchy (solid > outline > text) |
| **Deep nesting** | Primary task 4+ clicks away | Promote to top-level or add shortcut |

---

## 4.0 ROLE-BASED AUDIT

### 4.1 Default Persona

**UNLESS otherwise specified in .project file or design brief, assume this default persona:**

```yaml
default_persona:
  name: "Technical Software Engineer"
  age: 35
  experience: "10+ years professional development"
  technical_skill: "Expert"
  domain_knowledge: "High"

  characteristics:
    - Comfortable with technical jargon
    - Values efficiency over hand-holding
    - Expects keyboard shortcuts
    - Prefers dense information over whitespace
    - Appreciates advanced features
    - Tolerates complexity if it unlocks power

  task_preferences:
    - Quick access to advanced features
    - CLI or API alternatives to UI
    - Bulk operations and automation
    - Detailed logs and debugging info
    - Customization and configuration options

  anti_patterns:
    - Overly simplified UIs ("dumbed down")
    - Wizards with too many steps
    - Hiding advanced features completely
    - Long onboarding flows
    - Excessive confirmations for non-destructive actions
```

### 4.2 Role-Based Audit Checklist

For the default persona (technical software engineer, 35yo):

**Technical Depth:**
```
✓ Technical terms used appropriately (no over-simplification)
✓ Advanced features discoverable (not hidden)
✓ Keyboard shortcuts provided for frequent actions
✓ CLI/API alternatives documented
✓ Configuration options exposed (not auto-magic)
✓ Error messages include technical details (stack traces, codes)
✓ Logs and debugging tools available
```

**Information Density:**
```
✓ Dense layouts acceptable (no excessive whitespace)
✓ Tables/grids preferred over cards for data
✓ Information revealed on hover (not requiring clicks)
✓ Compact mode available for dashboards
✓ Multiple items per page (not paginated excessively)
```

**Efficiency:**
```
✓ Bulk operations available (select multiple, batch actions)
✓ Keyboard navigation fully supported (Tab, arrows, shortcuts)
✓ Quick actions via context menu (right-click)
✓ Search/filter on every list view
✓ Autocomplete and smart suggestions
✓ Undo/redo for non-trivial actions
```

**Flexibility:**
```
✓ Customizable views (column selection, sorting, grouping)
✓ Saved filters and custom queries
✓ Export to common formats (JSON, CSV, YAML)
✓ Import from common formats
✓ Theme/appearance customization
✓ Extension points or plugin system (if applicable)
```

**Trust & Control:**
```
✓ Minimal confirmations for safe actions (e.g., "Are you sure?" only for destructive ops)
✓ Ability to bypass wizards (advanced mode)
✓ Direct access to underlying data (inspect mode)
✓ Clear documentation of what's happening behind the scenes
✓ No forced tutorials (optional, dismissible)
```

### 4.3 Persona Adaptation

If .project file specifies a different persona, adjust audit criteria:

```yaml
persona_adjustments:
  non_technical_user:
    - Reduce jargon, add tooltips
    - Hide advanced features behind "Advanced" toggle
    - Add onboarding wizard
    - More confirmations for irreversible actions
    - Use cards/visual layouts over dense tables

  executive_decision_maker:
    - Focus on high-level metrics, not details
    - Visual dashboards over raw data
    - Summaries and insights, not raw logs
    - Mobile-first (executives on the go)
    - Simplified navigation (fewer options)

  power_user_admin:
    - Even denser than default engineer persona
    - CLI-first, UI-second
    - Raw access to configs and databases
    - No confirmations except for data loss
    - Scriptable and automatable

  occasional_user:
    - More guidance and onboarding
    - Simpler navigation (fewer choices)
    - Remembers state (resume where left off)
    - Help text and examples prominent
    - Progressive disclosure (hide complexity)
```

### 4.4 Role-Based Audit Workflow

```
Step 1: Identify target persona
├── Read .project file for persona definition
├── Check design brief for persona specification
└── If none specified → default to technical software engineer, 35yo

Step 2: Map persona characteristics to UI requirements
├── Technical skill level → jargon usage, feature complexity
├── Domain knowledge → onboarding needs, help text
├── Task frequency → keyboard shortcuts, quick actions
└── Efficiency preferences → information density, navigation depth

Step 3: Audit interface against persona requirements
├── Language: appropriate technical depth? ✓
├── Features: right balance of simple/advanced? ✓
├── Navigation: matches persona's mental model? ✓
├── Information density: matches persona's preference? ✓
└── Efficiency: matches persona's workflow speed? ✓

Step 4: Document persona assumptions
├── Add persona to asset metadata
├── Note any deviations from default persona
└── Justify UI choices based on persona needs
```

### 4.5 Persona-Specific Examples

**Example 1: Default Technical Engineer Persona**

```html
<!-- Dashboard for technical engineer -->
<main class="p-4">
  <!-- Dense layout: multiple stats visible -->
  <div class="grid grid-cols-4 gap-4 mb-6">
    <div class="stat-card">
      <p class="text-xs text-muted-foreground">Uptime</p>
      <p class="text-2xl font-bold">99.97%</p>
      <p class="text-xs text-primary">+0.02% vs yesterday</p>
    </div>
    <!-- More stats... -->
  </div>

  <!-- Table view (dense, sortable, filterable) -->
  <div class="table-container">
    <div class="flex justify-between mb-2">
      <input type="search" placeholder="Filter..." class="w-64" />
      <div class="flex gap-2">
        <button class="btn-outline">Export JSON</button>
        <button class="btn-outline">Bulk Edit</button>
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <th><input type="checkbox" /></th>
          <th>ID</th>
          <th>Status</th>
          <th>Created</th>
          <th>Actions</th>
        </tr>
      </thead>
      <!-- Rows... -->
    </table>
  </div>
</main>

<!--
Justification:
- Dense grid layout: engineer can process multiple stats at once
- Table view: efficient for scanning structured data
- Bulk actions: power user feature
- JSON export: technical format expected
- No excessive whitespace or "cards"
-->
```

**Example 2: Non-Technical User Persona**

```html
<!-- Same dashboard, adapted for non-technical user -->
<main class="p-8">
  <!-- Card-based layout: one stat per card, more whitespace -->
  <div class="grid grid-cols-2 gap-6 mb-8">
    <div class="card p-6 border border-border rounded-lg">
      <div class="flex items-center gap-3 mb-2">
        <span class="text-3xl">⬆️</span>
        <p class="text-sm text-muted-foreground">Website Availability</p>
      </div>
      <p class="text-3xl font-bold">99.97%</p>
      <p class="text-sm text-primary mt-2">Everything is running smoothly!</p>
    </div>
    <!-- More cards... -->
  </div>

  <!-- Card grid (visual, less dense) -->
  <div class="mb-6">
    <h2 class="text-xl font-semibold mb-4">Recent Activity</h2>
    <div class="grid grid-cols-1 gap-4">
      <div class="card p-4 border border-border rounded-lg">
        <div class="flex justify-between items-start">
          <div>
            <p class="font-medium">Project Alpha</p>
            <p class="text-sm text-muted-foreground">Created 2 hours ago</p>
          </div>
          <button class="btn-primary">View</button>
        </div>
      </div>
      <!-- More cards... -->
    </div>
  </div>
</main>

<!--
Justification:
- Card layout: easier to scan for non-technical users
- More whitespace: reduces cognitive load
- Friendly language: "Everything is running smoothly" vs "99.97% uptime"
- No bulk actions: non-technical users work one-at-a-time
- No JSON export: would prefer CSV or PDF
-->
```

---

## 4.5 VIEWPORT UTILITY DENSITY (VUD) AUDIT

### 4.5.1 Overview

VUD measures what percentage of the above-the-fold (ATF) viewport serves the user's actual goals versus decorative or wasted space. Pages that waste 40%+ of viewport on hero images and oversized text fail this audit.

### 4.5.2 Page Type Classification (MANDATORY)

Every page-level asset MUST be classified before layout:

| Page Type | Primary Goal | Hero Allowed | VUD Target | ATF Content Target |
|-----------|-------------|-------------|------------|-------------------|
| **WEBAPP** | Task completion | NEVER | ≥ 0.70 | 80%+ functional content |
| **DOCUMENTATION** | Find & understand | NEVER | ≥ 0.75 | 90%+ readable content |
| **PRODUCT** | Evaluate & convert | Compact (≤40vh) | ≥ 0.50 | 60%+ substantive content |
| **MARKETING** | Inspire & convert | Allowed (≤60vh) | ≥ 0.35 | 40%+ substantive content |

### 4.5.3 Reference Viewports

| Device | Width | Height | Usable ATF (minus chrome) |
|--------|-------|--------|--------------------------|
| Desktop HD | 1920px | 1080px | 1920 × 944 = 1,812,480px² |
| Desktop std | 1440px | 900px | 1440 × 764 = 1,100,160px² |
| Laptop small | 1366px | 768px | 1366 × 632 = 863,312px² |
| Tablet landscape | 1024px | 768px | 1024 × 632 = 646,768px² |
| Mobile | 390px | 844px | 390 × 708 = 276,120px² |

*Deductions: ~80px browser chrome, ~56px app navigation*

### 4.5.4 VUD Element Weights

| Element Category | Weight | Examples |
|-----------------|--------|----------|
| Primary task UI | 1.0 | Data tables, forms, editors, dashboards |
| Search / filters | 0.9 | Search bar, filter controls, sort |
| Navigation (functional) | 0.8 | Sidebar, tabs, breadcrumbs |
| Status / feedback | 0.7 | Alerts, progress indicators, toasts |
| Secondary actions | 0.5 | Export, settings, help links |
| Descriptive text | 0.4 | Help text, descriptions, labels |
| Branding (compact) | 0.3 | Logo + app name (single line) |
| Decorative whitespace | 0.1 | Margins beyond spacing tokens |
| Hero image / decoration | 0.05 | Stock photos, gradient backgrounds |
| Empty / wasted space | 0.0 | Unused viewport area |

### 4.5.5 VUD Calculation

```
VUD = Σ(element_area_px² × element_weight) / total_ATF_usable_area_px²

PASS/FAIL:
  VUD ≥ page_type_target → ✅ PASS
  VUD < page_type_target → ❌ FAIL — restructure layout
```

### 4.5.6 VUD Audit Checklist

```
☐ Page type classified (WEBAPP / DOCUMENTATION / PRODUCT / MARKETING)
☐ VUD target identified for page type
☐ ATF elements inventoried with area estimates (px²)
☐ Each element assigned weight from scoring table
☐ VUD score calculated
☐ VUD meets minimum for page type
☐ P1 content fully visible above the fold
☐ Hero section respects page type allowance
☐ No decorative elements >10% of ATF for webapp/docs
☐ Viewport height budget follows page type spec
```

### 4.5.7 Common VUD Failures

| Failure | Page Type | VUD Impact | Fix |
|---------|-----------|-----------|-----|
| Full-viewport hero image | WEBAPP | Drops to ~0.08 | Remove hero entirely, start with content |
| 72px heading + 48px subtitle | DOCS | Wastes 120px of height | Use text-2xl heading, start content immediately |
| Decorative gradient section | PRODUCT | 0.05 weight per px² | Replace with feature comparison table |
| 3 identical card rows | MARKETING | Low info density | Consolidate to single data-rich comparison |
| 200px of whitespace padding | WEBAPP | 0.0 weight | Reduce to space-4 (16px) between sections |
| Logo + tagline taking 180px | DOCS | 0.3 weight max | Compact to 48px header bar |

---

## 5.0 VALIDATION WORKFLOW

### 5.1 IA Validation Steps

```
1. User Goal Check
   ├── List top 3-5 user goals
   ├── Verify each has path ≤ 3 clicks
   └── Priority goals are easiest to reach

2. Navigation Depth Check
   ├── Map full hierarchy
   ├── Count levels (must be ≤ 3)
   └── No dead ends or orphan pages

3. Miller's Law Check
   ├── Count items at each nav level
   ├── Must be ≤ 7 items
   └── If >7, propose grouping

4. Label Consistency Check
   ├── List all nav labels
   ├── Check for plain language (no jargon)
   └── Verify consistency across product

5. Mobile Adaptation Check
   └── Document how nav works on mobile

6. Task Accessibility Check
   ├── Identify primary tasks (3-5)
   ├── Verify primary tasks ≤ 2 clicks
   ├── Verify primary tasks above fold
   ├── Check secondary tasks less prominent
   └── Validate keyboard shortcuts for primary

7. Persona Validation Check
   ├── Identify target persona (default: tech engineer)
   ├── Verify technical depth matches persona
   ├── Check information density matches persona
   └── Validate efficiency features for persona
```

### 5.2 UX Validation Steps

```
1. Token Scan
   ├── Search for raw hex values (#)
   ├── Search for inline styles with px values
   ├── Search for magic numbers (17px, 23px)
   └── Replace ALL with tokens

2. Hierarchy Audit
   ├── Count heading levels (H1, H2, H3, H4...)
   ├── If >3 levels, flatten structure
   ├── Count primary CTAs per section
   └── If >1, reduce to single focal point

3. Metadata Verification
   ├── Confirm asset UUID present
   ├── Verify project UUID matches .project
   ├── Check date is ISO format
   ├── Validate atomic level classification
   ├── Check persona documented
   └── Verify task accessibility map present

4. Accessibility Test
   ├── Run contrast checker on text
   ├── Verify focus states visible
   ├── Test keyboard navigation
   ├── Check ARIA labels
   └── Test primary task keyboard shortcuts

5. Performance Check
   ├── Measure file size vs limit
   ├── Count external resources
   ├── Measure DOM depth
   └── Estimate FCP (target <1800ms)

6. Task Accessibility Validation
   ├── Count primary tasks (should be 3-5)
   ├── Verify primary tasks have largest buttons
   ├── Check primary tasks above fold
   ├── Validate keyboard shortcuts for primary
   └── Confirm secondary tasks less prominent

7. Persona Validation
   ├── Confirm persona documented
   ├── Check language/jargon matches persona
   ├── Verify information density matches persona
   ├── Validate feature complexity matches persona
   └── Check efficiency features match persona needs
```

---

## 6.0 QUICK REFERENCE TABLES

### 6.1 Atomic Design Levels

| Level | Definition | File Size Limit | Examples |
|-------|------------|-----------------|----------|
| Atom | Cannot be broken down further | 5KB | button, input, label, badge |
| Molecule | Simple groups of atoms | 15KB | card, alert, form-field |
| Organism | Complex sections | 50KB | header, sidebar, footer, modal |
| Template | Page layouts | 100KB | dashboard-layout, landing-page |
| Page | Real content instances | 150KB | login, settings, product-detail |

### 6.2 Design Token Categories

| Token Category | CSS Variable | Usage |
|----------------|--------------|-------|
| Background | `--background` | Page background |
| Foreground | `--foreground` | Primary text |
| Primary | `--primary` | Brand color, CTAs |
| Muted | `--muted` | Subtle backgrounds |
| Border | `--border` | Borders, dividers |
| Destructive | `--destructive` | Errors, warnings |

### 6.3 Spacing Scale (4px base)

| Token | Size | Usage |
|-------|------|-------|
| space-1 | 4px | Tight padding |
| space-2 | 8px | Standard padding |
| space-4 | 16px | Section padding |
| space-6 | 24px | Component margins |
| space-8 | 32px | Section gaps |
| space-12 | 48px | Major sections |
| space-16 | 64px | Page margins |

### 6.4 Typography Scale

| Token | Size | Usage |
|-------|------|-------|
| text-xs | 12px | Fine print, labels |
| text-sm | 14px | Secondary text |
| text-base | 16px | Body text |
| text-lg | 18px | Lead paragraphs |
| text-xl | 20px | Section headers |
| text-2xl | 24px | Card titles |
| text-3xl | 30px | Page sections |
| text-4xl | 36px | Page titles |

### 6.5 Task Priority Visual Hierarchy

| Task Priority | Button Size | Button Style | Placement | Keyboard Shortcut |
|---------------|-------------|--------------|-----------|-------------------|
| Primary | px-6 py-3 (large) | Solid, primary color | Above fold, center/right | Required |
| Secondary | px-4 py-2 (medium) | Outline or ghost | Below fold or sidebar | Optional |
| Tertiary | px-3 py-1 (small) | Text link or icon | Overflow menu | Rare |

### 6.6 Default Persona Characteristics

| Aspect | Technical Engineer (Default) | Non-Technical User | Executive |
|--------|------------------------------|-------------------|-----------|
| **Jargon** | High (technical terms) | Low (plain language) | Business terms only |
| **Density** | High (tables, compact) | Low (cards, whitespace) | Medium (dashboards) |
| **Keyboard** | Expected | Optional | Rare |
| **Shortcuts** | Required | Nice-to-have | Not needed |
| **Bulk Ops** | Expected | Rare | Delegated |
| **Customization** | High | Low | Low |
| **Confirmations** | Minimal | Frequent | Moderate |

---

## 7.0 COMPLETE VALIDATION CHECKLIST

Use this master checklist for every IA or UX asset:

```
INFORMATION ARCHITECTURE:
☐ All primary user goals have clear paths (< 3 clicks)
☐ Navigation hierarchy is 3 levels or fewer
☐ No more than 7 items at any single navigation level
☐ Labels are consistent and user-centered
☐ No orphan pages (everything reachable)
☐ Error/empty states considered
☐ Mobile navigation approach documented
☐ Primary tasks more accessible than secondary tasks
☐ Task accessibility map created

DESIGN SYSTEM COMPLIANCE:
☐ All colors use hsl(var(--token)) format
☐ Typography uses scale (text-xs through text-7xl)
☐ Spacing uses token scale (space-1 through space-16)
☐ Border radius uses tokens
☐ Visual hierarchy limited to 3 levels
☐ Single primary focal point per section
☐ Adequate whitespace between elements
☐ Consistent element sizing
☐ Semantic HTML used

METADATA:
☐ Asset UUID assigned (8-char)
☐ Project UUID referenced
☐ Version number included
☐ Date recorded (YYYY-MM-DD)
☐ Atomic level classified
☐ Target persona documented
☐ Task accessibility map included
☐ Design tokens documented

ACCESSIBILITY:
☐ Contrast ratios meet WCAG 2.1 AA (4.5:1)
☐ Interactive states defined (hover, focus, active)
☐ ARIA labels present where needed
☐ Keyboard navigation fully supported
☐ Primary tasks keyboard-accessible
☐ Keyboard shortcuts for primary tasks

MILLER'S LAW (COGNITIVE LOAD):
☐ No more than 7 navigation items per level
☐ No more than 7 action buttons per section
☐ Tab bars limited to 7 tabs
☐ Dropdowns with >7 options use grouping

TASK ACCESSIBILITY:
☐ Primary tasks identified (3-5 max)
☐ Primary tasks ≤ 2 clicks from home
☐ Primary tasks above fold
☐ Primary tasks visually dominant (largest buttons)
☐ Primary tasks have keyboard shortcuts
☐ Secondary tasks less prominent but findable
☐ Tertiary tasks hidden in overflow/settings

ROLE-BASED VALIDATION:
☐ Target persona identified (default: tech engineer, 35yo)
☐ Language/jargon matches persona
☐ Information density matches persona
☐ Feature complexity matches persona
☐ Efficiency features match persona needs
☐ Navigation matches persona mental model

VIEWPORT UTILITY DENSITY (page-level assets):
☐ Page type classified (WEBAPP / DOCUMENTATION / PRODUCT / MARKETING)
☐ VUD target identified for page type
☐ VUD score calculated and meets target
☐ P1 content fully visible above the fold
☐ Hero respects page type allowance (NEVER for webapp/docs)
☐ No decorative elements >10% of ATF for webapp/docs
☐ Viewport height budget follows page type spec

PERFORMANCE:
☐ File size within atomic level limit
☐ Minimal external resources
☐ Minimal inline styles
☐ DOM nesting depth under 15 levels
☐ Estimated FCP under 1800ms
```

---

**References:**
- Full guidelines: `hmode/shared/design-system/MANAGEMENT_GUIDELINES.md`
- Validation examples: `hmode/shared/design-system/examples/VALIDATION_REPORT.md`
- IA agent spec: `hmode/agents/information-architecture-agent.md`
- UX agent spec: `hmode/agents/ux-component-agent.md`
- Persona library: `shared/personas/` (if available)

**Version:** 1.2.0
**Last Updated:** 2026-03-07
**Changes from 1.1.0:**
- Added Section 4.5: Viewport Utility Density (VUD) Audit
- Page type classification system (WEBAPP, DOCUMENTATION, PRODUCT, MARKETING)
- VUD scoring metric with element weights and targets per page type
- Reference viewport dimensions with usable ATF calculations
- Common VUD failures and fixes
- Updated complete validation checklist with VUD section

**Changes from 1.0.0:**
- Added Section 3.0: Primary/Secondary Task Accessibility
- Added Section 4.0: Role-Based Audit
- Added default persona (technical software engineer, 35yo)
- Updated asset header template with persona and task accessibility
- Expanded validation workflows with task and persona checks
- Added persona comparison table and examples
