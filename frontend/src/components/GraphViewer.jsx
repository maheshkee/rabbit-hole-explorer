import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';

const GraphViewer = ({ nodes, edges, onNodesChange, onEdgesChange, onNodeClick }) => {
  return (
    <div style={{ width: '100%', height: '100%' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        fitView
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
};

export default GraphViewer;
