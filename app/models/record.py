from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Record(Base):
    __tablename__ = 'records'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[int] = mapped_column(nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    date: Mapped[datetime]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
