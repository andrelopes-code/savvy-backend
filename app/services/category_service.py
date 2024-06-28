from sqlalchemy import or_, select

from app.core import exc
from app.models.category import Category
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schemas import CategoryIn


class CategoryService:
    def __init__(self, session, user: User):
        self.user = user
        self.session = session
        self.max_categories_count = 5
        self.repository = CategoryRepository(session)

    async def create_category(self, data: CategoryIn) -> Category:
        # Check if the user has reached the max categories count
        if self.user.categories_count >= self.max_categories_count:
            raise exc.ForbiddenException('Max categories reached')
        # Increment the user's categories count
        self.user.categories_count += 1
        self.session.add(self.user)
        # Create the category and return it
        category = Category(**data.model_dump(), user_id=self.user.id)
        created_category = await self.repository.save(category)
        return created_category

    async def get_categories(self) -> list[Category]:
        # Get all categories that belong to the user or
        # categories that do not belong to any user (public categories)
        stmt = select(Category).where(
            or_(
                Category.user_id.is_(None),
                Category.user_id == self.user.id,
            )
        )
        categories = await self.repository.get_all(stmt)
        return categories

    async def delete_category(self, category_id: int) -> Category:
        category = await self._validate_category(category_id)
        # Decrement the user's categories count
        self.user.categories_count -= 1
        self.session.add(self.user)
        # Delete the category and return it
        await self.repository.delete_instance(category)
        return category

    async def _validate_category(self, category_id: int) -> Category:
        """Check if the category exists and belongs to the user"""
        category = await self.repository.get_by_id(category_id)
        if not category or category.user_id != self.user.id:
            raise exc.NotFoundException(
                'Category not found or invalid for this user'
            )
        return category
