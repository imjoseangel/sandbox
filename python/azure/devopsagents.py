#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass
import os
import requests
import json


@dataclass
class RunJob:

    secret = os.getenv("ADV_TOKEN")
    organization: str
    poolid: str

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
            return len(results)

        return 0


def main():

    jobrequests = RunJob("raet", "63")
    print(jobrequests.get_running())


if __name__ == '__main__':
    main()
