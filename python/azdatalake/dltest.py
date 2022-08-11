#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import datetime
import json
import logging
import requests
import pandas as pd

from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError, HttpResponseError


clientid = os.getenv('AZURE_CLIENT_ID')
clientsecret = os.getenv('AZURE_CLIENT_SECRET')
tenantid = os.getenv('AZURE_TENANT_ID')
storageAccountName = os.getenv('AZURE_STORAGE_NAME')
containerName = "sports"
directoryName = "nba"


logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%d-%b-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def initialize_storage_account_ad(storage_account_name, client_id,
                                  client_secret, tenant_id):

    try:
        credential = ClientSecretCredential(
            tenant_id, client_id, client_secret)

        service_client = DataLakeServiceClient(
            account_url=f"https://{storage_account_name}.dfs.core.windows.net",
            credential=credential)

        logger.info(f"connected to {service_client.account_name}")

        return service_client

    except ResourceNotFoundError as e:
        logger.info(e)

        return None

    except HttpResponseError as e:
        logger.info(e)

        return None


def create_file_system(service_client):
    try:
        file_system_client = service_client.create_file_system(
            file_system=containerName)

        return file_system_client

    except ResourceExistsError:
        file_system_client = service_client.get_file_system_client(
            file_system=containerName)

        return file_system_client

    except HttpResponseError as e:
        logger.info(e)

        return None


def create_directory(file_system_client):
    try:
        file_system_client.create_directory(directoryName)

    except ResourceExistsError as e:
        logger.info(e)

    except HttpResponseError as e:
        logger.info(e)


def get_json():

    mainjsn = "https://data.nba.net/data/10s/prod/v1/calendar.json"

    nbanet = requests.get(mainjsn)
    nbadates = json.loads(nbanet.content)

    for nbadate in nbadates:

        try:
            datetime.datetime.strptime(nbadate, '%Y%m%d')

            scoreboard = f"https://data.nba.net/10s/prod/v1/{nbadate}/scoreboard.json"
            gameday = requests.get(scoreboard)
            games = json.loads(gameday.content)

            pdObj = pd.read_json(json.dumps(games['games']))
            csvData = pdObj.to_csv(index=False)

            logger.info(csvData)

        except ValueError:
            pass


def main():

    # client = initialize_storage_account_ad(
    #     storageAccountName, clientid, clientsecret, tenantid)
    # file_system = create_file_system(client)
    # create_directory(file_system)

    get_json()


if __name__ == '__main__':
    main()
