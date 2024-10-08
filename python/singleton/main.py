class _SingletonWrapper:
    """
    A singleton wrapper class. Its instances would be created
    for each decorated class.
    """

    def __init__(self, cls):
        self.__wrapped__ = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        """Returns a single instance of decorated class"""
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance


def singleton(cls):
    """
    A singleton decorator. Returns a wrapper object. A call on that object
    returns a single instance object of decorated class. Use the __wrapped__
    attribute to access the decorated class directly in unit tests.
    """
    return _SingletonWrapper(cls)


@singleton
class Logger:
    def __init__(self):
        self.log = []

    def write_log(self, message):
        self.log.append(message)

    def read_log(self):
        return self.log


logger1 = Logger()
logger2 = Logger()
logger3 = Logger()

logger1.write_log("Log message 1")
print(logger2.read_log())  # Output: ['Log message 1']

print(logger1 is logger2)  # Output: True

print(logger1 is logger3)  # Output: True
