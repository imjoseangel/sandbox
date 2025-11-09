"""
OAuth2 client for Azure AD token exchange.
"""

import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

from .config import Settings
from ..schemas.models import AuthTokens


class AzureOAuth2Client:
    """OAuth2 client for interacting with Azure AD token endpoint."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def exchange_code_for_tokens(
        self,
        code: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None,
    ) -> AuthTokens:
        """
        Exchange authorization code for tokens.

        Args:
            code: Authorization code from callback
            redirect_uri: Redirect URI used in authorization request
            code_verifier: PKCE code verifier (if PKCE was used)

        Returns:
            AuthTokens with access and refresh tokens

        Raises:
            HTTPException: If token exchange fails
        """
        data = {
            "client_id": self.settings.azure_client_id,
            "client_secret": self.settings.azure_client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "scope": " ".join(self.settings.azure_scopes),
        }

        if code_verifier:
            data["code_verifier"] = code_verifier

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.settings.token_endpoint,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                response.raise_for_status()
                token_response = response.json()
                return AuthTokens(**token_response)
        except httpx.HTTPStatusError as e:
            error_detail = self._parse_error_response(e.response)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Token exchange failed: {error_detail}",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to connect to Azure AD: {str(e)}",
            )

    async def refresh_access_token(self, refresh_token: str) -> AuthTokens:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: Refresh token

        Returns:
            AuthTokens with new access token

        Raises:
            HTTPException: If token refresh fails
        """
        data = {
            "client_id": self.settings.azure_client_id,
            "client_secret": self.settings.azure_client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "scope": " ".join(self.settings.azure_scopes),
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.settings.token_endpoint,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )
                response.raise_for_status()
                token_response = response.json()
                return AuthTokens(**token_response)
        except httpx.HTTPStatusError as e:
            error_detail = self._parse_error_response(e.response)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token refresh failed: {error_detail}",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to connect to Azure AD: {str(e)}",
            )

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Get user information from Microsoft Graph API.

        Args:
            access_token: Valid access token

        Returns:
            User information dictionary

        Raises:
            HTTPException: If request fails
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://graph.microsoft.com/v1.0/me",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = self._parse_error_response(e.response)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to get user info: {error_detail}",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to connect to Microsoft Graph: {str(e)}",
            )

    @staticmethod
    def _parse_error_response(response: httpx.Response) -> str:
        """Parse error response from Azure AD."""
        try:
            error_data = response.json()
            error = error_data.get("error", "unknown_error")
            error_description = error_data.get("error_description", "No description provided")
            return f"{error}: {error_description}"
        except Exception:
            return response.text or "Unknown error"
