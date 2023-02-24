#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is equel 3
(lambda x: print(x + 1))(2)

add_one = (lambda x: x + 1)
print(add_one(2))


full_name = (lambda first, last: f'Full name: {first.title()} {last.title()}')
print(full_name('guido', 'van rossum'))
