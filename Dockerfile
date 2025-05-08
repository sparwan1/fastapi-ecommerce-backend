# Use Python 3.11 slim image as base
# Slim image reduces the final image size while maintaining essential functionality
FROM python:3.11-slim

# Set working directory in the container
# This is where our application code will live
WORKDIR /app

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# PYTHONUNBUFFERED: Ensures Python output is sent straight to terminal
# PYTHONPATH: Adds the app directory to Python's path
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
# gcc and python3-dev are required for building some Python packages
# curl is needed for the healthcheck
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy requirements first to leverage Docker cache
# If requirements haven't changed, this layer will be cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# This is done after installing dependencies to optimize build time
COPY . .

# Create non-root user for security
# Running as non-root is a security best practice
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port 8000
# This is the port our FastAPI application will run on
EXPOSE 8000

# Health check configuration
# Checks if the application is running every 30 seconds
# Fails after 3 retries if the health check endpoint is not responding
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
# Uses uvicorn as the ASGI server
# Binds to all network interfaces (0.0.0.0) to allow external access
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 