"""FastAPI Azure AD SSO Authentication Package."""

from .main import app, create_app
from .core.config import get_settings, Settings
from .core.dependencies import get_current_user, require_roles, require_groups
from .schemas.models import UserInfo, AuthResponse, AuthTokens

__version__ = "1.0.0"
__all__ = [
    "app",
    "create_app",
    "get_settings",
    "Settings",
    "get_current_user",
    "require_roles",
    "require_groups",
    "UserInfo",
    "AuthResponse",
    "AuthTokens",
]
