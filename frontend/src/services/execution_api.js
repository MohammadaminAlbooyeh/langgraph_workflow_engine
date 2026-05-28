import api from './api';

export const executionApi = {
  list: (params) => api.get('/executions', { params }),
  get: (id) => api.get(`/executions/${id}`),
  create: (data) => api.post('/executions', data),
  start: (id, nodes, edges) => api.post(`/executions/${id}/start`, { nodes, edges }),
  cancel: (id) => api.post(`/executions/${id}/cancel`),
  pause: (id) => api.post(`/executions/${id}/pause`),
  resume: (id) => api.post(`/executions/${id}/resume`),
};
