import uuid
from typing import Annotated, Optional
from uuid import UUID

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, Request, HTTPException, status, Form, BackgroundTasks
from sqlalchemy.exc import IntegrityError

from auth.dependences import get_current_payload_in_token, get_current_user_db, bearer_schema
from auth.mail_service.sender_messages import send_message_verification_mail
from core.dependencies import get_session
from fastapi.security import OAuth2PasswordRequestForm

from auth.models import User
from auth.schemas import UserCreate, UserBase, Token
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from auth.crud import user_create, user_read, user_update_password, user_delete, verification_mail_true, \
    user_read_with_id
from auth.utils import (check_password, gen_jwt, authenticate_user, generate_jti_and_add_or_update_redis,
                        check_jti_in_redis)
import secrets
from datetime import timedelta
from settings import settings
from auth.redis import redis_client
from auth.dao import UserDAO
from auth.utils import gen_password_hash
from auth.exeptions import ex_user_is_already, ex_invalid_login_or_password

router = APIRouter(prefix='/auth', tags=['auth'])
template = Jinja2Templates('auth/templates')


# @router.post('/register', response_model=UserBase)
# async def register(user: Annotated[UserCreate, Depends()], session: Annotated[AsyncSession, Depends(get_session)]):
#     try:
#         current_user = await user_create(session=session, user=user)
#     except IntegrityError:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail='User or email is already exists')
#     return current_user

@router.post('/register', response_model=UserBase, responses={409: {'description': ex_user_is_already.detail}})
async def register(user: Annotated[UserCreate, Depends()], session: Annotated[AsyncSession, Depends(get_session)]):
    password_hash = gen_password_hash(user.password)
    already_exists = await UserDAO.get_one_or_none_item_by_filter(session=session,
                                                                  username=user.username)
    if already_exists:
        raise ex_user_is_already
    current_user = await UserDAO.create_item(session=session,
                                             username=user.username,
                                             email=user.email,
                                             password_hash=password_hash)
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
        raise ex_invalid_login_or_password
    payload_access = {'sub': current_user.username,
                      'id': str(current_user.id),
                      'email': current_user.email}
    access_token = gen_jwt(payload=payload_access,
                           expire=timedelta(seconds=settings.expire_access_token_seconds))
    jti = await generate_jti_and_add_or_update_redis(user=current_user.username,
                                                     expire_seconds=settings.expire_refresh_token_seconds)
    payload_refresh = payload_access.copy()
    payload_refresh['jti'] = jti
    refresh_token = gen_jwt(payload=payload_refresh,
                            expire=timedelta(seconds=settings.expire_refresh_token_seconds))
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post('/refresh')
async def refresh(payload_current_token: Annotated[dict, Depends(get_current_payload_in_token)]) -> Token:
    if not payload_current_token.get('jti') or not await check_jti_in_redis(payload_current_token.get('jti')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='invalid token',
                            headers={'WWW-Authenticate': 'Bearer'})

    jti = await generate_jti_and_add_or_update_redis(user=payload_current_token['sub'],
                                                     expire_seconds=settings.expire_refresh_token_seconds,
                                                     old_jti=payload_current_token['jti'])
    payload_current_token['jti'] = jti
    refresh_token = gen_jwt(payload=payload_current_token,
                            expire=timedelta(seconds=settings.expire_refresh_token_seconds))
    payload_current_token.pop('jti')
    access_token = gen_jwt(payload=payload_current_token, expire=timedelta(seconds=settings.expire_access_token_seconds))
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get('/user/{username}',
            response_model=UserBase,
            responses={404: {'description': 'Пользователя с ником: {username} не существует'}}
            )
async def get_user(username: str,
                   # user_id: Annotated[str, Depends(get_current_user)],
                   session: Annotated[AsyncSession, Depends(get_session)]):
    # user = await user_read(session=session, username=username)
    user = await UserDAO.get_one_or_none_item_by_filter(session=session, username=username)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Пользователя с ником: {username} не существует')


@router.put('/my_profile', response_model=UserBase)
async def change_password(old_password: Annotated[str, Form()],
                          new_password: Annotated[str, Form()],
                          current_user: Annotated[User, Depends(get_current_user_db)],
                          session: Annotated[AsyncSession, Depends(get_session)]):
    # TODO переписать круд на дао
    try:
        user = await user_update_password(session=session,
                                          current_user=current_user,
                                          new_password=new_password,
                                          old_password=old_password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'{e}')
    return user


@router.delete('/user/{username}')
async def del_user(session: Annotated[AsyncSession, Depends(get_session)]):
    if await user_delete(session=session):
        return 'ok'
    return 'error'


@router.get('/my_profile', response_model=UserBase)
async def my_profile(user: Annotated[User, Depends(get_current_user_db)]):
    return user


@router.get('/confirm-mail/{token}')
async def confirm_mail_token(session: Annotated[AsyncSession, Depends(get_session)],
                             token: str):
    user_id = redis_client.get(token)
    if user_id:
        user_id = UUID(user_id.decode('utf-8'))
        # current_user = await user_read_with_id(session=session, user_id=user_id)
        current_user = await UserDAO.get_one_or_none_item_by_filter(session=session, user_id=user_id)
        await verification_mail_true(session=session, current_user=current_user)  # TODO переписать круд на дао
        redis_client.delete(token)
        return {'message': 'Почта подтверждена'}
    return {'message': 'Токена не существует'}


@router.get('/confirm-mail')
async def confirm_mail(user: Annotated[User, Depends(get_current_user_db)],
                       background_tasks: BackgroundTasks):
    background_tasks.add_task(send_message_verification_mail, user.email, user.id)
    return {'message': f'Для подтверждения почты, оправлено письмо к вам на почту {user.email}'}



