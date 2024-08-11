import bcrypt


def gen_password_hash(password: str) -> str:
    password_hash = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    return password_hash.decode()


def check_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=password_hash.encode())
