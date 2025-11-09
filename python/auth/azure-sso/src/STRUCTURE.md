# Azure SSO - Application Structure (Following imjoseangel Pattern)

This directory has been restructured to follow the imjoseangel architecture pattern.

## Directory Structure

```bash
src/
├── __init__.py
├── main.py                     # FastAPI application entry point
│
├── api/                        # API route handlers
│   ├── __init__.py
│   ├── auth.py                # Authentication endpoints (login, callback, logout, etc.)
│   ├── default.py             # Version and default endpoints
│   └── health.py              # Health check endpoints (/healthz, /readyz)
│
├── core/                       # Core business logic
│   ├── __init__.py
│   ├── auth.py                # Azure AD authentication utilities
│   ├── config.py              # Application settings and configuration
│   ├── dependencies.py        # FastAPI dependencies and auth helpers
│   ├── oauth2_client.py       # OAuth2 client implementation
│   └── session.py             # Session management (Redis/in-memory)
│
└── schemas/                    # Pydantic models
    ├── __init__.py
    └── models.py              # Authentication and user data models
```

## Comparison with imjoseangel Structure

### imjoseangel Structure:

```bash
app/
├── main.py
├── api/
│   ├── default.py
│   ├── health.py
│   └── ingestion.py
├── core/
│   ├── config.py
│   ├── database.py
│   ├── processor.py
│   ├── utils.py
│   └── errors.py
└── schemas/
    ├── request.py
    ├── response.py
    └── ingestion.py
```

### Our Azure SSO Structure:

```bash
src/
├── main.py
├── api/
│   ├── auth.py          # Authentication routes
│   ├── default.py       # Version info
│   └── health.py        # Health checks
├── core/
│   ├── auth.py          # Auth utilities
│   ├── config.py        # Settings
│   ├── dependencies.py  # FastAPI deps
│   ├── oauth2_client.py # OAuth2 client
│   └── session.py       # Session mgmt
└── schemas/
    └── models.py        # Pydantic models
```

## Key Changes Made

1. **Created `api/` directory** - Moved routes.py to api/auth.py and added health.py and default.py
2. **Created `core/` directory** - Moved all business logic files (auth, config, dependencies, session, oauth2_client)
3. **Created `schemas/` directory** - Moved models.py to schemas/
4. **Updated imports** - All imports updated to reflect new structure:
   - `from .config` → `from .core.config`
   - `from .models` → `from .schemas.models`
   - etc.

## Benefits of This Structure

### 1. **Clear Separation of Concerns**

- **API Layer** (`api/`): Route handlers and endpoint definitions
- **Business Logic** (`core/`): Core functionality and utilities
- **Data Models** (`schemas/`): Request/response models and validation

### 2. **Scalability**

- Easy to add new API endpoints in `api/`
- Easy to add new core features in `core/`
- Easy to add new data models in `schemas/`

### 3. **Maintainability**

- Files are logically organized
- Easier to navigate and understand
- Follows industry best practices

### 4. **Consistency**

- Follows the same pattern as imjoseangel microservice
- Makes it easier for team members familiar with one service to work on another

## API Endpoints

### Health & Monitoring

- `GET /healthz` - Kubernetes liveness probe
- `GET /readyz` - Kubernetes readiness probe
- `GET /api/v1/` - Version information

### Authentication (Azure AD SSO)

- `GET /api/v1/auth/login` - Initiate Azure AD login
- `GET /api/v1/auth/callback` - OAuth2 callback handler
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/user` - Get current user info

### Protected Examples

- `GET /api/v1/protected` - Example protected route
- `GET /api/v1/admin` - Example admin-only route

## Running the Application

```bash
# Development mode
fastapi dev src/main.py

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Environment Configuration

See `.env` file for required environment variables:

- `AZURE_CLIENT_ID` - Azure AD application ID
- `AZURE_CLIENT_SECRET` - Azure AD client secret
- `AZURE_TENANT_ID` - Azure AD tenant ID
- `REDIRECT_URI` - OAuth2 redirect URI
- `SESSION_SECRET_KEY` - Secret key for session encryption
- `REDIS_URL` - Redis connection URL (optional)

## Next Steps

Following the imjoseangel pattern, you could further enhance this structure by:

1. **Add error handlers** - Create `core/errors.py` for centralized error handling
2. **Add utilities** - Create `core/utils.py` for shared utility functions
3. **Split schemas** - Split `schemas/models.py` into:
   - `schemas/request.py` - Request models
   - `schemas/response.py` - Response models
   - `schemas/errors.py` - Error models
4. **Add database layer** - Create `core/database.py` if you need database operations
5. **Add processors** - Create `core/processor.py` for data processing logic

## Migration Notes

All existing functionality has been preserved. The only changes are:

- File organization (directory structure)
- Import statements
- No breaking changes to the API endpoints
