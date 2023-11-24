from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError

URL = "https://mycosmos.documents.azure.com"
KEY = "mykey=="

try:
    client = CosmosClient(URL, credential=KEY)
    print(client)
except CosmosHttpResponseError as e:
    print(e)


database_name = "mydb"
container_name = "mycontainer"

database_obj = client.get_database_client(database_name)

todo_items_container = database_obj.get_container_client(container_name)
todo_items_container.read()
