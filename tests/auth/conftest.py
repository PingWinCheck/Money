import pytest_asyncio


@pytest_asyncio.fixture
async def create_user(client_async):
    response = await client_async.post('/auth/register', data={'username': 'ivan',
                                                               "email": 'ivan@mail.com',
                                                               'password': 'qwerty'})
    return response


@pytest_asyncio.fixture
async def authenticate_user(client_async):
    response = await client_async.post('/auth/token', data={'username': 'ivan',
                                                            'password': 'qwerty'})
    return response


@pytest_asyncio.fixture
async def authenticate_incorrect_user(client_async):
    response = await client_async.post('/auth/token', data={'username': 'ivan',
                                                            'password': 'qwertyz'})
    return response
