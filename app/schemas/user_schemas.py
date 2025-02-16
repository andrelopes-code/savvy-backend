from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from .custom_types import Password


class UserFields:
    name = Annotated[str, Field(max_length=20)]
    email = Annotated[EmailStr, ...]
    password = Annotated[
        Password,
        Field(
            description='Must contain at least one number and one uppercase'
            'and lowercase letter, and at least 8 or more characters',
        ),
    ]
    categories_count = Annotated[int, ...]


class UserIn(BaseModel):
    name: UserFields.name
    email: UserFields.email
    password: UserFields.password


class UserOut(BaseModel):
    id: int
    name: UserFields.name
    email: UserFields.email
    created_at: datetime
    updated_at: datetime
    categories_count: UserFields.categories_count


class UserUpdate(BaseModel):
    name: UserFields.name
