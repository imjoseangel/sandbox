"""Simplified M2M Client: Get token from Azure, call FastMCP server"""

import os
import asyncio
import logging
import requests
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config from env
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")


def get_token() -> str:
    """Get bearer token from Azure"""
    if not CLIENT_SECRET:
        logger.error("❌ CLIENT_SECRET not set")
        return None

    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"api://{CLIENT_ID}/.default",
    }

    logger.info(f"🔐 Getting token...")
    try:
        r = requests.post(url, data=data, timeout=10)
        if r.status_code != 200:
            logger.error(f"❌ {r.json().get('error_description')}")
            return None
        token = r.json()["access_token"]
        logger.info(f"✅ Token obtained")
        return token
    except Exception as e:
        logger.error(f"❌ {e}")
        return None


async def main():
    token = get_token()
    if not token:
        return

    logger.info(f"📞 Calling tools...")
    auth = BearerAuth(token)

    try:
        async with Client(MCP_SERVER_URL, auth=auth, name="M2M") as client:
            # Call tools
            r1 = await client.call_tool("protected_tool", {"data": "test"})
            logger.info(f"✅ protected_tool: {r1}")

            r2 = await client.call_tool("secure_query", {"query": "SELECT *"})
            logger.info(f"✅ secure_query: {r2}")

            r3 = await client.call_tool("get_token_info", {})
            logger.info(f"✅ token info: {r3}")
    except Exception as e:
        logger.error(f"❌ {e}")


if __name__ == "__main__":
    asyncio.run(main())
