# FastAPI Reference Example

## Overview
Gold standard FastAPI application with production-ready patterns and best practices.

## Key Features

### Pydantic Models
- Request/response validation
- Custom validators
- Field constraints
- Schema documentation
- Nested models

### Dependency Injection
- Database dependencies
- Authentication (example pattern)
- Service layer injection
- Testable design

### API Design
- RESTful endpoints
- Proper HTTP status codes
- Request validation
- Response models
- Error handling

### Documentation
- Auto-generated OpenAPI docs
- Endpoint descriptions
- Request/response examples
- Tags for organization

### Production Features
- CORS middleware
- Request logging
- Exception handlers
- Lifespan events
- Health check endpoint

## Files
- `main.py` - Complete FastAPI application

## Usage
```bash
pip install fastapi uvicorn pydantic

# Run development server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Base
- `GET /` - API information
- `GET /health` - Health check

### Users
- `GET /users` - List all users (pagination)
- `GET /users/{id}` - Get user by ID
- `POST /users` - Create new user
- `PATCH /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

## Documentation
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI spec: `http://localhost:8000/openapi.json`

## Standards Demonstrated
- **Models:** Pydantic with validation and docs
- **Dependencies:** Dependency injection pattern
- **Errors:** Custom exception handlers
- **Middleware:** CORS and logging
- **Async:** All endpoints async
- **Types:** Full type hints throughout
- **Docs:** Comprehensive docstrings
