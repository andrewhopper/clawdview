# Swimlane Diagram Skill

<!-- File UUID: e8f9a2c4-7d1b-4a3e-9f2d-8c6b5e4a3d2f -->

## Overview

Generate interactive swimlane diagrams using React Flow with synchronized zooming, panning swimlane bands, and sticky left-aligned labels. Perfect for visualizing process flows, SDLC phases, multi-agent workflows, and cross-functional processes.

## When to Use

- Visualizing multi-stage processes with different actors/agents
- SDLC or workflow diagrams with approval gates
- Cross-functional process flows
- System interaction diagrams with multiple swimlanes
- Any process requiring horizontal timeline + vertical role separation

## Key Features

1. **Zoomable Swimlane Bands**: Semi-transparent colored bands that zoom/pan with the diagram
2. **Sticky Labels**: Left-aligned swimlane labels that stay visible during horizontal panning
3. **Mode Toggling**: Toggle between different workflow modes (e.g., full SDLC vs SPIKE)
4. **Interactive Nodes**: Click nodes for descriptions, drag to rearrange
5. **Design System Integration**: Uses HSL color tokens from shared design system
6. **Responsive Controls**: Built-in zoom controls, minimap, and background grid

## Tech Stack

- **Framework**: Vite + React + TypeScript
- **Library**: `@xyflow/react` (React Flow v12+)
- **Styling**: Inline styles with design system tokens

## Core Implementation Pattern

### 1. Swimlane Data Structure

```typescript
const swimlanes = [
  { id: 'actor1', label: 'Actor Name', color: '220 70% 50%', yOffset: 0 },
  { id: 'actor2', label: 'Another Actor', color: '160 60% 45%', yOffset: 150 },
  // yOffset: vertical position (150px spacing recommended)
  // color: HSL values (without 'hsl()' wrapper)
];

const phases = [
  {
    id: '1',
    number: '1.0',
    name: 'PHASE_NAME',
    swimlane: 'actor1', // references swimlane.id
    description: 'Phase description',
    xOffset: 0, // horizontal position
    spikeVisible: true, // optional: for mode toggling
  },
];
```

### 2. Viewport Tracking for Synchronized Zooming

```typescript
function FlowCanvas({ mode }: { mode: boolean }) {
  const reactFlowInstance = useReactFlow();
  const [viewport, setViewport] = useState({ x: 0, y: 0, zoom: 0.5 });

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {/* Swimlane bands - zoom and pan with diagram */}
      <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', zIndex: 0, overflow: 'hidden' }}>
        <div
          style={{
            position: 'absolute',
            transform: `translate(${viewport.x}px, ${viewport.y}px) scale(${viewport.zoom})`,
            transformOrigin: '0 0',
            transition: 'transform 0.05s ease-out',
          }}
        >
          {swimlanes.map((lane) => (
            <div
              key={lane.id}
              style={{
                position: 'absolute',
                left: -10000,
                width: 20000,
                top: lane.yOffset,
                height: 150,
                backgroundColor: `hsla(${lane.color} / 0.1)`,
                borderBottom: `1px solid hsla(${lane.color} / 0.3)`,
              }}
            />
          ))}
        </div>
      </div>

      {/* Sticky labels - only vertical pan and zoom, no horizontal */}
      <div style={{ position: 'absolute', left: 0, top: 0, pointerEvents: 'none', zIndex: 10 }}>
        <div
          style={{
            position: 'absolute',
            transform: `translateY(${viewport.y}px) scale(${viewport.zoom})`,
            transformOrigin: '0 0',
            transition: 'transform 0.05s ease-out',
          }}
        >
          {swimlanes.map((lane) => (
            <div
              key={lane.id}
              style={{
                position: 'absolute',
                left: 0,
                top: lane.yOffset,
                height: 150,
                display: 'flex',
                alignItems: 'center',
                paddingLeft: '12px',
                paddingRight: '12px',
                backgroundColor: `hsla(${lane.color} / 0.2)`,
                backdropFilter: 'blur(8px)',
                borderRight: `2px solid hsla(${lane.color} / 0.5)`,
              }}
            >
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: `hsl(${lane.color})` }}>
                {lane.label}
              </div>
            </div>
          ))}
        </div>
      </div>

      <ReactFlow
        nodes={nodes}
        edges={edges}
        onMove={(_event, viewport) => setViewport(viewport)}
        fitView
        minZoom={0.2}
        maxZoom={1.5}
      >
        <Background color="hsl(240 3.7% 15.9%)" gap={16} variant={BackgroundVariant.Dots} />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}
```

### 3. Node Creation with Conditional Visibility

```typescript
const createNodes = (mode: boolean): Node[] => {
  return phases
    .filter(phase => mode ? phase.spikeVisible : true)
    .map((phase) => {
      const swimlane = swimlanes.find((s) => s.id === phase.swimlane)!;
      const isSpecialGate = phase.swimlane === 'human'; // example

      return {
        id: phase.id,
        type: 'default',
        position: { x: phase.xOffset, y: swimlane.yOffset },
        data: {
          label: (
            <div>
              <div className="phase-number">{phase.number}</div>
              <div className="phase-name">{phase.name}</div>
            </div>
          ),
          description: phase.description,
        },
        style: {
          backgroundColor: isSpecialGate ? 'hsl(0 62.8% 30.6%)' : `hsl(${swimlane.color})`,
          borderColor: isSpecialGate ? 'hsl(0 62.8% 50.6%)' : `hsl(${swimlane.color})`,
          color: 'hsl(0 0% 98%)',
          padding: '12px 16px',
          borderRadius: isSpecialGate ? '4px' : '8px',
          borderWidth: isSpecialGate ? '3px' : '2px',
          borderStyle: isSpecialGate ? 'double' : 'solid',
        },
      };
    });
};
```

### 4. Edge Styling by Type

```typescript
const edgeDefinitions = [
  { source: '1', target: '2', label: 'Next', type: 'flow', spikeVisible: true },
  { source: '2', target: 'h1', label: 'Request approval', type: 'approval', spikeVisible: false },
  { source: 'h1', target: '3', label: 'Approved', type: 'gate', spikeVisible: false },
];

const createEdges = (mode: boolean): Edge[] => {
  return edgeDefinitions
    .filter(edge => mode ? edge.spikeVisible : edge.type !== 'spike')
    .map((edge, idx) => {
      let color = '240 5% 64.9%'; // muted gray
      let strokeDasharray: string | undefined;
      let animated = false;
      let strokeWidth = 2;

      if (edge.type === 'gate') {
        color = '340 75% 55%'; // pink - approval granted
        strokeWidth = 3;
        animated = true;
      } else if (edge.type === 'approval') {
        color = '0 62.8% 50.6%'; // red - requesting approval
        strokeDasharray = '5 5';
      } else if (edge.type === 'delegation') {
        color = '160 60% 45%'; // green - delegation
        animated = true;
      } else if (edge.type === 'handoff') {
        color = '280 65% 60%'; // purple - handoff
        strokeDasharray = '5 5';
      }

      return {
        id: `edge-${idx}`,
        source: edge.source,
        target: edge.target,
        label: edge.label,
        type: 'smoothstep',
        animated,
        style: { stroke: `hsl(${color})`, strokeWidth, strokeDasharray },
        markerEnd: { type: MarkerType.ArrowClosed, color: `hsl(${color})` },
      };
    });
};
```

### 5. Mode Toggle UI

```typescript
function App() {
  const [spikeMode, setSpikeMode] = useState(false);

  return (
    <div className="app-container">
      <header>
        <h1>Swimlane Diagram</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', justifyContent: 'center' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={spikeMode}
              onChange={(e) => setSpikeMode(e.target.checked)}
              style={{ width: '1.25rem', height: '1.25rem', accentColor: 'hsl(30 80% 55%)' }}
            />
            <span style={{ color: spikeMode ? 'hsl(30 80% 55%)' : 'hsl(var(--foreground))' }}>
              Alternate Mode (e.g., SPIKE Mode)
            </span>
          </label>
        </div>
      </header>
      <div className="flow-container">
        <ReactFlowProvider>
          <FlowCanvas mode={spikeMode} />
        </ReactFlowProvider>
      </div>
    </div>
  );
}
```

## Design System Integration

### Color Tokens (from `hmode/shared/design-system/design-system/src/globals.css`)

```css
:root {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --primary: 0 0% 98%;
  --muted: 240 3.7% 15.9%;
  --destructive: 0 62.8% 30.6%;
  --chart-1: 220 70% 50%; /* blue */
  --chart-2: 160 60% 45%; /* green */
  --chart-3: 30 80% 55%;  /* orange */
  --chart-4: 280 65% 60%; /* purple */
  --chart-5: 340 75% 55%; /* pink */
}
```

### Using Tokens

```typescript
// Swimlane colors
{ id: 'human', color: '220 70% 50%' } // chart-1
{ id: 'agent', color: '160 60% 45%' } // chart-2

// Edge colors
backgroundColor: 'hsl(0 62.8% 30.6%)' // destructive
stroke: 'hsl(340 75% 55%)' // chart-5
```

## Project Setup

### 1. Create Vite Project

```bash
npm create vite@latest my-swimlane -- --template react-ts
cd my-swimlane
npm install
npm install @xyflow/react
```

### 2. Required Files

**`src/index.css`**: Include design system color tokens
**`src/App.css`**: Layout styles for header, container, legend
**`src/App.tsx`**: Main component with swimlane implementation

### 3. Key CSS Classes

```css
.app-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: hsl(var(--background));
  color: hsl(var(--foreground));
}

.flow-container {
  flex: 1;
  position: relative;
}

.legend {
  padding: 1rem;
  background: hsl(var(--card));
  border-top: 1px solid hsl(var(--border));
}

.legend-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}
```

## Common Edge Types & Colors

| Type | Color | Style | Use Case |
|------|-------|-------|----------|
| **flow** | Muted gray | Solid | Normal sequential flow |
| **approval** | Red | Dashed | Request for approval |
| **gate** | Pink | Animated, thick | Approval granted |
| **delegation** | Green | Animated | Delegate to agent |
| **handoff** | Purple | Dashed | Hand off between agents |
| **spike** | Orange | Animated, thick dash | Fast-track shortcut |

## Common Node Patterns

### Human Approval Gate
```typescript
{
  backgroundColor: 'hsl(0 62.8% 30.6%)', // destructive
  borderColor: 'hsl(0 62.8% 50.6%)',
  borderStyle: 'double',
  borderWidth: '3px',
  borderRadius: '4px',
}
```

### Standard Phase
```typescript
{
  backgroundColor: `hsl(${swimlane.color})`,
  borderColor: `hsl(${swimlane.color})`,
  borderWidth: '2px',
  borderRadius: '8px',
  padding: '12px 16px',
}
```

### Special Fast-Track Node
```typescript
{
  backgroundColor: 'hsl(30 80% 35%)',
  borderColor: 'hsl(30 80% 55%)',
  borderWidth: '4px',
  borderRadius: '50%', // circular
  width: '140px',
  height: '140px',
}
```

## Performance Tips

1. **Wide Swimlane Bands**: Use `left: -10000, width: 20000` to ensure bands extend beyond viewport at all zoom levels
2. **Transform Transitions**: Use `transition: 'transform 0.05s ease-out'` for smooth panning
3. **Pointer Events**: Set `pointerEvents: 'none'` on overlay elements to allow interaction with nodes
4. **Z-Index Layers**:
   - Background bands: `zIndex: 0`
   - React Flow: default (1-9)
   - Sticky labels: `zIndex: 10`

## Spacing Guidelines

| Element | Value | Notes |
|---------|-------|-------|
| Swimlane height | 150px | Vertical space per lane |
| Horizontal phase spacing | 250px+ | Between phase nodes |
| Node min-width | 140px | Minimum node width |
| Node padding | 12px 16px | Internal padding |
| Label padding | 12px | Sticky label padding |

## Example Use Cases

### 1. SDLC Process Flow
- **Swimlanes**: Human, Main Agent, Domain Agent, IA Agent, UX Agent, Infra Agent, Deploy Agent
- **Phases**: SEED → RESEARCH → FEASIBILITY → EXPANSION → ANALYSIS → SELECTION → PRD → DESIGN → TEST → CODE → INFRA → DEPLOY → REFINE
- **Gates**: Go/No-Go, Tech Approval, PRD Approval, Model Approval, Design Approval

### 2. Multi-Agent Workflow
- **Swimlanes**: User, Orchestrator, Specialist Agent 1, Specialist Agent 2, Specialist Agent 3
- **Edges**: Delegation (to agents), Handoff (between agents), Return (back to orchestrator)

### 3. Cross-Functional Process
- **Swimlanes**: Sales, Engineering, Product, Legal, Finance
- **Phases**: Lead → Qualification → Scoping → Contract → Payment → Delivery

## Reference Implementation

**Full working example**: `/Users/andyhop/dev/lab/hmode/shared/design-system/visualizations/sdlc-swimlane-reactflow/`

Key files:
- `src/App.tsx` (lines 19-310): Complete implementation
- `src/index.css`: Design system tokens
- `src/App.css`: Layout styles

## Deployment

```bash
npm run build
# Output in dist/
# Deploy to S3, Amplify, or any static host
```

## Quick Start Checklist

- [ ] Install `@xyflow/react` in Vite React TypeScript project
- [ ] Define swimlanes with id, label, color (HSL), yOffset
- [ ] Define phases with id, number, name, swimlane, xOffset, description
- [ ] Implement viewport state tracking with `onMove`
- [ ] Create swimlane bands layer (zIndex: 0) with full transform
- [ ] Create sticky labels layer (zIndex: 10) with Y-only transform
- [ ] Use `createNodes()` and `createEdges()` functions for dynamic filtering
- [ ] Add mode toggle if needed (checkbox in header)
- [ ] Style nodes by type (human gates, standard phases, special nodes)
- [ ] Color edges by type (flow, approval, gate, delegation, handoff)
- [ ] Add legend showing swimlanes and edge types
- [ ] Test zoom, pan, and mode toggling

---

**Created**: 2026-01-27
**Last Updated**: 2026-01-27
**Skill Type**: Visualization Pattern
**Dependencies**: React, TypeScript, Vite, @xyflow/react v12+
