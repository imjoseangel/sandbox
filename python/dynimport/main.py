#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import importlib


def dynamic_import(module):
    return importlib.import_module(module)


def main():
    """
    Main function
    """
    module = dynamic_import('memory_profiler')
    print(module.memory_usage())

    module_two = dynamic_import('psutil')
    print(module_two.cpu_times())


if __name__ == '__main__':
    main()
