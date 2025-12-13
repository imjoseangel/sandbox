#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
AZURE_JWKS_URI = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/discovery/v2.0/keys"
AZURE_ISSUER = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0"
ANONYMOUS_CLIENT_ID = "anonymous"
DEFAULT_PORT = 8000


class AuthError:
    __slots__ = ("_error", "_status", "_message")

    def __init__(self, error: str, status: int, message: str) -> None:
        self._error = error
        self._status = status
        self._message = message

    def to_dict(self) -> dict[str, Any]:
        return {"error": self._error, "status": self._status, "message": self._message}


READONLY_ERROR = AuthError(
    "Access denied", 403, "Read-only access. Provide a valid JWT token."
)


def create_role_error(role: str) -> AuthError:
    return AuthError("Access denied", 403, f"Requires {role} role")


class OptionalJWTAuthenticator(JWTVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        if not token:
            logger.info("Anonymous read-only access")
            return self._build_anonymous_token()

        logger.info("Validating Azure JWT token")
        result = await super().verify_token(token)
        if result is None:
            return self._build_anonymous_token()
        return result

    def _build_anonymous_token(self) -> AccessToken:
        return AccessToken(
            token="",
            client_id=ANONYMOUS_CLIENT_ID,
            scopes=[],
            claims={"roles": [], "access_level": "read-only"},
        )


class RequestAuthContext:
    __slots__ = ("_token", "_loaded")

    def __init__(self) -> None:
        self._token: AccessToken | None = None
        self._loaded = False

    @property
    def token(self) -> AccessToken | None:
        if not self._loaded:
            try:
                self._token = get_access_token()
            except Exception:
                self._token = None
            self._loaded = True
        return self._token

    @property
    def client_id(self) -> str | None:
        return self.token.client_id if self.token else None

    @property
    def is_anonymous(self) -> bool:
        return self.client_id == ANONYMOUS_CLIENT_ID

    @property
    def is_authenticated(self) -> bool:
        return self.client_id is not None and not self.is_anonymous

    @property
    def roles(self) -> list[str]:
        return self.token.claims.get("roles", []) if self.token else []

    def has_any_role(self, *required_roles: str) -> bool:
        return self.is_authenticated and bool(set(required_roles) & set(self.roles))


def require_auth(*roles: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
            ctx = RequestAuthContext()

            if ctx.is_anonymous or not ctx.is_authenticated:
                return READONLY_ERROR.to_dict()

            if roles and not ctx.has_any_role(*roles):
                return create_role_error(", ".join(roles)).to_dict()

            return func(*args, **kwargs)

        return wrapper

    return decorator


authenticator = OptionalJWTAuthenticator(jwks_uri=AZURE_JWKS_URI, issuer=AZURE_ISSUER)
mcp = FastMCP(name="Protected API", auth=authenticator)


@mcp.tool
@require_auth("Writers")
def protected_tool(data: str) -> dict[str, Any]:
    ctx = RequestAuthContext()
    logger.info("protected_tool executed by %s: %s", ctx.client_id, data)
    return {"success": True, "data": f"Processed: {data}"}


@mcp.tool
@require_auth("Writers")
def secure_query(query: str) -> dict[str, Any]:
    ctx = RequestAuthContext()
    logger.info("secure_query executed by %s: %s", ctx.client_id, query)
    return {
        "authenticated": ctx.is_authenticated,
        "client_id": ctx.client_id,
        "roles": ctx.roles,
        "access_level": ctx.token.claims.get("access_level", "read-write") if ctx.token else None,
    }


@mcp.tool
def get_token_info() -> dict[str, Any]:
    ctx = RequestAuthContext()
    if ctx.token is None:
        return {"authenticated": False}
    return {
        "client_id": ctx.token.client_id,
        "roles": ctx.token.claims.get("roles", []),
        "expires_at": ctx.token.expires_at,
        "access_level": "read-only" if ctx.is_anonymous else "read-write",
    }


def main() -> None:
    logger.info("Starting Protected API server on port %d", DEFAULT_PORT)
    mcp.run(transport="http", port=DEFAULT_PORT)


if __name__ == "__main__":
    main()
