export const selectAllWorkflows = (state) => state.workflows.workflows;
export const selectCurrentWorkflow = (state) => state.workflows.currentWorkflow;
export const selectWorkflowById = (id) => (state) =>
  state.workflows.workflows.find(w => w.id === id);
export const selectAllExecutions = (state) => state.executions.executions;
export const selectCurrentExecution = (state) => state.executions.currentExecution;
export const selectMetrics = (state) => state.monitoring.metrics;
export const selectSummary = (state) => state.monitoring.summary;
