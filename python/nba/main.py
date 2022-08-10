#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NBA Scraper
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import cv2
import json
from moviepy.editor import *
import pandas as pd
import pytesseract
import requests


def main():
    """
    Main function
    """

    date = '20220616'
    # Note that the date is in the format YYYYMMDD
    # http://data.nba.net/data/10s/prod/v1/calendar.json

    jsn = f"https://data.nba.net/10s/prod/v1/{date}/scoreboard.json"
    page = requests.get(jsn)
    j = json.loads(page.content)

    game_id = j['games'][0]['gameId']
    raw_game = f'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{game_id}.json'
    page = requests.get(raw_game)
    j = json.loads(page.content)
    df = pd.DataFrame(j['game']['actions'])

    print(df)


if __name__ == '__main__':
    main()
