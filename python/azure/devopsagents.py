#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass
import argparse
import os
import requests
import json

FALLBACK_ARGS = dict(organization='raet', poolid='1')


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

    def parse_arguments(self):
        '''argument parser'''
        parser = argparse.ArgumentParser(
            description='Get Azure DevOps Job Requests')
        parser.add_argument('--organization',
                            '-o',
                            help='organization. default: "raet"',
                            default=FALLBACK_ARGS['organization'])
        parser.add_argument(
            '--poolid',
            '-p',
            help='Pool id number. default: "1"',
            default=FALLBACK_ARGS['poolid'])

        self.args = parser.parse_args()


def main():

    jobrequests = RunJob("raet", "63")
    print(jobrequests.get_running())


if __name__ == '__main__':
    main()
