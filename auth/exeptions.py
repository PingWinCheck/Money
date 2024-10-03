from fastapi import HTTPException
from starlette import status

ex_user_is_already = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                   detail='Username is already exists')

ex_invalid_login_or_password = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                             detail='Invalid login or password',
                                             headers={'WWW-Authenticate': 'Bearer'})