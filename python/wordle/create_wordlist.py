#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import sys
from string import ascii_letters

try:
    in_path = pathlib.Path(sys.argv[1])
    out_path = pathlib.Path(sys.argv[2])
except IndexError as e:
    print(e)
    sys.exit(1)

try:
    words = sorted(
        {
            word.lower()
            for word in in_path.read_text(encoding="utf-8").split()
            if all(letter in ascii_letters for letter in word)
        },
        key=lambda word: (len(word), word),
    )
    out_path.write_text("\n".join(words), encoding="utf-8")

except FileNotFoundError as e:
    print(e)
    sys.exit(1)
