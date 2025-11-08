# Production Deployment Guide

## 🏭 Production Readiness Checklist

### Security

- [ ] Use HTTPS/TLS everywhere
- [ ] Rotate secrets regularly
- [ ] Use Azure Key Vault for secrets
- [ ] Implement rate limiting
- [ ] Enable audit logging
- [ ] Configure CORS properly
- [ ] Use secure session cookies
- [ ] Implement CSP headers
- [ ] Enable HSTS

### Infrastructure

- [ ] Use Redis for session storage
- [ ] Set up load balancer
- [ ] Configure health checks
- [ ] Set up monitoring
- [ ] Configure log aggregation
- [ ] Implement backup strategy
- [ ] Set up auto-scaling
- [ ] Configure CDN for static assets

### Configuration

- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Use long expiration for client secrets
- [ ] Configure proper CORS origins
- [ ] Set secure redirect URIs
- [ ] Enable production logging

## 🐳 Docker Production Deployment

### Build Optimized Image

```dockerfile
# Multi-stage build for smaller image
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/

ENV PATH=/root/.local/bin:$PATH
USER nobody

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Deploy with Docker Compose

```yaml
version: '3.8'

services:
  api:
    image: fastapi-azure-sso:latest
    replicas: 3
    environment:
      - ENVIRONMENT=production
      - REDIS_ENABLED=true
      - REDIS_HOST=redis
    depends_on:
      - redis
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx-prod.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
```

## ☸️ Kubernetes Deployment

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-sso
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-sso
  template:
    metadata:
      labels:
        app: fastapi-sso
    spec:
      containers:
      - name: api
        image: fastapi-azure-sso:latest
        ports:
        - containerPort: 8000
        env:
        - name: AZURE_TENANT_ID
          valueFrom:
            secretKeyRef:
              name: azure-credentials
              key: tenant-id
        - name: AZURE_CLIENT_ID
          valueFrom:
            secretKeyRef:
              name: azure-credentials
              key: client-id
        - name: AZURE_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: azure-credentials
              key: client-secret
        - name: REDIS_HOST
          value: redis-service
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/v1/auth/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/auth/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-sso-service
spec:
  selector:
    app: fastapi-sso
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Secret Management

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: azure-credentials
type: Opaque
data:
  tenant-id: <base64-encoded-tenant-id>
  client-id: <base64-encoded-client-id>
  client-secret: <base64-encoded-client-secret>
```

## 🌐 Azure App Service Deployment

### Deploy to Azure App Service

```bash
# Install Azure CLI
az login

# Create resource group
az group create --name fastapi-sso-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name fastapi-sso-plan \
  --resource-group fastapi-sso-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group fastapi-sso-rg \
  --plan fastapi-sso-plan \
  --name my-fastapi-sso \
  --runtime "PYTHON:3.11"

# Configure app settings
az webapp config appsettings set \
  --resource-group fastapi-sso-rg \
  --name my-fastapi-sso \
  --settings \
    AZURE_TENANT_ID="your-tenant-id" \
    AZURE_CLIENT_ID="your-client-id" \
    AZURE_CLIENT_SECRET="your-client-secret"

# Deploy code
az webapp up \
  --resource-group fastapi-sso-rg \
  --name my-fastapi-sso
```

## 🔐 Azure Key Vault Integration

### Setup

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# In src/config.py
if settings.azure_key_vault_enabled:
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=settings.azure_key_vault_url,
        credential=credential
    )

    # Retrieve secrets
    settings.azure_client_secret = client.get_secret("client-secret").value
    settings.secret_key = client.get_secret("app-secret-key").value
```

### Key Vault Setup

```bash
# Create Key Vault
az keyvault create \
  --name my-sso-keyvault \
  --resource-group fastapi-sso-rg \
  --location eastus

# Add secrets
az keyvault secret set \
  --vault-name my-sso-keyvault \
  --name client-secret \
  --value "your-client-secret"

# Grant access to App Service
az webapp identity assign \
  --resource-group fastapi-sso-rg \
  --name my-fastapi-sso

az keyvault set-policy \
  --name my-sso-keyvault \
  --object-id <app-service-principal-id> \
  --secret-permissions get list
```

## 📊 Monitoring Setup

### Application Insights

```python
# Install package
pip install opencensus-ext-azure

# In src/main.py
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=your-key'
))

# Log events
logger.info('User authenticated', extra={'user_id': user.id})
```

### Prometheus Metrics

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = create_app()
Instrumentator().instrument(app).expose(app)
```

## 🚨 Health Checks

### Advanced Health Check

```python
@app.get("/health")
async def health_check():
    checks = {
        "status": "healthy",
        "redis": await check_redis(),
        "azure_ad": await check_azure_ad(),
    }

    if all(checks.values()):
        return checks
    else:
        raise HTTPException(status_code=503, detail=checks)
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: |
        pip install -r requirements.txt
        pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Build Docker image
      run: docker build -t fastapi-sso:${{ github.sha }} .

    - name: Push to registry
      run: |
        docker tag fastapi-sso:${{ github.sha }} myregistry/fastapi-sso:latest
        docker push myregistry/fastapi-sso:latest

    - name: Deploy to Kubernetes
      run: kubectl rollout restart deployment/fastapi-sso
```

## 📈 Performance Optimization

### Enable Caching

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

### Connection Pooling

```python
# Redis connection pool
redis_pool = redis.ConnectionPool.from_url(
    settings.redis_url,
    max_connections=50
)
```

## 🛡️ Security Hardening

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request):
    ...
```

### Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

---

**Your application is now production-ready! 🚀**
