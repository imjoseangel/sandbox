import re
import string
import random
import itertools
import numpy as np


def count_doubles_numpy(val):
    ng = np.fromstring(val, dtype=np.byte)
    return np.sum(ng[:-1] == ng[1:])


def count_doubles_comprehension(val):
    return sum(1 for c1, c2 in zip(val, val[1:]) if c1 == c2)


def count_doubles(val):
    """Count repeated pair of chars ins a string"""
    total = 0
    for c1, c2 in zip(val, val[1:]):
        if c1 == c2:
            total += 1
    return total


def count_doubles_itertools(val):
    c1s, c2s = itertools.tee(val)
    next(c2s, None)
    total = 0
    for c1, c2 in zip(c1s, c2s):
        if c1 == c2:
            total += 1
    return total


def count_doubles_once(val):
    total = 0
    chars = iter(val)
    c1 = next(chars)
    for c2 in chars:
        if c1 == c2:
            total += 1
        c1 = c2
    return total


double_re = re.compile(r'(?=(.)\1)')


def count_doubles_regex(val):
    return len(double_re.findall(val))


val = ''.join(random.choice(string.ascii_letters) for i in range(1000000))


def test_pure_python(benchmark):
    benchmark(count_doubles, val)


def test_regex(benchmark):
    benchmark(count_doubles_regex, val)


def test_itertools(benchmark):
    benchmark(count_doubles_itertools, val)


def test_python_comprenhension(benchmark):
    benchmark(count_doubles_comprehension, val)


def test_pure_python_once(benchmark):
    benchmark(count_doubles_once, val)


def test_numpy(benchmark):
    benchmark(count_doubles_numpy, val)
