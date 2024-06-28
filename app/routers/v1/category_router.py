from fastapi import APIRouter

from app.core.dependencies import (
    AsyncDBSessionDepends,
    AuthenticatedDBUserDepends,
)
from app.schemas.category_schemas import CategoryIn
from app.schemas.record_schemas import CategoryOut
from app.services.category_service import CategoryService

router = APIRouter()


@router.get('/categories', response_model=list[CategoryOut])
async def get_gategories(
    session: AsyncDBSessionDepends,
    user: AuthenticatedDBUserDepends,
):
    category_service = CategoryService(session, user)
    return await category_service.get_categories()


@router.post('/categories', response_model=CategoryOut)
async def create_category(
    data: CategoryIn,
    session: AsyncDBSessionDepends,
    user: AuthenticatedDBUserDepends,
):
    category_service = CategoryService(session, user)
    return await category_service.create_category(data)


@router.delete('/categories/{category_id}', response_model=CategoryOut)
async def delete_category(
    category_id: int,
    session: AsyncDBSessionDepends,
    user: AuthenticatedDBUserDepends,
):
    category_service = CategoryService(session, user)
    return await category_service.delete_category(category_id)
