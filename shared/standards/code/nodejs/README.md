# Node.js/Express Reference Example

## Overview
Gold standard Node.js/Express API server with production-ready patterns.

## Key Features

### Server Architecture
- Express.js framework
- Router-based organization
- Middleware pipeline
- Graceful shutdown handling

### Error Handling
- Custom error classes
- Async error wrapper
- Centralized error handler
- Proper HTTP status codes

### Patterns
- Service layer separation
- Async/await throughout
- Request validation
- Response formatting

### Security
- Helmet.js for security headers
- CORS configuration
- Environment-based config
- Input validation

## Files
- `api-server.js` - Complete Express API server

## Usage
```bash
npm install express helmet cors
node api-server.js
```

## API Endpoints
- `GET /health` - Health check
- `GET /api/users` - List users
- `GET /api/users/:id` - Get user
- `POST /api/users` - Create user
- `PATCH /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user

## Standards Demonstrated
- **Structure:** Service layer + router + middleware
- **Error handling:** Custom errors with status codes
- **Async:** asyncHandler wrapper for route safety
- **Logging:** Structured logging with context
- **Config:** Environment variables with defaults
- **Shutdown:** Graceful shutdown with timeout
