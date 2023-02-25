#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is equel 3
(lambda x: print(x + 1))(2)

add_one = (lambda x: x + 1)
print(add_one(2))


full_name = (lambda first, last: f'Full name: {first.title()} {last.title()}')
print(full_name('guido', 'van rossum'))


(lambda x, y: print(x + y))(2, 3)


high_ord_func = (lambda x, func: x + func(x))

print(high_ord_func(2, lambda x: x * x))
print(high_ord_func(2, lambda x: x + 3))
