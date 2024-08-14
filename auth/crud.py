from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from auth.schemas import UserCreate
from auth.models import User


async def user_create(session: AsyncSession, user: UserCreate):
    from auth.utils import gen_password_hash
    password_hash = gen_password_hash(user.password)
    new_user = User(username=user.username, password_hash=password_hash, email=user.email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def user_read(session: AsyncSession, username: str):
    current_user = await session.execute(select(User).where(User.username == username))
    return current_user.scalar()
