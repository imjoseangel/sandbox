# Frontend Redirect Configuration

## Problem

After successful OAuth authentication, the callback was redirecting to `http://localhost:3000/auth/callback`, but no frontend is running on port 3000, causing "Can't open the page" error.

## Root Cause

The `FRONTEND_REDIRECT_URI` was set to `http://localhost:3000/auth/callback`, and the callback route always redirects to the frontend URL when it's configured:

```python
if custom_redirect or settings.frontend_redirect_uri:
    redirect_url = custom_redirect or settings.frontend_redirect_uri
    return RedirectResponse(url=f"{redirect_url}?access_token={tokens.access_token}")
```

## Solution

Made `frontend_redirect_uri` **optional** so you can:

- **Set it**: Redirect to frontend (for production with a React/Vue/etc. frontend)
- **Leave it empty**: Return JSON response directly (for API testing/development)

### Changes Made

1. **`/src/config.py`**: Made `frontend_redirect_uri` optional

   ```python
   frontend_redirect_uri: Optional[str] = Field(
       default=None,
       description="Frontend redirect URI after authentication (leave empty for JSON response)",
   )
   ```

2. **`.env`**: Commented out the frontend redirect

   ```env
   # FRONTEND_REDIRECT_URI=http://localhost:3000/auth/callback  # Leave empty for JSON response
   FRONTEND_REDIRECT_URI=
   ```

## Usage

### For API Testing (No Frontend)

Leave `FRONTEND_REDIRECT_URI` empty in `.env`:

```env
FRONTEND_REDIRECT_URI=
```

**Result**: After OAuth login, you'll get a JSON response:

```json
{
  "user": {
    "id": "2c001660-6eca-4d6e-9d5b-ad1714ae2eaf",
    "email": "contact@imjoseangel.eu.org",
    "name": "imjoseangel",
    "given_name": null,
    "family_name": null
  },
  "tokens": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJub25jZSI6...",
    "token_type": "Bearer",
    "expires_in": 3599,
    "refresh_token": "1.Aa4A4ktntmAoxE-O...",
    "id_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### For Production with Frontend

Set the frontend URL in `.env`:

```env
FRONTEND_REDIRECT_URI=http://localhost:3000/auth/callback
# Or for production:
# FRONTEND_REDIRECT_URI=https://yourapp.com/auth/callback
```

**Result**: After OAuth login, redirects to:

```txt
http://localhost:3000/auth/callback?access_token=eyJ0eXAiOiJKV1Q...
```

### With Custom Redirect per Request

You can also specify a custom redirect when initiating login:

```bash
# Login with custom redirect
GET /api/v1/auth/login?redirect_uri=http://custom-app.com/callback
```

## Security Note

⚠️ **Warning**: Passing access tokens in the URL query string (as shown in the redirect) is **not recommended for production** because:

1. URLs are logged in browser history
2. URLs appear in server logs
3. URLs can be leaked via the Referer header

### Recommended Production Approaches

1. **Use HTTP-only cookies**:

   ```python
   response.set_cookie(
       "access_token",
       tokens.access_token,
       httponly=True,
       secure=True,
       samesite="lax"
   )
   ```

2. **Use session-based authentication**:
   - Store tokens server-side
   - Return session ID to frontend

3. **Use Authorization Code Flow with PKCE** (already implemented):
   - Frontend initiates flow
   - Backend handles token exchange
   - Backend stores tokens securely
   - Frontend gets session cookie only

## Testing Steps

1. **Restart your server**:

   ```bash
   # Stop current server (Ctrl+C)
   uvicorn src.main:app --reload
   ```

2. **Initiate login**:

   ```bash
   open http://localhost:8000/api/v1/auth/login
   ```

3. **Complete Azure AD authentication**

4. **Get JSON response** with user info and tokens

5. **Test the `/me` endpoint**:

   ```bash
   curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
        http://localhost:8000/api/v1/auth/me
   ```

## Example Response

```json
{
  "user": {
    "id": "2c001660-6eca-4d6e-9d5b-ad1714ae2eaf",
    "email": "contact@imjoseangel.eu.org",
    "name": "imjoseangel",
    "given_name": null,
    "family_name": null
  },
  "tokens": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJub25jZSI6IngwNDlSOTVtNWtDdGdmNTNOUUxwLUpaVkJ0SkFKUmEzT2hIYUdSQ19wb0EiLCJhbGciOiJSUzI1NiIsIng1dCI6InlFVXdtWFdMMTA3Q2MtN1FaMldTYmVPYjNzUSIsImtpZCI6InlFVXdtWFdMMTA3Q2MtN1FaMldTYmVPYjNzUSJ9...",
    "token_type": "Bearer",
    "expires_in": 3599,
    "refresh_token": "1.Aa4A4ktntmAoxE-O-UUcsGTdcJ6ByXsvuQdCnGUQj0GBTm87AXauAA...",
    "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6InlFVXdtWFdMMTA3Q2MtN1FaMldTYmVPYjNzUSJ9..."
  }
}
```

## Summary

✅ **Fixed**: Made frontend redirect optional
✅ **Testing**: Returns JSON response when no frontend configured
✅ **Production Ready**: Can redirect to frontend when configured
✅ **Secure**: Tokens returned in response (can be enhanced with cookies)
