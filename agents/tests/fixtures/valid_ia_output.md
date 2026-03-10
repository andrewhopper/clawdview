---
name: "valid_ia_output_fixture"
uuid: 1d352e5b-8442-4f4d-b1ba-b061d922c6da
---

# Information Architecture: Analytics Dashboard

## Navigation Hierarchy

```
├── Primary Nav
│   ├── Dashboard (default)
│   │   ├── Overview
│   │   └── Real-time
│   ├── Reports
│   │   ├── Daily
│   │   ├── Weekly
│   │   └── Custom
│   ├── Settings
│   │   ├── Account
│   │   └── Integrations
│   └── Help
└── Utility Nav
    ├── Profile
    ├── Notifications
    └── Logout
```

**Depth Analysis:** 3 levels (within limit)
**Pattern:** Sidebar navigation (recommended for data-heavy dashboards)

## User Flow: First-time Setup

```
┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────┐
│  Login  │───▶│ Connect Data│───▶│ Set Metrics │───▶│Dashboard│
└─────────┘    └──────┬──────┘    └──────┬──────┘    └─────────┘
                     │                  │
                ┌────▼────┐        ┌────▼────┐
                │ Skip    │        │ Skip    │
                │ (later) │        │ (later) │
                └─────────┘        └─────────┘
```

**Happy Path:** Login → Connect Data → Set Metrics → Dashboard
**Alternative:** Users can skip setup and configure later

## Content Hierarchy

```
Page: Dashboard
├── [P1] Key Metrics (above fold)
│   ├── Total Revenue
│   ├── Active Users
│   └── Conversion Rate
├── [P2] Charts Section
│   ├── Trend Line
│   └── Comparison Bar
├── [P3] Recent Activity
└── [P4] Quick Actions
```

## IA HANDOFF SUMMARY:
- Navigation pattern: sidebar
- Page count: 9 pages across 4 sections
- Key flows: first-time setup, daily review, report export
- Components needed: [sidebar, breadcrumbs, tabs, cards, charts]
- Ready for: UX agent to compose visual components
