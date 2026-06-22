"""
Utility functions for JWT handling
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from pydantic import ValidationError

from app.config import settings
from app.schemas import TokenPayload


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Args:
        data: Data to encode in token
        expires_delta: Token expiration time delta

    Returns:
        JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token

    Args:
        data: Data to encode in token

    Returns:
        JWT token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[TokenPayload]:
    """
    Verify JWT token and extract payload

    Args:
        token: JWT token to verify

    Returns:
        Token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        return token_data
    except (JWTError, ValidationError):
        return None
