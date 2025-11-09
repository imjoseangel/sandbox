# Azure SSO Troubleshooting Guide

## "Invalid or expired state parameter" Error

### What This Error Means

This error occurs during the OAuth2 callback phase when the state parameter from Azure AD's redirect cannot be validated against the stored session. The state parameter is used for CSRF protection.

### Common Causes

1. **Session Expired**
   - Default timeout: 3600 seconds (1 hour)
   - User took too long to complete the authentication flow
   - **Solution**: Increase `SESSION_MAX_AGE` environment variable

2. **Server Restart (In-Memory Storage)**
   - When using in-memory session storage (development mode), sessions are lost on server restart
   - **Solution**: Use Redis for persistent session storage in production

3. **Redis Connection Issues**
   - Redis is configured but not running or unreachable
   - **Solution**: Verify Redis connection with `redis-cli ping`

4. **Clock Skew**
   - System time differences between server and Azure AD
   - **Solution**: Ensure system time is synchronized with NTP

### Quick Fixes

#### 1. Increase Session Timeout (Development)

```bash
# In your .env file
SESSION_MAX_AGE=7200  # 2 hours
```

#### 2. Enable Redis (Production)

```bash
# In your .env file
REDIS_ENABLED=true
REDIS_URL=redis://localhost:6379/0
```

Start Redis:

```bash
# Using Docker
docker run -d -p 6379:6379 redis:alpine

# Or install locally
brew install redis  # macOS
sudo apt-get install redis-server  # Ubuntu
```

#### 3. Check Session Status (Debug Endpoint)

```bash
# Test if a session exists
curl "http://localhost:8000/auth/session/check?state=YOUR_STATE_VALUE"
```

### Updated Code Features

The code has been updated with:

1. **Better Error Messages** - More descriptive error explaining possible causes
2. **Logging** - Added debug logging for session creation and retrieval
3. **Debug Endpoint** - `/auth/session/check` to verify session status
4. **Fixed Timestamp** - Corrected session creation timestamp

### Debugging Steps

1. **Check logs** for session creation and retrieval:

   ```log
   INFO: Created login session with state: abc12345...
   WARNING: Session not found for state: abc12345...
   ```

2. **Verify session storage**:
   - In-memory: Sessions reset on server restart
   - Redis: Check with `redis-cli keys "session:*"`

3. **Test the flow quickly** - Complete OAuth flow within a few minutes

4. **Check environment variables**:

   ```bash
   echo $SESSION_MAX_AGE
   echo $REDIS_ENABLED
   echo $REDIS_URL
   ```

### Production Recommendations

1. **Use Redis** for session storage
2. **Set appropriate timeout**: 600-1800 seconds (10-30 minutes)
3. **Monitor Redis** health and connection pool
4. **Enable logging** at INFO level
5. **Remove debug endpoint** (`/auth/session/check`) in production

### Configuration Example

```env
# Azure AD Configuration
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
REDIRECT_URI=http://localhost:8000/auth/callback

# Session Configuration
SESSION_MAX_AGE=1800  # 30 minutes
REDIS_ENABLED=true
REDIS_URL=redis://localhost:6379/0

# Security
JWT_SECRET=your-random-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
```

### Additional Resources

- [OAuth 2.0 State Parameter](https://auth0.com/docs/secure/attack-protection/state-parameters)
- [Azure AD OAuth 2.0 Flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow)
- [PKCE for OAuth 2.0](https://oauth.net/2/pkce/)
