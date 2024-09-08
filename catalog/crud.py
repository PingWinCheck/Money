from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, desc, and_
from sqlalchemy.orm import joinedload, selectinload
from auth.models import User
from catalog.models import Ruler, TypeMoney, Money, MoneyForUser


async def get_rulers(session: AsyncSession) -> list[Ruler]:
    stmt = select(Ruler).order_by(Ruler.start_year)
    result: Result = await session.execute(stmt)
    return list(result.scalars())


async def get_types_moneys_for_ruler(ruler_id: int,
                                     session: AsyncSession) -> list[TypeMoney]:
    stmt = (select(TypeMoney).options(joinedload(TypeMoney.ruler))
            .where(TypeMoney.ruler_id == ruler_id))
    result: Result = await session.execute(stmt)
    return list(result.scalars())


async def get_money_for_type_unique(type_id: int,
                                    session: AsyncSession) -> list[Money]:
    stmt = (select(Money).options(joinedload(Money.type_money),
                                  joinedload(Money.type_money).options(joinedload(TypeMoney.ruler)))
            .where(Money.type_money_id == type_id).distinct(Money.title))
    result: Result = await session.execute(stmt)
    return list(result.scalars())


async def get_current_money_all_year(money_id: int,
                                     money_type_id: int,
                                     session: AsyncSession) -> list[Money]:
    stmt1 = (select(Money).where(Money.id == money_id))
    result1 = await session.execute(stmt1)
    current_money = result1.scalar()
    stmt = (select(Money).options(joinedload(Money.type_money),
                                  joinedload(Money.type_money).options(joinedload(TypeMoney.ruler)))
            .where(and_(Money.type_money_id == money_type_id, Money.title == current_money.title)))
    result = await session.execute(stmt)
    return list(result.scalars())


async def add_money_in_current_user(user_id: UUID,
                                    money_id: int,
                                    session: AsyncSession):
    # new_entry = MoneyForUser(user_id=user_id, money_id=money_id)
    # session.add(new_entry)
    # await session.commit()
    # await session.refresh(new_entry)
    stmt = (select(User).options(selectinload(User.moneys)).where(User.id == user_id))

    current_user = await session.scalar(stmt)
    current_money = await session.scalar(select(Money).where(Money.id == money_id))
    current_user.moneys.append(current_money)
    await session.commit()
    # await session.refresh(current_user)
    return current_user


async def get_all_money_current_user(user_id: UUID,
                                     session: AsyncSession) -> User:
    stmt = (select(User)
            .options(selectinload(User.moneys))
            # .options(selectinload(User.moneys).options(selectinload(Money.type_money)))
            .options(selectinload(User.moneys).options(selectinload(Money.type_money).options(selectinload(TypeMoney.ruler))))
            .where(User.id == user_id))
    result = await session.scalar(stmt)
    return result
