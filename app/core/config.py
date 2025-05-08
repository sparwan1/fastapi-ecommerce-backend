"""
Application configuration settings.
This module manages all configuration settings for the application using Pydantic's BaseSettings.
Settings can be overridden through environment variables or .env file.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional, Dict, Any
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings class using Pydantic BaseSettings.
    All configuration settings are defined here with defaults where appropriate.
    Values can be overridden through environment variables or .env file.
    """
    
    # Application metadata
    PROJECT_NAME: str = "E-commerce API"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # MongoDB settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "ecommerce_db"
    
    # JWT and security settings
    SECRET_KEY: str = "change-this-in-production"  # Should be overridden in production
    JWT_SECRET_KEY: str  # Required for JWT token generation
    JWT_ALGORITHM: str = "HS256"  # JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Access token lifetime
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # Refresh token lifetime
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_METHODS: List[str] = ["*"]  # Allowed HTTP methods
    CORS_HEADERS: List[str] = ["*"]  # Allowed HTTP headers
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    # Logging configuration
    LOG_LEVEL: str = "DEBUG"  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_FORMAT: str = "json"  # Log format (json or text)
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60  # Maximum requests per minute per IP
    
    # Cache Settings
    CACHE_TTL: int = 300  # Cache time-to-live in seconds
    REDIS_URL: str = "redis://localhost:6379"
    
    # Email Settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@yourapp.com"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB in bytes
    ALLOWED_UPLOAD_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif"]
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        """Pydantic config class for settings management"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def get_mongodb_settings(self) -> Dict[str, Any]:
        """
        Get a dictionary of MongoDB settings.
        
        Returns:
            Dict[str, Any]: Dictionary with MongoDB connection parameters
        """
        return {
            "url": self.MONGODB_URL,
            "db_name": self.MONGODB_DB_NAME
        }
        
    def get_jwt_settings(self) -> Dict[str, Any]:
        """
        Get a dictionary of JWT authentication settings.
        
        Returns:
            Dict[str, Any]: Dictionary with JWT parameters
        """
        return {
            "secret_key": self.SECRET_KEY,
            "algorithm": self.JWT_ALGORITHM,
            "access_token_expire_minutes": self.ACCESS_TOKEN_EXPIRE_MINUTES
        }


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings instance.
    Uses lru_cache to ensure only one instance is created.
    
    Returns:
        Settings: The application settings instance
    """
    return Settings()

# Create settings instance
settings = get_settings() 