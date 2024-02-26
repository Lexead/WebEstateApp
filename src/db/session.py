from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..core import settings

async_engine = create_async_engine(
    url=settings.dev_settings.PG_DSN.unicode_string(),
    echo=True,
    future=True,
    pool_size=settings.dev_settings.SQLALCHEMY_POOL_SIZE,
    max_overflow=settings.dev_settings.SQLALCHEMY_MAX_OVERFLOW,
)

async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Session dependency"""

    async with async_session() as session:
        yield session
