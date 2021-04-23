#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass
import os
import json
import requests
from flask import Flask

FALLBACK_ARGS = dict(organization='inc', poolid='1')


@dataclass
class RunJob:

    secret: str = os.getenv("ADV_TOKEN", "")
    organization: str = os.getenv("ADV_ORGANIZATION", "inc")
    poolid: str = os.getenv("ADV_POOLID", "1")

    def __post_init__(self):
        pass

    def get_running(self):

        headers = {"Authorization": f"Basic {self.secret}"}
        url = (
            f"https://dev.azure.com/{self.organization}/"
            f"_apis/distributedtask/pools/{self.poolid}/jobrequests")

        try:
            response = requests.request("GET", url, headers=headers)
        except NameError as e:
            print(e)

        if response.ok:
            try:
                data = json.loads(response.text).get("value")
                results = [item for item in data if "result" not in item]
                return {'runningjobs': len(results)}
            except json.JSONDecodeError as e:
                pass

        return {'runningjobs': 0}


app = Flask(__name__)
jobrequests = RunJob()


@app.route('/')
def index():
    return jobrequests.get_running()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
