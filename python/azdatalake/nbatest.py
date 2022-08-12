#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import asyncio
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
        logger.error(e)
        return f"Error: {e}"

    except HttpResponseError as e:
        logger.error(e)
        return f"Error: {e}"

    except ValueError as e:
        logger.error(e)
        return f"Error: {e}"


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
        logger.error(e)
        return f"Error: {e}"

    except ValueError as e:
        logger.error(e)
        return f"Error: {e}"


def create_directory(file_system_client):
    try:
        file_system_client.create_directory(directoryName)

    except ResourceExistsError as e:
        logger.error(e)
        return f"Error: {e}"

    except HttpResponseError as e:
        logger.error(e)
        return f"Error: {e}"

    except ValueError as e:
        logger.error(e)
        return f"Error: {e}"


def upload_file_to_directory_bulk(service_client, filename):
    try:

        file_system_client = service_client.get_file_system_client(
            file_system=containerName)

        directory_client = file_system_client.get_directory_client(
            directoryName)

        file_client = directory_client.get_file_client(filename)

        local_file = open(filename, "r", encoding="utf-8")

        file_contents = local_file.read()
        file_client.upload_data(file_contents, overwrite=True)

        logger.info(f"uploaded {filename} to {directoryName}")

    except ResourceExistsError as e:
        logger.error(e)

    except HttpResponseError as e:
        logger.error(e)

    except ValueError as e:
        logger.error(e)


async def get_json(service_client):

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
            pdObj.to_csv(f"{nbadate}.csv", index=False)

            upload_file_to_directory_bulk(
                service_client, filename=f"{nbadate}.csv")

            os.remove(f"{nbadate}.csv")

            logger.info(pdObj)

        except ValueError:
            pass


def main():

    try:

        client = initialize_storage_account_ad(
            storageAccountName, clientid, clientsecret, tenantid)
        file_system = create_file_system(client)
        create_directory(file_system)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(get_json(client))
        loop.close()

    except KeyError as e:
        logger.error(e)

    except TypeError as e:
        logger.error(e)

    except ValueError as e:
        logger.error(e)

    except AttributeError as e:
        logger.error(e)


if __name__ == '__main__':
    main()
