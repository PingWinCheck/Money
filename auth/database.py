from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from settings import settings

DIALECT_DRIVER = 'postgresql+asyncpg'
engine = create_async_engine(url=f'{DIALECT_DRIVER}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}')

async_session_local = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
# async_session_local = sessionmaker(engine)

