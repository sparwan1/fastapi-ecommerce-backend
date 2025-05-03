"""
Logging configuration and utilities for the application.
This module provides a consistent way to log events across the application.
"""

import logging
import sys
import time
from typing import Any, Dict, Optional, Callable
from fastapi import Request
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Create logger
logger = logging.getLogger("app")

# Create filter to add request_id when missing
class RequestIDFilter(logging.Filter):
    """Filter that ensures every log record has a request_id field"""
    
    def filter(self, record):
        if not hasattr(record, 'request_id'):
            record.request_id = 'system'
        return True

def configure_logging(log_level: str = "INFO") -> None:
    """
    Configure the logging system with appropriate handlers and formatters.
    
    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure root logger
    logger.setLevel(numeric_level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)
    
    # Add request ID filter to ensure the field exists
    request_filter = RequestIDFilter()
    handler.addFilter(request_filter)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatter to handler
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    # Avoid duplicate log messages
    logger.propagate = False
    
    # For system logs outside of requests
    logger.info("Logging configured with level %s", log_level, extra={"request_id": "system"})

class RequestLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging request and response details.
    Adds a unique request ID to each request and logs timing information.
    """
    
    def __init__(self, app: ASGIApp):
        """Initialize middleware with the ASGI app."""
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Any:
        """
        Process the request and log details.
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            The response from the next middleware or route handler
        """
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Create a log context with request ID
        context = {"request_id": request_id}
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra=context
        )
        
        try:
            # Time the request processing
            start_time = time.time()
            
            # Process the request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {response.status_code} completed in {duration:.3f}s",
                extra=context
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}", extra=context)
            raise

def get_logger():
    """
    Get the configured logger.
    
    Returns:
        The configured logger instance
    """
    return logger 