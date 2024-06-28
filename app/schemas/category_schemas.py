from pydantic import BaseModel, Field


class CategoryOut(BaseModel):
    id: int
    name: str = Field(min_length='3', max_length=16)
    description: str | None = Field(default=None, max_length=50)


class CategoryIn(BaseModel):
    name: str = Field(min_length='3', max_length=16)
    description: str | None = Field(default=None, max_length=50)
