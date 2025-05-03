from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.users.routes import router as users_router
from app.api.products.routes import router as products_router
from app.api.cart.routes import router as cart_router
from app.db.mongodb import mongodb
from contextlib import asynccontextmanager
from app.core.logging import configure_logging, RequestLogMiddleware
from app.core.constants import DEFAULT_PAGE_SIZE

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configure logging
    configure_logging()
    
    # Startup: connect to db and create index
    await mongodb.connect_to_database()
    await mongodb.db.carts.create_index("user_id", unique=True)
    
    # Create additional indexes if needed
    await mongodb.db.users.create_index("email", unique=True)
    await mongodb.db.users.create_index("username", unique=True)
    await mongodb.db.products.create_index("name")
    await mongodb.db.products.create_index("category")
    await mongodb.db.products.create_index([("price", 1)])  # 1 for ascending
    
    yield
    
    # Shutdown: close connection
    await mongodb.close_database_connection()

app = FastAPI(
    title="E-commerce API",
    description="A RESTful API for e-commerce application",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add request logging middleware
app.add_middleware(RequestLogMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(products_router, prefix="/api/products", tags=["products"])
app.include_router(cart_router, prefix="/api/cart", tags=["cart"])

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce API", "documentation": "/docs"} 