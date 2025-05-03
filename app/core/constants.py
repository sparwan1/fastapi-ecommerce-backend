"""
Constants used throughout the application.
These values are centralized to avoid magic numbers and strings in the codebase.
"""

# Pagination defaults
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Collection names
USER_COLLECTION = "users"
PRODUCT_COLLECTION = "products"
CART_COLLECTION = "carts"

# Status messages
STATUS_OK = "success"
STATUS_ERROR = "error"

# Password security
BCRYPT_ROUNDS = 12  # Default for passlib's bcrypt

# Database field names
ID_FIELD = "_id"
USER_ID_FIELD = "user_id"
EMAIL_FIELD = "email"
USERNAME_FIELD = "username"
ITEMS_FIELD = "items"
PRICE_FIELD = "price"
QUANTITY_FIELD = "quantity"
STOCK_FIELD = "stock" 