/**
 * Activities service - API calls for activities
 */
import apiClient from './api';
import { Activity } from '../types';

export const activitiesService = {
  list: async (skip = 0, limit = 10, activityType?: string) => {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });
    if (activityType) {
      params.append('activity_type', activityType);
    }
    const response = await apiClient.get<Activity[]>(`/api/activities?${params}`);
    return response.data;
  },

  create: async (data: Partial<Activity>) => {
    const response = await apiClient.post<Activity>('/api/activities', data);
    return response.data;
  },

  get: async (id: string) => {
    const response = await apiClient.get<Activity>(`/api/activities/${id}`);
    return response.data;
  },

  update: async (id: string, data: Partial<Activity>) => {
    const response = await apiClient.put<Activity>(`/api/activities/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    await apiClient.delete(`/api/activities/${id}`);
  },

  getStats: async () => {
    const response = await apiClient.get('/api/activities/stats/summary');
    return response.data;
  },
};
