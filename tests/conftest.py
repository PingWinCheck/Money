import asyncio

import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.dependencies import get_session
from main import app
from settings import settings


@pytest_asyncio.fixture(scope="session")
async def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def connect_db_and_dependency_overrides():
    async_test_engine = create_async_engine(f'postgresql+asyncpg://{settings.test_db_user}:{settings.test_db_password}@{settings.test_db_host}:{settings.test_db_port}/{settings.test_db_name}')
    async_test_session = async_sessionmaker(async_test_engine, autoflush=False, expire_on_commit=False)

    async def get_test_session() -> AsyncSession:
        async with async_test_session() as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session


@pytest_asyncio.fixture(scope='session', autouse=True)
async def alembic_migrate():
    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('test', 'True')
    command.upgrade(alembic_cfg, 'head')
    yield
    command.downgrade(alembic_cfg, 'base')


@pytest_asyncio.fixture(scope="session")
async def client_async():
    async with AsyncClient(base_url='http://localhost:8000', transport=ASGITransport(app=app)) as client:
        yield client
