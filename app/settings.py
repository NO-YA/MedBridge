from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str = "sqlite:///./medbridge.db"
    DB_ECHO: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
