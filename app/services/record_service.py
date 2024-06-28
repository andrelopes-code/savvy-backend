from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core import exc
from app.models.category import Category
from app.models.record import Record
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.record_repository import RecordRepository
from app.schemas.record_schemas import RecordIn


class RecordService:
    def __init__(self, session: AsyncSession, user: User) -> None:
        self.user = user
        self.session = session
        self.repository = RecordRepository(session)

    async def create_record(self, data: RecordIn) -> Record:
        category = await self._validate_category(data.category_id)
        # Create the record, attach the category and return it
        record = Record(**data.model_dump(), user_id=self.user.id)
        created_record = await self.repository.save(record)
        created_record.category = category
        return created_record

    async def delete_record(self, record_id: int) -> Record:
        # Check if the record to be deleted exists
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise exc.NotFoundException('Record not found')
        # Check if the record belongs to the user
        if record.user_id != self.user.id:
            raise exc.UnauthorizedException('You cannot delete this record')
        # Delete the record and return it
        deleted_record = await self.repository.delete_by_id(record_id)
        return deleted_record

    async def get_user_records(self, sort: str | None = None) -> list[Record]:
        stmt = (
            select(Record)
            .options(joinedload(Record.category))
            .filter(Record.user_id == self.user.id)
        )
        if sort:
            RecordService._apply_sorting_if_valid(stmt, sort)
        # Get all records for the user and return them
        records = await self.repository.get_all(stmt)
        return records

    async def _validate_category(self, category_id: int) -> Category:
        # Check if the category exists and belongs to the user
        category_repository = CategoryRepository(self.session)
        category = await category_repository.get_by_id(category_id)
        if not category or category.user_id not in {None, self.user.id}:
            raise exc.NotFoundException(
                'Category not found or invalid for this user'
            )
        return category

    @staticmethod
    def _apply_sorting_if_valid(stmt: select, sort: str) -> None:
        """Apply sorting if valid sort parameter is provided"""
        match sort:
            case _:
                stmt = stmt.order_by(Record.date.desc())
