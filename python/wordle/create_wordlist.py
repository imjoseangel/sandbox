#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import sys
from string import ascii_letters
import re

try:
    in_path = pathlib.Path(sys.argv[1])
except IndexError as e:
    print("Missing source file")
    sys.exit(1)

try:
    out_path = pathlib.Path(sys.argv[2])
except IndexError as e:
    print("Missing destination file")
    sys.exit(1)

try:
    words = sorted(
        {
            word.lower()
            for word in in_path.read_text(encoding="utf-8").split()
            if all(letter in ascii_letters for letter in word)
            # if re.fullmatch(r"\w+", word)
        },
        key=lambda word: (len(word), word),
    )
    print(words)
    out_path.write_text("\n".join(words), encoding="utf-8")

except FileNotFoundError as e:
    print(e)
    sys.exit(1)
