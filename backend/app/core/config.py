"""Конфигурация приложения."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения."""

    # Database
    DATABASE_URL: str = "postgresql://safu:safu_password@localhost:5432/safu_timetable"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Timezone
    TZ: str = "Europe/Moscow"

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # Admin
    ADMIN_ENABLED: bool = True

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

