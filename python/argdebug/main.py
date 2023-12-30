#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


class ParseArgs():
    """ Parse command line arguments """

    def __init__(self) -> None:

        # Parse arguments passed at cli
        self.parse_arguments()

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
                            required=False,
                            default=0)

        self.args = parser.parse_args()


def main():
    options = ParseArgs()


if __name__ == '__main__':
    main()
