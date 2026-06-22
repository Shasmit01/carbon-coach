/**
 * Chat store - Zustand state management for chatbot
 */
import { create } from 'zustand';
import { ChatMessage } from '../types';

interface ChatState {
  sessionId: string | null;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;

  setSessionId: (sessionId: string) => void;
  setMessages: (messages: ChatMessage[]) => void;
  addMessage: (message: ChatMessage) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clear: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  sessionId: null,
  messages: [],
  isLoading: false,
  error: null,

  setSessionId: (sessionId) => set({ sessionId }),

  setMessages: (messages) => set({ messages }),

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  clear: () =>
    set({
      sessionId: null,
      messages: [],
      isLoading: false,
      error: null,
    }),
}));
