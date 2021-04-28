#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient


class AzureVMScaleSet():
    def __init__(self, client_id, secret, tenant_id, subscription_id):
        self.subscription_id = subscription_id
        self.credentials = ClientSecretCredential(
            client_id=client_id,
            client_secret=secret,
            tenant_id=tenant_id)

        self.scope = subscription_id
        self.compute_client = ComputeManagementClient(
            credential=self.credentials,
            subscription_id=self.subscription_id
        )

    def run(self):

        vmss = self.compute_client.virtual_machine_scale_set_vms.list(
            "rsg-scaleset", "vmsagents")

        vms = [print(item) for item in vmss]


def main():
    client_id = os.getenv("ARM_CLIENT_ID")
    secret = os.getenv("ARM_CLIENT_SECRET")
    subscription_id = os.getenv("ARM_SUBSCRIPTION_ID")
    tenant_id = os.getenv("ARM_TENANT_ID")

    azure_vms = AzureVMScaleSet(
        client_id, secret, tenant_id, subscription_id)
    azure_vms.run()


if __name__ == '__main__':
    main()
