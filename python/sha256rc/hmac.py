from Crypto.Hash import HMAC, SHA256


def calculateTag(key, data):
    hasher = HMAC.new(key, digestmod=SHA256)
    hasher.update(data)
    return hasher.digest()


def verifyTag(key, data, tag):
    hasher = HMAC.new(key, digestmod=SHA256)
    hasher.update(data)
    try:
        hasher.verify(tag)
        return True
    except ValueError:
        return False


calculateTag("42126c", "1687244585")
