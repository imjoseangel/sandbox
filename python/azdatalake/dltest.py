#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os

from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient


clientid = os.getenv('AZURE_CLIENT_ID')
clientsecret = os.getenv('AZURE_CLIENT_SECRET')
tenantid = os.getenv('AZURE_TENANT_ID')
storageAccountName = os.getenv('AZURE_STORAGE_NAME')


def initialize_storage_account_ad(storage_account_name, client_id, client_secret, tenant_id):

    try:
        global service_client

        credential = ClientSecretCredential(
            tenant_id, client_id, client_secret)

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=credential)

    except Exception as e:
        print(e)


def create_file_system():
    try:
        global file_system_client

        file_system_client = service_client.create_file_system(
            file_system="my-file-system")

    except Exception as e:
        print(e)


def create_directory():
    try:
        file_system_client.create_directory("my-directory")

    except Exception as e:
        print(e)


def main():

    initialize_storage_account_ad(
        storageAccountName, clientid, clientsecret, tenantid)


if __name__ == '__main__':
    main()
