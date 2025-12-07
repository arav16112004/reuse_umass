from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "reuse-umass"
    API_V1_PREFIX: str = "/api/v1"
    DB_URL: str = "sqlite:///./dev.db"  # e.g. postgres://user:pass@host:5432/db
    SECRET_KEY: str = "change-me"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ADMIN_EMAIL: str = "admin@example.com"

settings = Settings()
