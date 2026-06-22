"""
Analytics router
"""
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Activity, Goal
from app.routers.auth import get_current_user
from app.schemas import AnalyticsResponse, DailyEmissions, EmissionsTrendResponse

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/dashboard")
async def get_dashboard(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard data"""
    from datetime import date

    user_id = current_user["user_id"]
    today = date.today()

    # Today's emissions
    query = select(func.sum(Activity.carbon_emissions)).where(
        and_(
            Activity.user_id == user_id,
            func.date(Activity.created_at) == today,
        )
    )
    result = await db.execute(query)
    today_emissions = float(result.scalar() or 0.0)

    # This month's emissions
    first_day = date(today.year, today.month, 1)
    query = select(func.sum(Activity.carbon_emissions)).where(
        and_(
            Activity.user_id == user_id,
            func.date(Activity.created_at) >= first_day,
        )
    )
    result = await db.execute(query)
    month_emissions = float(result.scalar() or 0.0)

    # This year's emissions
    first_day_year = date(today.year, 1, 1)
    query = select(func.sum(Activity.carbon_emissions)).where(
        and_(
            Activity.user_id == user_id,
            func.date(Activity.created_at) >= first_day_year,
        )
    )
    result = await db.execute(query)
    year_emissions = float(result.scalar() or 0.0)

    # Total emissions
    query = select(func.sum(Activity.carbon_emissions)).where(Activity.user_id == user_id)
    result = await db.execute(query)
    total_emissions = float(result.scalar() or 0.0)

    # Active goals
    query = select(func.count(Goal.id)).where(
        and_(
            Goal.user_id == user_id,
            Goal.status == "active",
        )
    )
    result = await db.execute(query)
    active_goals = result.scalar() or 0

    # Activities count
    query = select(func.count(Activity.id)).where(Activity.user_id == user_id)
    result = await db.execute(query)
    activities_count = result.scalar() or 0

    # Last activity
    query = select(Activity.created_at).where(Activity.user_id == user_id).order_by(desc(Activity.created_at)).limit(1)
    result = await db.execute(query)
    last_activity = result.scalar()

    return {
        "total_emissions": total_emissions,
        "today_emissions": today_emissions,
        "this_month_emissions": month_emissions,
        "this_year_emissions": year_emissions,
        "active_goals": active_goals,
        "total_points": 0,  # TODO: Calculate from rewards
        "activities_count": activities_count,
        "last_activity_date": last_activity,
    }


@router.get("/emissions/summary")
async def get_emissions_summary(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get emissions summary by activity type"""
    query = (
        select(
            Activity.activity_type,
            func.sum(Activity.carbon_emissions).label("total"),
            func.count(Activity.id).label("count"),
        )
        .where(Activity.user_id == current_user["user_id"])
        .group_by(Activity.activity_type)
        .order_by(desc("total"))
    )

    result = await db.execute(query)
    emissions = result.all()

    return [
        {
            "activity_type": e[0],
            "total_emissions": float(e[1] or 0.0),
            "activity_count": e[2],
        }
        for e in emissions
    ]


@router.get("/emissions/trends")
async def get_emissions_trends(
    period: str = "monthly",
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get emissions trends"""
    from datetime import date

    user_id = current_user["user_id"]
    today = date.today()

    if period == "daily":
        # Last 30 days
        start_date = today - timedelta(days=30)
        date_format = "%Y-%m-%d"
    elif period == "weekly":
        # Last 12 weeks
        start_date = today - timedelta(weeks=12)
        date_format = "%Y-W%W"
    else:  # monthly
        # Last 12 months
        start_date = today - timedelta(days=365)
        date_format = "%Y-%m"

    query = (
        select(
            func.date_trunc(period, Activity.created_at).label("period"),
            func.sum(Activity.carbon_emissions).label("total"),
        )
        .where(
            and_(
                Activity.user_id == user_id,
                func.date(Activity.created_at) >= start_date,
            )
        )
        .group_by("period")
        .order_by("period")
    )

    result = await db.execute(query)
    data = result.all()

    return {
        "period": period,
        "data": [
            {
                "date": d[0],
                "emissions": float(d[1] or 0.0),
            }
            for d in data
        ],
    }


@router.get("/goals/progress")
async def get_goals_progress(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get progress of user's goals"""
    query = select(Goal).where(
        and_(
            Goal.user_id == current_user["user_id"],
            Goal.status == "active",
        )
    ).order_by(Goal.deadline)

    result = await db.execute(query)
    goals = result.scalars().all()

    return [
        {
            "id": str(g.id),
            "title": g.title,
            "progress_percentage": g.progress_percentage,
            "deadline": g.deadline,
            "baseline": g.baseline_emissions,
            "target": g.target_emissions,
        }
        for g in goals
    ]
