"""
Authentication router
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas import TokenResponse, UserCreate, UserResponse
from app.utils.jwt_handler import create_access_token, create_refresh_token, verify_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password"""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user

    Returns:
        Token response with access and refresh tokens
    """
    # Check if email already exists
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create new user
    from uuid import uuid4

    new_user = User(
        id=uuid4(),
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Create tokens
    access_token = create_access_token(
        data={"sub": str(new_user.id), "email": new_user.email, "role": new_user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(new_user.id), "email": new_user.email}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=60 * 60,  # 1 hour in seconds
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    email: str, password: str, db: AsyncSession = Depends(get_db)
):
    """
    Login user

    Returns:
        Token response with access and refresh tokens
    """
    # Find user by email
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # Update last login
    user.last_login = datetime.now()
    await db.commit()

    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=60 * 60,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """
    Refresh access token

    Returns:
        New access token
    """
    token_data = verify_token(refresh_token)

    if not token_data or token_data.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    new_access_token = create_access_token(
        data={
            "sub": token_data.sub,
            "email": token_data.email,
            "role": token_data.role,
        }
    )

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=refresh_token,
        expires_in=60 * 60,
    )


def get_current_user(token: str) -> dict:
    """
    Dependency to get current user from token

    Args:
        token: Bearer token from Authorization header

    Returns:
        User data from token
    """
    if not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
        )

    token_str = token.split(" ")[1]
    token_data = verify_token(token_str)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {"user_id": token_data.sub, "email": token_data.email, "role": token_data.role}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current authenticated user information"""
    query = select(User).where(User.id == current_user["user_id"])
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
