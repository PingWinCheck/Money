from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import async_session_local
from fastapi.security import OAuth2PasswordBearer

from auth.models import User
from auth.utils import check_jwt
from auth.crud import user_read


async def get_session() -> AsyncSession:
    async with async_session_local() as session:
        yield session


bearer_schema = OAuth2PasswordBearer('/auth/token')


async def get_current_user(token: Annotated[str, Depends(bearer_schema)]):
    payload = check_jwt(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='token expire',
                            headers={'WWW-Authenticate': 'Bearer'})
    sub = payload.get('sub')
    return sub


async def get_current_user_db(token: Annotated[str, Depends(bearer_schema)],
                              session: Annotated[AsyncSession, Depends(get_session)]):
    payload = check_jwt(token)
    print(f'{payload=}')
    if payload is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='token expire',
                            headers={'WWW-Authenticate': 'Bearer'})
    sub = payload.get('sub')
    current_user = await user_read(session=session, username=sub)
    print(current_user)
    return current_user
