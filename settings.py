from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str = 'POSTGRES'
    db_password: str = 'POSTGRES'
    db_host: str = 'localhost'
    db_port: str = '5432'
    db_name: str = 'POSTGRES'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()

