import os

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

secretName = os.getenv('AZURE_SECRET_NAME')
keyVaultName = os.getenv('AZURE_KEY_VAULT_NAME')

KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()

client = SecretClient(vault_url=KVUri, credential=credential)

print(f"Retrieving your secret from {keyVaultName}.")

try:
    retrieved_secret = client.get_secret(secretName)
    print(f"Your secret is '{retrieved_secret.value}'.")
except ValueError:
    pass


print("done.")
