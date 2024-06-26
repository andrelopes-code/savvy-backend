import pytest

from app.schemas.user_schemas import UserIn


@pytest.mark.asyncio()
async def test_get_token(client):
    new_user = UserIn(
        name='testuser', email='testuser@example.com', password='Pass12345'
    )

    response = await client.post('/users', json=new_user.model_dump())
    assert response.status_code == 201  # noqa

    login_data = {'username': 'testuser@example.com', 'password': 'Pass12345'}

    response = await client.post('/auth/token', data=login_data)
    assert response.status_code == 200  # noqa
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()
    assert 'token_type' in response.json()


@pytest.mark.asyncio()
async def test_get_token_fail(client):
    new_user = UserIn(
        name='testuser', email='testuser@example.com', password='Pass12345'
    )

    response = await client.post('/users', json=new_user.model_dump())
    assert response.status_code == 201  # noqa

    login_data = {'username': 'testuser@example.com', 'password': '12345Pass'}

    response = await client.post('/auth/token', data=login_data)
    assert response.status_code == 401  # noqa


@pytest.mark.asyncio()
async def test_refresh_token(client):
    new_user = UserIn(
        name='testuser', email='testuser@example.com', password='Pass12345'
    )

    response = await client.post('/users', json=new_user.model_dump())
    assert response.status_code == 201  # noqa

    login_data = {'username': 'testuser@example.com', 'password': 'Pass12345'}

    response = await client.post('/auth/token', data=login_data)
    assert response.status_code == 200  # noqa
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()
    assert 'token_type' in response.json()

    refresh_token = response.json()['refresh_token']

    response = await client.post(
        '/auth/token/refresh',
        headers={'X-Refresh-Token': 'Bearer ' + refresh_token},
    )

    assert response.status_code == 200  # noqa
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()
    assert 'token_type' in response.json()
