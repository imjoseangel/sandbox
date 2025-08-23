#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import base64
import hashlib
import json
import os
import secrets
import threading
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import httpx
from fastmcp import Client

# Configuration
OKTA_DOMAIN = os.getenv("OKTA_DOMAIN", "https://dev-12345.okta.com")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID", "0oa5xyz123456789abc")
OKTA_ISSUER = os.getenv("OKTA_ISSUER", f"{OKTA_DOMAIN}/oauth2/default")
OKTA_REDIRECT_URI = "http://localhost:3000/login/callback"
AUTH_TIMEOUT = 60
SERVER_URL = "http://localhost:8080/sse"


class OktaOAuthClient:
    """Handles Okta OAuth2 authentication with PKCE"""

    def __init__(self):
        self.code_verifier: str | None = None
        self.authorization_code: str | None = None
        self.server = None

    def generate_pkce_pair(self):
        """Generate PKCE code verifier and code challenge"""
        self.code_verifier = base64.urlsafe_b64encode(
            secrets.token_bytes(32)).decode('utf-8').rstrip('=')

        challenge_bytes = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(
            challenge_bytes).decode('utf-8').rstrip('=')

        return self.code_verifier, code_challenge

    def create_callback_handler(self):
        """Create callback handler class with access to self"""
        oauth_client = self

        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path.startswith('/login/callback'):
                    parsed_url = urlparse(self.path)
                    query_params = parse_qs(parsed_url.query)

                    if 'code' in query_params:
                        oauth_client.authorization_code = query_params['code'][0]
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b'<html><body><h1>Authorization successful!</h1></body></html>')
                    else:
                        self.send_response(400)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b'<html><body><h1>Authorization failed!</h1></body></html>')
                else:
                    self.send_response(404)
                    self.end_headers()

        return CallbackHandler

    async def get_access_token(self):
        """Get access token using OAuth2 with PKCE"""
        print("🔐 Starting OAuth2 authentication...")

        # Generate PKCE pair
        _, code_challenge = self.generate_pkce_pair()

        # Start callback server
        self.server = HTTPServer(('localhost', 3000), self.create_callback_handler())
        self.server.timeout = 1

        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        try:
            # Build and open authorization URL
            auth_params = {
                'client_id': OKTA_CLIENT_ID,
                'response_type': 'code',
                'scope': 'openid profile email',
                'redirect_uri': OKTA_REDIRECT_URI,
                'state': 'state123',
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256'
            }

            auth_url = f"{OKTA_ISSUER}/v1/authorize?"
            auth_url += "&".join([f"{k}={v}" for k, v in auth_params.items()])

            print("Opening browser for authentication...")
            webbrowser.open(auth_url)

            # Wait for authorization code
            await self._wait_for_authorization()

            # Exchange code for token
            return await self._exchange_code_for_token()

        finally:
            if self.server:
                self.server.shutdown()
                self.server.server_close()

    async def _wait_for_authorization(self):
        """Wait for authorization callback"""
        print("Waiting for authorization callback...")
        start_time = time.time()

        while not self.authorization_code:
            if time.time() - start_time > AUTH_TIMEOUT:
                raise TimeoutError("Authorization timed out")
            await asyncio.sleep(0.5)

    async def _exchange_code_for_token(self):
        """Exchange authorization code for access token"""
        print("🔄 Exchanging authorization code for token...")

        token_url = f"{OKTA_ISSUER}/v1/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': OKTA_CLIENT_ID,
            'code': self.authorization_code,
            'redirect_uri': OKTA_REDIRECT_URI,
            'code_verifier': self.code_verifier
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data, headers=headers)

            if response.status_code == 200:
                token_data = response.json()
                print("✅ Access token received!")
                return token_data['access_token']
            else:
                raise ValueError(f"Token exchange failed: {response.status_code} - {response.text}")


def decode_jwt_payload(token):
    """Decode JWT payload for debugging"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None

        payload = parts[1]
        padding = 4 - (len(payload) % 4)
        if padding != 4:
            payload += '=' * padding

        decoded_bytes = base64.urlsafe_b64decode(payload)
        return json.loads(decoded_bytes)
    except (ValueError, json.JSONDecodeError):
        return None


async def demo_mcp_calls(client):
    """Demonstrate MCP server calls"""
    print("\n🔧 Testing MCP server functionality...")

    # Call the 'greet' tool
    greet_result = await client.call_tool("greet", {"name": "Okta User"})
    print(f"greet result: {greet_result}")

    # Read the 'config' resource
    config_data = await client.read_resource("data://config")
    print(f"config resource: {config_data}")

    # Read user profile
    profile_102 = await client.read_resource("users://102/profile")
    print(f"User 102 profile: {profile_102}")

    # Call the 'add' tool
    add_result = await client.call_tool("add", {"a": 15, "b": 27})
    print(f"add result: {add_result}")


async def main():
    """Main function"""
    print("=== FastMCP Client with Okta Authentication ===")
    print(f"🏢 Okta Domain: {OKTA_DOMAIN}")
    print(f"🆔 Client ID: {OKTA_CLIENT_ID}")
    print(f"🔗 Redirect URI: {OKTA_REDIRECT_URI}")
    print()

    try:
        # Authenticate with Okta
        oauth_client = OktaOAuthClient()
        access_token = await oauth_client.get_access_token()

        # Display token info
        payload = decode_jwt_payload(access_token)
        if payload:
            print("\n--- JWT Token Information ---")
            for key in ['sub', 'email', 'name', 'iss', 'aud', 'iat', 'exp', 'scp']:
                print(f"{key.capitalize()}: {payload.get(key, 'N/A')}")

        # Connect to MCP server
        print(f"\n� Connecting to FastMCP server: {SERVER_URL}")
        client = Client(SERVER_URL, auth=access_token)

        async with client:
            print("✅ Connected to FastMCP server")
            await demo_mcp_calls(client)

    except (ConnectionError, TimeoutError, ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Cancelled by user")
    finally:
        print("\n--- Session finished ---")


if __name__ == "__main__":
    print("🚀 Starting FastMCP Okta Client")
    asyncio.run(main())
