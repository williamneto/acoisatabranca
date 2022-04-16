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
    SKIP_ANALIZE: bool
    UFS_INSTALL: str
    CTS_INSTALL: str
    INSTALL_CANDS: bool
    INSTALL_PARTIDOS: bool
    ANALIZE_PARTIDOS: bool

    class Config:
        env_file = ".env"

settings = Settings()
