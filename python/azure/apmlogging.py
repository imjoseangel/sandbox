#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
APM Test for Azure Logging
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import logging

logger = logging.getLogger(__name__)


def valuePrompt():
    """
    This function prompts the user for a value.
    """
    line = input("Enter a value: ")
    logger.warning(line)


def main():
    """
    Main function
    """

    while True:
        valuePrompt()


if __name__ == '__main__':
    main()
