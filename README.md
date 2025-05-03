# E-commerce Backend API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.6.3-47A248?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

A RESTful API for an e-commerce application built with FastAPI, async Python, and MongoDB.

---

## Table of Contents
- [Small Working Demo](#-working-demo)
- [Setup Instructions](#-setup-instructions)
- [API Documentation](#-api-documentation)
- [Design Decisions](#-design-decisions)
- [Scaling Considerations](#-scaling-considerations)
- [Project Structure](#-project-structure)
- [Testing](#-testing)

##  Working Demo


https://github.com/user-attachments/assets/d047a04a-1db1-45e4-b879-cdc4ec592d98


##  Setup Instructions

### Prerequisites

- Python 3.11+
- MongoDB (local or remote)
- pip (Python package manager)
- Git

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3.11 -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**
   - Install MongoDB Community Edition:
     - [macOS Installation](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/): `brew tap mongodb/brew`, `brew update`, 
     
        `brew install mongodb-community@8.0`
     - [Windows Installation](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)
     - [Linux Installation](https://www.mongodb.com/docs/manual/administration/install-on-linux/)
   - Start the MongoDB server:
     - macOS: `brew services start mongodb-community`
     - Windows: MongoDB should run as a service automatically
     - Linux: `sudo systemctl start mongod`

5. **Create a `.env` file in the root directory: (I have provided my .env file if needed for use)**
   ```
   MONGODB_URL=mongodb://localhost:27017
   MONGODB_DB_NAME=ecommerce_db
   SECRET_KEY=your-secret-key-here
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`

##  API Documentation

FastAPI provides automatic, interactive API documentation:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Main Endpoints

####  Users (`/api/users`)
- `POST /api/users/` — Create a new user
- `GET /api/users/` — List users (with pagination)
- `GET /api/users/{user_id}` — Get user by ID
- `PUT /api/users/{user_id}` — Update user (full)
- `PATCH /api/users/{user_id}` — Update user (partial)
- `DELETE /api/users/{user_id}` — Delete user

####  Products (`/api/products`)
- `POST /api/products/` — Create a new product
- `GET /api/products/` — List products (with filters for category, price, pagination)
- `GET /api/products/{product_id}` — Get product by ID
- `PUT /api/products/{product_id}` — Update product (full)
- `PATCH /api/products/{product_id}` — Update product (partial)
- `DELETE /api/products/{product_id}` — Delete product

####  Cart (`/api/cart`)
- `POST /api/cart/` — Create a cart for a user
- `GET /api/cart/{cart_id}` — Get cart by ID
- `POST /api/cart/{cart_id}/items` — Add item to cart
- `DELETE /api/cart/{cart_id}/items/{item_id}` — Remove item from cart
- `DELETE /api/cart/{cart_id}/clear` — Clear all items from cart
- `DELETE /api/cart/{cart_id}` — Delete cart

## Design Decisions

1. **Modular Architecture**
   - Repository pattern for data access with a generic base repository
   - Centralized error handling with custom exception classes
   - Dependency injection for flexible component integration
   - Middleware-based request processing pipeline

2. **Async Architecture**
   - FastAPI's async capabilities for non-blocking request handling
   - Motor async MongoDB driver for efficient database operations
   - Connection pooling for optimized resource utilization
   - Asynchronous context managers for resource lifecycle management

3. **Database Strategy**
   - MongoDB selected for schema flexibility with product variations
   - Strategic indexes for optimized query performance
   - Repository pattern abstracts database operations
   - Document-based model for natural JSON representation

4. **Robust Error Handling**
   - Centralized error system with typed exceptions
   - Consistent error response format
   - Proper HTTP status codes for different error scenarios
   - Detailed validation error reporting

5. **Security & Code Quality**
   - Password hashing with bcrypt
   - Environment-based configuration management
   - Input validation via Pydantic models
   - Type annotations throughout for better IDE support and runtime safety
   - Comprehensive logging with request ID tracking

## Scaling for High Traffic

1. **Horizontal Scaling**
   - Stateless application design enables multiple instances behind a load balancer
   - Containerization (Docker) for environment consistency and easy deployment
   - Kubernetes orchestration for automated scaling and self-healing
   - Configurable connection pools to manage resources efficiently

2. **Database Optimization**
   - Strategic MongoDB indexes implemented on frequently queried fields
   - Database sharding capability for horizontal scaling
   - Read replicas for read-heavy workloads
   - Connection pooling configured for optimal performance

3. **Caching & Performance**
   - Ready for Redis integration for caching frequent queries
   - Efficient database query patterns through repositories
   - Pagination implemented for large data sets
   - Asynchronous I/O to maximize throughput

4. **Monitoring & Resilience**
   - Structured logging with request tracking
   - Request timing for performance monitoring
   - Database connection retry mechanism
   - Graceful error handling and reporting

5. **Future Enhancements**
   - API rate limiting framework in place
   - Ready for message queue integration for async processing
   - Prepared for implementing circuit breakers for service resilience
   - Structured for multi-region deployment

## 📁 Project Structure

```
app/
├── api/            # Routes handle HTTP requests and responses
│   ├── users/      # User-related endpoints
│   ├── products/   # Product-related endpoints
│   └── cart/       # Cart-related endpoints
├── core/           # Configuration, security, and dependencies
│   ├── config.py   # Configuration settings
│   ├── constants.py # Application constants
│   ├── errors.py   # Error handling system
│   ├── logging.py  # Logging configuration
│   └──security.py  # Security utilities
│   
├── models/         # Database models
│   ├── mongodb.py  # MongoDB connection management
│   └── repositories/ # Repository pattern implementations
├── schemas/        # Pydantic models for data validation
└── db/             # MongoDB integration with async support via Motor
tests/              # Test files
```
