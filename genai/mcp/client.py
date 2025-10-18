import asyncio
import base64
import binascii
import json
import os
import traceback

import requests

from fastmcp import Client


def decode_jwt_payload(token):
    """Decode JWT payload for debugging (without verification)"""
    try:
        # Split the token into parts
        parts = token.split('.')
        if len(parts) != 3:
            return None

        # Decode the payload (second part)
        payload = parts[1]
        # Add padding if necessary
        padding = 4 - (len(payload) % 4)
        if padding != 4:
            payload += '=' * padding

        decoded_bytes = base64.urlsafe_b64decode(payload)
        payload_data = json.loads(decoded_bytes)
        return payload_data
    except (ValueError, json.JSONDecodeError, binascii.Error) as e:
        print(f"Error decoding JWT: {e}")
        return None


def get_okta_access_token(okta_domain, client_id, client_secret, scope="api.read"):
    """Obtain an access token from Okta using client credentials flow."""
    token_url = f"{okta_domain}/oauth2/default/v1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": scope
    }
    auth = (client_id, client_secret)
    response = requests.post(token_url, headers=headers,
                             data=data, auth=auth, timeout=10)
    if response.status_code != 200:
        print("Failed to get Okta token:")
        print("Status:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()
    return response.json()["access_token"]

def generate_token():
    """Generate a fresh JWT token using the private key"""
    with open("private_key.pem", "r", encoding="utf-8") as f:
        private_key_pem = f.read()

    payload = {
        "sub": "user-123",
        "name": "John Doe",
        "iat": datetime.datetime.now(tz=datetime.timezone.utc),
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30),
        "iss": "https://auth.example.com",
        "aud": "mcp-production-api"
    }

    return jwt.encode(payload, private_key_pem, algorithm="RS256")

async def interact_with_server():
    print("--- Creating Client ---")

    # JWT token for authentication
    # jwt_token = generate_token()

    # Okta configuration
    okta_domain = os.getenv("OKTA_DOMAIN", "https://dev-12345.okta.com")
    okta_client_id = os.getenv("OKTA_CLIENT_ID", "client_id")
    okta_client_secret = os.getenv("OKTA_CLIENT_SECRET", "client_secret")
    # Use a valid scope from your Okta authorization server
    okta_scope = os.getenv("OKTA_SCOPE", "api.read")

    # Obtain JWT token from Okta
    jwt_token = get_okta_access_token(
        okta_domain, okta_client_id, okta_client_secret, okta_scope)

    # Debug: Decode and display JWT payload
    payload = decode_jwt_payload(jwt_token)
    if payload:
        print("--- JWT Token Information ---")
        print(f"Subject: {payload.get('sub')}")
        print(f"Name: {payload.get('name')}")
        print(f"Issuer: {payload.get('iss')}")
        print(f"Audience: {payload.get('aud')}")
        print(f"Issued At: {payload.get('iat')}")
        print(f"Expires: {payload.get('exp')}")
        print(f"Full payload: {json.dumps(payload, indent=2)}")
        print()

    # Server URL
    server_url = "http://localhost:8080/sse"

    # Use the auth parameter with the JWT token (FastMCP automatically adds "Bearer ")
    client = Client(server_url, auth=jwt_token)

    print(
        f"Client configured to connect to: {server_url} with JWT authentication")

    try:
        async with client:
            print("--- Client Connected ---")
            # Call the 'greet' tool
            greet_result = await client.call_tool("greet", {"name": "Remote Client"})
            print(f"greet result: {greet_result}")

            # Read the 'config' resource
            config_data = await client.read_resource("data://config")
            print(f"config resource: {config_data}")

            # Read user profile 102
            profile_102 = await client.read_resource("users://102/profile")
            print(f"User 102 profile: {profile_102}")

    except (ConnectionError, TimeoutError, ValueError, RuntimeError) as e:
        print(f"An error occurred: {e}")
        print(f"Error type: {type(e).__name__}")
        traceback.print_exc()
    finally:
        print("--- Client Interaction Finished ---")


if __name__ == "__main__":
    asyncio.run(interact_with_server())
