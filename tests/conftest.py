import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool

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
    connection = await async_engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection)

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture()
async def client(session):
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app), base_url='http://localhost:8000/api/v1'
    ) as client:
        yield client
