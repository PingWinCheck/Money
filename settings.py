from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated
from dotenv import load_dotenv


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='allow')

    # конфиг для постгрес дб
    db_user: str = 'POSTGRES'
    db_password: str = 'POSTGRES'
    db_host: str = 'localhost'
    db_port: str = '5432'
    db_name: str = 'POSTGRES'

    # ключи для jwt
    private_key: str | None = None  # приватный ключ rsa для подписи jwt
    public_key: str | None = None  # публичный ключ rsa для проверки подписи jwt
    expire_access_token_seconds: int = 60 * 15
    expire_refresh_token_seconds: int = 60 * 60 * 24 * 30

    # конфиг для редис
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0

    # smtp
    smtp_pass: str = ''
    smtp_login: str = ''


load_dotenv()
settings = Settings()

