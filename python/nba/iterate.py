#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NBA Test
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import json
import requests
import pandas as pd


def get_json():

    mainjsn = "https://data.nba.net/data/10s/prod/v1/calendar.json"
    nbanet = requests.get(mainjsn)

    nbadates = json.loads(nbanet.content)

    pdObj = (pd.read_json(json.dumps(game['games'])) for game in
             (json.loads(gameday.content) for gameday in (requests.get(
                 f"https://data.nba.net/10s/prod/v1/{nbadate}/scoreboard.json")
                 for nbadate in (nbadate for nbadate in nbadates
                                 if nbadate.startswith('20')))))


def main():
    """
    Main function
    """
    get_json()


if __name__ == '__main__':
    main()
