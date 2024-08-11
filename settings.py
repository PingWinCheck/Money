from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated


class Settings(BaseSettings):
    db_user: str = 'POSTGRES'
    db_password: str = 'POSTGRES'
    db_host: str = 'localhost'
    db_port: str = '5432'
    db_name: str = 'POSTGRES'
    model_config = SettingsConfigDict(env_file='.env', extra='allow')
    private_key: str | None = None  # приватный ключ rsa для подписи jwt
    public_key: str | None = None  # публичный ключ rsa для проверки подписи jwt


settings = Settings()

