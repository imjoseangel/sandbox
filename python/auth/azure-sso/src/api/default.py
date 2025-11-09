"""
Default/version endpoints.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ..core.config import get_settings, Settings
from ..core.dependencies import get_current_user, require_roles
from ..schemas.models import UserInfo

router = APIRouter()


class VersionResponse(BaseModel):
    """Version information response."""
    app_name: str = Field(..., description="Application name")
    app_version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Environment name")


@router.get(
    "/",
    summary="Get version information",
    response_model=VersionResponse,
)
async def version(settings: Settings = Depends(get_settings)) -> VersionResponse:
    """
    Returns application version and environment information.

    This endpoint provides basic metadata about the running service.
    """
    return VersionResponse(
        app_name=settings.app_name,
        app_version=settings.app_version,
        environment=settings.environment,
    )


@router.get("/admin", summary="Admin Route")
async def admin_route(user: UserInfo = Depends(require_roles("Admin"))):
    """
    Example admin-only route.

    Requires user to have 'Admin' role.
    """
    return {
        "message": "Welcome to the admin panel!",
        "user": {
            "id": user.id,
            "name": user.name,
            "roles": user.roles,
        },
    }
