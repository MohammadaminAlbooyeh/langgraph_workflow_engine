import { useState, useEffect, useCallback } from 'react';
import { useDispatch } from 'react-redux';
import { agentApi } from '../services/agent_api';
import { setAgents } from '../store/actions/agentActions';

export function useAgents() {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);

  const fetchAgents = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await agentApi.list();
      dispatch(setAgents(data));
    } finally {
      setLoading(false);
    }
  }, [dispatch]);

  useEffect(() => { fetchAgents(); }, [fetchAgents]);
  return { fetchAgents, loading };
}
