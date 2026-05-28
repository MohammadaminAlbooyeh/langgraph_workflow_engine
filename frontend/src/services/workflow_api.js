import api from './api';

export const workflowApi = {
  list: (params) => api.get('/workflows', { params }),
  get: (id) => api.get(`/workflows/${id}`),
  create: (data) => api.post('/workflows', data),
  update: (id, data) => api.put(`/workflows/${id}`, data),
  delete: (id) => api.delete(`/workflows/${id}`),
  addNode: (id, node) => api.post(`/workflows/${id}/nodes`, node),
  addEdge: (id, edge) => api.post(`/workflows/${id}/edges`, edge),
  updateStatus: (id, status) => api.patch(`/workflows/${id}/status`, { status }),
};
