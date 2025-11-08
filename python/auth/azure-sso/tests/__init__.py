"""Test configuration module."""

import pytest


@pytest.fixture
def test_env(monkeypatch):
    """Set test environment variables."""
    monkeypatch.setenv("AZURE_TENANT_ID", "test-tenant")
    monkeypatch.setenv("AZURE_CLIENT_ID", "test-client")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "test-secret")
    monkeypatch.setenv("SECRET_KEY", "test-key")
    monkeypatch.setenv("SESSION_SECRET_KEY", "test-session-key")
