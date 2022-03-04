#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass
import logging
import sys
from waitress import serve
import requests
from flask import Flask, request


@dataclass
class RunJob:

    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
        stream=sys.stderr,
    )

    def get_running(self):

        url = ("https://www.google.com")

        try:
            response = requests.request("GET", url)
        except NameError as e:
            logging.error(e)

        return f'{{{response.text}}}'


app = Flask(__name__)
jobrequests = RunJob()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        return jobrequests.get_running()
    else:
        return 'GET Method not allowed'


def main():
    try:
        serve(app)
    except OSError as e:
        logging.error(e)


if __name__ == '__main__':
    main()
