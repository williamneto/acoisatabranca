from pydantic import BaseSettings

class Settings(BaseSettings):
    ENV: str
    HOST: str
    PORT: int
    PUBLIC_URL: str
    MONGO_URI: str
    MONGO_DB_NAME: str
    PUBLIC_URL: str
    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int
    AUTH_SECRET_TOKEN: str
    JWT_ALGORITHM: str
    ES_URL: str
    SKIP_INSTALL: bool
    UFS_INSTALL: str

    class Config:
        env_file = ".env"

settings = Settings()
