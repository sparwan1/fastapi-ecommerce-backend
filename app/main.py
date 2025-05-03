from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.users.routes import router as users_router
from app.api.products.routes import router as products_router
from app.api.cart.routes import router as cart_router
from app.db.mongodb import mongodb

app = FastAPI(
    title="E-commerce API",
    description="A RESTful API for e-commerce application",
    version="1.0.0"
)

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

@app.on_event("startup")
async def startup_db_client():
    await mongodb.connect_to_database()
    # Ensure unique index on user_id in carts
    await mongodb.db.carts.create_index("user_id", unique=True)

@app.on_event("shutdown")
async def shutdown_db_client():
    await mongodb.close_database_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce API"} 