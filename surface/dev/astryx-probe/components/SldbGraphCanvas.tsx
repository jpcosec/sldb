import '@xyflow/react/dist/style.css';
import './SldbGraphCanvas.css';
import {Background, Controls, ReactFlow, type Edge, type Node} from '@xyflow/react';

export interface SldbGraphCanvasProps {
  /** Nodes to draw. Defaults to a single demonstration node. */
  nodes?: Node[];
  /** Edges to draw. */
  edges?: Edge[];
  /** Called with the id of the node the user selects. */
  onSelect?: (id: string | null) => void;
}

const DEFAULT_NODES: Node[] = [
  {id: 'class-1', position: {x: 40, y: 40}, data: {label: 'Class: Document'}},
];

/** A React Flow canvas that takes every color from Astryx tokens. */
export function SldbGraphCanvas({
  nodes = DEFAULT_NODES,
  edges = [],
  onSelect,
}: SldbGraphCanvasProps) {
  return (
    <div className="sldb-graph" data-testid="sldb-graph" style={{height: '100%', minHeight: 240}}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        proOptions={{hideAttribution: true}}
        onNodeClick={(_, node) => onSelect?.(node.id)}
        onPaneClick={() => onSelect?.(null)}
      >
        <Background />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}
