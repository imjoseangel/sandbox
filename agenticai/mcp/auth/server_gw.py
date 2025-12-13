#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FastMCP Server with:
1. Optional authentication (allows discovery without token)
2. Gateway authentication via Bearer token
3. JWT verification for client tokens
4. Role-based access control
"""
import logging
import os
from typing import Any, Optional
from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.dependencies import get_access_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== CONFIG ====================
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "3752e0b7-fa39-4c87-91cf-f46f66dff538")
GATEWAY_BEARER_TOKEN = os.getenv("GATEWAY_BEARER_TOKEN", "gateway-secret-123")

# ==================== OPTIONAL AUTH VERIFIER ====================
class OptionalGatewayAndAzureAuth(JWTVerifier):
    """
    Accepts:
    - No token (allows discovery/listing tools)
    - Gateway token (static bearer token)
    - Azure JWT token (validated against JWKS)

    Tool execution can validate token presence/validity as needed.
    """
    def __init__(self, gateway_token: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gateway_token = gateway_token

    async def verify_token(self, token: str) -> Optional[AccessToken]:
        """Accept no token, gateway token, or valid Azure JWT"""

        # Accept gateway token (read-only, no execution)
        if token == self.gateway_token:
            logger.info("✅ Gateway authenticated (read-only access)")
            return AccessToken(
                token=token,
                client_id="gateway",
                scopes=[],
                claims={
                    "client_id": "gateway",
                    "roles": [],
                    "access_level": "read-only"
                }
            )

        # Validate as Azure JWT
        logger.info("Validating Azure JWT token...")
        return await super().verify_token(token)

# ==================== JWT VERIFIER ====================
verifier = OptionalGatewayAndAzureAuth(
    gateway_token=GATEWAY_BEARER_TOKEN,
    jwks_uri=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/discovery/v2.0/keys",
    issuer=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0",
)

# ==================== MCP SERVER ====================
# Use the verifier for auth - gateway tokens and Azure JWTs accepted
mcp = FastMCP(name="Protected API", auth=verifier)

# ==================== HELPERS ====================
def get_token_with_fallback() -> Optional[AccessToken]:
    """Get current token from request context, returns None for unauthenticated requests"""
    try:
        return get_access_token()
    except Exception:
        # No token provided or not available in context
        return None

def is_gateway() -> bool:
    """Check if client is the gateway (read-only access)"""
    token = get_token_with_fallback()
    if not token:
        return False
    return token.claims.get("client_id") == "gateway"

def is_authenticated() -> bool:
    """Check if client provided a valid JWT token (not anonymous, not gateway)"""
    token = get_token_with_fallback()
    if not token:
        return False
    client_id = token.claims.get("client_id")
    return client_id not in (None, "gateway")

def check_role(*roles: str) -> bool:
    """Check if current token has required role (only for authenticated users with JWT)"""
    # Gateway cannot execute tools
    if is_gateway():
        return False

    # Unauthenticated cannot execute
    if not is_authenticated():
        return False

    token = get_token_with_fallback()
    if not token:
        return False

    token_roles = token.claims.get("roles", [])
    return any(r in token_roles for r in roles)

# ==================== TOOLS ====================
@mcp.tool
def protected_tool(data: str) -> dict[str, Any]:
    """
    Protected tool - Requires valid JWT token with 'Writers' role

    Gateway token (read-only) cannot execute this.
    """
    if is_gateway():
        return {
            "error": "Access denied",
            "status": 403,
            "message": "Gateway token has read-only access. Cannot execute tools."
        }

    if not is_authenticated():
        return {
            "error": "Authentication required",
            "status": 401,
            "message": "Please provide a valid JWT bearer token (Authorization: Bearer <token>)"
        }

    if not check_role("Writers"):
        return {
            "error": "Access denied",
            "status": 403,
            "message": "Requires Writers role"
        }

    token = get_token_with_fallback()
    client_id = token.claims.get("client_id") if token else "unknown"
    logger.info(f"✅ protected_tool executed by {client_id}: {data}")
    return {"success": True, "data": f"Processed: {data}"}

@mcp.tool
def secure_query(query: str) -> dict[str, Any]:
    """
    Secure query - Requires valid JWT token with 'Writers' role

    Gateway token (read-only) cannot execute this.
    """
    if is_gateway():
        return {
            "error": "Access denied",
            "status": 403,
            "message": "Gateway token has read-only access. Cannot execute tools."
        }

    if not is_authenticated():
        return {
            "error": "Authentication required",
            "status": 401,
            "message": "Please provide a valid JWT bearer token (Authorization: Bearer <token>)"
        }

    if not check_role("Writers"):
        return {
            "error": "Access denied",
            "status": 403,
            "message": "Requires Writers role"
        }

    token = get_token_with_fallback()
    client_id = token.claims.get("client_id") if token else "unknown"
    logger.info(f"✅ secure_query executed by {client_id}: {query}")
    client_type = "gateway" if client_id == "gateway" else "authenticated"

    return {
        "authenticated": is_authenticated(),
        "client_type": client_type,
        "client_id": client_id,
        "roles": token.claims.get("roles", []),
        "access_level": token.claims.get("access_level", "read-write"),
    }

@mcp.tool
def list_available_tools() -> dict[str, Any]:
    """
    List all available tools and their requirements

    Available to all users (gateway, authenticated, and unauthenticated).
    Shows which tools the current user can execute.
    """
    token = get_token_with_fallback()

    if not token:
        client_type = "anonymous"
        client_id = "anonymous"
    else:
        client_id = token.claims.get("client_id")
        client_type = "gateway" if client_id == "gateway" else "authenticated"

    can_execute = is_authenticated() and not is_gateway()

    return {
        "client_type": client_type,
        "current_user": client_id,
        "can_execute_tools": can_execute,
        "available_tools": [
            {
                "name": "protected_tool",
                "description": "Protected tool - processes data",
                "executable_by": "users with Writers role (JWT token only)",
                "access_level": "read-write"
            },
            {
                "name": "secure_query",
                "description": "Secure query - executes database queries",
                "executable_by": "users with Writers role (JWT token only)",
                "access_level": "read-write"
            },
            {
                "name": "get_token_info",
                "description": "Get current token information",
                "executable_by": "everyone (gateway, authenticated, unauthenticated)",
                "access_level": "read-only"
            },
            {
                "name": "list_available_tools",
                "description": "List all available tools and their requirements",
                "executable_by": "everyone (gateway, authenticated, unauthenticated)",
                "access_level": "read-only"
            }
        ],
        "restrictions": {
            "gateway": "Read-only access only. Cannot execute data-modifying tools.",
            "authenticated": "Can execute tools based on JWT roles (e.g., Writers)",
            "unauthenticated": "Can only discover and list tools"
        }
    }

# ==================== MAIN ====================
def main():
    mcp.run(transport="http", port=8000)

if __name__ == '__main__':
    main()
