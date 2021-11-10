"""RP To-Do entry point script."""
# rptodo/__main__.py
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from rptodo import cli, __app_name__


def main():
    cli.app(prog_name=__app_name__)


if __name__ == '__main__':
    main()
