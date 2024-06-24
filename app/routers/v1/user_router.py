from fastapi import APIRouter

from app.core.dependencies import (
    AsyncDBSessionDepends,
    AuthenticatedDBUserDepends,
)
from app.schemas.user_schemas import UserIn, UserOut, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.post('/users', response_model=UserOut)
async def create_user(session: AsyncDBSessionDepends, data: UserIn):
    user_service = UserService(session)
    return await user_service.create_user(data)


@router.get('/users/me', response_model=UserOut)
async def get_current_user(current_user: AuthenticatedDBUserDepends):
    return current_user


@router.patch('/users/{user_id}', response_model=UserOut)
async def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: AuthenticatedDBUserDepends,
    session: AsyncDBSessionDepends,
):
    user_service = UserService(session)
    return await user_service.update_user(user_id, current_user, data)


@router.delete('/users/{id}')
async def delete_user(
    user_id: int,
    current_user: AuthenticatedDBUserDepends,
    session: AsyncDBSessionDepends,
):
    user_service = UserService(session)
    return await user_service.delete_user(user_id, current_user)
