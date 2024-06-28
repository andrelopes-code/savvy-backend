from app.models.record import Record

from .base_repository import AsyncCRUDRepository


class RecordRepository(AsyncCRUDRepository[Record]):
    def __init__(self, session):
        super().__init__(session, Record)
