#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import requests
import json


def main():
    secret = os.getenv("ADV_TOKEN")
    organization = os.getenv("ADV_ORG")
    poolid = os.getenv("ADV_POOLID")

    headers = {"Authorization": f"Basic {secret}"}
    url = f"https://dev.azure.com/{organization}/_apis/distributedtask/pools/{poolid}/jobrequests"

    try:
        response = requests.request("GET", url, headers=headers)
    except NameError as e:
        print(e)

    if response.ok:
        data = json.loads(response.text)

        data = data.get("value")

        x = [item for item in data if "result" not in item]
        print(json.dumps(x, indent=4, sort_keys=True))

        print(len(x))
        # print(json.dumps(data, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
