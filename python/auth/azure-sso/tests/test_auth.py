"""
Tests for Azure AD authentication.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock

from src.main import create_app
from src.config import Settings
from src.models import TokenData, UserInfo


@pytest.fixture
def test_settings():
    """Create test settings."""
    return Settings(
        azure_tenant_id="test-tenant-id",
        azure_client_id="test-client-id",
        azure_client_secret="test-client-secret",
        secret_key="test-secret-key",
        session_secret_key="test-session-secret",
        environment="testing",
    )


@pytest.fixture
def client(test_settings):
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint returns app info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/auth/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_login_redirects_to_azure(client):
    """Test login endpoint redirects to Azure AD."""
    response = client.get("/api/v1/auth/login", follow_redirects=False)
    assert response.status_code == 302
    assert "login.microsoftonline.com" in response.headers["location"]


def test_protected_endpoint_without_token(client):
    """Test protected endpoint rejects requests without token."""
    response = client.get("/api/v1/protected")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_token_validation():
    """Test token validation logic."""
    from src.auth import AzureADAuth

    settings = Settings(
        azure_tenant_id="test-tenant-id",
        azure_client_id="test-client-id",
        azure_client_secret="test-client-secret",
        secret_key="test-secret-key",
        session_secret_key="test-session-secret",
    )

    auth = AzureADAuth(settings)

    # Test invalid token format
    with pytest.raises(Exception):
        auth.validate_token("invalid-token")


def test_pkce_generation():
    """Test PKCE code verifier and challenge generation."""
    from src.auth import AzureADAuth

    settings = Settings(
        azure_tenant_id="test-tenant-id",
        azure_client_id="test-client-id",
        azure_client_secret="test-client-secret",
        secret_key="test-secret-key",
        session_secret_key="test-session-secret",
    )

    auth = AzureADAuth(settings)
    pkce = auth.generate_pkce_challenge()

    assert pkce.code_verifier
    assert pkce.code_challenge
    assert pkce.code_challenge_method == "S256"
    assert len(pkce.code_verifier) > 40


def test_extract_user_info():
    """Test user info extraction from token data."""
    from src.auth import AzureADAuth

    settings = Settings(
        azure_tenant_id="test-tenant-id",
        azure_client_id="test-client-id",
        azure_client_secret="test-client-secret",
        secret_key="test-secret-key",
        session_secret_key="test-session-secret",
    )

    auth = AzureADAuth(settings)

    token_data = TokenData(
        sub="user-123",
        email="test@example.com",
        name="Test User",
        preferred_username="testuser",
        roles=["User"],
        groups=["group-1"],
    )

    user_info = auth.extract_user_info(token_data)

    assert user_info.id == "user-123"
    assert user_info.email == "test@example.com"
    assert user_info.name == "Test User"
    assert "User" in user_info.roles


@pytest.mark.asyncio
async def test_session_management():
    """Test session creation and retrieval."""
    from src.session import SessionManager

    settings = Settings(
        azure_tenant_id="test-tenant-id",
        azure_client_id="test-client-id",
        azure_client_secret="test-client-secret",
        secret_key="test-secret-key",
        session_secret_key="test-session-secret",
        redis_enabled=False,  # Use in-memory for testing
    )

    manager = SessionManager(settings)

    state = manager.generate_state()
    nonce = manager.generate_nonce()

    assert len(state) > 20
    assert len(nonce) > 20

    # Create session
    await manager.create_session(
        state=state,
        code_verifier="test-verifier",
        nonce=nonce,
    )

    # Retrieve session
    session_data = await manager.get_session(state)
    assert session_data is not None
    assert session_data["code_verifier"] == "test-verifier"
    assert session_data["nonce"] == nonce

    # Delete session
    await manager.delete_session(state)
    session_data = await manager.get_session(state)
    assert session_data is None
