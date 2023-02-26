#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dis

# This is equal 3
(lambda x: print(x + 1))(2)

# And this
add_one = (lambda x: x + 1)
print(add_one(2))

# This prints Full name: Guido Van Rossum
full_name = (lambda first, last: f'Full name: {first.title()} {last.title()}')
print(full_name('guido', 'van rossum'))

# This is equal 5
(lambda x, y: print(x + y))(2, 3)


# This is equal 6 and 7 respectively
high_ord_func = (lambda x, func: x + func(x))

print(high_ord_func(2, lambda x: x * x))
print(high_ord_func(2, lambda x: x + 3))

# Inspect Lambdas

add = (lambda x, y: x + y)
print(type(add))

dis.dis(add)
print(add)


def add(x, y): return x + y


print(type(add))

dis.dis(add)
print(add)

# Multiline

print((lambda x:
      (x % 2 and 'odd' or 'even'))(3))

lambda x: x % 2 and 'odd' or 'even'

# Arguments all printing 6

print((lambda x, y, z: x + y + z)(1, 2, 3))

print((lambda x, y, z=3: x + y + z)(1, 2))

print((lambda x, y, z=3: x + y + z)(1, y=2))

print((lambda *args: sum(args))(1, 2, 3))

print((lambda **kwargs: sum(kwargs.values()))(one=1, two=2, three=3))

print((lambda x, *, y=0, z=0: x + y + z)(1, y=2, z=3))


# Defining a decorator
def trace(f):
    def wrap(*args, **kwargs):
        print(f"[TRACE] func: {f.__name__}, args: {args}, kwargs: {kwargs}")
        return f(*args, **kwargs)

    return wrap

# Applying decorator to a function


@trace
def add_two(x):
    return x + 2


# Calling the decorated function
print(add_two(3))

# Applying decorator to a lambda
print(trace(lambda x: x ** 2)(3))


print(list(map(trace(lambda x: x * 2), range(3))))


# Closures

def outer_func(x):
    y = 4
    return lambda z: x + y + z


for i in range(3):
    closure = outer_func(i)
    print(f"closure({i+5}) = {closure(i+5)}")


# Evaluation

numbers = 'one', 'two', 'three'
funcs = []

for n in numbers:
    funcs.append(lambda n=n: print(n))

for f in funcs:
    f()
