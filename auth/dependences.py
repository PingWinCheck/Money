from typing import Annotated
from fastapi import Depends, HTTPException, status
from auth.database import async_session_local
from fastapi.security import OAuth2PasswordBearer
from auth.utils import check_jwt


async def get_session():
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
