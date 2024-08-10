
from sqlalchemy.ext.asyncio import AsyncSession
from auth.schemas import UserCreate
from auth.models import User


async def create_user(session: AsyncSession, user: UserCreate):
    new_user = User(username=user.username, password_hash=user.password, email=user.email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
