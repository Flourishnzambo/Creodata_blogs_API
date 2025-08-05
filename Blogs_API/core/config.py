from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Blogs"
    DEBUG: bool = True

    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_HOST: str = Field(..., env="db_host")
    DB_NAME: str = Field(..., env="db_name")
    DB_USER: str = Field(..., env="db_user")
    DB_PASSWORD: str = Field(..., env="db_password")

    SECRET_KEY: str = Field(..., env="jwt_secret_key")  # or use env="SECRET_KEY" and rename in .env
    JWT_ALGORITHM: str = Field(..., env="jwt_algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env="jwt_access_token_expire_minutes")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
