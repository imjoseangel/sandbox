#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import asyncio
import concurrent.futures
import logging
import sys
import os
import requests

logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S", stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger('httprequests')
logging.getLogger("chardet.charsetprober").disabled = True

benchuri = os.environ.get('BENCHURI', 'http://www.example.com')


async def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

        fetch = asyncio.get_event_loop()
        futures = [
            fetch.run_in_executor(
                executor,
                requests.get,
                benchuri
            )
            for i in range(20)
        ]
        for request in await asyncio.gather(*futures):
            logger.info(request)

if __name__ == '__main__':

    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
