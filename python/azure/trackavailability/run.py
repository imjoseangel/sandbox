#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This code sends availability test every minute (default) to
Azure Application Insights."""

from datetime import datetime
import asyncio
import logging
import os
import sched
import sys
import time
import uuid
import requests
import yaml

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


async def trackavailability(appname, location, urlname):
    """ Track Function
    This function contains the main logic for the Availability Test
    sent to Azure Application Insights"""
    currenttime = datetime.utcnow().strftime("%Y-%m-%dT%X.%f0Z")

    try:
        duration = datetime.fromtimestamp(requests.get(
            urlname, timeout=30,
            verify=False).elapsed.total_seconds()).strftime("00.00:%M:%S.%f0")
        logging.info("Availability for %s - %s - SUCCESS",
                     urlname, location)
        success = True
    except requests.exceptions.MissingSchema as e:
        logging.error(e)
        sys.exit(1)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        logging.warning("Availability for %s - %s - FAIL",
                        urlname, location)
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
        logging.error("Connection Error")


def main():
    """ Main Function """

    try:
        with open('config.yaml', encoding='UTF-8') as configfile:
            config = yaml.safe_load(configfile)
    except FileNotFoundError:
        logging.error("File `config.yaml` not found")
        sys.exit(1)

    for application in config['applications']:

        try:

            appname = application['name']
            location = application['location']
            urlname = application['url']

            logging.info(
                "Tracking availability for %s - %s", urlname, location)

            loop = asyncio.get_event_loop()
            task = loop.create_task(
                trackavailability(appname, location, urlname))

            try:
                loop.run_until_complete(task)
            except asyncio.CancelledError:
                pass

        except KeyboardInterrupt:
            logging.info("Exiting...")


if __name__ == '__main__':
    main()
