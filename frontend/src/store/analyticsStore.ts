/**
 * Analytics store - Zustand state management for analytics
 */
import { create } from 'zustand';
import { DashboardData } from '../types';

interface AnalyticsState {
  dashboardData: DashboardData | null;
  emissionsSummary: any[];
  emissionsTrends: any;
  goalsProgress: any[];
  isLoading: boolean;
  error: string | null;

  setDashboardData: (data: DashboardData) => void;
  setEmissionsSummary: (data: any[]) => void;
  setEmissionsTrends: (data: any) => void;
  setGoalsProgress: (data: any[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clear: () => void;
}

export const useAnalyticsStore = create<AnalyticsState>((set) => ({
  dashboardData: null,
  emissionsSummary: [],
  emissionsTrends: null,
  goalsProgress: [],
  isLoading: false,
  error: null,

  setDashboardData: (data) => set({ dashboardData: data }),

  setEmissionsSummary: (data) => set({ emissionsSummary: data }),

  setEmissionsTrends: (data) => set({ emissionsTrends: data }),

  setGoalsProgress: (data) => set({ goalsProgress: data }),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  clear: () =>
    set({
      dashboardData: null,
      emissionsSummary: [],
      emissionsTrends: null,
      goalsProgress: [],
      isLoading: false,
      error: null,
    }),
}));
