import hmac
import hashlib
import sys

for counter in range(0, 1000000):
    for seed in range(0, 1000000):
        message = f"{seed}{counter}"

        signature = hmac.new(
            bytes(str(seed), 'utf-8'),
            msg=bytes(message, 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        print(signature[0:6])

        if signature[0:6] == "42126c":
            print(seed)
            sys.exit(0)
