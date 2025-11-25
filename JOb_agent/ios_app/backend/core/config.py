"""
Application configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App Info
    APP_NAME: str = "JobTracker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="production", env="ENVIRONMENT")
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_POOL_SIZE: int = Field(default=20, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=40, env="DB_MAX_OVERFLOW")
    
    # Redis
    REDIS_URL: str = Field(..., env="REDIS_URL")
    REDIS_CACHE_TTL: int = Field(default=3600, env="REDIS_CACHE_TTL")
    
    # Celery (Optional - for background tasks)
    CELERY_BROKER_URL: Optional[str] = Field(default=None, env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: Optional[str] = Field(default=None, env="CELERY_RESULT_BACKEND")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["*"],
        env="CORS_ORIGINS"
    )
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # OpenAI (Optional - for AI features)
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL")
    OPENAI_TEMPERATURE: float = Field(default=0.3, env="OPENAI_TEMPERATURE")
    
    # External Job APIs
    RAPIDAPI_KEY: Optional[str] = Field(default=None, env="RAPIDAPI_KEY")
    SERPAPI_KEY: Optional[str] = Field(default=None, env="SERPAPI_KEY")
    INDEED_PUBLISHER_ID: Optional[str] = Field(default=None, env="INDEED_PUBLISHER_ID")
    CLEARBIT_API_KEY: Optional[str] = Field(default=None, env="CLEARBIT_API_KEY")
    
    
    # Email Settings
    EMAIL_CHECK_INTERVAL: int = Field(default=3600, env="EMAIL_CHECK_INTERVAL")
    EMAIL_LOOKBACK_DAYS: int = Field(default=30, env="EMAIL_LOOKBACK_DAYS")
    
    # File Storage (AWS S3 or GCP)
    STORAGE_PROVIDER: str = Field(default="s3", env="STORAGE_PROVIDER")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    
    # Push Notifications (Firebase)
    FIREBASE_CREDENTIALS_PATH: Optional[str] = Field(default=None, env="FIREBASE_CREDENTIALS_PATH")
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Create settings instance
settings = Settings()


# Validate critical settings
def validate_settings():
    """Validate critical settings on startup"""
    required_settings = [
        ("SECRET_KEY", settings.SECRET_KEY),
        ("DATABASE_URL", settings.DATABASE_URL),
        ("REDIS_URL", settings.REDIS_URL),
    ]
    
    missing = []
    for name, value in required_settings:
        if not value:
            missing.append(name)
    
    if missing:
        raise ValueError(f"Missing required settings: {', '.join(missing)}")
    
    return True


if __name__ == "__main__":
    validate_settings()
    print("✓ Configuration validated successfully")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug: {settings.DEBUG}")
    print(f"Database: {settings.DATABASE_URL[:20]}...")
