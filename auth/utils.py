import uuid
from typing import Any
from datetime import timedelta, timezone, datetime

import bcrypt
import jwt
from fastapi import HTTPException, status
from jwt.exceptions import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from auth.models import User
from auth.schemas import UserCreate
from auth.crud import user_read
from settings import settings
from auth.redis import redis_client
from auth.dao import UserDAO


def gen_password_hash(password: str) -> str:
    password_hash = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    return password_hash.decode()


def check_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=password_hash.encode())


def gen_jwt(payload: dict[str, Any],
            expire: timedelta) -> str:
    payload = payload.copy()
    now = datetime.now(timezone.utc)
    payload['exp'] = now + expire
    token = jwt.encode(payload=payload, key=settings.private_key, algorithm='RS256')
    return token


def check_jwt(token: str) -> dict | None:
    try:
        payload: dict[str, Any] = jwt.decode(jwt=token, key=settings.public_key, algorithms=['RS256'])
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='invalid token',
                            headers={'WWW-Authenticate': 'Bearer'})
    return payload


async def authenticate_user(form_data: OAuth2PasswordRequestForm, session: AsyncSession) -> User | None:
    # current_user = await user_read(session=session, username=form_data.username)
    current_user = await UserDAO.get_one_or_none_item_by_filter(session=session, username=form_data.username)
    if current_user is None:
        return None
    if not check_password(form_data.password, current_user.password_hash):
        return None
    return current_user


async def generate_jti_and_add_or_update_redis(user: str, expire_seconds: int, old_jti: str | None = None) -> str:
    jti = str(uuid.uuid4())
    redis_client.set(jti, user, ex=expire_seconds)
    if old_jti:
        redis_client.delete(old_jti)
    return jti


async def check_jti_in_redis(jti: str):
    if redis_client.get(jti):
        return True
