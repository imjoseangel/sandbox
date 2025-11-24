# FastMCP with Okta Authentication Setup Guide

This guide shows you how to integrate Okta authentication with your FastMCP server and client.

## Prerequisites

1. **Okta Developer Account**: You need an Okta developer account. If you don't have one, sign up at [developer.okta.com](https://developer.okta.com/).

2. **Python Dependencies**: Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Okta Configuration

### Step 1: Create an Okta Application

1. **Sign in** to your Okta Developer Console
2. Go to **Applications** > **Applications**
3. Click **Create App Integration**
4. Choose **OIDC - OpenID Connect**
5. Choose **Single-Page Application (SPA)**
6. Configure the application:
   - **Name**: `FastMCP Client`
   - **Sign-in redirect URIs**: `http://localhost:3000/callback`
   - **Sign-out redirect URIs**: `http://localhost:3000`
   - **Controlled access**: Choose appropriate assignment (Everyone or specific groups)

### Step 2: Get Your Configuration Values

After creating the app, note down these values from the application settings:

- **Client ID**: Found in the "General" tab of your application
- **Okta Domain**: Your organization's Okta domain (e.g., `https://dev-12345.okta.com`)
- **Issuer**: Usually `{your-okta-domain}/oauth2/default`

### Step 3: Configure API Access (Optional)

If you want to use a custom audience:

1. Go to **Security** > **API**
2. Click on "default" authorization server (or create a new one)
3. Note the **Issuer** URL
4. Under **Scopes**, ensure you have appropriate scopes like `openid`, `profile`, `email`

## Environment Configuration

1. **Copy the environment template**:

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** with your Okta values:

   ```env
   OKTA_DOMAIN=https://dev-12345.okta.com
   OKTA_CLIENT_ID=0oa5xyz123456789abc
   OKTA_ISSUER=https://dev-12345.okta.com/oauth2/default
   OKTA_AUDIENCE=api://default
   ```

## Running the Application

### Step 1: Start the FastMCP Server

```bash
python server.py
```

This starts the server on `http://localhost:8080` with Okta JWT verification.

### Step 2: Run the Okta Client

```bash
python okta_client.py
```

This will:

1. Open your browser for Okta authentication
2. Handle the OAuth callback
3. Extract the access token
4. Connect to the FastMCP server with the token
5. Make authenticated requests to the server

## How It Works

### Server Side (`server.py`)

The server uses FastMCP's `JWTVerifier` configured with:

- **JWKS URI**: Okta's public key endpoint for token verification
- **Issuer**: Your Okta authorization server
- **Audience**: The intended audience for tokens

```python
verifier = JWTVerifier(
    jwks_uri=OKTA_JWKS_URI,
    issuer=OKTA_ISSUER,
    audience=OKTA_AUDIENCE
)
```

### Client Side (`okta_client.py`)

The client:

1. **Starts a local HTTP server** on port 3000 to handle OAuth callbacks
2. **Opens a browser** to Okta's authorization endpoint
3. **Handles the OAuth flow** (implicit flow for simplicity)
4. **Extracts the access token** from the callback
5. **Uses the token** to authenticate with the FastMCP server

### Authentication Flow

```
1. Client → Browser: Opens Okta login page
2. User → Okta: Enters credentials
3. Okta → Client: Redirects with access token
4. Client → Server: Sends requests with token
5. Server → Okta: Validates token using JWKS
6. Server → Client: Returns response if token is valid
```

## Troubleshooting

### Common Issues

1. **"Invalid Client" Error**:
   - Verify your `OKTA_CLIENT_ID` is correct
   - Ensure the redirect URI matches exactly (`http://localhost:3000/callback`)

2. **"Invalid Issuer" Error**:
   - Check your `OKTA_ISSUER` URL
   - Ensure it ends with `/oauth2/default` (or your custom auth server)

3. **"Invalid Audience" Error**:
   - Verify your `OKTA_AUDIENCE` setting
   - For default setup, use `api://default`

4. **Port 3000 Already in Use**:
   - Stop any other applications using port 3000
   - Or modify the `OKTA_REDIRECT_URI` in both files to use a different port

5. **Token Validation Fails**:
   - Ensure your Okta app is assigned to your user
   - Check that the scopes include `openid profile email`
   - Verify the token hasn't expired

### Debug Tips

1. **Check JWT Token**: The client decodes and displays JWT payload for debugging
2. **Server Logs**: Run the server with `log_level="DEBUG"` for detailed logs
3. **Network Issues**: Ensure you can reach both Okta and localhost from your machine

## Security Considerations

### Production Deployment

1. **Use Authorization Code Flow**: Replace implicit flow with PKCE for better security
2. **Secure Redirect URIs**: Use HTTPS and limit redirect URIs to your actual domains
3. **Token Storage**: Store tokens securely (not in memory/localStorage)
4. **Scope Limitation**: Request only necessary scopes
5. **Token Refresh**: Implement proper token refresh logic

### Environment Variables

Never commit your `.env` file with real credentials. The `.env.example` file shows the structure without exposing secrets.

## Advanced Configuration

### Custom Scopes

Add custom scopes in your Okta authorization server and request them in the client:

```python
auth_params = {
    'scope': 'openid profile email custom:read custom:write',
    # ... other params
}
```

### Claims Validation

You can extend the server to validate specific claims:

```python
# In your server, access token claims after verification
@mcp.tool()
def secure_operation() -> str:
    # The JWT verifier automatically validates standard claims
    # You can add custom claim validation here
    return "Secure operation completed"
```

### Multiple Authorization Servers

Configure multiple Okta authorization servers if needed:

```python
# For different environments or audiences
verifier = JWTVerifier(
    jwks_uri=f"{OKTA_ISSUER}/v1/keys",
    issuer=OKTA_ISSUER,
    audience=[OKTA_AUDIENCE, "api://mobile", "api://web"]
)
```

## Files Overview

- `server.py`: FastMCP server with Okta JWT verification
- `okta_client.py`: Client with Okta OAuth integration
- `client.py`: Original client with static JWT (for reference)
- `.env.example`: Environment template
- `requirements.txt`: Python dependencies
- `README.md`: This setup guide
