from http import HTTPStatus

import pytest


@pytest.mark.asyncio()
async def test_get_categories(client, authorization_header):
    response = await client.get('/categories', headers=authorization_header)

    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data == []


@pytest.mark.asyncio()
async def test_create_category(client, authorization_header):
    category_data = dict(name='Test', description='Test description')

    response = await client.post(
        '/categories', json=category_data, headers=authorization_header
    )

    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['name'] == category_data['name']
    assert data['description'] == category_data['description']


@pytest.mark.asyncio()
async def test_delete_category(client, authorization_header):
    category_data = dict(name='Test', description='Test description')

    response = await client.post(
        '/categories', json=category_data, headers=authorization_header
    )

    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['name'] == category_data['name']
    assert data['description'] == category_data['description']

    response = await client.delete(
        f'/categories/{data["id"]}', headers=authorization_header
    )

    assert response.status_code == HTTPStatus.OK
