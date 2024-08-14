from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException, status

from auth.dependences import get_session, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from auth.schemas import UserCreate, UserBase, Token
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from auth.crud import user_create
from auth.utils import check_password, gen_jwt, authenticate_user
from datetime import timedelta

router = APIRouter(prefix='/auth', tags=['auth'])
template = Jinja2Templates('auth/templates')


@router.post('/register', response_model=UserBase)
async def register(user: Annotated[UserCreate, Depends()], session: Annotated[AsyncSession, Depends(get_session)]):
    current_user = await user_create(session=session, user=user)
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


@router.get('/secret')
async def secret(user_id: Annotated[str, Depends(get_current_user)]):
    return user_id
