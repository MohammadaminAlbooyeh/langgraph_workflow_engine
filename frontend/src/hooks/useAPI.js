import { useState, useEffect } from 'react';
import api from '../services/api';

export function useAPI(endpoint, params = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    api.get(endpoint, { params })
      .then(res => { if (mounted) setData(res.data); })
      .catch(err => { if (mounted) setError(err.message); })
      .finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, [endpoint, JSON.stringify(params)]);

  return { data, loading, error, refetch: () => setLoading(true) };
}
