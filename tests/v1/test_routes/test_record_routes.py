from datetime import datetime, timezone
from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio()
async def test_create_record(user_category_autheaders, client: AsyncClient):
    # (User, Category, Authorization Headers)
    _, category, headers = user_category_autheaders

    record_data = dict(
        amount=20,
        description='vaquinha',
        category_id=category.id,
        date=datetime.now(timezone.utc).isoformat(),
    )
    response = await client.post(
        url='/records',
        headers=headers,
        json=record_data,
    )

    data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert data['amount'] == record_data['amount']
    assert data['description'] == record_data['description']
    assert data['category'] == {
        'id': category.id,
        'name': category.name,
        'description': category.description,
    }


@pytest.mark.asyncio()
async def test_get_records(user_category_autheaders, client: AsyncClient):
    # (User, Category, Authorization Headers)
    _, category, headers = user_category_autheaders
    # Create records
    for i in range(5):
        record_data = dict(
            amount=i + 1 * 10,
            description=f'vaquinha {i}',
            category_id=category.id,
            date=datetime.now(timezone.utc).isoformat(),
        )
        await client.post(
            url='/records',
            headers=headers,
            json=record_data,
        )

    expected_size = 5

    response = await client.get('/records', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == expected_size


@pytest.mark.asyncio()
async def test_delete_record(user_category_autheaders, client: AsyncClient):
    # (User, Category, Authorization Headers)
    _, category, headers = user_category_autheaders

    record_data = dict(
        amount=20,
        description='vaquinha',
        category_id=category.id,
        date=datetime.now(timezone.utc).isoformat(),
    )
    response = await client.post(
        url='/records',
        headers=headers,
        json=record_data,
    )

    data = response.json()

    deleted_record = await client.delete(
        url=f'/records/{data["id"]}',
        headers=headers,
    )

    assert deleted_record.status_code == HTTPStatus.OK
    assert deleted_record.json()


@pytest.mark.asyncio()
async def test_create_record_with_invalid_amount(
    user_category_autheaders, client: AsyncClient
):
    _, category, headers = user_category_autheaders
    record_data = dict(
        amount=0,
        description='vaquinha',
        category_id=category.id,
        date=datetime.now(timezone.utc).isoformat(),
    )
    response = await client.post(
        url='/records',
        headers=headers,
        json=record_data,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['loc'] == ['body', 'amount']


@pytest.mark.asyncio()
async def test_create_record_with_invalid_category(
    user_category_autheaders, client: AsyncClient
):
    _, _, headers = user_category_autheaders
    record_data = dict(
        amount=10,
        description='vaquinha',
        category_id=12,
        date=datetime.now(timezone.utc).isoformat(),
    )
    response = await client.post(
        url='/records',
        headers=headers,
        json=record_data,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Category not found or invalid for this user'
    }


@pytest.mark.asyncio()
async def test_create_record_with_invalid_description_length(
    user_category_autheaders, client: AsyncClient
):
    _, category, headers = user_category_autheaders
    record_data = dict(
        amount=10,
        description='x' * 31,
        category_id=category.id,
        date=datetime.now(timezone.utc).isoformat(),
    )
    response = await client.post(
        url='/records',
        headers=headers,
        json=record_data,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['loc'] == ['body', 'description']
