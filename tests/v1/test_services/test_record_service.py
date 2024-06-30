import pytest

from app.core import exc
from app.core.db.postgres import async_session
from app.schemas.record_schemas import RecordIn
from app.schemas.user_schemas import UserIn
from app.services.record_service import RecordService
from app.services.user_service import UserService


@pytest.mark.asyncio()
async def test_record_service_create_record(user_category_autheaders):
    user, category, _ = user_category_autheaders
    async with async_session() as session:
        record_service = RecordService(session, user)

        # New record to be created
        new_record = RecordIn(
            date='2022-01-01',
            category_id=category.id,
            amount=100,
            description='Test',
        )

        # Create the record
        record = await record_service.create_record(new_record)

        assert record
        assert record.user_id == user.id
        assert record.category_id == category.id
        assert record.amount == new_record.amount


@pytest.mark.asyncio()
async def test_record_service_delete_record(user_category_autheaders):
    user, category, _ = user_category_autheaders
    async with async_session() as session:
        record_service = RecordService(session, user)

        # New record to be created
        new_record = RecordIn(
            date='2022-01-01',
            category_id=category.id,
            amount=100,
            description='Test',
        )

        # Create the record
        record = await record_service.create_record(new_record)

        # Delete the record
        deleted_record = await record_service.delete_record(record.id)

        assert deleted_record
        assert deleted_record.id == record.id
        assert await record_service.get_user_records() == []


@pytest.mark.asyncio()
async def test_record_service_delete_record_not_found(
    user_category_autheaders,
):
    user, _, _ = user_category_autheaders
    async with async_session() as session:
        record_service = RecordService(session, user)

        with pytest.raises(exc.NotFoundException):
            await record_service.delete_record(123)


@pytest.mark.asyncio()
async def test_record_service_delete_record_unauthorized(
    user_category_autheaders,
):
    user, category, _ = user_category_autheaders
    async with async_session() as session:
        record_service = RecordService(session, user)

        # New record to be created
        new_record = RecordIn(
            date='2022-01-01',
            category_id=category.id,
            amount=100,
            description='Test',
        )

        new_user = UserIn(
            name='User Name',
            email='testuser@example.com',
            password='Pass12345',
        )
        new_user = await UserService(session).create_user(new_user)
        assert new_user

        # Create the record
        new_record_service = RecordService(session, new_user)
        record = await new_record_service.create_record(new_record)

        with pytest.raises(exc.UnauthorizedException):
            await record_service.delete_record(record.id)
