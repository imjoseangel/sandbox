#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timezone
from typing import Any
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.dependencies import get_access_token

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

AZURE_TENANT_ID = "3752e0b7-fa39-4c87-91cf-f46f66dff538"

# Configure JWT verification against your identity provider
verifier = JWTVerifier(
    jwks_uri=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/discovery/v2.0/keys",
    issuer=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0",
)

mcp = FastMCP(name="Protected API", auth=verifier)

# ==================== SIMPLE ROLE CHECK ====================
def check_role(*roles: str) -> bool:
    """Check if token has any of the required roles"""
    token = get_access_token()
    token_roles = token.claims.get("roles", [])
    return any(r in token_roles for r in roles)


# ==================== TOOLS ====================
@mcp.tool
def protected_tool(data: str) -> str:
    """Tool requiring 'Writers' role"""
    if not check_role("Writers"):
        return {"success": False, "error": "Access denied"}

    logger.info(f"✅ protected_tool executed with data: {data}")
    return f"Processed: {data}"


@mcp.tool
def secure_query(query: str) -> dict[str, Any]:
    """Query tool requiring 'Writers' role"""
    if not check_role("Writers"):
        return {"success": False, "error": "Access denied"}

    logger.info(f"✅ secure_query executed: {query}")
    return {
        "success": True,
        "data": f"Result for: {query}",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@mcp.tool
def get_token_info() -> dict[str, Any]:
    """Debug: See what's in your token (no role check)"""
    token = get_access_token()
    return {
        "client_id": token.client_id,
        "roles": token.claims.get("roles", []),
        "expires_at": token.expires_at,
    }


def main():
    mcp.run(transport="http", port=8000)

if __name__ == '__main__':
    main()
