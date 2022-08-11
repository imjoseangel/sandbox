import os

from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

clientid = os.getenv('AZURE_CLIENT_ID')
clientsecret = os.getenv('AZURE_CLIENT_SECRET')
tenantid = os.getenv('AZURE_TENANT_ID')
secretName = os.getenv('AZURE_SECRET_NAME')
keyVaultName = os.getenv('AZURE_KEY_VAULT_NAME')


KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = ClientSecretCredential(client_id=clientid,
                                    client_secret=clientsecret,
                                    tenant_id=tenantid)

client = SecretClient(vault_url=KVUri, credential=credential)

print(f"Retrieving your secret from {keyVaultName}.")

retrieved_secret = client.get_secret(secretName)
print(f"Your secret is '{retrieved_secret.value}'.")
print("done.")
