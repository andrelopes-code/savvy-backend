import asyncio

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool, text

from app.core.db.postgres import (
    DATABASE_URI,
    AsyncSession,
    create_async_engine,
)
from app.core.sec import SecurityService
from app.main import app
from app.models import Category
from app.schemas.user_schemas import UserIn
from app.services.user_service import UserService


async def create_category(session):
    """Create a category"""
    category = Category(name='Categoria', user_id=None)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def async_engine():
    """Creates a new database engine"""
    engine = create_async_engine(DATABASE_URI, future=True, poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def session(async_engine):
    """Creates a new database session for each test case"""

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
            await session.execute(
                text(f'ALTER SEQUENCE {table}_id_seq RESTART WITH 1;')
            )
            await session.commit()

    try:
        session = AsyncSession(
            bind=async_engine,
            expire_on_commit=False,
        )
        yield session

    finally:
        await truncate_all_tables(session)
        await session.close()


@pytest_asyncio.fixture()
async def client(session):
    """Creates a new AsyncClient for each test case"""
    async with AsyncClient(
        transport=ASGITransport(app), base_url='http://localhost:8000/api/v1'
    ) as client:
        yield client


@pytest_asyncio.fixture()
async def user(session):
    user_service = UserService(session)
    return await user_service.create_user(
        UserIn(email='testuser@ex.com', name='User Name', password='Pass12345')
    )


@pytest_asyncio.fixture()
async def authorization_header(user):
    """Create an authorization header for the user"""
    token = SecurityService.create_access_token({'sub': user.id})
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }


# ===================================== #
# *           Specific fixtures       * #
# ===================================== #


@pytest_asyncio.fixture()
async def user_category_autheaders(session, user):
    """Create a user, a category and a record

    Returns:
        Tuple[User, Category, Dict[str, str]]
    """
    token = SecurityService.create_access_token({'sub': user.id})
    catg = await create_category(session)
    return (
        user,
        catg,
        {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
    )
