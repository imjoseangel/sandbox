import asyncio
import base64
import binascii
import json
import traceback

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


async def interact_with_server():
    print("--- Creating Client ---")

    # JWT token for authentication
    jwt_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyLTEyMyIsIm5hbWUiOiJKb2huIERvZSIsImlhdCI6MTc1NTgxMzE5NSwiZXhwIjoxNzU1ODE0OTk1LCJpc3MiOiJodHRwczovL2F1dGguZXhhbXBsZS5jb20iLCJhdWQiOiJtY3AtcHJvZHVjdGlvbi1hcGkifQ.T5h_BuRU94Qw0uE1kboh4qpM6O4DpeYiF4VfG8nKdZfUvQESQDqqToF_GC7Xwtk4loCoNzme9cIuGeFdo2d3svmystw2nkNdoxlFfFrolgTTQHRf_gSBEiLM2Mxj1tqGhJZCvBCGUKZ_Gm7IAFMSWBoGF_NCjRO2BW25HB4Dc7Uc5dvsHmj4xv3PwbO0Wy_kXdDFM5-QzJnSGOTYylbhbfkhz8POZBhPYPVl1zrOotqqSLvOJv-qr61WsQLdohNaUh0RzgoJBaXF-5rha3JA_9Byw82W6D1nOnEcE1CJ5b8P-mHZD5ayok1Fq9xkjhYX9r5yEmKQebNb2w0musbzPA"

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
