from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.postgres import get_db
from app.core.sec import get_current_user, get_db_user
from app.models.user import User

# Dependency that gets the database session in an async context
AsyncDBSessionDepends = Annotated[AsyncSession, Depends(get_db)]
# Dependency login form data
LoginFormDataDepends = Annotated[OAuth2PasswordRequestForm, Depends()]
# Dependency that gets the current user from the token
AuthenticatedUserDepends = Annotated[dict, Depends(get_current_user)]
# Dependency that gets the current user from the database
AuthenticatedDBUserDepends = Annotated[User, Depends(get_db_user)]
