import { useState, useEffect, useCallback } from 'react';
import { monitoringApi } from '../services/monitoring_api';

export function useMonitoring() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchSummary = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await monitoringApi.summary();
      setSummary(data);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchSummary(); }, [fetchSummary]);
  return { summary, loading, refetch: fetchSummary };
}
