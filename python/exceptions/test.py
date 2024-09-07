#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    while True:
        try:
            x = input('enter something >>> ')
            print(x)
        except BaseException as e:  # Don't use this
            print('exception', e)


if __name__ == '__main__':
    main()
