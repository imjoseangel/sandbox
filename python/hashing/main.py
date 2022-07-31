#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from getpass import getpass
import bcrypt


def main():
    passwd = getpass('Password: ')

    hashed = bcrypt.hashpw(passwd.encode('UTF-8'), bcrypt.gensalt())
    check = bcrypt.checkpw(passwd.encode('UTF-8'), hashed)

    print(f'Hashed: {hashed.decode("UTF-8")}')
    print(f'Check: {check}')


if __name__ == '__main__':
    main()
