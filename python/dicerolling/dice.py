#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    """
    ~~~ App's main code block ~~~
    1. Get and validate user's input
    """

    num_dice_input = input("How many dice do you want to roll? [1-6] ")
    num_dice = parse_input(num_dice_input)


if __name__ == '__main__':
    main()
