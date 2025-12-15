
import logging
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/medbridge",
)

logger = logging.getLogger(__name__)

# Helpful runtime check: if the URL doesn't reference the asyncpg dialect, warn the user
if DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
    logger.warning(
        "DATABASE_URL does not include an async driver (asyncpg). "
        "Either update DATABASE_URL to 'postgresql+asyncpg://...' or install a sync driver like 'psycopg2-binary'."
    )

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async DB session."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """Create DB tables (safe to call on startup in dev)."""
    from .models import Base  # local import to avoid circular

    # Use connection begin to run sync metadata.create_all
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
