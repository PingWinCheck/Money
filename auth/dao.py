from sqlalchemy.ext.asyncio import AsyncSession

from core.dao import BaseDAO
from auth.models import User


class UserDAO(BaseDAO):
    model = User
