import random


def get_seed(rolling_code):
    for i in range(0, 0x1000000):
        random.seed(i)
        if rolling_code == random.randint(0, 0xffffff):
            return i
    return None


print(get_seed(0x42126c))
print(get_seed(0xd358f6))
