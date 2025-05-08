"""
Main application module for the E-commerce API.
This module initializes the FastAPI application and configures all necessary components.
"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.users.routes import router as users_router
from app.api.products.routes import router as products_router
from app.api.cart.routes import router as cart_router
from app.db.mongodb import mongodb
from contextlib import asynccontextmanager
from app.core.logging import configure_logging, RequestLogMiddleware
from app.core.constants import DEFAULT_PAGE_SIZE
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events for the application.
    
    Args:
        app: The FastAPI application instance
    """
    # Configure logging system
    configure_logging()
    
    # Startup: Initialize database connection and create indexes
    await mongodb.connect_to_database()
    
    # Create database indexes for optimal query performance
    # Cart indexes
    await mongodb.db.carts.create_index("user_id", unique=True)
    
    # User indexes
    await mongodb.db.users.create_index("email", unique=True)
    await mongodb.db.users.create_index("username", unique=True)
    
    # Product indexes
    await mongodb.db.products.create_index("name")
    await mongodb.db.products.create_index("category")
    await mongodb.db.products.create_index([("price", 1)])  # 1 for ascending order
    
    yield
    
    # Shutdown: Clean up database connection
    await mongodb.close_database_connection()

# Initialize FastAPI application with metadata and configuration
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A RESTful API for e-commerce application",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add request logging middleware for tracking API usage
app.add_middleware(RequestLogMiddleware)

# Configure CORS middleware for handling cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Register API routers with their respective prefixes and tags
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(products_router, prefix="/api/products", tags=["products"])
app.include_router(cart_router, prefix="/api/cart", tags=["cart"])

@app.get("/")
async def root():
    """
    Root endpoint that provides basic API information.
    
    Returns:
        dict: Welcome message and documentation URL
    """
    return {"message": "Welcome to the E-commerce API", "documentation": "/docs"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and container orchestration.
    Verifies database connectivity and returns service status.
    
    Returns:
        JSONResponse: Health status with database connection state
    """
    try:
        # Check MongoDB connection
        await mongodb.db.command('ping')
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "healthy", "database": "connected"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)}
        ) 