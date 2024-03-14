#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jwt
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient


VAULT_URL = "https://mykv.vault.azure.net"
PAYLOAD = {'some': 'payload'}


def main():
    credential = DefaultAzureCredential()
    client = KeyClient(vault_url=VAULT_URL, credential=credential)

    key = client.get_key("jwt")
    crypto_client = CryptographyClient(key, credential=credential)

    encoded_jwt = jwt.encode(PAYLOAD, key=key.key.n, algorithm="HS256")

    print(f"Encoded JWT: {encoded_jwt}")


if __name__ == '__main__':
    main()
