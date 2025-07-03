from base64 import b64encode
from gradio_client import Client


username = "myuser"
password = "mypassword"


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


headers = {'Authorization': basic_auth(username, password)}

client = Client("https://myurl.com",
                headers=headers)

result = client.predict(
    message="Hello!!",
    api_name="/chat"
)
print(result)
