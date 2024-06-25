import pytest
from httpx import AsyncClient

from app.schemas.user_schemas import UserIn, UserOut, UserUpdate


@pytest.mark.asyncio()
async def test_create_user(client: AsyncClient):
    # Create a new user
    new_user = UserIn(
        name='User Name', email='testuser@example.com', password='Pass12345'
    )

    # Make a POST request to the create_user route
    response = await client.post('/users', json=new_user.model_dump())

    # Assert that the response is successful
    assert response.status_code == 201  # noqa

    # Assert that the returned user matches the created user
    returned_user = UserOut(**response.json())
    assert returned_user.name == new_user.name
    assert returned_user.email == new_user.email


@pytest.mark.asyncio()
async def test_create_user_with_invalid_password(client: AsyncClient):
    # Create a new user
    new_user = dict(
        name='User Name', email='testuser@example.com', password='Pass'
    )

    response = await client.post('/users', json=new_user)

    assert response.status_code == 422  # noqa
    assert response.json()['detail'][0]['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_get_current_user(client):
    # Create a new user
    new_user = UserIn(
        name='testuser', email='testuser@example.com', password='Pass12345'
    )

    # Create the user in the database
    response = await client.post('/users', json=new_user.model_dump())
    assert response.status_code == 201  # noqa

    # Log in as the new user
    login_data = {'username': new_user.email, 'password': new_user.password}
    response = await client.post('/auth/token', data=login_data)

    # Get the access token from the response
    access_token = response.json()['access_token']

    # Make a GET request to the get_current_user route with the access token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = await client.get('/users/me', headers=headers)

    # Assert that the response is successful
    assert response.status_code == 200  # noqa

    # Assert that the returned user matches the created user
    returned_user = UserOut(**response.json())
    assert returned_user.name == new_user.name
    assert returned_user.email == new_user.email


@pytest.mark.asyncio()
async def test_get_current_user_unauthorized(client):
    # Make a GET request to the get_current_user route
    response = await client.get('/users/me')

    # Assert that the response is unauthorized
    assert response.status_code == 401  # noqa
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio()
async def test_update_user_route(client):
    # Create a new user
    new_user = UserIn(
        name='User Name', email='testuser@example.com', password='Pass12345'
    )

    # Make a POST request to the create_user route
    response = await client.post('/users', json=new_user.model_dump())

    # Assert that the response is successful
    assert response.status_code == 201  # noqa

    # Assert that the returned user matches the created user
    returned_user = UserOut(**response.json())
    assert returned_user.name == new_user.name
    assert returned_user.email == new_user.email

    # Update the user
    updated_user = UserUpdate(
        name='Updated User Name',
    )

    # Login as the new user
    login_data = {'username': new_user.email, 'password': new_user.password}
    response = await client.post('/auth/token', data=login_data)
    access_token = response.json()['access_token']

    # Make a PUT request to the update_user route
    response = await client.patch(
        f'/users/{returned_user.id}',
        json=updated_user.model_dump(),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    # Assert that the response is successful
    assert response.status_code == 200  # noqa

    # Assert that the returned user matches the updated user
    returned_user = UserOut(**response.json())
    assert returned_user.name == updated_user.name
