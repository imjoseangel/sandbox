#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NBA Test
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import datetime
import json
import requests


def get_json():

    mainjsn = "https://data.nba.net/data/10s/prod/v1/calendar.json"
    nbanet = requests.get(mainjsn)
    nbadates = json.loads(nbanet.content)

    output = (datetime.datetime.strptime(nbadate, '%Y%m%d')
              for nbadate in nbadates)


def main():
    """
    Main function
    """


if __name__ == '__main__':
    main()
