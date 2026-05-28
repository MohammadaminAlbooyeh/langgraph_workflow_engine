export const validateWorkflow = (nodes, edges) => {
  const errors = [];
  if (!nodes?.length) errors.push('Workflow must have at least one node');
  edges?.forEach((edge, i) => {
    if (!nodes.find(n => n.id === edge.source)) errors.push(`Edge ${i}: source not found`);
    if (!nodes.find(n => n.id === edge.target)) errors.push(`Edge ${i}: target not found`);
  });
  return errors;
};

export const validateNodeConfig = (config) => {
  const errors = [];
  if (config?.temperature != null && (config.temperature < 0 || config.temperature > 2)) {
    errors.push('Temperature must be between 0 and 2');
  }
  if (config?.maxTokens != null && config.maxTokens < 1) {
    errors.push('maxTokens must be positive');
  }
  return errors;
};
