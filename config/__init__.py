import os
from pydantic import BaseSettings

class CommonSettings(BaseSettings):
    APP_NAME: str = os.environ.get("APP_NAME", "Cowculator")
    DEBUG_MODE: bool = os.environ.get("DEBUG_MODE", False)


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = os.environ.get("PORT")


class DatabaseSettings(BaseSettings):
    DB_URL: str = os.environ.get("DB_URL")
    DB_NAME: str = os.environ.get("Cowculator")


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()