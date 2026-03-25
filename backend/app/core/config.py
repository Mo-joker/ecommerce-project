from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "E-Commerce API"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/ecommerce?charset=utf8mb4"

    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production-123456"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis 配置（可选）
    REDIS_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()