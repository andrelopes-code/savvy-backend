import asyncio
import random
import string
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.postgres import async_session
from app.models.category import Category
from app.models.record import Record
from app.models.user import User


async def init_db():
    async with async_session() as session:
        await add_admin_user_and_records(session)


async def add_admin_user_and_records(session: AsyncSession):
    user = await create_admin_user(session)
    await add_admin_records(session, user)


# Create admin user
async def create_admin_user(session: AsyncSession):
    user = User(
        name='Admin',
        email='admin@admin.org',
        password='Pass12345',
    )
    result = await session.execute(
        select(User).where(User.email == user.email)
    )
    user_exists = result.scalar()
    if user_exists is not None:
        return user_exists

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


# Add admin records
async def add_admin_records(session: AsyncSession, user: User):
    result = await session.scalars(select(Category))
    categories = result.all()

    session.add_all([
        Record(
            description=''.join(
                random.choice(string.ascii_letters)
                for _ in range(random.randint(10, 30))
            ),
            category_id=random.choice(categories).id,
            amount=random.randint(1, 1000),
            date=datetime.now(timezone.utc),
            user_id=user.id,
        )
        for _ in range(20)
    ])
    await session.commit()


if __name__ == '__main__':
    asyncio.run(init_db())
