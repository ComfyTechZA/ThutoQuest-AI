import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 10000;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    if (import.meta.env.VITE_DEBUG_MODE) {
      console.log('📤 API Request:', config.method.toUpperCase(), config.url);
    }
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    if (import.meta.env.VITE_DEBUG_MODE) {
      console.log('📥 API Response:', response.status, response.data);
    }
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('❌ Response Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('❌ Network Error: No response received');
    } else {
      console.error('❌ Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Career Prediction Service
export const careerService = {
  predictCareer: (studentData) =>
    apiClient.post('/predict-career', studentData),
  getCareerHistory: (studentId) =>
    apiClient.get(`/predict-career/${studentId}`),
};

// Quest Service
export const questService = {
  generateQuest: (studentData) =>
    apiClient.post('/generate-quest', studentData),
  getStudentQuests: (studentId, limit = 20, offset = 0) =>
    apiClient.get(`/quests/${studentId}`, {
      params: { limit, offset },
    }),
  completeQuest: (questId) =>
    apiClient.post(`/quests/${questId}/complete`),
};

// Health Check
export const healthService = {
  check: () => apiClient.get('/health'),
};

export default apiClient;
