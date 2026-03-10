"""Custom middleware for FastAPI application."""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .logging_config import get_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and adding request IDs."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with logging."""
        request_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()

        # Add request ID to request state
        request.state.request_id = request_id

        log = get_logger("http", request_id=request_id)
        log.info(
            "Request started",
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None,
        )

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000
        log.info(
            "Request completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )

        response.headers["X-Request-ID"] = request_id
        return response
