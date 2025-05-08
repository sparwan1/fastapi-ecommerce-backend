"""
Logging configuration and utilities for the application.
This module provides a consistent way to log events across the application with request tracking.
"""

import logging
import sys
import time
from typing import Any, Dict, Optional, Callable
from fastapi import Request
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.config import settings

# Create logger instance for the application
logger = logging.getLogger("app")

class RequestIDFilter(logging.Filter):
    """
    Custom logging filter that ensures every log record has a request_id field.
    This helps in tracking requests across the application.
    """
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add request_id to log record if not present.
        
        Args:
            record: The log record to process
            
        Returns:
            bool: True to allow the record to be logged
        """
        if not hasattr(record, 'request_id'):
            record.request_id = 'system'
        return True

def configure_logging() -> None:
    """
    Configure the application's logging system.
    Sets up the logging format, level, and handlers.
    """
    # Get log level from settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper())
    
    # Define a structured log format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
    
    # Configure basic logging
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Add request ID filter to the logger
    logger.addFilter(RequestIDFilter())

class RequestLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging request and response details.
    Adds a unique request ID to each request and logs timing information.
    """
    
    def __init__(self, app: ASGIApp):
        """
        Initialize middleware with the ASGI app.
        
        Args:
            app: The ASGI application
        """
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Any:
        """
        Process the request and log details.
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            The response from the next middleware or route handler
            
        Raises:
            Exception: If the request processing fails
        """
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Create a log context with request ID
        context = {"request_id": request_id}
        
        # Log request details
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra=context
        )
        
        try:
            # Time the request processing
            start_time = time.time()
            
            # Process the request
            response = await call_next(request)
            
            # Calculate request duration
            duration = time.time() - start_time
            
            # Log response details
            logger.info(
                f"Response: {response.status_code} completed in {duration:.3f}s",
                extra=context
            )
            
            # Add request ID to response headers for client tracking
            response.headers["X-Request-ID"] = request_id
            
            return response
        except Exception as e:
            # Log any errors that occur during request processing
            logger.error(f"Request failed: {str(e)}", extra=context)
            raise

def get_logger() -> logging.Logger:
    """
    Get the configured logger instance.
    
    Returns:
        logging.Logger: The configured logger instance
    """
    return logger 