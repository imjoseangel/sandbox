"""
FastAPI dependencies for authentication and authorization.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth import AzureADAuth
from .config import get_settings, Settings
from ..schemas.models import UserInfo


security = HTTPBearer()


def get_azure_auth(settings: Settings = Depends(get_settings)) -> AzureADAuth:
    """Dependency to get AzureADAuth instance."""
    return AzureADAuth(settings)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    azure_auth: AzureADAuth = Depends(get_azure_auth),
) -> UserInfo:
    """
    Dependency to get current authenticated user.
    Validates the access token and returns user information.

    Usage:
        @app.get("/protected")
        async def protected_route(user: UserInfo = Depends(get_current_user)):
            return {"user_id": user.id, "email": user.email}
    """
    token = credentials.credentials
    token_data = azure_auth.validate_token(token)
    return azure_auth.extract_user_info(token_data)


async def get_current_user_optional(
    request: Request,
    azure_auth: AzureADAuth = Depends(get_azure_auth),
) -> Optional[UserInfo]:
    """
    Dependency to get current user if authenticated, otherwise None.
    Useful for routes that work with or without authentication.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    try:
        token_data = azure_auth.validate_token(token)
        return azure_auth.extract_user_info(token_data)
    except HTTPException:
        return None


def require_roles(*required_roles: str):
    """
    Dependency factory to require specific roles.

    Usage:
        @app.get("/admin")
        async def admin_route(user: UserInfo = Depends(require_roles("Admin", "SuperUser"))):
            return {"message": "Admin access granted"}
    """

    async def role_checker(user: UserInfo = Depends(get_current_user)) -> UserInfo:
        if not any(role in user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {', '.join(required_roles)}",
            )
        return user

    return role_checker


def require_groups(*required_groups: str):
    """
    Dependency factory to require specific groups.

    Usage:
        @app.get("/finance")
        async def finance_route(user: UserInfo = Depends(require_groups("Finance-Team"))):
            return {"message": "Finance access granted"}
    """

    async def group_checker(user: UserInfo = Depends(get_current_user)) -> UserInfo:
        if not any(group in user.groups for group in required_groups):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required groups: {', '.join(required_groups)}",
            )
        return user

    return group_checker


def require_tenant(*allowed_tenants: str):
    """
    Dependency factory to restrict access to specific tenants.
    Useful for multi-tenant applications.

    Usage:
        @app.get("/tenant-data")
        async def tenant_route(user: UserInfo = Depends(require_tenant("tenant-id-1", "tenant-id-2"))):
            return {"tenant": user.tenant_id}
    """

    async def tenant_checker(user: UserInfo = Depends(get_current_user)) -> UserInfo:
        if user.tenant_id not in allowed_tenants:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access restricted to specific tenants",
            )
        return user

    return tenant_checker
