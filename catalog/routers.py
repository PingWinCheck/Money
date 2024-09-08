from fastapi import APIRouter, Depends, Form
from typing import Annotated

from auth.models import User
from core.dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from catalog.crud import (get_rulers, get_types_moneys_for_ruler, get_money_for_type_unique, get_current_money_all_year,
                          add_money_in_current_user, get_all_money_current_user)
from catalog.schemas import RulerSchema, TypeMoneySchema, MoneySchema, MoneySchemaExcludeYear, MoneyFromTheUser
from auth.dependences import get_current_user_db


router = APIRouter(prefix="/catalog", tags=['Catalog'])


@router.get('/rulers', response_model=list[RulerSchema])
async def rulers(session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_rulers(session=session)


@router.get('/rulers/{ruler_id}', response_model=list[TypeMoneySchema])
async def types_moneys_for_ruler(ruler_id: int,
                                 session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_types_moneys_for_ruler(ruler_id=ruler_id, session=session)


@router.get('/types/{type_id}', response_model=list[MoneySchemaExcludeYear])
async def money_for_type_for_ruler(type_id: int,
                                   session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_money_for_type_unique(type_id=type_id, session=session)


@router.get('/types/{type_id}/{money_id}', response_model=list[MoneySchema])
async def current_money_all_year(type_id: int,
                                 money_id: int,
                                 session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_current_money_all_year(money_id=money_id, money_type_id=type_id, session=session)


@router.post('/add_money_me')
async def add_money_me(current_user: Annotated[User, Depends(get_current_user_db)],
                       money_id: Annotated[int, Form()],
                       session: Annotated[AsyncSession, Depends(get_session)]):
    return await add_money_in_current_user(user_id=current_user.id, money_id=money_id, session=session)


@router.get('/my_catalog', response_model=MoneyFromTheUser)
async def my_catalog(current_user: Annotated[User, Depends(get_current_user_db)],
                     session: Annotated[AsyncSession, Depends(get_session)]):
    res = await get_all_money_current_user(user_id=current_user.id, session=session)
    return res


