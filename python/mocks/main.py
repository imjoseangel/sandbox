#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import mock


regular = mock.MagicMock()


def do_something(o):
    return o.something() + 1


obj = mock.MagicMock(name="an object")
obj.something.return_value = 2
print(do_something(obj))
