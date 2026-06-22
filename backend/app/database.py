"""
Database configuration and session management
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# Create base class for models
Base = declarative_base()

# Prepare database URL
database_url = settings.DATABASE_URL
if database_url.startswith("sqlite"):
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")

# Async database engine
async_engine = create_async_engine(
    database_url,
    echo=settings.DB_ECHO,
    future=True,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database (create tables)"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections"""
    await async_engine.dispose()
