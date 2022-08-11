#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import logging

from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError


clientid = os.getenv('AZURE_CLIENT_ID')
clientsecret = os.getenv('AZURE_CLIENT_SECRET')
tenantid = os.getenv('AZURE_TENANT_ID')
storageAccountName = os.getenv('AZURE_STORAGE_NAME')


logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%d-%b-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def initialize_storage_account_ad(storage_account_name, client_id, client_secret, tenant_id):

    try:
        credential = ClientSecretCredential(
            tenant_id, client_id, client_secret)

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=credential)

        logger.info(f"connected to {service_client.account_name}")

        return service_client

    except ResourceNotFoundError as e:
        print(e)


def create_file_system(service_client):
    try:
        file_system_client = service_client.create_file_system(
            file_system="my-file-system")

        return file_system_client

    except ResourceExistsError as e:
        print(e)


def create_directory(file_system_client):
    try:
        file_system_client.create_directory("my-directory")

    except ResourceExistsError as e:
        print(e)


def main():

    client = initialize_storage_account_ad(
        storageAccountName, clientid, clientsecret, tenantid)
    file_system = create_file_system(client)
    create_directory(file_system)


if __name__ == '__main__':
    main()
