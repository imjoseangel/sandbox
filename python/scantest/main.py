#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import nmap
import logging
import sys


def main():
    """
    Main function
    """

    # Add logging
    logging.basicConfig(format="%(asctime)s - %(message)s",
                        datefmt="%d-%b-%y %H:%M:%S", stream=sys.stderr, level=logging.DEBUG)

    # Initialize
    nmScan = nmap.PortScanner()

    # Scan
    nmScan.scan('10.100.10.0/16', '21', arguments='-O')

    # run a loop to print all the found result about the ports
    for host in nmScan.all_hosts():
        print(f'Host : {host} {nmScan[host].hostname()}')
        print(f'State : {nmScan[host].state()}')
        print(f'OS: {nmScan[host]["osmatch"][0]["osclass"][0]["osfamily"]}')

        if nmScan[host]["osmatch"][0]["osclass"][0]["osfamily"] == "Windows":

            for proto in nmScan[host].all_protocols():
                print('----------')
                print(f'Protocol : {proto}')

                lport = nmScan[host][proto].keys()
                print(lport)

                for port in lport:
                    print(
                        f'port : {port}\tstate : {nmScan[host][proto][port]["state"]}')


if __name__ == '__main__':
    main()
