"""
Services for business logic
"""
from decimal import Decimal
from typing import Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Activity, EmissionFactor, User


class EmissionCalculator:
    """Service for calculating carbon emissions"""

    @staticmethod
    async def calculate_emissions(
        db: AsyncSession,
        activity_type: str,
        category: Optional[str],
        value: float,
        unit: str,
    ) -> float:
        """
        Calculate carbon emissions for an activity

        Args:
            db: Database session
            activity_type: Type of activity
            category: Activity category/subcategory
            value: Numeric value
            unit: Unit of measurement

        Returns:
            Carbon emissions in kg CO2
        """
        # Query emission factor
        query = select(EmissionFactor).where(
            and_(
                EmissionFactor.category == activity_type,
                EmissionFactor.subcategory == (category or activity_type),
                EmissionFactor.is_active == True,
            )
        )

        result = await db.execute(query)
        factor = result.scalar_one_or_none()

        if not factor:
            # Default factor if not found
            return float(value) * 0.1

        # Calculate emissions: value * factor_value
        emissions = float(value) * float(factor.factor_value)
        return round(emissions, 4)

    @staticmethod
    async def get_daily_emissions(db: AsyncSession, user_id: str) -> float:
        """Get today's total emissions for a user"""
        from datetime import date

        query = select(func.sum(Activity.carbon_emissions)).where(
            and_(
                Activity.user_id == user_id,
                func.date(Activity.created_at) == date.today(),
            )
        )

        result = await db.execute(query)
        total = result.scalar()
        return float(total) if total else 0.0

    @staticmethod
    async def get_monthly_emissions(db: AsyncSession, user_id: str) -> float:
        """Get this month's total emissions for a user"""
        from datetime import date

        today = date.today()
        first_day = date(today.year, today.month, 1)

        query = select(func.sum(Activity.carbon_emissions)).where(
            and_(
                Activity.user_id == user_id,
                func.date(Activity.created_at) >= first_day,
            )
        )

        result = await db.execute(query)
        total = result.scalar()
        return float(total) if total else 0.0


class UserService:
    """Service for user operations"""

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        """Get user by ID"""
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_last_login(db: AsyncSession, user_id: str) -> None:
        """Update user's last login timestamp"""
        from datetime import datetime

        user = await UserService.get_user_by_id(db, user_id)
        if user:
            user.last_login = datetime.now()
            await db.commit()


class RewardService:
    """Service for reward operations"""

    @staticmethod
    def check_activity_count_reward(activity_count: int) -> Optional[dict]:
        """Check if user earned activity count reward"""
        rewards = {
            1: {"title": "First Activity", "points": 50},
            10: {"title": "Activity Explorer", "points": 100},
            50: {"title": "Sustainability Champion", "points": 250},
            100: {"title": "Eco Warrior", "points": 500},
        }
        return rewards.get(activity_count)

    @staticmethod
    def check_goal_completion_reward() -> dict:
        """Reward for completing a goal"""
        return {"title": "Goal Achiever", "points": 200}

    @staticmethod
    def calculate_streak_points(streak_days: int) -> int:
        """Calculate points for activity streak"""
        return min(streak_days * 10, 500)
