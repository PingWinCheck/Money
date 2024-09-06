from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from settings import settings

DIALECT_DRIVER = 'postgresql+asyncpg'
engine = create_async_engine(url=f'{DIALECT_DRIVER}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}',
                             echo=True)

async_session_local = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


class Base(DeclarativeBase):
    pass
