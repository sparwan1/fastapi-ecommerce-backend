"""
MongoDB connection management module.
This module handles the MongoDB connection lifecycle and provides the database instance.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
from app.core.logging import get_logger
import asyncio
from typing import Optional

logger = get_logger()

class MongoDB:
    """
    MongoDB connection manager.
    Handles connection lifecycle and provides access to the database.
    """
    
    def __init__(self):
        """Initialize MongoDB connection manager."""
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self._connection_retries = 3
        self._retry_delay = 1  # seconds

    async def connect_to_database(self) -> None:
        """
        Connect to the MongoDB database.
        Attempts connection with retries on failure.
        
        Raises:
            Exception: If connection fails after retries
        """
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}...", extra={"request_id": "system"})
        
        for attempt in range(1, self._connection_retries + 1):
            try:
                # Configure client with connection pooling
                self.client = AsyncIOMotorClient(
                    settings.MONGODB_URL,
                    maxPoolSize=10,
                    minPoolSize=1,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000
                )
                
                # Validate connection is working
                await self.client.admin.command('ping')
                
                # Get database
                self.db = self.client[settings.MONGODB_DB_NAME]
                
                logger.info(f"Connected to MongoDB database: {settings.MONGODB_DB_NAME}", extra={"request_id": "system"})
                return
                
            except Exception as e:
                if attempt == self._connection_retries:
                    logger.error(f"Failed to connect to MongoDB after {self._connection_retries} attempts: {str(e)}", extra={"request_id": "system"})
                    raise
                
                logger.warning(f"MongoDB connection attempt {attempt} failed: {str(e)}. Retrying in {self._retry_delay}s...", extra={"request_id": "system"})
                await asyncio.sleep(self._retry_delay)

    async def close_database_connection(self) -> None:
        """
        Close the MongoDB database connection.
        """
        if self.client:
            logger.info("Closing MongoDB connection...", extra={"request_id": "system"})
            self.client.close()
            logger.info("MongoDB connection closed", extra={"request_id": "system"})

    async def get_database(self) -> AsyncIOMotorDatabase:
        """
        Get the database instance, connecting if not already connected.
        
        Returns:
            The MongoDB database instance
        
        Raises:
            Exception: If the database is not initialized
        """
        if not self.db:
            await self.connect_to_database()
            
        if not self.db:
            logger.error("MongoDB database not initialized", extra={"request_id": "system"})
            raise Exception("Database not initialized")
            
        return self.db

# MongoDB singleton instance
mongodb = MongoDB() 