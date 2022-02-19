#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def bonAppetit(bill, k, b):
    """
    Function to calculate the amount of money that Anna did not share with
    Bob.
    """

    anna_paid = sum(bill[:k] + bill[k + 1:])

    # Calculate the amount of money that Anna did not share with Bob.
    anna_did_not_share = int(anna_paid / 2)

    # Compare the amount of money that Anna did not share with Bob with the
    # amount of money that Bob paid to Anna.
    if anna_did_not_share == b:
        print('Bon Appetit')
    else:
        print(int(b - anna_did_not_share))


def main():
    """
    Main function
    """
    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])
    k = int(first_multiple_input[1])

    bill = list(map(int, input().rstrip().split()))

    b = int(input().strip())

    bonAppetit(bill, k, b)


if __name__ == '__main__':
    main()
