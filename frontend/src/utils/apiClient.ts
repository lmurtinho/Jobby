import axios, { AxiosInstance, AxiosResponse } from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';

// API configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add authentication token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('authToken');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    
    if (error.response?.status === 403) {
      // Forbidden - user doesn't have permission
      console.error('Access forbidden');
    }
    
    if (error.response?.status >= 500) {
      // Server error
      console.error('Server error:', error.response.data);
    }
    
    return Promise.reject(error);
  }
);

// API endpoint functions
export const authAPI = {
  login: (credentials: { email: string; password: string }) =>
    apiClient.post('/api/v1/auth/login', credentials),
  
  register: (userData: { 
    name: string; 
    email: string; 
    password: string;
  }) =>
    apiClient.post('/api/v1/auth/register', userData),
  
  logout: () =>
    apiClient.post('/api/v1/auth/logout'),
  
  refreshToken: () =>
    apiClient.post('/api/v1/auth/refresh'),
  
  getProfile: () =>
    apiClient.get('/api/v1/auth/profile'),
};

export const jobsAPI = {
  getJobs: (params?: { 
    search?: string; 
    skills?: string[]; 
    location?: string; 
    remote?: boolean;
    page?: number;
    limit?: number;
  }) =>
    apiClient.get('/api/v1/jobs', { params }),
  
  getJobById: (id: string) =>
    apiClient.get(`/api/v1/jobs/${id}`),
  
  saveJob: (jobId: string) =>
    apiClient.post(`/api/v1/jobs/${jobId}/save`),
  
  unsaveJob: (jobId: string) =>
    apiClient.delete(`/api/v1/jobs/${jobId}/save`),
  
  getSavedJobs: () =>
    apiClient.get('/api/v1/jobs/saved'),
  
  getJobMatches: (userId: string) =>
    apiClient.get(`/api/v1/users/${userId}/job-matches`),
};

export const userAPI = {
  uploadResume: (file: File) => {
    const formData = new FormData();
    formData.append('resume', file);
    
    return apiClient.post('/api/v1/users/resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  updateProfile: (profileData: {
    firstName?: string;
    lastName?: string;
    location?: string;
    skills?: string[];
    experienceLevel?: string;
  }) =>
    apiClient.put('/api/v1/users/profile', profileData),
  
  getSkillAnalysis: (targetJobIds: string[]) =>
    apiClient.post('/api/v1/users/skill-analysis', { target_job_ids: targetJobIds }),
  
  calculateMatches: () =>
    apiClient.post('/api/v1/users/calculate-matches'),
};

// Health check endpoint
export const healthAPI = {
  check: () =>
    apiClient.get('/health'),
};

// Utility functions
export const setAuthToken = (token: string) => {
  localStorage.setItem('authToken', token);
};

export const clearAuthToken = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
};

export const getAuthToken = (): string | null => {
  return localStorage.getItem('authToken');
};

// Export the configured axios instance as default
export default apiClient;
