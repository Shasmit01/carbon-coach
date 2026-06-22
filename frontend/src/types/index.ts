/**
 * Types for the application
 */

export interface User {
  id: string;
  email: string;
  full_name?: string;
  avatar_url?: string;
  bio?: string;
  role: 'user' | 'admin';
  is_active: boolean;
  email_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface Activity {
  id: string;
  user_id: string;
  activity_type: string;
  category?: string;
  description?: string;
  value: number;
  unit: string;
  carbon_emissions: number;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface EmissionFactor {
  id: string;
  category: string;
  subcategory: string;
  description?: string;
  factor_value: number;
  unit: string;
  source?: string;
  region?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Goal {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  target_reduction: number;
  baseline_emissions: number;
  target_emissions: number;
  unit: string;
  category?: string;
  status: 'active' | 'completed' | 'failed' | 'paused';
  start_date: string;
  deadline: string;
  actual_reduction: number;
  progress_percentage: number;
  created_at: string;
  updated_at: string;
}

export interface Reward {
  id: string;
  user_id: string;
  reward_type: string;
  title: string;
  description?: string;
  points: number;
  points_multiplier: number;
  icon_url?: string;
  badge_name?: string;
  criteria: Record<string, any>;
  unlocked_at?: string;
  created_at: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  user_message: string;
  ai_response: string;
  ai_model: string;
  response_time_ms?: number;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface DashboardData {
  total_emissions: number;
  today_emissions: number;
  this_month_emissions: number;
  this_year_emissions: number;
  active_goals: number;
  total_points: number;
  activities_count: number;
  last_activity_date?: string;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}
