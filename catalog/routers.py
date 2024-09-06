from fastapi import APIRouter, Depends
from typing import Annotated
from core.dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from catalog.crud import get_rulers, get_types_moneys_for_ruler
from catalog.schemas import RulerSchema, TypeMoneySchema


router = APIRouter(prefix="/catalog", tags=['Catalog'])


@router.get('/rulers', response_model=list[RulerSchema])
async def rulers(session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_rulers(session=session)


@router.get('/rulers/{ruler_id}', response_model=list[TypeMoneySchema])
async def types_moneys_for_ruler(ruler_id: int,
                                 session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_types_moneys_for_ruler(ruler_id=ruler_id, session=session)
