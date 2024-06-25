import pytest
from httpx import AsyncClient

from app.core.db.postgres import AsyncSession, get_db


@pytest.mark.asyncio()
async def test_not_authenticated_user_dependency(client: AsyncClient):
    resp = await client.patch('/users/123')
    assert resp.status_code == 401  # noqa
    assert resp.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio()
async def test_get_db_dependency():
    async for s in get_db():
        assert isinstance(s, AsyncSession)
