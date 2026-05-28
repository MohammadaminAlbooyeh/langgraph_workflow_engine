import api from './api';

export const toolApi = {
  list: () => api.get('/tools'),
  execute: (name, params) => api.post('/tools/execute', { name, params }),
  register: (name, description, parameters) =>
    api.post('/tools/register', { name, description, parameters }),
};
