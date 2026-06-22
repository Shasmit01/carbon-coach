/**
 * Analytics service - API calls for analytics and dashboard
 */
import apiClient from './api';
import { DashboardData } from '../types';

export const analyticsService = {
  getDashboard: async () => {
    const response = await apiClient.get<DashboardData>('/api/analytics/dashboard');
    return response.data;
  },

  getEmissionsSummary: async () => {
    const response = await apiClient.get('/api/analytics/emissions/summary');
    return response.data;
  },

  getEmissionsTrends: async (period = 'monthly') => {
    const response = await apiClient.get(`/api/analytics/emissions/trends?period=${period}`);
    return response.data;
  },

  getGoalsProgress: async () => {
    const response = await apiClient.get('/api/analytics/goals/progress');
    return response.data;
  },
};
