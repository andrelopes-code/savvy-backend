from fastapi import APIRouter

from app.core.dependencies import AuthenticatedDepends

router = APIRouter(dependencies=[AuthenticatedDepends])


@router.post('/users')
async def create_user(): ...


@router.get('/users')
async def list_users(): ...


@router.get('/users/{id}')
async def get_user(id: int): ...


@router.patch('/users/{id}')
async def update_user(): ...


@router.delete('/users/{id}')
async def delete_user(): ...
