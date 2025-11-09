"""
Health check endpoints.
"""

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class HealthCheck(BaseModel):
    """Health check response model."""
    status: str = "OK"


@router.get(
    "/healthz",
    summary="Perform a health check",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def healthz() -> HealthCheck:
    """
    Health check endpoint for Docker/Kubernetes liveness probes.

    Returns HTTP 200 if the service is running.
    """
    return HealthCheck(status="OK")


@router.get(
    "/readyz",
    summary="Perform a readiness check",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
async def readiness_check() -> HealthCheck:
    """
    Readiness check endpoint for Docker/Kubernetes readiness probes.

    Returns HTTP 200 if the service is ready to accept traffic.
    """
    return HealthCheck(status="OK")
