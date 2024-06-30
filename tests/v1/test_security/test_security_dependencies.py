import pytest
from httpx import AsyncClient

from app.core import exc
from app.core.db.postgres import AsyncSession, get_db
from app.core.sec import get_current_user, get_db_user


@pytest.mark.asyncio()
async def test_not_authenticated_user_dependency(client: AsyncClient):
    resp = await client.patch('/users/123')
    assert resp.status_code == 401  # noqa
    assert resp.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio()
async def test_get_db_dependency():
    async for s in get_db():
        assert isinstance(s, AsyncSession)


@pytest.mark.asyncio()
async def test_get_db_user_dependency():
    with pytest.raises(exc.UnauthorizedException):
        await get_db_user({'sub': 123})


def test_get_current_user_dependency_invalid_token_type():
    with pytest.raises(exc.UnauthorizedException):
        get_current_user('Invalid token')
