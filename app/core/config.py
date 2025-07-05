from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Настройки базы данных
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # Настройки пула соединений
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    DB_ECHO: bool = False

    # Только токены бота
    BOT_TOKEN: str
    TEST_BOT_TOKEN: str

    # Настройки окружения
    ENVIRONMENT: Literal["development", "production"]
    
    AWS_ENDPOINT_URL: str = 'https://storage.yandexcloud.net'
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    
    BEARER_TOKEN: str
    API_BASE_URL: str
    
    YCL_APP_ID: str
    YCL_SECRET_KEY: str
    YCL_FOLDER_ID: str
    

    def generate_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = ConfigDict(
        env_file=".env",
        # env_file="/Users/vladdremenko/ПРОЕКТЫ/SUNA_BOT/backend/.env",  
        env_file_encoding="utf-8",
        case_sensitive=True,
        cache_strings=False,
        extra="allow"
    )


settings = Settings()