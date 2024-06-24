import pytest

from app.models import User


@pytest.mark.asyncio()
async def test_user_model_creation(session):
    user = User(
        name='André Lopes',
        email='andrelopes@gmail.com',
        password='Password123',
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.id


@pytest.mark.asyncio()
async def test_user_model_field_updated_at_is_updating(session):
    user = User(
        name='André Lopes',
        email='andrelopes@gmail.com',
        password='Password123',
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.id
    old_updated_at = user.updated_at

    user.name = 'Updated User'
    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.id
    assert user.updated_at != old_updated_at

    assert user.verify_password('Password123')


@pytest.mark.asyncio()
async def test_user_password_field_is_hashed(session):
    user = User(
        name='André Lopes',
        email='andrelopes@gmail.com',
        password='Password123',
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.password != 'Password123'
