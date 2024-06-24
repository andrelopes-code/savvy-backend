import pytest
from httpx import AsyncClient

from app.core.db.postgres import AsyncSession, get_db
from app.models.user import User


@pytest.mark.asyncio()
async def test_not_authenticated_user_dependency(client: AsyncClient):
    resp = await client.get('/users')
    assert resp.status_code == 401  # noqa
    assert resp.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio()
async def test_authenticated_user_dependency(session, client: AsyncClient):
    user = User(
        name='André Lopes',
        email='andrelopes@gmail.com',
        password='Password123',
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    resp = await client.post(
        '/auth/token',
        data={'username': 'andrelopes@gmail.com', 'password': 'Password123'},
    )

    access_token = resp.json()['access_token']
    refresh_token = resp.json()['refresh_token']

    assert resp.status_code == 200  # noqa
    assert access_token
    assert refresh_token

    resp = await client.get(
        '/users', headers={'Authorization': f'Bearer {access_token}'}
    )
    assert resp.status_code == 200  # noqa


@pytest.mark.asyncio()
async def test_get_db_dependency():
    async for s in get_db():
        assert isinstance(s, AsyncSession)
