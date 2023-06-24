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

        if signature[0:6] == "42126c":
            print(seed, "", counter)

            for counter in range(0, 1000000):
                message = f"{seed}{counter}"

                signature = hmac.new(
                    bytes(str(seed), 'utf-8'),
                    msg=bytes(message, 'utf-8'),
                    digestmod=hashlib.sha256
                ).hexdigest()

                if signature[0:6] == "d358f6":
                    print("FOUND")
                    print(seed, "", counter)
