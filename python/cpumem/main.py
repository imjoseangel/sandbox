#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import logging
import psutil


def main():
    """
    Main function
    """

    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logger.info("CPU usage: %s", psutil.cpu_percent())
    logger.info("Memory usage: %s", psutil.virtual_memory().percent)
    logger.info("Disk usage: %s", psutil.disk_usage('/').percent)


if __name__ == '__main__':
    main()
