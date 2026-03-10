"""
FastAPI Application - Reference Example

Demonstrates:
- FastAPI application structure
- Pydantic models for validation
- Dependency injection
- Router organization
- Error handling
- Async endpoints
- API documentation
- Middleware
"""

from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import logging

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enums
class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


# Pydantic models
class UserBase(BaseModel):
    """Base user model with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="User's email")
    role: UserRole = Field(default=UserRole.USER, description="User role")

    @validator('email')
    def email_must_be_lowercase(cls, v):
        """Ensure email is lowercase."""
        return v.lower()


class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(..., min_length=8, description="User password")


class User(UserBase):
    """Complete user model with ID."""
    id: str = Field(..., description="Unique user identifier")
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123",
                "name": "John Doe",
                "email": "john@example.com",
                "role": "user",
                "created_at": "2024-01-01T00:00:00",
            }
        }


class UserUpdate(BaseModel):
    """Model for updating user (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: Optional[UserRole] = None


class APIResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool = Field(..., description="Whether the operation succeeded")
    data: Optional[Any] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.now)


# Mock database
class Database:
    """Simple in-memory database."""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self._id_counter = 1

    def generate_id(self) -> str:
        """Generate unique ID."""
        id_str = str(self._id_counter)
        self._id_counter += 1
        return id_str

    def create_user(self, user_data: UserCreate) -> User:
        """Create new user."""
        user_id = self.generate_id()
        user = User(
            id=user_id,
            name=user_data.name,
            email=user_data.email,
            role=user_data.role,
        )
        self.users[user_id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)

    def get_all_users(self) -> List[User]:
        """Get all users."""
        return list(self.users.values())

    def update_user(self, user_id: str, updates: UserUpdate) -> Optional[User]:
        """Update user."""
        user = self.users.get(user_id)
        if not user:
            return None

        update_data = updates.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        return user

    def delete_user(self, user_id: str) -> bool:
        """Delete user."""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


# Global database instance
db = Database()


# Dependency injection
async def get_db() -> Database:
    """Dependency for getting database instance."""
    return db


# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Application starting up...")

    # Create sample users
    db.create_user(UserCreate(
        name="Admin User",
        email="admin@example.com",
        role=UserRole.ADMIN,
        password="password123"
    ))

    logger.info("Sample data loaded")

    yield

    # Shutdown
    logger.info("Application shutting down...")


# Create FastAPI app
app = FastAPI(
    title="User Management API",
    description="Reference FastAPI application with best practices",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    start_time = datetime.now()

    response = await call_next(request)

    duration = (datetime.now() - start_time).total_seconds()
    logger.info(
        f"{request.method} {request.url.path} - "
        f"{response.status_code} - {duration:.3f}s"
    )

    return response


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat(),
        }
    )


# Routes
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "User Management API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/users", response_model=List[User], tags=["users"])
async def list_users(
    db: Database = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List all users with pagination.

    Args:
        db: Database instance (injected)
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of users
    """
    users = db.get_all_users()
    return users[skip:skip + limit]


@app.get("/users/{user_id}", response_model=User, tags=["users"])
async def get_user(
    user_id: str,
    db: Database = Depends(get_db)
):
    """Get user by ID.

    Args:
        user_id: User identifier
        db: Database instance (injected)

    Returns:
        User object

    Raises:
        HTTPException: If user not found
    """
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@app.post(
    "/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    tags=["users"]
)
async def create_user(
    user_data: UserCreate,
    db: Database = Depends(get_db)
):
    """Create new user.

    Args:
        user_data: User creation data
        db: Database instance (injected)

    Returns:
        Created user
    """
    user = db.create_user(user_data)
    logger.info(f"Created user: {user.id}")
    return user


@app.patch("/users/{user_id}", response_model=User, tags=["users"])
async def update_user(
    user_id: str,
    updates: UserUpdate,
    db: Database = Depends(get_db)
):
    """Update user.

    Args:
        user_id: User identifier
        updates: Fields to update
        db: Database instance (injected)

    Returns:
        Updated user

    Raises:
        HTTPException: If user not found
    """
    user = db.update_user(user_id, updates)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    logger.info(f"Updated user: {user_id}")
    return user


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"]
)
async def delete_user(
    user_id: str,
    db: Database = Depends(get_db)
):
    """Delete user.

    Args:
        user_id: User identifier
        db: Database instance (injected)

    Raises:
        HTTPException: If user not found
    """
    success = db.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    logger.info(f"Deleted user: {user_id}")


# Run server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
