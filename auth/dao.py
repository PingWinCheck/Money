from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, selectinload

from core.dao import BaseDAO
from auth.models import User, Role, Permission


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def swap_activate(cls, user_id: UUID, session: AsyncSession) -> User | None:
        stmt = (select(cls.model).filter_by(id=user_id))
        user = await session.scalar(stmt)
        if user:
            user.is_active = not user.is_active
            await session.commit()
            await session.refresh(user)
        return user

    @classmethod
    async def get_user_with_roles_permissions(cls, user_id: UUID, session: AsyncSession):
        stmt = (select(cls.model).filter_by(id=user_id).options(selectinload(cls.model.roles)
                                                                .options(selectinload(Role.permissions))))
        user = await session.scalar(stmt)
        return user


