import pytest_asyncio
from sqlalchemy import NullPool, text

from app.core.db.postgres import (
    DATABASE_URI,
    AsyncSession,
    create_async_engine,
)


async def truncate_all_tables(session):
    models = [
        'users',
    ]
    for model in models:
        await session.execute(text(f'TRUNCATE TABLE {model} CASCADE;'))
        await session.commit()


@pytest_asyncio.fixture(scope='session')
async def async_engine():
    engine = create_async_engine(DATABASE_URI, future=True, poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def session(async_engine):
    connection = await async_engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection)

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()
