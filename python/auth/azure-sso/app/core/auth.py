"""
Azure AD authentication utilities.
Handles token validation, PKCE generation, and OAuth2 flows.
"""

import base64
import hashlib
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Optional
from urllib.request import urlopen

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from fastapi import HTTPException, status

from .config import Settings
from ..schemas.models import TokenData, UserInfo, PKCEChallenge

logger = logging.getLogger(__name__)


class AzureADAuth:
    """Azure AD authentication handler."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._jwks_cache: Optional[dict] = None
        self._jwks_cache_time: Optional[datetime] = None
        self._cache_duration = timedelta(hours=24)

    def generate_pkce_challenge(self) -> PKCEChallenge:
        """
        Generate PKCE code verifier and challenge.
        Used for enhanced security in authorization code flow.
        """
        code_verifier = (
            base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")
        )
        code_challenge = (
            base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode("utf-8")).digest()
            )
            .rstrip(b"=")
            .decode("utf-8")
        )
        return PKCEChallenge(
            code_verifier=code_verifier,
            code_challenge=code_challenge,
            code_challenge_method="S256",
        )

    def _get_jwks(self) -> dict:
        """
        Get JSON Web Key Set (JWKS) from Azure AD.
        Implements caching to reduce API calls.
        """
        now = datetime.utcnow()
        if (
            self._jwks_cache is not None
            and self._jwks_cache_time is not None
            and (now - self._jwks_cache_time) < self._cache_duration
        ):
            return self._jwks_cache

        try:
            with urlopen(self.settings.jwks_uri) as response:
                jwks = json.loads(response.read())
            self._jwks_cache = jwks
            self._jwks_cache_time = now
            return jwks
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to retrieve JWKS from Azure AD: {str(e)}",
            ) from e

    def _find_rsa_key(self, jwks: dict, unverified_header: dict) -> Optional[dict]:
        """Find the matching RSA key from JWKS based on the token header."""
        for key in jwks.get("keys", []):
            if key["kid"] == unverified_header.get("kid"):
                return {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        return None

    @staticmethod
    def _ensure_bytes(key: str | bytes) -> bytes:
        """Ensure the key is in bytes format."""
        if isinstance(key, str):
            return key.encode("utf-8")
        return key

    @staticmethod
    def _decode_value(val: str) -> int:
        """Decode base64url-encoded value to integer."""
        decoded = base64.urlsafe_b64decode(AzureADAuth._ensure_bytes(val) + b"==")
        return int.from_bytes(decoded, "big")

    @staticmethod
    def _rsa_pem_from_jwk(jwk: dict) -> bytes:
        """Convert JWK to PEM format public key."""
        return (
            RSAPublicNumbers(
                n=AzureADAuth._decode_value(jwk["n"]),
                e=AzureADAuth._decode_value(jwk["e"]),
            )
            .public_key(default_backend())
            .public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    def validate_token(
        self,
        token: str,
        verify_exp: bool = True,
        audience: Optional[str] = None,
    ) -> TokenData:
        """
        Validate JWT token from Azure AD.

        Args:
            token: JWT token to validate
            verify_exp: Whether to verify token expiration
            audience: Expected audience (defaults to client_id)

        Returns:
            TokenData with validated claims

        Raises:
            HTTPException: If token validation fails
        """
        if audience is None:
            audience = self.settings.azure_client_id

        try:
            # Get unverified header to find the right key
            unverified_header = jwt.get_unverified_header(token)
        except jwt.DecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token format: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

        # Get JWKS and find matching key
        jwks = self._get_jwks()
        rsa_key = self._find_rsa_key(jwks, unverified_header)

        if rsa_key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find appropriate signing key",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Convert JWK to PEM
        public_key = self._rsa_pem_from_jwk(rsa_key)

        try:
            # First decode without verification to see the actual issuer
            unverified_payload = jwt.decode(token, options={"verify_signature": False})
            actual_issuer = unverified_payload.get("iss")
            expected_issuer = self.settings.issuer

            logger.debug(f"Token validation - Expected issuer: {expected_issuer}")
            logger.debug(f"Token validation - Actual issuer: {actual_issuer}")

            # For multi-tenant apps using "common", accept the tenant-specific issuer
            # Azure AD issues tokens with tenant-specific issuer even when using /common endpoint
            expected_issuers = [expected_issuer]
            if self.settings.azure_authority == "common":
                # Also accept tenant-specific issuer
                tenant_specific_issuer = f"https://login.microsoftonline.com/{self.settings.azure_tenant_id}/v2.0"
                expected_issuers.append(tenant_specific_issuer)
                logger.debug(
                    f"Multi-tenant mode - Also accepting: {tenant_specific_issuer}"
                )

            # Validate issuer manually if using common authority
            if actual_issuer not in expected_issuers:
                raise jwt.InvalidIssuerError(f"Invalid issuer: {actual_issuer}")

            # Decode and validate token (skip issuer validation as we did it above)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=audience,
                options={"verify_exp": verify_exp, "verify_iss": False},
            )
            return TokenData(**payload)
        except jwt.ExpiredSignatureError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except jwt.InvalidAudienceError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token audience",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except jwt.InvalidIssuerError as exc:
            logger.error(
                f"Issuer mismatch - Expected: {self.settings.issuer}, Got: {actual_issuer}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token issuer. Expected: {self.settings.issuer}, Got: {actual_issuer}",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

    def extract_user_info(self, token_data: TokenData) -> UserInfo:
        """
        Extract user information from validated token data.

        Args:
            token_data: Validated token data

        Returns:
            UserInfo object with user details
        """
        return UserInfo(
            id=token_data.sub,
            email=token_data.email,
            name=token_data.name,
            preferred_username=token_data.preferred_username,
            roles=token_data.roles,
            groups=token_data.groups,
            tenant_id=token_data.tenant_id,
        )

    def build_authorization_url(
        self,
        redirect_uri: str,
        state: Optional[str] = None,
        nonce: Optional[str] = None,
        pkce_challenge: Optional[PKCEChallenge] = None,
        response_type: str = "code",
        response_mode: str = "query",
        prompt: Optional[str] = None,
    ) -> str:
        """
        Build Azure AD authorization URL.

        Args:
            redirect_uri: Redirect URI after authentication
            state: State parameter for CSRF protection
            nonce: Nonce for ID token validation
            pkce_challenge: PKCE challenge for enhanced security
            response_type: OAuth2 response type (code, id_token, etc.)
            response_mode: How the response is returned (query, fragment, form_post)
            prompt: Prompt parameter (login, consent, select_account, none)

        Returns:
            Full authorization URL
        """
        params = {
            "client_id": self.settings.azure_client_id,
            "response_type": response_type,
            "redirect_uri": redirect_uri,
            "response_mode": response_mode,
            "scope": " ".join(self.settings.azure_scopes),
        }

        if state:
            params["state"] = state
        if nonce:
            params["nonce"] = nonce
        if prompt:
            params["prompt"] = prompt
        if pkce_challenge:
            params["code_challenge"] = pkce_challenge.code_challenge
            params["code_challenge_method"] = pkce_challenge.code_challenge_method

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.settings.authorize_endpoint}?{query_string}"

    def build_logout_url(self, post_logout_redirect_uri: Optional[str] = None) -> str:
        """
        Build Azure AD logout URL.

        Args:
            post_logout_redirect_uri: URI to redirect after logout

        Returns:
            Logout URL
        """
        logout_endpoint = f"{self.settings.authority_url}/oauth2/v2.0/logout"
        if post_logout_redirect_uri:
            return (
                f"{logout_endpoint}?post_logout_redirect_uri={post_logout_redirect_uri}"
            )
        return logout_endpoint
