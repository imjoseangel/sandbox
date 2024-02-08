#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import os
import sched
import sys
import time
import uuid
import requests

logging.basicConfig(format="%(asctime)s - %(levelname)-5s - %(name)s - %(message)s",
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

try:
    url = f'{connmap["IngestionEndpoint"]}v2/track'  # type: ignore
    ikey = connmap['InstrumentationKey']  # type: ignore
except KeyError:
    logging.error("Check APPLICATIONINSIGHTS_CONNECTION_STRING "
                  "environment variable. Missing Quotes?")
    sys.exit(1)


appname = os.environ.get('APPNAME', 'Test Application')
location = os.environ.get('LOCATION', 'westeurope')
hostname = os.environ.get('HOSTNAME', 'https://www.example.com')
timesec = os.environ.get('TIMESEC', 60)


def trackavailability(scheduler):
    # schedule the next call first
    scheduler.enter(timesec, 1, trackavailability, (scheduler,))
    currenttime = datetime.utcnow().strftime("%Y-%m-%dT%X.%f0Z")

    try:
        duration = datetime.fromtimestamp(requests.get(
            hostname, timeout=30).elapsed.total_seconds()).strftime("00.00:%M:%S.%f0")
        logging.info(f"Availability for {hostname} - {location} - SUCCESS")
        success = True
    except requests.exceptions.MissingSchema as e:
        logging.error(e)
        sys.exit(1)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        logging.warning(f"Availability for {hostname} - {location} - FAIL")
        duration = "00.00:00:00"
        success = False

    body = {
        "data": {
            "baseData": {
                "ver": 2,
                "id": str(uuid.uuid4()),
                "name": appname,
                "duration": duration,
                "success": success,
                "runLocation": location,
                "message": f"{appname} Availability Test {'Success' if success else 'Fail'}",
                "properties": {}
            },
            "baseType": "AvailabilityData"
        },
        "ver": 1,
        "name": "Microsoft.ApplicationInsights.Metric",
        "time": currenttime,
        "sampleRate": 100,
        "iKey": ikey,
        "flags": 0
    }

    try:
        req = requests.post(url=url, json=body, timeout=30)
        logging.info(req.content.decode("utf-8"))
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        logging.error("Check connectivity. Connection Error")


def main():

    try:
        scheduler = sched.scheduler(time.time, time.sleep)
        logging.info(f"Tracking availability for {hostname} - {location}")
        trackavailability(scheduler)
        scheduler.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
