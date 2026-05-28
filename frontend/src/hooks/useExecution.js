import { useState, useCallback } from 'react';
import { useDispatch } from 'react-redux';
import { executionApi } from '../services/execution_api';
import { addExecution, updateExecution, setExecutions } from '../store/actions/executionActions';

export function useExecution() {
  const dispatch = useDispatch();
  const [loading, setLoadingState] = useState(false);

  const createExecution = useCallback(async (workflowId, inputs = {}) => {
    setLoadingState(true);
    try {
      const { data } = await executionApi.create({ workflow_id: workflowId, inputs });
      dispatch(addExecution(data));
      return data;
    } finally {
      setLoadingState(false);
    }
  }, [dispatch]);

  const startExecution = useCallback(async (executionId, nodes, edges) => {
    setLoadingState(true);
    try {
      const { data } = await executionApi.start(executionId, nodes, edges);
      dispatch(updateExecution(data));
      return data;
    } finally {
      setLoadingState(false);
    }
  }, [dispatch]);

  const cancelExecution = useCallback(async (executionId) => {
    const { data } = await executionApi.cancel(executionId);
    return data;
  }, []);

  return { createExecution, startExecution, cancelExecution, loading };
}
