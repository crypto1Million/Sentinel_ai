from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    APP_NAME: str = "Sentinel AI"

    API_HOST: str = "0.0.0.0"

    API_PORT: int = 8000

    POSTGRES_USER: str

    POSTGRES_PASSWORD: str

    POSTGRES_DB: str

    REDIS_HOST: str

    REDIS_PORT: int

    HELIUS_API_KEY: str = ""

    DEXSCREENER_API: str = ""

    JUPITER_API: str = ""

    RAYDIUM_API: str = ""

    ENVIRONMENT: str = "development"

    LOG_LEVEL: str = "INFO"

    class Config:

        env_file = ".env"


@lru_cache
def get_settings():

    return Settings()