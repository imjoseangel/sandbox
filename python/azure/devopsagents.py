#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass, field
from os.path import abspath, dirname, normpath
import base64
import json
import os
import sys
from waitress import serve
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
                results = self.get_data(data)
                return {'runningjobs': results}
            except json.JSONDecodeError as e:
                print(e)

        return {'runningjobs': 0}

    def get_data(self, data):
        results = len([item for item in data if "result" not in item])
        return results


app = Flask(__name__)
jobrequests = RunJob()


@app.route('/')
def home():
    print(jobrequests.get_running(), file=sys.stderr)
    return jobrequests.get_running()


def main():
    serve(app)


if __name__ == '__main__':
    main()
