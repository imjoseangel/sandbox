#!/usr/bin/env python
# -*- coding: utf-8 -*-

def show_parents(exception):
    while exception:
        print(exception)
        try:
            exception = exception.__bases__[0]
        except:
            break


def main():
    show_parents(ZeroDivisionError)
    show_parents(KeyError)


if __name__ == '__main__':
    main()
