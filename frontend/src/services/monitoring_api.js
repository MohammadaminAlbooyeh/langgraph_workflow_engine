import api from './api';

export const monitoringApi = {
  metrics: (type) => api.get('/monitoring/metrics', { params: { type } }),
  summary: () => api.get('/monitoring/summary'),
};
