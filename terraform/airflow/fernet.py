import json
from cryptography.fernet import Fernet


FERNET_KEY = Fernet.generate_key().decode()

print(json.dumps({'value': FERNET_KEY}))
