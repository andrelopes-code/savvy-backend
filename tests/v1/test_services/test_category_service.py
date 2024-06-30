import pytest

from app.core import exc
from app.schemas.category_schemas import CategoryIn
from app.services.category_service import CategoryService


@pytest.mark.asyncio()
async def test_category_service(session, user):
    category_service = CategoryService(session, user)
    assert category_service


@pytest.mark.asyncio()
async def test_category_service_get_categories(session, user):
    category_service = CategoryService(session, user)
    categories = await category_service.get_categories()
    assert categories == []


@pytest.mark.asyncio()
async def test_category_service_create_category(session, user):
    category_service = CategoryService(session, user)
    category = await category_service.create_category(
        CategoryIn(name='Category 1')
    )
    assert category


@pytest.mark.asyncio()
async def test_category_service_max_categories_count(session, user):
    category_service = CategoryService(session, user)

    for _ in range(5):
        await category_service.create_category(CategoryIn(name='Category'))

    with pytest.raises(exc.ForbiddenException) as e:
        await category_service.create_category(CategoryIn(name='Category'))

    assert e.value.detail == 'Max categories reached'


@pytest.mark.asyncio()
async def test_category_service_delete_category(session, user):
    category_service = CategoryService(session, user)

    category = await category_service.create_category(
        CategoryIn(name='Category 1')
    )
    assert category
    assert category_service.user.categories_count == 1

    category = await category_service.delete_category(category.id)
    assert category
    assert category_service.user.categories_count == 0

    with pytest.raises(exc.NotFoundException) as e:
        await category_service.delete_category(category.id)

    assert e.value.detail == 'Category not found or invalid for this user'
