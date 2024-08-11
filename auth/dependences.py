from auth.database import async_session_local
from fastapi.security import OAuth2PasswordBearer


async def get_session():
    async with async_session_local() as session:
        yield session


bearer_schema = OAuth2PasswordBearer('/auth/login')