import React, { useCallback, useRef } from 'react';
import ReactFlow, { Background, Controls, MiniMap, useNodesState, useEdgesState, addEdge } from 'react-flow-renderer';
import { constants } from '../utils/constants';

const nodeTypes = {};

export default function WorkflowCanvas({ nodes: initialNodes, edges: initialEdges, onNodesChange, onEdgesChange, readonly = false }) {
  const [nodes, setNodes, onNodesChangeHandler] = useNodesState(initialNodes || []);
  const [edges, setEdges, onEdgesChangeHandler] = useEdgesState(initialEdges || []);
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = React.useState(null);

  React.useEffect(() => {
    if (initialNodes) setNodes(initialNodes);
  }, [initialNodes, setNodes]);

  React.useEffect(() => {
    if (initialEdges) setEdges(initialEdges);
  }, [initialEdges, setEdges]);

  const onConnect = useCallback((params) => {
    if (readonly) return;
    setEdges(eds => addEdge({ ...params, animated: true }, eds));
  }, [setEdges, readonly]);

  const onDrop = useCallback((event) => {
    if (readonly) return;
    event.preventDefault();
    const type = event.dataTransfer.getData('application/reactflow');
    if (!type || !reactFlowInstance) return;
    const position = reactFlowInstance.screenToFlowPosition({ x: event.clientX, y: event.clientY });
    const newNode = {
      id: `node_${Date.now()}`,
      type: 'default',
      position,
      data: {
        label: type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' '),
        type,
        color: constants.NODE_COLORS[type] || '#6b7280',
      },
    };
    setNodes(nds => nds.concat(newNode));
  }, [reactFlowInstance, readonly, setNodes]);

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  return (
    <div ref={reactFlowWrapper} className="w-full h-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange || onNodesChangeHandler}
        onEdgesChange={onEdgesChange || onEdgesChangeHandler}
        onConnect={onConnect}
        onInit={setReactFlowInstance}
        onDrop={onDrop}
        onDragOver={onDragOver}
        fitView
        attributionPosition="bottom-left"
        nodeTypes={nodeTypes}
      >
        <Background color="#334155" gap={16} />
        <Controls className="bg-slate-800" />
        <MiniMap
          nodeColor={(node) => node.data?.color || '#6b7280'}
          maskColor="rgba(15, 23, 42, 0.8)"
          className="bg-slate-800 border border-slate-700"
        />
      </ReactFlow>
    </div>
  );
}
