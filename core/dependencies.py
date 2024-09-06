from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_local


async def get_session() -> AsyncSession:
    async with async_session_local() as session:
        yield session
