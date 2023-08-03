from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

ACCOUNT_URL = "https://stnarmhub.blob.core.windows.net"
default_credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(ACCOUNT_URL,
                                        credential=default_credential)
LOCAL_FILE_NAME = "rabbitm-backup.json"
CONTANER_NAME = str("rabbitbackup")

blob_client = blob_service_client.get_blob_client(container=CONTANER_NAME, blob=LOCAL_FILE_NAME)

with open(file=LOCAL_FILE_NAME, mode="rb") as data:
    blob_client.upload_blob(data)
