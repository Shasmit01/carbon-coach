"""
Simplified database models for local SQLite development
"""
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(50), default="user", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime)
    preferences: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    activities = relationship("Activity", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    rewards = relationship("Reward", back_populates="user", cascade="all, delete-orphan")
    chat_histories = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class Activity(Base):
    """Activity model for tracking carbon-producing activities"""

    __tablename__ = "activities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    value: Mapped[float] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    carbon_emissions: Mapped[float] = mapped_column(default=0.0, nullable=False)
    data: Mapped[dict] = mapped_column(JSON, default={})
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="activities")

    def __repr__(self) -> str:
        return f"<Activity(id={self.id}, type={self.activity_type}, emissions={self.carbon_emissions})>"


class EmissionFactor(Base):
    """Emission factor model for conversion calculations"""

    __tablename__ = "emission_factors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    subcategory: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    factor_value: Mapped[float] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(255))
    region: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<EmissionFactor(category={self.category}, subcategory={self.subcategory})>"


class Goal(Base):
    """Goal model for tracking reduction targets"""

    __tablename__ = "goals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    target_reduction: Mapped[float] = mapped_column(nullable=False)
    baseline_emissions: Mapped[float] = mapped_column(nullable=False)
    target_emissions: Mapped[float] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(String(50), default="kg_CO2")
    category: Mapped[Optional[str]] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="active", index=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    actual_reduction: Mapped[float] = mapped_column(default=0.0)
    progress_percentage: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="goals")

    def __repr__(self) -> str:
        return f"<Goal(id={self.id}, title={self.title}, status={self.status})>"


class Reward(Base):
    """Reward model for achievements and points"""

    __tablename__ = "rewards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    reward_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    points: Mapped[int] = mapped_column(default=0)
    points_multiplier: Mapped[float] = mapped_column(default=1.0)
    icon_url: Mapped[Optional[str]] = mapped_column(Text)
    badge_name: Mapped[Optional[str]] = mapped_column(String(100))
    criteria: Mapped[dict] = mapped_column(JSON, default={})
    unlocked_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="rewards")

    def __repr__(self) -> str:
        return f"<Reward(id={self.id}, title={self.title}, points={self.points})>"


class ChatHistory(Base):
    """Chat history model for storing conversations with AI"""

    __tablename__ = "chat_histories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    message_index: Mapped[int] = mapped_column(nullable=False)
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    ai_response: Mapped[str] = mapped_column(Text, nullable=False)
    response_tokens: Mapped[Optional[int]] = mapped_column()
    ai_model: Mapped[str] = mapped_column(String(100), default="gemma:2b")
    response_time_ms: Mapped[Optional[int]] = mapped_column()
    helpful: Mapped[Optional[bool]] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="chat_histories")

    def __repr__(self) -> str:
        return f"<ChatHistory(id={self.id}, session={self.session_id})>"
