/**
 * Activity store - Zustand state management for activities
 */
import { create } from 'zustand';
import { Activity } from '../types';

interface ActivityState {
  activities: Activity[];
  isLoading: boolean;
  error: string | null;

  setActivities: (activities: Activity[]) => void;
  addActivity: (activity: Activity) => void;
  updateActivity: (activity: Activity) => void;
  removeActivity: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clear: () => void;
}

export const useActivityStore = create<ActivityState>((set) => ({
  activities: [],
  isLoading: false,
  error: null,

  setActivities: (activities) => set({ activities }),

  addActivity: (activity) =>
    set((state) => ({
      activities: [activity, ...state.activities],
    })),

  updateActivity: (activity) =>
    set((state) => ({
      activities: state.activities.map((a) =>
        a.id === activity.id ? activity : a
      ),
    })),

  removeActivity: (id) =>
    set((state) => ({
      activities: state.activities.filter((a) => a.id !== id),
    })),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  clear: () =>
    set({
      activities: [],
      isLoading: false,
      error: null,
    }),
}));
