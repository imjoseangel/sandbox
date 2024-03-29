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

secret = os.getenv("AZP_TOKEN", "")
organization = os.getenv("AZP_ORG", "inc")
poolname = os.getenv("AZP_POOL", "1")

auth = f':{secret}'
encodeauth = base64.b64encode(auth.encode('utf-8'))

headers = {
    'Authorization':
    f'Basic {encodeauth.decode("utf-8")}'
}

agentpools = (
    f"https://dev.azure.com/{organization}/"
    f"_apis/distributedtask/pools?poolName={poolname}")

agentpoolres = requests.request("GET", agentpools, headers=headers, timeout=10)

if agentpoolres.ok:
    try:
        data = json.loads(agentpoolres.text).get("value")
        poolid = data[0]['id']

        logging.info(f"Pool ID: {poolid}")

        agents = (
            f"https://dev.azure.com/{organization}/"
            f"_apis/distributedtask/pools/{poolid}/agents")

        poolres = requests.request("GET", agents, headers=headers, timeout=10)

        if poolres.ok:
            try:
                data = json.loads(poolres.text).get("value")
                logging.info(data)

                try:
                    for item in data:
                        if item['status'] == 'offline':
                            logging.info(f"{item['id']} is offline")
                            url = (
                                f"https://dev.azure.com/{organization}/"
                                f"_apis/distributedtask/pools/{poolid}/agents/"
                                f"{item['id']}?api-version=4.1")
                            response = requests.request(
                                "DELETE", url, headers=headers, timeout=10)
                            if response.ok:
                                logging.info(f"{item['id']} is deleted")
                            else:
                                logging.error(f"{item['id']} is not deleted")
                except NameError as e:
                    logging.error(e)

            except json.JSONDecodeError as e:
                logging.error(f'JSONDecodeError: {e}')

    except json.JSONDecodeError as e:
        logging.error(f'JSONDecodeError: {e}')
