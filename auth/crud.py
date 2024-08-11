from sqlalchemy.ext.asyncio import AsyncSession
from auth.schemas import UserCreate
from auth.models import User
from auth.utils import gen_password_hash


async def user_create(session: AsyncSession, user: UserCreate):
    password_hash = gen_password_hash(user.password)
    new_user = User(username=user.username, password_hash=password_hash, email=user.email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

