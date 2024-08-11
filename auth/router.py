from typing import Annotated
from fastapi import APIRouter, Depends, Request

from auth.dependences import get_session, bearer_schema
from auth.schemas import UserCreate, UserBase
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from auth.crud import user_create


router = APIRouter(prefix='/auth', tags=['auth', 'user'])
template = Jinja2Templates('auth/templates')


@router.post('/register', response_model=UserBase)
async def register(user: Annotated[UserCreate, Depends()], session: Annotated[AsyncSession, Depends(get_session)]):
    current_user = await user_create(session=session, user=user)
    return current_user


# frontend
@router.get('/login')
async def reg(request: Request):
    return template.TemplateResponse(request, 'login.html')


@router.post('/login')
async def login():
    pass


@router.get('/test')
async def test(token: Annotated[str, Depends(bearer_schema)]):
    return 'ok'
