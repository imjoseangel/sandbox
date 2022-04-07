import functools
import time


def timer(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        runtime = time.perf_counter() - start
        print(f"{func.__name__} took {runtime:.4f} secs")
        return result
    return _wrapper


@timer
def complex_calculation():
    """Some complex calculation."""
    time.sleep(0.5)
    return 42


@timer
class MyClass:
    def complex_calculation(self):
        time.sleep(1)
        return 42


my_obj = MyClass()
my_obj.complex_calculation()
# print(complex_calculation())
