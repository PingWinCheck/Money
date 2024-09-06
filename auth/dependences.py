from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session
from fastapi.security import OAuth2PasswordBearer

from auth.models import User
from auth.utils import check_jwt
from auth.crud import user_read

bearer_schema = OAuth2PasswordBearer('/auth/token')


async def get_current_payload_in_token(token: Annotated[str, Depends(bearer_schema)]):
    payload = check_jwt(token)
    return payload


async def get_current_user_db(token: Annotated[str, Depends(bearer_schema)],
                              session: Annotated[AsyncSession, Depends(get_session)],
                              ) -> User:
    payload = check_jwt(token)
    sub = payload.get('sub')
    current_user = await user_read(session=session, username=sub)
    return current_user
