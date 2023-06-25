#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import sys


def main():

    for counter in range(0, 100):
        for seed in range(0, 100000000):
            my_str = f"{seed:06d}{counter}"
            my_hash = hashlib.sha256(my_str.encode('UTF-8')).hexdigest()

            # print(my_str)

            # print(my_hash[0:6])

            if my_hash[0:6] == "42126c":
                # print(my_hash[0:6])
                print(f"{seed:06d}")
                counter += 1
                # sys.exit(0)
                new_str = f"{seed:06d}{counter}"
                new_hash = hashlib.sha256(new_str.encode('UTF-8')).hexdigest()
                print(new_hash[0:6])


if __name__ == '__main__':
    main()
