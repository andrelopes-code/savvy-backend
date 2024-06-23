from app.models.user import User

from .base_repository import AsyncCRUDRepositoryWithEmail, AsyncSession


class UserRepository(AsyncCRUDRepositoryWithEmail[User]):
    """User repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
