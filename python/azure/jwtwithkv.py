#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import jwt
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.core.exceptions import ResourceNotFoundError
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm


VAULT_URL = "https://nine.vault.azure.net"
PAYLOAD = {'some': 'payload'}


def main():
    credential = DefaultAzureCredential()
    client = KeyClient(vault_url=VAULT_URL, credential=credential)

    with open('jwtRS256.key.pub', mode='rb') as public_file:
        public_key = public_file.read()

    with open('jwtRS256.key', mode='rb') as private_file:
        private_key = private_file.read()

    try:
        key = client.get_key("test")
        crypto_client = CryptographyClient(key, credential=credential)
    except ResourceNotFoundError as e:
        print(f'Error {e}')
        sys.exit(1)

    # encoded_jwt = crypto_client.encrypt(
    #     EncryptionAlgorithm.rsa_oaep, PAYLOAD)
    encoded_jwt = jwt.encode(PAYLOAD, key=private_key, algorithm="RS256")

    print(f"Encoded JWT: {encoded_jwt}")

    decoded_jwt = jwt.decode(encoded_jwt, public_key, algorithms=["RS256"])
    print(f"Decoded JWT: {decoded_jwt}")


if __name__ == '__main__':
    main()
