"""
Admin router
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import EmissionFactor, User
from app.routers.auth import get_current_user
from app.schemas import EmissionFactorCreate, EmissionFactorResponse, EmissionFactorUpdate
from uuid import uuid4

router = APIRouter(prefix="/api/admin", tags=["admin"])


def require_admin(current_user: dict = Depends(get_current_user)):
    """Dependency to require admin role"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


@router.get("/users", response_model=List[dict])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all users (admin only)"""
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()

    return [
        {
            "id": str(u.id),
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at,
            "last_login": u.last_login,
        }
        for u in users
    ]


@router.get("/users/{user_id}", response_model=dict)
async def get_user(
    user_id: str,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get user details (admin only)"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "bio": user.bio,
        "role": user.role,
        "is_active": user.is_active,
        "email_verified": user.email_verified,
        "created_at": user.created_at,
        "last_login": user.last_login,
    }


@router.put("/users/{user_id}", response_model=dict)
async def update_user(
    user_id: str,
    data: dict,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update user (admin only)"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if "is_active" in data:
        user.is_active = data["is_active"]

    if "role" in data:
        user.role = data["role"]

    await db.commit()

    return {"message": "User updated successfully"}


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete user (admin only)"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await db.delete(user)
    await db.commit()


@router.get("/emission-factors", response_model=List[EmissionFactorResponse])
async def list_emission_factors(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List emission factors (admin only)"""
    query = select(EmissionFactor).where(EmissionFactor.is_active == True)

    if category:
        query = query.where(EmissionFactor.category == category)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    factors = result.scalars().all()

    return factors


@router.post("/emission-factors", response_model=EmissionFactorResponse, status_code=status.HTTP_201_CREATED)
async def create_emission_factor(
    factor_data: EmissionFactorCreate,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create emission factor (admin only)"""
    new_factor = EmissionFactor(
        id=uuid4(),
        category=factor_data.category,
        subcategory=factor_data.subcategory,
        description=factor_data.description,
        factor_value=factor_data.factor_value,
        unit=factor_data.unit,
        source=factor_data.source,
        region=factor_data.region,
    )

    db.add(new_factor)
    await db.commit()
    await db.refresh(new_factor)

    return new_factor


@router.put("/emission-factors/{factor_id}", response_model=EmissionFactorResponse)
async def update_emission_factor(
    factor_id: str,
    factor_data: EmissionFactorUpdate,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update emission factor (admin only)"""
    query = select(EmissionFactor).where(EmissionFactor.id == factor_id)
    result = await db.execute(query)
    factor = result.scalar_one_or_none()

    if not factor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emission factor not found",
        )

    if factor_data.factor_value is not None:
        factor.factor_value = factor_data.factor_value

    if factor_data.description is not None:
        factor.description = factor_data.description

    if factor_data.source is not None:
        factor.source = factor_data.source

    await db.commit()
    await db.refresh(factor)

    return factor


@router.delete("/emission-factors/{factor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emission_factor(
    factor_id: str,
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete emission factor (admin only)"""
    query = select(EmissionFactor).where(EmissionFactor.id == factor_id)
    result = await db.execute(query)
    factor = result.scalar_one_or_none()

    if not factor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emission factor not found",
        )

    factor.is_active = False
    await db.commit()


@router.get("/statistics")
async def get_admin_statistics(
    current_user: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get global statistics (admin only)"""
    from sqlalchemy import func

    # Total users
    query = select(func.count(User.id))
    result = await db.execute(query)
    total_users = result.scalar() or 0

    # Active users
    query = select(func.count(User.id)).where(User.is_active == True)
    result = await db.execute(query)
    active_users = result.scalar() or 0

    from app.models import Activity

    # Total activities
    query = select(func.count(Activity.id))
    result = await db.execute(query)
    total_activities = result.scalar() or 0

    # Total emissions
    query = select(func.sum(Activity.carbon_emissions))
    result = await db.execute(query)
    total_emissions = float(result.scalar() or 0.0)

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_activities": total_activities,
        "total_emissions": total_emissions,
        "average_user_emissions": total_emissions / total_users if total_users > 0 else 0,
    }
