from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from core.dao import BaseDAO
from auth.models import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def deactivate(cls, user_id: UUID, session: AsyncSession) -> User | None:
        stmt = (select(cls.model).filter_by(id=user_id))
        user = await session.scalar(stmt)
        if user:
            if user.is_active:
                user.is_active = False
                await session.commit()
                await session.refresh(user)
        return user


