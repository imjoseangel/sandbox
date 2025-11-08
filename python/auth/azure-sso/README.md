# 🔐 FastAPI Azure AD / Entra ID SSO Authentication

A production-ready, enterprise-grade Single Sign-On (SSO) authentication system using FastAPI and Microsoft Azure AD (Entra ID). This implementation provides a complete OAuth2/OpenID Connect flow with enhanced security features, role-based access control, and multi-tenant support.

## ✨ Features

- **🔒 Secure Authentication**: OAuth2 Authorization Code Flow with PKCE
- **👥 Multi-tenant Support**: Works with personal accounts, single, and multi-tenant Azure AD
- **🎫 Token Management**: Access token validation, refresh token support, and secure session storage
- **🛡️ Security First**: JWT validation, CSRF protection, secure session handling
- **📊 Role-Based Access Control (RBAC)**: Built-in support for roles and groups
- **💾 Flexible Session Storage**: In-memory (development) and Redis (production)
- **🚀 Production Ready**: Docker support, health checks, structured logging
- **📖 Auto-generated API Docs**: Interactive Swagger UI and ReDoc
- **🎨 Frontend Example**: Ready-to-use HTML/JavaScript integration example

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │────────▶│   FastAPI    │────────▶│  Azure AD   │
│  (Browser)  │         │   Backend    │         │  (Entra ID) │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              ▼
                        ┌──────────┐
                        │  Redis   │
                        │ (Session)│
                        └──────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Azure AD Application Registration
- Redis (optional, for production)
- Docker & Docker Compose (optional)

## 🚀 Quick Start

### 1. Azure AD Setup

#### Step 1: Register Application in Azure Portal

1. Go to [Azure Portal](https://portal.azure.com) → Azure Active Directory → App registrations
2. Click **New registration**
3. Configure:
   - **Name**: Your Application Name
   - **Supported account types**:
     - Single tenant: "Accounts in this organizational directory only"
     - Multi-tenant: "Accounts in any organizational directory"
     - Personal + Work: "Accounts in any organizational directory and personal Microsoft accounts"
   - **Redirect URI**:
     - Type: Web
     - URI: `http://localhost:8000/api/v1/auth/callback`

#### Step 2: Configure Authentication

1. Go to **Authentication** section
2. Under **Platform configurations** → Web:
   - Add redirect URI: `http://localhost:8000/api/v1/auth/callback`
   - Add Front-channel logout URL (optional)
3. Under **Implicit grant and hybrid flows**:
   - ✅ Check "ID tokens" (for hybrid flow)
4. Under **Advanced settings**:
   - Allow public client flows: **Yes** (for PKCE support)

#### Step 3: Create Client Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Add description and expiration period
4. **Copy the secret value immediately** (you won't see it again!)

#### Step 4: API Permissions (Optional)

1. Go to **API permissions**
2. Add permissions:
   - Microsoft Graph → Delegated permissions
   - `openid`, `profile`, `email`, `User.Read`
3. Grant admin consent if required

#### Step 5: Get Your Credentials

- **Tenant ID**: Overview page → Directory (tenant) ID
- **Client ID**: Overview page → Application (client) ID
- **Client Secret**: The value you copied in Step 3

### 2. Project Setup

```bash
# Clone or create project directory
mkdir fastapi-azure-sso && cd fastapi-azure-sso

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or using Poetry
poetry install
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Azure AD credentials
nano .env
```

Required environment variables:
```bash
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
SECRET_KEY=generate-random-secret-key
SESSION_SECRET_KEY=another-random-secret-key
```

Generate secure secret keys:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Run the Application

#### Development Mode
```bash
# Run with uvicorn
uvicorn src.main:app --reload --port 8000

# Or using Python
python -m src.main
```

#### Production Mode with Docker
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api
```

### 5. Test the Application

1. **Open API Documentation**: http://localhost:8000/api/v1/docs
2. **Open Frontend Demo**: Open `frontend/index.html` in browser or serve with:
   ```bash
   python -m http.server 3000 --directory frontend
   ```
3. **Test Authentication Flow**:
   - Click "Sign in with Microsoft"
   - Authenticate with Azure AD
   - View your user information

## 📚 API Endpoints

### Authentication Endpoints

| Method | Endpoint                | Description             |
|--------|-------------------------|-------------------------|
| GET    | `/api/v1/auth/login`    | Initiate Azure AD login |
| GET    | `/api/v1/auth/callback` | OAuth2 callback handler |
| GET    | `/api/v1/auth/logout`   | Logout from Azure AD    |
| POST   | `/api/v1/auth/refresh`  | Refresh access token    |
| GET    | `/api/v1/auth/me`       | Get current user info   |
| GET    | `/api/v1/auth/health`   | Health check            |

### Protected Endpoints (Examples)

| Method | Endpoint            | Description         | Required    |
|--------|---------------------|---------------------|-------------|
| GET    | `/api/v1/protected` | Protected resource  | Valid token |
| GET    | `/api/v1/admin`     | Admin-only resource | Admin role  |

## 🔑 Usage Examples

### Backend - FastAPI

#### Basic Protected Route
```python
from fastapi import Depends
from src.dependencies import get_current_user
from src.models import UserInfo

@app.get("/api/data")
async def get_data(user: UserInfo = Depends(get_current_user)):
    return {"message": f"Hello {user.name}!"}
```

#### Role-Based Access Control
```python
from src.dependencies import require_roles

@app.get("/api/admin/users")
async def admin_users(user: UserInfo = Depends(require_roles("Admin", "SuperAdmin"))):
    return {"users": [...]}
```

#### Group-Based Access Control
```python
from src.dependencies import require_groups

@app.get("/api/finance/reports")
async def finance_reports(user: UserInfo = Depends(require_groups("Finance-Team"))):
    return {"reports": [...]}
```

### Frontend - JavaScript

#### Initiate Login
```javascript
// Redirect to login endpoint
window.location.href = 'http://localhost:8000/api/v1/auth/login';
```

#### Call Protected API
```javascript
const response = await fetch('http://localhost:8000/api/v1/protected', {
    headers: {
        'Authorization': `Bearer ${accessToken}`
    }
});
const data = await response.json();
```

#### Refresh Token
```javascript
const response = await fetch('http://localhost:8000/api/v1/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken })
});
const { access_token } = await response.json();
```

## 🔧 Configuration Options

### Multi-Tenant Configuration

For **multi-tenant** applications (supports any Azure AD):
```bash
AZURE_AUTHORITY=common
```

For **single-tenant** applications:
```bash
AZURE_AUTHORITY=your-tenant-id
```

For **organizational accounts** only:
```bash
AZURE_AUTHORITY=organizations
```

For **personal Microsoft accounts** only:
```bash
AZURE_AUTHORITY=consumers
```

### Session Storage

**Development** (In-Memory):
```bash
REDIS_ENABLED=False
```

**Production** (Redis):
```bash
REDIS_ENABLED=True
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Azure Scopes

Customize requested scopes:
```bash
AZURE_SCOPES=openid profile email User.Read Mail.Read
```

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t fastapi-azure-sso .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e AZURE_TENANT_ID=your-tenant-id \
  -e AZURE_CLIENT_ID=your-client-id \
  -e AZURE_CLIENT_SECRET=your-client-secret \
  -e SECRET_KEY=your-secret-key \
  -e SESSION_SECRET_KEY=your-session-secret \
  fastapi-azure-sso
```

### Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# Scale API instances
docker-compose up -d --scale api=3

# Stop services
docker-compose down
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 🔐 Security Best Practices

1. **Never commit secrets**: Use environment variables or Azure Key Vault
2. **Use HTTPS in production**: Configure SSL/TLS certificates
3. **Rotate secrets regularly**: Update client secrets and signing keys
4. **Implement rate limiting**: Prevent brute force attacks
5. **Enable audit logging**: Track authentication events
6. **Validate redirect URIs**: Prevent open redirect vulnerabilities
7. **Use short-lived tokens**: Configure appropriate expiration times
8. **Implement CORS properly**: Whitelist specific origins

## 📊 Monitoring & Logging

The application includes structured logging with JSON format support:

```python
# Example log output
{
    "timestamp": "2024-01-15T10:30:00Z",
    "level": "INFO",
    "message": "User authenticated",
    "user_id": "abc123",
    "tenant_id": "xyz789"
}
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### Common Issues

**Problem**: "Invalid redirect URI"
- **Solution**: Ensure redirect URI in Azure AD matches exactly: `http://localhost:8000/api/v1/auth/callback`

**Problem**: "AADSTS700016: Application not found"
- **Solution**: Verify Client ID is correct and app exists in your tenant

**Problem**: "Token validation failed"
- **Solution**: Check that tenant ID is correct and tokens haven't expired

**Problem**: "CORS error"
- **Solution**: Add your frontend origin to `CORS_ORIGINS` in `.env`

## 📚 Additional Resources

- [Microsoft Identity Platform Documentation](https://learn.microsoft.com/en-us/azure/active-directory/develop/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OAuth 2.0 RFC](https://tools.ietf.org/html/rfc6749)
- [OpenID Connect Specification](https://openid.net/connect/)

## 🎯 Roadmap

- [ ] Azure Key Vault integration
- [ ] Refresh token rotation
- [ ] Rate limiting middleware
- [ ] Audit logging
- [ ] GraphQL support
- [ ] WebSocket authentication
- [ ] Mobile app examples

---

**Built with ❤️ using FastAPI and Azure AD**
