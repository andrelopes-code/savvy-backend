from sqlalchemy import event

from app.utils.functions import update_model_timestamp

from .base import Base
from .category import Category
from .record import Record
from .user import User

# Event listeners for models
event.listen(User, 'before_update', update_model_timestamp)

__all__ = ['Base', 'User', 'Record', 'Category']
