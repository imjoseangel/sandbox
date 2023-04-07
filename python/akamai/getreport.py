#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from urllib.parse import urljoin
import requests
from akamai.edgegrid import EdgeGridAuth

# this is the "host" value from your credentials file
baseurl = 'https://host'
s = requests.Session()
s.auth = EdgeGridAuth(
    client_token='token',
    client_secret='secret',
    access_token='token'
)

result = s.get(urljoin(
    baseurl, '/reporting-api/v1/reports/traffic-by-response/versions/1/report-data?start=2023-04-01T00%3A00%3A00Z&end=2023-04-06T00%3A00%3A00Z'))
print(result.status_code)
print(json.dumps(result.json(), sort_keys=True, indent=4))
