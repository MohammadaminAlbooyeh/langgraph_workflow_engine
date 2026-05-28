export const handleDragStart = (event, nodeType) => {
  event.dataTransfer.setData('application/reactflow', nodeType);
  event.dataTransfer.effectAllowed = 'move';
};

export const handleDragOver = (event) => {
  event.preventDefault();
  event.dataTransfer.dropEffect = 'move';
};

export const handleDrop = (event, position, addNode) => {
  event.preventDefault();
  const type = event.dataTransfer.getData('application/reactflow');
  if (!type) return;
  const newNode = {
    id: `node_${Date.now()}`,
    type,
    position,
    data: { label: type.charAt(0).toUpperCase() + type.slice(1) },
  };
  addNode(newNode);
};
