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

    date = '20181019'

    jsn = f"https://data.nba.net/10s/prod/v1/{date}/scoreboard.json"
    page = requests.get(jsn)
    j = json.loads(page.content)

    print(j)


if __name__ == '__main__':
    main()
