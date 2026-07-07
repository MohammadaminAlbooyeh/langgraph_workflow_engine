"""Initialize the database."""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from backend.models.database import Base
from config.database_config import DatabaseConfig


async def init():
    config = DatabaseConfig()
    engine = create_async_engine(config.url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Database initialized successfully.")


if __name__ == "__main__":
    asyncio.run(init())
