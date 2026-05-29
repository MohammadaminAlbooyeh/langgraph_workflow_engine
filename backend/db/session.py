from __future__ import annotations
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy import inspect
from backend.models.database import Base
from config import database_config
from backend.utils.logger import get_logger

logger = get_logger(__name__)

_engine: AsyncEngine | None = None
_async_session_maker: async_sessionmaker[AsyncSession] | None = None


async def init_db():
    global _engine, _async_session_maker
    logger.info(f"Initializing database: {database_config.url}")
    _engine = create_async_engine(
        database_config.url,
        pool_size=database_config.pool_size,
        max_overflow=database_config.max_overflow,
        echo=database_config.echo,
    )
    _async_session_maker = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")


async def close_db():
    global _engine
    if _engine:
        await _engine.dispose()
        _engine = None
        logger.info("Database connection closed")


async def get_session() -> AsyncSession:
    if _async_session_maker is None:
        await init_db()
    session = _async_session_maker()
    try:
        yield session
    finally:
        await session.close()


def get_session_sync() -> async_sessionmaker[AsyncSession]:
    if _async_session_maker is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _async_session_maker
