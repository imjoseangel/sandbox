#!/usr/bin/env python
# -*- coding: utf-8 -*-

from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.core.exceptions import ClientAuthenticationError


def subscription_list():

    credential = DefaultAzureCredential()

    subscription_client = SubscriptionClient(credential)
    sub_list = subscription_client.subscriptions.list()
    column_width = 40

    print("Subscription ID".ljust(column_width) + "Display name")
    print("-" * (column_width * 2))

    try:
        for group in list(sub_list):
            print(f'{group.subscription_id:<{column_width}}{group.display_name}')
    except ClientAuthenticationError as e:
        pass


def main():
    print(subscription_list())


if __name__ == '__main__':
    main()
