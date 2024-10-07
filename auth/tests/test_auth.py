from httpx import AsyncClient, ASGITransport
import pytest
from main import app
import pytest_asyncio
import asyncio


@pytest_asyncio.fixture(scope="module")
async def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(base_url='http://localhost:8000', transport=ASGITransport(app=app)) as client:
        yield client


@pytest.mark.asyncio
async def test_register(async_client):

    response = await async_client.post('/auth/register', data={'username': 'ivan',
                                                               "email": 'ivan@mail.com',
                                                               'password': 'qwerty'})
    assert response.status_code == 200
    assert response.json() == {'username': 'ivan',
                               "email": 'ivan@mail.com'}


@pytest.mark.asyncio
async def test_get_user(async_client):
    response = await async_client.get('/auth/user/string33')

    assert response.status_code == 200
    assert response.json() == {
        'email': 'use33r@example.com',
        'username': 'string33',
    }

