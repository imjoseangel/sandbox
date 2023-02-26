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
