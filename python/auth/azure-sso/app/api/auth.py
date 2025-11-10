"""
Authentication routes for Azure AD OAuth2 flow.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import RedirectResponse, JSONResponse

from ..core.auth import AzureADAuth
from ..core.config import get_settings, Settings
from ..core.dependencies import get_current_user, get_azure_auth
from ..schemas.models import (
    UserInfo,
    AuthResponse,
    AuthTokens,
    TokenRefreshRequest,
)
from ..core.oauth2_client import AzureOAuth2Client
from ..core.session import SessionManager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth")


@router.get("/login", summary="Initiate Azure AD login")
async def login(
    redirect_uri: str = None,
    settings: Settings = Depends(get_settings),
    azure_auth: AzureADAuth = Depends(get_azure_auth),
):
    """
    Initiate Azure AD OAuth2 login flow.

    Redirects the user to Microsoft's login page.
    After successful authentication, user is redirected to /auth/callback.

    Query Parameters:
    - redirect_uri: Optional custom redirect URI after authentication
    """
    session_manager = SessionManager(settings)

    # Generate PKCE challenge for enhanced security
    pkce = azure_auth.generate_pkce_challenge()
    state = session_manager.generate_state()
    nonce = session_manager.generate_nonce()

    # Store session data
    await session_manager.create_session(
        state=state,
        code_verifier=pkce.code_verifier,
        nonce=nonce,
        redirect_uri=redirect_uri,
    )

    logger.info(f"Created login session with state: {state[:8]}...")

    # Build authorization URL
    auth_url = azure_auth.build_authorization_url(
        redirect_uri=settings.redirect_uri,
        state=state,
        nonce=nonce,
        pkce_challenge=pkce,
        response_type="code",
        prompt="select_account",  # Force account selection
    )

    # Close session manager connection
    await session_manager.close()

    return RedirectResponse(url=auth_url, status_code=status.HTTP_302_FOUND)


@router.get("/callback", summary="OAuth2 callback endpoint")
async def callback(
    code: str = None,
    state: str = None,
    error: str = None,
    error_description: str = None,
    settings: Settings = Depends(get_settings),
    azure_auth: AzureADAuth = Depends(get_azure_auth),
):
    """
    Handle OAuth2 callback from Azure AD.

    This endpoint receives the authorization code and exchanges it for tokens.

    Query Parameters:
    - code: Authorization code from Azure AD
    - state: State parameter for CSRF validation
    - error: Error code if authentication failed
    - error_description: Human-readable error description
    """
    # Handle errors from Azure AD
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {error_description or error}",
        )

    if not code or not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing code or state parameter",
        )

    # Retrieve and validate session
    session_manager = SessionManager(settings)
    session_data = await session_manager.get_session(state)

    if not session_data:
        logger.warning(f"Session not found for state: {state[:8] if state else 'None'}...")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid or expired state parameter. "
                "This can happen if: 1) The login session expired (timeout), "
                "2) The server was restarted, or 3) The state parameter was invalid. "
                "Please try logging in again."
            ),
        )

    logger.info(f"Retrieved session for state: {state[:8]}...")

    # Exchange code for tokens
    oauth_client = AzureOAuth2Client(settings)
    tokens = await oauth_client.exchange_code_for_tokens(
        code=code,
        redirect_uri=settings.redirect_uri,
        code_verifier=session_data.get("code_verifier"),
    )

    # Validate and extract user info from ID token
    if tokens.id_token:
        token_data = azure_auth.validate_token(tokens.id_token)
        user_info = azure_auth.extract_user_info(token_data)
    else:
        # Fallback: get user info from Microsoft Graph
        graph_data = await oauth_client.get_user_info(tokens.access_token)
        user_info = UserInfo(
            id=graph_data.get("id"),
            email=graph_data.get("mail") or graph_data.get("userPrincipalName"),
            name=graph_data.get("displayName"),
            given_name=graph_data.get("givenName"),
            family_name=graph_data.get("surname"),
        )

    # Clean up session
    await session_manager.delete_session(state)
    await session_manager.close()

    # Build response
    auth_response = AuthResponse(user=user_info, tokens=tokens)

    # Redirect to frontend or return JSON
    custom_redirect = session_data.get("redirect_uri")
    if custom_redirect or settings.frontend_redirect_uri:
        redirect_url = custom_redirect or settings.frontend_redirect_uri
        # In production, you might want to pass tokens securely (e.g., via secure cookie or session)
        return RedirectResponse(
            url=f"{redirect_url}?access_token={tokens.access_token}",
            status_code=status.HTTP_302_FOUND,
        )

    # Return JSON with properly serialized datetime fields
    return JSONResponse(content=auth_response.model_dump(mode='json'))


@router.post("/refresh", response_model=AuthTokens, summary="Refresh access token")
async def refresh_token(
    refresh_request: TokenRefreshRequest,
    settings: Settings = Depends(get_settings),
):
    """
    Refresh access token using refresh token.

    Request Body:
    - refresh_token: Valid refresh token

    Returns new access token and optionally a new refresh token.
    """
    oauth_client = AzureOAuth2Client(settings)
    tokens = await oauth_client.refresh_access_token(refresh_request.refresh_token)
    return tokens


@router.get("/session/check", summary="Check session status (debug)")
async def check_session(
    state: str,
    settings: Settings = Depends(get_settings),
):
    """
    Check if a session exists for a given state (debugging only).

    Query Parameters:
    - state: State parameter to check

    Returns:
    - Session status information
    """
    session_manager = SessionManager(settings)
    session_data = await session_manager.get_session(state)
    await session_manager.close()

    return JSONResponse(
        content={
            "state": state[:8] + "..." if len(state) > 8 else state,
            "exists": session_data is not None,
            "session_max_age": settings.session_max_age,
            "storage_type": "redis" if settings.redis_enabled and settings.redis_url else "in-memory",
        }
    )


@router.get("/logout", summary="Logout from Azure AD")
async def logout(
    post_logout_redirect_uri: str = None,
    settings: Settings = Depends(get_settings),
    azure_auth: AzureADAuth = Depends(get_azure_auth),
):
    """
    Logout from Azure AD.

    Redirects to Azure AD logout endpoint, which signs the user out
    and optionally redirects to a specified URI.

    Query Parameters:
    - post_logout_redirect_uri: URI to redirect after logout
    """
    redirect_uri = post_logout_redirect_uri or settings.frontend_redirect_uri
    logout_url = azure_auth.build_logout_url(redirect_uri)
    return RedirectResponse(url=logout_url, status_code=status.HTTP_302_FOUND)


@router.get("/me", response_model=UserInfo, summary="Get current user")
async def get_me(user: UserInfo = Depends(get_current_user)):
    """
    Get current authenticated user information.

    Requires valid Bearer token in Authorization header.
    """
    return user


@router.get("/health", summary="Health check")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "service": "azure-sso-auth"}
