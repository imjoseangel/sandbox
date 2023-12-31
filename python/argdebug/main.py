#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys


class ParseArgs():
    """ Parse command line arguments """

    def __init__(self) -> None:

        self.debug = {0: "NOTSET",
                      1: "DEBUG",
                      2: "INFO",
                      3: "WARNING",
                      4: "ERROR",
                      5: "CRITICAL"}

        # Parse arguments passed at cli
        self.parse_arguments()

        logging.basicConfig(format="%(asctime)s - %(levelname)-8s - %(name)s - %(message)s",
                            datefmt="%d-%m-%y %H:%M:%S",
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
                            choices=range(0, 6),
                            required=False,
                            default=3)

        self.args = parser.parse_args()


def main():
    ParseArgs()

    logging.info("Test message")
    logging.critical("Test message")


if __name__ == '__main__':
    main()
