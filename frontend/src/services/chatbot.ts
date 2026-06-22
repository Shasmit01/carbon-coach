/**
 * Chatbot service - API calls for AI chatbot
 */
import apiClient from './api';
import { ChatMessage } from '../types';

export const chatbotService = {
  sendMessage: async (message: string, sessionId?: string) => {
    const params = sessionId ? `?session_id=${sessionId}` : '';
    const response = await apiClient.post<ChatMessage>(
      `/api/chatbot/chat${params}`,
      { message }
    );
    return response.data;
  },

  getHistory: async (sessionId: string) => {
    const response = await apiClient.get(`/api/chatbot/history/${sessionId}`);
    return response.data;
  },

  clearHistory: async (sessionId: string) => {
    await apiClient.delete(`/api/chatbot/history/${sessionId}`);
  },

  checkStatus: async () => {
    const response = await apiClient.get('/api/chatbot/status');
    return response.data;
  },
};
