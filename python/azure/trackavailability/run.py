#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import os
import sys
import tomllib
import uuid
import requests

logging.basicConfig(format="%(asctime)s - %(levelname)-5s - %(name)s - %(message)s",
                    datefmt="%d-%m-%y %H:%M:%S",
                    stream=sys.stdout,
                    level=logging.INFO)

try:
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
except FileNotFoundError:
    logging.error("config.toml file not found")
    sys.exit(1)

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

try:
    location = config['base']['location']
except KeyError:
    logging.error("location key not found on config.toml")
    sys.exit(1)

body = {
    "data": {
        "baseData": {
            "ver": 2,
            "id": str(uuid.uuid4()),
            "name": "Microsoft Support Sample Webtest Result",
            "duration": "00.00:00:10",
            "success": True,
            "runLocation": location,
            "message": "Sample Webtest Result",
            "properties": {}
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
        print(body)
        req = requests.post(url=url, json=body, timeout=30)
        logging.info(req.content)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        logging.error("Check connectivity. Connection Error")


if __name__ == '__main__':
    main()
