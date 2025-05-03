"""
Application configuration settings.
This module manages all configuration settings for the application using Pydantic's BaseSettings.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional, Dict, Any


class Settings(BaseSettings):
    """
    Application settings class using Pydantic BaseSettings.
    All configuration settings are defined here with defaults where appropriate.
    Values can be overridden through environment variables or .env file.
    """
    
    # Application metadata
    PROJECT_NAME: str = "E-commerce API"
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # MongoDB settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "ecommerce_db"
    
    # JWT and security settings
    SECRET_KEY: str = "change-this-in-production"  # Will be overridden by .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    # Logging configuration
    LOG_LEVEL: str = "INFO"
    
    class Config:
        """Pydantic config class"""
        env_file = ".env"
        case_sensitive = True

    def get_mongodb_settings(self) -> Dict[str, Any]:
        """
        Get a dictionary of MongoDB settings.
        
        Returns:
            Dictionary with MongoDB connection parameters
        """
        return {
            "url": self.MONGODB_URL,
            "db_name": self.MONGODB_DB_NAME
        }
        
    def get_jwt_settings(self) -> Dict[str, Any]:
        """
        Get a dictionary of JWT authentication settings.
        
        Returns:
            Dictionary with JWT parameters
        """
        return {
            "secret_key": self.SECRET_KEY,
            "algorithm": self.ALGORITHM,
            "access_token_expire_minutes": self.ACCESS_TOKEN_EXPIRE_MINUTES
        }


# Create settings instance
settings = Settings() 