from typing import Annotated
from uuid import UUID

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, Request, HTTPException, status, Form
from sqlalchemy.exc import IntegrityError

from auth.dependences import get_session, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import UserCreate, UserBase, Token
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from auth.crud import user_create, user_read, user_update_password
from auth.utils import check_password, gen_jwt, authenticate_user
import secrets
from datetime import timedelta

router = APIRouter(prefix='/auth', tags=['auth'])
template = Jinja2Templates('auth/templates')


@router.post('/register', response_model=UserBase)
async def register(user: Annotated[UserCreate, Depends()], session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        current_user = await user_create(session=session, user=user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User is already exists')
    return current_user


# frontend
@router.get('/login')
async def reg(request: Request):
    return template.TemplateResponse(request, 'login.html')


@router.post('/token', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: Annotated[AsyncSession, Depends(get_session)]):
    current_user = await authenticate_user(form_data, session)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid login or password',
                            headers={'WWW-Authenticate': 'Bearer'})
    payload = {'sub': current_user.username,
               'id': str(current_user.id),
               'email': current_user.email}
    token = gen_jwt(payload=payload)
    return Token(access_token=token)


@router.get('/user/{username}', response_model=UserBase)
async def secret(username: str,
                 user_id: Annotated[str, Depends(get_current_user)],
                 session: Annotated[AsyncSession, Depends(get_session)]):
    user = await user_read(session=session, username=username)
    return user


@router.put('/user/{username}', response_model=UserBase)
async def change_password(username: str,
                          old_password: Annotated[str, Form()],
                          new_password: Annotated[str, Form()],
                          current_user: Annotated[str, Depends(get_current_user)],
                          session: Annotated[AsyncSession, Depends(get_session)]):
    if not secrets.compare_digest(username, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='У вас нет доступа к чужому аккаунту')
    try:
        user = await user_update_password(session=session,
                                          username=username,
                                          new_password=new_password,
                                          old_password=old_password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'{e}')
    return user

