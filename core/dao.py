from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def get_one_or_none_item_by_id(cls, session: AsyncSession, model_id: int) -> Optional[model]:
        stmt = (select(cls.model).filter_by(id=model_id))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all_items(cls, session: AsyncSession) -> list[Optional[model]]:
        stmt = (select(cls.model))
        return list(await session.scalars(stmt))

    @classmethod
    async def get_one_or_none_item_by_filter(cls, session: AsyncSession, **filter_by) -> Optional[model]:
        stmt = (select(cls.model).filter_by(**filter_by))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def create_item(cls, session: AsyncSession, **data) -> model:
        new_instance = cls.model(**data)
        session.add(new_instance)
        await session.commit()
        await session.refresh(new_instance)
        return new_instance

