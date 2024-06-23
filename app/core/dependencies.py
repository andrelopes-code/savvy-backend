from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.postgres import get_db

# Dependency that gets the database session in an async context
AsyncDBSessionDepends = Annotated[AsyncSession, Depends(get_db)]
