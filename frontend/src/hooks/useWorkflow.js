import { useState, useEffect, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { workflowApi } from '../services/workflow_api';
import { setWorkflows, setCurrentWorkflow, addWorkflow, updateWorkflow, deleteWorkflow, setLoading, setError } from '../store/actions/workflowActions';
import { selectAllWorkflows, selectCurrentWorkflow, selectAllExecutions } from '../store/selectors/workflowSelectors';

export function useWorkflows() {
  const dispatch = useDispatch();
  const workflows = useSelector(selectAllWorkflows);
  const currentWorkflow = useSelector(selectCurrentWorkflow);

  const fetchWorkflows = useCallback(async () => {
    dispatch(setLoading(true));
    try {
      const { data } = await workflowApi.list();
      dispatch(setWorkflows(data));
    } catch (err) {
      dispatch(setError(err.message));
    }
  }, [dispatch]);

  const fetchWorkflow = useCallback(async (id) => {
    try {
      const { data } = await workflowApi.get(id);
      dispatch(setCurrentWorkflow(data));
      return data;
    } catch (err) {
      dispatch(setError(err.message));
    }
  }, [dispatch]);

  const createWorkflow = useCallback(async (workflowData) => {
    try {
      const { data } = await workflowApi.create(workflowData);
      dispatch(addWorkflow(data));
      return data;
    } catch (err) {
      dispatch(setError(err.message));
    }
  }, [dispatch]);

  const editWorkflow = useCallback(async (id, workflowData) => {
    try {
      const { data } = await workflowApi.update(id, workflowData);
      dispatch(updateWorkflow(data));
      return data;
    } catch (err) {
      dispatch(setError(err.message));
    }
  }, [dispatch]);

  const removeWorkflow = useCallback(async (id) => {
    try {
      await workflowApi.delete(id);
      dispatch(deleteWorkflow(id));
    } catch (err) {
      dispatch(setError(err.message));
    }
  }, [dispatch]);

  useEffect(() => { fetchWorkflows(); }, [fetchWorkflows]);

  return { workflows, currentWorkflow, fetchWorkflows, fetchWorkflow, createWorkflow, editWorkflow, removeWorkflow };
}
