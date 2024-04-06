def add(symbol):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            return func(*args, **kwargs) + symbol
        return wrapper2
    return wrapper1


@add('!!')
def hello(name):
    return 'hello ' + name


print(hello('tom'))
