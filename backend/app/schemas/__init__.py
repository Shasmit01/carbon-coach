"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# ==================== User Schemas ====================


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""

    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """User update schema"""

    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[dict] = None


class UserResponse(UserBase):
    """User response schema"""

    id: UUID
    avatar_url: Optional[str]
    role: str
    is_active: bool
    email_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Activity Schemas ====================


class ActivityBase(BaseModel):
    """Base activity schema"""

    activity_type: str = Field(..., description="transport, energy, food, waste, shopping")
    category: Optional[str] = None
    description: Optional[str] = None
    value: float = Field(..., gt=0, description="Numeric value (km, kWh, kg, etc)")
    unit: str = Field(..., description="Measurement unit")


class ActivityCreate(ActivityBase):
    """Activity creation schema"""

    pass


class ActivityUpdate(BaseModel):
    """Activity update schema"""

    category: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None


class ActivityResponse(ActivityBase):
    """Activity response schema"""

    id: UUID
    user_id: UUID
    carbon_emissions: float
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Emission Factor Schemas ====================


class EmissionFactorBase(BaseModel):
    """Base emission factor schema"""

    category: str
    subcategory: str
    description: Optional[str] = None
    factor_value: float = Field(..., ge=0, description="kg CO2 per unit")
    unit: str
    source: Optional[str] = None
    region: Optional[str] = "Global"


class EmissionFactorCreate(EmissionFactorBase):
    """Emission factor creation schema"""

    pass


class EmissionFactorUpdate(BaseModel):
    """Emission factor update schema"""

    factor_value: Optional[float] = None
    description: Optional[str] = None
    source: Optional[str] = None


class EmissionFactorResponse(EmissionFactorBase):
    """Emission factor response schema"""

    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Goal Schemas ====================


class GoalBase(BaseModel):
    """Base goal schema"""

    title: str
    description: Optional[str] = None
    target_reduction: float = Field(..., ge=0, le=100, description="Reduction percentage")
    baseline_emissions: float
    target_emissions: float
    category: Optional[str] = None
    deadline: datetime


class GoalCreate(GoalBase):
    """Goal creation schema"""

    pass


class GoalUpdate(BaseModel):
    """Goal update schema"""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class GoalResponse(GoalBase):
    """Goal response schema"""

    id: UUID
    user_id: UUID
    unit: str
    status: str
    start_date: datetime
    actual_reduction: float
    progress_percentage: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Reward Schemas ====================


class RewardBase(BaseModel):
    """Base reward schema"""

    reward_type: str
    title: str
    description: Optional[str] = None
    points: int = 0
    badge_name: Optional[str] = None


class RewardResponse(RewardBase):
    """Reward response schema"""

    id: UUID
    user_id: UUID
    points_multiplier: float
    icon_url: Optional[str]
    criteria: dict
    unlocked_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Chat Schemas ====================


class ChatMessage(BaseModel):
    """Chat message schema"""

    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    """Chat response schema"""

    id: UUID
    session_id: UUID
    user_message: str
    ai_response: str
    ai_model: str
    response_time_ms: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Chat history response schema"""

    total_messages: int
    messages: list[ChatResponse]


# ==================== Analytics Schemas ====================


class DailyEmissions(BaseModel):
    """Daily emissions data"""

    date: datetime
    emissions: float
    activity_count: int


class EmissionsTrendResponse(BaseModel):
    """Emissions trend response"""

    period: str  # daily, weekly, monthly, yearly
    data: list[DailyEmissions]
    total_emissions: float
    average_daily: float


class DashboardResponse(BaseModel):
    """Dashboard data response"""

    total_emissions: float
    today_emissions: float
    this_month_emissions: float
    this_year_emissions: float
    active_goals: int
    total_points: int
    activities_count: int
    last_activity_date: Optional[datetime]


class AnalyticsResponse(BaseModel):
    """Analytics response schema"""

    user_id: UUID
    total_emissions: float
    daily_average: float
    activity_count: int
    goals_progress: list[dict]
    top_emission_sources: list[dict]


# ==================== Admin Schemas ====================


class UserAdminResponse(UserResponse):
    """User response for admin"""

    last_login: Optional[datetime]


class AdminStatsResponse(BaseModel):
    """Admin statistics response"""

    total_users: int
    total_activities: int
    total_emissions: float
    average_user_emissions: float
    active_goals: int
    total_rewards_given: int


# ==================== Authentication Schemas ====================


class TokenResponse(BaseModel):
    """Token response schema"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    """JWT token payload"""

    sub: str
    email: str
    role: str
    exp: Optional[datetime] = None


# ==================== Health Check Schemas ====================


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    version: str
    environment: str
    database: str
    ollama: str
    timestamp: datetime
