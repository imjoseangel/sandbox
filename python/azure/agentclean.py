#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import base64
import json
import logging
import sys
import requests

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%d-%b-%y %H:%M:%S",
    stream=sys.stderr,
)

secret = os.getenv("ADV_TOKEN", "")
organization = os.getenv("ADV_ORG", "inc")
poolid = os.getenv("ADV_POOL", "1")

auth = f':{secret}'
encodeauth = base64.b64encode(auth.encode('utf-8'))

headers = {
    'Authorization':
    f'Basic {encodeauth.decode("utf-8")}'
}

url = (
    f"https://dev.azure.com/{organization}/"
    f"_apis/distributedtask/pools/{poolid}/agents")

response = requests.request("GET", url, headers=headers)

if response.ok:
    try:
        data = json.loads(response.text).get("value")

        try:
            for item in data:
                if item['status'] == 'offline':
                    print(item)
        except NameError as e:
            logging.error(e)

    except json.JSONDecodeError as e:
        logging.error(e)
