#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import TextIOBase
from unittest import mock


different_things = mock.MagicMock()
different_things.side_effect = [1, 2, 3]
print(different_things())
print(different_things())
print(different_things())


def parse_three_lines(fpin):
    line = fpin.readline()
    name, item = line.split()
    modifier = fpin.readline().strip()
    extra = fpin.readline().strip()
    return {name: f"{item}/{modifier}+{extra}"}


filelike = mock.MagicMock(spec=TextIOBase)
filelike.readline.side_effect = [
    "thing important\n",
    "a-little\n",
    "to-some-people\n"
]
value = parse_three_lines(filelike)
print(value)
