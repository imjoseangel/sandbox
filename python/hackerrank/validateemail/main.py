#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def fun(s):
    # return True if s is a valid email, else return False
    pass


def filter_mail(emails):
    return list(filter(fun, emails))


def main():
    n = int(input())
    emails = []
    for _ in range(n):
        emails.append(input())

    filtered_emails = filter_mail(emails)
    filtered_emails.sort()
    print(filtered_emails)


if __name__ == '__main__':
    main()
