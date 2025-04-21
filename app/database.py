from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.settings import settings

engine = create_async_engine(settings.database_url, connect_args={"check_same_thread": False}, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)
async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session
