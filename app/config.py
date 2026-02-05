from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file=".env", env_ignore_empty=True, extra="ignore"
)


class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = _base_config


@lru_cache
def get_settings():
    return DatabaseSettings()


class SecuritySettings(BaseSettings):
    JWT_SECRET: str = "your_secret_key"
    JWT_ALGORITHM: str = "HS256"

    model_config = _base_config


settings = get_settings()
security_settings = SecuritySettings()
