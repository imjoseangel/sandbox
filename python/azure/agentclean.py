#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import base64

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
    f"_apis/distributedtask/pools/{poolid}/jobrequests")
