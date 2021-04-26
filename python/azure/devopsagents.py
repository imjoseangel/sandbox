#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass, field
import base64
import json
import logging
import os
import sys
import requests
from flask import Flask


@dataclass
class RunJob:

    auth: str = field(default="")
    encodeauth: str = field(default="")
    headers: dict = field(default_factory=dict)
    secret: str = os.getenv("ADV_TOKEN", "")
    organization: str = os.getenv("ADV_ORG", "inc")
    poolid: str = os.getenv("ADV_POOL", "1")

    def __post_init__(self):
        self.authencode()

    def authencode(self):

        self.auth = f':{self.secret}'
        self.encodeauth = base64.b64encode(self.auth.encode('utf-8'))

        self.headers = {
            'Authorization':
            'Basic {0}'.format(self.encodeauth.decode('utf-8'))
        }

    def get_running(self):

        url = (
            f"https://dev.azure.com/{self.organization}/"
            f"_apis/distributedtask/pools/{self.poolid}/jobrequests")

        try:
            response = requests.request("GET", url, headers=self.headers)
        except NameError as e:
            print(e)

        if response.ok:
            try:
                data = json.loads(response.text).get("value")
                results = len([item for item in data if "result" not in item])
                return {'runningjobs': results}
            except json.JSONDecodeError as e:
                print(e)

        return {'runningjobs': 0}


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
jobrequests = RunJob()


@app.route('/')
def index():
    print(jobrequests.get_running(), file=sys.stderr)
    return jobrequests.get_running()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)