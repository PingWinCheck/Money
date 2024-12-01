from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def get_one_or_none_item_by_id(cls, session: AsyncSession, id_: int) -> Optional[model]:
        stmt = (select(cls.model).filter_by(id=id_))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all_items(cls, session: AsyncSession) -> list[Optional[model]]:
        stmt = (select(cls.model))
        return list(await session.scalars(stmt))

    @classmethod
    async def get_all_items_with_offset_and_limit(cls, session: AsyncSession,
                                                  offset: int,
                                                  limit: int) -> list[Optional[model]]:
        stmt = (select(cls.model).offset(offset).limit(limit))
        return list(await session.scalars(stmt))

    @classmethod
    async def get_one_or_none_item_by_filter(cls, session: AsyncSession, **filter_by) -> Optional[model]:
        stmt = (select(cls.model).filter_by(**filter_by))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def create_item(cls, session: AsyncSession, **data) -> model:
        _new_instance = cls.model(**data)
        session.add(_new_instance)
        await session.commit()
        await session.refresh(_new_instance)
        return _new_instance


    # @classmethod
    # async def update_item_by_id(cls, session: AsyncSession, model_id: int, **data):
    #     stmt = (update(cls.model).filter_by(id=model_id).values(**data))
    #     try:
    #         await session.execute(stmt)
    #         await session.commit()
    #         return True
    #     except Exception as e:
    #         print(f'{e=}')
    #         await session.rollback()
    #         return False

