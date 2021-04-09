#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import pandas as pd
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.consumption import ConsumptionManagementClient


class AzureBillingCollector():

    def __init__(self, client_id, secret, tenant_id, subscription_id):
        self._subscription_id = subscription_id
        self._credentials = ServicePrincipalCredentials(
            client_id=client_id,
            secret=secret,
            tenant=tenant_id)

        self.scope = "subscriptions/" + subscription_id
        self.consumption_client = ConsumptionManagementClient(
            credentials=self._credentials,
            subscription_id=self._subscription_id
        )

    def run_by_date(self, date_filter):
        usages = self.consumption_client.usage_details.list(
            self.scope, filter=date_filter)
        self.printresults(usages)

    def run_by_billing_period(self, billing_period):
        scope = self.scope + "/providers/Microsoft.Billing/billingPeriods/" + billing_period
        usages = self.consumption_client.usage_details.list(scope)
        self.printresults(usages)

    def printresults(self, usages):
        results = []
        for item in usages:
            results.append(item.as_dict())

        pd.set_option('display.max_columns', None)
        dataframe = pd.DataFrame(results).to_csv('out.csv')


def run_example_by_datefilter(client_id, secret, tenant_id, subscription_id):
    azure_usage = AzureBillingCollector(
        client_id, secret, tenant_id, subscription_id)
    date_filter = "properties/usageStart ge '2021-02-26' AND properties/usageStart lt '2021-02-27'"
    print("Get data by date range '2021-04-07' and '2021-04-27'")
    azure_usage.run_by_date(date_filter)
    print("Done")


def run_example_by_billingperiod(client_id, secret, tenant_id, subscription_id):
    azure_usage = AzureBillingCollector(
        client_id, secret, tenant_id, subscription_id)
    print("Get data by billing period 202104")
    azure_usage.run_by_billing_period("202104")
    print("Done")


def main():

    client_id = os.getenv("ARM_CLIENT_ID")
    secret = os.getenv("ARM_CLIENT_SECRET")
    subscription_id = os.getenv("ARM_SUBSCRIPTION_ID")
    tenant_id = os.getenv("ARM_TENANT_ID")
    # billingPeriodName = '202103'

    # run_example_by_datefilter(client_id, secret, tenant_id, subscription_id)
    run_example_by_billingperiod(client_id, secret, tenant_id, subscription_id)
    # consumption = AzureBillingCollector(
    #     client_id, secret, tenant_id, subscription_id)

    # pages = consumption.consumption_client.usage_details.list_by_billing_period(
    #     billing_period_name=billingPeriodName, expand='properties/meterDetails,properties/additionalProperties')

    # first_page = pages.advance_page()
    # output = list(pages)

    # for item in pages:
    #     print(item)
    # print(f"{item.product} {item.pretax_cost}")
    # print(item.meter_details)


if __name__ == '__main__':
    main()
