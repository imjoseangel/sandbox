#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timezone
from typing import Any
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

AZURE_TENANT_ID = "b6674be2-2860-4fc4-8ef9-451cb064dd70"

# Configure JWT verification against your identity provider
verifier = JWTVerifier(
    jwks_uri=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/discovery/v2.0/keys",
    issuer=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0",
    audience="7bc9819e-b92f-4207-9c65-108f41814e6f",
)

mcp = FastMCP(name="Protected API", auth=verifier)

@mcp.tool
def protected_tool(data: str) -> str:
    """
    Protected tool requiring M2M authentication.

    FastMCP automatically validates the bearer token before this function executes.
    Token claims are available through the context if needed.
    """
    logger.info(f"🔧 protected_tool called with data: {data}")
    logger.info(f"✅ Token validation passed - authorized access granted")
    result = f"Processed: {data}"
    logger.info(f"📤 Returning: ✅ {result}")
    return f"✅ {result}"

@mcp.tool
def secure_query(query: str) -> dict[str, Any]:
    """
    Protected query tool with M2M authentication.

    FastMCP ensures only requests with valid tokens reach this tool.
    """
    logger.info(f"🔍 secure_query called with query: {query}")
    result = f"Query result for: {query}"
    return {
        "success": True,
        "data": result,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def main():
    mcp.run(transport="http", port=8000)

if __name__ == '__main__':
    main()
