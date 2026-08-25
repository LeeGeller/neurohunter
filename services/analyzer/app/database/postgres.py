"""Postgres database connection."""


from collections.abc import (
    AsyncGenerator,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import (
    settings,
)

DATABASE_URL = (
    f'postgresql+asyncpg://'
    f'{settings.postgres_user}:'
    f'{settings.postgres_password}@'
    f'{settings.postgres_host}:'
    f'{settings.postgres_port}/'
    f'{settings.postgres_db}'
)

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncGenerator(AsyncSession, None):
    """Get database session."""

    async with async_session() as session:
        yield session
