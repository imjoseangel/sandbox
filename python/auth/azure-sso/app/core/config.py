"""
Application configuration using Pydantic Settings.
Supports environment variables, .env files, and Azure Key Vault.
"""

from functools import lru_cache
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation and type safety."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Azure AD Configuration
    azure_tenant_id: str = Field(..., description="Azure AD Tenant ID")
    azure_client_id: str = Field(..., description="Azure AD Application Client ID")
    azure_client_secret: str = Field(
        ..., description="Azure AD Application Client Secret"
    )
    azure_authority: str = Field(
        default="common",
        description="Azure AD authority (common, organizations, consumers, or tenant ID)",
    )
    azure_scopes: str = Field(
        default="openid profile email User.Read",
        description="Space-separated Azure AD scopes",
    )

    # Application Configuration
    app_name: str = Field(default="FastAPI Azure SSO", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    environment: str = Field(
        default="development",
        description="Environment (development, staging, production)",
    )
    debug: bool = Field(default=False, description="Debug mode")
    secret_key: str = Field(..., description="Application secret key for encryption")

    # API Configuration
    api_prefix: str = Field(default="/api/v1", description="API route prefix")
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")

    # CORS Configuration
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated list of allowed CORS origins",
    )

    # Redirect URIs
    redirect_uri: str = Field(
        default="http://localhost:8000/api/v1/auth/callback",
        description="OAuth2 redirect URI for backend",
    )
    frontend_redirect_uri: Optional[str] = Field(
        default=None,
        description="Frontend redirect URI after authentication (leave empty for JSON response)",
    )

    # Token Configuration
    access_token_expire_minutes: int = Field(
        default=60, description="Access token expiration in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=7, description="Refresh token expiration in days"
    )

    # Session Configuration
    session_secret_key: str = Field(
        ..., description="Secret key for session encryption"
    )
    session_max_age: int = Field(default=3600, description="Session max age in seconds")

    # Redis Configuration
    redis_enabled: bool = Field(
        default=False, description="Enable Redis for session storage"
    )
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database number")
    redis_password: Optional[str] = Field(default=None, description="Redis password")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json or text)")

    # Azure Key Vault (Optional)
    azure_key_vault_enabled: bool = Field(
        default=False, description="Enable Azure Key Vault for secrets"
    )
    azure_key_vault_url: Optional[str] = Field(
        default=None, description="Azure Key Vault URL"
    )

    @field_validator("cors_origins")
    @classmethod
    def parse_cors_origins(cls, v: str) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in v.split(",") if origin.strip()]

    @field_validator("azure_scopes")
    @classmethod
    def parse_scopes(cls, v: str) -> list[str]:
        """Parse space-separated scopes into a list."""
        return [scope.strip() for scope in v.split() if scope.strip()]

    @property
    def authority_url(self) -> str:
        """Get the full Azure AD authority URL."""
        return f"https://login.microsoftonline.com/{self.azure_authority}"

    @property
    def authorize_endpoint(self) -> str:
        """Get the Azure AD authorize endpoint."""
        return f"{self.authority_url}/oauth2/v2.0/authorize"

    @property
    def token_endpoint(self) -> str:
        """Get the Azure AD token endpoint."""
        return f"{self.authority_url}/oauth2/v2.0/token"

    @property
    def jwks_uri(self) -> str:
        """Get the Azure AD JWKS URI."""
        return f"{self.authority_url}/discovery/v2.0/keys"

    @property
    def issuer(self) -> str:
        """Get the expected token issuer."""
        return f"{self.authority_url}/v2.0"

    @property
    def redis_url(self) -> Optional[str]:
        """Get Redis connection URL."""
        if not self.redis_enabled:
            return None
        password = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{password}{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()  # type: ignore[call-arg]
