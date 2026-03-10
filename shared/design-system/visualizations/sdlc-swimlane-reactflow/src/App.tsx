// File UUID: 4e78be4b-ea6f-4510-9bfc-b6cd3845c897

import { useCallback, useEffect, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  type Node,
  type Edge,
  MarkerType,
  useReactFlow,
  ReactFlowProvider,
  BackgroundVariant,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import './App.css';

// Swimlane definitions using design system chart colors
const swimlanes = [
  { id: 'human', label: 'Human', color: '220 70% 50%', yOffset: 0 }, // chart-1 (blue)
  { id: 'main', label: 'Main Claude Agent', color: '160 60% 45%', yOffset: 150 }, // chart-2 (green)
  { id: 'domain', label: 'Domain Modeling Agent', color: '280 65% 60%', yOffset: 300 }, // chart-4 (purple)
  { id: 'ia', label: 'Info Architecture Agent', color: '30 80% 55%', yOffset: 450 }, // chart-3 (orange)
  { id: 'ux', label: 'UX Composition Agent', color: '340 75% 55%', yOffset: 600 }, // chart-5 (pink)
  { id: 'infra', label: 'Infrastructure/SRE Agent', color: '160 60% 45%', yOffset: 750 }, // chart-2 (green)
  { id: 'amplify', label: 'Amplify Deploy Agent', color: '30 80% 55%', yOffset: 900 }, // chart-3 (orange)
];

// Phase definitions
const phases = [
  { id: '1', number: '1.0', name: 'SEED', swimlane: 'main', description: 'Capture idea', xOffset: 0, spikeVisible: true },
  { id: '2', number: '2.0', name: 'RESEARCH', swimlane: 'main', description: 'Persona & intent', xOffset: 250, spikeVisible: false },
  { id: '2.5', number: '2.5', name: 'FEASIBILITY', swimlane: 'main', description: 'Go/no-go (prod only)', xOffset: 500, spikeVisible: false },
  { id: 'h2.5', number: 'H', name: 'Go/No-Go', swimlane: 'human', description: 'Human approval gate', xOffset: 550, spikeVisible: false },
  { id: '3', number: '3.0', name: 'EXPANSION', swimlane: 'main', description: 'Explore solutions', xOffset: 750, spikeVisible: false },
  { id: '4', number: '4.0', name: 'ANALYSIS', swimlane: 'main', description: 'Compare options', xOffset: 1000, spikeVisible: false },
  { id: '5', number: '5.0', name: 'SELECTION', swimlane: 'main', description: 'Choose approach', xOffset: 1250, spikeVisible: false },
  { id: 'h5', number: 'H', name: 'Tech Approval', swimlane: 'human', description: 'Approve tech stack', xOffset: 1400, spikeVisible: false },
  { id: '5.5', number: '5.5', name: 'PRD', swimlane: 'main', description: 'Requirements (prod only)', xOffset: 1550, spikeVisible: false },
  { id: 'h5.5', number: 'H', name: 'PRD Approval', swimlane: 'human', description: 'Requirements sign-off', xOffset: 1700, spikeVisible: false },
  { id: '6.1', number: '6.1', name: 'Domain Models', swimlane: 'domain', description: 'Define data structures', xOffset: 1850, spikeVisible: false },
  { id: 'h6.1', number: 'H', name: 'Model Approval', swimlane: 'human', description: 'Approve domain models', xOffset: 2000, spikeVisible: false },
  { id: '6.2', number: '6.2', name: 'Info Arch', swimlane: 'ia', description: 'Navigation & flows', xOffset: 2150, spikeVisible: false },
  { id: '6.3', number: '6.3', name: 'UX Design', swimlane: 'ux', description: 'Mockups & components', xOffset: 2300, spikeVisible: false },
  { id: 'h6.3', number: 'H', name: 'Design Approval', swimlane: 'human', description: 'Approve UX design', xOffset: 2450, spikeVisible: false },
  { id: '7', number: '7.0', name: 'TEST', swimlane: 'main', description: 'Write tests first', xOffset: 2600, spikeVisible: false },
  { id: '8.1', number: '8.1', name: 'Code', swimlane: 'main', description: 'Write implementation', xOffset: 2850, spikeVisible: true },
  { id: '8.2', number: '8.2', name: 'Infrastructure', swimlane: 'infra', description: 'CDK/Terraform', xOffset: 3100, spikeVisible: true },
  { id: '8.3', number: '8.3', name: 'Deploy', swimlane: 'amplify', description: 'Amplify/publish', xOffset: 3350, spikeVisible: true },
  { id: '9', number: '9.0', name: 'REFINE', swimlane: 'main', description: 'Polish & iterate', xOffset: 3600, spikeVisible: true },
];

// Function to create nodes based on mode
const createNodes = (spikeMode: boolean): Node[] => {
  return phases
    .filter(phase => spikeMode ? phase.spikeVisible : true)
    .map((phase) => {
      const swimlane = swimlanes.find((s) => s.id === phase.swimlane)!;
      const isHumanGate = phase.swimlane === 'human';

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
          backgroundColor: isHumanGate ? 'hsl(0 62.8% 30.6%)' : `hsl(${swimlane.color})`,
          borderColor: isHumanGate ? 'hsl(0 62.8% 50.6%)' : `hsl(${swimlane.color})`,
          color: 'hsl(0 0% 98%)',
          padding: '12px 16px',
          borderRadius: isHumanGate ? '4px' : '8px',
          borderWidth: isHumanGate ? '3px' : '2px',
          minWidth: '140px',
          fontSize: '0.875rem',
          fontWeight: 600,
          borderStyle: isHumanGate ? 'double' : 'solid',
        },
      };
    });
};

// Define edges
const edgeDefinitions = [
  // Standard SDLC path
  { source: '1', target: '2', label: 'Next', type: 'flow', spikeVisible: false },
  { source: '2', target: '2.5', label: 'Persona confirmed', type: 'flow', spikeVisible: false },
  { source: '2.5', target: 'h2.5', label: 'Request approval', type: 'approval', spikeVisible: false },
  { source: 'h2.5', target: '3', label: 'Go decision', type: 'gate', spikeVisible: false },
  { source: '3', target: '4', label: 'Next', type: 'flow', spikeVisible: false },
  { source: '4', target: '5', label: 'Next', type: 'flow', spikeVisible: false },
  { source: '5', target: 'h5', label: 'Request tech approval', type: 'approval', spikeVisible: false },
  { source: 'h5', target: '5.5', label: 'Tech approved', type: 'gate', spikeVisible: false },
  { source: '5.5', target: 'h5.5', label: 'Request PRD approval', type: 'approval', spikeVisible: false },
  { source: 'h5.5', target: '6.1', label: 'PRD approved', type: 'gate', spikeVisible: false },
  { source: '6.1', target: 'h6.1', label: 'Request model approval', type: 'approval', spikeVisible: false },
  { source: 'h6.1', target: '6.2', label: 'Models approved', type: 'gate', spikeVisible: false },
  { source: '6.2', target: '6.3', label: 'IA spec', type: 'handoff', spikeVisible: false },
  { source: '6.3', target: 'h6.3', label: 'Request design approval', type: 'approval', spikeVisible: false },
  { source: 'h6.3', target: '7', label: 'Design approved', type: 'gate', spikeVisible: false },
  { source: '7', target: '8.1', label: 'Begin coding', type: 'flow', spikeVisible: false },
  { source: '8.1', target: '8.2', label: 'Need infra', type: 'delegation', spikeVisible: true },
  { source: '8.2', target: '8.3', label: 'Infra ready', type: 'handoff', spikeVisible: true },
  { source: '8.3', target: '9', label: 'Deployed', type: 'return', spikeVisible: true },

  // SPIKE path (bypass phases 2-7)
  { source: '1', target: '8.1', label: 'SPIKE: Skip to code (max 3 days)', type: 'spike', spikeVisible: true },
];

// Function to create edges based on mode
const createEdges = (spikeMode: boolean): Edge[] => {
  return edgeDefinitions
    .filter(edge => {
      if (spikeMode) {
        // In spike mode: show only edges marked as visible in spike mode
        return edge.spikeVisible;
      } else {
        // In full SDLC mode: show all edges EXCEPT the spike shortcut
        return edge.type !== 'spike';
      }
    })
    .map((edge, idx) => {
      let color = '240 5% 64.9%'; // muted
      let strokeDasharray: string | undefined;
      let animated = false;
      let strokeWidth = 2;

      if (edge.type === 'gate') {
        color = '340 75% 55%'; // chart-5 (pink) - gate approval from human
        strokeWidth = 3;
        animated = true;
      } else if (edge.type === 'approval') {
        color = '0 62.8% 50.6%'; // destructive (red) - requesting human approval
        strokeDasharray = '5 5';
        strokeWidth = 2;
      } else if (edge.type === 'delegation') {
        color = '160 60% 45%'; // chart-2 (green) - delegation to agent
        animated = true;
      } else if (edge.type === 'return' || edge.type === 'handoff') {
        color = '280 65% 60%'; // chart-4 (purple) - handoff between agents
        strokeDasharray = '5 5';
      } else if (edge.type === 'spike') {
        color = '30 80% 55%'; // chart-3 (orange) - SPIKE fast-track path
        strokeWidth = 4;
        animated = true;
        strokeDasharray = '10 5';
      }

      return {
        id: `edge-${idx}`,
        source: edge.source,
        target: edge.target,
        label: edge.label,
        type: 'smoothstep',
        animated,
        style: {
          stroke: `hsl(${color})`,
          strokeWidth,
          strokeDasharray,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: `hsl(${color})`,
        },
      };
    });
};

function FlowCanvas({ spikeMode }: { spikeMode: boolean }) {
  const reactFlowInstance = useReactFlow();
  const nodes = createNodes(spikeMode);
  const edges = createEdges(spikeMode);
  const [viewport, setViewport] = useState({ x: 0, y: 0, zoom: 0.5 });

  useEffect(() => {
    setTimeout(() => {
      reactFlowInstance.fitView({ padding: 0.1, duration: 800 });
    }, 100);
  }, [reactFlowInstance, spikeMode]);

  const onNodeClick = useCallback((_event: React.MouseEvent, node: Node) => {
    const description = node.data.description || 'No description';
    alert(`Phase ${node.id}\n\n${description}`);
  }, []);

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {/* Swimlane bands */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          pointerEvents: 'none',
          zIndex: 0,
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
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
                right: -10000,
                top: lane.yOffset,
                width: 20000,
                height: 150,
                backgroundColor: `hsla(${lane.color} / 0.1)`,
                borderBottom: `1px solid hsla(${lane.color} / 0.3)`,
              }}
            />
          ))}
        </div>
      </div>

      {/* Sticky swimlane labels */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          pointerEvents: 'none',
          zIndex: 10,
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
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
              <div
                style={{
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  color: `hsl(${lane.color})`,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  whiteSpace: 'nowrap',
                }}
              >
                {lane.label}
              </div>
            </div>
          ))}
        </div>
      </div>

      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodeClick={onNodeClick}
        onMove={(_event, viewport) => setViewport(viewport)}
        fitView
        minZoom={0.2}
        maxZoom={1.5}
        defaultViewport={{ x: 0, y: 0, zoom: 0.5 }}
      >
        <Background color="hsl(240 3.7% 15.9%)" gap={16} variant={BackgroundVariant.Dots} />
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            const bgColor = node.style?.backgroundColor as string;
            return bgColor || 'hsl(160 60% 45%)';
          }}
          maskColor="rgba(0, 0, 0, 0.2)"
        />
      </ReactFlow>
    </div>
  );
}

function App() {
  const [spikeMode, setSpikeMode] = useState(false);

  return (
    <div className="app-container">
      <header>
        <h1>SDLC Swimlane Diagram</h1>
        <p className="subtitle">Interactive React Flow - Agent & Human Handoffs</p>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          justifyContent: 'center',
          marginBottom: '0.5rem'
        }}>
          <label style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            cursor: 'pointer',
            fontSize: '0.875rem',
            fontWeight: 500
          }}>
            <input
              type="checkbox"
              checked={spikeMode}
              onChange={(e) => setSpikeMode(e.target.checked)}
              style={{
                width: '1.25rem',
                height: '1.25rem',
                cursor: 'pointer',
                accentColor: 'hsl(30 80% 55%)'
              }}
            />
            <span style={{ color: spikeMode ? 'hsl(30 80% 55%)' : 'hsl(var(--foreground))' }}>
              SPIKE Mode (Skip phases 2-7, max 3 days)
            </span>
          </label>
        </div>
        <p className="instructions">
          Scroll to zoom • Drag to pan • Click nodes for details
        </p>
      </header>

      <div className="flow-container">
        <ReactFlowProvider>
          <FlowCanvas spikeMode={spikeMode} />
        </ReactFlowProvider>
      </div>

      <div className="legend">
        <h2>Swimlanes</h2>
        <div className="legend-grid">
          {swimlanes.map((lane) => (
            <div key={lane.id} className="legend-item">
              <div
                className="legend-color"
                style={{ backgroundColor: `hsl(${lane.color})` }}
              />
              <span className="legend-text">{lane.label}</span>
            </div>
          ))}
        </div>

        <h2 style={{ marginTop: '1.5rem' }}>Edge Types</h2>
        <div className="legend-grid">
          <div className="legend-item">
            <div
              className="legend-color"
              style={{ backgroundColor: 'hsl(240 5% 64.9%)', width: '30px' }}
            />
            <span className="legend-text">Normal flow</span>
          </div>
          <div className="legend-item">
            <div
              className="legend-color"
              style={{ backgroundColor: 'hsl(0 62.8% 50.6%)', width: '30px' }}
            />
            <span className="legend-text">Request approval (dashed)</span>
          </div>
          <div className="legend-item">
            <div
              className="legend-color"
              style={{ backgroundColor: 'hsl(340 75% 55%)', width: '30px' }}
            />
            <span className="legend-text">Gate approval (animated)</span>
          </div>
          <div className="legend-item">
            <div
              className="legend-color"
              style={{ backgroundColor: 'hsl(160 60% 45%)', width: '30px' }}
            />
            <span className="legend-text">Delegation (animated)</span>
          </div>
          <div className="legend-item">
            <div
              className="legend-color"
              style={{ backgroundColor: 'hsl(280 65% 60%)', width: '30px' }}
            />
            <span className="legend-text">Handoff (dashed)</span>
          </div>
          {spikeMode && (
            <div className="legend-item">
              <div
                className="legend-color"
                style={{ backgroundColor: 'hsl(30 80% 55%)', width: '30px' }}
              />
              <span className="legend-text">SPIKE fast-track (animated, thick)</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
