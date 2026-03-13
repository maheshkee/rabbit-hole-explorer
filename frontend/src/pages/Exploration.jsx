import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { getExplorationGraph, expandNode } from '../services/api';
import GraphViewer from '../components/GraphViewer';
import { useNodesState, useEdgesState } from 'reactflow';
import { getLayoutedElements } from '../utils/graphLayout';

const Exploration = () => {
  const { id } = useParams();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [topic, setTopic] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  const fetchGraph = useCallback(async () => {
    try {
      const data = await getExplorationGraph(id);
      setTopic(data.topic);

      // Convert backend nodes into React Flow nodes
      const initialNodes = data.nodes.map((node) => ({
        id: node.id.toString(),
        data: { label: node.title },
        position: { x: 0, y: 0 },
      }));

      // Convert backend edges into React Flow edges
      const rfEdges = data.edges.map((edge) => ({
        id: `${edge.source}-${edge.target}`,
        source: edge.source.toString(),
        target: edge.target.toString(),
        animated: true,
      }));

      // Calculate automatic layout using Dagre
      const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
        initialNodes,
        rfEdges,
        'TB'
      );

      setNodes(layoutedNodes);
      setEdges(layoutedEdges);
    } catch (error) {
      console.error('Error fetching exploration:', error);
    } finally {
      setIsLoading(false);
    }
  }, [id, setNodes, setEdges]);

  useEffect(() => {
    fetchGraph();
  }, [id]);

  const handleNodeClick = async (event, node) => {
    console.log('Node clicked:', node);
    try {
      setIsLoading(true);
      await expandNode(node.id);
      // Re-fetch the graph to show new nodes and edges
      await fetchGraph();
    } catch (error) {
      console.error('Error expanding node:', error);
      alert('Failed to expand node');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && nodes.length === 0) {
    return <div style={{ padding: '2rem' }}>Loading graph...</div>;
  }

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '1rem', background: '#f0f0f0', borderBottom: '1px solid #ccc', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ margin: 0 }}>Exploration: {topic}</h2>
        <button onClick={() => window.location.href = '/'}>Back to Home</button>
      </header>
      <div style={{ flex: 1, position: 'relative' }}>
        {isLoading && <div style={{ position: 'absolute', top: 10, right: 10, zIndex: 10, background: 'rgba(255,255,255,0.8)', padding: '5px' }}>Updating...</div>}
        <div style={{ width: '100%', height: '100%' }}>
          <GraphViewer 
            nodes={nodes} 
            edges={edges} 
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={handleNodeClick}
          />
        </div>
      </div>
    </div>
  );
};

export default Exploration;
