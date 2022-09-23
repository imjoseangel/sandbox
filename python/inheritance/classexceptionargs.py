class EmailError(ValueError):
    def __init__(self, status, message):
        self.status = status
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.status}: {self.message}"


email = "admin#libray.net"
try:
    if "@" not in email:
        raise EmailError("pending!", "wrong format!")
except EmailError as e:
    print(e)
