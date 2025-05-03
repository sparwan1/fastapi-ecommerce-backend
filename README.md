# E-commerce API

A RESTful API for an e-commerce application built with FastAPI, async Python, and MongoDB.

## Features

- User authentication and authorization
- Product management
- Shopping cart functionality
- MongoDB database integration
- Async operations for better performance

## Prerequisites

- Python 3.11
- MongoDB
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce-backend
```

2. Create and activate a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=ecommerce_db
SECRET_KEY=your-secret-key-here
```

## Running the Application

1. Start MongoDB server

2. Run the FastAPI application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── api/            # API routes
│   ├── users/      # User-related endpoints
│   ├── products/   # Product-related endpoints
│   └── cart/       # Cart-related endpoints
├── core/           # Core functionality
├── models/         # Database models
├── schemas/        # Pydantic schemas
└── db/             # Database configuration
tests/              # Test files
```

## Testing

Run tests using pytest:
```bash
pytest
``` 