#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import json
import os
import requests
import sys
import urllib
import boto3


# Step 1: Authenticate user in your own identity system.

# Step 2: Using the access keys for an IAM user in your AWS account,
# call "AssumeRole" to get temporary access keys for the federated user

# Note: Calls to AWS STS AssumeRole must be signed using the access key ID
# and secret access key of an IAM user or using existing temporary credentials.
# The credentials can be in Amazon EC2 instance metadata, in environment variables,
# or in a configuration file, and will be discovered automatically by the
# client('sts') function. For more information, see the Python SDK docs:
# http://boto3.readthedocs.io/en/latest/reference/services/sts.html
# http://boto3.readthedocs.io/en/latest/reference/services/sts.html#STS.Client.assume_role

def main():
    """
    Main function
    """
    sts_connection = boto3.client('sts')

    assumed_role_object = sts_connection.assume_role(
        RoleArn=f"arn:aws:iam::{os.environ.get('AWS_ACCOUNT_ID')}:role/ROLE-NAME",
        RoleSessionName="AssumeRoleSession",
    )


if __name__ == '__main__':
    main()
