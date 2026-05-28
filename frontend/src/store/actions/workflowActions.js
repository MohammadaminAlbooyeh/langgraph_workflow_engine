export const setWorkflows = (workflows) => ({ type: 'SET_WORKFLOWS', payload: workflows });
export const setCurrentWorkflow = (workflow) => ({ type: 'SET_CURRENT_WORKFLOW', payload: workflow });
export const addWorkflow = (workflow) => ({ type: 'ADD_WORKFLOW', payload: workflow });
export const updateWorkflow = (workflow) => ({ type: 'UPDATE_WORKFLOW', payload: workflow });
export const deleteWorkflow = (id) => ({ type: 'DELETE_WORKFLOW', payload: id });
export const setLoading = (loading) => ({ type: 'SET_LOADING', payload: loading });
export const setError = (error) => ({ type: 'SET_ERROR', payload: error });
