"""
Configuration module for the application
"""
import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_VERSION: str = "v1"
    API_TITLE: str = "AI Carbon Footprint Coach"
    API_DESCRIPTION: str = "REST API for tracking and reducing carbon footprint"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost/carbon_coach"
    DB_ECHO: bool = False

    # JWT Configuration
    JWT_SECRET: str = "your-secret-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Supabase Configuration (Optional)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None

    # Ollama Configuration
    OLLAMA_API_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma:2b"
    OLLAMA_TIMEOUT: int = 120

    # SMTP Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_EMAIL: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "Carbon Coach"

    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "https://localhost",
    ]

    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # File Upload Configuration
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
