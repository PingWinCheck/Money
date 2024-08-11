from typing import Any
from datetime import timedelta, timezone, datetime

import bcrypt
import jwt
from jwt.exceptions import ExpiredSignatureError
from settings import settings


def gen_password_hash(password: str) -> str:
    password_hash = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    return password_hash.decode()


def check_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=password_hash.encode())


def gen_jwt(payload: dict[str, Any],
            expire: timedelta = timedelta(minutes=15)) -> str:
    if not payload.get('exp'):
        payload = payload.copy()
        now = datetime.now(timezone.utc)
        payload['exp'] = now + expire
    token = jwt.encode(payload=payload, key=settings.private_key, algorithm='RS256')
    return token


def check_jwt(token: str) -> dict | None:
    try:
        payload: dict[str, Any] = jwt.decode(jwt=token, key=settings.public_key, algorithms=['RS256'])
        return payload
    except ExpiredSignatureError:
        return None

