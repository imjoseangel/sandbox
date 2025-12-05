from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider

# The AzureProvider handles Azure's token format and validation
auth_provider = AzureProvider(
    client_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    client_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    tenant_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    base_url="http://localhost:8000",
    required_scopes=['access_as_user']
)

mcp = FastMCP(name="Azure Secured App", auth=auth_provider)


# Add a protected tool to test authentication
@mcp.tool
async def get_user_info() -> dict:
    """Returns information about the authenticated Azure user."""
    from fastmcp.server.dependencies import get_access_token

    token = get_access_token()
    # The AzureProvider stores user data in token claims
    return {
        "azure_id": token.claims.get("sub") or "N/A",
        "email": token.claims.get("email") or "N/A",
        "name": token.claims.get("name") or "Unknown User",
        "job_title": token.claims.get("job_title") or "N/A",
        "office_location": token.claims.get("office_location") or "N/A"
    }
