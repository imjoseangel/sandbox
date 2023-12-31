#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys


class ParseArgs():
    """ Parse command line arguments """

    def __init__(self) -> None:

        self.debug = {0: "INFO",
                      1: "WARNING",
                      2: "DEBUG"}

        # Parse arguments passed at cli
        self.parse_arguments()

        logging.basicConfig(format="%(asctime)s - %(message)s",
                            datefmt="%d-%b-%y %H:%M:%S",
                            stream=sys.stdout,
                            level=eval(f'logging.{self.debug.get(self.args.verbose)}'))

    def parse_arguments(self):
        """ Parse arguments passed at cli """

        description = '''
        This program is used as example to use debug logging.
        '''

        parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument('-v', '--verbose',
                            help='enable verbose (default 0)',
                            type=int,
                            choices=range(0, 3),
                            required=False,
                            default=0)

        self.args = parser.parse_args()


def main():
    options = ParseArgs()


if __name__ == '__main__':
    main()
