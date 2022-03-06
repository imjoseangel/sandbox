#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass
import logging
import os
import sys
import time
import requests
from waitress import serve
from flask import Flask, request


def animation():
    anime = "|/-\\"
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write("\r" + anime[i % len(anime)])
        sys.stdout.flush()


@dataclass
class RunJob:

    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
        filename="iplogger.log",
        filemode="w"
    )

    @staticmethod
    def get_running():

        url = ("https://imjoseangel.eu")

        try:
            response = requests.request("GET", url)
            logging.info(request.environ)
            return response.text
        except NameError as e:
            logging.error(e)
            return None


app = Flask(__name__)
jobrequests = RunJob()


@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        # logging.info(operator.attrgetter(item)(request))
        return jobrequests.get_running()

    return None


def main():
    """
    Main function
    """
    os.system('clear')

    print(""" ██▓ ██▓███   ██▓     ▒█████    ▄████   ▄████ ▓█████  ██▀███
▓██▒▓██░  ██▒▓██▒    ▒██▒  ██▒ ██▒ ▀█▒ ██▒ ▀█▒▓█   ▀ ▓██ ▒ ██▒
▒██▒▓██░ ██▓▒▒██░    ▒██░  ██▒▒██░▄▄▄░▒██░▄▄▄░▒███   ▓██ ░▄█ ▒
░██░▒██▄█▓▒ ▒▒██░    ▒██   ██░░▓█  ██▓░▓█  ██▓▒▓█  ▄ ▒██▀▀█▄
░██░▒██▒ ░  ░░██████▒░ ████▓▒░░▒▓███▀▒░▒▓███▀▒░▒████▒░██▓ ▒██▒
░▓  ▒▓▒░ ░  ░░ ▒░▓  ░░ ▒░▒░▒░  ░▒   ▒  ░▒   ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
 ▒ ░░▒ ░     ░ ░ ▒  ░  ░ ▒ ▒░   ░   ░   ░   ░  ░ ░  ░  ░▒ ░ ▒░
 ▒ ░░░         ░ ░   ░ ░ ░ ▒  ░ ░   ░ ░ ░   ░    ░     ░░   ░
 ░               ░  ░    ░ ░        ░       ░    ░  ░   ░
                                                            """)
    try:
        serve(app)
    except OSError as e:
        logging.error(e)


if __name__ == '__main__':
    main()
