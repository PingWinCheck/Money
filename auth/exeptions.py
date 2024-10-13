from fastapi import HTTPException
from starlette import status

ex_user_is_already = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                   detail='Username is already exists')

ex_invalid_login_or_password = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail='Invalid login or password',
                                             headers={'WWW-Authenticate': 'Bearer'})

ex_incorrect_token = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail='Incorrect token',
                                   headers={'WWW-Authenticate': 'Bearer'})
