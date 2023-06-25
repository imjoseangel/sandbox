#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib



def main():

    for counter in range(0, 100000000):
        seed = 1687244585
        my_str = f"{seed}{counter}"
        my_hash = hashlib.sha256(my_str.encode('UTF-8')).hexdigest()

        # print(my_str)

        # print(my_hash[0:6])

        if my_hash[0:6] == "42126c":
            print(counter)


if __name__ == '__main__':
    main()
