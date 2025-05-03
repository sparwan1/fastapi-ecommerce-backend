"""
Centralized error handling for the application.
This module provides custom exception classes and utility functions for consistent error handling.
"""

from fastapi import HTTPException, status
from typing import Any, Dict, Optional, List

class AppError(HTTPException):
    """Base class for application-specific exceptions."""
    def __init__(
        self, 
        status_code: int, 
        detail: str,
        code: str = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code = code or "error"

class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    def __init__(self, detail: str, code: str = "not_found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            code=code
        )

class BadRequestError(AppError):
    """Raised when a request contains invalid parameters or data."""
    def __init__(self, detail: str, code: str = "bad_request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            code=code
        )

class ConflictError(AppError):
    """Raised when a resource already exists or there's a conflict."""
    def __init__(self, detail: str, code: str = "conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            code=code
        )

class UnauthorizedError(AppError):
    """Raised when authentication is required but not provided or invalid."""
    def __init__(self, detail: str = "Not authenticated", code: str = "unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            code=code,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenError(AppError):
    """Raised when the authenticated user doesn't have permission."""
    def __init__(self, detail: str = "Not authorized", code: str = "forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            code=code
        )

class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(
        self, 
        detail: str = "Validation error", 
        errors: Optional[List[Dict[str, Any]]] = None,
        code: str = "validation_error"
    ):
        self.errors = errors or []
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            code=code
        )

class DatabaseError(AppError):
    """Raised when a database operation fails."""
    def __init__(self, detail: str = "Database error", code: str = "database_error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            code=code
        )

# Error response model
def error_response(
    status_code: int,
    message: str,
    code: str = None,
    errors: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Create a standardized error response dictionary.
    
    Args:
        status_code: HTTP status code
        message: Error message
        code: Error code for identifying the error type
        errors: List of detailed error information
        
    Returns:
        A dictionary with error details
    """
    response = {
        "status": "error",
        "code": code or "error",
        "message": message
    }
    
    if errors:
        response["errors"] = errors
        
    return response 