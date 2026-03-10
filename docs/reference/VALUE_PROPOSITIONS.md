## 💡 VALUE PROPOSITION REGISTRY (problems/)

**Purpose:** Capture customer segments, jobs, pains, and gains using Strategyzer's Value Proposition Canvas framework to inform prototype development.

### Framework

```
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│     VALUE MAP (Prototypes)      │     │    CUSTOMER PROFILE (Problems)  │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│  🎁 Gain Creators               │────▶│  📈 Gains (Desired outcomes)    │
│  💊 Pain Relievers              │────▶│  😫 Pains (Obstacles, risks)    │
│  🛠️  Products & Services         │────▶│  📋 Jobs (Tasks to accomplish)  │
└─────────────────────────────────┘     └────────┬────────────────────────┘
                                                 │
                                        👤 Customer Segment (Who)
```

### File Types

**👤 Customer Segments (WHO)** - `customer-description-{6char}.md`
- Define personas: roles, demographics, behaviors
- Example: `customer-dev-teams-using-ai-i6d9e3.md`

**📋 Customer Jobs (WHAT)** - `job-description-{6char}.md`
- What customers are trying to accomplish
- Types: Functional (tasks), Social (image), Emotional (feelings)
- Example: `job-design-system-architecture-j7e1f4.md`

**😫 Customer Pains (OBSTACLES)** - `pain-description-{6char}.md`
- Negative outcomes, risks, obstacles preventing job completion
- Intensity: Extreme, Severe, Moderate, Light
- Example: `pain-ai-slow-latency-o3d6e9.md`

**📈 Customer Gains (DESIRES)** - `gain-description-{6char}.md`
- Positive outcomes, benefits, desires from completing jobs
- Importance: Essential, Expected, Desired, Nice-to-have
- Example: `gain-consistent-ai-decisions-l9a3b6.md`

### Filename Convention

**Format:** `[type]-[2-3-word-description]-[6char].md`

**Components:**
- **Type:** `customer`, `job`, `pain`, or `gain`
- **Description:** 2-3 lowercase words, hyphen-separated (concise, descriptive)
- **ID:** 6-character alphanumeric identifier (generated via `openssl rand -hex 3`)

**Examples:**
- `customer-remote-dev-teams-a3f7c9.md`
- `job-pair-programming-b2e8d1.md`
- `pain-collaboration-latency-c4f9a3.md`
- `gain-seamless-pairing-d5a1b2.md`

### Relationship Model

```
CUSTOMER → has → JOBS → causing → PAINS → relieved by → PROTOTYPES (Pain Relievers)
                     └─→ expecting → GAINS → created by → PROTOTYPES (Gain Creators)
```

### Workflow

1. **Identify Customer:** Create `customer-description-{6char}.md`
2. **Define Jobs:** Create `job-description-{6char}.md` linked to customer
3. **Capture Pains:** Create `pain-description-{6char}.md` for obstacles
4. **Capture Gains:** Create `gain-description-{6char}.md` for desired outcomes
5. **Build Prototypes:** Reference pains/gains in Phase 1 seed docs
6. **Update Status:** Mark pains "Relieved" or gains "Delivered" when prototypes address them

### Prioritization

**Build order:**
1. **Essential gains + Extreme pains** (must-solve)
2. **Expected gains + Severe pains** (high ROI)
3. **Desired gains + Moderate pains** (nice-to-have)

**Exception:** High-impact opportunity (10x revenue) can override priority.

### ID Generation

```bash
# Generate 6-char ID
openssl rand -hex 3    # Returns: a3f7c9
```

### Status Values

**Customer Segments:** Active | Exploring | Deprioritized
**Jobs:** Active | Researching | Parked
**Pains:** Open | In Progress | Relieved | Obsolete
**Gains:** Open | In Progress | Delivered | Obsolete

**See:** `problems/README.md` for complete framework documentation.

