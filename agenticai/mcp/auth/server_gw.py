#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastMCP Server with gateway and JWT authentication, and role-based access control.
"""
from __future__ import annotations

import logging
import os
from collections.abc import Callable
from functools import wraps
from typing import Any

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.dependencies import get_access_token

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "3752e0b7-fa39-4c87-91cf-f46f66dff538")
GATEWAY_BEARER_TOKEN = os.getenv("GATEWAY_BEARER_TOKEN", "gateway-secret-123")
AZURE_JWKS_URI = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/discovery/v2.0/keys"
AZURE_ISSUER = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0"
GATEWAY_CLIENT_ID = "gateway"
DEFAULT_PORT = 8000


class AuthError:
    """Immutable authentication error response."""

    __slots__ = ("_error", "_status", "_message")

    def __init__(self, error: str, status: int, message: str) -> None:
        self._error = error
        self._status = status
        self._message = message

    @property
    def error(self) -> str:
        return self._error

    @property
    def status(self) -> int:
        return self._status

    @property
    def message(self) -> str:
        return self._message

    def to_dict(self) -> dict[str, Any]:
        return {"error": self._error, "status": self._status, "message": self._message}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(error={self._error!r}, status={self._status})"


GATEWAY_READONLY_ERROR = AuthError(
    error="Access denied",
    status=403,
    message="Gateway token has read-only access. Cannot execute tools.",
)

AUTH_REQUIRED_ERROR = AuthError(
    error="Authentication required",
    status=401,
    message="Provide a valid JWT bearer token (Authorization: Bearer <token>)",
)


def create_role_error(role: str) -> AuthError:
    """Create an error response for missing required role."""
    return AuthError("Access denied", 403, f"Requires {role} role")


class HybridJWTAuthenticator(JWTVerifier):
    """
    Authentication verifier supporting both static gateway tokens and Azure JWT tokens.

    Gateway tokens provide read-only access while JWT tokens are validated
    against Azure JWKS for full access with role-based permissions.
    """

    __slots__ = ("_gateway_token",)

    def __init__(self, gateway_token: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._gateway_token = gateway_token

    async def verify_token(self, token: str) -> AccessToken | None:
        if token == self._gateway_token:
            logger.info("Gateway authenticated with read-only access")
            return self._build_gateway_token(token)

        logger.info("Validating Azure JWT token")
        return await super().verify_token(token)

    def _build_gateway_token(self, token: str) -> AccessToken:
        return AccessToken(
            token=token,
            client_id=GATEWAY_CLIENT_ID,
            scopes=[],
            claims={
                "client_id": GATEWAY_CLIENT_ID,
                "roles": [],
                "access_level": "read-only",
            },
        )


class RequestAuthContext:
    """Encapsulates authentication state for the current request with lazy token loading."""

    __slots__ = ("_token", "_loaded")

    def __init__(self) -> None:
        self._token: AccessToken | None = None
        self._loaded = False

    @property
    def token(self) -> AccessToken | None:
        if not self._loaded:
            try:
                self._token = get_access_token()
            except Exception:  # noqa: BLE001
                self._token = None
            self._loaded = True
        return self._token

    @property
    def client_id(self) -> str | None:
        if self.token is None:
            return None
        return self.token.claims.get("client_id")

    @property
    def is_gateway(self) -> bool:
        return self.client_id == GATEWAY_CLIENT_ID

    @property
    def is_authenticated(self) -> bool:
        return self.client_id is not None and not self.is_gateway

    @property
    def roles(self) -> list[str]:
        if self.token is None:
            return []
        return self.token.claims.get("roles", [])

    def has_any_role(self, *required_roles: str) -> bool:
        if not self.is_authenticated:
            return False
        return bool(set(required_roles) & set(self.roles))


def require_auth(
    *roles: str,
    allow_gateway: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator for role-based access control on MCP tools.

    Args:
        *roles: Required roles (any one grants access)
        allow_gateway: Whether gateway token access is permitted
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
            ctx = RequestAuthContext()

            if ctx.is_gateway:
                if not allow_gateway:
                    return GATEWAY_READONLY_ERROR.to_dict()
                return func(*args, **kwargs)

            if not ctx.is_authenticated:
                return AUTH_REQUIRED_ERROR.to_dict()

            if roles and not ctx.has_any_role(*roles):
                return create_role_error(", ".join(roles)).to_dict()

            return func(*args, **kwargs)

        return wrapper

    return decorator


authenticator = HybridJWTAuthenticator(
    gateway_token=GATEWAY_BEARER_TOKEN,
    jwks_uri=AZURE_JWKS_URI,
    issuer=AZURE_ISSUER,
)

mcp = FastMCP(name="Protected API", auth=authenticator)


@mcp.tool
@require_auth("Writers")
def protected_tool(data: str) -> dict[str, Any]:
    """Protected tool requiring 'Writers' role. Gateway tokens cannot execute this."""
    ctx = RequestAuthContext()
    logger.info("protected_tool executed by %s: %s", ctx.client_id, data)
    return {"success": True, "data": f"Processed: {data}"}


@mcp.tool
@require_auth("Writers")
def secure_query(query: str) -> dict[str, Any]:
    """Secure query requiring 'Writers' role. Returns authentication context details."""
    ctx = RequestAuthContext()
    logger.info("secure_query executed by %s: %s", ctx.client_id, query)

    access_level = None
    if ctx.token is not None:
        access_level = ctx.token.claims.get("access_level", "read-write")

    return {
        "authenticated": ctx.is_authenticated,
        "client_type": "authenticated",
        "client_id": ctx.client_id,
        "roles": ctx.roles,
        "access_level": access_level,
    }


@mcp.tool
def get_token_info() -> dict[str, Any]:
    """Return current token information for debugging purposes."""
    ctx = RequestAuthContext()
    if ctx.token is None:
        return {"error": "No token available", "authenticated": False}

    return {
        "client_id": ctx.token.client_id,
        "roles": ctx.token.claims.get("roles", []),
        "expires_at": ctx.token.expires_at,
    }


def main() -> None:
    """Start the MCP server with HTTP transport."""
    logger.info("Starting Protected API server on port %d", DEFAULT_PORT)
    mcp.run(transport="http", port=DEFAULT_PORT)


if __name__ == "__main__":
    main()
