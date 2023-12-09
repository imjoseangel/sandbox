#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


def l(kla0, lil1):
    result = ""
    for tuj2, item in enumerate(kla0):
        result += chr(ord(item) ^ ord(lil1[tuj2 % len(lil1)]))
    return result


ss = "#515551"

x = l("3c3c3c", ss)

print(hashlib.md5(x.encode()).hexdigest())
