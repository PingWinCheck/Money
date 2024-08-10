from typing import Annotated
from fastapi import APIRouter, Form, Depends, Body, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import UserCreate, UserCreate1
from fastapi.templating import Jinja2Templates
from auth.database import async_session_local
from sqlalchemy.ext.asyncio import AsyncSession
from auth.crud import create_user


router = APIRouter(prefix='/auth', tags=['auth', 'user'])
template = Jinja2Templates('auth/templates')


async def get_session():
    async with async_session_local() as session:
        yield session


@router.post('/register')
async def register(user: Annotated[UserCreate, Depends()], session: Annotated[AsyncSession, Depends(get_session)]):
    current_user = await create_user(session=session, user=user)
    return current_user


# frontend
@router.get('/login')
async def reg(request: Request):
    return template.TemplateResponse(request, 'login.html')
