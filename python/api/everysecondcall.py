#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import logging
import os
import sys
import requests
import json
import sched
import time

path = os.path.dirname(os.path.realpath(__file__))
# logging.basicConfig(filename=f"{path}/access.log", filemode="a", format="%(asctime)s - %(message)s",
#                     datefmt="%d-%b-%y %H:%M:%S", level=logging.DEBUG)
logging.basicConfig(format="%(asctime)s - %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S", stream=sys.stderr, level=logging.DEBUG)

sched = sched.scheduler(time.time, time.sleep)


def run_request(scheduler):

    url = "https://"

    payload = json.dumps({
        "CompanyId": "1",
        "OtherItems": [
            {
                "RequestId": "1",
                "RequestNumber": "1",
                "TransitionId": "1"
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload)
    logging.info(response.status_code)

    # do your stuff
    sched.enter(1, 1, run_request, (scheduler,))


def main():

    sched.enter(1, 1, run_request, (sched,))
    sched.run()


if __name__ == '__main__':
    main()
