/**
 * Auth service - API calls for authentication
 */
import apiClient from './api';
import { AuthTokens, User } from '../types';

export const authService = {
  register: async (email: string, password: string, fullName: string) => {
    const response = await apiClient.post<AuthTokens>('/api/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const response = await apiClient.post<AuthTokens>('/api/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  getCurrentUser: async () => {
    const response = await apiClient.get<User>('/api/auth/me');
    return response.data;
  },

  refreshToken: async (refreshToken: string) => {
    const response = await apiClient.post<AuthTokens>('/api/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },
};
