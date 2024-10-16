#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.network.aio import NetworkManagementClient


async def main():
    credential = DefaultAzureCredential()
    SUBSCRIPTION_ID = "8aff1e2b-1c08-45f2-94d5-59bdfd6d2176"
    RESOURCE_GROUP = "rg-networking-centralhub-prd"
    PUBLIC_IP_NAME = "VpnGwIp"
    network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)
    public_ip_address = ""
    method = "Dynamic"

    while public_ip_address != "52.169.122.148":

        async_poller = await network_client.public_ip_addresses.begin_create_or_update(
            RESOURCE_GROUP, PUBLIC_IP_NAME, {
                "location": "northeurope",
                "public_ip_allocation_method": method,
            })
        public_ip_address = await async_poller.result()

        match method:
            case "Static":
                print(public_ip_address.ip_address)
                method = "Dynamic"
            case "Dynamic":
                method = "Static"

    await network_client.close()
    await credential.close()


if __name__ == "__main__":
    try:
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(
            main()
        )
        event_loop.close()
    except KeyboardInterrupt:
        pass
