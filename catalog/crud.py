from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, desc, and_, func
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from auth.models import User
from catalog.models import Ruler, TypeMoney, Money, MoneyForUser


# async def get_rulers(session: AsyncSession) -> list[Ruler]:
#     stmt = select(Ruler).order_by(Ruler.start_year)
#     result: Result = await session.execute(stmt)
#     return list(result.scalars())


async def get_rulers_v2(session: AsyncSession,
                        offset: int,
                        limit: int):
    stmt = (select(Ruler).order_by(Ruler.start_year).limit(limit).offset(offset))
    result = await session.scalars(stmt)
    return list(result)


# async def get_count_all_rulers(session: AsyncSession):
#     stmt = (select(func.count(Ruler.id)))
#     return await session.scalar(stmt)


async def get_total_count_for_ruler(session: AsyncSession):
    stmt = (select(func.count(Ruler.id)))
    return await session.scalar(stmt)


async def get_types_moneys_for_ruler(ruler_id: int,
                                     session: AsyncSession) -> list[TypeMoney]:
    stmt = (select(TypeMoney).options(joinedload(TypeMoney.ruler))
            .where(TypeMoney.ruler_id == ruler_id))
    result: Result = await session.execute(stmt)
    return list(result.scalars())


async def get_ruler_with_type_money_list(ruler_id: int,
                                         session: AsyncSession):
    stmt = (select(Ruler).options(selectinload(Ruler.type_moneys))).where(Ruler.id == ruler_id)
    return await session.scalar(stmt)


async def get_ruler_with_type_with_money_list(ruler_id: int,
                                              type_id: int,
                                              session: AsyncSession):
    # stmt_sub = (select(TypeMoney.ruler_id).where(TypeMoney.id == type_id).subquery())
    # stmt = (select(Ruler).options(selectinload(Ruler.type_moneys))
    #         .where(Ruler.id == ruler_id, Ruler.id.in_(stmt_sub)))

    stmt = (select(Ruler).options(contains_eager(Ruler.type_moneys).options(selectinload(TypeMoney.moneys)))
            .where(Ruler.id == ruler_id, TypeMoney.id == type_id, TypeMoney.ruler_id == ruler_id))
    return await session.scalar(stmt)


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
