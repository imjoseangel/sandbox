import hmac
import hashlib

counter = 1
seed = "123456"

message = f"{seed}{counter}"

signature = hmac.new(
    bytes(seed, 'utf-8'),
    msg=bytes(message, 'utf-8'),
    digestmod=hashlib.sha256
).hexdigest().upper()

print(signature)
