from typing import Optional, Sequence, Union
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import log


class AsyncCRUDRepository[T]:
    """An async BASE repository for CRUD operations"""

    def __init__(self, session: AsyncSession, model: T):
        """Initialize the repository

        Args:
            session (AsyncSession): The database session.
            model (T): The database model class related to the repository.
        """
        self.session = session
        self.model = model

    async def save(self, instance: T) -> T:
        """Save an instance of the model in the database

        Args:
            instance (T): The instance to be saved.

        Returns:
            T: The saved instance.
        """
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_all(self, stmt=None) -> Sequence[T]:
        """Get all instances of the model

        Args:
            stmt (Optional[Select], optional): The statement to be executed.
            Defaults to None.

        Returns:
            Sequence[T]: A list of all instances.
        """
        if stmt is None:
            stmt = select(self.model)

        scalar_result = await self.session.scalars(stmt)
        instances = scalar_result.all()
        return instances

    async def get_by_id(self, pk: UUID | int) -> Optional[T]:
        """Get an instance by its id

        Args:
            pk (UUID | int): The id of the instance.

        Returns:
            Optional[T]: The instance or None if not found.
        """
        stmt = select(self.model).where(self.model.id == pk)
        instance = await self.session.scalar(stmt)
        return instance

    async def delete_by_id(self, pk: UUID | int) -> Optional[T]:
        """Delete an instance by its id

        Args:
            pk (UUID | int): The id of the instance.

        Returns:
            Optional[T]: The deleted instance or None if not found.
        """
        instance = await self.get_by_id(pk)
        if not instance:
            return None

        await self.session.delete(instance)
        await self.session.commit()
        return instance

    async def update_by_id(
        self, pk: UUID | int, data: Union[dict, BaseModel]
    ) -> Union[None, T]:
        """Update an instance by its id

        Args:
            pk (UUID | int): The id of the instance.
            data (Union[dict, BaseModel]): The data to be updated. Needs to
            be a dictionary or a Pydantic model.

        Returns:
            Union[None, T]: The updated instance or None if not found.
        """
        instance = await self.get_by_id(pk)
        if not instance:
            return None

        return await self.update(instance, data)

    async def update(self, instance: T, data: Union[dict, BaseModel]) -> T:
        """Update an instance

        Args:
            instance (T): The instance to be updated.
            data (Union[dict, BaseModel]): The data to be updated. Needs to
            be a dictionary or a Pydantic model.

        Returns:
            T: The updated instance.
        """
        AsyncCRUDRepository.update_instance_fields(instance, data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    @staticmethod
    def update_instance_fields(model: T, data: Union[dict, BaseModel]):
        """Update the fields of an instance

        Args:
            model (T): The instance to be updated.
            data (Union[dict, BaseModel]): The data to be updated. Needs to
            be a dictionary or a Pydantic model.
        """
        if isinstance(data, dict):
            for field, value in data.items():
                if hasattr(model, field) and value is not None:
                    setattr(model, field, value)

        elif isinstance(data, BaseModel):
            for field, value in data:
                if hasattr(model, field) and value is not None:
                    setattr(model, field, value)
        else:
            log.exception(f'Invalid data type updating model: {type(data)}')
            raise TypeError(
                f'Invalid data type: {type(data)}. Expected dict or BaseModel.'
            )


class AsyncCRUDRepositoryWithEmail[T](AsyncCRUDRepository[T]):
    """async CRUD repository with email methods"""

    def __init__(self, session: AsyncSession, model: T):
        """Initialize the repository

        Args:
            session (AsyncSession): The database session.
            model (T): The database model class related to the repository.
        """
        super().__init__(session, model)

    async def get_by_email(self, email: str, stmt=None) -> Optional[T]:
        """Get an instance by its email

        Args:
            email (str): The email of the instance.
            stmt (Optional[Select]): The statement to be executed.
            Defaults to None.

        Returns:
            Optional[T]: The instance or None if not found.
        """
        if stmt is None:
            stmt = select(self.model).where(self.model.email == email)

        instance = await self.session.scalar(stmt)
        return instance

    async def delete_by_email(self, email: str) -> Optional[T]:
        """Delete an instance by its email

        Args:
            email (str): The email of the instance.
        Returns:
            Optional[T]: The deleted instance or None if not found.
        """
        instance = await self.get_by_email(email)
        if not instance:
            return None

        await self.session.delete(instance)
        await self.session.commit()
        return instance
