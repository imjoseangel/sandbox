#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hashlib
import json
import time
import uuid
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

# Azure Key Vault details
vault_url = "https://your-key-vault-name.vault.azure.net"
key_name = "your-rsa-key-name"

# JWT claims
claims = {
    "iss": "your-client-id",
    "sub": "integration-user",
    "aud": "https://test.example.com",
    "exp": int(time.time()) + 600,  # Expiry time (10 minutes from now)
    "jti": str(uuid.uuid4()),  # Unique identifier for replay attack prevention
}

# Create a JWT header
header = {"alg": "RS256", "typ": "JWT"}

# Serialize and base64 URL encode the header and payload
header_and_payload = f"{base64.urlsafe_b64encode(json.dumps(header).encode()).decode()}.{base64.urlsafe_b64encode(json.dumps(claims).encode()).decode()}"

# Authenticate to Azure Key Vault
credential = DefaultAzureCredential()
key_client = KeyClient(vault_url, credential)
key = key_client.get_key(key_name)

# Create a CryptographyClient for signing
crypto_client = CryptographyClient(key, credential)
digest = hashlib.sha256(header_and_payload.encode()).digest()
signature = crypto_client.sign(SignatureAlgorithm.rs256, digest)

# Create the final JWT
jwt_token = f"{header_and_payload}.{base64.urlsafe_b64encode(signature).decode()}"

print(f"Encoded JWT: {jwt_token}")
