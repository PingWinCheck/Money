from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from auth.schemas import UserCreate
from auth.models import User


async def user_create(session: AsyncSession, user: UserCreate) -> User:
    from auth.utils import gen_password_hash

    password_hash = gen_password_hash(user.password)
    new_user = User(username=user.username, password_hash=password_hash, email=user.email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def user_read(session: AsyncSession, username: str) -> User:
    current_user = await session.execute(select(User).where(User.username == username))
    return current_user.scalar()


async def user_update_password(session: AsyncSession, username: str, new_password: str, old_password: str):
    from auth.utils import gen_password_hash, check_password
    current_user = await user_read(session=session, username=username)
    if not check_password(old_password, current_user.password_hash):
        raise ValueError('Старый пароль не верный')
    password_hash = gen_password_hash(new_password)
    current_user.password_hash = password_hash
    await session.commit()
    await session.refresh(current_user)
    return current_user

