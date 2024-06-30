from fastapi import APIRouter, status

from app.core.dependencies import (
    AsyncDBSessionDepends,
    AuthenticatedDBUserDepends,
)
from app.schemas.record_schemas import (
    RecordIn,
    RecordOut,
    RecordWithCategoryOut,
)
from app.services.record_service import RecordService

router = APIRouter()


@router.get('/records', response_model=list[RecordWithCategoryOut])
async def get_user_records(
    user: AuthenticatedDBUserDepends,
    session: AsyncDBSessionDepends,
    sort: str | None = None,
):
    record_service = RecordService(session, user)
    return await record_service.get_user_records(sort=sort)


@router.post(
    '/records',
    response_model=RecordWithCategoryOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_record(
    user: AuthenticatedDBUserDepends,
    session: AsyncDBSessionDepends,
    data: RecordIn,
):
    record_service = RecordService(session, user)
    return await record_service.create_record(data)


@router.delete('/records/{record_id}', response_model=RecordOut)
async def delete_record(
    user: AuthenticatedDBUserDepends,
    session: AsyncDBSessionDepends,
    record_id: int,
):
    record_service = RecordService(session, user)
    return await record_service.delete_record(record_id)
