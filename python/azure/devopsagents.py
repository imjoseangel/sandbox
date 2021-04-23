#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass
import argparse
import os
import requests
import json
from flask import Flask

FALLBACK_ARGS = dict(organization='inc', poolid='1')


@dataclass
class RunJob:

    secret = os.getenv("ADV_TOKEN")
    organization = os.getenv("ADV_ORGANIZATION")
    poolid = os.getenv("ADV_POOLID")

    def __post_init__(self):
        pass

    def get_running(self):

        headers = {"Authorization": f"Basic {self.secret}"}
        url = f"https://dev.azure.com/{self.organization}/_apis/distributedtask/pools/{self.poolid}/jobrequests"

        try:
            response = requests.request("GET", url, headers=headers)
        except NameError as e:
            print(e)

        if response.ok:
            data = json.loads(response.text).get("value")
            results = [item for item in data if "result" not in item]
            return {'runningjobs': len(results)}

        return {'runningjobs': 0}


app = Flask(__name__)
jobrequests = RunJob()


@app.route('/')
def index():
    return jobrequests.get_running()
