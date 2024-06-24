import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool, text

from app.core.db.postgres import (
    DATABASE_URI,
    AsyncSession,
    create_async_engine,
    get_db,
)
from app.main import app


@pytest_asyncio.fixture(scope='session')
async def async_engine():
    engine = create_async_engine(DATABASE_URI, future=True, poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def session(async_engine):
    async def truncate_all_tables(session: AsyncSession):
        tables = [
            # ! Add new tables here
            # ! The order of the tables is important
            'users',
            'records',
            'categories',
        ]

        for table in tables:
            await session.execute(text(f'TRUNCATE TABLE {table} CASCADE;'))
            await session.commit()

    try:
        session = AsyncSession(bind=async_engine)
        yield session

    finally:
        await truncate_all_tables(session)
        await session.close()


@pytest_asyncio.fixture()
async def client(session):
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app), base_url='http://localhost:8000/api/v1'
    ) as client:
        yield client
