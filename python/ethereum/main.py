#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ethereum main module.
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from web3 import Web3


def main():
    """
    Main function
    """
    print(Web3.toWei(1, 'ether'))

    print(Web3.fromWei(500000000, 'gwei'))


if __name__ == '__main__':
    main()
