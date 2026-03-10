"""Health check endpoints."""

from fastapi import APIRouter

from ..models import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check application health status."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
    )


@router.get("/ready")
async def readiness_check() -> dict:
    """Check if application is ready to serve traffic."""
    # Add actual readiness checks here (DB, cache, etc.)
    return {"ready": True}
