#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import configparser
import json
import logging
import os
import sys
import requests

import msrest
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient


class AzureVMScaleSet():
    def __init__(self, client_id, secret, tenant_id, subscription_id):

        logging.basicConfig(
            format="%(asctime)s %(levelname)s: %(message)s",
            level=logging.INFO,
            datefmt="%d-%b-%y %H:%M:%S",
            stream=sys.stderr,
        )

        self.subscription_id = subscription_id
        self.data = 0

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

        try:
            self.resource_group = self._config['DEFAULT']['resource_group']
            self.scaleset = self._config['DEFAULT']['scaleset']
        except KeyError as e:
            logging.error(f'DEFAULT {e} key not defined in config.ini')

        try:
            self.url = self._config['api']['url']
            self.value = self._config['api']['valuelocation']
        except KeyError as e:
            logging.error(f'api {e} key not defined in config.ini')

    def workpath(self):
        """ Return Work Path """
        return self._work_path

    def path(self):
        """ Returns Path """
        return self._path

    def config(self):
        """ Returns Config """
        return self._config

    def get_urldata(self):
        try:
            response = requests.request("GET", self.url)

            if response.ok:
                try:
                    self.data = json.loads(response.text).get(self.value)
                except json.JSONDecodeError as e:
                    logging.error(e)

        except requests.exceptions.ConnectionError as e:
            logging.error(e)

        except ValueError:
            logging.error(e)

        except NameError as e:
            logging.error(e)

        except AttributeError as e:
            logging.error(e)

    def run(self):

        self.get_urldata()

        try:
            vMachineScaleSet = self.compute_client.virtual_machine_scale_sets.get(
                self.resource_group, self.scaleset)

            scale = self.compute_client.virtual_machine_scale_sets.begin_create_or_update(
                self.resource_group, self.scaleset,
                {'Location': vMachineScaleSet.location,
                 'sku': {'name': vMachineScaleSet.sku.name,
                         'capacity': self.data,
                         'tier': vMachineScaleSet.sku.tier}})

            logging.info(scale.result())

        except AttributeError as e:
            logging.error(e)


def main():
    client_id = os.getenv("ARM_CLIENT_ID")
    secret = os.getenv("ARM_CLIENT_SECRET")
    subscription_id = os.getenv("ARM_SUBSCRIPTION_ID")
    tenant_id = os.getenv("ARM_TENANT_ID")

    try:
        azure_vms = AzureVMScaleSet(
            client_id, secret, tenant_id, subscription_id)
        azure_vms.run()
    except msrest.exceptions.SerializationError as e:
        logging.error(e)
    except ValueError as e:
        logging.error(e)


if __name__ == '__main__':
    main()
