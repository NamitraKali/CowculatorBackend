from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "Cowculator"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb+srv://NamKali:pratima01@testcluster.jpjks.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    DB_NAME: str = "Cowculator"


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()