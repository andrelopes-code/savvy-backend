from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core import settings

DATABASE_URI = 'postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
    settings.DATABASE_NAME,
    settings.DATABASE_PASSWORD,
    settings.DATABASE_HOST,
    settings.DATABASE_PORT,
    settings.DATABASE_NAME,
)

engine = create_async_engine(DATABASE_URI, future=True)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    """This function is used to get a database session in an async context"""
    async with async_session() as s:
        yield s


# A FastAPI dependency that gets the database session in an async context
AsyncDBSessionDepends = Annotated[AsyncSession, Depends(get_db)]
