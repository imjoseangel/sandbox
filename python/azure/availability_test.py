#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import os
import requests
import sys

logging.basicConfig(format="%(asctime)s - %(levelname)-6s - %(name)s - %(message)s",
                    datefmt="%d-%m-%y %H:%M:%S",
                    stream=sys.stdout,
                    level=logging.INFO)

try:
    connectionstring = os.environ['APPLICATIONINSIGHTS_CONNECTION_STRING']
except KeyError:
    logging.error("Setup APPLICATIONINSIGHTS_CONNECTION_STRING "
                  "environment variable")
    sys.exit(1)

try:
    connmap = dict(map(lambda item: item.split(
        '='), connectionstring.split(';')))  # type: ignore
except ValueError:
    logging.error("Check APPLICATIONINSIGHTS_CONNECTION_STRING "
                  "environment variable. Empty?")
    sys.exit(1)

time = datetime.utcnow().strftime("%Y-%m-%dT%X.%f0Z")

try:
    url = f'{connmap["IngestionEndpoint"]}v2/track'  # type: ignore
    ikey = connmap['InstrumentationKey']  # type: ignore
except KeyError:
    logging.error("Check APPLICATIONINSIGHTS_CONNECTION_STRING "
                  "environment variable. Missing Quotes?")
    sys.exit(1)

body = {
    "data": {
        "baseData": {
            "ver": 2,
            "id": "SampleRunId",
            "name": "Microsoft Support Sample Webtest Result",
            "duration": "00.00:00:10",
            "success": True,
            "runLocation": "West Europe",
            "message": "Sample Webtest Result",
            "properties": {
                "Sample Property": "Sample Value"
            }
        },
        "baseType": "AvailabilityData"
    },
    "ver": 1,
    "name": "Microsoft.ApplicationInsights.Metric",
    "time": time,
    "sampleRate": 100,
    "iKey": ikey,
    "flags": 0
}


def main():
    try:
        req = requests.post(url=url, json=body, timeout=30)
        logging.info(req.content)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        logging.error("Check connectivity. Connection Error")


if __name__ == '__main__':
    main()
