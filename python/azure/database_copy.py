#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from azure.mgmt.sql import SqlManagementClient
from azure.identity import DefaultAzureCredential


# PREREQUISITES
#    pip install azure-identity
#    pip install azure-mgmt-sql


def main():

    logging.basicConfig(format="%(asctime)s - %(levelname)-8s - %(name)s - %(message)s",
                        datefmt="%d-%m-%y %H:%M:%S",
                        stream=sys.stdout,
                        level=logging.INFO)

    subscription_id = "00000000-1111-2222-3333-444444444444"
    srcversion = "v0.0.1"
    dstversion = "v0.0.2"
    resource_group = "sbx-neu-dev-jam-rg"
    server_name = "sbx-neu-dev-jam-sql"
    database_name = "sbx-neu-dev-jam-sql"
    location = "northeurope"

    client = SqlManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id,
    )

    response = client.databases.begin_create_or_update(
        resource_group_name=resource_group,
        server_name=server_name,
        database_name=f"{database_name}_{dstversion}",
        parameters={
            "location": location,
            "properties": {
                "createMode": "Copy",
                "sourceDatabaseId": f"/subscriptions/{subscription_id}/"
                f"resourceGroups/{resource_group}/providers/Microsoft.Sql/"
                f"servers/{server_name}/databases/{database_name}_{srcversion}",
            },
            "sku": {"name": "Standard", "tier": "Standard", "capacity": 20},
        },  # type: ignore
    ).result()  # type: ignore

    logging.info(response)


# x-ms-original-file: specification/sql/resource-manager/Microsoft.Sql/preview/
# 2023-02-01-preview/examples/CreateDatabaseCopyMode.json

if __name__ == "__main__":
    main()
