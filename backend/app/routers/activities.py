"""
Activities router
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Activity
from app.routers.auth import get_current_user
from app.schemas import ActivityCreate, ActivityResponse, ActivityUpdate
from app.services.emission_calculator import EmissionCalculator
from uuid import uuid4

router = APIRouter(prefix="/api/activities", tags=["activities"])


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_data: ActivityCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new activity"""
    # Calculate emissions
    emissions = await EmissionCalculator.calculate_emissions(
        db,
        activity_data.activity_type,
        activity_data.category,
        activity_data.value,
        activity_data.unit,
    )

    # Create activity
    new_activity = Activity(
        id=uuid4(),
        user_id=current_user["user_id"],
        activity_type=activity_data.activity_type,
        category=activity_data.category,
        description=activity_data.description,
        value=activity_data.value,
        unit=activity_data.unit,
        carbon_emissions=emissions,
    )

    db.add(new_activity)
    await db.commit()
    await db.refresh(new_activity)

    return new_activity


@router.get("", response_model=List[ActivityResponse])
async def list_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    activity_type: str = Query(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's activities"""
    query = select(Activity).where(Activity.user_id == current_user["user_id"])

    if activity_type:
        query = query.where(Activity.activity_type == activity_type)

    query = query.order_by(desc(Activity.created_at)).offset(skip).limit(limit)

    result = await db.execute(query)
    activities = result.scalars().all()

    return activities


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific activity"""
    query = select(Activity).where(
        and_(
            Activity.id == activity_id,
            Activity.user_id == current_user["user_id"],
        )
    )

    result = await db.execute(query)
    activity = result.scalar_one_or_none()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    return activity


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: str,
    activity_data: ActivityUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an activity"""
    query = select(Activity).where(
        and_(
            Activity.id == activity_id,
            Activity.user_id == current_user["user_id"],
        )
    )

    result = await db.execute(query)
    activity = result.scalar_one_or_none()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    # Update fields if provided
    if activity_data.value is not None or activity_data.unit is not None:
        # Recalculate emissions
        value = activity_data.value or activity.value
        unit = activity_data.unit or activity.unit
        activity.carbon_emissions = await EmissionCalculator.calculate_emissions(
            db,
            activity.activity_type,
            activity.category,
            value,
            unit,
        )
        activity.value = value
        activity.unit = unit

    if activity_data.category is not None:
        activity.category = activity_data.category

    if activity_data.description is not None:
        activity.description = activity_data.description

    await db.commit()
    await db.refresh(activity)

    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an activity"""
    query = select(Activity).where(
        and_(
            Activity.id == activity_id,
            Activity.user_id == current_user["user_id"],
        )
    )

    result = await db.execute(query)
    activity = result.scalar_one_or_none()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    await db.delete(activity)
    await db.commit()


@router.get("/stats/summary")
async def get_activity_stats(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get activity statistics for user"""
    from sqlalchemy import func
    from datetime import date

    today = date.today()

    # Today's emissions
    query = select(func.sum(Activity.carbon_emissions)).where(
        and_(
            Activity.user_id == current_user["user_id"],
            func.date(Activity.created_at) == today,
        )
    )
    result = await db.execute(query)
    today_emissions = result.scalar() or 0.0

    # Activity count
    query = select(func.count(Activity.id)).where(
        Activity.user_id == current_user["user_id"]
    )
    result = await db.execute(query)
    total_activities = result.scalar() or 0

    return {
        "today_emissions": float(today_emissions),
        "total_activities": total_activities,
    }
