import math
from time import sleep

from fastapi import APIRouter, Depends, Form, HTTPException, status, Response, Query
from typing import Annotated

from auth.models import User
from catalog.models import Ruler, TypeMoney
from core.dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from catalog.crud import (get_types_moneys_for_ruler, get_money_for_type_unique, get_current_money_all_year,
                          add_money_in_current_user, get_all_money_current_user, get_ruler_with_type_money_list,
                          get_ruler_with_type_with_money_list, get_rulers_v2,
                          get_total_count_for_ruler)
from catalog.schemas import RulerSchema, TypeMoneySchema, MoneySchema, MoneySchemaExcludeYear, MoneyFromTheUser
from auth.dependences import get_current_user_db


router = APIRouter(prefix="/catalog", tags=['Catalog'])
router_v2 = APIRouter(prefix='/v2/catalog', tags=['Catalog'])


# @router.get('/rulers', response_model=list[RulerSchema])
# async def rulers(session: Annotated[AsyncSession, Depends(get_session)]):
#     return await get_rulers(session=session)


@router_v2.get('/rulers')
async def rulers_v2(session: Annotated[AsyncSession, Depends(get_session)],
                    page: Annotated[int, Query(ge=1)] = 1,
                    limit: Annotated[int, Query(ge=1)] = 3):
    offset = -limit + page * limit
    # total_items = await get_count_all_rulers(session=session)
    total_items = await get_total_count_for_ruler(session=session)

    result = await get_rulers_v2(session=session, offset=offset, limit=limit)
    total_page = math.ceil(total_items / limit)
    sleep(1)
    if result:
        return {'total_items': total_items,
                'items_per_page': limit,
                'current_page': page,
                'total_pages': total_page,
                'data': result}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='data is null')


# @router.get('/rulers/{ruler_id}', response_model=list[TypeMoneySchema])
# async def types_moneys_for_ruler(ruler_id: int,
#                                  session: Annotated[AsyncSession, Depends(get_session)]):
#     return await get_types_moneys_for_ruler(ruler_id=ruler_id, session=session)


@router_v2.get('/rulers/{ruler_id}')
async def get_ruler_with_type_money(ruler_id: int,
                                    session: Annotated[AsyncSession, Depends(get_session)],
                                    # page: int = 1,
                                    # limit: int = 3
                                    ):
    sleep(2)
    total_items = await get_total_count_for_ruler(session=session)
    # total_page = math.ceil(total_items / limit)
    result = await get_ruler_with_type_money_list(ruler_id=ruler_id, session=session)
    if result:
        return {'total_items': total_items,
                'data': result}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Страница не найдена')


@router.get('/v2/ruler/{ruler_id}/type/{type_id}')
async def ruler_with_type_with_money(ruler_id: int,
                                     type_id: int,
                                     session: Annotated[AsyncSession, Depends(get_session)]):
    result = await get_ruler_with_type_with_money_list(ruler_id=ruler_id, type_id=type_id, session=session)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Страница не найдена')


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


