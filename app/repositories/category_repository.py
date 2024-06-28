from app.models.category import Category

from .base_repository import AsyncCRUDRepository


class CategoryRepository(AsyncCRUDRepository[Category]):
    def __init__(self, session):
        super().__init__(session, Category)
