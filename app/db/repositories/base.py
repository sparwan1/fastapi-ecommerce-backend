"""
Base repository implementation for MongoDB collections.
This module provides a generic repository pattern implementation for MongoDB collections.
"""

from typing import Any, Dict, List, Optional, TypeVar, Generic, Union
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.errors import NotFoundError, DatabaseError
from app.core.logging import get_logger
from app.models.base import BaseDBModel

# Type variable for the model
ModelType = TypeVar("ModelType", bound=BaseDBModel)

# Logger
logger = get_logger()

class BaseRepository(Generic[ModelType]):
    """
    Base repository class for MongoDB collections.
    Provides common CRUD operations for MongoDB collections.
    """
    
    def __init__(self, collection: AsyncIOMotorCollection):
        """
        Initialize the repository with a MongoDB collection.
        
        Args:
            collection: The MongoDB collection to use
        """
        self.collection = collection

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find a single document matching the query.
        
        Args:
            query: The query to find the document
            
        Returns:
            The found document or None if not found
        """
        try:
            return await self.collection.find_one(query)
        except Exception as e:
            logger.error(f"Error finding document: {str(e)}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def find_all(
        self, 
        query: Optional[Dict[str, Any]] = None, 
        skip: int = 0, 
        limit: int = 100,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """
        Find all documents matching the query.
        
        Args:
            query: The query to find the documents
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            sort: List of (key, direction) pairs for sorting
            
        Returns:
            List of found documents
        """
        try:
            cursor = self.collection.find(query or {}).skip(skip).limit(limit)
            
            if sort:
                cursor = cursor.sort(sort)
                
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Error finding documents: {str(e)}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def count(self, query: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents matching the query.
        
        Args:
            query: The query to count documents
            
        Returns:
            Number of matching documents
        """
        try:
            return await self.collection.count_documents(query or {})
        except Exception as e:
            logger.error(f"Error counting documents: {str(e)}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new document.
        
        Args:
            data: The document data to insert
            
        Returns:
            The created document
        """
        try:
            result = await self.collection.insert_one(data)
            return await self.find_one({"_id": result.inserted_id})
        except Exception as e:
            logger.error(f"Error creating document: {str(e)}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a document by ID.
        
        Args:
            id: The ID of the document to update
            data: The data to update
            
        Returns:
            The updated document or None if not found
        """
        try:
            query = {"_id": ObjectId(id)}
            update = {"$set": data}
            result = await self.collection.update_one(query, update)
            
            if result.matched_count == 0:
                return None
                
            return await self.find_one(query)
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def upsert(self, query: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a document if it exists, or create it if it doesn't.
        
        Args:
            query: The query to find the document
            data: The data to update or insert
            
        Returns:
            The updated or created document
        """
        try:
            update = {"$set": data}
            result = await self.collection.update_one(query, update, upsert=True)
            
            if result.upserted_id:
                return await self.find_one({"_id": result.upserted_id})
            else:
                return await self.find_one(query)
        except Exception as e:
            logger.error(f"Error upserting document: {str(e)}")
            raise DatabaseError(f"Database error: {str(e)}")

    async def delete(self, id: str) -> bool:
        """
        Delete a document by ID.
        
        Args:
            id: The ID of the document to delete
            
        Returns:
            True if the document was deleted, False otherwise
        """
        try:
            result = await self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise DatabaseError(f"Database error: {str(e)}")
            
    async def delete_many(self, query: Dict[str, Any]) -> int:
        """
        Delete multiple documents matching the query.
        
        Args:
            query: The query to match documents to delete
            
        Returns:
            Number of deleted documents
        """
        try:
            result = await self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            raise DatabaseError(f"Database error: {str(e)}") 