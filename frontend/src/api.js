import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Recruitment APIs
export const candidateAPI = {
  getAll: () => api.get('/candidates/'),
  create: (data) => api.post('/candidates/', data),
  getById: (id) => api.get(`/candidates/${id}`),
};

export const positionAPI = {
  getAll: () => api.get('/positions/'),
  create: (data) => api.post('/positions/', data),
  getById: (id) => api.get(`/positions/${id}`),
};

export const applicationAPI = {
  getAll: () => api.get('/applications/'),
  create: (data) => api.post('/applications/', data),
  getById: (id) => api.get(`/applications/${id}`),
};

// Employee & Onboarding APIs
export const employeeAPI = {
  getAll: () => api.get('/employees/'),
  create: (data) => api.post('/employees/', data),
  getById: (id) => api.get(`/employees/${id}`),
};

export const onboardingAPI = {
  createChecklist: (employeeId, data) => 
    api.post(`/employees/${employeeId}/onboarding/checklist`, data),
  askQuestion: (employeeId, data) => 
    api.post(`/employees/${employeeId}/onboarding/query`, data),
  updateProgress: (employeeId, data) => 
    api.post(`/employees/${employeeId}/onboarding/progress`, data),
};

export default api;
