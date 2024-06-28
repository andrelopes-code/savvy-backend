from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class RecordIn(BaseModel):
    amount: int = Field(gt=0, strict=True)
    description: Annotated[str, Field(max_length=30)]
    date: datetime
    category_id: int


class CategoryOut(BaseModel):
    id: int
    name: str
    description: str | None


class RecordOut(BaseModel):
    id: int
    amount: int
    description: str
    date: datetime


class RecordWithCategoryOut(BaseModel):
    id: int
    amount: int
    description: str
    date: datetime
    category: CategoryOut
