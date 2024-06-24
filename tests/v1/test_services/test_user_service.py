import pytest

from app.core import exc
from app.schemas.user_schemas import UserIn, UserUpdate
from app.services.user_service import UserService


@pytest.mark.asyncio()
async def test_user_service(session):
    user_service = UserService(session)

    assert user_service

    new_user = await user_service.create_user(
        UserIn(
            name='User Name',
            email='testuser@example.com',
            password='Pass12345',
        )
    )

    assert new_user
    assert new_user.id


@pytest.mark.asyncio()
async def test_user_service_email_in_use(session):
    user_service = UserService(session)

    assert user_service

    await user_service.create_user(
        UserIn(
            name='User Name',
            email='testuser@example.com',
            password='Pass12345',
        )
    )

    with pytest.raises(exc.BadRequestException):
        await user_service.create_user(
            UserIn(
                name='User Name',
                email='testuser@example.com',
                password='Pass12345',
            )
        )


@pytest.mark.asyncio()
async def test_user_service_update_user(session):
    user_service = UserService(session)

    assert user_service

    new_user = await user_service.create_user(
        UserIn(
            name='User Name',
            email='testuser@example.com',
            password='Pass12345',
        )
    )

    assert new_user
    assert new_user.id

    updated_user = await user_service.update_user(
        user_id=new_user.id,
        current_user=new_user,
        data=UserUpdate(
            name='Updated Name',
        ),
    )

    assert updated_user


@pytest.mark.asyncio()
async def test_user_service_not_allowed_to_update_user(session):
    user_service = UserService(session)

    assert user_service

    new_user = await user_service.create_user(
        UserIn(
            name='User Name',
            email='testuser@example.com',
            password='Pass12345',
        )
    )

    assert new_user
    assert new_user.id

    with pytest.raises(exc.UnauthorizedException):
        await user_service.update_user(
            user_id=new_user.id + 1,
            current_user=new_user,
            data=UserUpdate(
                name='Updated Name',
            ),
        )


@pytest.mark.asyncio()
async def test_user_service_delete_user(session):
    user_service = UserService(session)

    assert user_service

    new_user = await user_service.create_user(
        UserIn(
            name='User Name',
            email='testuser@example.com',
            password='Pass12345',
        )
    )

    assert new_user
    assert new_user.id

    await user_service.delete_user(
        user_id=new_user.id,
        current_user=new_user,
    )

    assert not await user_service.repository.get_by_id(new_user.id)


@pytest.mark.asyncio()
async def test_user_service_not_allowed_to_delete_user(session):
    user_service = UserService(session)

    assert user_service

    new_user = await user_service.create_user(
        UserIn(
            name='User Name',
            email='testuser@example.com',
            password='Pass12345',
        )
    )

    assert new_user
    assert new_user.id

    with pytest.raises(exc.UnauthorizedException):
        await user_service.delete_user(
            user_id=new_user.id + 1,
            current_user=new_user,
        )
