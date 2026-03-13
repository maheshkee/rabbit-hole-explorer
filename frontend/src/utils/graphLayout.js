import dagre from 'dagre';

const nodeWidth = 172;
const nodeHeight = 36;

/**
 * Calculates a hierarchical layout for a graph using Dagre.
 * @param {Array} nodes - React Flow nodes
 * @param {Array} edges - React Flow edges
 * @param {string} direction - Layout direction ('TB' for Top-to-Bottom, 'LR' for Left-to-Right)
 * @returns {Object} - Object containing nodes with calculated positions and the original edges
 */
export const getLayoutedElements = (nodes, edges, direction = 'TB') => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  dagreGraph.setGraph({ 
    rankdir: direction,
    nodesep: 50,
    ranksep: 100,
    marginx: 50,
    marginy: 50
  });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const layoutedNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    
    return {
      ...node,
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
      // Ensure source/target positions are set correctly for the layout direction
      targetPosition: direction === 'TB' ? 'top' : 'left',
      sourcePosition: direction === 'TB' ? 'bottom' : 'right',
    };
  });

  return { nodes: layoutedNodes, edges };
};
