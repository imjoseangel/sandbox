#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import configparser
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

        self._path = os.path.dirname(os.path.realpath(__file__))
        self._work_path = os.path.dirname(self._path)
        self._config = configparser.ConfigParser()
        self._config.read(self._path + '/{0}'.format('config.ini'))

        self.resource_group = self._config['DEFAULT']['resource_group']
        self.scaleset = self._config['DEFAULT']['scaleset']

    def workpath(self):
        """ Return Work Path """
        return self._work_path

    def path(self):
        """ Returns Path """
        return self._path

    def config(self):
        """ Returns Config """
        return self._config

    def run(self):

        vMachineScaleSet = self.compute_client.virtual_machine_scale_sets.get(
            self.resource_group, self.scaleset)

        self.compute_client.virtual_machine_scale_sets.begin_create_or_update(
            self.resource_group, self.scaleset,
            {'Location': vMachineScaleSet.location,
             'sku': {'name': vMachineScaleSet.sku.name, 'capacity': 0, 'tier': vMachineScaleSet.sku.tier}})


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
