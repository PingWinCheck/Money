from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload

from catalog.models import Ruler, TypeMoney


async def get_rulers(session: AsyncSession):
    stmt = select(Ruler)
    result: Result = await session.execute(stmt)
    return list(result.scalars())


async def get_types_moneys_for_ruler(ruler_id: int,
                                     session: AsyncSession):
    stmt = (select(TypeMoney).options(joinedload(TypeMoney.ruler))
            .where(TypeMoney.ruler_id == ruler_id))
    result: Result = await session.execute(stmt)
    return list(result.scalars())
