from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exc
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserIn, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = UserRepository(session)

    async def create_user(self, data: UserIn) -> User:
        user = User(**data.model_dump())

        # Check if email is already in use by another user
        if await self.email_in_use(user.email):
            raise exc.BadRequestException('Email already in use')
        # Create the user and return it
        created_user = await self.repository.save(user)
        return created_user

    async def update_user(
        self,
        user_id: int,
        current_user: User,
        data: UserUpdate,
    ) -> User:
        # Check if the current user is the one being updated
        if user_id != current_user.id:
            raise exc.UnauthorizedException('You cannot update this user')
        # Update the user and return it
        updated_user = await self.repository.update(current_user, data)
        return updated_user

    async def email_in_use(self, email: str) -> bool:
        """Check if an email is already in use

        Args:
            email (str): The email to be checked

        Returns:
            bool: True if email is in use, False otherwise
        """
        user = await self.repository.get_by_email(email)
        return True if user else False
