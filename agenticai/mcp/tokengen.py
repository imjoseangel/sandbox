#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import jwt

# --- Token Generation with Private Key ---

# 1. Read the private key from the file
with open("private_key.pem", "r", encoding="utf-8") as f:
    private_key_pem = f.read()

# 2. Define the JWT payload
# This is the data you want to store in the token.
payload = {
    "sub": "user-123",
    "name": "John Doe",
    "iat": datetime.datetime.now(tz=datetime.timezone.utc),
    "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30),
    "iss": "https://auth.example.com",
    "aud": "mcp-production-api"
}

# 3. Create the JWT using the private key
# We use the RS256 algorithm, which is a common choice for RSA keys.
token = None
try:
    token = jwt.encode(payload, private_key_pem, algorithm="RS256")
    print("Generated JWT:")
    print(token)
except (jwt.InvalidKeyError, ValueError, TypeError) as e:
    print(f"Error encoding token: {e}")
    token = None

# --- Token Verification with Public Key ---

if token:
    # 4. Read the public key from the file
    with open("public_key.pem", "r", encoding="utf-8") as f:
        public_key_pem = f.read()

    # 5. Verify and decode the JWT using the public key
    try:
        decoded_payload = jwt.decode(
            token,
            public_key_pem,
            algorithms=["RS256"],
            issuer="https://auth.example.com",
            audience="mcp-production-api"
        )
        print("\nSuccessfully decoded JWT payload:")
        print(decoded_payload)
    except jwt.InvalidSignatureError:
        print("\nVerification failed: Invalid signature.")
    except jwt.ExpiredSignatureError:
        print("\nVerification failed: Token has expired.")
    except jwt.InvalidIssuerError:
        print("\nVerification failed: Invalid issuer.")
    except jwt.InvalidAudienceError:
        print("\nVerification failed: Invalid audience.")
    except (jwt.InvalidTokenError, jwt.DecodeError) as e:
        print(f"\nAn error occurred during verification: {e}")


# Generate a private key
# openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Extract the public key from the private key
# openssl pkey -in private_key.pem -pubout -out public_key.pem

# pip install PyJWT cryptography
