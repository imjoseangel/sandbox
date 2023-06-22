#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import sys


def main():

    for counter in range(0, 1000000):
        for seed in range(0, 1000000):
            my_str = f"{seed:06d}{counter}"
            my_hash = hashlib.sha256(my_str.encode('UTF-8')).hexdigest()

            # print(my_str)

            # print(my_hash[0:6])

            if my_hash[0:6] == "42126c":
                # print(my_hash[0:6])
                file1 = open("42126c.txt", "a")
                file1.write(f"{seed:06d}\n")
                print(f"{seed:06d}")
                # sys.exit(0)


if __name__ == '__main__':
    main()
