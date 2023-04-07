#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from akamai.edgegrid import EdgeGridAuth
from urllib.parse import urljoin

# this is the "host" value from your credentials file
baseurl = 'https://bu'
s = requests.Session()
s.auth = EdgeGridAuth(
    client_token='ct',
    client_secret='cs',
    access_token='at'
)

result = s.get(urljoin(
    baseurl, '/reporting-api/v1/reports/traffic-by-response/versions/1/report-data?start=2023-03-01T00%3A00%3A00Z&end=2023-04-01T00%3A00%3A00Z'))
print(result.status_code)
print(result.json())
