"""
FastAPI application with Azure AD SSO authentication.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings, Settings
from .dependencies import get_current_user, require_roles
from .models import UserInfo
from .routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    settings = get_settings()
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📊 Environment: {settings.environment}")
    print(f"🔐 Azure AD Tenant: {settings.azure_tenant_id}")
    print(f"💾 Session Store: {'Redis' if settings.redis_enabled else 'In-Memory'}")

    yield

    # Shutdown
    print("🛑 Shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Production-ready Azure AD / Entra ID SSO Authentication API",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Trusted Host Middleware (for production)
    if settings.is_production:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"],  # Configure properly in production
        )

    # Include routers
    app.include_router(auth_router, prefix=settings.api_prefix)

    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "docs": f"{settings.api_prefix}/docs",
        }

    @app.get(f"{settings.api_prefix}/protected")
    async def protected_route(user: UserInfo = Depends(get_current_user)):
        """Example protected route requiring authentication."""
        return {
            "message": "You have access to this protected route!",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
            },
        }

    @app.get(f"{settings.api_prefix}/admin")
    async def admin_route(user: UserInfo = Depends(require_roles("Admin"))):
        """Example admin-only route."""
        return {
            "message": "Welcome to the admin panel!",
            "user": {
                "id": user.id,
                "name": user.name,
                "roles": user.roles,
            },
        }

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler."""
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
