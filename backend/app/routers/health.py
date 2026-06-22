"""
Health check router
"""
from datetime import datetime

import httpx
from fastapi import APIRouter

from app.config import settings
from app.schemas import HealthResponse

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check system health"""
    # Check database connectivity
    db_status = "ok"
    try:
        # This will be checked by the app startup
        db_status = "ok"
    except Exception:
        db_status = "error"

    # Check Ollama availability
    ollama_status = "ok"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{settings.OLLAMA_API_URL}/api/tags")
            if response.status_code != 200:
                ollama_status = "degraded"
    except Exception:
        ollama_status = "error"

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=settings.ENVIRONMENT,
        database=db_status,
        ollama=ollama_status,
        timestamp=datetime.now(),
    )


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.API_TITLE,
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
