import pytest

# from tests.auth.conftest import create_user


# class TestAuth:
#     access_token = None
#     refresh_token = None
#     token_type = None
#
#     @pytest.mark.asyncio
#     async def test_register(self, client_async):
#         response = await client_async.post('/auth/register', data={'username': 'ivan',
#                                                                    "email": 'ivan@mail.com',
#                                                                    'password': 'qwerty'})
#         assert response.status_code == 200, 'Ошибка при создании пользователя'
#         assert response.json() == {'username': 'ivan',
#                                    "email": 'ivan@mail.com'}, 'Не верный ответ от сервера'
#
#     @pytest.mark.asyncio
#     async def test_get_user(self, client_async):
#         response = await client_async.get('/auth/user/ivan')
#
#         assert response.status_code == 200
#         assert response.json() == {
#             'email': 'ivan@mail.com',
#             'username': 'ivan',
#         }
#
#     @pytest.mark.asyncio
#     async def test_authenticated_get_token(self, client_async):
#         response = await client_async.post('/auth/token', data={'username': 'ivan',
#                                                                 'password': 'qwerty'})
#         assert response.status_code == 200
#         data: dict = response.json()
#         self.access_token = data.get('access_token')
#         self.refresh_token = data.get('refresh_token')
#         self.token_type = data.get('token_type')
#         print(f'AUTH******* {self.access_token=}')
#         assert self.access_token
#         assert self.refresh_token
#         assert self.token_type == 'Bearer'
#         TestAuth.access_token = self.access_token
#         TestAuth.refresh_token = self.refresh_token
#         TestAuth.token_type = self.token_type
#
#     @pytest.mark.asyncio
#     async def test_refresh(self, client_async):
#         print(f'REFRESH******* {self.access_token=}')
#         response = await client_async.get('/auth/refresh')
#         assert response.status_code == 401
#
#         access_token = f'{self.token_type} {self.access_token}'
#         response = await client_async.get('/auth/refresh', headers={'Authorization': access_token})
#         assert response.status_code == 401
#
#         refresh_token = f'{self.token_type} {self.refresh_token}'
#         response = await client_async.get('/auth/refresh', headers={'Authorization': refresh_token})
#         assert response.status_code == 200
#         data = response.json()
#
#         response = await client_async.get('/auth/refresh', headers={'Authorization': refresh_token})
#         assert response.status_code == 401, 'Вход со старым рефреш токеном на /auth/refresh'
#
#         self.access_token = data.get('access_token')
#         self.refresh_token = data.get('refresh_token')
#         self.token_type = data.get('token_type')
#         assert self.access_token
#         assert self.refresh_token
#         assert self.token_type == 'Bearer'
#
#         TestAuth.access_token = self.access_token
#         TestAuth.refresh_token = self.refresh_token
#         TestAuth.token_type = self.token_type
#
#
#     @pytest.mark.asyncio
#     async def test_my_profile_without_token(self, client_async):
#         response = await client_async.get('/auth/my_profile')
#         assert response.status_code == 401
#
#     @pytest.mark.asyncio
#     async def test_my_profile_with_access_token(self, client_async):
#         token = f'{self.token_type} {self.access_token}'
#         response = await client_async.get('/auth/my_profile', headers={'Authorization': token})
#         assert response.status_code == 200
#         data: dict = response.json()
#         assert data.get('username') == 'ivan'
#         assert data.get('email') == 'ivan@mail.com'
#
#     @pytest.mark.asyncio
#     async def test_change_password(self, client_async):
#         response = await client_async.put('/auth/my_profile', data={'old_password': 'qwerty',
#                                                                     'new_password': 'abcdef'})
#         assert response.status_code == 401
#
#         response = await client_async.put('/auth/my_profile', data={'old_password': 'qqwweerr',
#                                                                     'new_password': 'abcdef'},
#                                           headers={'Authorization': f'Bearer {self.access_token}'})
#         assert response.status_code == 400
#
#         response = await client_async.put('/auth/my_profile',
#                                           data={'old_password': 'qwerty',
#                                                 'new_password': 'abcdef'},
#                                           headers={'Authorization': f'Bearer {self.access_token}'})
#         assert response.status_code == 200
#         data: dict = response.json()
#         assert data.get('username') == 'ivan'
#         assert data.get('email') == 'ivan@mail.com'
#
#     @pytest.mark.asyncio
#     async def test_authenticate_with_new_password(self, client_async):
#         response = await client_async.post('/auth/token', data={'username': 'ivan',
#                                                                 'password': 'qwerty'})
#         assert response.status_code == 403
#
#         response = await client_async.post('/auth/token', data={'username': 'ivan',
#                                                                 'password': 'abcdef'})
#         assert response.status_code == 200
#         data: dict = response.json()
#         self.access_token = data.get('access_token')
#         self.refresh_token = data.get('refresh_token')
#         self.token_type = data.get('token_type')
#         assert self.access_token
#         assert self.refresh_token
#         assert self.token_type == 'Bearer'


@pytest.mark.asyncio
async def test_create_user(create_user):
    assert create_user.status_code == 201


@pytest.mark.asyncio
async def test_create_already_user(create_user):
    assert create_user.status_code == 409
    assert create_user.json().get('detail') == 'Username is already exists'


@pytest.mark.asyncio
async def test_authenticate_user(authenticate_user):
    assert authenticate_user.status_code == 200
    assert 'access_token' in authenticate_user.json()
    assert 'refresh_token' in authenticate_user.json()
    assert 'token_type' in authenticate_user.json()
    assert authenticate_user.json()['token_type'] == 'Bearer'


@pytest.mark.asyncio
async def test_authenticate_incorrect_user(authenticate_incorrect_user):
    assert authenticate_incorrect_user.status_code == 401
    assert authenticate_incorrect_user.json()['detail'] == 'Invalid login or password'


@pytest.mark.asyncio
async def test_my_profile(authenticate_user, client_async):
    response_without_authenticate = await client_async.get('/auth/my_profile')
    assert response_without_authenticate.status_code == 401
    assert response_without_authenticate.json()['detail'] == 'Not authenticated'

    response_with_incorrect_authenticate_token = await client_async.get('/auth/my_profile',
                                                                        headers={'Authorization': 'random token'})
    assert response_with_incorrect_authenticate_token.status_code == 401
    assert response_without_authenticate.json()['detail'] == 'Not authenticated'

    access_token_bearer = f'Bearer {authenticate_user.json()["access_token"]}'
    response_with_authenticate = await client_async.get('/auth/my_profile',
                                                        headers={'Authorization': access_token_bearer})
    assert response_with_authenticate.status_code == 200
    assert response_with_authenticate.json()['username'] == 'ivan'
    assert response_with_authenticate.json()['email'] == 'ivan@mail.com'

    refresh_token_bearer = f'Bearer {authenticate_user.json()["refresh_token"]}'
    response_with_refresh_token = await client_async.get('/auth/my_profile',
                                                         headers={'Authorization': refresh_token_bearer})
    assert response_with_refresh_token.status_code == 401
    assert response_with_refresh_token.json()['detail'] == 'Incorrect token'


@pytest.mark.asyncio
async def test_refresh_token(authenticate_user, client_async):
    response_without_authenticate = await client_async.get('/auth/refresh')
    assert response_without_authenticate.status_code == 401
    assert response_without_authenticate.json()['detail'] == 'Not authenticated'

    response_with_incorrect_authenticate_token = await client_async.get('/auth/refresh',
                                                                        headers={'Authorization': 'random token'})
    assert response_with_incorrect_authenticate_token.status_code == 401
    assert response_without_authenticate.json()['detail'] == 'Not authenticated'

    access_token_bearer = f'Bearer {authenticate_user.json()["access_token"]}'
    response_with_access_token_authenticate = await client_async.get('/auth/refresh',
                                                                     headers={'Authorization': access_token_bearer})
    assert response_with_access_token_authenticate.status_code == 401
    assert response_with_access_token_authenticate.json()['detail'] == 'invalid token'

    refresh_token_bearer = f'Bearer {authenticate_user.json()["refresh_token"]}'
    response_with_refresh_token = await client_async.get('/auth/refresh',
                                                         headers={'Authorization': refresh_token_bearer})
    assert response_with_refresh_token.status_code == 200
    assert 'access_token' in response_with_refresh_token.json()
    assert 'refresh_token' in response_with_refresh_token.json()
    assert 'token_type' in response_with_refresh_token.json()
    assert response_with_refresh_token.json()['token_type'] == 'Bearer'

    new_access_token_bearer = f'Bearer {response_with_refresh_token.json()["access_token"]}'
    new_refresh_token_bearer = f'Bearer {response_with_refresh_token.json()["refresh_token"]}'

    new_response_with_old_refresh_token = await client_async.get('/auth/refresh',
                                                                 headers={'Authorization': refresh_token_bearer})
    assert new_response_with_old_refresh_token.status_code == 401

    new_response_with_new_refresh_token = await client_async.get('/auth/refresh',
                                                                 headers={'Authorization': new_refresh_token_bearer})
    assert new_response_with_new_refresh_token.status_code == 200

