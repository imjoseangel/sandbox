"""
Pydantic models for authentication and user data.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class TokenData(BaseModel):
    """Token data extracted from JWT."""

    sub: str = Field(..., description="Subject (user ID)")
    email: Optional[EmailStr] = Field(None, description="User email")
    name: Optional[str] = Field(None, description="User display name")
    preferred_username: Optional[str] = Field(None, description="Preferred username")
    roles: list[str] = Field(default_factory=list, description="User roles")
    groups: list[str] = Field(default_factory=list, description="User groups")
    tenant_id: Optional[str] = Field(None, alias="tid", description="Tenant ID")
    app_id: Optional[str] = Field(None, alias="appid", description="Application ID")
    exp: Optional[int] = Field(None, description="Expiration timestamp")
    iat: Optional[int] = Field(None, description="Issued at timestamp")


class UserInfo(BaseModel):
    """User information model."""

    id: str = Field(..., description="User unique identifier")
    email: Optional[EmailStr] = Field(None, description="User email")
    name: Optional[str] = Field(None, description="User display name")
    preferred_username: Optional[str] = Field(None, description="Preferred username")
    roles: list[str] = Field(default_factory=list, description="User roles")
    groups: list[str] = Field(default_factory=list, description="User groups")
    tenant_id: Optional[str] = Field(None, description="Tenant ID")


class AuthTokens(BaseModel):
    """OAuth2 tokens response."""

    access_token: str = Field(..., description="Access token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    refresh_token: Optional[str] = Field(None, description="Refresh token")
    id_token: Optional[str] = Field(None, description="ID token")
    scope: Optional[str] = Field(None, description="Granted scopes")


class AuthResponse(BaseModel):
    """Authentication response with user info and tokens."""

    user: UserInfo = Field(..., description="User information")
    tokens: AuthTokens = Field(..., description="Authentication tokens")
    authenticated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Authentication timestamp"
    )


class LoginRequest(BaseModel):
    """Login request model."""

    redirect_uri: Optional[str] = Field(
        None, description="Custom redirect URI after login"
    )
    state: Optional[str] = Field(
        None, description="State parameter for CSRF protection"
    )
    nonce: Optional[str] = Field(None, description="Nonce for ID token validation")


class CallbackRequest(BaseModel):
    """OAuth2 callback request model."""

    code: str = Field(..., description="Authorization code")
    state: Optional[str] = Field(None, description="State parameter")
    session_state: Optional[str] = Field(None, description="Session state")
    error: Optional[str] = Field(
        None, description="Error code if authentication failed"
    )
    error_description: Optional[str] = Field(None, description="Error description")


class LogoutRequest(BaseModel):
    """Logout request model."""

    post_logout_redirect_uri: Optional[str] = Field(
        None, description="URI to redirect after logout"
    )


class TokenRefreshRequest(BaseModel):
    """Token refresh request model."""

    refresh_token: str = Field(..., description="Refresh token")


class PKCEChallenge(BaseModel):
    """PKCE challenge for enhanced security."""

    code_verifier: str = Field(..., description="Code verifier (random string)")
    code_challenge: str = Field(..., description="Code challenge (hashed verifier)")
    code_challenge_method: str = Field(
        default="S256", description="Code challenge method"
    )
