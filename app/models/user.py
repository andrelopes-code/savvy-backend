from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.sec import SecurityService

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=True, index=True, unique=True
    )
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        default=datetime.now(timezone.utc),
    )

    @validates('password')
    def _validate(_, key, password):
        """Ensures that the password will be hashed"""
        return SecurityService.get_password_hash(password)

    def verify_password(self, plain_password):
        """Check if password matches the hash"""
        return SecurityService.verify_password(plain_password, self.password)
