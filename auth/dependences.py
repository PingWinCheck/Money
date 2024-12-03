from typing import Annotated, Callable, TYPE_CHECKING, Union
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.exeptions import ex_incorrect_token
from core.dependencies import get_session
from fastapi.security import OAuth2PasswordBearer

from auth.models import User
from auth.utils import check_jwt
from auth.crud import user_read
from auth.dao import UserDAO


if TYPE_CHECKING:
    from auth.permissions import PermissionEnum

bearer_schema = OAuth2PasswordBearer('/auth/token')


async def get_current_payload_in_token(token: Annotated[str, Depends(bearer_schema)]):
    payload = check_jwt(token)
    return payload


async def get_current_user_db(token: Annotated[str, Depends(bearer_schema)],
                              session: Annotated[AsyncSession, Depends(get_session)],
                              ) -> User:
    payload = check_jwt(token)
    # TODO: запрет на доступ, через рефреш токен, посредством проверки на наличие jti, вероятно нужно будет переписать, на более очевидный способ
    if payload.get('jti'):
        raise ex_incorrect_token
    sub = payload.get('sub')
    # current_user = await user_read(session=session, username=sub)
    current_user = await UserDAO.get_user_with_roles_permissions(session=session, user_id=sub)
    if current_user is None:
        raise HTTPException(status_code=403,
                            detail='Не удалось идентифицировать вас, возможно ваша учетная запись удалена')
    return current_user


async def get_active_current_user(current_user: Annotated[User, Depends(get_current_user_db)]) -> User:
    if current_user.is_active is True:
        return current_user
    raise HTTPException(status_code=403,
                        detail='Ваша учетная запись не активна, либо удалена')


def check_permission(permission: Union["PermissionEnum", str]) -> Callable:
    async def permission_checker(current_user: Annotated[User, Depends(get_active_current_user)]) -> User:
        user_permission_list = [permission_.name for role in current_user.roles for permission_ in role.permissions]
        if permission not in user_permission_list:
            raise HTTPException(status_code=403,
                                detail='Доступ запрещен, у вас нет необходимых прав')
        return current_user
    return permission_checker
